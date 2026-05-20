# Validation And Scope

Use this reference when starting `agentic-rails-update`, validating paths, or deciding which files are in scope.

## Source Starter Validation

Before comparing files, verify that the supplied source directory looks like `agentic_rails_context_starter`.

Strong signals include:

- `AGENTIC_RAILS_README.MD`
- `.agentic-rails.json`
- `Documentation/design.md`
- `Documentation/milestones.md`
- `Documentation/goals*.md`
- `Documentation/implementation_plans/`
- `Documentation/implementation_plans/plan.md`
- `Documentation/implementation_plans/implementation-log.md`

If the path does not look like the starter, stop and tell the user what was missing. Do not continue against an uncertain source path.

## Target Project Validation

Run from the derived child project unless the user explicitly provides a target project path.

Check whether the target appears Agentic Rails-derived using signals such as:

- `AGENTIC_RAILS_README.MD`
- `.agentic-rails.json`
- `Documentation/`
- `Documentation/design.md`
- `Documentation/milestones.md`
- `Documentation/goals*.md`
- `Documentation/implementation_plans/`

If the target does not clearly look derived from Agentic Rails, stop and ask the user whether this is the intended target.

Do not use this skill on the central `agentic_rails_context_starter` repository itself. Do not use it to update reusable skills, agents, rules, or workflow tooling; those belong to `agentic_rails_tooling`.

## Files To Inspect

Process starter files in this order:

1. Root `README.md`
2. Root Agentic Rails identity or description files:
   - `AGENTIC_RAILS_README.MD`
   - `AGENTIC_RAILS.md`
   - `.agentic-rails.json`
3. `Documentation/design.md`
4. `Documentation/milestones.md`
5. every starter `Documentation/goals*.md` file
6. every target `Documentation/goals*.md` file, to detect target-only goal documents that need metadata checks
7. current Tier 4 implementation-plan templates:
   - `Documentation/implementation_plans/plan.md`
   - `Documentation/implementation_plans/implementation-log.md`
   - other repository-local implementation-plan template files clearly marked as templates

Do not bulk-update every historical implementation-plan folder.

## Files Not To Rewrite By Default

Do not rewrite or normalize completed implementation-plan folders, including:

- `Documentation/implementation_plans/GOAL_*/plan.md`
- `Documentation/implementation_plans/GOAL_*/implementation-log.md`
- `Documentation/implementation_plans/GOAL_*/complaining.md`
- `Documentation/implementation_plans/GOAL_*/thinking.md`
- `Documentation/implementation_plans/GOAL_*/evidence.md`
- `Documentation/implementation_plans/GOAL_*/handover/`

Historical execution records preserve what the project knew at the time. Only touch old implementation-plan folders when the user explicitly asks for historical migration.

## Missing Target Files

If the starter has a standard context file that the target project is missing:

- Create missing files when they are framework identity files or template files.
- Create missing documentation files only when doing so will not fabricate project-specific content.
- Use starter content only as scaffolding.
- Mark placeholders honestly.
- Report created files.

For missing `goals*.md` files, do not create arbitrary new goal files unless the starter defines a standard template file and the target clearly lacks the template equivalent.

## README Handling

Root `README.md` is risky because derived projects often replace it with project-specific content.

When updating `README.md`:

- Never overwrite the whole file by default.
- Look for a clearly marked Agentic Rails section.
- Update only that section when present.
- If no section exists, suggest or add a small Agentic Rails metadata section only when safe.
- Prefer keeping framework explanation in `AGENTIC_RAILS_README.MD`.
