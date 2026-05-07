---
name: rails-planning-questions-format
version: 1.0
---

# Per-Plan Questions File Format

Use this format for `questions.md` created beside every `plan.md` under `Documentation/implementation_plans/<task-folder>/`.

The file is plan-local. It captures open questions discovered while writing or executing this specific plan so the human or a follow-up agent can answer them and revise the plan without losing context.

## File shape

```md
# Questions — <Task Name>

- Plan: `<relative path to plan.md>`
- Goal: `<goal-id or task-id>`
- Status: `OPEN | NONE | RESOLVED`
- Last Updated: `<DD Month YYYY>`

Use this file to record open questions discovered while writing or executing this plan.
Answer these later — the human or a follow-up agent can revise the plan once answers are available.

## Questions

- Q: `<question text>`
  Impact: `<why the answer matters to the plan>`
  Assumption: `<temporary assumption written into the plan>`
  Status: `OPEN | ANSWERED`
  Answer: `<answer when known — leave blank until answered>`
```

## Rules

- Create this file beside every new `plan.md`, even when no questions exist.
- Set `Status: NONE` and write `_No open questions._` when the plan has no gaps.
- Set `Status: OPEN` when one or more questions are unanswered.
- Set `Status: RESOLVED` when all questions have been answered and the plan updated.
- Record the same temporary assumption in the plan's `Risks And Open Questions` section so the uncertainty is visible in both places.
- Update this file when answers arrive, not only when questions are created.
- Do not delete answered questions. Move them under a `## Resolved` heading if the list grows long.

## Example — open questions

```md
# Questions — Add Report Export Support

- Plan: `plan.md`
- Goal: `GOAL_2_3`
- Status: `OPEN`
- Last Updated: `07 May 2026`

## Questions

- Q: Should CSV export include soft-deleted records?
  Impact: Determines whether the query must join the archive table.
  Assumption: Soft-deleted records are excluded until confirmed otherwise.
  Status: OPEN
  Answer:

- Q: Is there a maximum export row limit enforced at the API level?
  Impact: The export endpoint may need pagination or a streaming response.
  Assumption: Limit of 10 000 rows assumed for now.
  Status: OPEN
  Answer:
```

## Example — no questions

```md
# Questions — Fix Login Token Refresh

- Plan: `plan.md`
- Goal: `BUG_fix-login-token-refresh`
- Status: `NONE`
- Last Updated: `07 May 2026`

_No open questions._
```
