---
name: skill-template
description: Use this template when creating a new Agent Skill that needs valid SKILL.md frontmatter, declared arguments, concise trigger guidance, and a workflow.
disable-model-invocation: false
argument-hint: "<payload> [--flag]"
metadata:
  version: "2.0"
  template: "true"
---

# Skill Template

Replace this starter content with real task-specific expertise before treating the skill as production-ready. The bar this must meet is `context/wiki/skill-authoring-standard.md`; `scripts/rails_lint.py` enforces its mechanical half.

Set `disable-model-invocation` deliberately: `true` when the skill must run only on an explicit user request, `false` when ambient triggering is wanted. Delete `argument-hint` and the `## Arguments` section below only if the skill genuinely takes nothing.

## Arguments

The skill was invoked with: $ARGUMENTS

Read that line before doing anything else. It is free text, so parse it leniently, and treat plain-language equivalents as equal to the tokens.

| Token | Meaning |
| --- | --- |
| `--flag` | What it turns on, and what happens when it is absent. |
| anything else | The main payload. |

Empty `$ARGUMENTS` is the normal case, never an error. Never ask the user to re-invoke with arguments — and never obtain mid-run a parameter the invocation could have carried.

## When to use

- Use this as the starting point for a small or moderate skill.
- Use `skill-template-advanced` instead when the skill needs a reference library.

## Workflow

1. Rename the folder and `name` field to the final skill name.
2. Rewrite `description` to say what the skill does and when to use it, beginning with the word "Use".
3. Replace the argument table with the skill's real parameters, or delete it.
4. Add the workflow, defaults, gotchas, and output contract the agent needs.
5. Move longer detail into `references/` and link to it — never restate a reference's content here.

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Replace this list with the skill's real rules, each stated once.

## Acceptance

State observable facts a third party can check, not questions for the agent that did the work:

- The named output file exists at the stated path.

No unfalsifiable criteria, and no self-attestation. Where real judgment is needed, dispatch `agents/quality-gate-persona/AGENT.md` and take its verdict instead.
