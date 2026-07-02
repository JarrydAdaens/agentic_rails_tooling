---
name: rails-update-from-starter-version-and-merge-policy
metadata:
  version: "3.0"
---

# Version And Merge Policy

<!-- rails-lint-allow: VC001 VC004 -->
<!-- Justification: this file's Structural Migration Policy section documents
     migration-detection logic for rails-update-from-starter. It must name
     retired folder/file shapes verbatim so the skill can recognize them on a
     target project: the literal `sprints/` folder from the layout generation
     that sat between the earliest layout and the current milestone-centric
     one, and the even older `goals*.md` / `milestones.md` / `tier0/` shapes.
     These are detection signals describing OLD project shapes the skill
     migrates away from, not descriptions of the current framework. -->

Use this reference when interpreting front matter, comparing source versions, deciding whether a merge is safe, or migrating an older legacy project forward to the current milestone-centric layout.

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

Older projects may carry these at the top level (un-nested) and unquoted (`version: 1.4`). Treat a top-level, unquoted shape as a legacy-era signal: normalize it to the nested, quoted `metadata.*` shape during update. For bulk front-matter normalization across many files, prefer the `rails-clean-frontmatter` skill over hand-editing.

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
- Overwriting will not delete project-specific design, milestones, stories, backlog entries, or execution history.

Preserve:

- project purpose
- architecture decisions
- milestone definitions, including their story lists and sequencing notes
- backlog story names, types, priorities, scores, and statuses
- acceptance criteria
- out-of-scope decisions
- implementation-plan links
- completed work references
- project-specific constraints
- manually maintained rationale

Starter updates should add or improve:

- front matter fields (nested, quoted `metadata.*` shape)
- context hierarchy descriptions (name the tiers — Dictation, Design, Milestone, Story, Implementation Plan, Phase — not numbers)
- navigation sections
- template instructions
- framework identity sections
- placeholder cleanup guidance
- new conventions that help future agents understand the project
- links to new standard files or folders (`milestones/`, `backlog/`, `dictations-tier-0/`, `implementation-plans/<milestone-slug>/<story-slug>/`)

If a safe merge is not obvious, leave the file unchanged and report the conflict.

## Structural Migration Policy

Run this only in migration mode (a target still on an older legacy layout, per [validation-and-scope.md](validation-and-scope.md#era-detection-and-mode-selection)). Always create a recovery checkpoint first. The goal is to carry the project forward without losing a single project-specific decision and without rewriting execution history.

Apply the mapping surface by surface. Prefer creating the new structure, porting content, verifying, then reporting the old files for removal — rather than deleting first.

### Dictation folder

- Move raw transcription from `context/tier0/` (or the `Documentation/` Dictation equivalent) into `context/dictations-tier-0/`.
- Preserve filenames and raw content; do not re-synthesize.
- Add the current Dictation README and note template if missing.

### Design and the Milestones Index

- Keep the existing `design.md` content and project-specific synthesis.
- Add the **Milestones Index** subsection to `design.md`: a table with one row per milestone linking down to `milestones/milestone-N.md`.
- Update the embedded context-hierarchy table to the current tier shape (name the tiers; do not add tier numbers outside `design.md`'s own canonical table).

### Milestones and stories

- Split a single `context/milestones.md` into one `context/milestones/milestone-N.md` per milestone, using the starter milestone shape (intent, why it matters, outcome, status, story index, backlog sources).
- If the target is on the layout generation that sat between the earliest layout and the current one — where `milestones/` docs existed but only indexed stories scheduled elsewhere in a separate `context/sprints/` folder — fold each of those scheduled groupings directly into the owning milestone's **Stories** section, in the current starter's story shape (type, summary, value, rough scope, CER, plan link, status). The milestone document becomes the direct container; nothing should still point at a `context/sprints/` folder afterward.
- Carry each milestone's and story's intent, rationale, status, and any links forward verbatim where possible.
- Keep the Milestones Index in `design.md` in sync with the new files.

### Goals and legacy backlog entries to stories

- Convert each goal from `context/goals*.md` into a **Story**. If it is already scheduled for delivery, place it directly inside its milestone document's Stories section; otherwise stage it in `context/backlog/` as an unscheduled story-inventory entry.
- The backlog is one global, priority-sorted pool capped at 30 stories per file (`backlog-1.md`, `backlog-2.md`, ...), not one file per milestone, and it is not a formal tier — it is staging input for milestone planning (Milestone -1).
- For each story, preserve: name, type (Feature/Bug/Refactor/...), summary, value, scope, status, acceptance criteria, out-of-scope notes, and the existing implementation-plan link.
- Map old goal statuses onto story statuses (for example a completed goal becomes a story marked complete). Leave the milestone-association column as the goal's known milestone (or prior sprint/milestone) association, or `*unscheduled*` when none applies.
- Leave CER score columns as `—` unless the old goal already recorded complexity/effort/risk.

### Retiring the intermediate scheduling folder

- Do not create a `context/sprints/` folder, and do not preserve one in the migrated project. That folder belonged to the layout generation between the earliest layout and the current one; the current starter has no scheduling layer between Milestone and Story.
- If the target still has a `context/sprints/` folder, fold every story it references into the owning milestone document's Stories section (see above), then report the folder as superseded so the user can remove it once the port is verified.
- Do not fabricate story sequencing that the old scheduling folder never actually recorded; if the old grouping was already delivered, you may note it in the milestone's Interdependency Order or Notes section as historical context, but do not invent new sequencing.

### Implementation plans

- Leave completed, legacy-named plan folders (for example `GOAL_*/` or a flat, ungrouped `STORY_<cycle>_<story>_slug/`) untouched as historical execution records.
- Do not rename them; renaming breaks links and rewrites history.
- New plans created after migration use the grouped path `implementation-plans/<milestone-slug>/<story-slug>/plan.md`.

### Verification and cleanup

- After porting, verify that every goal or legacy story maps to a story (either inside a milestone or in the backlog), every milestone maps to a milestone doc and an index row, and all preserved links still resolve.
- Report the old `milestones.md`, `goals*.md`, `tier0/`, and any legacy scheduling folder as superseded. Remove them only after the user confirms the migration looks correct, or leave them and recommend removal in the report.

## Implementation-Plan Template Handling

The current starter does not ship a standalone implementation-plan template folder; the plan shape is supplied by right-rail planning tooling. A story's plan folder normally holds one primary artifact, `plan.md` — which includes its own `## Execution Log` and `## Completion Review` sections once execution starts and completes — plus optional `phase-N.md` files and other sidecars (`questions.md`, `evidence.md`, `complaining.md`, `research.md`) only when explicitly requested or genuinely required. Do not create or resurrect a standalone default-artifact template folder in the target, and do not scaffold sidecar files by default when creating a new plan folder during migration or alignment.

If a derived project maintains its own project-local plan template, preserve project additions unless they conflict with newer starter requirements. Do not migrate old completed plans unless explicitly requested.
