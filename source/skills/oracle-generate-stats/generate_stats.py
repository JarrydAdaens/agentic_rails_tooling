# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "tiktoken",
# ]
# ///

import sys
import os
import json
import re
import tiktoken
from datetime import datetime, timezone
from pathlib import Path


# Sidecar schema v2 (Oracle M3-S6): adds schema_version and precision to the v1
# fields (file, updated, size_bytes, lines, chars, tokens, tokenizer). v1 sidecars
# (no schema_version key) are never read by this script -- regeneration overwrites
# them wholesale, which upgrades them to v2.
SIDECAR_SCHEMA_VERSION = 2

# Ledger-level precision taxonomy, a closed set per the Oracle M3-S1 API contract
# decision record (section 5). Sidecar counts are always "estimated" -- they tokenize
# content that was never sent to a model. Stamp precision defaults to "reported" --
# the producing skill passes a cost its source tool actually measured.
VALID_PRECISIONS = {"reported", "delta", "estimated"}
SIDECAR_PRECISION = "estimated"
DEFAULT_STAMP_PRECISION = "reported"

# When the producer's cost comes from its provider's own accounting (ccusage etc.),
# no local tokenizer produced the number -- name the source honestly instead.
DEFAULT_STAMP_TOKENIZER = "provider-reported"

STAMP_START = "<!-- oracle:cost-stamp:start -->"
STAMP_END = "<!-- oracle:cost-stamp:end -->"
STAMP_PATTERN = re.compile(
    re.escape(STAMP_START) + r".*?" + re.escape(STAMP_END) + r"\n?",
    re.DOTALL,
)

MARKDOWN_EXTENSIONS = {".md", ".markdown"}


SKIP_EXTENSIONS = {
    ".stats",
    ".pyc", ".pyo", ".pyd",
    ".exe", ".dll", ".so", ".dylib",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
    ".pdf", ".zip", ".tar", ".gz", ".7z", ".rar",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    ".db", ".sqlite", ".lock",
}

SKIP_DIRS = {
    ".git", ".hg", ".svn",
    "node_modules", "__pycache__",
    ".venv", "venv", ".env",
}


def should_skip(path: Path) -> bool:
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return True
    if path.name.startswith("."):
        return True
    return False


def collect_files(path: Path) -> list[Path]:
    files = []
    if path.is_file():
        if not should_skip(path):
            files.append(path)
    elif path.is_dir():
        for item in sorted(path.rglob("*")):
            if not item.is_file():
                continue
            if any(part in SKIP_DIRS for part in item.parts):
                continue
            if should_skip(item):
                continue
            files.append(item)
    return files


def process_file(path: Path, enc) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  SKIP  {path}  ({e})")
        return False

    stat = path.stat()
    token_count = len(enc.encode(text))

    data = {
        "schema_version": SIDECAR_SCHEMA_VERSION,
        "file": path.name,
        "updated": datetime.now(timezone.utc).isoformat(),
        "size_bytes": stat.st_size,
        "lines": text.count("\n") + 1,
        "chars": len(text),
        "tokens": token_count,
        "tokenizer": "tiktoken cl100k_base",
        "precision": SIDECAR_PRECISION,
    }

    stats_path = Path(str(path) + ".stats")
    stats_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    # ASCII arrow: a cp1252 console (Windows default) cannot encode "→".
    print(f"  OK    {path}  ->  {token_count:,} tokens")
    return True


def build_stamp_block(tokens: int, tokenizer: str, precision: str, model: str | None, stamped_utc: str) -> str:
    """Build the one-entry cost stamp: comment-delimited so re-stamps are detectable,
    with a single visible line so rendered markdown shows the cost."""
    parts = [
        f"**Production cost:** {tokens:,} tokens",
        f"{tokenizer} ({precision})",
    ]
    if model:
        parts.append(f"model {model}")
    parts.append(f"stamped {stamped_utc}")
    visible_line = " · ".join(parts)
    return f"{STAMP_START}\n{visible_line}\n{STAMP_END}\n"


def apply_stamp(text: str, block: str) -> str:
    """Return text with exactly one stamp block as its final entry.

    Idempotence rule: every existing stamp block is removed, then the fresh block is
    appended at the end -- re-stamping replaces, never duplicates, even if a previous
    stamp was somehow moved mid-document.
    """
    text = STAMP_PATTERN.sub("", text)
    text = text.rstrip("\n")
    if text:
        return text + "\n\n" + block
    return block


def stamp_artifact(path: Path, tokens: int, tokenizer: str, precision: str, model: str | None) -> None:
    """Stamp a markdown artifact with its production cost, then refresh its sidecar
    so the sidecar's own counts reflect the stamped content."""
    text = path.read_text(encoding="utf-8", errors="replace")
    stamped_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    block = build_stamp_block(tokens, tokenizer, precision, model, stamped_utc)
    path.write_text(apply_stamp(text, block), encoding="utf-8")

    enc = tiktoken.get_encoding("cl100k_base")
    process_file(path, enc)


def parse_stamp_args(argv: list[str]):
    """Parse stamp-mode arguments. Returns (path, tokens, tokenizer, precision, model)
    or an error string. Flag style is hand-rolled, matching the sibling Oracle skills."""
    args = list(argv)

    def take_flag_value(flag):
        if flag not in args:
            return None
        idx = args.index(flag)
        if idx + 1 >= len(args):
            raise ValueError(f"{flag} requires a value.")
        value = args[idx + 1]
        del args[idx:idx + 2]
        return value

    try:
        raw_tokens = take_flag_value("--stamp-cost")
        tokenizer = take_flag_value("--tokenizer") or DEFAULT_STAMP_TOKENIZER
        precision = take_flag_value("--precision") or DEFAULT_STAMP_PRECISION
        model = take_flag_value("--model")
    except ValueError as e:
        return str(e)

    try:
        tokens = int(raw_tokens)
    except (TypeError, ValueError):
        return f"--stamp-cost requires an integer token count, got: {raw_tokens!r}"
    if tokens < 0:
        return f"--stamp-cost must be non-negative, got: {tokens}"

    if precision not in VALID_PRECISIONS:
        allowed = ", ".join(sorted(VALID_PRECISIONS))
        return f"--precision must be one of: {allowed} (got: {precision!r})"

    if len(args) != 1:
        return "Stamp mode takes exactly one markdown artifact path."

    path = Path(args[0])
    if not path.is_file():
        return f"Artifact not found: {path}"
    if path.suffix.lower() not in MARKDOWN_EXTENSIONS:
        return f"Stamp mode only stamps markdown artifacts (.md/.markdown), got: {path.name}"

    return path, tokens, tokenizer, precision, model


def run_stamp_mode(argv: list[str]) -> int:
    parsed = parse_stamp_args(argv)
    if isinstance(parsed, str):
        print(f"Error: {parsed}")
        return 1

    path, tokens, tokenizer, precision, model = parsed
    stamp_artifact(path, tokens, tokenizer, precision, model)
    print(f"Stamped {path} with production cost {tokens:,} tokens ({tokenizer}, {precision}).")
    return 0


def main():
    if len(sys.argv) < 2:
        print("Error: nothing specified.")
        print()
        print("Usage:")
        print("  Whole directory:     generate_stats.py <directory>")
        print("  Specific file(s):    generate_stats.py <file1> <file2> ...")
        print("  Stamp cost:          generate_stats.py --stamp-cost <tokens> <artifact.md>")
        print("                       [--tokenizer ID] [--precision reported|delta|estimated] [--model NAME]")
        print()
        print("Please specify a directory or one or more files.")
        sys.exit(1)

    if "--stamp-cost" in sys.argv:
        sys.exit(run_stamp_mode(sys.argv[1:]))

    targets = [Path(arg) for arg in sys.argv[1:]]

    missing = [t for t in targets if not t.exists()]
    if missing:
        for m in missing:
            print(f"Error: not found: {m}")
        sys.exit(1)

    files = []
    for t in targets:
        files.extend(collect_files(t))

    if not files:
        print("No processable files found in the specified target(s).")
        sys.exit(0)

    enc = tiktoken.get_encoding("cl100k_base")

    print(f"Processing {len(files)} file(s)...")
    print()

    ok = sum(process_file(f, enc) for f in files)
    skipped = len(files) - ok

    print()
    print(f"Done.  {ok} written,  {skipped} skipped.")


if __name__ == "__main__":
    main()
