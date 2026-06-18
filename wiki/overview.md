---
metadata:
  version: "1.0"
---

# Agent Skills Overview

Agent Skills are a lightweight, open format for extending AI agents with specialized knowledge, reusable workflows, scripts, references, templates, and other resources.

At minimum, a skill is a folder containing `SKILL.md`:

```text
my-skill/
|-- SKILL.md
|-- scripts/
|-- references/
|-- assets/
`-- ...
```

## Why Skills Exist

Skills package context that agents do not reliably know by default:

- Domain expertise, such as legal review, data pipelines, presentation standards, or internal engineering workflows.
- Repeatable procedures that should be consistent and auditable.
- Portable capability modules that can be reused across compatible agent clients.

## Progressive Disclosure

Skills are loaded in stages:

1. Discovery: the agent sees only the skill name and description.
2. Activation: the agent reads the full `SKILL.md` when a task matches the description.
3. Execution: the agent follows the instructions and loads scripts, references, or assets only as needed.

This lets a client keep many skills available without putting every full instruction file into context at startup.

## Open Standard

The Agent Skills format was originally developed by Anthropic, released as an open standard, and adopted across multiple agentic tools, including OpenAI Codex and other coding agents.

Source: [AgentSkills.io Overview](https://agentskills.io/home)
