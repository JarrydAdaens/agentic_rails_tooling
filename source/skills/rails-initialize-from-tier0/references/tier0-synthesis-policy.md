---
name: rails-initialize-from-tier0-synthesis-policy
metadata:
  version: "2.0"
---

# Tier 0 Synthesis Policy

Use this reference when converting a raw Tier 0 dictation into maintained Agentic Rails project context.

## Core Rule

Preserve the raw Tier 0 source first. Then synthesize durable decisions into the maintained seven-tier context files.

Tier 0 is evidence and source material. After synthesis, the working project truth should live in:

- Tier 1: `context/design.md`, including its **Milestones Index** subsection
- Tier 2: `context/milestones/milestone-N.md`, one file per milestone
- Tier 3: `context/sprints/sprint-N.md`, usually deferred until sprint planning close to execution
- Tier 4: `context/backlog/backlog-N.md`, the priority-sorted story pool
- Tier 5: `context/implementation-plans/STORY_*/` only when work is ready to execute or when a context-synthesis plan records the initialization itself

Initialization builds the upper, planning-time tiers (Design + Milestones + Backlog). Sprints and implementation plans are planned close to execution and are not forced during initialization.

Before editing maintained docs, write a short initialization plan unless the user explicitly asked for immediate implementation. The plan should name the layout, target files, source intake set, scope boundaries, assumptions, checkpoint strategy, and verification checks.

## Intake File Requirements

Create or update a Tier 0 file under `context/dictations-tier-0/` with:

- date and short topic
- source type, such as dictated notes, AI chat, AI-generated deep research report, kickoff document, transcript, or pasted prompt
- raw notes, preserved as faithfully as practical
- important signals
- open questions
- integration notes listing the maintained files updated from this source

Match the starter's intake shape (`DICTATIONS_TIER_0_NOTE_TEMPLATE.md`): `Source`, `Raw Notes`, `Important Signals`, and `Integration Notes` that name `../design.md` (and its Milestones Index), `../milestones/`, `../sprints/`, `../backlog/`, and `../implementation-plans/`.

Do not polish the raw notes into a spec. The point is to preserve provenance.

When the user provides both raw intent and research synthesis, keep them as separate Tier 0 files unless the user asks for a single combined intake. Use raw intent for priorities and taste; use research synthesis for architecture options, tradeoffs, stack decisions, and external constraints.

## Checkpoints

Create a recovery checkpoint after preserving Tier 0 and before broad maintained-doc synthesis.

Acceptable checkpoints include:

- a Git commit when the repository is Git-backed and the user has asked for or approved commits
- a recorded Git status plus clear report entry when committing is not requested
- a filesystem/content checkpoint in non-Git repositories, listing the preserved Tier 0 files and planned synthesis targets

Do not perform destructive cleanup or force Git operations to make a checkpoint.

## Extraction Pass

Before editing maintained docs, extract a working outline from the Tier 0 source:

- project name and short description
- intended users or operators
- primary problem being solved
- core product or system capabilities
- proposed architecture and major components
- important data flows or workflows
- platform, language, framework, infrastructure, and dependency signals
- non-functional requirements such as privacy, security, reliability, performance, accessibility, explainability, or observability
- explicit non-goals and deferred ideas
- milestone candidates (macro-features or major delivery phases)
- story candidates and acceptance signals (discrete units of work)
- risks, ambiguities, contradictions, and unresolved decisions

When the Tier 0 source is unclear, prefer an `Open Questions` or `Assumptions` section over confident invention.

## Identity Map

For every initialization, define a small canonical identity map before rewriting maintained docs:

- canonical project name
- repository name
- short description
- owner or team, if known
- old names or prototype names to remove
- old product, company, stack, or architecture terms to remove
- new replacement terms where they are unambiguous
- terms that must remain only in raw Tier 0, historical logs, or provenance

When Tier 0 describes a transfiguration, fork, prototype conversion, or project rename, treat the identity map as critical. Maintained docs should describe the new project directly, not as "the thing that used to be X."

Avoid transitional language in maintained truth unless the section is explicitly about provenance. Common terms to purge from final project-facing docs include:

- `inherited`
- `legacy`
- `reference context`
- `reference architecture`
- `transfigured`
- `transfiguration`
- `old project`
- `prototype conversion`

Do not blindly delete these terms from raw Tier 0, historical implementation logs, or an explicit migration note where provenance matters.

## Bulk Identity Cleanup

For many repetitive terminology replacements, use a reviewed bulk-edit approach instead of hand-editing hundreds of occurrences.

Safe pattern:

1. Build a small replacement dictionary from the identity map.
2. Restrict the file set to maintained project truth and intentionally selected support docs.
3. Exclude raw Tier 0, historical logs, reusable templates, generated files, binaries, and external dependencies.
4. Run a dry scan first and review the proposed matches.
5. Apply replacements with a short script or equivalent structured tool when the matches are straightforward.
6. Re-scan targeted files and manually inspect risky replacements.

Do not use broad replacement scripts when terms are ambiguous or domain-specific. In those cases, edit section-aware.

## Starter Residue Sweep

After the main synthesis pass, inspect project-facing maintained files for starter residue:

- root `README.md`
- `AGENTS.md`
- front matter in maintained context files
- the Tier 0 README or index
- `context/design.md` and its Milestones Index
- `context/milestones/` milestone docs
- `context/backlog/` story files
- wiki/secrets guidance
- source/test/script README stubs

Replace residue with project-aware text when the file is maintained truth. Keep reusable templates and tier README files when they are intentionally reusable, but make surrounding metadata and links project-aware.

When legacy identity residue is present, run the same sweep for old project names, old stack names, and transitional language from the identity map.

## Front Matter

Preserve existing YAML front matter shape where present.

For project-specific files, update obvious starter placeholders:

```yaml
owner: "<actual owner or unknown>"
repo: "<actual repository name>"
description: "<short project-specific description>"
```

Do not change `agentic_rails_source_version` during initialization unless the file still represents the same starter source version. If unsure, leave it unchanged and report the uncertainty.

## README.md

Root `README.md` should become project-facing.

Populate:

- project name
- short description
- overview
- current status
- getting started notes, if known
- project context links
- repository layout only where it helps

Keep a concise Agentic Rails context section linking to `context/`, `context/design.md`, `context/milestones/`, `context/backlog/`, and `AGENTIC_RAILS_README.MD`.

Do not turn the project README into a generic Agentic Rails explainer.

## AGENTIC_RAILS_README.MD

Keep the framework explanation intact.

Limit edits to:

- front matter owner, repo, and description
- small project-specific notes if the file already expects them
- links that must match the repository's actual structure

Do not replace the Agentic Rails overview with product requirements.

## AGENTS.md

Preserve the agent operating rules.

Update only project-specific metadata or context-loading guidance that is clearly stale after initialization. Keep rules that tell future agents to read laws, design, milestones, sprints, the relevant backlog story, and any relevant implementation plans.

## context/design.md

The design file is the main Tier 1 synthesis target.

Populate it with:

- executive summary
- purpose, audience, and problem statement
- core principles that actually constrain decisions
- architecture and component boundaries
- repository structure as known
- important workflows, pipelines, or user journeys
- configuration and secret-management direction, even if provisional
- security and privacy expectations
- observability and debugging expectations
- testing policy
- performance expectations or an explicit note that performance is not yet defined
- assumptions and open questions when the Tier 0 source is incomplete

Keep useful starter structure, but remove obvious placeholder examples after replacing them with real project content.

### Milestones Index (inside design.md)

The **Milestones Index** is a subsection of `design.md`, not a separate file. It is the table of contents that links down to each milestone document under `milestones/`.

Populate the index table with one row per milestone:

| Milestone | Document | Status | Why it matters | What it unlocks |
| --- | --- | --- | --- | --- |

Keep the index in sync with the files in `context/milestones/`. When a backlog story later scores as epic-sized, promote it into this index as a new milestone.

## context/milestones/

Use milestones for roadmap stages (macro-features or major delivery phases), not tiny tasks. There is one file per milestone (`milestone-1.md`, `milestone-2.md`, ...), each indexing the sprints that will deliver it.

For each milestone document, populate:

- intent (one sentence describing the macro-feature or phase)
- why it matters
- impact (what completing it unlocks)
- status, normally `Not Started`
- a Sprint Index table (sprints are usually added later, during sprint planning)
- backlog source notes (which backlog themes feed this milestone, and known interdependencies)

Create one milestone document per milestone you synthesize, and add a matching row to the Milestones Index in `design.md`.

If the Tier 0 source only supports one milestone, keep one milestone document and record expansion questions.

For broad roadmaps, create all needed milestone documents. Expand the first one or two milestones more deeply so immediate work can begin. Keep later milestones concise but still meaningful: each still needs intent, why-it-matters, and impact.

## context/backlog/

The backlog is the Tier 4 story pool: discrete work units (features, bugs, refactors), built once from Design + Milestones and priority-sorted front-to-back. It replaces the retired per-milestone goals files.

Backlog rules:

- **One global, priority-sorted pool**, not one file per milestone. Most urgent, concrete, doable stories go in the front file; wishful, experimental, least-concrete stories sink to the back.
- **30-story cap per file.** Overflow spawns the next file (`backlog-1.md`, `backlog-2.md`, ...).
- Match the starter's story shape: a Story Index table (`# | Story | Type | Priority | Complexity | Effort | Risk | Sprint | Status`) followed by one section per story with a stable `<a id="story-N">` anchor.

For each story, include:

- type (Feature, Bug, or Refactor)
- summary of the discrete unit of work
- why / value and rough urgency
- rough scope (what it touches)
- scores left as `—` (filled during sprint planning, by right-rail tooling)
- a reclassification check: if scoring later reveals it is epic-sized, promote it to a Milestone

Set story status to `Backlog` unless the Tier 0 source clearly says otherwise. Leave the `Sprint` column as `*unscheduled*` — scheduling stories into sprints is a later sprint-planning step, not part of initialization.

When the repository tracks setup work as stories, prefer making the first backlog story an initialization/context story such as `Initialize Project Context`. Mark it complete only after Tier 0 is preserved, maintained context is populated, residue checks are done, and the final report is produced. This makes initialization visible as completed project work rather than invisible setup.

## context/sprints/ (usually deferred)

Sprint planning is where the hard thinking happens (scoring, mitigation, phase fragmentation) and it runs close to execution. Do not force a full sprint plan during Tier 0 initialization.

Seed a Tier 3 sprint only when:

- the user explicitly asks to plan the first sprint, or
- the first milestone is clearly ready and the user wants immediate work queued

When seeding a sprint, copy `SPRINT_TEMPLATE.md`, link it to its milestone, and schedule a small set of front-backlog stories into it. Otherwise leave `sprints/` as starter scaffolding and record that sprint planning is the next step.

## Tier 5 Plans

Do not create detailed feature implementation plans by default.

Consider creating one initialization or context-synthesis plan when it helps future agents understand what was populated. This plan should record setup scope, source links, files changed, verification checklist, and open questions. It should not become an implementation plan for every future product feature.

Create initial Tier 5 folders only when:

- the user asks for implementation plans
- the Tier 0 document identifies an immediate ready-to-build story with enough acceptance criteria
- the agent has enough repository context to make a plan executable

When creating plans, create a story-specific folder under `context/implementation-plans/` named for the story:

```text
context/implementation-plans/STORY_<sprint>_<story>_short-slug/
```

For setup work not yet scheduled into a sprint, a descriptive slug such as `STORY_0_init_initialize-project-context/` is acceptable. Each executed plan folder ends up holding `plan.md`, `implementation-log.md`, and `completion-review.md`. Update the relevant story's plan link after creating a plan.

## No Code Implementation During Context Setup

Keep initialization focused on context population unless the user explicitly asks for code work. Do not mix product implementation into the context setup pass.

## Open Questions

If the Tier 0 source leaves important gaps, record them in the most relevant maintained file:

- design-level uncertainty in `context/design.md`
- roadmap uncertainty in the Milestones Index or a `context/milestones/` doc
- delivery uncertainty in a `context/backlog/` story
- task execution uncertainty in a Tier 5 `plan.md`

Prefer explicit questions over quiet assumptions.

## Conflict Handling

If Tier 0 contradicts existing project-specific context:

1. Preserve the raw contradiction in the Tier 0 intake file.
2. Do not silently overwrite maintained context.
3. Update maintained context only when the Tier 0 source clearly supersedes it.
4. Otherwise, add an open question or report a blocked item.
