# Agentic Tooling

`agentic_tooling` is my reusable capability library for agentic development.

It keeps the durable pieces of AI-assisted engineering in one version-controlled place: rules, skills, specialist agents, workflow-skills, and the prompt source material used to create or improve them. The point is not loyalty to Anthropic, OpenAI, Google, Cursor, Windsurf, or any other specific IDE or model provider. The point is portable agent capability that can be installed, copied, adapted, and reused wherever the current best tool expects it.

This repository is especially useful beside project templates such as [`agentic_starter`](../agentic_starter/), where the project owns its local context and this repository supplies reusable operating knowledge.

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

- `skills/check-dot-agent`
- `skills/commit-log`
- `skills/grade`
- `skills/mermaid-scout`
- `skills/mermaid-mapper`
- `skills/mermaid-validation`
- `skills/mermaid-aggregation`
- `skills/skill-template`
- `skills/skill-template-advanced`

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

- `skills/commit-history-workflow`
- `skills/implementation-plan-executor-workflow`
- `skills/mermaid-mapper-workflow`
- `skills/plan-spam-workflow`

Workflow-skills should coordinate. They can define queues, subagent roles, artifact paths, handover rules, and validation gates. Reusable domain behavior should still live in ordinary skills when possible.

### `agents/`

`agents/` contains named specialist workers.

An agent is different from a skill. A skill says, "Here is how to do this task." An agent says, "Here is the kind of worker you are, how you think, what quality bar you uphold, and which references you consult."

Current examples include:

- `agents/gamedev`
- `agents/wpf`
- `agents/xna`

Each agent bundle typically includes:

- `AGENT.md` for the role definition and operating contract
- Provider-facing metadata under an `agents/` subfolder
- `references/` for focused supporting knowledge

Use `agents/` for durable specialist workers, not small reusable procedures.

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

## Relationship To `agentic_starter`

[`agentic_starter`](../agentic_starter/) is a companion GitHub template for new projects.

The split is:

| Repository | Owns |
| --- | --- |
| `agentic_starter` | Project-local context: Tier 0 intake, design, laws, milestones, goals, implementation plans, handovers, and wiki notes. |
| `agentic_tooling` | Reusable agent capabilities: shared rules, Agent Skills, workflow-skills, specialist agents, and prompt-development source material. |

In practice, `agentic_starter` gives a project its documentation-first operating model. It is intentionally empty of application code. It gives future agent sessions a five-tier context system:

- Tier 0 raw intake and addenda
- Tier 1 design
- Tier 2 milestones
- Tier 3 goals
- Tier 4 implementation plans and handovers

This repository gives agents reusable tools to execute inside that model.

For example:

- A new project can start from `agentic_starter`.
- The project's `AGENTS.md` and `Documentation/agenticworkflow.md` define how agents load local context.
- Shared rules from this repository can be copied or installed into the IDE's expected rule location.
- Skills such as `commit-log`, `grade`, or `implementation-plan-executor-workflow` can be installed globally or made available through `%USERPROFILE%\.agents`.
- Specialist agents such as `agents/wpf` can be used when the project calls for that domain expertise.

The project remains usable without this repository, but it becomes much stronger when these reusable assets are available.

## Relationship To `kung-fu`

[`kung-fu`](../kung-fu/) is the WPF companion application/template in this ecosystem.

Where `agentic_starter` is a general project-context template, `kung-fu` is a WPF-oriented starter with real application structure, WPF documentation, `AGENTS.md` guidance, `Documentation/` context files, laws, tests, and a concrete source tree. It is a practical place where this repository's WPF rules and agentic workflow ideas are exercised against a desktop application codebase.

The relationship is practical rather than branded. `agentic_tooling` stores reusable rules and agent capabilities. `kung-fu` shows those practices applied to a WPF project shape.

## Working Model

When adding or updating reusable context, place it in the narrowest layer that matches its job:

- Put it in `rules/` if it is short, prescriptive, and style-oriented.
- Put it in `skills/` if it is reusable expertise, workflow knowledge, or a portable task module.
- Put it in `skills/<name>-workflow/` if it coordinates a larger multi-step process, subagents, queues, or durable artifacts.
- Put it in `agents/` if it defines a named specialist worker with a mission, operating model, and reference library.
- Put it in `prompt_dev/skills_prompts/` if it is prompt source material used to generate or evolve an artifact.
- Put it in `wiki/` if it documents the standards and local conventions behind the repository.
- Put it in `ide_specific/` only when a tool requires a nonstandard compatibility file.

## Layer Examples

- A WPF naming rule belongs in `rules/wpf_rules.md`.
- A reusable commit message process belongs in `skills/commit-log`.
- A large Mermaid mapping pipeline belongs in `skills/mermaid-mapper-workflow`.
- The individual Mermaid scout, mapper, validator, and aggregator behaviors belong in separate normal skills.
- A production-grade WPF specialist worker belongs in `agents/wpf`.
- The prompt material used to generate a skill belongs in `prompt_dev/skills_prompts/`.

## Maintenance Notes

- Prefer open standards and portable formats.
- Keep the AgentSkills.io specification close at hand when changing skills.
- Keep rules concise.
- Keep normal skills task-shaped and reusable.
- Suffix advanced orchestrations with `-workflow`.
- Keep workflow-skills focused on orchestration rather than swallowing every detail.
- Keep agents explicit about mission, scope, collaboration boundaries, references, and quality bar.
- Keep prompt records when they are the real source behind generated artifacts.
- Keep IDE-specific files isolated from the core architecture.

## Repository

- Repository: https://github.com/JarrydSemmens/agentic_tooling
- Owner: Jarryd Adaens
- Last Updated: 2026-04-26
