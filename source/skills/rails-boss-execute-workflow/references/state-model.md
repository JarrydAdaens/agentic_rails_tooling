---
name: rails-boss-execute-state-model
description: Progress row state values, transitions, and resume semantics for the Boss execute workflow.
metadata:
  version: "2.0"
---

# Progress Row State Model

Only the **Boss** mutates the `Status` column in `context/_boss-runs/<run-slug>/progress.md`.

## Status values

| Status | Meaning |
| --- | --- |
| `TODO` | Ready for the Boss to assign to a worker |
| `DOING` | Assigned to a worker and currently in flight |
| `VERIFYING` | Worker returned; the independent verifier has been dispatched and has not yet been accepted |
| `DONE` | Verifier returned `PASS` or `PASS WITH NOTES`, and any required commit exists |
| `BLOCKED` | Verifier returned `BLOCK`, the worker could not finish, or the result was not acceptable; see `logs/` |

## Transitions

| From | To | When |
| --- | --- | --- |
| `TODO` | `DOING` | Boss dispatches the story to a worker |
| `DOING` | `VERIFYING` | Worker returns and the Boss dispatches the verifier |
| `DOING` | `BLOCKED` | Worker reports a blocker, or changed files exist without an acceptable commit |
| `VERIFYING` | `DONE` | Verdict is `PASS` or `PASS WITH NOTES` with cited evidence |
| `VERIFYING` | `BLOCKED` | Verdict is `BLOCK` |
| `BLOCKED` | `TODO` | Boss explicitly requeues after a deliberate retry decision |

`VERIFYING` exists so that a Boss whose context was compacted between the worker's return and the verifier's verdict can tell, from `progress.md` alone, that the story still needs judging. Without it, that row is indistinguishable from one still in flight.

## Rules

- Do not mark a story `DONE` on the worker's own report. Only a verifier verdict moves a row out of `VERIFYING`.
- Do not mark a story `DONE` if files changed and no real commit exists.
- Do not mark a story `DONE` on a verdict with no cited evidence, or one whose gaps mean the acceptance criteria were never actually checked. That result is unverifiable: record what could not be checked and escalate.
- Do not mark a source checklist item complete before the corresponding progress row is `DONE`.
- Write the row's new state to `progress.md` before starting the next thing, never after.
- Preserve story ids exactly when they came from source documents. Synthetic ids such as `STEP-001` are stable once created.
- The `Model` column records what a worker actually ran on. Correct it downward to `inherited (unresolved)` if a requested override did not take; never leave a model there that was only requested.
- The `Verdict` column records the verifier's verdict, or `skipped` when `--verify off` is in effect. It stays blank until verification runs — never fill it ahead of the verdict.
- After three failed verifications of the same story, the row stays `BLOCKED` and the run continues with the next runnable story. Do not requeue a fourth time, and do not end the run over one blocked row.

## Resume

Resume is **per run slug**, not per repository. A `progress.md` belongs to exactly one run folder, and the Boss only opens one when the user named that run slug via `--resume`. Finding a run folder from a previous invocation is not permission to continue it — see the run-slug rules in `SKILL.md`.

Within a named run:

- If `progress.md` already exists, resume from its current rows.
- `TODO` rows still need work.
- `DOING` rows were already dispatched — check them and either resume or rewrite them intentionally.
- `VERIFYING` rows have a worker result to judge. Re-dispatch the verifier against the recorded commit SHA; do not re-run the worker.
- `DONE` rows are skipped.
- `BLOCKED` rows stay blocked until the Boss intentionally requeues them.
