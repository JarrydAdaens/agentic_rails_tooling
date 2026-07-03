---
name: handover-path-selection
metadata:
  version: "1.0"
---

# Handover Path Selection

Choose the handover path inside the target project, not inside the reusable tooling repository unless the tooling repository itself is the target.

The default artifact path is:

```text
handover/shallow-handover.md
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
4. If multiple folders remain plausible and the choice affects where the handover will be written, ask the user before writing.

Ignore `IMPLEMENTATION_PLAN_TEMPLATE` when detecting active plan folders.

## Fallback Context Folder

When no active Agentic Rails plan folder is identifiable, write the handover under the target context or documentation folder.

Selection order:

1. `context/`
2. `documentation/`
3. `docs/`
4. `Docs/`
5. Create `context/` if no context or documentation folder exists.

Examples:

```text
context/handover/shallow-handover.md
documentation/handover/shallow-handover.md
docs/handover/shallow-handover.md
```
