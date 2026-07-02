# Backlog Format

The story backlog is an unscheduled story inventory, not a formal context tier — informally "Milestone -1". It lives at `context/backlog/backlog-N.md` (matches `rails-initialize-from-tier0`'s seeding convention — reuse it, don't invent a competing one).

## File cap and naming

- Cap each backlog file at **30 stories**.
- When a file would exceed 30, start `backlog-<N+1>.md` instead of growing the current file.
- Files are numbered sequentially: `backlog-1.md`, `backlog-2.md`, `backlog-3.md` ...
- A story does not need to move files once assigned one — the cap governs new-story placement, not tidiness of existing files.

## Evergreen and intentionally messy

The backlog can represent 6 months to multiple years of work. It is not meant to be perfectly organized start-to-end, and it is supplemented over time as understanding improves — new stories get added continuously, not just pulled into milestones. Do not "clean up" the backlog into a falsely tidy state; preserve its working messiness.

## Sort order within a file

Front-to-back:

- **Front** — most urgent, most concrete, most doable now.
- **Back** — most wishful, most experimental, least concrete, least urgent.

Re-sort a file whenever stories are added, removed, or rescoped enough to change their place in this ordering.

## Story fields

Each story is a subsection inside its backlog file. Minimum fields:

```markdown
### <story-slug>

- **Milestone:** <milestone name/path once pulled in, or "unassigned">
- **Status:** backlog | in-milestone | superseded
- **Depends On:** <story-slug(s), or "none">
- **CER:** Complexity <n> / Effort <n> / Risk <n> (or "not yet scored")

<one-paragraph story summary — what, not how>
```

- `<story-slug>` is a short kebab-case identifier that carries straight through to the story's eventual `context/implementation-plans/<milestone-slug>/<story-slug>/plan.md` folder without translation, once it is pulled into a milestone and an implementation plan is generated for it.
- `Depends On` is the authoritative dependency signal for `rails-milestone-planning`'s ordering pass. Leave it as `none` until a real dependency is confirmed — do not pre-fill guesses.
- `CER` fields are populated only after a real `rails-grade-cer` run. Leave them as "not yet scored" rather than guessing.
- `Milestone` stays `unassigned` until the story is pulled into a milestone document's story list; once pulled in, hold the milestone name/path here so the backlog entry still traces to where the story now lives.
- `Status` moves to `in-milestone` the moment a story is pulled into a milestone's story list, and to `superseded` if the entry was replaced or rewritten rather than pulled in unchanged (see Reclassification bookkeeping below for the epic-promotion case).

## Reclassification bookkeeping

When a story is promoted into its own Milestone document (see the Reclassification section in `SKILL.md`), delete its subsection from the backlog file entirely — it has outgrown the story tier — and note the promotion (old story slug, new milestone doc path) in the target milestone document's Backlog Sources or Notes section if the project keeps one. Do not leave a stub or pointer behind in the backlog file itself; the backlog should only ever contain current, real stories.
