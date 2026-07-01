---
name: rails-sprint-planning
description: >-
  Use this skill to turn the Tier 4 story backlog and Tier 2 milestone docs
  into scored, dependency-ordered Tier 3 Sprints, and to keep the backlog
  itself alive over time. Use it to drain a fresh milestone into its first
  sprint(s), or to ad-hoc rebalance an existing sprint that has scope-crept
  and needs overflow shunted into a secondary sprint. Calls the rails-grade-cer
  skill for scoring rather than reimplementing it, and reclassifies epic-sized
  backlog items into Milestone docs when CER exposes them. Not model-invocable
  — the user calls this by name when they are ready to plan or rebalance
  sprints; it does not trigger itself on ambient planning conversation.
disable-model-invocation: true
metadata:
  version: "1.0"
---

# Rails Sprint Planning

Turn a Design doc and Milestone docs into an executable, prioritized Tier 4 story backlog, then assemble that backlog into scored, dependency-ordered, normalized Tier 3 Sprints.

This is the skill that replaces trying to hold an entire project's plan in your head and working multiple milestones at once. It exists so you only ever plan what's next, close to execution.

```text
Tier 1 Design -> Tier 2 Milestone -> Tier 3 Sprint -> Tier 4 Story (backlog) -> Tier 5 Implementation Plan
                                          ^ this skill assembles this          ^ this skill maintains this
```

`rails-sprint-planning` is a right-rail capability; its output (`context/milestones/`, `context/sprints/`, `context/backlog/`) lives in the target project's left rail.

## Not Model-Invocable

`disable-model-invocation: true` is intentional. This skill only runs when the user names it explicitly ("plan sprints for milestone X", "rebalance sprint Y", `/rails-sprint-planning ...`). It does not fire on ambient planning chatter, and it does not decide for itself when a sprint has drifted enough to need rebalancing — that judgment call belongs to the user (see Overflow below).

## Scope

### Owns the backlog

This skill **creates and maintains** `context/backlog/`. It is not a consumer of a backlog produced elsewhere — `rails-initialize-from-tier0` may seed the first backlog file during project setup, but this skill is what keeps it alive afterward: pulling new stories out of Design/Milestone docs, resorting, capping, and reclassifying, on an ongoing basis.

See [references/backlog-format.md](references/backlog-format.md) for the file cap, sort order, and story fields.

### Calls CER, doesn't reimplement it

Complexity/Effort/Risk scoring is **not owned here**. Follow the `rails-grade-cer` skill against backlog items and stories and consume its score table. This skill is a consumer of CER, same as the orchestrator downstream will be. Never invent a score.

### Reclassifies epics exposed by CER

When a backlog item's CER score comes back epic-sized, this skill pulls it out of the story backlog and promotes it to a Milestone doc under `context/milestones/` — see Reclassification below. CER exposes the epic; this skill acts on it.

### Does NOT do

- Design → Milestone breakdown negotiation. That is `rails-initialize-from-tier0` (or a future ingestion/7-tier planning skill), upstream of this one.
- Fragmenting a single story's implementation into Tier 6 Phases. That is downstream — `rails-planning-phaser`, run against a Tier 5 implementation plan.
- Computing CER scores itself. See above — always call `rails-grade-cer`.
- Selecting models or executing anything. That is the Orchestrator, which consumes this skill's Sprint output.

## Two Operating Modes

Same skill, two entry points, both interactive (see Interactivity below).

### Mode A — Per-milestone drain (initial)

Used on a fresh milestone to lay out its full delivery path:

1. Search `context/backlog/` for everything relevant to the milestone (e.g. milestone "Dockerize RivalSight" → search for Docker scripts, containerization, secrets).
2. Gather the matching stories.
3. Score them via `rails-grade-cer` — individually, then cumulatively for the candidate sprint grouping.
4. Order by interdependency (see Dependency Ordering below).
5. Assemble into one or more Sprints under `context/sprints/` — a milestone is not guaranteed to fit in a single sprint.

### Mode B — Per-sprint rebalance (ad-hoc)

Run any time — multiple times a day, weekly, monthly — against an **existing** sprint:

1. Re-check the sprint's stories against current scope/estimates. Re-run `rails-grade-cer` on any story whose scope looks like it moved since it was last scored.
2. If stories have blown out and no longer fit (see Overflow below), spawn a secondary sprint file and shunt the overflow into it.
3. Leave each resulting sprint with one clear, concise, single deliverable goal.

This is the mechanism that stops scope creep from silently bloating a sprint past its original intent.

## Interactivity Model

Sprint assembly is interactive, not a silent batch job:

1. Propose a sprint assembly — which stories, what order, how many sprints.
2. The user reviews and pushes back — too many sprints, wrong grouping, wrong order, whatever.
3. Negotiate until the shape fits.
4. Lock it in → write the normalized Sprint file(s), ready for the Orchestrator.

Do not write final sprint files before the user has signed off on the proposed shape. A draft proposal in chat first is fine; the durable file is the locked-in result.

## Dependency Ordering

Goals and milestones are sequential and are rarely worked out of order — default to the order the backlog and milestone docs already imply. Within a milestone drain, only reorder stories where a real dependency forces it (e.g. secrets work can't start before the Docker scripts it references exist).

Detect dependency in this priority order:

1. **Explicit.** A `Depends On` field on the story in the backlog (see [references/backlog-format.md](references/backlog-format.md)). Always trust this over inference.
2. **Inferred.** If no explicit field exists, infer from story content (one story's description references an artifact another story produces). Propose the inferred order to the user as part of the sprint proposal — do not silently lock in an inferred dependency without surfacing it.
3. **Default.** If neither applies, preserve backlog order (front-to-back = most urgent/concrete first, per [references/backlog-format.md](references/backlog-format.md)).

When you infer a dependency, write it back onto the story as an explicit `Depends On` field once the user confirms it, so the next drain or rebalance doesn't have to re-infer it.

## Reclassification (Epic Detection)

When `rails-grade-cer` returns a story with scores that are epic-sized (any axis materially past the story-tier range CER would expect, or CER's own reasoning calls out that the item reads like a milestone in disguise):

1. **Propose, don't silently promote.** Tell the user the item looks epic-sized and show the CER scores driving that read.
2. On confirmation, pull the item out of its backlog file and create a new `context/milestones/milestone-N.md` from it, following the milestone doc conventions already established in the project (or the starter's milestone template if this is the first milestone doc created this way).
3. Add the new milestone to the Milestones Index in `context/design.md` if that index exists.
4. Remove the promoted item from the backlog file it came from and renumber/re-sort that file per [references/backlog-format.md](references/backlog-format.md).

Never auto-promote without the confirmation step in 1 — reclassification changes tier ownership and downstream Sprint/Orchestrator assumptions, so it warrants a checkpoint even though most of this skill's other proposals can move fast.

## Overflow (Ad-Hoc Rebalance)

"Blown out" is a judgment call, not a fixed variance threshold. The user decides when a sprint no longer fits; this skill supports that call with CER re-scores rather than making the call itself.

- Re-score the drifted stories with `rails-grade-cer` and show the before/after (or current cumulative) numbers alongside the original sprint's cumulative scores.
- If the user judges the sprint blown out, split it: keep the still-fitting stories in the original sprint file, move the rest into a new secondary sprint file, and give each resulting sprint its own single deliverable goal.
- If the user judges it still fits despite a score increase, leave the sprint as one unit and just update its recorded cumulative scores.

Never spawn a secondary sprint on this skill's own initiative — always surface the re-score and let the user call it.

## Output

A normalized Sprint file — one or more per invocation — written to `context/sprints/sprint-N.md`, containing:

- The ordered set of stories assigned to it, with their story ids.
- Cumulative CER scores for the sprint.
- A single, clear deliverable goal statement.

See [references/sprint-template.md](references/sprint-template.md) for the exact structure. This is the artifact the Orchestrator consumes directly to begin execution — do not add execution instructions, model selections, or phase breakdowns to it; those belong further downstream.

## Hard Rules

- **Never invent a CER score.** Every complexity/effort/risk number in a backlog entry or sprint file comes from following `rails-grade-cer`. If a score is stale or missing, re-run CER before using it in a proposal.
- **Never silently promote an epic.** Reclassification always gets a confirmation checkpoint (see Reclassification).
- **Never silently spawn overflow.** Splitting a sprint is the user's call, supported by CER, never this skill's own initiative (see Overflow).
- **Never write a final Sprint or Milestone file before the user signs off on the proposed shape.** Propose in chat first; write only the locked-in result.
- **Respect the 30-story backlog file cap.** Overflow spawns a new backlog file rather than growing one file unbounded — see [references/backlog-format.md](references/backlog-format.md).
- **Preserve sequential order by default.** Do not reorder stories or milestones without a real, surfaced dependency reason.
- **Don't do the upstream or downstream job.** No Design→Milestone negotiation, no Tier 6 phase fragmentation, no model selection, no execution.

## Operating Model

1. Determine the entry point: a fresh milestone name (Mode A) or an existing sprint file (Mode B). Ask if ambiguous.
2. Load the minimum context needed: the named milestone doc and/or sprint file, the relevant `context/backlog/*.md` files, and `context/design.md`'s Milestones Index if present.
3. **Mode A:** search the backlog for stories matching the milestone, gather them, score via `rails-grade-cer`, determine dependency order (see Dependency Ordering), and draft a candidate sprint grouping (possibly more than one sprint).
4. **Mode B:** re-check the named sprint's stories, re-score any that look drifted, and determine whether the user judges it blown out (see Overflow).
5. Check every re-scored or newly-scored story for epic-sized results; if any are found, run the Reclassification checkpoint before continuing sprint assembly.
6. Propose the sprint shape to the user in chat (stories, order, count of sprints, cumulative scores, single deliverable goal per sprint). Negotiate.
7. On sign-off, write the locked Sprint file(s) to `context/sprints/sprint-N.md` using [references/sprint-template.md](references/sprint-template.md).
8. Update `context/backlog/*.md` to reflect any stories that moved into a sprint, any reclassified epics removed, and any newly-confirmed `Depends On` fields.
9. Report the exact paths of every file written or updated, plus the CER scores behind each decision.

## Validation

Before considering this skill applied correctly, confirm:

- Every score used came from a `rails-grade-cer` invocation, not an invented number.
- The user signed off on the sprint shape (stories, order, sprint count) before any Sprint file was written.
- Any epic-sized item was proposed for reclassification and only promoted after user confirmation.
- Any sprint split (overflow) happened only after the user judged the sprint blown out, with CER re-scores shown in support.
- Story order preserves sequential/backlog order except where a real dependency was surfaced and, if inferred, confirmed and written back as an explicit `Depends On` field.
- No backlog file exceeds 30 stories after this run; overflow went to a new backlog file, not an oversized existing one.
- Every written or updated file path (`context/backlog/*.md`, `context/milestones/*.md`, `context/sprints/*.md`) was reported to the user.
