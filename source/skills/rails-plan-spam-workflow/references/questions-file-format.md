---
name: rails-plan-spam-questions-file-format
metadata:
  version: "2.2"
---

# Questions File Structure

`rails-plan-spam-workflow` uses a two-level questions structure.

## Level 1 — Per-plan questions.md

Each worker (following `rails-planning` conventions) creates a `questions.md` file beside its `plan.md`:

```text
context/implementation-plans/<task-folder>/questions.md
```

This file is owned by the plan. It records only the questions for that specific goal.

Format is defined in `skills/rails-planning/references/questions-format.md`.

## Level 2 — Run-folder questions index

The Boss maintains a questions index inside the run folder:

```text
context/plan-spam-<slug>/questions.md
```

This file does two things:

1. **Index** — links to every per-plan `questions.md` with current status so the user has one place to survey all open questions across the run.
2. **Boss questions** — cross-cutting questions that span multiple goals, affect sequencing, or require answers before any worker proceeds.

## Run-folder questions.md shape

```md
# Plan Spam Questions — <Run Folder Name>

Run: `context/plan-spam-<slug>/`
Date: `<YYYY-MM-DD>`
Source: `<source documents>`

Per-plan questions live beside each plan under `context/implementation-plans/`.
This file indexes them and carries cross-run Boss questions.

## Per-Plan Questions Index

| Goal | Plan Folder | Questions File | Status |
| --- | --- | --- | --- |
| GOAL 3.4 | `context/implementation-plans/GOAL_3_4_slug/` | [questions.md](../../../implementation-plans/GOAL_3_4_slug/questions.md) | OPEN |
| GOAL 3.5 | `context/implementation-plans/GOAL_3_5_slug/` | [questions.md](../../../implementation-plans/GOAL_3_5_slug/questions.md) | NONE |

## Boss Questions

Cross-cutting questions that apply to multiple plans, affect sequencing, or must be answered before workers proceed.

- Q: `<question text>`
  Affects: `<GOAL-ID, GOAL-ID>`
  Assumption: `<temporary assumption>`
  Status: `OPEN | ANSWERED`
  Answer: `<answer when known>`
```

## Rules

- Workers write to their own plan-local `questions.md`. They do not write to the run-folder index directly.
- After reviewing each worker, the Boss updates the index row status (`OPEN` or `NONE`) to reflect the per-plan file.
- Boss questions are pre-flight or cross-run. Add them before dispatching workers when the source material raises concerns that span goals.
- The Boss may add a Boss question mid-run if a worker's output reveals a cross-cutting concern.
- The index `Status` column is updated by the Boss only, by reading the per-plan `questions.md` status after worker acceptance.
- Use `OPEN` when any unanswered question remains in that plan's file. Use `NONE` when the per-plan file has `Status: NONE`.
