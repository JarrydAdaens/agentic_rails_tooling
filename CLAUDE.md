# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`agentic_rails_tooling` is the **right rail** of the Agentic Rails framework: a version-controlled library of reusable agent capabilities. It contains almost no executable code — the artifacts are Markdown (`SKILL.md`, `AGENT.md`, rules, references) plus prompt source material. There is no build, no test suite, and no lint step. "Correctness" here means well-formed artifacts that obey the naming and frontmatter conventions below.

It is the companion to `agentic_rails_context_starter` (the **left rail**, project-local context) and is deployed into IDEs by the external `kung-fu` WPF app. This repo is the source of truth; sync is one-way outward. Edit artifacts here, never in the deployed copies.

Read `README.md` for the full layer-by-layer rationale and `AGENTIC_RAILS_README.MD` for the framework philosophy (five-tier context, provenance, handover). Don't duplicate their content into new files.

## The three primary layers

Everything else in the repo supports these. When adding capability, pick the **narrowest** layer that fits:

- **`rules/`** — short, prescriptive style/engineering standards (C#, C++, WPF, Qt, etc.). Entry point is `rules/index.md`, which routes to the smallest relevant set by stack. If a rule file grows into procedural expertise, it belongs in `skills/` instead.
- **`skills/`** — portable, task-shaped capability units. A skill says "here is how to do this task." Orchestration skills that coordinate subagents, queues, or durable artifacts use the **`-workflow`** suffix (e.g. `rails-boss-execute-workflow`, `rails-plan-spam-workflow`) so they surface in skill autocomplete while staying recognizable.
- **`agents/`** — named specialist personas. A persona says "here is the kind of worker you are." Folder name and frontmatter `name` must end in **`-persona`** (e.g. `wpf-persona`, `unreal-persona`). Each bundle has `AGENT.md` plus a `references/` library of focused knowledge files.

## Supporting directories

- `templates/` — blank scaffolds for new artifacts (`templates/skills/skill-template`, `skill-template-advanced`). Copy into an active folder, then rename and fill in. Not deployed.
- `archived/` — preserved-but-inactive artifacts (mirrors the main categories). Not deployed; mine for reference only.
- `prompt_dev/skills_prompts/` — prompt records and source material behind generated artifacts. Often the real design history; preserve it.
- `wiki/` — local notes on the [Agent Skills spec](https://agentskills.io/specification) and this repo's alignment decisions.
- `ide_specific/` — deliberate junk pile for nonportable vendor files (e.g. `ide_specific/claude_global/CLAUDE.md` is the user's *global* Claude config, unrelated to this file).
- `workflows/` — **dead.** Holds only `NOT USED.txt`. Workflows now live in `skills/` with the `-workflow` suffix; do not revive this folder.

## Authoring conventions

These are load-bearing because the artifacts are consumed by other agents via progressive disclosure (discovery → activation → execution).

- **Skill folder structure**: a skill is a folder with a required `SKILL.md`; optional `scripts/`, `references/`, `assets/`. Move long detail into `references/` and link to it, keeping `SKILL.md` focused on the trigger and workflow.
- **`name` field**: lowercase letters, numbers, and hyphens only, and it **must match the folder name**. Persona names end in `-persona`; workflow skills end in `-workflow`.
- **`description` field**: under 1024 characters, and written as "Use this when…" — it is the only thing an agent sees at discovery time, so it must convey both what the artifact does and when to reach for it.
- **Frontmatter**: every artifact carries YAML frontmatter with `metadata.version` (a quoted string, e.g. `version: "1.2"`). Use the `rails-clean-frontmatter` skill to normalize/repair frontmatter across the repo rather than hand-editing many files.

## Git conventions

The user's global rules (loaded from `~/.claude/rules/global_rules.md`) require a specific commit format: a `[GOAL X.Y]` or `[XXX-123]` heading (≤72 chars) followed by `~ Problem:`, body lines (`~ Fixed:`, `~ Changed:`, `~ Added:`, etc.), and `~ Resolution:`. The full template is in `skills/commit-log/references/commit_log_template.md`; the `commit-log` skill produces it. American English throughout. Keep PRs small and focused — no cross-cutting refactors mixed with feature work.
