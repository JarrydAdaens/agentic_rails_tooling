---
name: rails-planning-plan-template
description: Implementation Plan Template.
metadata:
  version: "3.0"
---

# Implementation Plan Template

Scale this structure to the work and use a stronger local template when present. Headings with no useful content may be omitted. A plan captures executable intent; it does not require a full context scaffold.

```markdown
# Plan: <Outcome>

Status: <Draft | Ready | In Progress | Blocked | Complete>
Authority: <user request and accepted decisions>
Status owner: <this plan or link to the existing tracker>

## Outcome and scope
<Concrete result, acceptance, permitted edits, exclusions, and constraints.>

## Current understanding
<Affected files/contracts; preserved behavior; relevant maintained context.>

## Dependencies and delivery steps
| Step | Change and evidence | Prerequisites | Estimate / uncertainty |
| --- | --- | --- | --- |
| <id> | <independently checkable result> | <real dependency or none> | <qualitative size or evidenced range> |

## Checks and recovery
<Artifact-specific commands or review; unavailable checks; rollback or retained snapshot if warranted.>

## Questions and assumptions
<Unknown, impact, discovery/decision needed, and temporary assumption.>

## Assessment (optional)
<Qualitative complexity and effort; inherent consequence, implementation hazards, and residual risk.>

## Evidence and execution record
<Fill during execution: verified changes, commands/results, pending work, diff/commit identity, next step.>
```

Milestone and story links are conditional. A standalone plan need not create either. Keep source links adjacent to claims. Summing ordinal estimates is not a schedule; identify the critical dependency path, likely elapsed range, and external waits separately when forecasting.

A completion entry records acceptance evidence, limitations, actual status, and commit policy. With an external tracker, keep local delivery evidence and link the authoritative item. A no-commit result remains explicitly uncommitted.

Use phases only at natural seams with meaningful acceptance and recovery. Splitting work does not remove inherent consequences. Sidecars are for genuinely separate evidence collections or explicit requests; sanitized observations may be useful, private chain-of-thought is never captured.
