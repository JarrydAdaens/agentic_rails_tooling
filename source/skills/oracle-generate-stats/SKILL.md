---
name: oracle-generate-stats
description: >
  Generate or refresh .stats sidecar files for text files.
  Each sidecar (e.g. design.md.stats) records token count, line count,
  character count, and byte size without reading file content into context.
  Accepts a directory, a single file, or multiple named files.
  Also stamps markdown artifacts with their actual production token cost
  (--stamp-cost) as a single idempotent final entry.
  Aborts with guidance if nothing is specified.
  Trigger: "generate stats", "refresh stats", "update .stats files",
  "run oracle-generate-stats on <target>", "stamp the cost on <artifact>",
  or after compressing/editing context files when sidecar data needs
  to be refreshed.
disable-model-invocation: false
metadata:
  version: "1.2"
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

## Sidecar Schema (v2)

```json
{
  "schema_version": 2,
  "file": "design.md",
  "updated": "2026-06-18T10:30:00Z",
  "size_bytes": 18432,
  "lines": 412,
  "chars": 18012,
  "tokens": 4830,
  "tokenizer": "tiktoken cl100k_base",
  "precision": "estimated"
}
```

- `schema_version` — sidecar format version. Bumped only on breaking shape changes.
- `precision` — always `"estimated"` for sidecar counts: the tokens were counted by a
  local tokenizer over content that was never actually sent to a model. Labels follow
  the Oracle API contract's closed taxonomy (`reported` / `delta` / `estimated`).

**v1 compatibility:** sidecars written before v2 lack `schema_version` and `precision`.
Consumers should treat a sidecar without `schema_version` as v1 and not assume the new
fields exist. This script never reads existing sidecars — regenerating any file
overwrites its sidecar wholesale, upgrading v1 to v2 cleanly and never crashing on the
old shape.

## Cost Stamping (`--stamp-cost`)

Stamp a markdown artifact with the actual token cost of producing it, appended as the
artifact's single concise final entry:

```
uv run skills/oracle-generate-stats/generate_stats.py --stamp-cost <tokens> <artifact.md> \
  [--tokenizer ID] [--precision reported|delta|estimated] [--model NAME]
```

The stamp is an HTML-comment-delimited block whose markers are invisible in rendered
markdown; only one bold line shows:

```markdown
<!-- oracle:cost-stamp:start -->
**Production cost:** 12,345 tokens · provider-reported (reported) · model claude-fable-5 · stamped 2026-07-09T03:00:00Z
<!-- oracle:cost-stamp:end -->
```

Rules:

- **Idempotent.** Re-stamping removes any existing stamp block and appends the fresh
  one at the end — never duplicates, even if a stamp was stranded mid-document by
  later edits.
- **Artifacts stay clean.** The stamp is one visible line; heavy metadata belongs in
  the `.stats` sidecar, which stamping automatically regenerates so its counts reflect
  the stamped content (otherwise it would go stale immediately).
- **Defaults are honest.** `--tokenizer` defaults to `provider-reported` and
  `--precision` to `reported`: the typical producer passes a cumulative cost its own
  provider accounting measured, not a local tokenizer count. `--precision` accepts only
  the contract taxonomy (`reported`, `delta`, `estimated`) and rejects anything else.
- **Markdown only.** Stamp mode refuses non-`.md`/`.markdown` targets — the comment
  markers are markdown-safe, not universal.

### Producer convention (v1)

Producing skills pass their cumulative cost **explicitly** via `--stamp-cost`. There is
no session introspection or automatic cost capture: the skill that produced the
artifact is the only party that knows what it spent (e.g. from its provider usage
records), so it reports that number when it stamps. Example — a planning skill that
finishes writing `plan.md` having consumed 48,210 tokens:

```
uv run skills/oracle-generate-stats/generate_stats.py --stamp-cost 48210 plan.md --model claude-fable-5
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
