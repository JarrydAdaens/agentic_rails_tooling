<h1 align="center">grugg-compress</h1>

<p align="center">
  <strong>shrink memory file. save token every session.</strong>
</p>

---

A Claude Code skill that compresses your project memory files (`CLAUDE.md`, todos, preferences) into grugg/caveman format — so every session loads fewer tokens automatically.

Claude read `CLAUDE.md` on every session start. If file big, cost big. Grugg make file small. Cost go down forever.

## What It Do

```
/grugg-compress CLAUDE.md
```

Backup saved out-of-tree so skill auto-loaders don't re-ingest it:

```
CLAUDE.md                                                ← compressed (Claude reads this — fewer tokens every session)
%LOCALAPPDATA%\grugg-compress\backups\<dir>\CLAUDE.original.md  ← human-readable backup (you edit this)
```

Original never lost. Read and edit the `.original.md` at that path. Delete the backup, then run the skill again to re-compress after edits.

## Benchmarks

Real results on real project files:

| File | Original | Compressed | Saved |
|------|----------:|----------:|------:|
| `claude-md-preferences.md` | 706 | 285 | **59.6%** |
| `project-notes.md` | 1145 | 535 | **53.3%** |
| `claude-md-project.md` | 1122 | 636 | **43.3%** |
| `todo-list.md` | 627 | 388 | **38.1%** |
| `mixed-with-code.md` | 888 | 560 | **36.9%** |
| **Average** | **898** | **481** | **46%** |

All validations passed — headings, code blocks, URLs, file paths preserved exactly.

## Before / After

**Original (706 tokens):**

> "I strongly prefer TypeScript with strict mode enabled for all new code. Please don't use `any` type unless there's genuinely no way around it, and if you do, leave a comment explaining the reasoning. I find that taking the time to properly type things catches a lot of bugs before they ever make it to runtime."

**Grugg (285 tokens):**

> "Prefer TypeScript strict mode always. No `any` unless unavoidable — comment why if used. Proper types catch bugs early."

**Same instructions. 60% fewer tokens. Every. Single. Session.**

## Security

`grugg-compress` is flagged as Snyk High Risk due to subprocess and file I/O patterns detected by static analysis. This is a false positive — see [SECURITY.md](./SECURITY.md) for a full explanation of what the skill does and does not do.

## Install

**Requires:** Python 3.10+ and [uv](https://docs.astral.sh/uv/) on PATH.

No manual dependency install needed — `uv run` handles it automatically.

The skill lives at:

```
grugg-compress/
```

## Usage

```
/grugg-compress <filepath>
```

Examples:
```
/grugg-compress CLAUDE.md
/grugg-compress docs/preferences.md
/grugg-compress todos.md
```

### What files work

| Type | Compress? |
|------|-----------|
| `.md`, `.txt`, `.rst`, `.typ`, `.typst`, `.tex` | Yes |
| Extensionless natural language | Yes |
| `.py`, `.js`, `.ts`, `.json`, `.yaml` | Skip (code/config) |
| `*.original.md` | Skip (backup files) |

## How It Work

```
/grugg-compress CLAUDE.md
        ↓
detect file type        (no tokens)
        ↓
Claude compresses       (tokens — one call)
        ↓
validate output         (no tokens)
  checks: headings, code blocks, URLs, file paths, bullets
        ↓
if errors: Claude fixes cherry-picked issues only   (tokens — targeted fix)
  does NOT recompress — only patches broken parts
        ↓
retry up to 2 times
        ↓
write compressed → CLAUDE.md
write backup     → %LOCALAPPDATA%\grugg-compress\backups\<dir>\CLAUDE.original.md
```

Only two things use tokens: initial compression + targeted fix if validation fails. Everything else is local Python.

## Model

Two paths, depending on whether `ANTHROPIC_API_KEY` is set:

- **No API key (normal case):** calls the `claude` CLI, which uses whatever model you've set as your default. No model string involved.
- **API key set:** uses the Anthropic SDK with a pinned current Sonnet (`claude-sonnet-4-6`). The Messages API needs a concrete model ID — there's no floating "latest" alias — so override it with `GRUGG_MODEL` when you want a different one:

```
GRUGG_MODEL=claude-opus-4-8 /grugg-compress CLAUDE.md
```

## What Is Preserved

Grugg compress natural language. It never touch:

- Code blocks (` ``` ` fenced or indented)
- Inline code (`` `backtick content` ``)
- URLs and links
- File paths (`/src/components/...`)
- Commands (`npm install`, `git commit`)
- Technical terms, library names, API names
- Headings (exact text preserved)
- Tables (structure preserved, cell text compressed)
- Dates, version numbers, numeric values

## Why This Matter

`CLAUDE.md` loads on **every session start**. A 1000-token project memory file costs tokens every single time you open a project. Over 100 sessions that's 100,000 tokens of overhead — just for context you already wrote.

Grugg cut that by ~46% on average. Same instructions. Same accuracy. Less waste.

```
┌────────────────────────────────────────────┐
│  TOKEN SAVINGS PER FILE    █████       46% │
│  SESSIONS THAT BENEFIT     ██████████ 100% │
│  INFORMATION PRESERVED     ██████████ 100% │
│  SETUP TIME                █            1x │
└────────────────────────────────────────────┘
```

## Part of Grugg

This skill is part of the grugg toolkit — making Claude use fewer tokens without losing accuracy.

- **grugg** — make Claude *speak* like Grugg (cuts response tokens ~65%)
- **grugg-compress** — make Claude *read* less (cuts context tokens ~46%)

Upstream: [caveman by JuliusBrussee](https://github.com/JuliusBrussee/caveman)
