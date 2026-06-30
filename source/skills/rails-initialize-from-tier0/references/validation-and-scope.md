---
name: rails-initialize-from-tier0-validation-and-scope
metadata:
  version: "2.0"
---

# Validation And Scope

Use this reference when starting `rails-initialize-from-tier0`, validating paths, or deciding which files are in scope.

## Required Inputs

The skill needs:

- Target project root: default to the current repository when the user does not specify a path.
- Tier 0 source: one or more file paths, pasted texts, or existing files under `context/dictations-tier-0/`.

If the Tier 0 source is pasted in chat or lives outside the repository, create a durable repo-local intake file before synthesizing it. Do not make future agents depend on a downloads folder, chat transcript, or machine-specific external path.

Use a filename like:

```text
YYYY-MM-DD_initial_project_seed.md
YYYY-MM-DD_deep_research_report_<short-topic>.md
YYYY-MM-DD_kickoff_notes_<short-topic>.md
YYYY-MM-DD_addendum_<short-topic>.md
```

Useful initialization inputs can include a raw voice dictation plus an AI-generated deep research synthesis, such as a NotebookLM research report. Preserve both as Tier 0 and treat the research report as partially synthesized source material, not as maintained truth by itself.

Distinguish initialization seeds from later enrichment inputs. A Tier 0 file about outstanding questions, milestone prep, or a narrow addendum is usually not enough to initialize a repository from scratch.

## Layout Detection

Confirm the target uses the current seven-tier `context/` layout before choosing paths:

```text
context/
context/dictations-tier-0/
context/design.md            (contains the Milestones Index subsection)
context/milestones/          (one milestone-N.md per milestone)
context/sprints/             (one sprint-N.md per sprint)
context/backlog/             (backlog-N.md story files, 30 stories per file)
context/implementation-plans/
context/laws.md
context/agenticworkflow.md
context/agent-thinking.md
context/wiki/
```

Set these working variables in the initialization plan:

- context root: `context/`
- Tier 0 folder: `context/dictations-tier-0/`
- Tier 1 design file: `context/design.md` (Milestones Index lives inside it)
- Tier 2 milestone folder: `context/milestones/`
- Tier 3 sprint folder: `context/sprints/`
- Tier 4 backlog folder: `context/backlog/`
- Tier 5 implementation-plan folder: `context/implementation-plans/`

### Drift detection (old five-tier signals)

If the target shows old five-tier residue instead of the seven-tier layout, treat it as drift, not as a supported layout:

- a single `context/milestones.md` file (now a `milestones/` folder plus a Milestones Index in `design.md`)
- `context/goals*.md` files (the `goal` work unit is retired; the work unit is now a **Story** in `backlog/`)
- a `context/tier0/` folder (now `context/dictations-tier-0/`)
- a `Documentation/` context root (older era; the current starter uses `context/`)

Do not silently convert a drifted repository as part of Tier 0 initialization. Report the drift and recommend updating the project from the current starter (for example with `rails-update-from-starter`) before, or alongside, initialization. If front matter shows an old or missing `agentic_rails_source_version`, expect path and metadata drift; validate actual files instead of assuming structure.

## Target Project Validation

Run from the derived child project unless the user provides a target project path.

Strong Agentic Rails target signals include:

- `AGENTIC_RAILS_README.MD`
- `AGENTS.md`
- `context/`
- `context/dictations-tier-0/`
- `context/design.md` (with a Milestones Index)
- `context/milestones/`
- `context/sprints/`
- `context/backlog/`
- `context/implementation-plans/`

If the target lacks most of these signals, stop and ask whether this is the intended repository.

If the detected design, milestone, or backlog files already contain real project-specific content, treat the task as enrichment or selective re-synthesis, not blank initialization. Ask before replacing maintained truth unless the user explicitly requested a full reinitialization.

Do not use this skill on:

- the central `agentic_rails_context_starter` repository itself
- the reusable `agentic_rails_tooling` repository
- the `agentic-rails-memory` repository
- generic skills, agents, rules, or workflow tooling repositories

## Starter Path Use

The local `agentic_rails_context_starter` path is optional when the target already contains the expected starter files.

Ask for the starter path only when:

- the target is missing core starter structure
- the agent must recreate starter files or compare against the current starter
- the user explicitly asks to refresh starter structure during initialization

If a starter path is supplied, validate it with signals such as:

- `AGENTIC_RAILS_README.MD`
- `AGENTS.md`
- `context/design.md`
- `context/milestones/milestone-1.md`
- `context/sprints/sprint-1.md`
- `context/backlog/backlog-1.md`
- `context/dictations-tier-0/README-DICTATIONS-TIER-0.md`
- `context/implementation-plans/` (a `.gitkeep`-only folder in the current starter; there is no checked-in plan template)

If the supplied path does not look like `agentic_rails_context_starter`, stop and tell the user what was missing.

## Files To Inspect

Inspect these before editing:

1. Root `README.md`
2. `AGENTIC_RAILS_README.MD`
3. `AGENTS.md`
4. `context/dictations-tier-0/` README and existing intake files
5. `context/design.md` (including its Milestones Index)
6. `context/milestones/` milestone docs
7. `context/sprints/` sprint docs
8. `context/backlog/` story files
9. `context/implementation-plans/` for any existing plan folders
10. workflow docs such as `context/agenticworkflow.md`
11. wiki/secrets guidance and source/test/script README stubs when present

Use existing project-specific content if present. If the repository is not actually fresh, merge carefully and report the pre-existing content instead of pretending initialization started from a blank template.

## Files In Scope

Default editable files:

- `README.md`
- `AGENTIC_RAILS_README.MD` front matter and project-specific references
- `AGENTS.md` project-specific metadata and loading guidance
- `context/dictations-tier-0/<intake-file>.md`
- `context/design.md` (Tier 1, including the Milestones Index)
- `context/milestones/milestone-N.md` (Tier 2)
- `context/backlog/backlog-N.md` (Tier 4 stories)
- support docs with starter residue, including wiki/secrets guidance and source/test/script README stubs
- optional `context/sprints/sprint-N.md` (Tier 3) and new folders under `context/implementation-plans/` (Tier 5), only when justified

## Scale Strategy

If initialization touches more than 3-4 maintained files, do not try to keep every file's draft content in one agent context.

Prefer this order:

1. Keep one boss-level initialization plan with layout, identity map, file batches, and verification checks.
2. Use available subagents or IDE task delegation for isolated file batches when the environment supports it.
3. If subagents are unavailable, process files in small batches and re-read the plan, identity map, and relevant source before each batch.
4. Verify each batch before moving to the next one.

The goal is focused context, not ceremony. Do not create extra process artifacts unless they help the current repository.

## Files Not To Rewrite By Default

Do not rewrite these unless the user explicitly requests it or the change is a narrow project-specific addition:

- `context/laws.md`
- `context/agenticworkflow.md`
- `context/agent-thinking.md`
- `context/wiki/**`
- the starter templates: `context/dictations-tier-0/DICTATIONS_TIER_0_NOTE_TEMPLATE.md`, `context/milestones/MILESTONE_TEMPLATE.md`, `context/sprints/SPRINT_TEMPLATE.md`, `context/backlog/BACKLOG_TEMPLATE.md`
- the tier README files (`README-DICTATIONS-TIER-0.md`, `README-MILESTONES.md`, `README-SPRINTS.md`, `README-BACKLOG.md`)
- completed or historical implementation-plan folders under `context/implementation-plans/`

## Placeholder Detection

Treat content as replaceable starter scaffolding when it contains phrases such as:

- `Project Name`
- `Your Name`
- `your-repo`
- `Milestone 1: *Name*`
- `Sprint 1: *Name*`
- `Story name` / `Story: *Name*`
- `Service or dependency`
- `Principle 1`
- `Replace this section`
- `Replace the placeholders`
- `Replace placeholders with`
- `starter scaffolding`
- `placeholder stories`

Do not delete a section merely because it still has template wording. First decide whether the section remains useful as structure, then replace only the placeholder text with project-specific synthesis.

Also detect legacy or prototype identity residue when Tier 0 is transforming an existing project into a new one. Examples include old project names, old product names, old company names, old stack names, and obsolete architecture labels supplied by the Tier 0 document.

## Verification Search Boundaries

Use targeted scans. Do not rely on broad searches for words such as `template`, `placeholder`, or `starter` across the whole repository.

Exclude or classify expected false positives:

- raw Tier 0 intake
- reusable starter templates and tier README files
- examples and cheat sheets
- Doxygen or language-specific template terminology
- code concepts that legitimately use words such as placeholder
- historical notes or completed implementation records

The verification question is not "does this word exist anywhere?" The question is "does starter identity residue remain in maintained project truth?"

For identity transformations, also ask: "does old project identity or migration-language residue remain in maintained project truth?"

## Git And Filesystem State

If the target has a `.git/` directory, run a Git status check when available and report changed files. If Git is not available or the target is not a Git repository, switch to filesystem/content verification.

If a Git operation fails because of `.git/index.lock` or permission friction, report the blocker. Do not remove lock files or force cleanup unless the user approves.
