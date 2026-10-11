---
name: rails-planning-phaser-phase-template
metadata:
  version: "2.0"
---

# Phase template

Each phase describes a concrete increment and its checks. Execution status belongs
in the manifest. Optional numerical CER results are advisory; no model field is
derived from them.

```markdown
---
name: phase-<N>
description: <observable phase outcome>
metadata:
  version: "<project document version>"
---

# Phase <N>: <title>

## Depends on

<Earlier phase and the completed capability this phase assumes, or none.>

## Objective and scope

<Concrete outcome, owned artifacts, exclusions, and accepted user decisions.>

## Assessment

<Complexity, effort, and uncertainty. Describe inherent consequences,
implementation hazards, and residual risk after the proposed checks.>

## Implementation

1. <Concrete changes and dependencies.>
2. <Next change, including recovery where applicable.>

## Verification and acceptance

- <Relevant command or observable check and expected result.>
- <Artifact remains usable, or named preexisting failure is documented.>

## Recovery and handoff

<How to recover partial implementation and what the next phase may assume.>
```

Supply the actual commands for the affected artifact. A document change may need
link or syntax checks; application changes may need builds or behavior tests.
Do not add an unrelated build merely because the work has a phase file.
