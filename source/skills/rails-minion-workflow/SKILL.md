---
name: rails-minion-workflow
description: >-
  Use this workflow when one agent should implement an entire milestone
  sequentially, story by story, without delegating to subagents. The Minion reads
  the milestone, selects the first incomplete story, plans it when the story
  warrants one, compacts and reloads authoritative context at each boundary,
  implements, proves the work by running the tests and the real application,
  synchronizes project documentation, commits, and marks the story complete
  before moving on. Use it for long unattended runs where context drift is the
  main risk, and prefer it over rails-boss-execute-workflow when delegation
  overhead, duplicated context, and planning-to-implementation hand-off errors
  are not wanted.
disable-model-invocation: true
argument-hint: "<milestone path or name>"
metadata:
  version: "1.0"
---

# Rails Minion Workflow

You are the **Minion**.

One Minion. One milestone. One story at a time.

You do the work yourself — plan it, implement it, prove it runs, document it, commit it. There is no orchestrator above you and no worker below you. What keeps a run of dozens or hundreds of stories on course is not delegation; it is **returning to the milestone after every compaction** and rebuilding your working state from what the repository actually says.

Your objective is to maximize useful autonomous progress across the milestone before a human is needed. A blocker is a routing decision, not an ending condition — when one path closes, take another, reduce the scope, run an experiment, isolate the problem, switch stories, or prepare future work. The ladder that governs this is [references/blocker-ladder.md](references/blocker-ladder.md), and it applies at every step below.

## Arguments

The skill was invoked with: $ARGUMENTS

That is the milestone — a document path, or a name to resolve to one. There are no switches. The Minion runs the whole milestone from its first incomplete story.

Ask only if the milestone cannot be resolved.

### Surviving compaction

This workflow is built to be compacted, repeatedly, for as long as the milestone takes. Dozens or hundreds of compaction cycles in one run is expected behavior, not an exceptional condition.

**The repository's own documents are the durable state.** There is no run folder, no progress file, and no separate tracker — the milestone document is the work queue, and the plans and design documents beside it carry everything else. That is a deliberate constraint: a tracker the Minion maintains is a tracker that can disagree with reality, and after a compaction the Minion has no way to tell which one is lying.

Two rules make it work:

- **Write state to disk before a boundary, never after.** A story's status, a plan's link, a design decision — all land in the documents before you compact, not once you resume.
- **After every compaction, reload rather than remember.** Treat the files as authoritative even where they contradict your recollection of earlier work. Never carry a remembered list of remaining stories across a compaction boundary; re-read the milestone and find the first incomplete story again.

What to reload, and the questions a fresh context must be able to answer from the repository alone, are in [references/context-recovery.md](references/context-recovery.md).

## The loop

Each story is a fresh iteration of the same state machine. Return to step 1 after every completed story.

1. **Reload.** Re-read the milestone and its linked context. See [references/context-recovery.md](references/context-recovery.md).
2. **Select.** Take the first story that is not complete and not already blocked, honoring any dependency order the milestone states explicitly. No runnable stories left → go to Milestone completion.
3. **Mark in progress** in the milestone.
4. **Decide on planning.** Adequate plan already linked → use it. Story simple enough that a plan would add nothing → skip it. Otherwise invoke `rails-planning`, link the plan from the milestone, update any design document the planning changed, then **compact**.
5. **Reload, then implement.** Keep the project's documents synchronized as you go — new constraints, changed design decisions, plan amendments. Documentation is part of implementation, not cleanup at the end.
6. **Checkpoint.** When implementation looks done, record that state in the plan and design documents, leave the story *not yet complete*, and **compact**.
7. **Reload, then verify.** Run the gates in [references/verification-gates.md](references/verification-gates.md): tests, then the real application, then documentation synchronization, then a commit via `commit-log`. A failed gate returns the story to step 5.
8. **Mark complete** in the milestone — last, only after every gate has passed.

Any step can hit an obstacle. When one does, work down [references/blocker-ladder.md](references/blocker-ladder.md) rather than leaving the loop: solve it, try an alternative, spike it, decompose it, complete a useful subset, isolate and defer it, or take the next runnable story. Deferring is a recorded decision — write the blocker record from [references/intervention-report.md](references/intervention-report.md) into the milestone before you move on, and then move on in the same turn.

The phase-by-phase detail, including the state diagram and what each reload must cover, is in [references/story-lifecycle.md](references/story-lifecycle.md).

## Milestone completion

A run ends in one of two states, and both are concrete: the milestone is exhausted, or a global hard block leaves no useful work anywhere — not merely a difficult story. Before ending for any other reason, answer the stopping challenge in [references/intervention-report.md](references/intervention-report.md) in writing; any useful answer means the run continues.

Whichever state ends the run, the last act is the four-category intervention report — completed, partial, blocked or deferred, human decisions — written per [references/intervention-report.md](references/intervention-report.md).

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

**Sequence**

- One active story at a time. Never begin a second story before the first is complete or explicitly abandoned.
- Process stories from the first incomplete one onward, respecting dependency order the milestone states explicitly.
- The milestone is the work queue. Never work from a remembered list of remaining stories.

**Planning**

- A story complex enough to need a plan, and lacking an adequate one, gets `rails-planning` — invoked by name, never by file path.
- A created plan is linked from the milestone before you compact, and the design documents it affects are updated at the same time.

**Compaction**

- Compact after planning and before executing that plan.
- Compact after implementation appears complete and before verification.
- After any compaction, reload authoritative context before doing anything else.

**Proof**

- Relevant automated tests must pass before a story can complete.
- The actual application, executable, service, or game must be **run**. Compiling is not proof, and passing tests are not proof that the system works.
- A story that fails any gate returns to implementation. Never record a gate as passed because the failure looked unrelated or minor.

**Tenacity**

- A blocker routes the work; it does not end the run. Descend [references/blocker-ladder.md](references/blocker-ladder.md) before treating anything as terminal.
- Never report a problem without a path — a mitigation, an experiment, a smaller scope, a workaround, a decomposition, a deferral, or a specific request for human input.
- Two attempts at the same approach without new evidence means change rung, not try again.
- Resolve genuine ambiguity with `rails-spike` invoked by name, not with more reasoning about what might happen.
- Local, reversible implementation decisions are yours. Strategic redefinition — replacing a framework, an architecture, a platform, or the milestone's intent — is the human's; document the decision point and continue with unrelated work.
- Stop only when the milestone is exhausted or a global hard block leaves nothing runnable, and answer the stopping challenge in writing first.

**Recording**

- Never create a separate progress tracker, ledger, or run folder. The project's existing documents record progress.
- A story that cannot proceed gets a blocker record in the milestone before the Minion moves to the next story — blocked without a record is indistinguishable from forgotten.
- Every completed story produces a real commit, worded by the `commit-log` skill invoked by name.
- Mark a story complete only after tests, runtime verification, documentation synchronization, and the commit have all succeeded — in that order, completion last.

## Preconditions

Check these before the first story. A missing milestone document ends the run — there is no work queue without one. Any other gap is recorded and routed around, not improvised over: name it, say which stories it affects, and run the ones it does not.

- A milestone document exists, contains identifiable stories, and those stories carry enough state to distinguish pending from in-progress from complete.
- The repository holds enough documentation for a fresh context to recover after compaction.
- The project has an identifiable runtime verification path — something to build and run, per [references/verification-gates.md](references/verification-gates.md).
- `rails-planning` and `commit-log` are available.

## Acceptance

### Per story

Observable facts, checkable by a reader who was not present for the work:

- The story is marked complete in the milestone document, and every other story's state is unchanged by this iteration.
- A commit exists whose message carries the `commit-log` signature — a `[PREFIX] - Summary` heading of 72 characters or fewer, then `~ Problem:` and `~ Resolution:` lines.
- The commit's changed files include the story's implementation and every document updated for it.
- If the story was planned, the milestone contains a link to that plan, and the plan's path resolves.
- The test command and the runtime verification command that ran are both named in the story's own record, with their outcomes.

### Per milestone

- Every story in the milestone document is marked complete, or carries a blocker record naming its blocker, the attempts made, the partial work that landed, and the next action.
- Every plan created during the run is linked from the milestone, and every link resolves.
- The run ends with the four-category intervention report, and every blocked item in it is traceable to a blocker record in the project's documents.
- No file exists that was created solely to track this workflow's progress.
- A fresh agent reading only the repository can state which milestone ran, that it is complete, and where each story's plan and commit are — without access to this run's context.

Confirm milestone completion by **re-reading the milestone from disk**, not by recalling that you processed every story. Having done the work is not evidence; the document is.

## Relationship to the other Rails skills

- **`rails-boss-execute-workflow`** dispatches a subagent per story and judges the result with an independent verifier. Prefer the Boss when stories are independent enough to run in parallel, or when a specialist persona must own the implementation. Prefer the Minion when delegation overhead, duplicated context, and planning-to-implementation hand-off errors cost more than they buy. The Minion's substitute for an independent verifier is the compaction boundary at step 6: verification runs from a context that was rebuilt from the repository, not from the narrative that produced the code.
- **`rails-plan-spam-workflow`** generates many plans up front through delegated workers. The Minion plans one story at a time, immediately before implementing it, so the plan never goes stale between authoring and execution.
- **`rails-spike`** answers a single uncertainty with the smallest experiment that produces evidence. The Minion invokes it at rung 3 of the ladder, integrates its recommended path, and keeps working while it runs where independent work exists.
- **`rails-planning-phaser`** splits a story too large or too risky to run as one unit. It is rung 4.
- **`rails-planning`** owns plan quality and structure. The Minion owns only the decision of *when* a plan is needed, linking it into the milestone, compacting afterward, and later executing it.
- **`commit-log`** owns commit wording. A successful commit through it is part of a story's definition of done.
