---
name: rails-milestone-planning-backlog-format
description: Backlog Shape and Ownership.
metadata:
  version: "2.0"
---

# Backlog Shape and Ownership

Use the project's existing backlog or external tracker, when adopted. Core does not need a backlog. An unscheduled work inventory is not a Milestone and requires no pseudo-milestone number.

For a file-based backlog under the target root, `context/backlog/backlog-N.md` is a supported convention. Keep stable IDs and split large files for readability without moving history solely to satisfy a story-count quota.

```markdown
### <stable-story-id>: <Outcome>

- Summary / acceptance: <concrete result>
- Source: <request/design link>
- Priority / reason: <actual urgency or value>
- Depends on: <confirmed prerequisite IDs or none; uncertain dependencies marked>
- Delivery owner: <tracker link or selected milestone link>
- Assessment (optional): <qualitative complexity/effort and risk components, confidence>
```

Once scheduled, the entry links the authoritative delivery owner rather than mirroring progress. Preserve historical IDs and plan links. A proposed broader outcome can be recorded with its rationale; promotion to a new milestone requires scope authority and is never triggered by a score. Superseded entries retain a traceable replacement link when referenced elsewhere.
