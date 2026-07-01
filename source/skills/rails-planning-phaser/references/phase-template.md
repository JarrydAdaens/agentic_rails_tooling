---
name: rails-planning-phaser-phase-template
metadata:
  version: "1.0"
---

# Phase File Template

A phase file is a small, self-contained plan. Use this template for every `phase-N.md` written beside a manifest.

```markdown
---
name: phase-<N>
recommended-model: <assigned model from the manifest's phase registry>
complexity: <n>
effort: <n>
risk: <n>
---

# Phase <N>: <short phase title>

## Depends On

`<phase-N-1, or "none — this is the first phase">`. State what this phase assumes already exists or already works because the prior phase completed it. A phase must not assume anything beyond what an earlier phase's completion guarantees.

## Objective

State the concrete, testable outcome this phase must produce, in one short paragraph. This should read like a miniature version of a plan's Objective section — narrow enough that a smaller model can hold the whole thing in mind.

## Implementation Steps

1. `<step>`
   - Edits: `<concrete expected changes>`
2. `<step>`

Keep steps concrete and sequenced, exactly as they would appear in a full plan — a phase file is not a summary of steps, it is the steps.

## Verification

State how to confirm this phase succeeded before moving to the next one:

- `<automated check — build, test, or command>`
- `<manual check, if any>`

## Acceptance Criteria

- `<observable outcome that proves this phase is done>`
- The application still compiles and runs after this phase, unchanged in that respect from before the phase started (unless the phase's explicit purpose was to fix a build break).

## Notes

`<Anything the executing model should know that does not fit above: known ambiguities inherited from the original plan, a risk specific to this phase, or a pointer back to the manifest for broader context. Leave blank if there is nothing beyond the above.>`
```

## Frontmatter Rules

- `name` is always `phase-<N>` matching the filename, e.g. `phase-3` for `phase-3.md`.
- `recommended-model` must exactly match the `Model` column for this phase in the manifest's phase registry. If they ever disagree, that is a bug in the phasing process — fix it before reporting the phasing as done.
- `complexity`, `effort`, and `risk` are the phase's own re-graded scores from `rails-grade-cer`, never copied from the original plan's pre-phase scores and never invented.

## Body Rules

- Do not shrink a phase's steps into vague prose just because it is "only a phase." A phase file carries the same level of concrete detail a full plan would for the same slice of work.
- Do not reference other phase files by content — only by number, and only in `Depends On`. A sub-agent executing phase 3 should never need to open phase 1 or phase 2 to understand what phase 3 asks for.
- Do not duplicate the manifest's `Plan Context` paragraph here. If broader context is genuinely needed to do this phase's work, that likely means the phase boundary was drawn in the wrong place.
