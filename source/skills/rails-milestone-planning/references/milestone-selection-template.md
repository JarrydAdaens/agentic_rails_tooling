---
name: rails-milestone-planning-milestone-selection-template
description: Milestone Selection Structure.
metadata:
  version: "2.0"
---

# Milestone Selection Structure

Adapt the existing milestone at its established target-root path; a new explicitly requested outcome may use `context/milestones/<milestone-slug>.md`. Preserve published identity/version policies only where adopted.

```markdown
# Milestone: <Delivery outcome>

Outcome and acceptance: <what this delivers and evidence of completion>
Scope authority: <request and settled decisions; mark proposals explicitly>
Status owner: <this milestone or external tracker link>

## Selected work and dependencies
| ID | Outcome / acceptance | Depends on | Owner / authoritative link | Plan (if any) |
| --- | --- | --- | --- | --- |
| <id> | <result> | <ids or none> | <link> | <existing location> |

## Delivery assumptions and forecast
<Critical path, implementation effort, external waits, ranges with basis, unknowns.>

## Deferred work
| Item / source link | Reason | Destination / decision needed |
| --- | --- | --- |
| <stable id> | <reason> | <existing backlog/tracker or proposed grouping> |

## Refinement evidence
<Material scope/dependency changes and their authority; preserve completed work.>
```

An optional assessment may use qualitative complexity/effort and consequence/hazards/residual risk from `rails-grade-cer`. Never sum bands into a cumulative forecast. Plan links can point to current plans, standalone substantial plans, or adopted milestone/story folders; do not create placeholders for every candidate.
