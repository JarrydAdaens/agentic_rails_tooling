# Agentic Tooling

This repository is not just a collection of rules. It is a modular context system for AI-assisted development.

The goal is to store reusable context in the right layer, so agents can be given exactly the amount and kind of guidance they need:

- Small style and standards guidance
- Reusable skill-sized knowledge modules
- Agent definitions with tools and expertise
- Prompt records that act as the source material for generated outputs

## Core Idea

Different kinds of context should not all live in one place.

This repository separates:

- Lightweight rules from deeper expertise
- Reusable skill modules from agent definitions
- Generated artifacts from the prompt text that produced them

That separation makes it easier to maintain, evolve, and reuse context across projects and agents.

## Repository Structure

### `.rules/`

This folder is for style guides, coding rules, and smaller context files.

Use `.rules/` for things like:

- Language and framework standards
- Formatting expectations
- Naming conventions
- General engineering rules
- Workspace-level behavior constraints

Current examples include:

- `.rules/global_rules.md`
- `.rules/csharp_rules.md`
- `.rules/cplusplus_rules.md`
- `.rules/wpf_rules.md`
- `.rules/qt_rules.md`
- `.rules/.cursorrules`

In short: `.rules/` is for concise guidance and style-shaping context, not broad expertise systems.

### `.skills/`

This folder is for modular chunks of context.

A skill is a reusable unit of expertise, behavior, or process guidance that an agent can load when it is relevant. Skills are larger and more capability-oriented than rules.

Use `.skills/` for things like:

- Domain knowledge such as WPF, game development, or XNA/MonoGame
- Process skills such as writing commit logs correctly
- Tool-usage guidance for specific CLIs or workflows
- Progressive-disclosure expertise split across reference files

Current examples include:

- `.skills/wpf`
- `.skills/gamedev`
- `.skills/xna`
- `.skills/commit-log`
- `.skills/commit-history`
- `.skills/skill-template`
- `.skills/skill-template-advanced`

In short: `.skills/` is where deeper, task-shaped context lives.

### `.agents/`

This folder is for defining agents: their tools, their expertise, and the shape of the work they are meant to do.

Agents will usually depend on skills, and they are often used to prime a sub-agent for a specific role.

Use `.agents/` for things like:

- Specialist agent definitions
- Tool access configuration
- Role-specific expertise bundles
- Sub-agent priming setups

In short: `.agents/` defines the worker, while `.skills/` defines reusable knowledge the worker can carry.

### `prompt_dev/`

This folder holds records of prompts used to produce artifacts.

Right now it mainly contains WPF-development prompt material that was driven by NotebookLM, but the idea is broader than that.

If a skill file is an output artifact, the text files in `prompt_dev/` are closer to source code.

That means:

- A prompt record can capture how a skill or context pack was produced
- The generated skill can be refined later without losing the original source thinking
- The repository can preserve both the artifact and the prompt lineage behind it

In short: `prompt_dev/` is the source-material layer for generated context.

## How the Layers Relate

Think of the repository as a stack:

1. `.rules/` shapes style, standards, and small constraints.
2. `.skills/` provides modular expertise and reusable task guidance.
3. `.agents/` assembles tools and skills into a usable specialist worker.
4. `prompt_dev/` preserves the prompt history and source material behind generated outputs.

These layers are related, but they should not be collapsed into one another.

For example:

- A WPF naming or formatting convention belongs in `.rules/`
- A production-grade WPF engineering knowledge system belongs in `.skills/`
- A UI-focused specialist sub-agent definition belongs in `.agents/`
- The prompt set used to generate a WPF skill belongs in `prompt_dev/`

## Working Model

When adding or updating context, place it in the narrowest layer that matches its job.

Use this rule of thumb:

- Put it in `.rules/` if it is short, prescriptive, and style-oriented.
- Put it in `.skills/` if it is reusable expertise, workflow knowledge, or a modular context pack.
- Put it in `.agents/` if it defines what an agent can do and how it should be equipped.
- Put it in `prompt_dev/` if it is source prompt material used to generate or evolve an output artifact.

## Skills as Modular Context

Many of the skills in this repository use progressive disclosure.

That means:

- The main skill file defines stance, routing, and when to load deeper material
- Reference files hold focused chunks of deeper expertise
- Only the smallest relevant set of references should be loaded for a given task

This keeps broad domains usable without turning every skill into a giant context dump.

## Maintenance Notes

- Keep rules concise.
- Keep skills modular.
- Keep agents explicit about tools and role.
- Keep prompt records when they are the real source behind generated artifacts.
- Prefer focused files over giant omnibus documents.
- Preserve the distinction between source material and produced output.

## Repository

- Repository: https://github.com/JarrydSemmens/agentic_tooling
- Owner: Jarryd Adaens
- Last Updated: 2026-04-06
