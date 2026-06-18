# Tier 0 Synthesis Policy

Use this reference when converting a raw Tier 0 document into maintained Agentic Rails project context.

## Core Rule

Preserve the raw Tier 0 source first. Then synthesize durable decisions into maintained context files.

Tier 0 is evidence and source material. After synthesis, the working project truth should live in:

- Tier 1: detected `design.md`
- Tier 2: detected `milestones.md`
- Tier 3: detected `goals*.md`
- Tier 4: detected implementation-plan folder only when work is ready to execute or when a context-synthesis plan records the initialization itself

Before editing maintained docs, write a short initialization plan unless the user explicitly asked for immediate implementation. The plan should name the layout, target files, source intake set, scope boundaries, assumptions, checkpoint strategy, and verification checks.

## Intake File Requirements

Create or update a Tier 0 file with:

- date and short topic
- source type, such as dictated notes, AI chat, AI-generated deep research report, kickoff document, transcript, or pasted prompt
- raw notes, preserved as faithfully as practical
- important signals
- open questions
- integration notes listing the maintained files updated from this source

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
- milestone candidates
- goal candidates and acceptance signals
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
- Tier 0 README or index
- design, milestones, and goals
- wiki/secrets guidance
- source/test/script README stubs
- implementation-plan indexes or starter examples

Replace residue with project-aware text when the file is maintained truth. Keep reusable templates when they are intentionally reusable, but make surrounding metadata and links project-aware.

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

Keep a concise Agentic Rails context section linking to `context/`, `context/design.md`, `context/milestones.md`, and `AGENTIC_RAILS_README.MD`.

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

Update only project-specific metadata or context-loading guidance that is clearly stale after initialization. Keep rules that tell future agents to read design, milestones, goals, and relevant implementation plans.

## context/design.md

The detected design file is the main Tier 1 synthesis target.

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

## context/milestones.md

Use milestones for roadmap stages, not tiny tasks.

Populate:

- table of contents with one row per milestone
- stable milestone anchors
- milestone intent
- why it matters
- expected impact
- status, normally `Not Started`
- linked goals file for each milestone

Create one goals file per milestone by default:

```text
context/goals1.md
context/goals2.md
context/goals3.md
```

If the Tier 0 source only supports one milestone, keep one milestone and record expansion questions.

## context/goals*.md

Use goals for concrete deliverables with acceptance criteria.

For each milestone goals file, include:

- milestone context and problem
- summary table with goal links, names, plan status, status, and intent
- milestone scope
- out-of-scope items
- solution overview if known
- one section per goal with stable anchors such as `goal-1-1`
- source context linking to the Tier 0 intake file when useful
- deliverables
- acceptance criteria
- out of scope
- dependencies and agent guidelines when they materially help future execution

Set goal status to `Not Started` unless the Tier 0 source clearly says otherwise.

Set plan status to `No` unless a Tier 4 plan is created during initialization.

For broad roadmaps, create all needed milestone goal files. Expand the first one or two milestones more deeply so immediate work can begin. Keep later milestones concise but still executable: each goal still needs intent, deliverables, acceptance criteria, and out-of-scope notes where useful.

When the repository tracks setup work as goals, prefer making `Goal 1.1` an initialization/context goal such as `Initialize Project Context`. Mark it complete only after Tier 0 is preserved, maintained context is populated, residue checks are done, and the final report is produced. This makes initialization visible as completed project work rather than invisible setup.

## Tier 4 Plans

Do not create detailed feature implementation plans by default.

Consider creating one initialization or context-synthesis plan when it helps future agents understand what was populated. This plan should record setup scope, source links, files changed, verification checklist, and open questions. It should not become an implementation plan for every future product feature.

Create initial Tier 4 folders only when:

- the user asks for implementation plans
- the Tier 0 document identifies immediate ready-to-build goals with enough acceptance criteria
- the agent has enough repository context to make a plan executable

When creating plans, use the existing implementation-plan template shape and create task-specific folders such as:

```text
context/implementation-plans/GOAL_1_1_short-slug/
```

Use the older `Documentation/implementation_plans/` folder shape when the repository uses that layout.

Update the relevant goal's Tier 4 plan link after creating a plan.

## No Code Implementation During Context Setup

Keep initialization focused on context population unless the user explicitly asks for code work. Do not mix product implementation into the context setup pass.

## Open Questions

If the Tier 0 source leaves important gaps, record them in the most relevant maintained file:

- design-level uncertainty in `context/design.md`
- roadmap uncertainty in `context/milestones.md`
- delivery uncertainty in `context/goals*.md`
- task execution uncertainty in a Tier 4 `plan.md`

Prefer explicit questions over quiet assumptions.

## Conflict Handling

If Tier 0 contradicts existing project-specific context:

1. Preserve the raw contradiction in the Tier 0 intake file.
2. Do not silently overwrite maintained context.
3. Update maintained context only when the Tier 0 source clearly supersedes it.
4. Otherwise, add an open question or report a blocked item.
