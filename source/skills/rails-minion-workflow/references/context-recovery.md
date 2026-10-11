---
name: rails-minion-workflow-context-recovery
description: Evidence to reload after an interruption or context reset.
metadata:
  version: "2.0"
---

# Context recovery

Reload the active request, commit/review policy, chosen status owner, active plan
when needed, completion receipt, current HEAD/diff, and the relevant source/tests.
Load design context only for affected decisions. Compaction is optional and
cannot prove that verification is independent.

A fresh agent needs to establish which item is active, what was changed, which
checks ran against which identity, whether completion delivery or a commit is
pending, and which dependencies remain. Use the tracker's established syntax;
no separate local story table is needed for an external status owner.

Reconcile evidence before taking the next item. An authorized commit containing
the sealed receipt and terminal source metadata proves completion even if the
previous turn ended before reporting it. A no-commit result is valid while its
recorded diff identity matches; modified artifacts require appropriate renewed
checks. A completed historical commit is not undone by an unrelated new HEAD.
