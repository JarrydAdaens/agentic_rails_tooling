---
name: complaining-path-selection
metadata:
  version: "1.0"
---

# Complaint Log Path Selection

This reference applies only when a standalone `complaining.md` is genuinely warranted (see `SKILL.md`'s "Standalone Artifact" section). The default is to raise friction directly to the user or append it to the active plan's `## Complaints / Friction` section — no path selection needed for that case.

Choose the complaint log path inside the target project, not inside the reusable tooling repository unless the tooling repository itself is the target.

## Selection Order

1. Use a user-specified complaint log path or implementation-plan folder.
2. If the repository follows Agentic Rails and an active implementation-plan folder is identifiable, write `complaining.md` in that story folder.
3. If the friction belongs to a planning run rather than one story, write it under that run's scoped folder: `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/complaining.md`.
4. If the repository follows Agentic Rails but no active implementation-plan folder or planning run is identifiable, use an obvious existing context or documentation folder (see step 5), and state plainly that it was written outside any plan or run folder because none exists — do not silently default to `context/complaining.md`.
5. In other repositories, use an obvious existing context or documentation folder in this order:
   - `context/`
   - `documentation/`
   - `docs/`
   - `Docs/`
6. If no context or documentation folder exists, create `context/`.

The complaint log filename is always:

```text
complaining.md
```

## Examples

```text
context/implementation-plans/milestone-1/story-1-2-short-slug/complaining.md
context/implementation-plans/milestone-1/_planning-runs/2026-07-02-plan-spam-run/complaining.md
context/complaining.md
documentation/complaining.md
docs/complaining.md
Docs/complaining.md
```

## Agentic Rails Detection

Treat a repository as using Agentic Rails when one or more of these markers exist at or near the project root:

- `AGENTIC_RAILS_README.MD`
- `AGENTIC_RAILS.md`
- `.agentic-rails.json`
- `context/implementation-plans/`
- `context/agenticworkflow.md`

## Active Plan Folder Selection

If the repository uses Agentic Rails, prefer the active implementation-plan story folder, nested under its milestone: `context/implementation-plans/<milestone-slug>/<story-slug>/`.

1. Use a user-specified implementation-plan folder.
2. Use the only non-template story folder found by searching one level under each `context/implementation-plans/<milestone-slug>/`.
3. Use the most recently modified non-template story folder across all milestones.
4. If multiple folders remain plausible and the choice affects where `complaining.md` will be written, ask the user before writing.

Ignore `IMPLEMENTATION_PLAN_TEMPLATE` and `_planning-runs/` folders when detecting active plan folders — those are templates and temporary planning-run scratch space, not durable story folders.

## Existing Files

If the file already exists, leave its current content in place and append future entries.

If the file exists but is empty, add at least:

```markdown
# Complaining Log
```

If the file has another reasonable heading or existing log structure, preserve it.

## Unclear Roots

When operating from a nested folder, inspect nearby project markers such as `.git`, solution files, package manifests, `AGENTS.md`, or existing documentation folders to identify the project root.

If multiple plausible roots exist and the choice affects where the complaint log will be written, choose the root that owns the current task. If that cannot be inferred safely, ask the user.
