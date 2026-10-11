---
name: rails-boss-execute-state-model
description: Single-owner dispatch, acceptance, and continuation state.
metadata:
  version: "3.0"
---

# State and recovery

Choose the existing source tracker as status owner where possible. Otherwise a
run's `progress.md` may own the queue. Other views contain links and evidence,
not independently edited status copies. Only the coordinator mutates owned queue
state; workers report their result and preserve unrelated changes.

| State | Meaning and evidence |
| --- | --- |
| TODO | Named item is eligible within the bounded queue. |
| DOING | Worker lease/identity and ownership recorded before dispatch. |
| CHECKING | Result exists; relevant deterministic checks or selected review remain. |
| COMPLETING | Completion transaction exists; metadata, commit, or tracker delivery remains. |
| DONE | Required checks and chosen completion policy reconciled with artifact identity. |
| BLOCKED | Concrete missing dependency, failed gate, or repeated failed approach is recorded. |

Use the tracker's existing vocabulary when it has one. A read-only delivery
receipt can expose these transaction stages without claiming ownership of the
tracked story state.

On continuation inspect live workers before creating another lease. Reconcile
`COMPLETING` using the [completion contract](completion-contract.md). A successful
Git commit can be recognized after a crash without another implementation pass.
A failed commit leaves preserved work and a pending transaction, not `DONE`.
Verified no-commit work needs its recorded diff identity; later changed content
requires new checks or a recorded superseding result.

Checks and review bind to artifact content, configuration, and user decisions.
Material changes invalidate affected evidence; unrelated new commits do not
automatically require a full new review. A missing tool for a required check is
an error with a next action. Optional review can be omitted under run policy.

Blocked items stay blocked until their evidence or dependency changes. Retry only
with a concrete new approach or newly available prerequisite; never blindly
restart completed work after compaction.
