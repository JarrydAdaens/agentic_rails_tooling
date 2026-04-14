---
name: plan-spam-state-model
version: 1.0
---

# Progress row state model

Only the **Boss** mutates the `Status` column in `documentation/workflows/plan_spam/progress.md`.

## Status values

| Status | Meaning |
| --- | --- |
| `TODO` | Ready for the Boss to assign to a planning worker |
| `DOING` | Assigned to a worker and currently in flight |
| `DONE` | Worker finished successfully and the output plan file was accepted |
| `BLOCKED` | Worker could not finish, produced an unacceptable plan, or hit a collision or missing-context problem; see `logs/` |

## Transitions

| From | To | When |
| --- | --- | --- |
| `TODO` | `DOING` | Boss dispatches the goal to a planning worker |
| `DOING` | `DONE` | Worker result is accepted, the plan file exists at the expected path, and any open questions were captured in `questions.md` |
| `DOING` | `BLOCKED` | Worker is blocked, output is missing, output is duplicate, wrong template was used, the plan is too shallow, or required questions were not captured |
| `BLOCKED` | `TODO` | Boss explicitly requeues after a deliberate retry decision |

## Rules

- Do not mark a row `DONE` before the worker result is reviewed.
- Do not mark a row `DONE` if the output file is missing or clearly does not follow the assigned template.
- Do not mark a row `DONE` if visible uncertainty exists but the worker failed to capture the corresponding questions in `documentation/workflows/plan_spam/questions.md`.
- A row may still be `DONE` while questions remain unanswered if the plan is still useful and the uncertainty is marked honestly.
- Preserve goal ids exactly when they came from source documents.
- Synthetic ids such as `PLAN-001` are stable once created.

## Resume

- If `progress.md` already exists, resume from its current rows.
- `TODO` rows still need work.
- `DOING` rows should be checked and either resumed or rewritten intentionally by the Boss because those rows were already dispatched.
- `DONE` rows are skipped.
- `BLOCKED` rows stay blocked until the Boss intentionally requeues them.
