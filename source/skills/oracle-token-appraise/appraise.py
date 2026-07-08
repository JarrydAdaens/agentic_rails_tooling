# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "tiktoken",
# ]
# ///

"""Appraise a file's token cost without reading its content into the caller's context.

Two estimation sources, in preference order:

1. Oracle Server's `POST /v1/estimate` (M3-S1 contract record §6.3) when reachable —
   model-aware tokenizer selection, honest tokenizerMatch labeling. The server reads the
   file itself (paths-only request); this script never sends file content over the wire.
2. Local `tiktoken` `cl100k_base` counting (this skill's original behavior) when the server
   is unreachable, or rejects the request (e.g. a path it cannot see or read).

In both modes, only the summary printed below ever reaches the calling agent's context —
never the file's raw content.
"""

import json
import os
import sys
import urllib.error
import urllib.request

import tiktoken

DEFAULT_SERVER_URL = "http://localhost:5140"
DEFAULT_WINDOW = 40000
DEFAULT_TARGET_MODEL = "claude"

# Health probes answer "is anyone there?" -- keep them snappy so an absent server
# falls back to the local path fast instead of hanging the CLI.
HEALTH_TIMEOUT_SECONDS = 1.5
REQUEST_TIMEOUT_SECONDS = 5.0

# Verdict banding, inherited verbatim from this skill's original local classifier and
# shared with the server's ContextWindowVerdict (M3-S1 contract record §6.3, §7.5):
# SMALL < 10% <= MEDIUM < 40% <= LARGE < 80% <= HUGE.
VERDICT_DESCRIPTIONS = {
    "SMALL": "SMALL  — safe to read whole file",
    "MEDIUM": "MEDIUM — read whole file with care",
    "LARGE": "LARGE  — consider reading in sections",
    "HUGE": "HUGE   — do not read whole file; summarise or chunk",
}

# Network/parsing failures that mean "the server didn't give us a usable answer" --
# every one of these triggers the local fallback rather than crashing the script.
SERVER_FAILURE_EXCEPTIONS = (
    urllib.error.URLError,
    TimeoutError,
    OSError,
    ValueError,
    KeyError,
)


def classify_verdict(usage_percent):
    """Classify a window-usage percentage into SMALL/MEDIUM/LARGE/HUGE."""
    if usage_percent < 10:
        return "SMALL"
    if usage_percent < 40:
        return "MEDIUM"
    return "LARGE" if usage_percent < 80 else "HUGE"


def server_base_url(env=None):
    """Resolve the Oracle Server base URL from ORACLE_SERVER_URL, else the localhost default."""
    env = os.environ if env is None else env
    raw = env.get("ORACLE_SERVER_URL", "").strip()
    return (raw or DEFAULT_SERVER_URL).rstrip("/")


def probe_health(base_url, timeout=HEALTH_TIMEOUT_SECONDS, opener=None):
    """Probe GET /health. Returns True if the server answers 200, False on any failure."""
    opener = urllib.request.urlopen if opener is None else opener
    try:
        with opener(f"{base_url}/health", timeout=timeout) as response:
            return response.status == 200
    except SERVER_FAILURE_EXCEPTIONS:
        return False


def request_estimate(base_url, absolute_path, target_model, window, timeout=REQUEST_TIMEOUT_SECONDS, opener=None):
    """POST /v1/estimate for one file path. Raises on any failure -- callers decide the fallback.

    Sends only the file's path, never its content (SK-2's hard invariant, M3-S1 contract
    record §6.3) -- the server reads the file itself, and must therefore be able to see the
    same filesystem (the same-machine assumption documented in SKILL.md).
    """
    opener = urllib.request.urlopen if opener is None else opener
    body = json.dumps(
        {
            "targetModel": target_model,
            "paths": [absolute_path],
            "window": window,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/v1/estimate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with opener(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def appraise_file(file_path, window=DEFAULT_WINDOW, target_model=DEFAULT_TARGET_MODEL, env=None, opener=None):
    """Appraise one file's token cost. Returns a report dict; raises FileNotFoundError/OSError
    on unreadable input. Never returns file content -- only counts and labels."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    file_size = os.path.getsize(file_path)
    char_count = len(text)
    line_count = text.count("\n") + 1

    base_url = server_base_url(env)
    server_report = None
    fallback_reason = None

    if probe_health(base_url, opener=opener):
        try:
            absolute_path = os.path.abspath(file_path)
            server_result = request_estimate(base_url, absolute_path, target_model, window, opener=opener)
            # Field extraction stays inside this guard: a 200 response with missing or
            # renamed fields (or an unknown verdict token) must fall back, not crash.
            server_report = {
                "source": f"Oracle Server (targetModel={target_model})",
                "tokenizer_label": (
                    f"{server_result['tokenizer']['id']} ({server_result['tokenizer']['tokenizerMatch']})"
                ),
                "token_count": server_result["totalTokens"],
                "usage_percent": server_result["usagePercent"],
                "verdict": VERDICT_DESCRIPTIONS[server_result["verdict"]],
            }
        except SERVER_FAILURE_EXCEPTIONS as error:
            fallback_reason = str(error) or type(error).__name__
    else:
        fallback_reason = "server unreachable"

    if server_report is not None:
        source = server_report["source"]
        tokenizer_label = server_report["tokenizer_label"]
        token_count = server_report["token_count"]
        usage_percent = server_report["usage_percent"]
        verdict_description = server_report["verdict"]
    else:
        enc = tiktoken.get_encoding("cl100k_base")
        token_count = len(enc.encode(text))
        usage_percent = (token_count / window) * 100
        verdict_description = VERDICT_DESCRIPTIONS[classify_verdict(usage_percent)]
        source = f"local tiktoken ({fallback_reason})"
        tokenizer_label = "tiktoken:cl100k_base"

    return {
        "file_path": file_path,
        "file_size": file_size,
        "line_count": line_count,
        "char_count": char_count,
        "source": source,
        "tokenizer_label": tokenizer_label,
        "token_count": token_count,
        "window": window,
        "usage_percent": usage_percent,
        "verdict": verdict_description,
    }


def format_report(report):
    """Render an appraisal report dict as the skill's printed summary."""
    lines = [
        f"File:       {os.path.basename(report['file_path'])}",
        f"Size:       {report['file_size']:,} bytes",
        f"Lines:      {report['line_count']:,}",
        f"Characters: {report['char_count']:,}",
        f"Source:     {report['source']}",
        f"Tokenizer:  {report['tokenizer_label']}",
        f"Tokens:     {report['token_count']:,}",
        f"Window:     {report['window']:,} tokens",
        f"Usage:      {report['usage_percent']:.1f}%",
        f"Verdict:    {report['verdict']}",
    ]
    return "\n".join(lines)


def parse_args(argv):
    """Parse the CLI's minimal flag set: positional file path, --window N, --model NAME."""
    if len(argv) < 1:
        return None

    file_path = argv[0]

    window = DEFAULT_WINDOW
    if "--window" in argv:
        idx = argv.index("--window")
        if idx + 1 < len(argv):
            window = int(argv[idx + 1])

    target_model = DEFAULT_TARGET_MODEL
    if "--model" in argv:
        idx = argv.index("--model")
        if idx + 1 < len(argv):
            target_model = argv[idx + 1]

    return file_path, window, target_model


def main():
    parsed = parse_args(sys.argv[1:])
    if parsed is None:
        print("Usage: appraise.py <file_path> [--window N] [--model TARGET_MODEL]")
        sys.exit(1)

    file_path, window, target_model = parsed

    try:
        report = appraise_file(file_path, window=window, target_model=target_model)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)
    except OSError as error:
        print(f"Error reading file: {error}")
        sys.exit(1)

    print(format_report(report))


if __name__ == "__main__":
    main()
