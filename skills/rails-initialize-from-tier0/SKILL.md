---
name: rails-initialize-from-tier0
description: >-
  Use this skill when initializing or populating a newly created repository from
  the Agentic Rails context starter using a large Tier 0 intake document,
  dictated project seed, AI-generated research report, transcript, rough
  requirements dump, or kickoff notes.
  Use it to preserve the raw Tier 0 source, synthesize project-specific
  left-rail context, replace starter placeholders in design, milestones, goals,
  README, and related context files, and optionally seed initial implementation
  plans without overwriting reusable Agentic Rails framework material.
metadata:
  version: "1.4"
---

# Rails Initialize From Tier 0

Populate a new Agentic Rails-derived project from a raw Tier 0 document.

This is an intake synthesis skill, not a generic documentation rewrite. Preserve the human's raw source, then promote stable decisions into maintained context tiers so future agents can build from the repository instead of from memory.

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
2. Detect whether the project uses the current `context/` layout or the older `Documentation/` layout using [references/validation-and-scope.md](references/validation-and-scope.md).
3. Validate that the target appears to be a new or lightly populated Agentic Rails-derived project. If maintained design already contains real project truth, switch to enrichment/merge behavior instead of blank initialization.
4. Unless the user explicitly asks to implement immediately, write a short initialization plan naming target files, source inputs, scope boundaries, assumptions, and verification checks before editing.
5. Locate or create a durable Tier 0 intake file under the detected Tier 0 folder.
6. Preserve every raw Tier 0 input, including research reports, without polishing away uncertainty.
7. Create a checkpoint after preserving Tier 0 before broad synthesis, using Git only when available and appropriate.
8. Extract project signals: purpose, audience, problem, constraints, architecture, milestones, goals, non-goals, risks, external dependencies, and open questions.
9. Extract a canonical identity map: project name, repository name, old names to purge, new names to use, and transitional terms to avoid.
10. Choose a scale strategy. For more than 3-4 maintained files, use an orchestration or batch pattern so each pass has a focused file set.
11. Populate or replace starter placeholders in the maintained tiers using [references/tier0-synthesis-policy.md](references/tier0-synthesis-policy.md).
12. Keep reusable framework identity and template guidance intact where it is still useful.
13. Remove placeholder examples only from project-specific maintained truth after replacing them with real content.
14. Prefer tracking initialization itself as a near-term goal or context-synthesis Tier 4 plan when the repository uses goals for work tracking.
15. Produce the factual initialization report from [references/report-and-validation.md](references/report-and-validation.md).

## Default File Priority

Populate in dependency order:

1. `context/tier0/<intake-file>.md`
2. root `README.md`
3. `AGENTIC_RAILS_README.MD` front matter and project-specific references only
4. `AGENTS.md` project-specific fields only
5. `context/design.md`
6. `context/milestones.md`
7. `context/goals*.md`
8. support docs such as Tier 0 README/index, wiki/secrets guidance, and source/test/script README stubs when they still contain starter residue
9. optional initialization or ready-to-execute folders under `context/implementation-plans/`

Use equivalent paths under `Documentation/` when the target uses the older layout. Do not rewrite laws, workflow docs, wiki files, or implementation-plan templates unless the Tier 0 initialization explicitly requires project-specific additions and the change is safe.

## Safety Rules

- Never delete the raw Tier 0 source after synthesizing it.
- Never invent certainty. Record unknowns as assumptions or open questions.
- Never treat Tier 0 as authoritative after synthesis; maintained context becomes the working truth.
- Never overwrite reusable Agentic Rails framework explanation with project-specific prose.
- Never leave important requirements stranded only in Tier 0 when they affect design, milestones, goals, or plans.
- Never create detailed implementation plans for vague goals unless the user asks for planning exploration.
- Never store secrets, credentials, private keys, or sensitive personal data from the intake document. Redact or flag them for the user.
- Never assume Git is available. Use Git checks when the target is a Git repository; otherwise use filesystem and content verification.
- Never leave final maintained docs speaking as if the project is still a migration from another identity. Keep migration terms in raw Tier 0, logs, or explicit provenance only.
- Never force a blank-starter overwrite onto a project that already has maintained design, milestones, or goals. Treat late-stage Tier 0 as enrichment unless the user explicitly requests reinitialization.
