---
name: rails-planning-questions-format
metadata:
  version: "1.1"
---

# Per-Plan Questions File Format (Opt-In)

By default, open questions live inline in `plan.md`'s own `## Questions / Unknowns` section — see [plan-template.md](plan-template.md). A standalone `questions.md` is **not** created by default; use this format only when the user explicitly asks for one, or the story is large/phased enough that a separately-tracked questions file is genuinely justified.

When created, `questions.md` lives beside `plan.md` under `context/implementation-plans/<milestone-slug>/<story-slug>/`.

The file is plan-local. It captures open questions discovered while writing or executing this specific plan so the human or a follow-up agent can answer them and revise the plan without losing context.

## File shape

```md
# Questions — <Task Name>

- Plan: `<relative path to plan.md>`
- Story/Work ID: `<story-id or work-id>`
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

- Only create this file when explicitly requested or genuinely justified by story size/phasing (see the note above). Otherwise use `plan.md`'s `## Questions / Unknowns` section instead.
- Set `Status: NONE` and write `_No open questions._` when the plan has no gaps.
- Set `Status: OPEN` when one or more questions are unanswered.
- Set `Status: RESOLVED` when all questions have been answered and the plan updated.
- Record the same temporary assumption in the plan's `## Questions / Unknowns` section so the uncertainty is visible in both places.
- Update this file when answers arrive, not only when questions are created.
- Do not delete answered questions. Move them under a `## Resolved` heading if the list grows long.

## Example — open questions

```md
# Questions — Add Report Export Support

- Plan: `plan.md`
- Story/Work ID: `STORY_2_3`
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
- Story/Work ID: `BUG_fix-login-token-refresh`
- Status: `NONE`
- Last Updated: `07 May 2026`

_No open questions._
```
