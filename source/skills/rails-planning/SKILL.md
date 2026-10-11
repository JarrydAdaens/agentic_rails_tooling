---
name: rails-planning
description: Use this skill to create, locate, or revise one durable plan for substantial repository work, preserving existing decisions and the project's chosen tracking location.
disable-model-invocation: false
argument-hint: "<work request or plan path> [--revise] [--sidecar evidence,complaining,thinking]"
metadata:
  version: "3.0"
---

# Rails Planning

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently; plain-language equivalents carry the same meaning as tokens.

| Token | Meaning |
| --- | --- |
| `--revise` | Revise the existing plan. Absent means discover whether one already owns this work. |
| `--sidecar <names>` | Explicitly requested evidence, complaining, or thinking sidecars. Absent means none. |
| anything else | Work request or plan path; empty arguments use established session scope and known paths. |

## References

- [Plan structure](references/plan-template.md)
- [Open questions and sidecars](references/questions-format.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Use a durable plan when dependencies, scope, uncertainty, consequence, or continuation make it useful, or when the user explicitly requests one. A routine small edit needs no milestone, scorecard, or planning artifact by default.
- Keep one primary plan for the work. Reuse the current plan or established local location, including `context/current-plan.md`. An external tracker may own status; link it rather than mirroring its ledger.
- New unassigned substantial work may use `context/implementation-plans/<work-slug>/plan.md`. Adopted milestone stories may use `context/implementation-plans/<milestone-slug>/<story-slug>/plan.md`. All paths are relative to the target repository root. Preserve historical paths; do not invent a milestone or move existing plans for tidiness.
- Preserve user decisions, historical execution evidence, and unrelated dirty work. Raw Dictation informs the plan; maintained project decisions govern unless the user explicitly supersedes them.
- Size steps from real dependencies and independently verifiable outcomes. CER is optional qualitative assessment through `rails-grade-cer`, never numerical model routing or a prerequisite to routine work.
- Deterministic checks follow the affected artifact. Consequential boundaries may warrant one independent reviewer with scope, acceptance, and user decisions. Compaction does not provide reviewer independence.
- Commit policy comes from session authorization. Planning neither requires nor authorizes a commit, implementation, deployment, or a new delegation run.
- Sidecars need an explicit request or a concrete separately maintained evidence need; record that reason. They contain sanitized observations, never private reasoning traces.

## Workflow

1. Read the target's instructions, the named request, and relevant maintained context. Inspect existing plans, adopted profile, tracker ownership, and Git state when available.
2. Resolve new planning versus revision and whether durable planning serves this work. If the requested task is a routine implementation edit, proceed under its existing authority; do not turn this skill into a barrier.
3. Select the existing plan or a collision-free descriptive path using the rule list. Write the outcome, scope, constraints, likely affected files, dependencies, acceptance, checks, and important unknowns using the reference.
4. Sequence the work by prerequisites. Identify blocked items, what can proceed independently, recovery needs, and estimate uncertainty. Leave later work thin until evidence supports detail.
5. Record any optional CER result inline, including evidence and uncertainty. Invoke `rails-planning-phaser` only when natural delivery seams justify phases or the user requests it.
6. Save the plan and report its path, assumptions that affect delivery, and unresolved requirements. Report a deliberate chat-only or no-plan outcome when that matches the task.

## Surviving compaction

For a long planning session, the selected primary plan carries accepted decisions, open questions, source links, and the next planning step. Write these before changing focus or starting the next step. Resume by reading that plan and checking current project state; no forced reset is required.

## Observable output

The selected plan exists at the reported location and identifies concrete acceptance checks and dependencies. Existing execution history remains present. Optional files have a recorded purpose, and a small task has no invented milestone.
