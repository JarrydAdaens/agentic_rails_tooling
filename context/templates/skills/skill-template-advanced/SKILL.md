---
name: skill-template-advanced
description: Use this template when creating a broad Agent Skill that needs progressive disclosure, focused reference files, and routing guidance without loading all domain knowledge up front.
disable-model-invocation: false
argument-hint: "<payload> [--flag]"
metadata:
  version: "2.0"
  template: "true"
---

# Advanced Progressive-Disclosure Skill Template

For building large skills that represent a real expertise domain without turning the main skill file into a monolith — UI engineering, game development, framework architecture, tooling ecosystems, and similar domains needing both breadth and restraint.

The bar this must meet is `context/wiki/skill-authoring-standard.md`; `scripts/rails_lint.py` enforces its mechanical half. Nothing in this file restates what a reference says, and no section restates another section.

Set `disable-model-invocation` deliberately. Delete `argument-hint` and `## Arguments` only if the skill genuinely takes nothing.

## Arguments

The skill was invoked with: $ARGUMENTS

Read that line before doing anything else. It is free text, so parse it leniently, and treat plain-language equivalents as equal to the tokens.

| Token | Meaning |
| --- | --- |
| `--flag` | What it turns on, and what happens when it is absent. |
| anything else | The main payload. |

Empty `$ARGUMENTS` is the normal case, never an error.

## Routing

This file is the **router and operating model**, not the body of knowledge. It answers what the domain covers, how to think inside it, which references to load, and what defaults and boundaries shape the work. The references hold the domain truth.

Before loading anything, identify what the user is actually solving and which expertise layer is in play. Then load the **smallest** reference set that gives enough domain truth — one for a narrow task, two when it crosses a boundary, more only when the work genuinely spans layers. The goal is solving the problem, not proving coverage.

Keep each reference tight and single-purpose. When one starts carrying multiple concerns, split it. Prefer the least complex solution the domain allows.

## Included Example References

Structural examples, not final content. Rename and rewrite each one to own a single real concern, then update these links.

- [references/reference-1.md](references/reference-1.md) — one focused expertise slice.
- [references/reference-2.md](references/reference-2.md) — a second slice that should stay separate from the first.
- [references/reference-3.md](references/reference-3.md) — a third slice, where progressive loading choices matter.

Add more references only for genuinely separate concerns.

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Replace this list with the skill's real rules, each stated once.
- Replace every placeholder above before treating a derived skill as production-ready.

### Surviving compaction

Required when this skill's run can outlive one context window. Name the files that carry the durable state, and state that they are written before each next step rather than at the end. Delete this section for a skill that completes within a single exchange.

## Acceptance

State observable facts a third party can check, not questions for the agent that did the work:

- The named output file exists at the stated path.

No unfalsifiable criteria, and no self-attestation. Where real judgment is needed, dispatch `agents/quality-gate-persona/AGENT.md` and take its verdict instead.
