# Tier 4 Implementation Plan Template

Use this template for `rails-planning` unless the target repository has a stronger local implementation-plan template.

```markdown
# <Task Name> - Implementation Plan

## Metadata

- Task Type: `GOAL | FEATURE | BUG | REFACTOR | SPIKE`
- Task Name: `<short task title>`
- Status: `Draft | Ready | In Progress | Blocked | Complete | Superseded`
- Owner: `<human, team, or agent if known>`
- Last Updated: `<DD Month YYYY>`

## Linked Context

- Design: `../../design.md`
- Milestone: `<link if applicable>`
- Goal: `<link if applicable>`
- Tier 0 Source: `<link only if materially relevant>`
- Related Plans: `<links if applicable>`
- External Tooling: `<skills, agents, workflows if required>`

## Objective

State the concrete outcome this plan must produce.

## Problem Summary

Describe the issue, feature gap, or implementation need.

## Scope

### In Scope

- `<scope item>`

### Out Of Scope

- `<explicit non-goal>`

## Current State

Summarize the existing relevant repository state.

## Assumptions And Constraints

- `<assumption or constraint>`

## Files And Areas Likely Affected

- `<path>` - `<reason>`

## Implementation Steps

1. `<step>`
2. `<step>`
3. `<step>`

## Verification Plan

### Automated Checks

- `<command or test area>`

### Manual Checks

1. `<manual verification step>`

## Risks And Open Questions

- Risk: `<risk>`
- Question: `<open question>`

## Completion Checklist

- [ ] Implementation matches the linked design and goal context
- [ ] Scope stayed inside this plan
- [ ] Relevant docs were updated if behaviour changed
- [ ] Verification was completed or explicitly deferred
- [ ] `implementation-log.md` was updated during execution
```
