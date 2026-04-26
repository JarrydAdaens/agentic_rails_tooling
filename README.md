# Agentic Tooling

`agentic_tooling` is my reusable capability library for agentic development.

It keeps the durable pieces of AI-assisted engineering in one place: rules, skills, specialist agents, workflow-skills, and the source prompts used to create or improve them. The point is not loyalty to one IDE, model provider, or vendor convention. The point is portable, version-controlled agent capability that can be installed or adapted wherever the current best tool expects it.

This repository is especially useful alongside project templates such as [`agentic_starter`](../agentic_starter/), where the project owns its local context and this repository supplies reusable operating knowledge.

## Core Idea

Agentic IDEs are useful, but their conventions are fragmented. Some recognize global rules. Some understand skills. Some support agents. Some have their own private folders. A few are starting to recognize central user-level locations such as `%USERPROFILE%\.agents`.

This repository keeps those concerns separated:

- `rules/` contains concise engineering standards and style guidance.
- `skills/` contains reusable Agent Skills and advanced workflow-skills.
- `agents/` contains named specialist workers with role contracts and reference libraries.
- `prompt_dev/skills_prompts/` preserves high-value prompt source material.
- `ide_specific/` holds unavoidable vendor-specific compatibility files.

The goal is to stay IDE-agnostic while still being practical enough to use every day.

## Grounded In Agent Skills

Much of this repository's skills model is based on the open [Agent Skills specification](https://agentskills.io/specification).

Agent Skills define a lightweight folder format for giving agents new capabilities. A skill is a directory containing a required `SKILL.md` file with metadata and instructions. Skills can also include optional `scripts/`, `references/`, and `assets/` folders.

The specification matters because it gives this repository a real standard to build on:

- Skills are portable folders, not hidden IDE state.
- The `name` and `description` fields let agents discover relevant skills cheaply.
- Full instructions load only when the task calls for them.
- Extra scripts, references, and assets can be loaded on demand.
- The format supports cross-product reuse as more clients adopt it.

This repository leans into that model. The custom parts here exist to make the standard usable across many agentic IDEs, not to replace the standard.

## Repository Structure

### `rules/`

This folder is for concise shared rules: style guides, coding rules, and smaller instruction sets.

Start at `rules/index.md`. It is the entry point for selecting the minimum relevant shared rules for a repository and task.

Use `rules/` for:

- General engineering behavior
- Language and framework standards
- Formatting and naming conventions
- Stack-specific rules such as C#, C++, WPF, and Qt
- Compatibility files such as `rules/.cursorrules`

Rules should stay short and prescriptive. If a file becomes a large body of procedural expertise, it probably belongs in `skills/` or `agents/`.

### `skills/`

This folder is the main reusable capability layer.

A normal skill is a portable task-shaped unit of expertise. It should help an agent do one class of work reliably without becoming a whole persona.

Examples include:

- `skills/commit-log`
- `skills/grade`
- `skills/check-dot-agent`
- `skills/mermaid-scout`
- `skills/mermaid-mapper`
- `skills/mermaid-validation`
- `skills/mermaid-aggregation`
- `skills/skill-template`
- `skills/skill-template-advanced`

Use `skills/` for repeatable workflows, tool guidance, templates, and focused process knowledge.

### `skills/*-workflow`

Advanced multi-step workflows also live in `skills/`, but they are suffixed with `-workflow`.

The old `workflows/` folder was an exploratory failure. The idea was good: some agentic procedures are large enough to run for hours, use subagents heavily, persist intermediate artifacts, and produce reusable outputs. The problem is that agentic IDEs generally do not understand a separate `workflows/` primitive.

The practical convention is:

```text
<name>-workflow
```

That makes powerful workflows easy to find through autocomplete in ordinary skill pickers while still making their purpose obvious.

Examples include:

- `skills/commit-history-workflow`
- `skills/implementation-plan-executor-workflow`
- `skills/mermaid-mapper-workflow`
- `skills/plan-spam-workflow`

Workflow-skills should stay orchestration-focused. They can coordinate subagents, define artifact paths, manage queues, and compose smaller skills. The reusable domain behavior should still live in ordinary skills where possible.

### `agents/`

This folder is for named specialist agents.

An agent is different from a skill. A skill says, "Here is how to do this task." An agent says, "Here is the kind of worker you are, how you think, what quality bar you uphold, and which references you consult."

Current examples include:

- `agents/gamedev`
- `agents/wpf`
- `agents/xna`

Each agent bundle typically includes:

- `AGENT.md` for the role definition and operating contract
- provider-facing metadata under an `agents/` subfolder
- `references/` for focused supporting knowledge

Use `agents/` for durable specialist workers, not small reusable procedures.

### `prompt_dev/skills_prompts/`

Prompts can be as valuable as source code.

`prompt_dev/skills_prompts/` preserves prompt records and source material used to create, revise, or reason about skills and agents. If a generated skill is the artifact, these prompt records are often the design history behind it.

Keeping them separate makes it easier to refine the artifacts later without losing the original thinking.

### `ide_specific/`

This folder is intentionally a junk pile for vendor-specific files and conventions that do not belong in a standard layer.

It exists because real tools are messy. Some IDEs need one-off files, global folders, or naming conventions that are not portable. Those files can live here as a means to an end, but they should not define the repository's architecture.

### `workflows/`

`workflows/` is not the active workflow system.

It contains `NOT USED.txt`, which records the decision to stop using a standalone workflows folder. Advanced workflows now live under `skills/` with the `-workflow` suffix because that works better across current agentic IDEs.

## Relationship To `agentic_starter`

[`agentic_starter`](../agentic_starter/) is a companion GitHub template for new projects.

The split is:

| Repository | Owns |
| --- | --- |
| `agentic_starter` | Project-local context: Tier 0 intake, design, laws, milestones, goals, implementation plans, handovers, and wiki notes. |
| `agentic_tooling` | Reusable agent capabilities: shared rules, skills, workflow-skills, specialist agents, and prompt-development source material. |

In practice, `agentic_starter` gives a project its documentation-first operating model. This repository gives agents better reusable tools to execute inside that model.

For example:

- A new project can start from `agentic_starter`.
- The project's `AGENTS.md` and `Documentation/agenticworkflow.md` define how agents load local context.
- Shared rules from this repository can be copied or installed into the IDE's expected rule location.
- Skills such as `commit-log` or `implementation-plan-executor-workflow` can be installed globally or made available through `%USERPROFILE%\.agents`.
- Specialist agents such as `agents/wpf` can be used when the project calls for that domain expertise.

The project remains usable without this repository, but it becomes much stronger when these reusable assets are available.

## Relationship To `kung-fu`

[`kung-fu`](../kung-fu/) is a WPF companion project and application/template that lives in the same ecosystem as this repository's rules.

Where this repository stores reusable rules and agent capabilities, `kung-fu` demonstrates and benefits from the WPF-oriented version of that workflow: a documentation-first project shape, `AGENTS.md` guidance, `Documentation/` context files, WPF rules, and a concrete application codebase.

The relationship is practical rather than branded. `kung-fu` is one place these rules and agent practices are exercised against a real WPF codebase.

## Working Model

When adding or updating reusable context, place it in the narrowest layer that matches its job:

- Put it in `rules/` if it is short, prescriptive, and style-oriented.
- Put it in `skills/` if it is reusable expertise, workflow knowledge, or a portable task module.
- Put it in `skills/<name>-workflow/` if it coordinates a larger multi-step process, subagents, queues, or durable artifacts.
- Put it in `agents/` if it defines a named specialist worker with a mission, operating model, and reference library.
- Put it in `prompt_dev/skills_prompts/` if it is prompt source material used to generate or evolve an artifact.
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
- Keep rules concise.
- Keep normal skills task-shaped and reusable.
- Suffix advanced orchestrations with `-workflow`.
- Keep workflow-skills thin enough that they coordinate rather than swallow every detail.
- Keep agents explicit about mission, scope, collaboration boundaries, references, and quality bar.
- Keep prompt records when they are the real source behind generated artifacts.
- Keep IDE-specific files isolated from the core architecture.

## Repository

- Repository: https://github.com/JarrydSemmens/agentic_tooling
- Owner: Jarryd Adaens
- Last Updated: 2026-04-26
