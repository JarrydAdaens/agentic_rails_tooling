---
name: rails-update-from-starter
description: >-
  Use this skill when updating a project derived from Agentic Rails so its
  project-local context files, templates, front matter, framework metadata, and
  standard documentation structure stay aligned with a local checked-out
  agentic_rails_context_starter source of truth. Use when refreshing derived
  Agentic Rails projects from the starter without overwriting project-specific
  design, milestones, goals, historical implementation plans, or provenance.
metadata:
  version: "1.0"
  agentic_rails_source_version: "1.0"
---

# Rails Update From Starter

Keep a derived Agentic Rails project aligned with the current local `agentic_rails_context_starter` repository.

This is a comparison and selective merge skill, not a blind overwrite skill. It belongs to the right rail as reusable behavior; its edits belong to the child project's left-rail context.

## Required Input

Require the local filesystem path to the current `agentic_rails_context_starter` checkout.

If the user did not provide the path, ask exactly:

```text
Where is your local agentic_rails_context_starter repository? Please provide the exact directory path on disk.
```

Stop until the user provides the path. Do not guess the starter path.

## Progressive Disclosure

Load only the reference needed for the current phase:

- For repository signals, ordered file selection, and target/source checks, read [references/validation-and-scope.md](references/validation-and-scope.md).
- For front matter semantics, version comparison, and selective merging, read [references/version-and-merge-policy.md](references/version-and-merge-policy.md).
- For the required final report and completion checklist, read [references/report-and-validation.md](references/report-and-validation.md).

## Operating Model

1. Identify the target project root. Default to the current repository unless the user provides a target path.
2. Identify the local `agentic_rails_context_starter` source path, asking for it if missing.
3. Validate the starter path and target project using [references/validation-and-scope.md](references/validation-and-scope.md).
4. Build the ordered list of source files to compare.
5. For each comparable source/target file, parse YAML front matter and compare the target's starter-source version against the starter file's `version`.
6. Compare outdated files against the starter and apply only safe, section-aware updates.
7. Add or normalize missing starter-source front matter where safe.
8. Synchronize current implementation-plan templates only.
9. Leave completed historical implementation-plan folders untouched unless the user explicitly asks for historical migration.
10. Produce the factual update report from [references/report-and-validation.md](references/report-and-validation.md).

## Default File Priority

Inspect root framework files before documentation files:

1. `README.md`
2. `AGENTIC_RAILS_README.MD`, `AGENTIC_RAILS.md`, `.agentic-rails.json`
3. `Documentation/design.md`
4. `Documentation/milestones.md`
5. `Documentation/goals*.md`
6. current Tier 4 templates under `Documentation/implementation_plans/`

Do not bulk-update historical implementation-plan folders such as `Documentation/implementation_plans/GOAL_*/`.

## Safety Rules

- Never destroy project-specific context to copy starter placeholder text.
- Never downgrade a target file whose `agentic_rails_source_version` is newer than the supplied starter file's `version`.
- Never treat local `version` as proof of starter freshness.
- Never rewrite completed Tier 4 execution history by default.
- Never assume the starter checkout is current when version comparison says otherwise.
- Never hide conflicts. Leave unsafe files unchanged and surface them in the report.
