---
name: rails-update-from-starter
description: >-
  Use this skill when updating a project derived from Agentic Rails so its
  project-local context files, templates, front matter, framework metadata, and
  standard documentation structure stay aligned with a local checked-out
  agentic_rails_context_starter source of truth. Use when refreshing derived
  Agentic Rails projects from the current seven-tier starter without overwriting
  project-specific design, milestones, sprints, backlog stories, historical
  implementation plans, or provenance. Includes a compatibility layer that
  migrates older five-tier projects (single milestones.md, goals files, tier0/
  or Documentation/ layouts) forward to the seven-tier structure.
disable-model-invocation: true
metadata:
  version: "2.0"
---

# Rails Update From Starter

Keep a derived Agentic Rails project aligned with the current local `agentic_rails_context_starter` repository.

This is a comparison and selective merge skill, not a blind overwrite skill. It belongs to the right rail as reusable behavior; its edits belong to the child project's left-rail context.

The current starter uses the **seven-tier** layout: `dictations-tier-0/`, `design.md` (with an embedded Milestones Index), `milestones/`, `sprints/`, `backlog/`, and `implementation-plans/`. Derived projects come in two eras, so the skill runs in one of two modes.

## Two Modes

The skill detects the target project's era and chooses a mode (see [references/validation-and-scope.md](references/validation-and-scope.md)):

- **Alignment mode (default).** The target already uses the seven-tier layout. Perform selective, section-aware front-matter, structure, and template alignment against the starter. This is the common case for recently created projects.
- **Migration mode (compatibility layer).** The target still uses the older five-tier layout (a single `context/milestones.md`, `context/goals*.md`, a `context/tier0/` folder, or a `Documentation/` context root). Carry the project forward to the seven-tier structure using the migration mapping in [references/version-and-merge-policy.md](references/version-and-merge-policy.md), preserving every project-specific decision and all historical execution records.

## Required Input

Require the local filesystem path to the current `agentic_rails_context_starter` checkout.

If the user did not provide the path, ask exactly:

```text
Where is your local agentic_rails_context_starter repository? Please provide the exact directory path on disk.
```

Stop until the user provides the path. Do not guess the starter path.

## Progressive Disclosure

Load only the reference needed for the current phase:

- For repository signals, era detection, ordered file selection, and target/source checks, read [references/validation-and-scope.md](references/validation-and-scope.md).
- For front matter semantics, version comparison, selective merging, and the five-tier to seven-tier migration mapping, read [references/version-and-merge-policy.md](references/version-and-merge-policy.md).
- For the required final report and completion checklist, read [references/report-and-validation.md](references/report-and-validation.md).

## Operating Model

1. Identify the target project root. Default to the current repository unless the user provides a target path.
2. Identify the local `agentic_rails_context_starter` source path, asking for it if missing.
3. Validate the starter path and target project, and detect the target's era, using [references/validation-and-scope.md](references/validation-and-scope.md).
4. Choose the mode: alignment for seven-tier targets, migration for older five-tier targets.
5. Before any structural migration, create a recovery checkpoint (a Git commit when the repo is Git-backed and the user approves; otherwise a recorded status plus a clear report entry). Structural migration is a larger operation than a front-matter bump.
6. Build the ordered list of source files to compare or map.
7. For each comparable source/target file, parse YAML front matter and compare the target's `metadata.agentic_rails_source_version` against the starter file's `metadata.version`.
8. In alignment mode: compare outdated files against the starter and apply only safe, section-aware updates.
9. In migration mode: apply the seven-tier mapping — promote the milestones table into the Design **Milestones Index**, split `milestones.md` into `milestones/` docs, convert `goals*.md` into `backlog/` story files, rename the Tier 0 folder to `dictations-tier-0/`, and create the new `sprints/` scaffolding — while preserving project content.
10. Add or normalize missing `metadata.agentic_rails_source_version` front matter where safe. Use `rails-clean-frontmatter` for bulk front-matter normalization rather than hand-editing many files.
11. Leave completed historical implementation-plan folders (`GOAL_*/`, `STORY_*/`) untouched unless the user explicitly asks for historical migration.
12. Produce the factual update report from [references/report-and-validation.md](references/report-and-validation.md).

## Default File Priority

Inspect root framework files before documentation files, mapping old-era equivalents when the target is pre-seven-tier:

1. `README.md`
2. `AGENTIC_RAILS_README.MD`, `AGENTIC_RAILS.md`, `.agentic-rails.json`
3. `context/design.md` (Tier 1, including the Milestones Index subsection)
4. `context/milestones/` (Tier 2; old-era source is a single `context/milestones.md`)
5. `context/sprints/` (Tier 3; new in seven-tier — created during migration)
6. `context/backlog/` (Tier 4 stories; old-era source is `context/goals*.md`)
7. `context/dictations-tier-0/` (Tier 0; old-era source is `context/tier0/` or a `Documentation/` equivalent)
8. support files whose names changed (for example `AgentThinking.md` to `agent-thinking.md`)

Do not bulk-update historical implementation-plan folders such as `context/implementation-plans/GOAL_*/` or `context/implementation-plans/STORY_*/`.

## Safety Rules

- Never destroy project-specific context to copy starter placeholder text.
- Never downgrade a target file whose `metadata.agentic_rails_source_version` is newer than the supplied starter file's `metadata.version`.
- Never treat a local `metadata.version` as proof of starter freshness.
- Never rewrite completed implementation-plan execution history (`GOAL_*/`, `STORY_*/`) by default.
- Never lose a goal during migration. Every old goal becomes a backlog story with its name, status, deliverables, acceptance criteria, out-of-scope notes, and plan link preserved.
- Never delete the old five-tier files until their content is fully ported and verified; prefer creating the new structure first, then reporting the originals for cleanup.
- Never perform a structural migration without first creating a recovery checkpoint or explicitly recording why one was deferred.
- Never assume the starter checkout is current when version comparison says otherwise.
- Never hide conflicts. Leave unsafe files unchanged and surface them in the report.
- Never reintroduce retired vocabulary in migrated truth: no `goals` as a tier, no single `milestones.md`, no `tier0/` folder, and never `task` as a tier name.
