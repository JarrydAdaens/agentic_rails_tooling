---
name: rails-minion-workflow
description: >-
  Use this workflow when the user explicitly requests one agent to implement a
  bounded set of Agentic Rails work sequentially, without delegated workers,
  preserving continuation state and honoring the run's commit policy.
disable-model-invocation: true
argument-hint: "<work or milestone> [--limit N] [--commit none|single|batch] [--review auto|required|off] [--resume]"
metadata:
  version: "2.0"
---

# Rails Minion Workflow

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and treat plain-language equivalents as equal to the tokens
("do these two yourself and leave them uncommitted" sets that queue and `--commit none`).

| Token | Meaning |
| --- | --- |
| `--limit N` | Maximum named items for this run. Absent means the finite requested scope; a named milestone can authorize its remaining items. |
| `--commit none|single|batch` | Honor the run's no-commit, item-commit, or coherent-batch policy. Absent means existing session authority; without commit authorization use `none`. |
| `--review auto|required|off` | Default `auto` selects one independent review for consequential work; `off` omits optional review only. |
| `--resume` | Continue the identified run from durable evidence. Absent means use the existing request context; do not infer unrelated work. |
| anything else | Work items or a milestone path/name. Empty arguments use established session scope; investigate before asking if no bounded request is identifiable. |

## References

- [Story lifecycle](references/story-lifecycle.md)
- [Artifact checks](references/verification-gates.md)
- [Context recovery](references/context-recovery.md)
- [Blocker handling](references/blocker-ladder.md)
- [Outcome report](references/intervention-report.md)
- [Completion transaction](references/completion-contract.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Implement one coherent item at a time within the authorized queue and budget.
  A milestone is optional when the request already defines useful work.
- Choose one status owner: existing tracker, milestone, or plan. Link external
  tracker items rather than creating parallel story state. Completion receipts
  are evidence of delivery, not another backlog.
- Preserve preexisting dirty, staged, and untracked work. Record its baseline
  before edits and stage only owned accepted changes if a commit is authorized.
- Use a plan only when it helps substantial work; use relevant deterministic
  checks for the changed artifact. Runtime changes need evidence through the
  affected path where available; docs-only work needs no invented application run.
- Review is selective. For a chosen consequential boundary, use one independent
  read-only reviewer with scope, acceptance criteria, and accepted user decisions.
  Missing required checks remain errors; waived requirements need explicit authority.
- Honor existing commit authorization once. Verified uncommitted completion is
  valid under `none`; authorized completion includes terminal metadata in the
  accepted commit and reconciles crash recovery before repeating work.
- Write continuation and completion state before the next mutation. Compact only
  for actual context pressure or supported host behavior, then reload from evidence.
  Compaction does not establish reviewer independence.
- Stop a repeated approach after two attempts without new evidence. Continue
  independent authorized items; do not expand scope into ceremonial planning or
  experiments merely because one item is blocked.

## Procedure

1. Inspect the request, target instructions, status owner, HEAD and dirty files.
   Establish bounds, dependencies, checks, commit policy, and review policy.
2. Reconcile existing active/completing work before choosing the next item. Use
   the lifecycle reference for continuation and the completion reference for
   identity/commit reconciliation.
3. Use an adequate existing plan, invoke `rails-planning` by name when needed,
   or implement the narrow request directly. Record material decisions where
   project truth already lives.
4. Implement and run artifact-specific checks. Add selected independent review
   only at the useful boundary. Preserve unavailable-check diagnostics accurately.
5. Prepare, seal, and reconcile the completion transaction. Publish through the
   sole status owner, then move to the next eligible item within the run bounds.
6. Report completed, partial, and blocked outcomes and their evidence identities.

## Surviving compaction

The chosen source status owner, the active plan when useful, and explicitly located
completion receipts hold continuation state. They record scope, user authority,
active item, baseline, verification identity, and pending delivery. Write before
an interruption and reload with current Git state after one. A progress sidecar
is unnecessary when the existing tracker already owns these facts.

## Observable results

Accepted work has relevant checks and either a reconciled commit or stable
verified diff identity. A fresh agent can identify remaining work without repeating
completed implementation. Unavailable checks, partial outcomes, and external
tracker delivery gaps remain visible.
