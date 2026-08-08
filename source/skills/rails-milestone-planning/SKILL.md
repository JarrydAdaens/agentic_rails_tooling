---
name: rails-milestone-planning
description: >-
  Use this skill to turn the story backlog (an unscheduled story inventory,
  informally "Milestone -1") and the Design doc's Milestones Index into a
  scored, dependency-ordered story list inside a Milestone document, and to
  keep the backlog itself alive over time. Use it to pull backlog stories
  into a fresh milestone's story list, or to refine an existing milestone
  whose story list has grown past a sensible scope and needs stories shunted
  into Deferred / Follow-up Work. Calls the rails-grade-cer skill for
  scoring rather than reimplementing it, and promotes epic-sized backlog
  items into their own Milestone documents when CER exposes them. Not
  model-invocable — the user calls this by name when they are ready to plan
  or refine a milestone's story list; it does not trigger itself on ambient
  planning conversation.
disable-model-invocation: true
argument-hint: "<milestone name or number> [--create|--refine] [--no-rescore]"
metadata:
  version: "2.1"
---

# Rails Milestone Planning

Turn a Design doc and the story backlog into an executable, prioritized story inventory, then select and sequence that inventory into a scored, dependency-ordered story list inside a Milestone document.

This is the skill that replaces trying to hold an entire project's plan in your head and working multiple milestones at once. It exists so you only ever plan what's next, close to execution.

```text
Design -> Milestone -> Story (backlog) -> Implementation Plan
              ^ this skill assembles the story list here    ^ this skill maintains this
```

`rails-milestone-planning` is a right-rail capability; its output (`context/milestones/`, `context/backlog/`) lives in the target project's left rail.

## Not Model-Invocable

`disable-model-invocation: true` is intentional. This skill only runs when the user names it explicitly ("plan milestone X", "refine milestone Y", `/rails-milestone-planning ...`). It does not fire on ambient planning chatter, and it does not decide for itself when a milestone's story list has drifted enough to need refinement — that judgment call belongs to the user (see Overflow below).

## Scope

### Owns the backlog

This skill **creates and maintains** `context/backlog/`. It is not a consumer of a backlog produced elsewhere — `rails-initialize-from-tier0` may seed the first backlog file during project setup, but this skill is what keeps it alive afterward: pulling new stories out of Design/Milestone docs, resorting, capping, and reclassifying, on an ongoing basis.

See [references/backlog-format.md](references/backlog-format.md) for the file cap, sort order, and story fields.

### Calls CER, doesn't reimplement it

Complexity/Effort/Risk scoring is **not owned here**. Follow the `rails-grade-cer` skill against backlog items and stories and consume its score table. This skill is a consumer of CER, same as the orchestrator downstream will be. Never invent a score.

### Promotes epics exposed by CER

When a backlog item's CER score comes back epic-sized, this skill pulls it out of the story backlog and promotes it into its own Milestone document under `context/milestones/` — see Reclassification below. CER exposes the epic; this skill acts on it.

### Does NOT do

- Design → Milestone outcome negotiation (deciding what a milestone's Intent, Why It Matters, and Outcome / Definition of Done are). That is `rails-initialize-from-tier0` (or a future ingestion/design-planning skill), upstream of this one. This skill assumes a milestone already exists — except for the minimal shell it creates itself during Reclassification or Overflow (see below).
- Fragmenting a single story's implementation into Phases. That is downstream — `rails-planning-phaser`, run against a story's implementation plan.
- Computing CER scores itself. See above — always call `rails-grade-cer`.
- Selecting models or executing anything. That is the Orchestrator, which consumes the milestone's story list.

## Arguments

The skill was invoked with: $ARGUMENTS

Read that line before doing anything else. It is free text, so parse it leniently, and treat plain-language equivalents as equal to the tokens ("just reorder them" is `--no-rescore`).

| Token | Meaning |
| --- | --- |
| `--create` | Mode A — lay out a fresh milestone's full delivery path. |
| `--refine` | Mode B — revise an existing milestone's story list. |
| `--no-rescore` | Reuse the CER scores already recorded rather than re-grading moved stories. Absent means re-score anything whose scope looks like it moved. |
| anything else | The milestone name or number. Ask only if it cannot be resolved. |

With neither `--create` nor `--refine`, infer the mode from whether the milestone already has a story list, and say which you chose before writing anything.

## Two Operating Modes

Same skill, two entry points, both interactive (see Interactivity below).

### Mode A — Milestone creation (initial)

Used on a fresh milestone to lay out its full delivery path:

1. Search `context/backlog/` for everything relevant to the milestone (e.g. milestone "Dockerize RivalSight" → search for Docker scripts, containerization, secrets).
2. Gather the matching stories.
3. Score them via `rails-grade-cer` — individually, then cumulatively for the candidate story list.
4. Order by interdependency (see Dependency Ordering below).
5. Write the selected, ordered stories into the milestone document's Story Index and Stories sections. A milestone should generally hold roughly 10 to 20 stories — a guideline, not a hard rule. If the backlog search turns up far more relevant stories than the milestone can hold without becoming unreadable, hold the excess back in Deferred / Follow-up Work rather than force it in.

### Mode B — Milestone refinement (ad-hoc)

Run any time — multiple times a day, weekly, monthly — against an **existing** milestone's story list:

1. Re-check the milestone's stories against current scope/estimates. Re-run `rails-grade-cer` on any story whose scope looks like it moved since it was last scored.
2. If the story list has grown past a sensible scope and no longer fits one milestone (see Overflow below), move the excess into Deferred / Follow-up Work and, if the user agrees, spin up a follow-up milestone document to hold it.
3. Leave each resulting milestone with one clear, concise outcome statement.

This is the mechanism that stops scope creep from silently bloating a milestone past its original intent.

## Interactivity Model

Story-list assembly is interactive, not a silent batch job:

1. Propose a story list — which stories, what order, whether a follow-up milestone is needed.
2. The user reviews and pushes back — too many stories, wrong grouping, wrong order, whatever.
3. Negotiate until the shape fits.
4. Lock it in → write the normalized story list into the milestone document, ready for the Orchestrator.

Do not write the final story list before the user has signed off on the proposed shape. A draft proposal in chat first is fine; the durable file is the locked-in result.

## Dependency Ordering

Milestones are sequential and are rarely worked out of order — default to the order the backlog and Design doc's Milestones Index already imply. Within a milestone's story selection, only reorder stories where a real dependency forces it (e.g. secrets work can't start before the Docker scripts it references exist).

Detect dependency in this priority order:

1. **Explicit.** A `Depends On` field on the story in the backlog (see [references/backlog-format.md](references/backlog-format.md)). Always trust this over inference.
2. **Inferred.** If no explicit field exists, infer from story content (one story's description references an artifact another story produces). Propose the inferred order to the user as part of the story-list proposal — do not silently lock in an inferred dependency without surfacing it.
3. **Default.** If neither applies, preserve backlog order (front-to-back = most urgent/concrete first, per [references/backlog-format.md](references/backlog-format.md)).

When you infer a dependency, write it back onto the story as an explicit `Depends On` field once the user confirms it, so the next milestone creation or refinement pass doesn't have to re-infer it.

## Reclassification (Epic Detection)

`rails-grade-cer` owns the definition of epic-sized: any axis scoring past 10. When it returns such a story:

1. **Propose, don't silently promote.** Tell the user the item looks epic-sized and show the CER scores driving that read.
2. On confirmation, pull the item out of its backlog file and create a new `context/milestones/milestone-N.md` from it, following the milestone doc conventions already established in the project (or the starter's milestone template if this is the first milestone doc created this way).
3. Add the new milestone to the Milestones Index in `context/design.md` if that index exists.
4. Remove the promoted item from the backlog file it came from and renumber/re-sort that file per [references/backlog-format.md](references/backlog-format.md).

Never auto-promote without the confirmation step in 1 — reclassification changes tier ownership and downstream story-list/Orchestrator assumptions, so it warrants a checkpoint even though most of this skill's other proposals can move fast.

## Overflow (Ad-Hoc Refinement)

"Blown out" is a judgment call, not a fixed variance threshold. The user decides when a milestone's story list no longer fits; this skill supports that call with CER re-scores rather than making the call itself.

- Re-score the drifted stories with `rails-grade-cer` and show the before/after (or current cumulative) numbers alongside the milestone's original cumulative scores.
- If the user judges the milestone blown out, split it: keep the still-fitting stories in the original milestone document's Story Index, move the rest into that document's Deferred / Follow-up Work section, and — if the user wants them actively planned rather than merely deferred — spin up a follow-up milestone document for them with its own single outcome statement.
- If the user judges it still fits despite a score increase, leave the milestone's story list as one unit and just update its recorded cumulative scores.

Never spin up a follow-up milestone on this skill's own initiative — always surface the re-score and let the user call it.

## Output

The selected, ordered story list is written directly into the milestone document at `context/milestones/milestone-N.md` — there is no separate scheduling file. Writing it means populating or updating that document's:

- Story Index table.
- Per-story blocks (with CER, plan link when generated, and status).
- Interdependency Order section.
- Backlog Sources section (links back to the backlog entries each story came from).
- Deferred / Follow-up Work section, when Overflow applies.

See [references/milestone-selection-template.md](references/milestone-selection-template.md) for the exact section structure this skill writes and updates. This is the artifact the Orchestrator consumes directly to begin execution — do not add execution instructions, model selections, or phase breakdowns to it; those belong further downstream.

## Hard Rules

- **Never invent a CER score.** Every complexity/effort/risk number in a backlog entry or milestone story list comes from following `rails-grade-cer`. If a score is stale or missing, re-run CER before using it in a proposal.
- **Never silently promote an epic.** Reclassification always gets a confirmation checkpoint (see Reclassification).
- **Never silently spin up a follow-up milestone.** Splitting a milestone's story list is the user's call, supported by CER, never this skill's own initiative (see Overflow).
- **Never write the final story list before the user signs off on the proposed shape.** Propose in chat first; write only the locked-in result.
- **Respect the 30-story backlog file cap.** Overflow spawns a new backlog file rather than growing one file unbounded — see [references/backlog-format.md](references/backlog-format.md).
- **Preserve sequential order by default.** Do not reorder stories or milestones without a real, surfaced dependency reason.
- **Don't do the upstream or downstream job.** No Design→Milestone outcome negotiation beyond the minimal shell described in Reclassification/Overflow, no Phase fragmentation, no model selection, no execution.

## Operating Model

1. Determine the entry point: a fresh milestone name (Mode A) or an existing milestone document (Mode B). Ask if ambiguous.
2. Load the minimum context needed: the named milestone doc, the relevant `context/backlog/*.md` files, and `context/design.md`'s Milestones Index if present.
3. **Mode A:** search the backlog for stories matching the milestone, gather them, score via `rails-grade-cer`, determine dependency order (see Dependency Ordering), and draft a candidate story list (possibly deferring some to Deferred / Follow-up Work).
4. **Mode B:** re-check the named milestone's stories, re-score any that look drifted, and determine whether the user judges the story list blown out (see Overflow).
5. Check every re-scored or newly-scored story for epic-sized results; if any are found, run the Reclassification checkpoint before continuing story-list assembly.
6. Propose the story list to the user in chat (stories, order, whether a follow-up milestone is needed, cumulative scores, single outcome statement). Negotiate.
7. On sign-off, write the locked story list into the milestone document (and any follow-up milestone document) using [references/milestone-selection-template.md](references/milestone-selection-template.md).
8. Update `context/backlog/*.md` to reflect any stories pulled into a milestone, any reclassified epics removed, and any newly-confirmed `Depends On` fields.
9. Report the exact paths of every file written or updated, plus the CER scores behind each decision.

## Acceptance

Observable facts about what landed on disk:

- Every CER field written carries a score, or the literal `not yet scored` — never a number this skill invented.
- No backlog file under `context/backlog/` contains more than 30 stories.
- Every story whose order differs from backlog order carries an explicit `Depends On` field naming why.
- The milestone document's story list was written only after the user's sign-off appears in the conversation.
- Every written or updated path under `context/backlog/` and `context/milestones/` was reported to the user.
