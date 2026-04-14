---
name: plan-spam-questions-file-format
version: 1.0
---

# Shared Questions File Format

Use this format for `documentation/workflows/plan_spam/questions.md`.

The file is shared across the whole run.
Every queued goal gets its own section before workers start.
Every question must include the exact goal id so the user can answer later and a follow-up agent can revise the matching plans.

## File shape

```md
# Plan Spam Questions

Use this file to collect clarifying questions discovered during bulk planning.
The user answers these later after the planning pass is complete.

## <GOAL-ID> - <Short Goal Title>

Status: OPEN

- Question 1: <question text>
  Impact: <why the answer matters to the plan>
  Assumption used for now: <temporary assumption written into the plan>

- Question 2: <question text>
  Impact: <why the answer matters to the plan>
  Assumption used for now: <temporary assumption written into the plan>

## <GOAL-ID> - <Short Goal Title>

Status: NONE

- No open questions.
```

## Rules

- Preserve the exact goal id in every section heading.
- Use `Status: OPEN` when one or more unanswered questions remain.
- Use `Status: NONE` when the worker genuinely has no open questions.
- Keep the wording concise and answerable.
- Record the same assumption in the plan's open-questions section so the uncertainty is visible in both places.
- Update only the assigned goal section unless the Boss explicitly says otherwise.
