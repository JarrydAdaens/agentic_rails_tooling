---
name: rails-minion-workflow-verification-gates
description: Relevant deterministic checks and selective review evidence.
metadata:
  version: "2.0"
---

# Artifact checks

Select checks from the changed artifact and adopted project requirements. Run
meaningful deterministic checks before paid review. Repeat only affected checks
after a relevant change or to resolve a concrete failure.

| Changed artifact | Useful evidence |
| --- | --- |
| Documentation/configuration | Syntax, link, schema, or targeted lint checks; no unrelated application launch. |
| Library | Tests exercising affected behavior and consumers. |
| CLI/tool | A representative invocation through the changed path. |
| UI/game | Relevant build plus runtime/UI evidence where the change needs it. |
| Service/API | Tests and the changed runtime/endpoint where applicable. |
| Infrastructure/migration | Preview, compatibility checks, rollback, and bounded environment evidence. |

Record command, outcome, environment limits, and artifact identity. Distinguish
preexisting failures from new regressions. An unavailable required check is an
error; an optional missing check is a stated limitation. Review outcomes are
`PASS`, `FAIL`, `ERROR`, or an explicitly authorized `WAIVED`.

Bind any selected independent review to the diff, relevant configuration,
accepted user decisions, and ownership. A reviewer cannot require forbidden
scope expansion. A metadata update by the status owner is not a reason to rerun
unrelated implementation tests; changes to checked content invalidate its evidence.

Commit policy belongs to the [completion contract](completion-contract.md).
Passing checks does not itself authorize a commit.
