---
name: rails-minion-workflow-story-lifecycle
description: The six phases of one Minion story iteration, the compaction boundaries between them, and the state machine the loop follows.
metadata:
  version: "1.0"
---

# Story Lifecycle

One story is one full pass through phases A–F. Every story starts from the same entry point, so a run of one story and a run of a hundred follow identical mechanics.

## Phase A — Reload authoritative context

Before touching a story, rebuild working state from the repository. Reload the milestone, the active story, any plan linked to it, the relevant design documentation, and the implementation context the story will touch.

Where the files contradict your recollection of earlier work, the files win. That is the whole point of the phase.

## Phase B — Decide whether planning is required

Three outcomes:

**An adequate plan already exists.** Load it, confirm it still describes the story as written, confirm the milestone references it, and move toward execution.

**The story is simple.** A story whose implementation is obvious from its own description — a rename, a config change, a documented API call, a small well-bounded fix — gains nothing from a planning document. Skip it and move toward execution.

**The story is complex and unplanned.** Invoke `rails-planning` by name. Then, before compacting: link the plan from the milestone, update any design or context document the planning decision changed, and record the plan's status. The linkage lives in the project's documents — never in a note to yourself.

## Phase C — Compact before execution

Compact after planning, or whenever preparation has accumulated substantial context.

Then reload: milestone, active story, its plan, relevant design and context documents. Confirm which story is active before writing a line of implementation.

This is the anti-drift boundary that makes a planned story survive the gap between planning it and building it.

## Phase D — Execute the story

Implement the active story directly.

Keep the project's documents synchronized with meaningful changes as they happen — newly discovered constraints, changed design decisions, modified architecture, revised implementation details, plan amendments, milestone changes. Documentation updates belong inside implementation, not in a cleanup pass at the end, because a compaction between the change and the cleanup loses the reason for the change.

## Phase E — Implementation checkpoint

When implementation appears complete:

1. Update the plan to record that its implementation work is done, where that status is represented.
2. Update the design documents with the decisions implementation actually settled.
3. Update the story's state — but **do not mark it complete**. It is not complete until it is proven and committed.
4. Compact.

## Phase F — Reload before verification

Reload the milestone, story, plan, and relevant design context. Then inspect the **actual implementation state** on disk — the diff, the files, the tests — rather than trusting the account of it you produced in phase D.

Verification from a rebuilt context is what this workflow substitutes for an independent reviewing agent. Skipping the reload collapses that separation and returns you to grading your own homework.

Proceed into the gates in [verification-gates.md](verification-gates.md).

## State machine

```text
START
  |
  v
Reload milestone + context
  |
  v
Find first incomplete story ---- none ----> MILESTONE COMPLETE
  |
  v
Mark story in progress
  |
  v
Needs a plan? -- yes --> Adequate plan exists? -- no --> rails-planning
  |                              |                            |
  |                              |                            v
  |                              |                    Link plan into docs
  |                              |                            |
  |                              +----------------------------+
  |                                                           |
  |                                                           v
  +---- no ------------------------------------------------> COMPACT
                                                              |
                                                              v
                                                       Reload context
                                                              |
                                                              v
                                                       Execute story
                                                              |
                                                              v
                                              Sync docs as work happens
                                                              |
                                                              v
                                                  Implementation done
                                                              |
                                                              v
                                                           COMPACT
                                                              |
                                                              v
                                                       Reload context
                                                              |
                        +---- fail ---- Run tests ------------+
                        |                    |
                        v                  pass
                   Fix the work              |
                        ^                    v
                        +---- fail ---- Run the application
                        |                    |
                        |                  pass
                        |                    v
                        |            Sync documentation
                        |                    |
                        |                    v
                        +---- fail ---- commit-log
                                             |
                                          success
                                             |
                                             v
                                     Mark story complete
                                             |
                                             v
                                     Reload milestone --> LOOP
```

## Failure handling

A failed gate returns the story to active work. It never downgrades into a note to fix later.

- **Planning failure** — `rails-planning` cannot produce a usable plan. The story stays incomplete. Resolve the planning problem; do not proceed as though planning succeeded.
- **Test failure** — diagnose, correct, rerun. If the fix changes design or plan assumptions, update those documents too, then re-verify from the top of the gates.
- **Runtime failure** — return to phase D. Fix, rerun the tests, rerun the runtime verification. A test suite that passes while the application does not run is a signal about the tests, worth recording.
- **Commit failure** — the story stays incomplete. Resolve the problem, commit successfully, and only then mark the story complete.

If the same story fails its gates three times, stop the run and escalate to the human rather than attempting a fourth. Three failures mean the story or its plan is wrong, not that the implementation needs another pass.
