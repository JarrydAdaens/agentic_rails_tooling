---
name: mermaid-mapper-state-model
version: 1.0
agentic_rails_source_version: 1.0
---

# Scoutmap row state model

Only the **Boss** (the agent executing `.workflows/mermaid-mapper/WORKFLOW.md`) mutates the first column of each data row in `scoutmap.md`.

## State emoji markers

| Emoji | Meaning |
| --- | --- |
| ⬜ | Unassigned: ready for the Boss to assign to a mapper |
| 🟩 | Assigned: a mapper owns this row; work in flight |
| ❎ | Completed: mapper output passed validation and partial is accepted |
| 🟥 | Failed: validation failed; see `logs/` for reasons |

## Transitions

| From | To | When |
| --- | --- | --- |
| ⬜ | 🟩 | Boss picks the row for the next mapper chunk |
| 🟩 | ❎ | Mapper partial passes validation; partial file stored |
| 🟩 | 🟥 | Mapper partial fails validation; Boss logs failure |
| 🟥 | (none in v1) | Terminal until a future **requeue** policy |

## Rules

- Do not hand-edit state while a workflow run is in progress unless you are recovering manually.
- **Resume**: if `scoutmap.md` already exists, the Boss continues from current emojis: rows still ⬜ need work; ❎ rows are skipped; 🟥 stay failed unless policy adds requeue.

## Policy (v1)

- **Failed rows are terminal.** Optional later extension: Boss may rewrite 🟥 back to ⬜ to retry.

## Related

- Row line format: `.skills/mermaid-scout/references/scoutmap-format.md`
