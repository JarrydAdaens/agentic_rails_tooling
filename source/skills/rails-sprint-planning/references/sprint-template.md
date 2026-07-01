# Sprint Template

Write locked-in sprints to `context/sprints/sprint-N.md`, numbered sequentially (`sprint-1.md`, `sprint-2.md`, ...). When Mode B splits a sprint, the overflow sprint gets the next free sprint number — it is a new sprint file, not a suffix on the original.

```markdown
---
metadata:
  version: "1.0"
---

# Sprint <N> — <short deliverable name>

- **Milestone:** <milestone name and path, e.g. context/milestones/milestone-2.md>
- **Status:** proposed | locked | in-progress | done
- **Locked:** <DD Month YYYY, once the user signs off — leave blank while still "proposed">
- **Split from:** <sprint id, only present if this sprint exists because Mode B split an overflowing sprint>

## Deliverable Goal

<one clear, concise sentence stating what this sprint delivers. If you cannot state it in one sentence, the sprint is not normalized yet — go back and negotiate the shape further.>

## Stories (ordered)

| Order | Story ID | Depends On | Complexity | Effort | Risk | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `STORY_2_1_example-slug` | none | `<n>` | `<n>` | `<n>` | |
| 2 | `STORY_2_2_example-slug` | `STORY_2_1_example-slug` | `<n>` | `<n>` | `<n>` | |

Order is execution order, not backlog order — dependencies win over backlog position (see Dependency Ordering in `SKILL.md`).

## Cumulative CER

| Axis | Cumulative Score |
| --- | --- |
| Complexity | `<n>` |
| Effort | `<n>` |
| Risk | `<n>` |

Cumulative scores come from summing (or otherwise combining, per `rails-grade-cer`'s own guidance) the per-story scores above — never invented separately from them.

## Rebalance History

<Only present once this sprint has been through Mode B at least once. One row per rebalance pass.>

| Date | Trigger | Action | Resulting Sprints |
| --- | --- | --- | --- |
| <DD Month YYYY> | <story that drifted, and why> | split / re-scored in place | `sprint-N.md`, `sprint-N+1.md` |
```

## Notes

- Do not add model selection, execution instructions, or phase breakdowns to a Sprint file — that is downstream of this skill (Orchestrator, `rails-planning-phaser`).
- A Sprint file's `Status` moves to `locked` only after the user has signed off on the proposed shape in chat. Never write a sprint straight to `locked` on first proposal.
- Keep the Deliverable Goal to one sentence. If a milestone drain (Mode A) produces multiple sprints, each one still gets exactly one deliverable goal — that is what makes a milestone-worth of stories legible as separable sprints in the first place.
