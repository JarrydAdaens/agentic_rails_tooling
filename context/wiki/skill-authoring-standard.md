---
name: skill-authoring-standard
description: The bar every source/skills SKILL.md is held to — frontmatter, arguments, one canonical rule list, no self-evaluation, progressive disclosure, cross-artifact addressing, and compaction survival.
metadata:
  version: "1.0"
---

# Skill Authoring Standard

This is the bar every `source/skills/*/SKILL.md` is held to.

It is an **authoring-time** document. It is not deployed, and **no skill may link to it** — a
deployed skill linking to a non-deployed file produces a broken link in every target project,
which is the exact defect section 6 bans. `scripts/rails_lint.py` enforces the mechanical half.
The rest is reviewed by dispatching `source/agents/quality-gate-persona/AGENT.md` over the skill
with this file supplied as its project-rules input.

`source/skills/rails-boss-execute-workflow/SKILL.md` is the reference implementation of every
section below. Read it before writing or reshaping a skill.

## 1. Frontmatter

- `name` matches the folder. `description` is under 1024 characters and begins with the word
  `Use`. `metadata.version` is a quoted string.
- State `disable-model-invocation` explicitly: `true` when the skill must run only on an explicit
  user request, `false` when ambient triggering is wanted. Do not omit it.
- Carry `argument-hint` whenever the skill has any parameter a user could supply at invocation
  time. Shape: `"<required payload> [--switch value] [--flag]"`.

## 2. Arguments

**A parameter the invocation could have carried is never obtained by asking the user mid-run.**

- A skill with an `argument-hint` carries `## Arguments` as its first body section, containing:
  the line `The skill was invoked with: $ARGUMENTS`; an instruction to parse it leniently and
  treat plain-language equivalents as equal to the tokens; and a two-column token table whose
  final row is `anything else`, describing the main payload.
- Every token states its default when absent. Empty `$ARGUMENTS` is the normal case, never an
  error, and never a reason to ask the user to re-invoke with arguments.
- Do not invent a bespoke invocation syntax in prose. The `argument-hint` is the syntax; examples
  show real invocation lines, not bracketed pseudo-grammar.

## 3. One canonical rule list

- Each rule is stated **once**, in one section, and nothing else in the file restates it. Name
  that section `## Non-negotiable rules` and open it with: "This is the canonical rule list.
  Nothing else in this document restates it."
- `## Core Principles` plus `## Hard Rules` plus `## Validation` as three passes over one ruleset
  is the defect this replaces. Procedural sections link to the rule list; they do not re-derive it.
- A rule that needs restating to be obeyed is badly worded. Fix the wording once.

## 4. No self-evaluation

- A skill never ends with a checklist asking the agent that just did the work whether it did the
  work.
- Where an acceptance bar is genuinely needed, state it as **observable artifact facts a third
  party can check**: "`plan.md` exists at the stated path", "no `cer-score-card.md` remains in the
  folder", "the commit message carries a `~ Resolution:` line".
- Never write an unfalsifiable criterion — "useful questions were asked where appropriate", "the
  tone was collaborative", "the plan is grounded in concrete context".
- Where real judgment is needed, do not self-attest: dispatch
  `agents/quality-gate-persona/AGENT.md` and take its `PASS` / `PASS WITH NOTES` / `BLOCK` verdict
  plus its `GAPS / UNCERTAINTY` section. Separating the agent doing the work from the agent judging
  it is the single strongest quality lever available.

## 5. Progressive disclosure

- `SKILL.md` holds the trigger, the arguments, the workflow, and the rule list. Everything else
  lives in `references/` and is reached by link.
- If content lives in a reference, `SKILL.md` links to it and states at most the one-line
  consequence a reader needs in order to route correctly. Never reproduce a reference's table,
  template, or worked example in `SKILL.md` — that makes the reference not worth loading.
- Every file in `references/` is linked from `SKILL.md` or from another reference. An unlinked
  reference is dead weight: delete it, do not link it to satisfy this rule.

## 6. Cross-artifact addressing

- **Invoke another skill by name, never by path** — `rails-grade-cer`, not
  `skills/rails-grade-cer/SKILL.md`. Deployed skills live in the agent's own configuration
  directory; a worker's working directory is the target repository. A path like
  `skills/rails-planning/references/plan-template.md` resolves from neither, and it resolves least
  of all inside a prompt handed to a subagent.
- Only two path forms are legal in a `SKILL.md` body: `references/<file>.md` relative links to
  this skill's own references, and paths relative to the **target repository** root under
  `context/`. Always say which root a path is relative to.
- Content a subagent needs from another skill's reference is either restated inline in the
  dispatch payload, or obtained by telling the worker to invoke that skill by name. It is never
  passed as a filesystem path.

## 7. Compaction survival

- Any skill whose run can outlive one context window says so under a heading containing the words
  "surviving" and "compaction", and names the exact files that carry the durable state.
- The rule those files obey: **write state to disk before starting the next step, never after.**
  Never hold run state only in the conversation.
- Mandatory for every `-workflow` skill. Also mandatory for long interactive sessions — an
  artifact written once at the end, gated on hardcoded trigger phrases, is lost work the moment
  the session is compacted or abandoned.

## 8. Size

A `SKILL.md` past roughly 400 lines is almost always restating itself. Before adding a section,
find the section that already says it and improve that one instead.

## What is enforced how

| Enforced by `rails_lint.py` | Reviewed by `quality-gate-persona` |
| --- | --- |
| `FM002`–`FM005`, `DS001`, `AR001`–`AR003`, `WF001`–`WF002`, `RF001`–`RF002`, `PT001`, `SE001`, `DP001`, `LN001` | Whether a skill actually takes parameters (§2); whether criteria are falsifiable (§4); whether sections duplicate each other (§3); whether prose paraphrases a reference (§5); whether the named state files are sufficient to resume (§7) |

Four things in this standard are **not** mechanically decidable, and the linter deliberately does
not pretend otherwise:

- **Internal duplication (§3)** cannot be linted. An n-gram similarity heuristic delivers neither
  determinism nor a low false-positive rate, which are this linter's contract. `LN001` is a crude
  size proxy at best.
- **Whether a skill takes parameters (§2)** lives in prose. `AR001`–`AR003` enforce only the
  internal consistency of what an author declared; a skill with real parameters and no
  `argument-hint` passes clean.
- **Whether acceptance criteria are falsifiable (§4)** is semantic. `SE001` catches the habit's
  most visible form — a heading named `Validation` — not its substance.
- **Whether named state files suffice to resume (§7)** requires reading them. `WF001` proves only
  that a statement exists.
