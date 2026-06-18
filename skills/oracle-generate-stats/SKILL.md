---
name: oracle-generate-stats
description: >
  Generate or refresh .stats sidecar files for text files.
  Each sidecar (e.g. design.md.stats) records token count, line count,
  character count, and byte size without reading file content into context.
  Accepts a directory, a single file, or multiple named files.
  Aborts with guidance if nothing is specified.
  Trigger: "generate stats", "refresh stats", "update .stats files",
  "run oracle-generate-stats on <target>", or after compressing/editing
  context files when sidecar data needs to be refreshed.
metadata:
  version: "1.0"
---

# Oracle Generate Stats

## Purpose

Write or refresh `.stats` sidecar files alongside text files. Each sidecar
contains raw file metrics — token count, lines, characters, bytes — computed
by a local Python script via `uv run`. File content never enters the context window.

Sidecar naming: `filename.ext.stats`
Example: `design.md` → `design.md.stats`

## Prerequisites

`uv` must be installed on the host machine. First run downloads `tiktoken` into
uv's cache. Subsequent runs hit the cache and are fast.

## Trigger

- `/oracle-generate-stats <target>`
- "generate stats for this directory"
- "refresh the .stats files in context/"
- "update stats after compression"
- After any skill that modifies context files (e.g. caveman-compress)

## Process

1. Locate `generate_stats.py` in the same directory as this SKILL.md:
   `skills/oracle-generate-stats/generate_stats.py`

2. Run via bash with one of these forms:

   Whole directory (recursive):
   ```
   uv run skills/oracle-generate-stats/generate_stats.py <directory>
   ```

   Single file:
   ```
   uv run skills/oracle-generate-stats/generate_stats.py <file>
   ```

   Multiple specific files:
   ```
   uv run skills/oracle-generate-stats/generate_stats.py <file1> <file2> <file3>
   ```

3. If the user has not specified a target, **do not guess**. Abort and ask:
   > "Please specify a target — a directory, a single file, or a list of files."

4. Report the script output to the user.

## Sidecar Schema

```json
{
  "file": "design.md",
  "updated": "2026-06-18T10:30:00Z",
  "size_bytes": 18432,
  "lines": 412,
  "chars": 18012,
  "tokens": 4830,
  "tokenizer": "tiktoken cl100k_base"
}
```

## What Gets Skipped

- Existing `.stats` files (never generate stats-of-stats)
- Binary formats: images, audio, video, archives, compiled files
- Hidden files (dot-prefixed names)
- Hidden directories: `.git`, `node_modules`, `__pycache__`, `.venv`

## Typical Workflow

1. Edit or compress context files
2. Run `oracle-generate-stats` on the affected directory
3. `git diff` shows changed `.md` files alongside updated `.stats` files
4. Token deltas are visible in the diff without opening the source files
