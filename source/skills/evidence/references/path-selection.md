---
name: evidence-path-selection
metadata:
  version: "1.0"
---

# Evidence Path Selection

This reference applies only when a standalone `evidence.md` is genuinely warranted (see `SKILL.md`'s Artifact section). The default is to write inline into the active plan's `## Evidence / References` section — no path selection needed for that case.

Choose the `evidence.md` path inside the target project, not inside the reusable tooling repository unless the tooling repository itself is the target.

## Agentic Rails Detection

Treat a repository as using Agentic Rails when one or more of these markers exist at or near the project root:

- `AGENTIC_RAILS_README.MD`
- `AGENTIC_RAILS.md`
- `.agentic-rails.json`
- `context/implementation-plans/`
- `context/agenticworkflow.md`

## Active Plan Folder Selection

If the repository uses Agentic Rails, prefer the active implementation-plan story folder, nested under its milestone:

```text
context/implementation-plans/<milestone-slug>/<story-slug>/
```

1. Use a user-specified implementation-plan folder.
2. Use the only non-template story folder found by searching one level under each `context/implementation-plans/<milestone-slug>/`.
3. Use the most recently modified non-template story folder across all milestones.
4. If multiple folders remain plausible and the choice affects where `evidence.md` will be written, ask the user before writing.

Ignore `IMPLEMENTATION_PLAN_TEMPLATE` and `_planning-runs/` folders when detecting active plan folders — those are templates and temporary planning-run scratch space, not durable story folders.

Write `evidence.md` beside `plan.md` in that story folder, never in `context/` root.

## No Identifiable Plan Folder

When no active Agentic Rails plan folder is identifiable, do not default to writing `evidence.md` into `context/` root or a generic documentation folder — that is exactly the "dumped in `context/` root" pattern the framework's artifact policy forbids. Instead:

1. Ask the user which implementation-plan folder (or other specific work folder) the evidence belongs to.
2. If the user confirms there truly is no plan or work folder for this task, and still wants a standalone file, write it to the target project's context or documentation folder as an explicit last resort, in this order: `context/`, `documentation/`, `docs/`, `Docs/` — and say plainly that it was written outside any plan folder because none exists.

If `evidence.md` already exists, preserve it and append or update only the relevant sections.
