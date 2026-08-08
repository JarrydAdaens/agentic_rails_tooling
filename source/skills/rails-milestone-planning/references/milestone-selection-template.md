---
name: rails-milestone-planning-selection-template
description: The story-list sections rails-milestone-planning writes inside an existing milestone document.
metadata:
  version: "1.0"
---

# Milestone Selection Template

This is not a standalone document template — a milestone's Intent, Why It Matters, and Outcome / Definition of Done are set upstream, when the milestone document itself is created. This reference shows the story-list-specific sections `rails-milestone-planning` writes and updates *inside* an existing milestone document at `context/milestones/milestone-N.md`.

When Mode B (refinement) moves stories out of a milestone because it has grown past a sensible scope, the follow-up milestone is a new document, numbered next in sequence (`milestone-N+1.md`) — never a suffix or variant of the original.

```markdown
## Story List Status

- **Status:** proposed | locked | in-progress | done
- **Locked:** <DD Month YYYY, once the user signs off — leave blank while still "proposed">
- **Follow-up Of:** <source milestone doc path, only present if this milestone document exists because a Mode B refinement pass moved deferred stories out of another milestone>

## Story Index

| # | Story | Type | Complexity | Effort | Risk | Plan | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `<story-slug>` | Feature | `<n>` | `<n>` | `<n>` | [plan.md](../implementation-plans/<milestone-slug>/<story-slug>/plan.md) | Not Started |
| 2 | `<story-slug>` | Feature | `<n>` | `<n>` | `<n>` | [plan.md](../implementation-plans/<milestone-slug>/<story-slug>/plan.md) | Not Started |

Order is execution order, not backlog order — dependencies win over backlog position (see Dependency Ordering in `SKILL.md`).

## Interdependency Order

Sequencing constraints between stories, stated in prose (e.g. "story 2 cannot start before story 1's Docker scripts exist"). Mirror each confirmed dependency onto the story's backlog entry as an explicit `Depends On` field (see [backlog-format.md](backlog-format.md)) so it does not need to be re-inferred next time.

## Backlog Sources

Links back to the backlog entries each selected story came from, so the pull can be traced.

## Deferred / Follow-up Work

Stories deliberately left out of this milestone's story list during Mode A, or moved out during a Mode B refinement pass. One row per story, noting why and where it went.

| Date | Story | Reason | Disposition |
| --- | --- | --- | --- |
| <DD Month YYYY> | `<story-slug>` | <why it didn't fit / drifted> | left in backlog / follow-up milestone: `milestone-N+1.md` |

## Cumulative CER

| Axis | Cumulative Score |
| --- | --- |
| Complexity | `<n>` |
| Effort | `<n>` |
| Risk | `<n>` |

Cumulative scores come from summing (or otherwise combining, per `rails-grade-cer`'s own guidance) the per-story scores in the Story Index above — never invented separately from them.

## Refinement History

<Only present once this milestone's story list has been through Mode B at least once. One row per refinement pass.>

| Date | Trigger | Action | Resulting Milestones |
| --- | --- | --- | --- |
| <DD Month YYYY> | <story that drifted, and why> | deferred / follow-up spun up / re-scored in place | `milestone-N.md`, `milestone-N+1.md` |
```

## Notes

- Do not add model selection, execution instructions, or phase breakdowns to these sections — that is downstream of this skill (Orchestrator, `rails-planning-phaser`).
- `Story List Status` moves to `locked` only after the user has signed off on the proposed shape in chat. Never write it straight to `locked` on first proposal.
- The milestone's outcome statement (one sentence, set where the milestone itself was created) stays authoritative. If Mode A or B produces a follow-up milestone, that follow-up still gets exactly one outcome statement of its own — that is what keeps a milestone's worth of stories legible as a separable, deliverable unit.
- There is no fixed capacity or velocity figure for a milestone's story list. "Blown out" is a scope judgment the user makes with CER re-scores in hand (see Overflow in `SKILL.md`), not a threshold this template enforces.
