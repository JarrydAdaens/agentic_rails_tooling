---
metadata:
  version: "1.0"
---

# Best Practices For Skill Creators

Good skills are grounded in real expertise, not generic advice. They capture the steps, corrections, formats, constraints, and edge cases that make a task reliable in practice.

## Start From Real Work

Useful source material includes:

- A hands-on task completed with an agent.
- Corrections the user had to make during execution.
- Internal docs, runbooks, style guides, schemas, and API specs.
- Code review comments, issues, and historical fixes.
- Real failures and their resolutions.

## Spend Context Carefully

Once a skill activates, the full `SKILL.md` competes with the task, conversation, and other loaded context. Include what the agent would likely miss without the skill:

- Project-specific conventions.
- Domain-specific procedures.
- Non-obvious edge cases.
- Tool choices and exact commands.
- Output formats and validation requirements.

Cut generic background that the model already knows.

## Scope Skills Coherently

A skill should cover a coherent unit of work. Too narrow and several skills need to load for one task; too broad and activation becomes noisy. If the skill grows, keep the core routing and workflow in `SKILL.md`, then move deeper material to focused `references/` files.

## Calibrate Control

Use strict instructions for fragile, stateful, destructive, or sequence-sensitive work. Use more flexible guidance when multiple approaches are valid and the task can tolerate variation.

Prefer defaults over menus. Pick the normal tool or workflow, then mention alternatives only as escape hatches.

## Effective Patterns

- Gotchas: concrete facts that prevent likely mistakes.
- Templates: exact output structures for repeated deliverables.
- Checklists: ordered steps for multi-stage work.
- Validation loops: do the work, validate, fix, repeat.
- Plan-validate-execute: create an intermediate plan before batch or destructive work.
- Bundled scripts: package repeated parsing, validation, or generation logic.

Source: [AgentSkills.io Best Practices](https://agentskills.io/skill-creation/best-practices)
