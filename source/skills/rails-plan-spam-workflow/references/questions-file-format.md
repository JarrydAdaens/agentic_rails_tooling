---
name: rails-plan-spam-questions-file-format
metadata:
  version: "3.0"
---

# Questions Index Structure

`rails-plan-spam-workflow` uses a two-level questions structure.

## Level 1 — Per-plan `## Questions / Unknowns`

Each worker (following `rails-planning` conventions) records open questions directly inside its own `plan.md`, under `## Questions / Unknowns`:

```text
context/implementation-plans/<milestone-slug>/<story-slug>/plan.md
```

This section is owned by the plan. It records only the questions for that specific story or work item. There is no standalone per-plan `questions.md` by default — that file stays opt-in per `rails-planning` conventions, for stories that genuinely need a durable, separately-tracked questions log.

## Level 2 — Run-folder questions index

The Boss maintains a questions index inside each involved milestone's planning-run folder:

```text
context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/questions.md
```

This file does two things:

1. **Index** — links to each plan's `## Questions / Unknowns` section with current status so the user has one place to survey all open questions across the run.
2. **Boss questions** — cross-cutting questions that span multiple stories, affect sequencing, or require answers before any worker proceeds.

This index is a run-scoped convenience artifact, not a durable one. Deleting the `_planning-runs/<run-slug>/` folder after the run completes loses the aggregated overview, never the underlying questions, which remain inside each accepted `plan.md`.

## Run-folder questions.md shape

```md
# Plan Spam Questions — <Milestone Name>, Run <run-slug>

Milestone: `context/implementation-plans/<milestone-slug>/`
Run: `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/`
Date: `<YYYY-MM-DD>`
Source: `<source documents>`

Per-plan questions live inside each plan's `## Questions / Unknowns` section under
`context/implementation-plans/<milestone-slug>/`. This file indexes them and carries
cross-run Boss questions.

## Per-Plan Questions Index

| Story | Plan Folder | Questions | Status |
| --- | --- | --- | --- |
| STORY 3.4 | `context/implementation-plans/milestone-1/story-3-4-slug/` | [plan.md#questions--unknowns](../../story-3-4-slug/plan.md#questions--unknowns) | OPEN |
| STORY 3.5 | `context/implementation-plans/milestone-1/story-3-5-slug/` | [plan.md#questions--unknowns](../../story-3-5-slug/plan.md#questions--unknowns) | NONE |

## Boss Questions

Cross-cutting questions that apply to multiple plans, affect sequencing, or must be answered before workers proceed.

- Q: `<question text>`
  Affects: `<STORY-ID, STORY-ID>`
  Assumption: `<temporary assumption>`
  Status: `OPEN | ANSWERED`
  Answer: `<answer when known>`
```

## Rules

- Workers write to their own plan's `## Questions / Unknowns` section. They do not write to the run-folder index directly.
- After reviewing each worker, the Boss updates the index row status (`OPEN` or `NONE`) to reflect that plan's `## Questions / Unknowns` section.
- Boss questions are pre-flight or cross-run. Add them before dispatching workers when the source material raises concerns that span stories.
- The Boss may add a Boss question mid-run if a worker's output reveals a cross-cutting concern.
- The index `Status` column is updated by the Boss only, by reading each plan's `## Questions / Unknowns` section after worker acceptance.
- Use `OPEN` when any unanswered question remains in that section. Use `NONE` when the section is empty or explicitly states none were needed.
