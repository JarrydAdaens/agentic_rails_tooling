---
name: rails-initialize-from-tier0
description: >-
  Use this skill when initializing or populating a newly created repository from
  the Agentic Rails context starter using a large Tier 0 intake document,
  dictated project seed, AI-generated research report, transcript, rough
  requirements dump, or kickoff notes.
  Use it to preserve the raw Tier 0 dictation, synthesize project-specific
  left-rail context, replace starter placeholders in design (with its Milestones
  Index), milestone docs, the story backlog, README, and related context files,
  and optionally seed sprints or initial implementation plans without
  overwriting reusable Agentic Rails framework material.
disable-model-invocation: true
metadata:
  version: "2.0"
---

# Rails Initialize From Tier 0

Populate a new Agentic Rails-derived project from a raw Tier 0 dictation.

This is an intake synthesis skill, not a generic documentation rewrite. Preserve the human's raw source, then promote stable decisions into the maintained seven-tier context system so future agents can build from the repository instead of from memory.

## The Seven-Tier Target

The current context starter uses a seven-tier, backlog-driven, Scrum-aligned layout. Initialization populates the upper, planning-time tiers and leaves the lower, execution-time tiers as scaffolding:

| Tier | Location | Initialization role |
| --- | --- | --- |
| 0 - Transcription | `context/dictations-tier-0/` | Preserve the raw intake faithfully. |
| 1 - Design | `context/design.md` | Main synthesis target; includes the **Milestones Index** subsection. |
| 2 - Milestone | `context/milestones/milestone-N.md` | One file per milestone; keep in sync with the Milestones Index. |
| 3 - Sprint | `context/sprints/sprint-N.md` | Usually deferred — sprint planning happens close to execution. |
| 4 - Story | `context/backlog/backlog-N.md` | Build the priority-sorted story backlog (30 stories per file). |
| 5 - Implementation Plan | `context/implementation-plans/STORY_*/plan.md` | Optional; only when a story is ready to execute. |
| 6 - Phase *(optional)* | `context/implementation-plans/STORY_*/` | Not created during initialization. |

The retired vocabulary matters: there are no `goals`, no single `milestones.md`, and no `tier0/` folder. The discrete work unit is a **Story** living in the `backlog/`; milestones are a folder of docs indexed from `design.md`.

## Required Input

Require a Tier 0 source document or pasted Tier 0 source text.

If the user did not provide the Tier 0 source, ask exactly:

```text
Please provide the Tier 0 source document path or paste the raw Tier 0 intake text you want synthesized into this Agentic Rails project.
```

Default the target project root to the current repository unless the user provides a target path.

The local `agentic_rails_context_starter` checkout is optional when the target already contains starter files. If the target is missing core starter structure, ask for the starter path before creating missing structure.

## Progressive Disclosure

Load only the reference needed for the current phase:

- For required inputs, target checks, starter signals, and files in scope, read [references/validation-and-scope.md](references/validation-and-scope.md).
- For Tier 0 preservation, synthesis rules, and how to populate each maintained context tier, read [references/tier0-synthesis-policy.md](references/tier0-synthesis-policy.md).
- For the final report, completion checklist, and example trigger patterns, read [references/report-and-validation.md](references/report-and-validation.md).

## Operating Model

1. Identify the target project root. Default to the current repository.
2. Confirm the target uses the current seven-tier `context/` layout (`dictations-tier-0/`, `design.md`, `milestones/`, `sprints/`, `backlog/`, `implementation-plans/`). Treat old five-tier signals (a single `milestones.md`, `goals*.md`, or a `tier0/` folder) as drift, using [references/validation-and-scope.md](references/validation-and-scope.md).
3. Validate that the target appears to be a new or lightly populated Agentic Rails-derived project. If maintained design already contains real project truth, switch to enrichment/merge behavior instead of blank initialization.
4. Unless the user explicitly asks to implement immediately, write a short initialization plan naming target files, source inputs, scope boundaries, assumptions, and verification checks before editing.
5. Locate or create a durable Tier 0 intake file under `context/dictations-tier-0/`.
6. Preserve every raw Tier 0 input, including research reports, without polishing away uncertainty.
7. Create a checkpoint after preserving Tier 0 before broad synthesis, using Git only when available and appropriate.
8. Extract project signals: purpose, audience, problem, constraints, architecture, milestones, stories, non-goals, risks, external dependencies, and open questions.
9. Extract a canonical identity map: project name, repository name, old names to purge, new names to use, and transitional terms to avoid.
10. Choose a scale strategy. For more than 3-4 maintained files, use an orchestration or batch pattern so each pass has a focused file set.
11. Populate or replace starter placeholders in the maintained tiers using [references/tier0-synthesis-policy.md](references/tier0-synthesis-policy.md): Design + Milestones Index first, then the milestone docs, then the story backlog.
12. Keep reusable framework identity and template guidance intact where it is still useful.
13. Remove placeholder examples only from project-specific maintained truth after replacing them with real content.
14. Prefer tracking initialization itself as the first backlog story or a Tier 5 context-synthesis plan when the repository tracks setup work.
15. Produce the factual initialization report from [references/report-and-validation.md](references/report-and-validation.md).

## Default File Priority

Populate in dependency order:

1. `context/dictations-tier-0/<intake-file>.md` (Tier 0)
2. root `README.md`
3. `AGENTIC_RAILS_README.MD` front matter and project-specific references only
4. `AGENTS.md` project-specific fields only
5. `context/design.md` (Tier 1), including the **Milestones Index** subsection
6. `context/milestones/milestone-N.md` (Tier 2), one file per milestone, kept in sync with the Milestones Index
7. `context/backlog/backlog-N.md` (Tier 4 stories), priority-sorted, 30 stories per file
8. support docs such as the Tier 0 README/index, wiki/secrets guidance, and source/test/script README stubs when they still contain starter residue
9. optional Tier 3 `context/sprints/sprint-N.md` and Tier 5 folders under `context/implementation-plans/`, only when work is ready to execute or the user asks

Do not rewrite laws, the workflow doc, wiki files, or the milestone/sprint/backlog/dictation templates unless the Tier 0 initialization explicitly requires project-specific additions and the change is safe.

## Safety Rules

- Never delete the raw Tier 0 source after synthesizing it.
- Never invent certainty. Record unknowns as assumptions or open questions.
- Never treat Tier 0 as authoritative after synthesis; maintained context becomes the working truth.
- Never overwrite reusable Agentic Rails framework explanation with project-specific prose.
- Never leave important requirements stranded only in Tier 0 when they affect design, milestones, the backlog, or plans.
- Never force premature sprint planning. Initialization builds Design, Milestones, and the Backlog; sprints and implementation plans are planned close to execution unless the user asks otherwise.
- Never create detailed implementation plans for vague stories unless the user asks for planning exploration.
- Never store secrets, credentials, private keys, or sensitive personal data from the intake document. Redact or flag them for the user.
- Never assume Git is available. Use Git checks when the target is a Git repository; otherwise use filesystem and content verification.
- Never leave final maintained docs speaking as if the project is still a migration from another identity. Keep migration terms in raw Tier 0, logs, or explicit provenance only.
- Never force a blank-starter overwrite onto a project that already has maintained design, milestones, or a real backlog. Treat late-stage Tier 0 as enrichment unless the user explicitly requests reinitialization.
- Never reintroduce retired vocabulary: no `goals`, no single `milestones.md`, no `tier0/` folder, and never use `task` as a tier name.
