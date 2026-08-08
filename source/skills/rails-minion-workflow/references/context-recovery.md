---
name: rails-minion-workflow-context-recovery
description: What the Minion reloads after each compaction, the questions the repository alone must answer, and why no separate progress tracker is allowed.
metadata:
  version: "1.0"
---

# Context Recovery

Compaction is a workflow boundary, not just a token-saving measure. It forces the Minion to rebuild its working state from documents that other agents and humans can also read — which is what stops a long run from drifting away from what the project actually asked for.

## What to reload

After every compaction, and before every story:

1. **The milestone document** — the work queue, and the only authority on which stories are complete.
2. **The active story** — its description, acceptance criteria, and current state.
3. **The linked plan**, if the story has one.
4. **Relevant design documentation** — the parts the story touches, not the whole set.
5. **The implementation context** the story will change — the files, tests, and interfaces in its blast radius.

Reload what the next phase needs, not everything available. A reload that pulls in the entire repository defeats the compaction it follows.

## The recovery questions

State is sufficiently recorded when a fresh context, reading only the repository, can answer all of these:

- Which milestone is being executed?
- Which stories are complete?
- Which story is active?
- Does the active story have a plan, and where is it?
- Has implementation been performed?
- Has verification passed?
- What remains to be done?

Before any compaction, check that the documents answer these. If one of them can only be answered from the conversation, write it to a document first — that is the whole cost of surviving the boundary, and it is much cheaper than reconstructing lost work.

## Story states

Use the syntax the project's own documents already use. Conceptually the states are:

- **pending** — not started.
- **in progress** — claimed by the current run.
- **implementation complete, awaiting verification** — where the project's conventions can express it. Where they cannot, the story stays *in progress* until it is genuinely complete; do not invent a new marker vocabulary for one workflow's benefit.
- **complete** — every gate passed, commit landed.

Never mark a story complete early on the expectation that the remaining gates will pass.

## Why there is no tracker

A progress file the Minion maintains is a second source of truth. After a compaction it can disagree with the milestone, and the Minion has no way to tell which one is wrong — the very situation the reload exists to prevent. So the milestone is the queue, the plans carry the detail, and the design documents carry the decisions.

This has a cost worth naming: the Minion must keep those documents genuinely current during implementation, because there is no scratch space to defer it into. That cost is the feature. It means the repository is always in a state where another agent or a human can pick the milestone up mid-run.

## Interconnection

Documents form a graph, not a pile of isolated files:

- The milestone references each story's plan.
- A plan identifies the story it belongs to.
- Design documents are updated when a plan introduces or changes a design decision.

A plan nothing links to is invisible to the next fresh context, which makes it equivalent to not existing.
