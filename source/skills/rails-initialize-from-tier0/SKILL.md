---
name: rails-initialize-from-tier0
description: >-
  Use this skill when initializing or populating a newly created repository from
  the Agentic Rails context starter using a large dictation intake document,
  dictated project seed, AI-generated research report, transcript, rough
  requirements dump, or kickoff notes.
  Use it to preserve the raw dictation, synthesize project-specific
  left-rail context, replace starter placeholders in design (with its Milestones
  Index), milestone docs, the story backlog, README, and related context files,
  and optionally seed initial implementation plans without overwriting reusable
  Agentic Rails framework material.
disable-model-invocation: true
metadata:
  version: "2.1"
---

# Rails Initialize From Dictation

Populate a new Agentic Rails-derived project from a raw dictation intake.

This is an intake synthesis skill, not a generic documentation rewrite. Preserve the human's raw source, then promote stable decisions into the maintained context tier system so future agents can build from the repository instead of from memory.

## The Context Tier System

The current context starter uses a milestone-centric layout. Initialization populates the upper, planning-time tiers and leaves the lower, execution-time tiers as scaffolding:

| Name | Location | Initialization role |
| --- | --- | --- |
| Dictation | `context/dictations-tier-0/` | Preserve the raw intake faithfully. |
| Design | `context/design.md` | Main synthesis target; includes the **Milestones Index** subsection. |
| Milestone | `context/milestones/milestone-N.md` | One file per milestone; keep in sync with the Milestones Index. Contains that milestone's story list directly. |
| Story | Inside milestone docs, optionally staged first in `context/backlog/` | Build the story list for each milestone, drawing from the backlog's unscheduled story inventory. |
| Implementation Plan | `context/implementation-plans/<milestone-slug>/<story-slug>/plan.md` | Optional; only when a story is ready to execute. |
| Phase *(optional)* | Inside the story's plan folder | Not created during initialization. |

The retired vocabulary matters: there are no `goals`, no single `milestones.md`, no `tier0/` folder, and no separate scheduling layer between Milestone and Story. The discrete work unit is a **Story** that lives directly inside a milestone document, optionally staged first in `backlog/` — an unscheduled story inventory, not a formal tier. Milestones are a folder of docs indexed from `design.md`.

## Required Input

Require a dictation source document or pasted dictation source text.

If the user did not provide the dictation source, ask exactly:

```text
Please provide the dictation source document path or paste the raw dictation intake text you want synthesized into this Agentic Rails project.
```

Default the target project root to the current repository unless the user provides a target path.

The local `agentic_rails_context_starter` checkout is optional when the target already contains starter files. If the target is missing core starter structure, ask for the starter path before creating missing structure.

## Progressive Disclosure

Load only the reference needed for the current phase:

- For required inputs, target checks, starter signals, and files in scope, read [references/validation-and-scope.md](references/validation-and-scope.md).
- For dictation preservation, synthesis rules, and how to populate each maintained context tier, read [references/tier0-synthesis-policy.md](references/tier0-synthesis-policy.md).
- For the final report, completion checklist, and example trigger patterns, read [references/report-and-validation.md](references/report-and-validation.md).

## Operating Model

1. Identify the target project root. Default to the current repository.
2. Confirm the target uses the current context tier system layout (`dictations-tier-0/`, `design.md`, `milestones/`, `backlog/`, `implementation-plans/`). Treat legacy layout signals as drift rather than a supported layout, using [references/validation-and-scope.md](references/validation-and-scope.md).
3. Validate that the target appears to be a new or lightly populated Agentic Rails-derived project. If maintained design already contains real project truth, switch to enrichment/merge behavior instead of blank initialization.
4. Unless the user explicitly asks to implement immediately, write a short initialization plan naming target files, source inputs, scope boundaries, assumptions, and verification checks before editing.
5. Locate or create a durable dictation intake file under `context/dictations-tier-0/`.
6. Preserve every raw dictation input, including research reports, without polishing away uncertainty.
7. Create a checkpoint after preserving the dictation before broad synthesis, using Git only when available and appropriate.
8. Extract project signals: purpose, audience, problem, constraints, architecture, milestones, stories, non-goals, risks, external dependencies, and open questions.
9. Extract a canonical identity map: project name, repository name, old names to purge, new names to use, and transitional terms to avoid.
10. Choose a scale strategy. For more than 3-4 maintained files, use an orchestration or batch pattern so each pass has a focused file set.
11. Populate or replace starter placeholders in the maintained tiers using [references/tier0-synthesis-policy.md](references/tier0-synthesis-policy.md): Design + Milestones Index first, then the milestone docs, then the story backlog.
12. Keep reusable framework identity and template guidance intact where it is still useful.
13. Remove placeholder examples only from project-specific maintained truth after replacing them with real content.
14. Prefer tracking initialization itself as the first backlog story or a context-synthesis implementation plan when the repository tracks setup work.
15. Produce the factual initialization report from [references/report-and-validation.md](references/report-and-validation.md).

## Default File Priority

Populate in dependency order:

1. `context/dictations-tier-0/<intake-file>.md` (Dictation)
2. root `README.md`
3. `AGENTIC_RAILS_README.MD` front matter and project-specific references only
4. `AGENTS.md` project-specific fields only
5. `context/design.md` (Design), including the **Milestones Index** subsection
6. `context/milestones/milestone-N.md` (Milestone), one file per milestone, kept in sync with the Milestones Index
7. `context/backlog/backlog-N.md` (story inventory), priority-sorted, 30 stories per file
8. support docs such as the Dictation README/index, wiki/secrets guidance, and source/test/script README stubs when they still contain starter residue
9. optional `context/implementation-plans/<milestone-slug>/<story-slug>/plan.md` folders, only when work is ready to execute or the user asks

Do not rewrite laws, the workflow doc, wiki files, or the milestone/backlog/dictation templates unless the dictation initialization explicitly requires project-specific additions and the change is safe.

## Safety Rules

- Never delete the raw dictation source after synthesizing it.
- Never invent certainty. Record unknowns as assumptions or open questions.
- Never treat the dictation as authoritative after synthesis; maintained context becomes the working truth.
- Never overwrite reusable Agentic Rails framework explanation with project-specific prose.
- Never leave important requirements stranded only in the dictation when they affect design, milestones, the backlog, or plans.
- Never force premature implementation planning. Initialization builds Design, Milestones, and the Backlog; stories are pulled into milestones and implementation plans are written close to execution unless the user asks otherwise.
- Never create detailed implementation plans for vague stories unless the user asks for planning exploration.
- Never store secrets, credentials, private keys, or sensitive personal data from the intake document. Redact or flag them for the user.
- Never assume Git is available. Use Git checks when the target is a Git repository; otherwise use filesystem and content verification.
- Never leave final maintained docs speaking as if the project is still a migration from another identity. Keep migration terms in raw dictation, logs, or explicit provenance only.
- Never force a blank-starter overwrite onto a project that already has maintained design, milestones, or a real backlog. Treat late-stage dictation as enrichment unless the user explicitly requests reinitialization.
- Never reintroduce retired vocabulary: no `goals`, no single `milestones.md`, no `tier0/` folder, and never use `task` as a tier name.
