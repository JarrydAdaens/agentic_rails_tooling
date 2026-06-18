---
metadata:
  version: "1.0"
---

# Agent Skills Specification

This page summarizes the compatibility requirements for skills in this repository.

## Directory Structure

A skill directory must contain `SKILL.md`. Optional folders can hold executable scripts, reference material, and static assets.

```text
skill-name/
|-- SKILL.md
|-- scripts/
|-- references/
|-- assets/
`-- ...
```

## SKILL.md Format

`SKILL.md` must contain YAML frontmatter followed by Markdown instructions.

Required frontmatter:

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

Optional frontmatter:

```yaml
license: Apache-2.0
compatibility: Requires git and internet access.
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Read
```

## Name Rules

The `name` field:

- Must be 1-64 characters.
- Must use lowercase letters, numbers, and hyphens only.
- Must not start or end with a hyphen.
- Must not contain consecutive hyphens.
- Must match the parent directory name.

## Description Rules

The `description` field:

- Must be non-empty and at most 1024 characters.
- Should say what the skill does and when to use it.
- Should include specific user-intent keywords that help the agent activate it.

## Body Guidance

The Markdown body has no strict schema. Recommended content includes:

- Step-by-step instructions.
- Input and output examples.
- Gotchas and edge cases.
- Validation loops.

Keep `SKILL.md` under 500 lines when practical. Move longer references into `references/` and tell the agent exactly when to load them.

## Optional Directories

- `scripts/`: executable helpers with clear dependencies, non-interactive inputs, helpful errors, and predictable output.
- `references/`: focused supporting documentation loaded on demand.
- `assets/`: templates, images, schemas, lookup tables, or other static resources.

## Validation

Use the reference validator when available:

```bash
skills-ref validate ./my-skill
```

Source: [AgentSkills.io Specification](https://agentskills.io/specification)
