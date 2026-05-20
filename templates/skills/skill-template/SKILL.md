---
name: skill-template
description: Use this template when creating a new Agent Skill that needs valid SKILL.md frontmatter, concise trigger guidance, workflow instructions, examples, and validation notes.
metadata:
  template: "true"
  version: "1.0"
  agentic_rails_source_version: "1.0"
---

# Skill Template

Replace this starter content with real task-specific expertise before treating the skill as production-ready.

## When to use

- Use this as the starting point for a small or moderate skill.
- Use `skill-template-advanced` instead when the skill needs a reference library or complex progressive disclosure.

## Instructions

1. Rename the folder and `name` field to the final skill name.
2. Rewrite `description` so it says what the skill does and when to use it.
3. Add the workflow, defaults, gotchas, and output contract the agent needs.
4. Move longer details into `references/` and link to them from this file.
5. Validate that the folder name and `name` field match.

## Examples

- Example user request that should trigger this skill.
- Example output shape the skill should produce.

## Validation

- Confirm the `description` is under 1024 characters.
- Confirm the skill name uses lowercase letters, numbers, and hyphens only.
- Confirm no placeholder text remains.

