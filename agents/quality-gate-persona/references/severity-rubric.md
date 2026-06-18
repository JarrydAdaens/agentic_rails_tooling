# Severity Rubric

## Purpose

Use this rubric to rank findings consistently.

## Severities

`BLOCK` means the changeset should not be committed until resolved or explicitly accepted by the human owner. Use for:

- Build breaks.
- Test failures caused by the changeset.
- Data loss, corruption, unsafe migrations, or irreversible side effects.
- Security, privacy, credential, licensing, or IP exposure.
- Hard architectural boundary violations.
- Scope violations that would mislead reviewers.
- Missing core behavior required by the plan.

`MAJOR` means a real defect or rule violation should be fixed before ordinary review, but the changeset is not necessarily catastrophic. Use for:

- Missed edge cases called out by the plan.
- Incorrect architecture or wiring that is likely to fail.
- Meaningful convention or rule violations.
- Insufficient tests for risky changed behavior.
- Unverified but likely correctness issues.

`MINOR` means the issue is safe to commit with notes when the operator accepts the tradeoff. Use for:

- Small style, naming, or clarity issues.
- Harmless deviations from local convention.
- Low-risk TODOs or documentation gaps.
- Validation gaps that do not threaten the current change.

Always order findings `BLOCK`, then `MAJOR`, then `MINOR`.
