# Agentic Tooling

This repository is a layered context system for AI-assisted development.

The goal is to keep reusable guidance in the right place, so agents can load the minimum useful context for the job:

- Short rules and standards
- Reusable skills and workflow modules
- Specialist agent definitions
- Prompt-development records that preserve source material

## Core Idea

Different kinds of context should not live in the same layer.

This repository separates:

- Lightweight rules from deeper reusable guidance
- Reusable skills from named specialist agents
- Produced artifacts from the prompt material that generated them

That separation makes the system easier to maintain, evolve, and reuse across projects.

## Repository Structure

### `.rules/`

This folder is for concise rule files: style guides, coding rules, and smaller instruction sets.

Start at `.rules/index.md`. It is the entry point for selecting the minimum relevant shared rules for a given repository and task.

Use `.rules/` for things like:

- Language and framework standards
- Formatting expectations
- Naming conventions
- General engineering rules
- Workspace-level behavior constraints

Current examples include:

- `.rules/index.md`
- `.rules/global_rules.md`
- `.rules/csharp_rules.md`
- `.rules/cplusplus_rules.md`
- `.rules/wpf_rules.md`
- `.rules/qt_rules.md`
- `.rules/.cursorrules`

In short: `.rules/` is for concise guidance and style-shaping context, not for large domain knowledge packs.

### `.skills/`

This folder is for reusable capability modules that an agent can load on demand.

A skill is a portable unit of expertise, behavior, or process guidance. It should stay reusable across different agent roles rather than defining a full specialist worker.

Use `.skills/` for things like:

- Process skills such as writing commit logs correctly
- Tool-usage guidance for specific CLIs or workflows
- Reusable compatibility checks
- Templates for authoring new skills

Current examples include:

- `.skills/commit-log`
- `.skills/commit-history`
- `.skills/check_dot_agent`
- `.skills/skill-template`
- `.skills/skill-template-advanced`

In short: `.skills/` is for reusable task-shaped knowledge, not broad persona-style specialist workers.

### `.agents/`

This folder is for named specialist agents: workers with an explicit mission, operating model, quality bar, and supporting reference library.

An agent bundle in this repository typically contains:

- `AGENT.md` for the role definition and operating contract
- `agents/openai.yaml` for provider-facing interface metadata
- `references/` for focused domain modules loaded only when needed

Current examples include:

- `.agents/gamedev`
- `.agents/wpf`
- `.agents/xna`

These three used to live under `.skills/`, but they fit better as agents because each one defines a specialist role, a way of thinking, collaboration boundaries, and a curated reference library rather than a narrowly reusable skill.

In short: `.agents/` defines the worker, while `.skills/` defines reusable knowledge a worker can carry.

### `prompt_dev/`

This folder holds prompt-development records used to produce artifacts.

If a skill or agent file is an output artifact, the text files in `prompt_dev/` are closer to source material.

That means:

- A prompt record can capture how a skill or agent bundle was produced
- The generated artifact can be refined later without losing the original source thinking
- The repository can preserve both the artifact and the prompt lineage behind it

In short: `prompt_dev/` is the source-material layer for generated context.

## How the Layers Relate

Think of the repository as a stack:

1. `.rules/` shapes style, standards, and small constraints.
2. `.skills/` provides reusable workflow guidance and modular expertise.
3. `.agents/` defines specialist workers with role contracts and supporting reference libraries.
4. `prompt_dev/` preserves the prompt history and source material behind generated outputs.

These layers are related, but they should not be collapsed into one another.

For example:

- A WPF naming or formatting convention belongs in `.rules/`
- A reusable commit-log workflow belongs in `.skills/commit-log`
- A production-grade WPF specialist worker belongs in `.agents/wpf`
- The prompt set used to generate or evolve one of those artifacts belongs in `prompt_dev/`

## Working Model

When adding or updating context, place it in the narrowest layer that matches its job.

Use this rule of thumb:

- Put it in `.rules/` if it is short, prescriptive, and style-oriented.
- Put it in `.skills/` if it is reusable expertise, workflow knowledge, or a portable task module.
- Put it in `.agents/` if it defines a named worker: mission, scope, operating model, and supporting references.
- Put it in `prompt_dev/` if it is source prompt material used to generate or evolve an output artifact.

## Skills and Agents

Both skills and agents can use progressive disclosure, but they serve different purposes.

Typical pattern:

- A skill provides reusable guidance that many different agents can load.
- An agent defines who is doing the work, how it should think, when it should escalate, and which references it should consult.
- Reference files keep deeper expertise modular so the active context stays small.

If a context pack starts behaving like a standing specialist persona instead of a portable capability module, it likely belongs in `.agents/`.

## Maintenance Notes

- Keep rules concise.
- Keep skills portable and reusable.
- Keep agents explicit about mission, scope, collaboration boundaries, and quality bar.
- Keep provider metadata aligned with the actual agent definition.
- Keep prompt records when they are the real source behind generated artifacts.
- Prefer focused files over giant omnibus documents.
- Preserve the distinction between source material and produced output.

## Repository

- Repository: https://github.com/JarrydSemmens/agentic_tooling
- Owner: Jarryd Adaens
- Last Updated: 2026-04-07
