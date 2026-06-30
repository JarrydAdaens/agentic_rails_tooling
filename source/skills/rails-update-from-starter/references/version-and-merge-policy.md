---
name: rails-update-from-starter-version-and-merge-policy
metadata:
  version: "2.0"
---

# Version And Merge Policy

Use this reference when interpreting front matter, comparing source versions, deciding whether a merge is safe, or migrating an older five-tier project forward.

## Front Matter Model

Context files use YAML front matter. The current starter nests version fields under a `metadata:` block and quotes them as strings:

```yaml
---
name: design
description: <one-line summary>
metadata:
  version: "2.0"
  agentic_rails_source_version: "2.0"
  owner: "Your Name"
  repo: "your-repo"
---
```

Each comparable file has two relevant version concepts:

| Field | Meaning |
| --- | --- |
| `metadata.version` | The local file version inside the derived project. This may advance independently as the project evolves. |
| `metadata.agentic_rails_source_version` | The version of the corresponding source file from `agentic_rails_context_starter` that this local file last incorporated. |

Older projects may carry these at the top level (un-nested) and unquoted (`version: 1.4`). Treat a top-level, unquoted shape as an old-era signal: normalize it to the nested, quoted `metadata.*` shape during update. For bulk front-matter normalization across many files, prefer the `rails-clean-frontmatter` skill over hand-editing.

The local `metadata.version` is not the same as `metadata.agentic_rails_source_version`. A child project may legitimately have:

```yaml
metadata:
  version: "7.9"
  agentic_rails_source_version: "1.2"
```

This means the local project has heavily evolved, but it last incorporated starter conventions from starter file version `1.2`.

## Version Comparison Rules

For each comparable source/target file:

1. Read source front matter from the starter file (`metadata.version`).
2. Read target front matter from the derived project file (`metadata.agentic_rails_source_version`).
3. Compare the target's source version against the source file's version.

If the target source version is missing:

- Assume the target is outdated.
- Compare the source and target files.
- Update framework structure where safe.
- Improve or add missing front matter in the nested, quoted shape.
- Preserve project-specific content.

If the target source version is lower than the starter version:

- Treat the target as behind.
- Compare the source and target files.
- Selectively merge starter improvements.
- Update `metadata.agentic_rails_source_version` after a successful merge.
- Preserve the target file's local `metadata.version` unless the repository convention requires incrementing it.

If the target source version equals the starter version:

- Treat the target as current.
- Skip content changes unless required front matter fields or obvious structural metadata are missing.
- Report that the file is current.

If the target source version is higher than the starter version:

- Stop for that file.
- Do not downgrade or guess.
- Record the file as blocked and tell the user.
- Explain that the starter checkout may be stale, the target version metadata may be incorrect, or the target may have been updated from a newer starter.

## Merge Policy

Prefer section-aware and front-matter-aware merging.

Do not perform a blind full-file overwrite unless all of the following are true:

- The target file is still obvious starter placeholder content.
- The user has not customized it.
- The source file is clearly the newer authoritative starter version.
- Overwriting will not delete project-specific design, milestones, sprints, backlog stories, or execution history.

Preserve:

- project purpose
- architecture decisions
- milestone definitions
- sprint plans and their scheduled stories
- backlog story names, types, priorities, scores, and statuses
- acceptance criteria
- out-of-scope decisions
- implementation-plan links
- completed work references
- project-specific constraints
- manually maintained rationale

Starter updates should add or improve:

- front matter fields (nested, quoted `metadata.*` shape)
- context hierarchy descriptions (seven-tier)
- navigation sections
- template instructions
- framework identity sections
- placeholder cleanup guidance
- new conventions that help future agents understand the project
- links to new standard files or folders (`milestones/`, `sprints/`, `backlog/`, `dictations-tier-0/`)

If a safe merge is not obvious, leave the file unchanged and report the conflict.

## Structural Migration Policy

Run this only in migration mode (an older five-tier target, per [validation-and-scope.md](validation-and-scope.md#era-detection-and-mode-selection)). Always create a recovery checkpoint first. The goal is to carry the project forward without losing a single project-specific decision and without rewriting execution history.

Apply the mapping surface by surface. Prefer creating the new structure, porting content, verifying, then reporting the old files for removal — rather than deleting first.

### Tier 0 folder

- Move raw transcription from `context/tier0/` (or the `Documentation/` Tier 0 equivalent) into `context/dictations-tier-0/`.
- Preserve filenames and raw content; do not re-synthesize.
- Add the current Tier 0 README and note template if missing.

### Design and the Milestones Index

- Keep the existing `design.md` content and project-specific synthesis.
- Add the **Milestones Index** subsection to `design.md`: a table with one row per milestone linking down to `milestones/milestone-N.md`.
- Update the embedded context-hierarchy table to the seven-tier shape.

### Milestones

- Split the single `context/milestones.md` into one `context/milestones/milestone-N.md` per milestone, using the starter milestone shape (intent, why it matters, impact, status, sprint index, backlog source).
- Carry each milestone's intent, rationale, status, and any links forward verbatim where possible.
- Keep the Milestones Index in `design.md` in sync with the new files.

### Goals to backlog stories

- Convert each goal from `context/goals*.md` into a **Story** in `context/backlog/`.
- The backlog is one global, priority-sorted pool capped at 30 stories per file (`backlog-1.md`, `backlog-2.md`, ...), not one file per milestone.
- For each story, preserve: name, type (Feature/Bug/Refactor), summary, value, scope, status, acceptance criteria, out-of-scope notes, and the existing implementation-plan link.
- Map old goal statuses onto story statuses (for example a completed goal becomes a story marked complete). Leave the `Sprint` column as the goal's known sprint/milestone association, or `*unscheduled*` when none applies.
- Leave score columns as `—` unless the old goal already recorded complexity/effort/risk.

### Sprints

- Create the `context/sprints/` folder with the current README and template.
- Do not fabricate sprint plans. Sprint planning happens close to execution. If old goals recorded a clear, already-delivered grouping, you may record it as a completed sprint; otherwise leave sprints as scaffolding and note that sprint planning is the next step.

### Implementation plans

- Leave `GOAL_*` plan folders untouched as historical execution records.
- Do not rename them to `STORY_*`; renaming breaks links and rewrites history.
- New plans created after migration use the `STORY_<sprint>_<story>_slug/` naming.

### Verification and cleanup

- After porting, verify that every goal maps to a story, every milestone maps to a milestone doc and an index row, and all preserved links still resolve.
- Report the old `milestones.md`, `goals*.md`, and `tier0/` files as superseded. Remove them only after the user confirms the migration looks correct, or leave them and recommend removal in the report.

## Implementation-Plan Template Handling

The current starter does not ship an implementation-plan template (the folder holds only `.gitkeep`); the plan, log, and completion-review shapes are supplied by right-rail planning tooling. Do not create or resurrect an `IMPLEMENTATION_PLAN_TEMPLATE/` folder in the target.

If a derived project maintains its own project-local plan template, preserve project additions unless they conflict with newer starter requirements. Do not migrate old completed plans unless explicitly requested.
