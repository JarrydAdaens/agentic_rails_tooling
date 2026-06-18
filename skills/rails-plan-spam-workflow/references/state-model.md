---
name: rails-plan-spam-state-model
version: 2.1
agentic_rails_source_version: 2.1
---

# Progress Row State Model

Only the **Boss** mutates the `Status` column in `context/plan-spam-<slug>/progress.md`.

The run folder (`context/plan-spam-<slug>/`) is unique per invocation. See the run folder naming rules in `skills/rails-plan-spam-workflow/SKILL.md`.

## Status values

| Status | Meaning |
| --- | --- |
| `TODO` | Ready for the Boss to assign to a planning worker |
| `DOING` | Assigned to a worker and currently in flight |
| `DONE` | Worker finished successfully and all three output files were accepted |
| `BLOCKED` | Worker could not finish, produced an unacceptable plan, or hit a collision or missing-context problem; see `logs/` |

## Transitions

| From | To | When |
| --- | --- | --- |
| `TODO` | `DOING` | Boss dispatches the goal to a planning worker |
| `DOING` | `DONE` | Worker result is accepted: `plan.md`, `implementation-log.md`, and `questions.md` all exist at expected paths, and the Boss updated the run-folder questions index |
| `DOING` | `BLOCKED` | Worker is blocked, any of the three output files is missing, wrong template was used, plan is too shallow, or required questions were not captured |
| `BLOCKED` | `TODO` | Boss explicitly requeues after a deliberate retry decision |

## Rules

- Do not mark a row `DONE` before the worker result is reviewed.
- Do not mark a row `DONE` if `plan.md`, `implementation-log.md`, or `questions.md` is missing from the plan folder.
- Do not mark a row `DONE` if the plan clearly does not follow `skills/rails-planning/references/plan-template.md` or the repository-local template.
- Do not mark a row `DONE` if visible uncertainty exists but the worker failed to capture corresponding questions in the plan-local `questions.md`.
- A row may still be `DONE` while questions remain unanswered as long as the plan is useful, the uncertainty is marked honestly, and the questions are in `questions.md`.
- Preserve goal ids exactly when they came from source documents.
- Synthetic ids such as `PLAN-001` are stable once created.

## Resume

- If `progress.md` already exists in the run folder, resume from its current rows.
- `TODO` rows still need work.
- `DOING` rows should be checked and either resumed or rewritten intentionally by the Boss because those rows were already dispatched.
- `DONE` rows are skipped.
- `BLOCKED` rows stay blocked until the Boss intentionally requeues them.
