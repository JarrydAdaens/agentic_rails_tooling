---
metadata:
  version: "1.0"
---

# Agentic Rails Tooling

`agentic_rails_tooling` is the right rail of the Agentic Rails framework — a reusable capability library for agentic development.

It keeps the durable pieces of AI-assisted engineering in one version-controlled place: rules, skills, specialist persona bundles, workflow-skills, and the prompt source material used to create or improve them. The point is not loyalty to Anthropic, OpenAI, Google, Cursor, Windsurf, or any other specific IDE or model provider. The point is portable agent capability that can be installed, copied, adapted, and reused wherever the current best tool expects it.

This repository is especially useful beside project templates such as [`agentic_rails_context_starter`](../agentic_rails_context_starter/), where the project owns its local context and this repository supplies reusable operating knowledge.

## Core Idea

Agentic IDEs are useful, but their conventions are fragmented. Some understand rules. Some understand skills. Some understand named agents. Some expect private dotfolders. Some are starting to recognize central user-level locations such as `%USERPROFILE%\.agents` for shared rules, skills, and agents.

This repository exists to keep that complexity under control without letting any one IDE define the architecture.

The stars of the repository are:

- `rules/`
- `skills/`
- `agents/`

Everything else exists to support those folders, preserve source material, document standards, or handle unavoidable compatibility problems.

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

For deeper local notes, see [`wiki/home.md`](wiki/home.md). The wiki summarizes AgentSkills.io guidance and records this repository's local alignment decisions.

## Repository Structure

### `rules/`

`rules/` contains concise engineering standards and style guidance.

Start at [`rules/index.md`](rules/index.md). It is the entry point for selecting the smallest relevant rule set for a repository and task.

Use `rules/` for:

- General engineering behavior
- Language and framework standards
- Formatting and naming conventions
- Stack-specific guidance such as C#, C++, WPF, and Qt
- Compatibility files such as [`rules/.cursorrules`](rules/.cursorrules)

Rules should stay short and prescriptive. If a file becomes a large body of procedural expertise, it probably belongs in `skills/` or `agents/`.

### `skills/`

`skills/` is the main reusable capability layer.

A normal skill is a portable task-shaped unit of expertise. It helps an agent do one class of work reliably without becoming a whole persona.

Current examples include:

- `skills/commit-log`
- `skills/grade`
- `skills/rails-planning`
- `skills/rails-pair-programming`
- `skills/complaining`
- `skills/evidence`
- `skills/handover`
- `skills/thinking-out-loud`

Use `skills/` for repeatable workflows, tool guidance, templates, validation loops, and focused process knowledge.

### `skills/*-workflow`

Advanced workflows also live in `skills/`, but they are suffixed with `-workflow`.

The old [`workflows/`](workflows/) folder was an exploratory failure. The idea was right: some agentic procedures are large enough to run for hours, coordinate subagents, persist intermediate artifacts, and produce reusable work. The problem is that agentic IDEs generally do not understand a separate `workflows/` primitive.

The practical convention is:

```text
<name>-workflow
```

That keeps powerful workflows easy to find through autocomplete in ordinary skill pickers while still making their orchestration role obvious.

Current examples include:

- `skills/rails-boss-execute-workflow`
- `skills/rails-plan-spam-workflow`

Workflow-skills should coordinate. They can define queues, subagent roles, artifact paths, handover rules, and validation gates. Reusable domain behavior should still live in ordinary skills when possible.

### `agents/`

`agents/` contains named specialist persona bundles.

An agent persona is different from a skill. A skill says, "Here is how to do this task." A persona says, "Here is the kind of worker you are, how you think, what quality bar you uphold, and which references you consult."

Agent folder names and frontmatter names must use the suffix `-persona`. That naming convention keeps progressive-disclosure persona information visually distinct from task skills and workflow-skills.

Current examples include:

- `agents/quality-gate-persona`
- `agents/unreal-persona`
- `agents/web-persona`
- `agents/wpf-persona`
- `agents/xna-persona`

Each persona bundle typically includes:

- `AGENT.md` for the role definition and operating contract
- Provider-facing metadata under an `agents/` subfolder
- `references/` for focused supporting knowledge

Use `agents/` for durable specialist personas, not small reusable procedures.

### `archived/`

`archived/` contains agentic artifacts that are preserved but no longer treated as active reusable capability.

Use it for skills, rules, agents, workflows, and related material that may still have reference value but is of dubious current usefulness, superseded by another artifact, or not worth exposing through normal IDE consumption paths.

The archive mirrors the main capability categories:

- `archived/agents/`
- `archived/skills/`
- `archived/rules/`
- `archived/workflows/`

Archived artifacts should not be copied into agentic IDE configuration by default. They can be restored or mined later, but the active folders remain the source that tools and humans should normally consume.

### `templates/`

`templates/` contains blank or minimal starter points for creating new agentic artifacts.

Use it for examples and scaffolds for new skills, persona bundles, rules, workflows, and similar reusable context. Templates are source material for authors, not production capability.

The template area mirrors the main capability categories:

- `templates/agents/`
- `templates/skills/`
- `templates/rules/`
- `templates/workflows/`

Current examples include:

- `templates/skills/skill-template`
- `templates/skills/skill-template-advanced`

When creating a new artifact, start from the closest template, copy it into the active folder, then rename and fill it in. Do not expose templates directly to agentic IDEs.

### `prompt_dev/skills_prompts/`

Prompts can be as valuable as source code.

`prompt_dev/skills_prompts/` preserves prompt records and source material used to create, revise, or reason about skills and agents. If a generated skill is the artifact, these prompt records are often the design history behind it.

Keeping prompt source material separate makes it easier to refine the artifacts later without losing the original thinking.

### `wiki/`

`wiki/` contains local documentation about Agent Skills and this repository's conventions.

It is not a replacement for AgentSkills.io. It is a local, reviewable companion that captures the parts of the standard this repository relies on most often:

- Overview
- Specification notes
- Best practices
- Description optimization
- Skill evaluation
- Script usage
- Repository alignment notes

### `ide_specific/`

`ide_specific/` is intentionally a junk pile for vendor-specific files and conventions that do not belong in the standard layers.

It exists because real tools are messy. Some IDEs need one-off folders, rule files, metadata, or naming conventions that are not portable. Those files can live here as a means to an end, but they should not define the repository's architecture.

### `workflows/`

`workflows/` is not the active workflow system.

It contains [`workflows/NOT USED.txt`](workflows/NOT%20USED.txt), which records the decision to stop using a standalone workflows folder. Advanced workflows now live under `skills/` with the `-workflow` suffix because that works better across current agentic IDEs.

## Relationship To `agentic_rails_context_starter`

[`agentic_rails_context_starter`](../agentic_rails_context_starter/) is the companion GitHub template for new projects — the left rail of the Agentic Rails framework.

The split is:

| Repository | Owns |
| --- | --- |
| `agentic_rails_context_starter` | Project-local context: Tier 0 intake, design, milestones, goals, implementation plans, handovers, and wiki notes. |
| `agentic_rails_tooling` | Reusable agent capabilities: shared rules, Agent Skills, workflow-skills, specialist persona bundles, and prompt-development source material. |

In practice, `agentic_rails_context_starter` gives a project its documentation-first operating model. It is intentionally empty of application code. It gives future agent sessions a five-tier context system:

- Tier 0 raw intake and addenda
- Tier 1 design
- Tier 2 milestones
- Tier 3 goals
- Tier 4 implementation plans and handovers

This repository gives agents reusable tools to execute inside that model.

For example:

- A new project can start from `agentic_rails_context_starter`.
- The project's `AGENTS.md` and `context/agenticworkflow.md` define how agents load local context.
- Shared rules from this repository can be copied or installed into the IDE's expected rule location.
- Skills such as `commit-log`, `rails-planning`, or `rails-boss-execute-workflow` can be installed globally or made available through `%USERPROFILE%\.agents`.
- Specialist personas such as `agents/wpf-persona` can be used when the project calls for that domain expertise.

The project remains usable without this repository, but it becomes much stronger when these reusable assets are available.

## Relationship To `kung-fu`

[`kung-fu`](../kung-fu/) is the local WPF deployment app for consuming the artifacts in this repository across agentic IDEs.

This repository is the source of truth. Kung Fu reads configured source folders for skills, rules, workflows, and agents, then copies them outward into the folder layouts expected by different IDEs, profiles, staging folders, or the shared `%USERPROFILE%/.agents` workspace.

The relationship is deliberately one-way:

```text
agentic_tooling -> Kung Fu sync -> IDE and workspace configuration folders
```

Kung Fu manages deployment, not authorship. Edits should happen in this repository, while Kung Fu makes the active artifacts available wherever the current agentic tool expects them. Archived artifacts are retained here for reference, and templates are retained here for authoring new artifacts. Neither `archived/` nor `templates/` should be included in the normal Kung Fu sync set unless a specific artifact is intentionally promoted into an active folder.

## Working Model

When adding or updating reusable context, place it in the narrowest layer that matches its job:

- Put it in `rules/` if it is short, prescriptive, and style-oriented.
- Put it in `skills/` if it is reusable expertise, workflow knowledge, or a portable task module.
- Put it in `skills/<name>-workflow/` if it coordinates a larger multi-step process, subagents, queues, or durable artifacts.
- Put it in `agents/` if it defines a named specialist persona with a mission, operating model, and reference library.
- Put it in `archived/` if it is preserved for reference but should not be part of the active agentic capability set.
- Put it in `templates/` if it is a blank, skeletal, or example starter point for creating a future artifact.
- Put it in `prompt_dev/skills_prompts/` if it is prompt source material used to generate or evolve an artifact.
- Put it in `wiki/` if it documents the standards and local conventions behind the repository.
- Put it in `ide_specific/` only when a tool requires a nonstandard compatibility file.

## Layer Examples

- A WPF naming rule belongs in `rules/wpf_rules.md`.
- A reusable commit message process belongs in `skills/commit-log`.
- A questionable or superseded skill belongs in `archived/skills/`.
- A retired multi-skill workflow, such as the old Mermaid mapping pipeline, belongs in `archived/skills/` with its related skills.
- A blank starter for a future persona bundle belongs in `templates/agents/`.
- A production-grade WPF specialist persona belongs in `agents/wpf-persona`.
- The prompt material used to generate a skill belongs in `prompt_dev/skills_prompts/`.

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
- Keep templates out of normal sync/deployment paths; copy from them into active folders before use.

## Repository

- Repository: https://github.com/JarrydSemmens/agentic_rails_tooling
- Owner: Jarryd Adaens
- Last Updated: 2026-05-07
