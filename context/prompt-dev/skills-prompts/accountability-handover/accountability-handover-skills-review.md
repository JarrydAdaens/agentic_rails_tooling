---
metadata:
  version: "1.0"
---

# Review: Accountability Handover Skills Plan

Reviewer perspective: the agent that would actually run these skills. Focus is on real gaps that would break the design's intent, not nitpicks.

## Biggest gap: the artifact workers can't see what they need to see

The design says the deep handover must **tutor** the human and **ground claims in source**. The plan ships each worker only the briefing path plus their artifact skill. Briefings as listed (repo shape, changed files, planning docs found, test commands, dependency surfaces) are *metadata*, not *content*. So either:

- **Workers re-Read/Grep the repo themselves.** Fine, but with 6 parallel workers you get 6 independent passes over the same code, no shared mental model, and contradictory facts in different artifacts ("no tests exist" in one, a cited test path in another).
- **Workers stay inside the briefing.** Then artifacts are surface-level rewordings — exactly the failure the design is built to prevent.

Pick one and write it down. Recommendation: make the Boss curate an **in-scope file list** (with brief role notes per file) inside the briefing, and require workers to Read those files before writing. That bounds inspection cost and gives every worker the same ground truth.

## The 180 review and retrospective are flying blind as fresh subagents

A subagent spawned to write `04-180-performance-review.md` has zero memory of the actual collaboration — no scope-creep events, no ambiguous instructions, no abandoned approaches. It can only observe commits and code. Same problem for `03-post-mortem-retrospective.md`'s "what was difficult" and "mistakes or weak calls" sections.

The Boss agent (which has the conversation context) is the only one who actually witnessed the collaboration. Three options:

1. The Boss writes those two artifacts itself, and only spawns workers for the source-grounded ones (technical report, walkthrough, SBOM, maintenance map).
2. The Boss explicitly distills conversation context — user friction, decisions, dropped paths, ambiguity moments — into the briefing as a "collaboration log" section, and workers cite it.
3. Rescope those artifacts to only what's observable from artifacts (loses most of the value).

Recommendation: do (1) and (2) together. The briefing's "user-stated task intent" line currently underweights this — it should be a substantial section.

## Default-parallel is the wrong default

Artifacts cite and depend on each other: the technical report establishes the architecture story; the walkthrough rides on it; the maintenance map's risk claims overlap the SBOM's dependency-risk notes; the index references everything. Parallel-from-the-start = duplication, drift, and contradictory claims the Boss has to catch in validation.

Cheap fix: **technical report runs first**, then the remaining workers run in parallel and are allowed to cite it. The index is last (already correct in the plan).

## Boss "validation" is overpromised

"Boss accepts an artifact only when major claims are source-grounded or marked uncertain … no artifact pretends unverified work was verified." Verifying that honestly means re-checking every claim against source — a task the size of the original write. Realistically Boss can only spot-check, scan for unhedged certainty words, and trust the worker's structured return contract.

Be honest about this in the plan. Add a concrete worker return field like `claims_verified_against_source: [list]` and `claims_inferred_or_assumed: [list]` so Boss has something structured to spot-check rather than re-reading prose.

## Smaller things worth deciding before you build

- **Where do the output files live?** `shallow-accountability-handover.md` and `deep-accountability-handover/` — at repo root? Under `documentation/`? In the target repo or this tooling repo? The `complaining` skill solved this with a `references/path-selection.md`; do the same.
- **"Reusable directly" claim for the artifact skills is shaky.** A standalone `performance-review-180-handover` invocation has no briefing and no collaboration log. Either accept they're worker-only, or design a fallback path for direct use.
- **No size guard.** Six parallel workers re-inspecting a large repo gets expensive fast. Worth a "if changed-file count > N, recommend shallow first or scope to a subset" check in the Boss.
- **Skill folder count.** 8 new skills + 1 agent for one feature is a lot of surface. The six artifact skills are very thin (one Markdown template each). Worth considering whether they should be `references/<artifact>.md` files inside the deep skill rather than standalone skills — fewer SKILL.mds to maintain, same worker dispatch story.

## Questions for the author

1. Is the deep handover meant to run on **the work just done in this conversation** (so the Boss has all the context) or on **a project the agent is seeing for the first time** (cold start from git history)? The plan reads like both — they need different briefing strategies.
2. For the 180 review: do you want the AI to actually be candid about the human, or is this aspirational? It's the most novel artifact and also the one most likely to get watered down by safety reflexes if not explicitly licensed in the skill text.
3. How married are you to having one skill per artifact vs. folding the templates into `references/` under the deep skill? Either works; the multi-skill version is more decomposable but heavier to maintain.
