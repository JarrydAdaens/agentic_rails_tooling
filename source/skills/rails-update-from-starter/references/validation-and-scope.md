---
name: rails-update-from-starter-validation-and-scope
metadata:
  version: "3.0"
---

# Validation And Scope

<!-- rails-lint-allow: VC001 VC004 -->
<!-- Justification: this file's Era Detection section documents
     migration-detection logic for rails-update-from-starter. It must name
     retired folder/file shapes verbatim so the skill can recognize them on a
     target project: the literal `sprints/` folder from the layout generation
     that sat between the earliest layout and the current milestone-centric
     one, and the even older `goals*.md` / `milestones.md` / `tier0/` shapes.
     These are detection signals describing OLD project shapes the skill
     migrates away from, not descriptions of the current framework. -->

Use this reference when starting `rails-update-from-starter`, validating paths, detecting the target's era, or deciding which files are in scope.

## Source Starter Validation

Before comparing files, verify that the supplied source directory looks like the current `agentic_rails_context_starter`.

Strong current-layout signals include:

- `AGENTIC_RAILS_README.MD`
- `AGENTS.md`
- `context/design.md` (contains a Milestones Index subsection)
- `context/milestones/` with `milestone-1.md` and `MILESTONE_TEMPLATE.md`, where each milestone document contains its own stories directly
- `context/backlog/` with `backlog-1.md` and `BACKLOG_TEMPLATE.md`, presented as an unscheduled story inventory rather than a formal tier
- `context/dictations-tier-0/` with `DICTATIONS_TIER_0_NOTE_TEMPLATE.md`
- `context/implementation-plans/` (a `.gitkeep`-only folder in the current starter; there is no checked-in plan template, and existing plan folders are grouped as `<milestone-slug>/<story-slug>/`)

If the supplied source still shows an older layout — a single `context/milestones.md`, `context/goals*.md`, a `context/tier0/` folder, an `IMPLEMENTATION_PLAN_TEMPLATE/` folder, or a `context/sprints/` folder with milestones that only index stories rather than contain them — it is a stale starter checkout. Tell the user the starter itself is out of date and stop; do not migrate a target against an old source.

If the path does not look like the starter at all, stop and tell the user what was missing. Do not continue against an uncertain source path.

## Target Project Validation

Run from the derived child project unless the user explicitly provides a target project path.

Check whether the target appears Agentic Rails-derived using signals such as:

- `AGENTIC_RAILS_README.MD`
- `.agentic-rails.json`
- `context/` or `Documentation/`
- `context/design.md` (or `Documentation/design.md`)
- a milestones surface (`context/milestones/` or `context/milestones.md`)
- a work-unit surface (`context/backlog/` or `context/goals*.md`)
- an implementation-plan folder

If the target does not clearly look derived from Agentic Rails, stop and ask the user whether this is the intended target.

Do not use this skill on the central `agentic_rails_context_starter` repository itself, the `agentic-rails-memory` repository, or to update reusable skills, agents, rules, or workflow tooling; those belong to `agentic_rails_tooling`.

## Era Detection And Mode Selection

Decide the target's era before selecting files. This drives whether the run is **alignment** or **migration**.

Treat the target as **current (alignment mode)** when it has:

- `context/dictations-tier-0/`
- `context/design.md` with a Milestones Index subsection
- `context/milestones/` as a folder, with stories living directly inside each milestone document
- `context/backlog/`, treated as an unscheduled story inventory rather than a formal tier
- `context/implementation-plans/<milestone-slug>/<story-slug>/` grouping (where any plan folders exist)

Treat the target as **legacy (migration mode)** when it shows any of:

- a single `context/milestones.md` file (rather than a `milestones/` folder)
- `context/goals*.md` files
- a `context/tier0/` folder (rather than `dictations-tier-0/`)
- a `Documentation/` context root instead of `context/`
- an `IMPLEMENTATION_PLAN_TEMPLATE/` folder or `GOAL_*` plan folders
- a `context/sprints/` folder, or `milestones/` documents that only index stories kept elsewhere instead of containing them directly
- a flat, ungrouped `implementation-plans/STORY_*/` layout instead of `implementation-plans/<milestone-slug>/<story-slug>/`
- front matter with old top-level `version:` / `agentic_rails_source_version:` fields rather than nested `metadata.*`

A target can be partly migrated (mixed signals). When in doubt, treat it as migration mode for the parts that are still legacy, and alignment mode for the parts already on the current layout. Report exactly what era each surface is in.

### Legacy layout mapping (reference)

The target may be on either of two legacy generations. The older one predates any milestone/story split at all; the newer one introduced milestones and a separate scheduling folder but kept stories out of the milestone document itself. Both map to the same current target shape.

| Legacy surface | Current surface | Migration action |
| --- | --- | --- |
| `tier0/` or `Documentation/` Dictation | `context/dictations-tier-0/` | Move/rename the folder; keep raw transcription intact. |
| `design.md` | `context/design.md` | Keep; add the **Milestones Index** subsection. |
| `milestones.md` (single file) | `context/milestones/milestone-N.md` | Split each milestone into its own doc; index them from Design. |
| `milestones/` (index-only) + `sprints/` (scheduling folder) | `context/milestones/milestone-N.md` (containing stories directly) | Fold each scheduled grouping into the owning milestone's Stories section; retire the scheduling folder. |
| `goals*.md` / goals | `context/backlog/backlog-N.md` stories, or directly into a milestone's Stories section if already scheduled | Convert each goal into a story, preserving content and plan links. |
| `implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/` | (removed) | The starter no longer ships a plan template; do not recreate it. |
| `implementation-plans/GOAL_*/` or flat `STORY_*/` folders | left as historical | Do not rewrite; preserve as execution history. |

The detailed, safety-bounded procedure for applying this mapping lives in [version-and-merge-policy.md](version-and-merge-policy.md#structural-migration-policy).

## Files To Inspect

Process files in this order, mapping legacy equivalents when the target predates the current layout:

1. Root `README.md`
2. Root Agentic Rails identity or description files:
   - `AGENTIC_RAILS_README.MD`
   - `AGENTIC_RAILS.md`
   - `.agentic-rails.json`
3. `context/design.md` and its Milestones Index (legacy equivalent: `design.md` plus `milestones.md`)
4. Milestones: starter `context/milestones/*.md` against target `context/milestones/*.md` (index-only variant), or a single `context/milestones.md`
5. Stories: starter's per-milestone Stories sections and `context/backlog/*.md` against target `context/backlog/*.md`, a legacy scheduling folder's scheduled stories, or every `context/goals*.md`
6. Dictation: starter `context/dictations-tier-0/` against target `context/dictations-tier-0/` or `context/tier0/`
7. Support files whose names or shapes changed, such as `agent-thinking.md` (legacy: `AgentThinking.md`)

Do not bulk-update historical implementation-plan folders.

## Files Not To Rewrite By Default

Do not rewrite or normalize completed implementation-plan folders, including:

- `context/implementation-plans/GOAL_*/` (earliest-layout execution history)
- `context/implementation-plans/STORY_*/`, whether flat (legacy scheduling-folder era) or grouped under `<milestone-slug>/<story-slug>/` (current-era execution history)
- the `plan.md` file inside them (including any `## Execution Log` / `## Completion Review` sections it already contains) and any opt-in sidecar files present, such as `implementation-log.md`, `completion-review.md`, `complaining.md`, `thinking.md`, `evidence.md`, or `handover/`

Historical execution records preserve what the project knew at the time. Legacy-named plan folders stay legacy-named; renaming them would break their links and rewrite history. Only touch old implementation-plan folders when the user explicitly asks for historical migration.

## Missing Target Files

If the starter has a standard context surface that the target project is missing:

- Create missing framework identity files and starter templates (milestone, backlog, and dictation templates and their tier READMEs).
- Create the missing current-layout folders (`milestones/`, `backlog/`, `dictations-tier-0/`) when migrating, populating them from the legacy equivalents rather than from blank placeholders.
- Create new context files only when doing so will not fabricate project-specific content. Use starter content only as scaffolding and mark placeholders honestly.
- Do not scaffold optional sidecar files (`questions.md`, `evidence.md`, `complaining.md`, `research.md`) into any implementation-plan folder by default; those stay opt-in per [version-and-merge-policy.md](version-and-merge-policy.md#implementation-plan-template-handling).
- Report created files.

Do not invent arbitrary backlog or milestone documents beyond what the target's existing content (or the starter template) justifies.

## README Handling

Root `README.md` is risky because derived projects often replace it with project-specific content.

When updating `README.md`:

- Never overwrite the whole file by default.
- Look for a clearly marked Agentic Rails section or context-links section.
- Update only that section when present, refreshing links to the current-layout surfaces (`context/milestones/`, `context/backlog/`, and so on).
- If no section exists, suggest or add a small Agentic Rails metadata section only when safe.
- Prefer keeping framework explanation in `AGENTIC_RAILS_README.MD`.
