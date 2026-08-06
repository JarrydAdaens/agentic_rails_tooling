---
name: wiki-worker-model-selection-research
description: Sourced research behind the Boss workflow's worker-model tables — the Anthropic and OpenAI model rosters, how each harness sets a subagent's model, and the known limitations.
metadata:
  version: "1.0"
---

# Worker Model Selection — Research

Background for `source/skills/rails-boss-execute-workflow/references/model-selection.md`, which is the operative artifact. This page holds the evidence and citations; the reference holds the rules. When a model roster changes, update both — the reference so agents behave correctly, this page so the next person can see why.

**Researched 3 August 2026.** Everything below is a point-in-time observation about commercial products that change frequently. Treat dates as load-bearing.

## The problem being solved

An orchestration skill dispatches subagents. Left alone, both major harnesses default subagents to **the orchestrator's own model**. That is the worst default for cost: the boss is deliberately run on a capable model precisely because orchestration and reconciliation are the hard part, while the dispatched work is usually a well-specified plan step that a much cheaper model can execute correctly.

Before this change, the workaround was manual — the user typed "use Opus for the subagents" into the prompt on every run. That is a per-session tax on the human, and it is exactly the kind of standing decision a skill should encode.

## Anthropic family — Claude Code

### The roster

| Model | Position |
| --- | --- |
| Claude Fable 5 | Most capable widely released model; most expensive tier |
| Claude Opus 5 | Complex agentic coding and enterprise work |
| Claude Sonnet 5 | Best speed/intelligence balance; near-Opus on coding and agentic work |
| Claude Haiku 4.5 | Fastest and most cost-effective; simple tasks |

Sources: [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview), [pricing](https://platform.claude.com/docs/en/pricing).

Fable's exclusion from automatic selection is a cost decision, not a capability one. It sits above the Opus tier on price, so an orchestrator that reaches for it unprompted is spending the user's budget on a judgment call the user did not make. The rule is: recommend and ask, never dispatch.

### How a subagent's model gets set

Claude Code subagents take a `model` value that accepts an alias (`sonnet`, `opus`, `haiku`, `fable`), a full model ID (`claude-opus-5`, `claude-sonnet-5`), or the literal `inherit`. **Omitting it defaults to `inherit`** — the subagent runs on the main conversation's model. That default is the behavior this work exists to override.

Resolution order, highest priority first ([Create custom subagents](https://code.claude.com/docs/en/sub-agents), [Model configuration](https://code.claude.com/docs/en/model-config)):

1. The `CLAUDE_CODE_SUBAGENT_MODEL` environment variable
2. The per-invocation `model` parameter on the dispatch
3. The subagent definition's `model` frontmatter
4. The main conversation's model

As of Claude Code v2.1.196, setting `CLAUDE_CODE_SUBAGENT_MODEL` to `inherit` behaves the same as leaving it unset, so resolution falls through to the per-invocation parameter.

**Gotcha worth knowing:** the environment variable outranks the per-invocation parameter. A user with `CLAUDE_CODE_SUBAGENT_MODEL` exported globally will silently defeat every per-worker choice an orchestrator makes, with no error. This is the concrete case behind the reference's "verify, then record `inherited (unresolved)`" rule.

The per-invocation `model` parameter is also visible in the Agent tool's own schema, which enumerates `sonnet`, `opus`, `haiku`, and `fable` — with the documented exception that a `fork`-type subagent always inherits the parent model and ignores a `model` override.

## OpenAI family — Codex CLI

### The roster

GPT-5.6 reached Codex at general availability on 9 July 2026 as a three-tier family. Official positioning ([Models](https://learn.chatgpt.com/docs/models)):

| Model | Slug | Positioning |
| --- | --- | --- |
| Sol | `gpt-5.6-sol` | Flagship. Strongest capability for complex coding, computer use, research, and cybersecurity. |
| Terra | `gpt-5.6-terra` | Balanced workhorse. Competitive with GPT-5.5 at lower cost. Favors speed and efficiency over depth — exploration, read-heavy scans, large-file review. Works well for parallel workers returning distilled results to the main agent. |
| Luna | `gpt-5.6-luna` | Fast and affordable. Strong capability at the lowest cost in the family; suited to narrow, repetitive, mechanically checkable work. |

Reasoning effort is a separate axis from model choice: GPT-5.6 supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`. An `ultra` setting additionally fans work out across internal subagents for divisible problems — relevant here because it multiplies spend and so should never be selected automatically.

Third-party reporting gives a cost shape (Sol roughly 2× Terra and 5× Luna on input, with steeper output multipliers) and per-tier effort suggestions — Sol at `xhigh`, Terra at `high`, Luna at `medium` — along with the recommendation to use Luna for subagent delegation and reserve Sol for high-stakes work such as architecture decisions, security reviews, and complex multi-file refactors. Sources: [Codex Knowledge Base](https://codex.danielvaughan.com/2026/07/01/gpt-5-6-sol-terra-luna-codex-cli-model-selection-tiered-reasoning-cache-breakpoints/), [ynaito.dev](https://ynaito.dev/en/writing/codex-gpt-5-6-sol-terra-luna/), [Codextime](https://codexti.me/gpt-5-6). Treat the exact multipliers as indicative; the official pricing page is authoritative.

### How a subagent's model gets set

Codex custom agent files accept `model` and `model_reasoning_effort` alongside other `config.toml` keys such as `sandbox_mode`, `mcp_servers`, and `skills.config`. Documented resolution order is: explicit spawn value → configured default → the parent's value ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)).

The same page's own model guidance for subagents mirrors the tiering used in the reference: `gpt-5.6` for demanding multi-step work needing planning and complex reasoning, `gpt-5.6-terra` for speed-focused exploration and read-heavy scanning, `gpt-5.6-luna` for fast, narrowly-scoped repetitive agents. For effort it recommends `high` for agents tracing complex logic (reviewers, security work) and `medium` as the general default.

### The documented capability may not hold in the shipping CLI

Users have reported since the GPT-5.6 drop that spawned subagents inherit the parent's model and reasoning effort regardless of what was requested, and that the previously available per-spawn model selection no longer works:

- [openai/codex#11795 — "Allow configuring subagent model and reasoning_effort in config"](https://github.com/openai/codex/issues/11795)
- [openai/codex#31814 — "GPT-5.6 Sol cannot specify subagent models, forcing all subagents to also be Sol instances"](https://github.com/openai/codex/issues/31814)
- [OpenAI Developer Community — "Codex cli can no longer spawn subagents with specific models or reasoning"](https://community.openai.com/t/codex-cli-can-no-longer-spawn-subagents-with-specific-models-or-reasoning/1386290)

These are user reports against specific CLI versions, not an official deprecation. The practical consequence for the skill is a design constraint rather than a blocker: a per-worker model override on Codex is **requested, not guaranteed**. The reference therefore requires the Boss to verify the worker's actual model where the harness surfaces it, and to record `inherited (unresolved)` rather than the requested model when the override did not take.

**Worth re-testing** whenever the Codex CLI is upgraded: spawn a labeled Terra worker from a Sol boss and check the worker's reported model. That single check tells you whether the Codex column of the table is live or aspirational on the installed version.

## Why not reuse the CER matrix

`rails-planning-phaser` already carries `references/model-matrix.md`, mapping complexity/effort/risk triples to model tiers. It was deliberately **not** reused as the Boss's difficulty rubric.

That matrix sizes a plan for *phasing* — deciding whether a plan must be fractured and how small the pieces need to be. Its own header states its values are provisional seeds not yet calibrated against real completion outcomes, and that the two skills were introduced together partly to generate the data those thresholds should eventually be checked against. Using uncalibrated phasing thresholds as a predictor of which model can *execute* a story would be borrowing confidence the numbers do not have, and would couple two rulesets that should be free to be recalibrated independently.

The Boss instead classifies execution difficulty directly — how well-specified the step is, its blast radius, whether design judgment is required, and how expensive failure would be. If completion data later shows CER predicts execution success well, merging the two is a legitimate future revision; it should not be assumed up front.

### The collision this creates, and how it is resolved

Documenting the distinction is not enough on its own. A phaser-produced manifest writes a concrete **assigned model** per phase — `qwen-3.6-local`, `haiku`, `claude-opus` — into exactly the artifact a Boss reads when executing that plan. Absent a stated precedence, a Boss could reasonably treat `Assigned Model: qwen-3.6-local` as an instruction and try to dispatch it, in a session that may not be running in that family at all.

The resolution is a precedence rule in the Boss's own reference: a phaser capability tier is read as a **difficulty band**, never as a dispatch target, and the actual model always comes from the family table for the session the Boss is running in. The local tier reads as Routine, the light-cloud tier as Standard, and the uncapped top tier as Hard — or Extreme when the phase is also destructive, security-relevant, or long-horizon.

A cleaner long-term fix would be renaming the phaser's field from "assigned model" to something unambiguously non-executable — "phasing capability tier" — so the artifact never looks like a dispatch instruction in the first place. That is a change to `rails-planning-phaser` and its manifest and phase templates, and is left as follow-up work.

## Design consequences for the skill

1. **Vendor rosters live in exactly one file.** Model names churn; duplicating them across skills guarantees drift. Other orchestration skills point at `rails-boss-execute-workflow/references/model-selection.md`.
2. **Family detection comes from the runtime, not the repository.** The same repository is worked on from Claude Code and Codex on different days. Inferring a family from `AGENTS.md` or from a prior run's artifacts would be wrong roughly as often as it is right.
3. **Unresolved is a first-class outcome.** Two of the three failure paths here — unknown family, override ignored — are entirely plausible in normal use. A run that records `inherited (unresolved)` is correct. A run that reports a clean per-story model assignment it never applied has corrupted its own provenance record, which is worse than not selecting at all.
4. **The top tier is opt-in.** Fable in the Anthropic family, and Codex's `ultra` effort, are both explicit-request-only for the same reason: they are large spending decisions that belong to the user.
