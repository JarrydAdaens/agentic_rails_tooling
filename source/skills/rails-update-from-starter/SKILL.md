---
name: rails-update-from-starter
description: >-
  Use this skill when updating a project derived from Agentic Rails so its
  project-local context files, templates, front matter, framework metadata, and
  standard documentation structure stay aligned with a local checked-out
  agentic_rails_context_starter source of truth. Use when refreshing derived
  Agentic Rails projects from the current milestone-centric starter without
  overwriting project-specific design, milestones, backlog stories, historical
  implementation plans, or provenance. Includes a compatibility layer that
  migrates projects still on an older, legacy context layout (a single
  milestones.md, goals files, a tier0/ or Documentation/ root, or a prior
  generation where milestones only indexed stories kept elsewhere) forward to
  the current context tier system.
disable-model-invocation: true
metadata:
  version: "3.0"
---

# Rails Update From Starter

Keep a derived Agentic Rails project aligned with the current local `agentic_rails_context_starter` repository.

This is a comparison and selective merge skill, not a blind overwrite skill. It belongs to the right rail as reusable behavior; its edits belong to the child project's left-rail context.

The current starter uses the context tier system's milestone-centric layout: `dictations-tier-0/` (Dictation), `design.md` (Design, with an embedded Milestones Index), `milestones/` (Milestone, containing stories directly), an informal `backlog/` story inventory that stages work before it is pulled into a milestone, and `implementation-plans/<milestone-slug>/<story-slug>/plan.md` (Implementation Plan, with optional Phase files). Derived projects come from several eras, so the skill runs in one of two modes.

## Two Modes

The skill detects the target project's era and chooses a mode (see [references/validation-and-scope.md](references/validation-and-scope.md)):

- **Alignment mode (default).** The target already uses the current milestone-centric layout. Perform selective, section-aware front-matter, structure, and template alignment against the starter. This is the common case for recently created projects.
- **Migration mode (compatibility layer).** The target still uses an older, legacy context layout — either the earliest layout (a single legacy milestones file, per-goal backlog files, and an unrenamed dictation folder or `Documentation/` root) or a later, now-also-retired generation where milestones only indexed stories kept in a separate backlog tier and plans lived in a flat, ungrouped folder. See [references/validation-and-scope.md](references/validation-and-scope.md) for the exact legacy filenames and folders this skill detects. Carry the project forward to the current milestone-centric structure using the migration mapping in [references/version-and-merge-policy.md](references/version-and-merge-policy.md), preserving every project-specific decision and all historical execution records.

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
- For front matter semantics, version comparison, selective merging, and the legacy-layout migration mapping, read [references/version-and-merge-policy.md](references/version-and-merge-policy.md).
- For the required final report and completion checklist, read [references/report-and-validation.md](references/report-and-validation.md).

## Operating Model

1. Identify the target project root. Default to the current repository unless the user provides a target path.
2. Identify the local `agentic_rails_context_starter` source path, asking for it if missing.
3. Validate the starter path and target project, and detect the target's era, using [references/validation-and-scope.md](references/validation-and-scope.md).
4. Choose the mode: alignment for targets already on the current milestone-centric layout, migration for targets still on an older legacy layout.
5. Before any structural migration, create a recovery checkpoint (a Git commit when the repo is Git-backed and the user approves; otherwise a recorded status plus a clear report entry). Structural migration is a larger operation than a front-matter bump.
6. Build the ordered list of source files to compare or map.
7. For each comparable source/target file, parse YAML front matter and compare the target's `metadata.agentic_rails_source_version` against the starter file's `metadata.version`.
8. In alignment mode: compare outdated files against the starter and apply only safe, section-aware updates.
9. In migration mode: apply the legacy-layout mapping from [references/version-and-merge-policy.md](references/version-and-merge-policy.md) — fold every legacy surface into the current milestone-centric shape (stories live inside milestone docs, plans are grouped under `implementation-plans/<milestone-slug>/<story-slug>/`, and the backlog becomes an informal story inventory) — while preserving project content.
10. Add or normalize missing `metadata.agentic_rails_source_version` front matter where safe. Use `rails-clean-frontmatter` for bulk front-matter normalization rather than hand-editing many files.
11. Leave completed historical implementation-plan folders untouched unless the user explicitly asks for historical migration.
12. Produce the factual update report from [references/report-and-validation.md](references/report-and-validation.md).

## Default File Priority

Inspect root framework files before documentation files, mapping legacy equivalents when the target predates the current layout:

1. `README.md`
2. `AGENTIC_RAILS_README.MD`, `AGENTIC_RAILS.md`, `.agentic-rails.json`
3. `context/design.md` (Design, including the Milestones Index subsection)
4. `context/milestones/` (Milestone, containing stories directly; legacy source is a single-file or index-only equivalent — see [references/version-and-merge-policy.md](references/version-and-merge-policy.md))
5. `context/backlog/` (informal story inventory / Milestone -1; legacy source is a formally tiered backlog folder or per-goal files — see the reference)
6. `context/dictations-tier-0/` (Dictation; legacy source is an unrenamed dictation folder or a `Documentation/` equivalent)
7. support files whose names changed (for example `AgentThinking.md` to `agent-thinking.md`)

Do not bulk-update historical implementation-plan folders such as `context/implementation-plans/GOAL_*/` or any other completed, legacy-named plan folder.

## Safety Rules

- Never destroy project-specific context to copy starter placeholder text.
- Never downgrade a target file whose `metadata.agentic_rails_source_version` is newer than the supplied starter file's `metadata.version`.
- Never treat a local `metadata.version` as proof of starter freshness.
- Never rewrite completed implementation-plan execution history by default.
- Never lose a goal or story during migration. Every legacy work item becomes a story inside its milestone (or, until scheduled, a backlog entry) with its name, status, deliverables, acceptance criteria, out-of-scope notes, and plan link preserved.
- Never delete legacy files until their content is fully ported and verified; prefer creating the new structure first, then reporting the originals for cleanup.
- Never perform a structural migration without first creating a recovery checkpoint or explicitly recording why one was deferred.
- Never assume the starter checkout is current when version comparison says otherwise.
- Never hide conflicts. Leave unsafe files unchanged and surface them in the report.
- Never reintroduce retired vocabulary or retired layout shapes in migrated truth: no legacy single-file milestones document, no legacy per-goal files, no unrenamed dictation-tier folder, no milestone-as-index-only shape, no flat/ungrouped implementation-plan folder, and never `task` as a tier name.
- Never scaffold optional plan sidecar files (`questions.md`, `evidence.md`, `complaining.md`, `research.md`) by default; `plan.md` is the one primary artifact.
