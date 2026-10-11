---
name: rails-boss-execute-workflow
description: >-
  Use this workflow when the user explicitly requests delegated implementation
  of a bounded set of Agentic Rails work items, with durable coordination,
  relevant checks, and recoverable completion.
disable-model-invocation: true
argument-hint: "<work request> [--serial|--parallel N] [--limit N] [--resume <run-slug>] [--require <skill>,...] [--verify auto|required|off] [--commit none|single|batch] [--model <name>] [--clean]"
metadata:
  version: "3.0"
---

# Rails Boss Execute Workflow

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents ("finish these three with
no commits" means the named queue and `--commit none`).

| Token | Meaning |
| --- | --- |
| `--serial` | One active implementation worker; this is the default. |
| `--parallel N` | Explicit maximum active implementation workers, limited by host capacity and disjoint ownership. Absent means one. |
| `--limit N` | Maximum items from the authorized queue. Absent means only the finite named scope, never the whole backlog by inference. |
| `--resume <run-slug>` | Continue that run. Absent means resolve an explicitly requested continuation from existing evidence, or create a collision-free run. |
| `--require <skill>,...` | Additional worker skills. Absent means only requirements applicable to the chosen artifacts. |
| `--verify auto|required|off` | Independent review policy; default `auto` selects one review for consequential work. `off` disables optional paid review, never deterministic checks or an adopted required gate. |
| `--commit none|single|batch` | Run policy: leave verified work uncommitted, commit a completed item, or commit a coherent authorized batch. Absent means use existing session authority; without commit authorization use `none`. The switch does not override a user's prohibition. |
| `--model <name>` | Request an authorized, available worker override. Absent means runtime inheritance. |
| `--clean` | Retire the identified owned run state after preserving its evidence; begin a fresh run. Absent means preserve it. Never delete product outputs or unrelated work. |
| anything else | Named documents, stories, plans, or requested work. Empty arguments use established session scope; investigate known paths before asking if scope remains ambiguous. |

## References

- [State and recovery](references/state-model.md)
- [Completion transaction](references/completion-contract.md)
- [Runtime model selection](references/model-selection.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Activation authorizes bounded delegation for the named work. Give each worker
  exact files/responsibility, dependencies, acceptance checks, user decisions,
  commit policy, and stop conditions. Workers share the codebase and preserve
  others' edits. Serialize overlap instead of relying on parallelism alone.
- Establish one status owner before dispatch: the existing tracker, milestone,
  plan, or a run queue when none exists. When an external tracker owns status,
  link its items; local receipts are delivery evidence, not a mirrored backlog.
- Existing session authorization governs commits. Workers return verified
  changes; the coordinator owns completion metadata and any authorized commit.
  `commit-log` supplies wording only when a commit is authorized. No commit is
  required for a verified no-commit result.
- Use deterministic artifact-specific checks first. Review is selective and
  scoped to the actual diff, configuration, acceptance criteria, and accepted
  user decisions. Missing required evidence is `ERROR`, never approval. Record
  explicit waivers with their authority; never manufacture a passing check.
- Freeze verified identity and prepare recovery state before finalizing source
  status. Include terminal metadata in any authorized completion commit. On
  restart reconcile the transaction with actual Git/diff identity before
  redispatching or declaring completion.
- Discover runtime controls and inherit model/effort by default. Record requested
  and observed identities separately; unknown observation stays unknown.
- Keep work inside the finite queue and declared budget. Two attempts without
  new evidence change the approach; preserve the blocker and continue independent
  authorized items. Do not create extra planning, review, or investigation work
  simply to keep a run active.
- Compaction follows context pressure and supported host behavior. Checkpoint
  before interruption; a reset is neither a required stage nor independent review.

## Setup

Read named source material and the target repository's instructions. Inspect
HEAD, staged/unstaged changes, and untracked files; record preexisting dirty work.
Resolve the queue, status owner, relevant checks, review policy, commit authority,
and any specialist persona requirement once.

All paths below are relative to the target repository root. If a run record is
needed, use `context/_boss-runs/<run-slug>/briefing.md` with a kebab-case collision-free
slug. Record source links, scope, exclusions, ownership, decisions, policies,
active worker identities, and delivery-record paths. Use `progress.md` only when
it is the chosen status owner. Established trackers need no second status table.

## Execution

1. Select eligible items within scope and dependencies. Record dispatch intent
   and worker ownership durably before spawning.
2. Dispatch one worker per coherent slice at the declared concurrency cap.
   Invoke required skills/personas by name or supply their relevant contract
   inline; do not pass machine-specific paths to deployed artifacts.
3. On return inspect changed files and deterministic check evidence. Routine
   work can proceed from those checks. At a consequential boundary, dispatch one
   read-only reviewer with the scoped diff and accepted decisions. A reviewer
   may identify a scope conflict; it may not demand forbidden edits.
4. Complete through the transaction reference, using a commit SHA or verified
   diff identity according to policy. Update the sole status owner through its
   supported interface; record unavailable external updates as pending delivery.
5. Select the next eligible item. Finish with completed, partial, and blocked
   results, evidence identities, actual commit outcomes, and remaining decisions.

## Surviving compaction

The chosen status owner, `briefing.md` when created, and the explicitly located
completion receipts carry durable state. Write them before the next dispatch or
completion mutation. Reload those records and current Git state on continuation.
If exactly one run matches a request to continue, use it; investigate multiple
candidates before asking. Preserve run records while they are the only evidence
for no-commit work or a pending delivery.

## Observable results

Each accepted item has relevant check evidence bound to its artifact identity,
a reconciled completion record, and one authoritative status location. The final
report distinguishes committed and verified uncommitted work, optional review,
missing checks, and pending tracker delivery.
