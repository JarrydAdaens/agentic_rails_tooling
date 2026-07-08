---
name: oracle-token-appraise
description: >
  Appraise a file's token cost before reading it into context.
  Runs a local Python script via uv — file content never enters the context window.
  Queries Oracle Server's model-aware estimation API when reachable, falling back to
  local tiktoken counting when it is not. Returns token count, size, line count,
  window usage percentage, estimation source, tokenizer identity, and a read verdict.
  Use before reading any file when token budget is a concern.
  Trigger: "appraise <file>", "how big is <file>", "check tokens in <file>",
  "can I afford to read <file>", or whenever an agent should check a file's cost
  before ingesting it.
disable-model-invocation: false
metadata:
  version: "1.2"
---

# Oracle Token Appraise

## Purpose

Check a file's token cost **without reading its contents into context**. The script
runs via `uv run` in an isolated environment and returns a summary. The agent uses
the verdict to decide how to proceed.

## Prerequisites

`uv` must be installed on the host machine. First run downloads `tiktoken` into uv's
cache. Subsequent runs are fast cache hits — no repeated downloads.

## Estimation source: Oracle Server or local tiktoken

The script tries Oracle Server first and falls back automatically:

1. **Oracle Server** (`POST /v1/estimate`, model-aware) — used when the server answers
   a short `/health` probe. The script sends the file's **absolute path only** (never
   its content) plus the target model and window; Oracle Server reads the file itself
   and returns token counts, tokenizer identity, and a verdict.
2. **Local tiktoken** (`cl100k_base`, this skill's original behavior) — used when the
   server is unreachable, or rejects the request (e.g. a path it cannot read).

Every report names which source and tokenizer produced it (`Source:` / `Tokenizer:`
lines), so results are never presented as more precise than they are.

### Configuration

| Variable | Default | Meaning |
|---|---|---|
| `ORACLE_SERVER_URL` | `http://localhost:5140` | Oracle Server base URL. Same convention as `oracle-token-stats`'s live mode. |

No other configuration is read from the environment; `--window` and `--model` (below)
are CLI flags, not env vars.

### Same-machine assumption

Server mode sends a **file path**, not file content — Oracle Server reads the path
itself. This only works when Oracle Server can see the same filesystem the agent is
working in (today: the same machine). If the server is running elsewhere, or the path
is only valid to this process (e.g. a Git-Bash/WSL-style `/d/...` path that Windows's
`Path.IsPathFullyQualified` rejects as not fully qualified), the server 400s the
request and the script **falls back to local tiktoken** rather than failing — it never
surfaces a raw server error as a hard failure. Files over the server's 10 MB
per-path cap fail the same way and fall back the same way.

### Accuracy note

Server-side tokenizer selection depends on Oracle Server's model registry
(`oracle.models.json`). If that file isn't configured on the server's machine, **every**
`targetModel` — including the default `claude` — degrades to a characters-per-token
heuristic (`heuristic:chars-per-token-4`), which is coarser than this skill's original
fixed `cl100k_base` count. The `Tokenizer:` line always names the tokenizer and match
label actually used, so this degradation is visible, not silent. Configuring the
registry on the server improves accuracy; the skill does not require it.

## Trigger

- `/oracle-token-appraise <filepath>`
- "appraise this file before reading it"
- "how many tokens is <file>?"
- Proactively, before reading any file where token budget is a concern

## Process

1. Locate `appraise.py` in the same directory as this SKILL.md:
   `skills/oracle-token-appraise/appraise.py`

2. Run via bash — do **not** read the file into context first:

   ```
   uv run skills/oracle-token-appraise/appraise.py <absolute_or_relative_file_path>
   ```

   To specify a non-default context window size:

   ```
   uv run skills/oracle-token-appraise/appraise.py <file_path> --window 8000
   ```

   To specify the target model (drives server-side tokenizer selection; default `claude`):

   ```
   uv run skills/oracle-token-appraise/appraise.py <file_path> --model gpt-4o
   ```

3. Report the full output to the user.

4. Act on the **Verdict** line:

   | Verdict | Action |
   |---|---|
   | SMALL — safe to read whole file | Read the file normally |
   | MEDIUM — read whole file with care | Read, but note the cost to the user |
   | LARGE — consider reading in sections | Offer to read in chunks, or read only relevant sections |
   | HUGE — do not read whole file | Do not read the whole file; summarise structure, read targeted sections only |

## Critical Rule

**Never read the file content into context before running the appraisal.**
The entire point of this skill is to inspect the file's cost *without* paying it.
Run the script first. Let the verdict decide what happens next.

## Output Example

Server-sourced (Oracle Server reachable):

```
File:       design.md
Size:       18,432 bytes
Lines:      412
Characters: 18,012
Source:     Oracle Server (targetModel=claude)
Tokenizer:  tiktoken:cl100k_base (proxy)
Tokens:     4,830
Window:     40,000 tokens
Usage:      12.1%
Verdict:    SMALL  — safe to read whole file
```

Local fallback (server unreachable or rejected the request):

```
File:       design.md
Size:       18,432 bytes
Lines:      412
Characters: 18,012
Source:     local tiktoken (server unreachable)
Tokenizer:  tiktoken:cl100k_base
Tokens:     4,830
Window:     40,000 tokens
Usage:      12.1%
Verdict:    SMALL  — safe to read whole file
```
