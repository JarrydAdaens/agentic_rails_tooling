# AGENTS.md

This file provides repository guidance for agentic IDEs and coding agents working in this repository. It is vendor-neutral: Cursor, Claude Code, Codex, Windsurf, OpenCode, Antigravity, and other skills-compatible clients should treat it as the project-level instruction entry point when they load `AGENTS.md` (or an adapter equivalent).

## What this repository is

`agentic_rails_tooling` is the **right rail** of the Agentic Rails framework: a version-controlled library of reusable agent capabilities. It contains almost no executable code — the artifacts are Markdown (`SKILL.md`, `AGENT.md`, rules, references) plus prompt source material. There is no build, but there **is** a lint step: `scripts/rails_lint.py` deterministically enforces the naming, frontmatter, and vocabulary conventions below. Run it (`python scripts/rails_lint.py .`) before committing artifact changes and before deployment; a clean exit is the repo's definition of well-formed.

It sits alongside `agentic_rails_context_starter` (the **left rail**, project-local context) and `agentic-rails-memory` (the framework's **records office** — durable cross-project artifacts, a record store beside the line rather than a rail). This repo also owns the logic that captures, curates, and rebuilds memory artifacts. It is deployed into IDEs by the external `kung-fu` WPF app, which syncs only the `source/` tree. This repo is the source of truth; sync is one-way outward. Edit artifacts here, never in the deployed copies.

Read `README.md` for the full layer-by-layer rationale and `AGENTIC_RAILS_README.MD` for the framework philosophy (the context tier system, the rails and the records office, provenance, handover). Don't duplicate their content into new files.

## Top-level layout

- `source/` — the only deployable tree. Holds `source/rules/`, `source/skills/`, and `source/agents/`.
- `scripts/` — repo infrastructure (not deployed): `scripts/rails_lint.py` plus its tests. See `scripts/README-SCRIPTS.md`.
- `context/` — everything *about* this repo (not deployed): `context/design.md`, `context/templates/`, `context/prompt-dev/`, `context/wiki/`.
- `archived/` — preserved-but-inactive artifacts (not deployed).
- `proposals/` — inbox of self-contained candidate capabilities dropped off by the `rails-new-proposal` skill (not deployed, excluded from lint; slices are verbatim copies from foreign projects — review, then promote or delete).
- `ide_specific/` — nonportable vendor files (a deliberate junk pile).

## The three primary layers

These all live under `source/`. When adding capability, pick the **narrowest** layer that fits:

- **`source/rules/`** — short, prescriptive style/engineering standards (C#, C++, WPF, Qt, TypeScript, React, etc.), authored for Claude Code: each file carries only a top-level `paths:` list of quoted glob strings, or no frontmatter at all for rules that should load every session (global, unit-testing). Claude Code auto-loads them by matching `paths:` globs against touched files — there is no routing index to read. Support for other IDEs (Cursor, Windsurf, Copilot, etc.) is produced at copy time by Kung Fu's conversion scripts, not hand-maintained per-IDE files in this repo. If a rule file grows into procedural expertise, it belongs in `source/skills/` instead.
- **`source/skills/`** — portable, task-shaped capability units. A skill says "here is how to do this task." Orchestration skills that coordinate subagents, queues, or durable artifacts use the **`-workflow`** suffix (e.g. `rails-boss-execute-workflow`, `rails-plan-spam-workflow`) so they surface in skill autocomplete while staying recognizable.
- **`source/agents/`** — named specialist personas. A persona says "here is the kind of worker you are." Folder name and frontmatter `name` must end in **`-persona`** (e.g. `wpf-persona`, `unreal-persona`). Each bundle has `AGENT.md` plus a `references/` library of focused knowledge files.

A fourth layer, `source/verifiers/` (reusable pass/fail acceptance checks), lived here until July 2026. Verifiers and guardrails are lifecycle artifacts — they install, update, and uninstall — so they were extracted to the `agentic_rails_marketplace` repository and are distributed through the native plugin marketplaces of Claude Code and Codex, not by Kung Fu. New verifiers and guardrails belong there, never here.

Likewise, in July 2026 the personal, non-Rails skills (`commit-log`, `grade`, `grugg`, `grugg-compress`, the `oracle-*` token-tooling family, `wpf-starter-update`, `wpf-tree-sensor`) were extracted to the separate `jarryds-agent-marketplace` repository. Every skill in this repo must be specific to the Agentic Rails system — it assumes the target project follows the `agentic_rails_context_starter` layout. A generic, works-anywhere skill belongs in `jarryds-agent-marketplace`, never here.

## Supporting directories

- `context/design.md` — the purpose and design of this repository. Read it before reshaping the layout.
- `context/templates/` — blank scaffolds for new artifacts (`context/templates/skills/skill-template`, `skill-template-advanced`). Copy into an active `source/` folder, then rename and fill in. Not deployed.
- `context/prompt-dev/skills-prompts/` — prompt records and source material behind generated artifacts. Often the real design history; preserve it.
- `context/wiki/` — local notes on the [Agent Skills spec](https://agentskills.io/specification) and this repo's alignment decisions.
- `archived/` — preserved-but-inactive artifacts (mirrors the main categories). Not deployed; mine for reference only.
- `ide_specific/` — deliberate junk pile for nonportable vendor files (IDE-global configs, vendor-only adapters, and similar). Do not treat contents here as portable Agentic Rails artifacts.

## Authoring conventions

These are load-bearing because the artifacts are consumed by other agents via progressive disclosure (discovery → activation → execution).

- **Naming**: file and folder names use **kebab-case**, not `snake_case` or `PascalCase`, except for tool-mandated names (`SKILL.md`, `AGENT.md`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `AGENTIC_RAILS_README.MD`, `.cursorrules`, `.gitkeep`) and language-idiomatic code files.
- **Skill folder structure**: a skill is a folder with a required `SKILL.md`; optional `scripts/`, `references/`, `assets/`. Move long detail into `references/` and link to it, keeping `SKILL.md` focused on the trigger and workflow.
- **`name` field**: lowercase letters, numbers, and hyphens only, and it **must match the folder name**. Persona names end in `-persona`; workflow skills end in `-workflow`.
- **`description` field**: under 1024 characters, and written as "Use this when…" — it is the only thing an agent sees at discovery time, so it must convey both what the artifact does and when to reach for it.
- **Frontmatter**: every artifact carries YAML frontmatter with `metadata.version` (a quoted string, e.g. `version: "1.2"`). Use the `rails-clean-frontmatter` skill to normalize/repair frontmatter across the repo rather than hand-editing many files.

## Git conventions

When the user or their global rules require a structured commit format, use the `commit-log` skill (maintained in the separate `jarryds-agent-marketplace` repository and installed globally — not part of this repo). Typical shape: a `[STORY X.Y]` or `[XXX-123]` heading (≤72 chars), then `~ Problem:`, body lines (`~ Fixed:`, `~ Changed:`, `~ Added:`, etc.), and `~ Resolution:`. American English throughout. Keep PRs small and focused — no cross-cutting refactors mixed with feature work.
