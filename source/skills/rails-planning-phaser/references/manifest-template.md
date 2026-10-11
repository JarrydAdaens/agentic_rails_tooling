---
name: rails-planning-phaser-manifest-template
metadata:
  version: "2.0"
---

# Manifest template

Preserve project metadata and decisions. A single-unit plan keeps its original
body and gains or updates one `## Decomposition` note explaining why no split is
useful. Include requested CER results in that note without a model assignment.

A phased manifest uses this shape, adapted to the project's existing conventions:

```markdown
---
name: <existing plan name>
description: <plan purpose>
metadata:
  version: "<project document version>"
---

# <Task name> — phased plan

## Objective and scope

<Concise purpose, accepted decisions, exclusions, and links to relevant context.>

## Assessment

<Complexity and effort in words, with uncertainty. Distinguish inherent
consequences, implementation hazards, and residual risk. Optional requested CER
results remain advisory and identify the grading source.>

## Provenance

The byte-exact source and prior phases are recorded by `phasing-state.json` and
its referenced history journal. These are historical evidence. This manifest is
the status owner for execution; history files must not be executed as current work.

## Phase registry

| Phase | Depends on | Outcome | Status | Verification | Notes |
| --- | --- | --- | --- | --- | --- |
| phase-1.md | none | <observable outcome> | not started | pending | |
| phase-2.md | Phase 1 | <observable outcome> | not started | pending | |

## Execution policy

<Name the status owner and phase acceptance checks. Record the user's commit
policy and whether workers are authorized. Runtime model/effort inheritance is
the default. Record requested and observed identities only when work executes.>

## Decomposition rationale

<Explain useful checkpoints and how existing completed work was handled.>
```

Registry statuses are `not started`, `in progress`, `completed`, or `blocked`.
Verification records the actual command/result or remaining acceptance work.
During rephasing, preserve completed outcomes and cite the prior snapshot; do not
reset executed work into pending status merely because numbering changed.
