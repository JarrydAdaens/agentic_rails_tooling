---
name: rails-boss-execute-model-selection
description: Worker-model selection tables for the Boss — how to classify a story's difficulty and map it to a model within the vendor family the session is already running in.
metadata:
  version: "1.0"
---

# Worker Model Selection

The Boss runs on whatever model the session was started with. It does not choose its own model and must never try to switch it. What it does choose is the model each **dispatched worker** runs on.

This file is the single owner of the vendor model rosters used by Agentic Rails orchestration skills. Other skills that need a worker-model roster should point here rather than duplicating one.

> These rosters name specific commercial models and therefore go stale. Treat a name here that the harness does not offer as evidence this file needs updating, not as a reason to invent a substitute. Model names, availability, and effort levels observed as of **3 August 2026** — see `context/wiki/worker-model-selection-research.md` in the tooling repository for sources.

## Step 1 — Resolve the family and the harness

Before selecting anything, establish two facts:

1. **Which model the Boss itself is running on**, and therefore which vendor family the session belongs to.
2. **Whether the harness can actually set a worker's model** on dispatch.

Prefer evidence the runtime gives you: the harness's own model indicator, the dispatch tool's parameters, or a direct statement from the user. Do not infer a family from the repository, from `AGENTS.md`, or from what a previous run did.

If either fact cannot be established, do **not** guess a roster. Fall back to inheritance (Step 4) and say so.

## Step 2 — Classify the story's difficulty

Classify each queued story into one band. Judge the story as an **execution** task — how hard is it to *do*, given the plan in front of you — not as a planning artifact.

| Band | Signals |
| --- | --- |
| **Routine** | Fully specified step. Mechanical or near-mechanical: a rename, a config change, a documented API call, moving a file, applying a stated pattern. Small blast radius, obvious verification, nothing to design. |
| **Standard** | Well-specified plan step with ordinary judgment inside it. A handful of files in one subsystem, a normal feature slice, straightforward tests. The plan says what to build; the worker decides only how. |
| **Hard** | Genuine design judgment, cross-cutting change, unfamiliar subsystem, thin or ambiguous plan, tricky concurrency or state, or a change whose failure is expensive to detect. |
| **Extreme** | Long-horizon autonomous work, a change whose failure is dangerous or hard to reverse (data migration, auth, destructive operations), or a story the user has explicitly flagged as needing maximum capability. |

Two rules that override the band:

- **A mandatory specialist persona does not change the band.** Persona and model are independent choices — pass both.
- **When a story sits between bands, take the higher one.** A retried `BLOCKED` story moves up one band on its retry, because the first attempt is evidence the lower band was insufficient.

This is deliberately *not* the CER matrix from `rails-planning-phaser`. CER scores size a plan for phasing; they are provisional, uncalibrated, and were never validated as a predictor of which model can execute a story. Do not substitute one for the other.

### Precedence over a phased plan's assigned model

A plan produced by `rails-planning-phaser` carries a per-phase **assigned model** in its manifest and phase frontmatter, drawn from that skill's own capability matrix — which names models such as `qwen-3.6-local`. Those names are **capability-tier markers for phasing, not dispatch targets.** They describe how small a phase had to be cut, on a scale seeded before any completion data existed, and they carry no knowledge of which vendor family the current session is running in.

The Boss must never dispatch a worker on a model name read out of a phase manifest. Translate instead:

| Capability tier in the manifest | Read as difficulty band |
| --- | --- |
| The local tier, threshold `(5, 5, 5)` | Routine |
| The light-cloud tier, threshold `(7, 7, 7)` | Standard |
| The uncapped top tier | Hard — or Extreme if the phase is also destructive, security-relevant, or long-horizon |

Then map that band through the tables below, in the session's own family. Record the translation in `briefing.md` when a run executes a phased plan, so the divergence from the manifest's stated model is visible rather than looking like a mistake.

## Step 3 — Map the band to a model

### Anthropic family (Claude Code and compatible harnesses)

| Band | Worker model | Notes |
| --- | --- | --- |
| Routine | Haiku | The default for well-written plans. Most stories in a properly planned milestone land here. |
| Standard | Sonnet | The mid tier. Use when the story needs real judgment but not deep reasoning. |
| Hard | Opus | Design judgment, cross-cutting work, thin plans, expensive failure modes. |
| Extreme | Opus | Stays on Opus. Do **not** auto-escalate past it. |

**Fable is never auto-selected.** It is reserved for explicit user request — "use Fable for the workers", or naming it for a specific story. Its cost is the reason: it is the most expensive tier and the Boss must not spend it on the user's behalf. If the Boss believes a story genuinely warrants Fable, it says so and asks; it does not dispatch one.

### OpenAI family (Codex CLI and compatible harnesses)

| Band | Worker model | Reasoning effort | Notes |
| --- | --- | --- | --- |
| Routine | `gpt-5.6-luna` | `medium` | Narrow, repetitive, mechanically verifiable work. |
| Standard | `gpt-5.6-terra` | `high` | The workhorse tier. Also the right pick for read-heavy exploration workers that return a distilled result. |
| Hard | `gpt-5.6-sol` | `xhigh` | Architecture decisions, security-relevant changes, complex multi-file refactors. |
| Extreme | `gpt-5.6-sol` | `max` | Reserve `max`. Do not use `ultra` unless the user asks for it by name — it fans out internal subagents and multiplies spend. |

Where the harness accepts them, these map to the `model` and `model_reasoning_effort` keys on the dispatched agent.

### Any other family

If the Boss is running on a model outside both rosters (a Gemini, Grok, or local model, or an unrecognized harness), there is no table to consult. Do not translate a band into a guessed model name from a family this file does not cover. Go to Step 4.

## Step 4 — When selection is not possible

Three situations end here: the family is unknown, the harness exposes no per-worker model control, or an override was set and the worker demonstrably ran on something else.

In all three:

1. **Inherit.** Let workers run on whatever the harness gives them — normally the Boss's own model.
2. **Record `inherited (unresolved)`** in the `Model` column of `progress.md` for every affected row. Do not write a model name you did not actually set.
3. **Disclose it** in `briefing.md` and to the user, with the reason.

Never report that model selection happened when it did not. An unresolved run that says so is correct; a run that reports a tidy per-story model assignment it never actually applied is a lie in the provenance record.

### Known harness limitations

On Claude Code, a subagent's `model` defaults to `inherit` when unset, and the `CLAUDE_CODE_SUBAGENT_MODEL` environment variable **outranks the per-invocation model parameter**. A user with that variable exported will silently defeat every per-worker selection, with no error raised. A `fork`-type subagent also always inherits the parent model and ignores an override. In either case the correct record is `inherited (unresolved)`, not the model you asked for.

On Codex CLI, per-subagent `model` and `model_reasoning_effort` are documented as configurable — resolved as explicit spawn value, then configured default, then the parent's value. However, users have reported since the GPT-5.6 release that spawned subagents inherit the parent's model and effort regardless of what was requested. Treat a per-worker override on Codex as **requested, not guaranteed**: check the worker's reported model where the harness surfaces it, and if the override did not take, record `inherited (unresolved)` per the rule above rather than the model you asked for.

## Reporting

The Boss states its model policy to the user before dispatch, in the same breath as parallelism, and again in the final report. Use a concrete form:

```text
Boss model: Fable 5 (session model, unchanged)
Worker models: Haiku ×4 routine, Sonnet ×2 standard, Opus ×1 hard (STORY 1.6 — auth migration)
```

or, when unresolved:

```text
Boss model: GPT-5.6 Sol (session model, unchanged)
Worker models: inherited (unresolved) — this harness did not honor the per-worker model override
```
