---
name: implementation-plan-executor-state-model
version: 1.0
agentic_rails_source_version: 1.0
---

# Progress row state model

Only the **Boss** mutates the `Status` column in `documentation/workflows/implementation_plan_executor/progress.md`.

## Status values

| Status | Meaning |
| --- | --- |
| `TODO` | Ready for the Boss to assign to a worker |
| `DOING` | Assigned to a worker and currently in flight |
| `DONE` | Worker finished successfully, verification passed, and any required commit exists |
| `BLOCKED` | Worker could not finish or the result was not acceptable; see `logs/` |

## Transitions

| From | To | When |
| --- | --- | --- |
| `TODO` | `DOING` | Boss dispatches the goal to a worker |
| `DOING` | `DONE` | Worker result is accepted and the required commit exists when files changed |
| `DOING` | `BLOCKED` | Worker is blocked, validation fails, or changed files exist without an acceptable commit |
| `BLOCKED` | `TODO` | Boss explicitly requeues after a deliberate retry decision |

## Rules

- Do not mark a goal `DONE` before the worker result is reviewed.
- Do not mark a goal `DONE` if files changed and no real commit exists.
- Do not mark a source checklist item complete before the corresponding progress row is `DONE`.
- Preserve goal ids exactly when they came from source documents.
- Synthetic ids such as `STEP-001` are stable once created.

## Resume

- If `progress.md` already exists, resume from its current rows.
- `TODO` rows still need work.
- `DOING` rows should be checked and either resumed or rewritten intentionally by the Boss because those rows were already dispatched.
- `DONE` rows are skipped.
- `BLOCKED` rows stay blocked until the Boss intentionally requeues them.
