---
name: rails-minion-workflow-story-lifecycle
description: Bounded implementation and completion transitions.
metadata:
  version: "2.0"
---

# Story lifecycle

Resolve an eligible item and record ownership before changing files. Use an
existing plan or create one only when it improves substantial work. Implement,
run relevant checks, select independent review where warranted, and prepare the
[completion transaction](completion-contract.md).

| Stage | Resume behavior |
| --- | --- |
| Working | Inspect preserved baseline, live diff, and active owner before resuming. |
| Checking | Run missing or invalidated checks; do not redo accepted implementation. |
| Preparing completion | Receipt exists before terminal metadata. Finish metadata and seal against the verified identity. |
| Commit pending | Verify Git first. A failed commit preserves the pending result; retry only the authorized delivery step. |
| Verified uncommitted | Compare recorded artifact/diff identity and retain no-commit policy. |
| Completed committed | Recognize the exact receipt/artifacts in an ancestor commit; do not redispatch. |
| Blocked | Preserve evidence and select an independent authorized item. |

The source tracker owns story state. Local receipt stages describe delivery,
which can be pending even after implementation and checks have finished. If an
external status API is unavailable, report pending delivery with its source link;
do not invent a local completed mirror.

Compaction is not a lifecycle stage. Checkpoint whenever interruption or context
pressure makes it useful, and reload the evidence after continuation.
