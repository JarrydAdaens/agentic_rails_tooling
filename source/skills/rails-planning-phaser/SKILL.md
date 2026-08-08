---
name: rails-planning-phaser
description: >-
  Use this skill to fracture a plan into sequential, executable phases. It grades
  the plan with CER, and if any axis breaches threshold it splits the plan at
  natural seams into small phases that each fit under the local model's threshold,
  re-grades every phase, and rewrites the original plan into a manifest that
  registers and tracks them. Use whenever a plan is too large, complex, or risky
  to run as one unit; when work needs to be sized for a local model; or when
  preparing a plan for orchestrated sub-agent execution. Assigns each phase a
  model tier and escalates to the human if the work needs more than seven phases
  (it's really multiple stories) or can't be reduced below threshold.
disable-model-invocation: false
argument-hint: "<plan path> [--dry-run] [--rephase]"
metadata:
  version: "1.1"
---

# Rails Planning Phaser

Take a single plan, grade it with `rails-grade-cer`, and — if it breaches threshold — fracture it into **sequential phases** small enough for a local model to execute end-to-end. Rewrite the original plan into a **manifest** that points at the phases and tracks their execution.

The point is a dark factory: keep real execution on the local rig by default, sizing each phase so the local model can actually do the work rather than deferring to a cloud model. Where phasing cannot get a phase small enough, this skill assigns it up the model tier rather than over-cutting.

Phasing is not triggered by failure. A plan scoring past threshold has not failed — it is just larger than one execution unit. That is ordinary software engineering. This skill's job is to size the work to the executor.

## Arguments

The skill was invoked with: $ARGUMENTS

Read that line before doing anything else. It is free text, so parse it leniently, and treat plain-language equivalents as equal to the tokens ("just show me the cut" is `--dry-run`).

| Token | Meaning |
| --- | --- |
| `--dry-run` | Report the proposed phase boundaries and scores without writing phase files or rewriting the plan. Absent means write. |
| `--rephase` | Proceed on a target that is already phased, replacing the existing manifest and phase files. Absent means refuse — see the already-phased check. |
| anything else | The path to the plan being phased. Ask only if it cannot be resolved. |

Empty `$ARGUMENTS` means phase the named plan for real, refusing if it is already phased — the normal case.

## Why This Shape

The rules are in [the rule list below](#non-negotiable-rules); these are the reasons behind them, stated once.

- **Phasing sizes work to an executor, it does not judge quality.** The threshold is the local model's competence boundary, not a quality bar, and a plan scoring past it has not failed — it is simply larger than one execution unit.
- **Cut at natural seams, not by arithmetic.** Because seams are respected rather than effort being sliced into equal buckets, the *sum* of phase scores can exceed the original plan's scores. That is expected, not a defect.
- **Lean on the plan's own structure.** A good plan already describes testable increments; this skill groups them. The grouping hints in the loop are hints, not a seam-finding algorithm.
- **Say when phasing cannot help.** Work that is inherently too big or too risky to reduce should be reported as such, not dressed up as solved.

## Relationship To `rails-grade-cer`

This skill holds no grading rubric of its own. Every score in this skill comes from following the `rails-grade-cer` skill against the whole document being scored (the original plan, or later, an individual phase). Grade all three axes at `concise` detail — this skill only needs the score table, not the paragraphs.

`rails-grade-cer` returns its score card inline by default and writes a `cer-score-card.md` file only when one was explicitly requested. Take the scores from what it returns — never go looking for a file, and never treat a missing one as a failure. This skill embeds the scores into the manifest and phase frontmatter rather than keeping grading artifacts around, so **if** a score-card file was produced, delete it after reading. The plan's scoring history is not lost: it lives in the manifest and in git history, not as loose score-card files.

## Inputs

- **Target document.** A plan by default, but this skill can run on anything CER can grade — a plan, a phase, or a story summary. Locate it via the canonical Agentic Rails plan path (`context/implementation-plans/<milestone-slug>/<story-slug>/plan.md`) or an explicit path the user gives. If ambiguous, ask. A plan found one level deep under a legacy layout still works when named explicitly — report the layout rather than migrating it.
- **Thresholds.** Come from [references/model-matrix.md](references/model-matrix.md), not from the user, and that file is the only place the numbers and the comparison are stated. They are provisional seeds, not yet calibrated against real completion outcomes; treat them as authoritative until better data exists, and do not let the user override them ad hoc.
- This skill reads the target, writes the manifest and phase files, and follows `rails-grade-cer` for every score. It does not execute the plan's work.

## Already-Phased Check (do this first)

Before doing anything else, check whether the target folder already looks phased: a `plan.md` containing a Phase Registry table, or existing `phase-1.md`/`phase-N.md` files beside it.

If it is already phased, **refuse**: tell the user the plan is already phased, point them at the existing manifest and phase files, and stop. Do not re-phase, diff, or silently overwrite. If the user wants to redo phasing, they can say so explicitly and re-run this skill after reverting or removing the existing manifest state themselves.

A plan carrying only a single-unit CER annotation (see below) is **not** considered phased — it has no phase registry or phase files, so this skill may run on it again if its CER scores have since changed.

## The Phasing Loop

1. **Grade the target with CER.** Follow `rails-grade-cer` on the whole document, all three axes, `concise` detail. Read the scores it returns; delete a `cer-score-card.md` only if one was produced.

2. **Check against the tier-1 threshold** from [references/model-matrix.md](references/model-matrix.md), whose Assignment Rule defines what "covered" means:
   - **tier 1 covers all three axes** → no phasing needed. Annotate the plan in place with a single-unit CER assignment block (see [references/manifest-template.md](references/manifest-template.md), Single-Unit Variant) and stop. No phase files, no phase registry table — there is only one unit of work and it already fits the local model.
   - **Any axis exceeds tier 1** → phase it (continue).

3. **Fracture at natural seams.** Read the plan's own structure (its implementation steps, file groupings, and stated completion points) and group it into candidate phases, each a complete, testable increment. Aim for each phase to land inside tier 1 on all three axes. Useful hints, not rules: bundle setup/scaffolding work into an early phase, cut at points the plan itself already treats as checkpoints, keep a step and everything it strictly depends on in the same phase, and never propose a cut that would leave the app non-compiling or a feature half-wired.

4. **Ceiling check — before writing anything.** Count the candidate phases. If more than **7**, stop immediately: do not write phase files, do not modify the original plan. Escalate to the human (see the Seven-Phase Ceiling section below) and end here.

5. **Write draft phase files.** For each candidate phase, write `phase-1.md` … `phase-N.md` beside the original plan using [references/phase-template.md](references/phase-template.md), with the phase's slice of the work but placeholder frontmatter (no scores yet).

6. **Re-grade every phase with CER.** One CER invocation per phase file just written, identical in method to step 1. Embed the resulting three scores into that phase file's frontmatter. Delete any `cer-score-card.md` that was produced.

7. **Resolve phases that will not drop below threshold.** If a phase still exceeds tier 1 after natural-seam grouping — because merging was needed to stay testable, or the work is inherently heavy — do **not** over-cut it further. Assign it up [references/model-matrix.md](references/model-matrix.md) to the lowest tier whose thresholds cover all three of its scores. Leave it as one phase at that tier.

8. **Assign models and rewrite the manifest.** Every phase gets an assigned model in the manifest's phase registry and a matching recommended model in its own frontmatter. Rewrite the original `plan.md` in place into the manifest using the Full Manifest Variant in [references/manifest-template.md](references/manifest-template.md).

9. **Report.** Tell the user the manifest path, every phase file path, each phase's assigned model and scores, and whether any phase was tiered up instead of reduced.

## Model Capability Matrix

The tier table, the inclusive comparison, and the assignment rule all live in [references/model-matrix.md](references/model-matrix.md). Read it before assigning a tier. The only consequence needed here: this skill tries to fit every phase into tier 1 before accepting a higher tier.

## The Seven-Phase Ceiling

Seven phases is the hard ceiling. Needing an eighth means the target is mis-tiered: it is a story that should be split into at least two stories before phasing.

On breach, this skill does **not** produce phase files and does **not** touch the original plan. It stops and tells the human plainly: this is too many phases for one unit of work, so split the original into multiple stories at the Story tier, then run this skill on each story separately. Name the problem; do not attempt the story split yourself — that is one tier up, and this skill's job stops at phasing.

## The Manifest

The original `plan.md` is **rewritten in place** into a manifest when phasing occurs. No separate copy of the pre-phase plan is kept — git history holds the previous version. A parent plan sitting alongside its own phases would just create conflicting sources of truth.

The manifest is the single source of truth and the communication channel between sub-agents: an orchestrator reads it, spins up a sub-agent for the next phase, hands it the manifest plus that phase file. The sub-agent executes, writes its status and notes back into the manifest's phase registry row, and returns. The next sub-agent sees the updated state.

Keep the plan-level context carried into the manifest **short**: one paragraph condensing the original goal/objective and high-level scope. Do not copy the full original plan body verbatim — the detail that mattered for execution now lives in the phase files, and the original wording remains fully recoverable from git history. See [references/manifest-template.md](references/manifest-template.md) for the exact structure and the phase registry table schema.

## Phase Files

Phase files are small plans — same shape as any Agentic Rails plan, just guaranteed small (fits under threshold, or is the smallest legal testable unit at its assigned tier).

- **Naming:** `phase-1.md`, `phase-2.md`, `phase-3.md` … Sequential integers only. Never a content-based name — a descriptive name adds nothing for a smaller model loading one specific phase file and only invites drift from the registry.
- **Location:** the plan's existing folder, beside the manifest.
- **Structure:** frontmatter carries the recommended model and the three CER scores; the body carries the same kind of content a plan uses (objective, steps, verification, acceptance). See [references/phase-template.md](references/phase-template.md).

This is progressive disclosure in practice: a sub-agent working phase 2 loads only phase 2, not the entire original plan. It reads the manifest for state and its own phase file for the work — nothing more. The manifest's **assigned** model for a phase and that phase file's own **recommended** model must always agree; if they do not, something in the phasing process broke and should be corrected before reporting done.

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- **Never break the build.** No phase leaves the application non-compiling or non-running. A phase must be independently testable. This outranks hitting the threshold.
- **Sequential only.** Phases run in order. Never emit or imply phases can execute out of order.
- **Local first, and never over-cut.** Always try to fit tier 1, but do not split past what natural seams allow just to force a lower score. When no legal seam gets a phase into tier 1, assign it up a tier and leave it whole.
- **Stop at seven.** More than seven candidate phases → escalate to the human as a mis-tiered story. Emit no phase files, touch no existing files.
- **Rewrite, don't duplicate.** The plan becomes the manifest in place. No parallel copy of the pre-phase plan.
- **Don't execute.** This skill phases, grades, and assigns models. It does not do the plan's work.
- **Grade via CER only.** Every score comes from following `rails-grade-cer`. This skill holds no rubric of its own, and never invents a number.
- **Don't litter grading artifacts.** If a `cer-score-card.md` was produced, delete it after reading its scores. Usually there is nothing to delete.
- **Refuse on already-phased targets.** If a manifest and phase files already exist, stop and tell the user — do not silently re-phase or overwrite.

## Acceptance

Observable facts about what landed on disk:

- Either the plan carries a single-unit CER annotation and no `phase-*.md` files exist, or there are between 1 and 7 files named `phase-N.md` with sequential integers.
- No `cer-score-card.md` produced by this run remains in the plan's folder. One the user asked for separately is theirs to keep.
- Every phase's assigned model in the manifest string-matches that phase file's own recommended model.
- The manifest's plan-level context is shorter than the original plan body, not a copy of it.
- When the ceiling was breached: no `phase-*.md` files exist, the original `plan.md` is unmodified, and the escalation was reported.
- The exact paths of the manifest and every phase file were reported to the user.
