---
name: rails-minion-workflow-verification-gates
description: The four gates every Minion story passes before it may be marked complete - tests, running the real application, documentation synchronization, and the commit.
metadata:
  version: "1.0"
---

# Verification Gates

Four gates, in order. Each one must pass before the next is attempted. A failure at any gate returns the story to implementation — see the failure handling in [story-lifecycle.md](story-lifecycle.md).

Run these from the reloaded context of phase F, not from the context that wrote the code.

## Gate 1 — Automated tests

Run the tests relevant to the changed area. Where the project conventionally requires a broader suite for that area, run that too.

Name the exact command and report its outcome. "Tests pass" without the command is not a result a reader can check.

Scope this proportionately: the goal is confidence the story works and did not break its neighbors, not a green full suite on every story. Pre-existing failures unrelated to the story are reported as pre-existing, not silently fixed and not silently ignored.

## Gate 2 — Run the actual application

**Compiling is not proof. Passing tests are not proof.** The system the story changed must run.

The mechanism depends on what the project is:

| Project type | Runtime verification |
| --- | --- |
| Game | Build and run it. Navigate far enough to exercise the change where practical. Capture a screenshot when visual confirmation is meaningful. |
| Desktop or mobile UI | Build and run it. Use the project's own visual-quality or UI validation gate where one exists. |
| Service or API | Start it. Exercise the changed endpoint or behavior through the project's normal runtime path. |
| CLI or tool | Run the executable against a case that exercises the change. |
| Library | Run the consuming test harness or an example program — something that loads and calls the built artifact. |

Resolve the project's actual verification path once, at the start of the run, and record it. If none can be identified, say so before the first story rather than quietly skipping this gate for the whole milestone.

Where a project ships its own runtime gate as a skill or plugin, invoke it by name rather than reimplementing it.

## Gate 3 — Synchronize documentation

Confirm the project's existing documents describe the implementation that now exists: the story's state in the milestone, the plan's status, the milestone-to-plan link, and any design document the work changed.

This is a check, not the moment to start documenting. Most of this landed during phase D; what remains here is reconciling the last of it.

No completion ledger, no summary file, no run folder. If something about this story's outcome is worth keeping, it belongs in a document that already exists.

## Gate 4 — Commit

Invoke the `commit-log` skill by name, generate the message from it, and make a real commit.

The commit covers the story's implementation and every document changed for it, together — a story whose code and documentation land in separate commits leaves either one meaningless on its own.

A story is not complete until its commit has succeeded. If the commit fails, the story stays incomplete.

## Then, and only then

Mark the story complete in the milestone.

Completion is recorded last because every earlier gate can still send the story backward. A story marked complete before its commit is a story that lies to the next fresh context that reads the milestone.
