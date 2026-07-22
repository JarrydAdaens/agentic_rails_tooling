---
name: rails-planning-plan-template
metadata:
  version: "2.1"
---

# Implementation Plan Template

Use this template for `rails-planning` and `rails-plan-spam-workflow` unless the target repository has a stronger local implementation-plan template.

Every story gets **one primary artifact**: `plan.md`. It carries the intended work at planning time, and — as execution proceeds — what actually happened. Do not split it into separate `questions.md`, `evidence.md`, `complaining.md`, `thinking.md`, `implementation-log.md`, or `completion-review.md` files by default; those stay opt-in, for large or phased stories or when explicitly requested (see the skill's Core Rule). `thinking.md` is the one exception that is never a `plan.md` section — when justified, it is always a standalone sidecar file beside `plan.md` (see the skill's Core Rule).

An Implementation Plan means a Story has been translated into concrete implementation reality: named files, modules, classes, interfaces, validation surfaces, and execution steps. If exact locations are unknown, name the narrowest credible subsystem and the discovery step needed to confirm it.

```markdown
# Plan: <Story Name>

## Metadata

- Task Type: `STORY | FEATURE | BUG | REFACTOR | SPIKE`
- Status: `Draft | Ready | In Progress | Blocked | Complete | Superseded`
- Owner: `<human, team, or agent if known>`
- Last Updated: `<DD Month YYYY>`

## Linked Context

- Milestone: `<link to context/milestones/<milestone-slug>.md, if applicable>`
- Story: `<link or id to the story inside the milestone document>`
- Backlog source: `<link to the originating backlog entry, if the story was pulled from the backlog>`
- Dictation source: `<link only if raw dictation materially shaped the work>`
- Related Plans: `<links if applicable>`
- External Tooling: `<skills, agents, workflows if required>`

## CER

- Complexity: `<0-10, or > with forecast, or — if not yet graded>`
- Effort: `<0-10, or > with forecast, or — if not yet graded>`
- Risk: `<0-10, or > with forecast, or — if not yet graded>`
- Notes: `<short rationale, or the source of the grading (e.g. rails-grade-cer)>`

## Objective

State the concrete outcome this plan must produce in one short paragraph.

## Scope

### In Scope

- `<scope item>`

### Out Of Scope

- `<explicit out-of-scope item>`

## Non-Goals

- `<related work this plan deliberately does not attempt>`

## Current Understanding

Summarize the existing relevant repository state before writing steps.

- Likely files or directories: `<path and role>`
- Likely classes, functions, services, screens, or subsystems: `<name and role>`
- Existing behaviors to preserve: `<behavior>`
- Interfaces, data contracts, or external dependencies: `<name and contract>`
- Known tests, build steps, or observability points: `<name and location>`
- Assumptions and constraints: `<assumption or constraint>`

If exact locations are unknown, name the narrowest credible subsystem and the discovery step needed to confirm it.

## Questions / Unknowns

- Q: `<open question>`
  Impact: `<why the answer matters to the plan>`
  Assumption: `<temporary assumption used until answered>`
  Status: `OPEN | ANSWERED`
  Answer: `<answer when known>`

If nothing is open, state that plainly rather than omitting the section.

## Execution Steps

1. `<step>`
   - Why: `<reason this step exists>`
   - Edits: `<concrete expected changes>`
   - Dependencies: `<ordering notes if any>`

2. `<step>`

## Validation

### Automated Checks

- `<command or test area>`

### Manual Checks

1. `<manual verification step>`

### Acceptance Criteria

- `<observable outcome>`
- `<regression or compatibility guardrail>`

## Risk Mitigation

- Risk: `<risk>`
  Mitigation: `<how it is reduced, tested, or gated — or "accepted" with a short reason>`

## Phase Split

Only present when needed — when the plan exceeds CER thresholds or carries high risk. Points to `phase-1.md`, `phase-2.md`, etc. inside this same story folder. See `rails-planning-phaser`.

## Evidence / References

Short inline notes or links: files changed, commits, tests run, build results, validation evidence, planning inputs, known unverified claims. Do not create a separate `evidence.md` by default — that stays opt-in for audit/provenance needs.

## Complaints / Friction

Only present when useful: missing permissions, ambiguous requirements, broken tooling, risky assumptions, repeated workarounds, missing domain knowledge, unclear validation paths. Log real friction, proportionally — no invented complaints, no venting, no filler when nothing went wrong. Do not create a separate `complaining.md` by default — that stays opt-in for long-running workflows needing durable friction tracking.

When an entry is worth recording, use this shape:

```markdown
### <Short complaint title>

**What happened:** <direct description of the problem>
**Why this made the task harder:** <friction, uncertainty, wasted time, or risk introduced>
**What was tried:** <relevant attempts, commands, edits, or reasoning paths>
**What would improve this:** <practical fix, clearer instructions, better tooling, different workflow>
```

Separate observed fact from interpretation — add a trailing **What I think:** line for judgment, risk assessment, or recommendation when the entry needs one.

## Execution Log

Only present once execution starts. Chronological record of what was actually done, deviations from the plan, and why. Fill this in during and after execution, not at plan-creation time. Standalone `implementation-log.md` is opt-in only, for large or phased stories.

## Completion Review

Only present once the story is done. Estimates vs. actuals (CER and time), what worked, what didn't, and a root-cause split for anything that went wrong. This is the memory records office's primary data source — do not skip it silently. Standalone `completion-review.md` is opt-in only, for large or phased stories.
```

## `thinking.md` Sidecar

Unlike the other sidecars above, `thinking.md` is never a `plan.md` section — it is always a standalone file beside `plan.md`, created only when justified (see the skill's Core Rule). It is not a private chain-of-thought dump; it is a sanitized, source-grounded working log for a later human or agent.

Good entries: a useful investigation path, a discovered constraint, an observation worth preserving, or something explicitly flagged to revisit.

Do not record: hidden step-by-step reasoning, generic status updates that already belong in chat or `## Execution Log`, unsourced speculation, or routine command output that supports no useful observation.

```markdown
# Thinking Notes

## Investigation Notes

## Discovered Constraints

## Useful Observations

## Things To Revisit
```
