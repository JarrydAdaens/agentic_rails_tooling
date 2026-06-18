---
name: oracle-token-appraise
description: >
  Appraise a file's token cost before reading it into context.
  Runs a local Python script via uv — file content never enters the context window.
  Returns token count, size, line count, window usage percentage, and a read verdict.
  Use before reading any file when token budget is a concern.
  Trigger: "appraise <file>", "how big is <file>", "check tokens in <file>",
  "can I afford to read <file>", or whenever an agent should check a file's cost
  before ingesting it.
metadata:
  version: "1.0"
---

# Oracle Token Appraise

## Purpose

Check a file's token cost **without reading its contents into context**. The script
runs via `uv run` in an isolated environment and returns a summary. The agent uses
the verdict to decide how to proceed.

## Prerequisites

`uv` must be installed on the host machine. First run downloads `tiktoken` into uv's
cache. Subsequent runs are fast cache hits — no repeated downloads.

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

```
File:       design.md
Size:       18,432 bytes
Lines:      412
Characters: 18,012
Tokens:     4,830  (tiktoken cl100k_base)
Window:     40,000 tokens
Usage:      12.1%
Verdict:    SMALL  — safe to read whole file
```
