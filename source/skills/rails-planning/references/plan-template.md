---
name: rails-planning-plan-template
metadata:
  version: "1.0"
---

# Tier 5 Implementation Plan Template

Use this template for `rails-planning` and `rails-plan-spam-workflow` unless the target repository has a stronger local implementation-plan template.

Tier 5 planning means a Story has been translated into concrete implementation reality: named files, modules, classes, interfaces, validation surfaces, and execution steps. If exact locations are unknown, name the narrowest credible subsystem and the discovery step needed to confirm it.

```markdown
# <Task Name> - Implementation Plan

## Metadata

- Task Type: `STORY | FEATURE | BUG | REFACTOR | SPIKE`
- Story/Work ID: `<story-id or feature-id if applicable>`
- Task Name: `<short task title>`
- Status: `Draft | Ready | In Progress | Blocked | Complete | Superseded`
- Owner: `<human, team, or agent if known>`
- Last Updated: `<DD Month YYYY>`

## Linked Context

- Design: `../../design.md`
- Milestone: `<link if applicable>`
- Story: `<link if applicable>`
- Tier 0 Source: `<link only if materially relevant>`
- Related Plans: `<links if applicable>`
- External Tooling: `<skills, agents, workflows if required>`

## Objective

State the concrete outcome this plan must produce in one short paragraph.

## Problem Summary

Describe the issue, feature gap, or implementation need.

## Scope

### In Scope

- `<scope item>`

### Out Of Scope

- `<explicit out-of-scope item>`

## Current State

Summarize the existing relevant repository state.

## Tier 5 Implementation Context

Ground the plan in concrete implementation reality before writing steps.

- Likely files or directories: `<path and role>`
- Likely classes, functions, services, screens, or subsystems: `<name and role>`
- Existing behaviors to preserve: `<behavior>`
- Interfaces, data contracts, or external dependencies: `<name and contract>`
- Known tests, build steps, or observability points: `<name and location>`

If exact locations are unknown, name the narrowest credible subsystem and the discovery step needed to confirm it.

## Assumptions And Constraints

- `<assumption or constraint>`

## Implementation Steps

1. `<step>`
   - Why: `<reason this step exists>`
   - Edits: `<concrete expected changes>`
   - Dependencies: `<ordering notes if any>`

2. `<step>`

## Verification Plan

### Automated Checks

- `<command or test area>`

### Manual Checks

1. `<manual verification step>`

## Acceptance Criteria

- `<observable outcome>`
- `<regression or compatibility guardrail>`

## Risks And Open Questions

- Risk: `<risk>`
- Question: `<open question>`
- Assumption used until answered: `<temporary assumption>`

## Completion Checklist

- [ ] Implementation matches the linked design and story context
- [ ] Scope stayed inside this plan
- [ ] Relevant docs were updated if behavior changed
- [ ] Verification was completed or explicitly deferred
- [ ] `implementation-log.md` was updated during execution
- [ ] `questions.md` was updated or confirmed closed
```
