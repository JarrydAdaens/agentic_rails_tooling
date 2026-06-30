---
name: rails-initialize-from-tier0-validation-and-scope
metadata:
  version: "1.0"
---

# Validation And Scope

Use this reference when starting `rails-initialize-from-tier0`, validating paths, or deciding which files are in scope.

## Required Inputs

The skill needs:

- Target project root: default to the current repository when the user does not specify a path.
- Tier 0 source: one or more file paths, pasted texts, or existing files under the detected Tier 0 folder.

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

Detect the target's actual Agentic Rails era before choosing paths.

Prefer the current layout when present:

```text
context/
context/tier0/
context/design.md
context/milestones.md
context/goals*.md
context/implementation-plans/
```

Support the older layout when that is what the repository uses:

```text
Documentation/
Documentation/tier0/
Documentation/design.md
Documentation/milestones.md
Documentation/goals*.md
Documentation/implementation_plans/
```

Set these working variables in the initialization plan:

- context root: `context/` or `Documentation/`
- Tier 0 folder: `<context-root>/tier0/`
- implementation-plan folder: `implementation-plans/` or `implementation_plans/`
- goals naming pattern: `goals*.md` under the detected context root

Do not rename an older repository to the new layout as part of initialization unless the user explicitly asks for a layout migration.

If front matter shows an old or missing `agentic_rails_source_version`, expect path and metadata drift. Validate actual files instead of assuming the current starter structure.

## Target Project Validation

Run from the derived child project unless the user provides a target project path.

Strong Agentic Rails target signals include:

- `AGENTIC_RAILS_README.MD`
- `AGENTS.md`
- `context/` or `Documentation/`
- a Tier 0 folder
- `design.md`
- `milestones.md`
- `goals*.md`
- an implementation-plan template folder

If the target lacks most of these signals, stop and ask whether this is the intended repository.

If the detected design, milestone, or goals files already contain real project-specific content, treat the task as enrichment or selective re-synthesis, not blank initialization. Ask before replacing maintained truth unless the user explicitly requested a full reinitialization.

Do not use this skill on:

- the central `agentic_rails_context_starter` repository itself
- the reusable `agentic_rails_tooling` repository
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
- `context/milestones.md`
- `context/goals1.md`
- `context/tier0/README.md`
- `context/implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/plan.md`

If the supplied path does not look like `agentic_rails_context_starter`, stop and tell the user what was missing.

## Files To Inspect

Inspect these before editing:

1. Root `README.md`
2. `AGENTIC_RAILS_README.MD`
3. `AGENTS.md`
4. detected Tier 0 README or index
5. existing Tier 0 intake files
6. detected `design.md`
7. detected `milestones.md`
8. existing `goals*.md`
9. implementation-plan template, index, or example folders
10. workflow docs such as `agenticworkflow.md`
11. wiki/secrets guidance and source/test/script README stubs when present

Use existing project-specific content if present. If the repository is not actually fresh, merge carefully and report the pre-existing content instead of pretending initialization started from a blank template.

## Files In Scope

Default editable files:

- `README.md`
- `AGENTIC_RAILS_README.MD` front matter and project-specific references
- `AGENTS.md` project-specific metadata and loading guidance
- detected Tier 0 intake file
- detected Tier 0 README or index
- detected design file
- detected milestones file
- detected goals files
- support docs with starter residue, including wiki/secrets guidance and source/test/script README stubs
- optional new folders under the detected implementation-plan folder

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
- `context/AgentThinking.md`
- `context/wiki/**`
- `context/implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/**`
- equivalent older-layout support files under `Documentation/`
- completed or historical implementation-plan folders

## Placeholder Detection

Treat content as replaceable starter scaffolding when it contains phrases such as:

- `Project Name`
- `Your Name`
- `your-repo`
- `Agentic Starter`
- `Replace this section`
- `Describe the project`
- `Milestone 1: Name`
- `Goal 1.1 - *Name*`
- `Service or dependency`
- `Principle 1`
- `description: ???`
- `placeholder sections`

Do not delete a section merely because it still has template wording. First decide whether the section remains useful as structure, then replace only the placeholder text with project-specific synthesis.

Also detect legacy or prototype identity residue when Tier 0 is transforming an existing project into a new one. Examples include old project names, old product names, old company names, old stack names, and obsolete architecture labels supplied by the Tier 0 document.

## Verification Search Boundaries

Use targeted scans. Do not rely on broad searches for words such as `template`, `placeholder`, or `starter` across the whole repository.

Exclude or classify expected false positives:

- raw Tier 0 intake
- reusable implementation-plan templates
- examples and cheat sheets
- Doxygen or language-specific template terminology
- code concepts that legitimately use words such as placeholder
- historical notes or completed implementation records

The verification question is not "does this word exist anywhere?" The question is "does starter identity residue remain in maintained project truth?"

For identity transformations, also ask: "does old project identity or migration-language residue remain in maintained project truth?"

## Git And Filesystem State

If the target has a `.git/` directory, run a Git status check when available and report changed files. If Git is not available or the target is not a Git repository, switch to filesystem/content verification.

If a Git operation fails because of `.git/index.lock` or permission friction, report the blocker. Do not remove lock files or force cleanup unless the user approves.
