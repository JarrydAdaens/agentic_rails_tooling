---
name: agentic-rails-tooling-readme
metadata:
  version: "2.2"
  owner: Jarryd Adaens
---

# Agentic Rails Tooling

`agentic_rails_tooling` is the **right rail** of the Agentic Rails framework — a reusable capability library for agentic development.

It keeps the durable pieces of AI-assisted engineering in one version-controlled place: rules, skills, workflow-skills, specialist persona bundles, and the prompt source material used to create or improve them. The point is not loyalty to Anthropic, OpenAI, Google, Cursor, Windsurf, or any other specific IDE or model provider. The point is portable agent capability that can be installed, copied, adapted, and reused wherever the current best tool expects it.

This repository sits alongside the other core framework repositories:

| Role | Repository | Owns |
| --- | --- | --- |
| Left rail | `agentic_rails_context_starter` | Project-local context, plans, implementation logs, and handovers |
| Right rail | `agentic_rails_tooling` (this repo) | Reusable rules, skills, workflow-skills, and personas — plus the logic that operates on memory |
| Records office | `agentic-rails-memory` | The durable, markdown-only store of cross-project learnings and Resumes — beside the line, not a rail |

Read [`AGENTIC_RAILS_README.MD`](AGENTIC_RAILS_README.MD) for the full framework philosophy (the context tier system, the rails and the records office, provenance, and handover). This README is scoped to how *this* repository is laid out and used.

## Core Idea

Agentic IDEs are useful, but their conventions are fragmented. Some understand rules. Some understand skills. Some understand named agents. Some expect private dotfolders. Some are starting to recognize central user-level locations such as `%USERPROFILE%\.agents` for shared rules, skills, and agents.

This repository exists to keep that complexity under control without letting any one IDE define the architecture. The authored artifacts live in [`source/`](source/); everything else either documents, scaffolds, preserves, or accommodates them.

## Top-Level Layout

```text
agentic_rails_tooling/
  source/        Deployable artifacts — the stars of the repo
    rules/       Concise engineering standards and style guidance
    skills/      Portable task capabilities, including *-workflow orchestrations
    agents/      Named specialist persona bundles
  context/       Everything about this repo (not deployed)
    design.md    Purpose and design of this repository
    templates/   Blank scaffolds for new artifacts
    prompt-dev/  Prompt source material behind generated artifacts
    wiki/        Agent Skills spec notes and local alignment decisions
  archived/      Preserved-but-inactive artifacts (not deployed)
  ide_specific/  Nonportable vendor files (a deliberate junk pile)
```

Only `source/` is synced outward into IDEs. `context/`, `archived/`, and `ide_specific/` stay here.

## Grounded In Agent Skills

Much of this repository's skills model is based on the open [Agent Skills specification](https://agentskills.io/specification) and [Agent Skills overview](https://agentskills.io/home).

AgentSkills.io describes Agent Skills as a standardized way to give AI agents new capabilities and expertise. A skill is a folder containing a required `SKILL.md` file with metadata and instructions. Skills may also include optional `scripts/`, `references/`, and `assets/` folders.

```text
my-skill/
|-- SKILL.md
|-- scripts/
|-- references/
|-- assets/
`-- ...
```

That standard matters because it matches the way agentic work scales:

- Skills are portable folders, not hidden IDE state.
- `name` and `description` let agents discover relevant skills cheaply.
- Full instructions load only when a task calls for them.
- Scripts, references, templates, and assets can be bundled with the skill and loaded on demand.
- A useful skill can be reused across any skills-compatible agent client.

AgentSkills.io also documents progressive disclosure: discovery, activation, then execution. This repository leans into that model. Agents should see enough metadata to know what exists, then load the larger instructions, scripts, and references only when the task actually needs them.

For deeper local notes, see [`context/wiki/home.md`](context/wiki/home.md). The wiki summarizes AgentSkills.io guidance and records this repository's local alignment decisions.

## `source/` — The Deployable Artifacts

Everything under `source/` is authored to be installed into an IDE or the shared `%USERPROFILE%\.agents` workspace. It is the only part of the repository Kung Fu syncs outward.

### `source/rules/`

`source/rules/` contains concise standards with unambiguous file triggers. Claude Code loads global rules (`global-rules.md`, `unit-testing-rules.md`) unconditionally and path-scoped rules when their globs match. WPF, Qt, and Unreal guidance lives in the on-demand `rails-stack-guidance` skill because XAML and C++ extensions do not identify those frameworks reliably.

Use `source/rules/` for:

- General engineering behavior
- Language and framework standards
- Formatting and naming conventions
- Language guidance with reliable file triggers, such as C#, TypeScript, and React

Support for other IDEs (Cursor, Windsurf, Copilot, etc.) is produced at copy time by Kung Fu's conversion scripts from this Claude-Code-first source, not by hand-maintained per-IDE files in this repo.

Rules should stay short and prescriptive. If a file becomes a large body of procedural expertise, it probably belongs in `source/skills/` or `source/agents/`.

### `source/skills/`

`source/skills/` is the main reusable capability layer.

A normal skill is a portable task-shaped unit of expertise. It helps an agent do one class of work reliably without becoming a whole persona.

Current examples include:

- `source/skills/rails-planning`
- `source/skills/rails-pair-programming`
- `source/skills/rails-grade-cer`

Use `source/skills/` for repeatable workflows, tool guidance, templates, validation loops, and focused process knowledge.

### `source/skills/*-workflow`

Advanced workflows also live in `source/skills/`, but they are suffixed with `-workflow`.

The idea behind a workflow is right: some agentic procedures are large enough to run for a long time, coordinate subagents, persist intermediate artifacts, and produce reusable work. The problem is that agentic IDEs generally do not understand a separate `workflows/` primitive, so a dedicated top-level folder was retired. The practical convention is:

```text
<name>-workflow
```

That keeps powerful workflows easy to find through autocomplete in ordinary skill pickers while still making their orchestration role obvious.

Current examples include:

- `source/skills/rails-boss-execute-workflow`
- `source/skills/rails-plan-spam-workflow`

Workflow-skills should coordinate. They can define queues, subagent roles, artifact paths, handover rules, and validation gates. Reusable domain behavior should still live in ordinary skills when possible.

### `source/agents/`

`source/agents/` contains named specialist persona bundles.

An agent persona is different from a skill. A skill says, "Here is how to do this task." A persona says, "Here is the kind of worker you are, how you think, what quality bar you uphold, and which references you consult."

Agent folder names and frontmatter names must use the suffix `-persona`. That naming convention keeps progressive-disclosure persona information visually distinct from task skills and workflow-skills.

Current examples include:

- `source/agents/quality-gate-persona`
- `source/agents/unreal-persona`
- `source/agents/web-persona`
- `source/agents/wpf-persona`
- `source/agents/xna-persona`

Each persona bundle typically includes:

- `AGENT.md` for the role definition and operating contract
- A `<persona>.toml` adapter for vendors that expect one, plus provider-facing metadata under an `agents/` subfolder
- `references/` for focused supporting knowledge

Use `source/agents/` for durable specialist personas, not small reusable procedures.

## `context/` — Everything About This Repo

`context/` holds the material that explains, scaffolds, and supports the artifacts in `source/`. None of it is deployed.

### `context/design.md`

[`context/design.md`](context/design.md) records the purpose, structure, and design decisions behind this repository. Read it first when you need to understand *why* the layout is shaped the way it is before changing it.

### `context/templates/`

`context/templates/` contains blank or minimal starting points for creating new agentic artifacts.

Use it for examples and scaffolds for new skills, persona bundles, and rules. Templates are source material for authors, not production capability.

The template area mirrors the main capability categories:

- `context/templates/agents/`
- `context/templates/rules/`
- `context/templates/skills/`

Current examples include:

- `context/templates/skills/skill-template`
- `context/templates/skills/skill-template-advanced`

When creating a new artifact, start from the closest template, copy it into the active `source/` folder, then rename and fill it in. Do not expose templates directly to agentic IDEs.

### `context/prompt-dev/skills-prompts/`

Prompts can be as valuable as source code.

`context/prompt-dev/skills-prompts/` preserves prompt records and source material used to create, revise, or reason about skills and agents. If a generated skill is the artifact, these prompt records are often the design history behind it.

Keeping prompt source material separate makes it easier to refine the artifacts later without losing the original thinking.

### `context/wiki/`

`context/wiki/` contains local documentation about Agent Skills and this repository's conventions.

It is not a replacement for AgentSkills.io. It is a local, reviewable companion that captures the parts of the standard this repository relies on most often:

- Overview
- Specification notes
- Best practices
- Description optimization
- Skill evaluation
- Script usage
- Repository alignment notes

## `archived/`

`archived/` contains agentic artifacts that are preserved but no longer treated as active reusable capability.

Use it for skills, rules, agents, and related material that may still have reference value but is of dubious current usefulness, superseded by another artifact, or not worth exposing through normal IDE consumption paths.

The archive mirrors the main capability categories:

- `archived/agents/`
- `archived/skills/`
- `archived/rules/`

Archived artifacts should not be copied into agentic IDE configuration by default. They can be restored or mined later, but `source/` remains the set that tools and humans should normally consume.

## `ide_specific/`

`ide_specific/` is intentionally a junk pile for vendor-specific files and conventions that do not belong in the standard layers.

It exists because real tools are messy. Some IDEs need one-off folders, rule files, metadata, or naming conventions that are not portable. Those files can live here as a means to an end, but they should not define the repository's architecture.

## Naming Conventions

- File and folder names use **kebab-case** (`commit-log-template.md`, `wpf-rules.md`), not `snake_case` or `PascalCase`, except where a tool mandates a fixed name.
- Conventional, tool-recognized names are preserved as-is: `SKILL.md`, `AGENT.md`, `README.md`, `SECURITY.md`, `AGENTS.md`, `CLAUDE.md`, `AGENTIC_RAILS_README.MD`, `.cursorrules`, and `.gitkeep`.
- Code files keep their language idioms (Python and JavaScript use the conventions their ecosystems expect).
- Persona folders and `name` fields end in `-persona`; orchestration skills end in `-workflow`.

## Rails vs. Personal Skill Classification

This repository currently mixes framework skills with loose personal/experimental skills. The six-tier addendum (§11) sets the ownership test: a skill is part of Agentic Rails when other Rails skills directly consume it, Rails workflows call it, Rails documentation requires it, it reads or writes Rails context artifacts, or it implements core Rails behavior such as planning, CER, milestone creation, orchestration, handover, or memory capture. Everything else is personal — useful, but not a Rails framework component.

This is the classification decision only. The physical move to a separate personal-skills repository is deferred: it needs Kung Fu to support multiple skill source roots first (six-tier addendum §12), which is out of scope here. Until then, personal skills stay in this repo's `source/skills/` and `source/agents/`, just flagged below.

### Rails framework skills

| Skill | Why it's Rails |
| --- | --- |
| `rails-planning` | Produces the primary Implementation Plan artifact (`plan.md`) |
| `rails-milestone-planning` | Produces Milestone documents from the backlog |
| `rails-grade-cer` | Scores Complexity/Effort/Risk, the routing input for planning |
| `rails-planning-phaser` | Fractures an over-large plan into Phases using CER |
| `rails-initialize-from-tier0` | Bootstraps a project's context tier structure from Dictation |
| `rails-update-from-starter` | Reconciles a derived project's context tiers against the starter |
| `rails-plan-spam-workflow` | Orchestrates bulk plan creation across milestone stories |
| `rails-boss-execute-workflow` | Orchestrates execution against implementation plans |
| `rails-clean-frontmatter` | Normalizes/repairs frontmatter across Rails artifacts |
| `rails-memory-learnings` | Writes session learnings into the memory records office |
| `rails-pair-programming` | Explicitly reads Story/plan context from the context tier system |
| `rails-project-appraisal` | Reads design/milestone/backlog/plan context tiers and writes its verdict as a durable `context/reports/` artifact |

`complaining`, `evidence`, and `thinking-out-loud` were early experiments in generating the provenance artifacts (`## Complaints / Friction`, `## Evidence / References`, `thinking.md`) that `rails-planning` now produces directly as part of its own opt-in sidecars; their salvageable content (the complaint entry format, the `thinking.md` good/bad-entry guidance) was folded into `rails-planning`'s `references/plan-template.md` and the three skills were archived. `handover` (Reads `plan.md`, implementation log, and other Rails provenance artifacts to produce a handover) was archived as unused; no actively deployed skill currently produces `handover/` artifacts. All four are preserved under `archived/skills/` for reference.

### Personal / loose skills (extracted July 2026)

This repo previously also carried personal, non-Rails skills: `commit-log`, `grade`, `grugg`, `grugg-compress`, the `oracle-*` token-tooling family, `wpf-starter-update`, and `wpf-tree-sensor`. None of them assume the Agentic Rails context tier system, so in July 2026 they were extracted to the separate `jarryds-agent-marketplace` repository. The rule going forward: every skill here must be specific to Agentic Rails — it may assume the target project follows the `agentic_rails_context_starter` layout. Generic, works-anywhere skills belong in `jarryds-agent-marketplace`.

Some Rails skills reference the extracted skills by their installed name (`rails-boss-execute-workflow` requires workers to load `commit-log`; `rails-project-appraisal` contrasts itself with `grade`). Those references are to the globally installed skills, not to paths in this repo — they keep working as long as the marketplace skills are installed.

`source/agents/` (`quality-gate-persona`, `unreal-persona`, `web-persona`, `wpf-persona`, `xna-persona`) are all personal: generic domain-specialist personas usable in any repository, not specific to the Rails context tier system. `quality-gate-persona` references a generic "task plan" and "evidence," which overlaps with Rails vocabulary by coincidence rather than by dependency — it doesn't require the context tier system to function.

## Relationship To The Other Rails

The framework splits responsibilities across three repositories so no rail absorbs another's job:

| Repository | Owns |
| --- | --- |
| `agentic_rails_context_starter` | Project-local context: Dictation intake, design, milestones, stories, implementation plans, and handovers. |
| `agentic_rails_tooling` (this repo) | Reusable agent capabilities: shared rules, Agent Skills, workflow-skills, persona bundles, prompt-development source material, and the logic that captures, curates, and rebuilds memory artifacts. |
| `agentic-rails-memory` | Durable, markdown-only cross-project artifacts: learnings and model/agent Resumes. Artifacts only — never the logic that produces or consumes them. |

In practice, the context starter gives a project its documentation-first operating model and is intentionally empty of application code. This repository gives agents the reusable tools to execute inside that model. The memory repository accumulates the track record that lets the framework route the next task from real, measured data rather than gut feel — and the routing logic that reads and writes it lives here, in the right rail.

For example:

- A new project starts from `agentic_rails_context_starter`.
- The project's `AGENTS.md` and context files define how agents load local context.
- Shared rules from this repository are copied or installed into the IDE's expected rule location.
- Skills such as `rails-planning` or `rails-boss-execute-workflow` are installed globally or made available through `%USERPROFILE%\.agents`.
- Specialist personas such as `source/agents/wpf-persona` are used when the project calls for that domain expertise.

The project remains usable without this repository, but it becomes much stronger when these reusable assets are available.

## Relationship To `kung-fu`

`kung-fu` is the local WPF deployment app for consuming the artifacts in this repository across agentic IDEs.

This repository is the source of truth. Kung Fu reads the `source/` tree, then copies its skills, rules, and agents outward into the folder layouts expected by different IDEs, profiles, staging folders, or the shared `%USERPROFILE%/.agents` workspace.

The relationship is deliberately one-way:

```text
source/ -> Kung Fu sync -> IDE and workspace configuration folders
```

Kung Fu manages deployment, not authorship. Edits should happen in this repository, while Kung Fu makes the active artifacts available wherever the current agentic tool expects them. `context/`, `archived/`, and `ide_specific/` are not part of the normal sync set.

## Working Model

When adding or updating reusable context, place it in the narrowest layer that matches its job:

- Put it in `source/rules/` if it is short, prescriptive, and style-oriented.
- Put it in `source/skills/` if it is reusable expertise, workflow knowledge, or a portable task module.
- Put it in `source/skills/<name>-workflow/` if it coordinates a larger multi-step process, subagents, queues, or durable artifacts.
- Put it in `source/agents/` if it defines a named specialist persona with a mission, operating model, and reference library.
- Put it in `archived/` if it is preserved for reference but should not be part of the active agentic capability set.
- Put it in `context/templates/` if it is a blank, skeletal, or example starter point for creating a future artifact.
- Put it in `context/prompt-dev/skills-prompts/` if it is prompt source material used to generate or evolve an artifact.
- Put it in `context/wiki/` if it documents the standards and local conventions behind the repository.
- Put it in `ide_specific/` only when a tool requires a nonstandard compatibility file.

## Layer Examples

- WPF, Qt, and Unreal guidance is selected explicitly through `source/skills/rails-stack-guidance/`; broad XAML or C++ globs do not activate it.
- A Rails-specific planning process belongs in `source/skills/rails-planning`.
- A generic, non-Rails skill (commit wording, artifact grading, token tooling) belongs in the separate `jarryds-agent-marketplace` repository, not here.
- A questionable or superseded skill belongs in `archived/skills/`.
- A blank starter for a future persona bundle belongs in `context/templates/agents/`.
- A production-grade WPF specialist persona belongs in `source/agents/wpf-persona`.
- The prompt material used to generate a skill belongs in `context/prompt-dev/skills-prompts/`.

## Maintenance Notes

- Prefer open standards and portable formats.
- Keep the AgentSkills.io specification close at hand when changing skills.
- Keep rules concise.
- Keep normal skills task-shaped and reusable.
- Suffix advanced orchestrations with `-workflow`.
- Keep workflow-skills focused on orchestration rather than swallowing every detail.
- Keep agent personas explicit about mission, scope, collaboration boundaries, references, and quality bar.
- Keep prompt records when they are the real source behind generated artifacts.
- Keep IDE-specific files isolated from the core architecture.
- Keep archived artifacts out of normal sync/deployment paths unless deliberately restored.
- Keep templates out of normal sync/deployment paths; copy from them into active `source/` folders before use.

## Repository

- Repository: https://github.com/JarrydSemmens/agentic_rails_tooling
- Owner: Jarryd Adaens
- Last Updated: 2026-07-03
