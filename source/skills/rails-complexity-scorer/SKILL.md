---
name: rails-complexity-scorer
description: >-
  Use this skill to score the execution complexity of Agentic Rails
  implementation plans and decide whether they should be split into smaller
  phase files for lower-capability or cheaper models. Use when sizing a
  plan against a target model or capability budget, auditing a backlog before
  worker dispatch, detecting plans that are too large for one pass, splitting
  Tier 4 plans into progressive phase sub-plans, or right-sizing work for
  subagents, local models, mid-capability models, or cost-sensitive execution.
disable-model-invocation: false
metadata:
  version: "1.0"
---

# Rails Complexity Scorer

Measure an Agentic Rails Tier 4 plan's execution size, compare it to a target
model's capability budget, and split oversized plans into independently
executable phase files.

This is right-rail behavior. The generated `complexity-report.md` and any
`phases/phase-N.md` files belong in the target project's left rail beside the
source plan.

## Core Rule

Score execution size, not product scope.

Use this skill after the work is already a coherent deliverable. If a plan is
trying to deliver unrelated features, stop and flag a scope problem instead of
phasing it. Phase splitting preserves one deliverable and makes it executable by
smaller agents.

## Locate The Plan

Prefer Agentic Rails Tier 4 plan paths:

```text
context/implementation-plans/<task-folder>/plan.md
documentation/implementation-plans/<task-folder>/plan.md
docs/implementation-plans/<task-folder>/plan.md
```

If the user gives a plan path, use that exact plan. If several related plans
exist and the target is unclear, ask which plan to score.

## Establish Budget

Use the explicit budget if the user supplies one. If the user names a model tier
instead, use these starting budgets unless the repository has stronger local
calibration:

| Model Tier | Examples | Budget |
| --- | --- | --- |
| Small local | 7B-13B class | 8 |
| Mid local | 24B-32B class | 12 |
| Large local | 70B class | 20 |
| Frontier | hosted high-capability models | 40 |

Budgets are capability assumptions, not truth. If the user names an unknown
model without a budget or tier, ask for the budget before scoring.

## Complexity Rubric

Count units from what the plan says.

| Element | Units | Count Rule |
| --- | --- | --- |
| Implementation step | 1 | Each discrete action the executing agent must perform |
| Distinct file touched | 1 | Count each file once, even if several steps touch it |
| Decision point or branch | 1 | Each conditional path the executor must reason through |
| New abstraction | 2 | New class, interface, API surface, schema, module, service, or protocol |
| Cross-step dependency | 1 | A step whose correctness depends on an earlier step's output |
| External integration | 2 | New package, service, protocol, remote API, toolchain, or storage contract |

Do not pad the score to force a split. Do not shrink the score to avoid one.
If the plan is vague, score only the visible work and note that missing detail
may hide additional complexity.

## Operating Model

1. Read the target `plan.md`.
2. Establish the target model and budget.
3. Extract implementation steps, expected files, decisions, abstractions,
   dependencies, and integrations.
4. Score each rubric row and sum the total.
5. Compare score to budget:
   - `Total Score <= Budget`: verdict is `SINGLE-PASS`.
   - `Total Score > Budget`: verdict is `BOULDER`.
6. Always write `complexity-report.md` beside the plan.
7. For `BOULDER`, write phase files under `phases/`.
8. Report the score, verdict, budget, and exact written paths.

## Phase Fracturing

When the verdict is `BOULDER`, split the plan into the smallest practical
number of phases where every phase fits within the budget.

Rules:

- Walk implementation steps in order and accumulate units.
- Close a phase before adding a step that would exceed budget.
- Never split an atomic step across phases. If one atomic step exceeds budget,
  flag it as needing decomposition before execution.
- Preserve dependencies. A phase must not require output from a later phase.
- Reorder only clearly independent steps, and record the reason in the report.
- Prefer balanced phases over filling every phase to the ceiling.
- Keep each phase independently executable after its predecessors are complete.

Do not copy all future phase steps into every phase file. Progressive disclosure
is the point: a worker executing Phase 2 should load Phase 2, the original
project context, and any completed prior handoff, not every remaining phase.

## Output Layout

Write outputs beside the source plan:

```text
context/implementation-plans/<task-folder>/
  plan.md
  complexity-report.md
  phases/
    phase-1.md
    phase-2.md
```

Preserve the source `plan.md` unless the user asks for an index to be added
there. Put the phase index in `complexity-report.md` by default.

## Complexity Report Template

Use this structure for `complexity-report.md`:

```markdown
# Complexity Report - <Task Name>

- Plan: `<relative path to plan.md>`
- Target Model: `<model name or "unspecified">`
- Budget: `<units>`
- Total Score: `<units>`
- Verdict: `SINGLE-PASS | BOULDER`
- Last Updated: `<DD Month YYYY>`

## Score Breakdown

| Element | Count | Units |
| --- | --- | --- |
| Implementation steps | `<n>` | `<n>` |
| Distinct files | `<n>` | `<n>` |
| Decision points | `<n>` | `<n>` |
| New abstractions | `<n>` | `<2n>` |
| Cross-step dependencies | `<n>` | `<n>` |
| External integrations | `<n>` | `<2n>` |
| **Total** |  | `<sum>` |

## Verdict Detail

State plainly whether the plan fits the budget or must be split.

## Phase Index

Include only for `BOULDER`.

| Phase | Objective | Score | File |
| --- | --- | --- | --- |
| 1 | `<one-line objective>` | `<units>` | `phases/phase-1.md` |

## Notes

- Indivisible steps that exceeded budget, if any.
- Steps reordered for balance, if any.
- Assumptions or ambiguity in the source plan.
```

## Phase File Template

Use this structure for each `phases/phase-N.md`:

```markdown
# <Task Name> - Phase <N> of <Total>

## Phase Objective

One sentence describing what this phase delivers.

## Phase Complexity

- Score: `<units>`
- Budget: `<budget>`

## Precondition

State what earlier phases must have completed. For Phase 1, state that this is
the entry point.

## Steps

1. `<step>`
   - Why: `<reason>`
   - Edits: `<concrete expected changes>`
   - Files: `<paths>`

## Verification

### Automated Checks

- `<command or test area for this phase>`

### Manual Checks

1. `<manual verification step for this phase>`

## Handoff

State what exists when this phase is complete and what the next phase may
assume.
```

## Validation

Before considering the scoring complete, confirm:

- A budget was established explicitly or from a known tier.
- Unknown models were not silently assigned a budget.
- The report shows every rubric row and the total.
- The verdict follows directly from score versus budget.
- Single-pass plans did not receive phase files.
- Boulder phase files each fit within budget, unless an indivisible oversized
  step was explicitly flagged.
- Dependencies are respected.
- `complexity-report.md` exists beside `plan.md`.
- Boulder phases live under `phases/` and do not include each other's steps.
- The user was told the score, verdict, budget, and exact paths written.
