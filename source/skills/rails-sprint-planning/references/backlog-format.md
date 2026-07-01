# Backlog Format

The Tier 4 story backlog lives at `context/backlog/backlog-N.md` (matches `rails-initialize-from-tier0`'s seeding convention — reuse it, don't invent a competing one).

## File cap and naming

- Cap each backlog file at **30 stories**.
- When a file would exceed 30, start `backlog-<N+1>.md` instead of growing the current file.
- Files are numbered sequentially: `backlog-1.md`, `backlog-2.md`, `backlog-3.md` ...
- A story does not need to move files once assigned one — the cap governs new-story placement, not tidiness of existing files.

## Evergreen and intentionally messy

The backlog can represent 6 months to multiple years of work. It is not meant to be perfectly organized start-to-end, and it is supplemented over time as understanding improves — new stories get added continuously, not just drained. Do not "clean up" the backlog into a falsely tidy state; preserve its working messiness.

## Sort order within a file

Front-to-back:

- **Front** — most urgent, most concrete, most doable now.
- **Back** — most wishful, most experimental, least concrete, least urgent.

Re-sort a file whenever stories are added, removed, or rescoped enough to change their place in this ordering.

## Story fields

Each story is a subsection inside its backlog file. Minimum fields:

```markdown
### STORY_<milestone>_<n>_<short-slug>

- **Milestone:** <milestone name or "unassigned">
- **Status:** backlog | scheduled | in-sprint | done
- **Depends On:** <story id(s), or "none">
- **CER:** Complexity <n> / Effort <n> / Risk <n> (or "not yet scored")
- **Sprint:** <sprint id, once scheduled, else blank>

<one-paragraph story summary — what, not how>
```

- `STORY_<milestone>_<n>_<short-slug>` matches the Tier 5 implementation-plan folder naming convention (`STORY_3_1_short-readable-name`) so a story's id carries straight through to its eventual `context/implementation-plans/` folder without translation.
- `Depends On` is the authoritative dependency signal for `rails-sprint-planning`'s ordering pass. Leave it as `none` until a real dependency is confirmed — do not pre-fill guesses.
- `CER` fields are populated only after a real `rails-grade-cer` run. Leave them as "not yet scored" rather than guessing.
- `Sprint` stays blank until the story is locked into a written Sprint file.

## Reclassification bookkeeping

When a story is promoted to a Milestone (see the Reclassification section in `SKILL.md`), delete its subsection from the backlog file entirely — it no longer belongs at the Story tier — and note the promotion (old story id, new milestone doc path) in the target Sprint or Milestone doc's own history if the project keeps one. Do not leave a stub or pointer behind in the backlog file itself; the backlog should only ever contain current, real stories.
