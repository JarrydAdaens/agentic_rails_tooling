---
name: rails-update-from-starter-validation-and-scope
metadata:
  version: "2.0"
---

# Validation And Scope

Use this reference when starting `rails-update-from-starter`, validating paths, detecting the target's era, or deciding which files are in scope.

## Source Starter Validation

Before comparing files, verify that the supplied source directory looks like the current `agentic_rails_context_starter`.

Strong seven-tier signals include:

- `AGENTIC_RAILS_README.MD`
- `AGENTS.md`
- `context/design.md` (contains a Milestones Index subsection)
- `context/milestones/` with `milestone-1.md` and `MILESTONE_TEMPLATE.md`
- `context/sprints/` with `sprint-1.md` and `SPRINT_TEMPLATE.md`
- `context/backlog/` with `backlog-1.md` and `BACKLOG_TEMPLATE.md`
- `context/dictations-tier-0/` with `DICTATIONS_TIER_0_NOTE_TEMPLATE.md`
- `context/implementation-plans/` (a `.gitkeep`-only folder in the current starter; there is no checked-in plan template)

If the supplied source still shows old five-tier signals (a single `context/milestones.md`, `context/goals*.md`, a `context/tier0/` folder, or an `IMPLEMENTATION_PLAN_TEMPLATE/` folder), it is a stale starter checkout. Tell the user the starter itself is out of date and stop; do not migrate a target against an old source.

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

Treat the target as **seven-tier (alignment mode)** when it has:

- `context/dictations-tier-0/`
- `context/design.md` with a Milestones Index subsection
- `context/milestones/` as a folder
- `context/sprints/`
- `context/backlog/`

Treat the target as **older five-tier (migration mode)** when it shows any of:

- a single `context/milestones.md` file (rather than a `milestones/` folder)
- `context/goals*.md` files
- a `context/tier0/` folder (rather than `dictations-tier-0/`)
- a `Documentation/` context root instead of `context/`
- an `IMPLEMENTATION_PLAN_TEMPLATE/` folder or `GOAL_*` plan folders
- front matter with old top-level `version:` / `agentic_rails_source_version:` fields rather than nested `metadata.*`

A target can be partly migrated (mixed signals). When in doubt, treat it as migration mode for the parts that are still old, and alignment mode for the parts already on the seven-tier layout. Report exactly what era each surface is in.

### Five-tier to seven-tier mapping (reference)

| Old (5-tier) surface | New (7-tier) surface | Migration action |
| --- | --- | --- |
| `tier0/` or `Documentation/` Tier 0 | `context/dictations-tier-0/` | Move/rename the folder; keep raw transcription intact. |
| `design.md` | `context/design.md` | Keep; add the **Milestones Index** subsection. |
| `milestones.md` (single file) | `context/milestones/milestone-N.md` | Split each milestone into its own doc; index them from Design. |
| (none) | `context/sprints/` | Create scaffolding; sprint planning happens close to execution. |
| `goals*.md` / goals | `context/backlog/backlog-N.md` stories | Convert each goal into a backlog story, preserving content and plan links. |
| `implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/` | (removed) | The starter no longer ships a plan template; do not recreate it. |
| `GOAL_*` plan folders | left as historical | Do not rewrite; preserve as execution history. |

The detailed, safety-bounded procedure for applying this mapping lives in [version-and-merge-policy.md](version-and-merge-policy.md#structural-migration-policy).

## Files To Inspect

Process files in this order, mapping old-era equivalents when the target is pre-seven-tier:

1. Root `README.md`
2. Root Agentic Rails identity or description files:
   - `AGENTIC_RAILS_README.MD`
   - `AGENTIC_RAILS.md`
   - `.agentic-rails.json`
3. `context/design.md` and its Milestones Index (old-era: `design.md` plus `milestones.md`)
4. Milestones: starter `context/milestones/*.md` against target `context/milestones/*.md` or a single `context/milestones.md`
5. Stories: starter `context/backlog/*.md` against target `context/backlog/*.md` or every `context/goals*.md`
6. Sprints: starter `context/sprints/*.md`; create the folder in the target if migrating
7. Tier 0: starter `context/dictations-tier-0/` against target `context/dictations-tier-0/` or `context/tier0/`
8. Support files whose names or shapes changed, such as `agent-thinking.md` (old-era `AgentThinking.md`)

Do not bulk-update historical implementation-plan folders.

## Files Not To Rewrite By Default

Do not rewrite or normalize completed implementation-plan folders, including:

- `context/implementation-plans/GOAL_*/` (old-era execution history)
- `context/implementation-plans/STORY_*/` (current-era execution history)
- the `plan.md`, `implementation-log.md`, `completion-review.md`, `complaining.md`, `thinking.md`, `evidence.md`, and `handover/` files inside them

Historical execution records preserve what the project knew at the time. Goal-named plan folders stay goal-named; renaming them would break their links and rewrite history. Only touch old implementation-plan folders when the user explicitly asks for historical migration.

## Missing Target Files

If the starter has a standard context surface that the target project is missing:

- Create missing framework identity files and starter templates (milestone, sprint, backlog, and dictation templates and their tier READMEs).
- Create the missing seven-tier folders (`milestones/`, `sprints/`, `backlog/`, `dictations-tier-0/`) when migrating, populating them from the old-era equivalents rather than from blank placeholders.
- Create new context files only when doing so will not fabricate project-specific content. Use starter content only as scaffolding and mark placeholders honestly.
- Report created files.

Do not invent arbitrary backlog or milestone documents beyond what the target's existing content (or the starter template) justifies.

## README Handling

Root `README.md` is risky because derived projects often replace it with project-specific content.

When updating `README.md`:

- Never overwrite the whole file by default.
- Look for a clearly marked Agentic Rails section or context-links section.
- Update only that section when present, refreshing links to the seven-tier surfaces (`context/milestones/`, `context/backlog/`, and so on).
- If no section exists, suggest or add a small Agentic Rails metadata section only when safe.
- Prefer keeping framework explanation in `AGENTIC_RAILS_README.MD`.
