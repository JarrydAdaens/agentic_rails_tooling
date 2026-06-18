---
name: complaining-path-selection
metadata:
  version: "1.0"
---

# Complaint Log Path Selection

Choose the complaint log path inside the target project, not inside the reusable tooling repository unless the tooling repository itself is the target.

## Selection Order

1. Use a user-specified complaint log path or implementation-plan folder.
2. If the repository follows Agentic Rails and an active implementation-plan folder is identifiable, write `complaining.md` in that folder.
3. If the repository follows Agentic Rails but no active implementation-plan folder is identifiable, write `context/complaining.md`.
4. In other repositories, use an obvious existing context or documentation folder in this order:
   - `context/`
   - `documentation/`
   - `docs/`
   - `Docs/`
5. If no context or documentation folder exists, create `context/`.

The complaint log filename is always:

```text
complaining.md
```

## Examples

```text
context/implementation-plans/GOAL_1_2_short-slug/complaining.md
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

If the repository uses Agentic Rails, prefer the active implementation-plan folder:

1. Use a user-specified implementation-plan folder.
2. Use the only non-template folder under `context/implementation-plans/`.
3. Use the most recently modified non-template folder under `context/implementation-plans/`.
4. If multiple folders remain plausible and the choice affects where `complaining.md` will be written, ask the user before writing.

Ignore `IMPLEMENTATION_PLAN_TEMPLATE` when detecting active plan folders.

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
