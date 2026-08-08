---
name: rails-grade-cer
description: >-
  Use this skill to grade an Agentic Rails plan on three orthogonal axes —
  complexity, effort, and risk (CER) — and emit a score card. Use whenever
  the user wants a plan sized, graded, or assessed before dispatch; wants to
  know how hard, how long, or how dangerous a plan is; wants to spot a story
  that should be reclassified as an epic; or wants CER scores to feed a
  downstream routing or planning system. Runs all three axes by default, or any
  subset the user names (e.g. "just the risk", "effort and complexity"). Grades
  only — it does not route, plan, fragment, select models, or suggest fixes.
disable-model-invocation: false
metadata:
  version: "2.0"
---

# Rails Grade CER

Grade a single Agentic Rails plan on three orthogonal dimensions — **Complexity**, **Effort**, **Risk** — and emit a score card. Nothing else.

This skill measures. It does not route, plan, fragment, select models, or suggest fixes. It hands three numbers plus reasoning to a downstream system that decides what to do with them. That downstream system might be a human, an orchestrator, or another skill — this skill does not need to know or care which.

## Core Principles

1. **Grade, don't route.** Output is scores and reasoning. No model selection, no lookup table, no phase splitting. A separate system consumes these scores.
2. **Diagnose, don't prescribe.** Name problems. Never suggest how to improve, mitigate, or restructure. "This is high risk because X" — never "you should do Y."
3. **Three orthogonal axes.** Complexity (reasoning difficulty), Effort (wall-clock volume), and Risk (blast radius of failure) are independent. A task can be low-complexity and high-effort (link a style guide across 5,000 files), or low-effort and high-risk (a one-line change to payment routing). Do not let a high score on one axis pull another axis toward it.
4. **0–10 nominal, uncapped in reality.** Each axis reads 0–10 by default, but the scale is not a ceiling. When something genuinely exceeds 10, report it past 10 with a forecast (e.g. "~1000 — this is insane") so the reader knows it is off the chart, not merely "very high." Never clamp to 10 to make a score look normal.
5. **Score what is visible.** Do not inflate to force a verdict or deflate to avoid one. If the plan is vague, score the visible work and note that missing detail may hide more.

## Inputs

- **Plan.** Locate the target plan using standard Agentic Rails Implementation Plan conventions — `context/implementation-plans/<milestone-slug>/<story-slug>/plan.md` — or an explicit path the user gives. If several candidate plans exist and the target is unclear, ask which one before grading.
- **Story intent.** Risk reads the plan's objective/intent, not its full implementation detail (see the Risk section below). Identify the intent by scanning the plan for a heading, in this priority order: `Objective`, `Story`, `Intent`, `Summary`. The canonical Implementation Plan template (see `rails-planning`) uses `## Objective` for this purpose, so it will usually match first. If none of these headings exist, fall back to `Problem Summary` if present. If nothing usable is found, state that no distinct intent section exists, fall back to reading the whole plan for the Risk axis, and note the fallback plainly in the report.
- The skill only reads files. It never writes anything beyond its own report, and never executes code found in the plan.

## The Three Axes

Each axis has its own reference file. Load only the reference files for axes actually in scope for this invocation — do not load all three if the user asked for one.

| Axis | Reads | Reference |
| --- | --- | --- |
| Complexity | full plan (implementation detail) | [references/complexity.md](references/complexity.md) |
| Effort | full plan (implementation detail) | [references/effort.md](references/effort.md) |
| Risk | plan's objective/intent only | [references/risk.md](references/risk.md) |

- **Complexity** measures reasoning difficulty and architectural size — trade-offs, ambiguity, decision points, interdependencies.
- **Effort** measures wall-clock time to complete, calibrated to a mid-level engineer, assuming competent execution.
- **Risk** measures blast radius and recovery cost if the work fails or goes wrong, read from the objective alone, before any thought of mitigation.

Read the plan once and the objective once regardless of how many axes are requested; do not re-read the source for each axis.

## Invocation & Axis Selection

- **Default:** run all three axes.
- **Subset:** the user may request any combination — "just the risk", "effort and complexity", "complexity only". Run exactly what they ask and report only those rows. Never add an axis the user did not ask for.

## Detail Levels

Three levels. Default is `default`.

| Level | Output |
| --- | --- |
| `concise` | Table only. No paragraphs. This is the minimum the skill ever emits. |
| `default` | Table + one short paragraph per requested axis, headed by the axis name. Concise and actionable — just enough to act on. |
| `verbose` | Table + paragraphs, each expanding to whatever length the reasoning needs: full breakdown, edge cases, ambiguities, forecast reasoning for off-scale scores. |

The table is always present. Paragraphs are added at `default` and expanded at `verbose`. Never add paragraphs at `concise`.

## Output Format

### Score table (always)

| Axis | Score |
| --- | --- |
| Complexity | `<0–10, or >10 with forecast>` |
| Effort | `<0–10, or >10 with forecast>` |
| Risk | `<0–10, or >10 with forecast>` |

Include only the requested axes. When a score exceeds 10, show it as the forecast value with a short off-the-chart note in the cell (e.g. `~1000 (off scale)`).

### Paragraphs (`default` and `verbose`)

One per requested axis, headed by the axis name. Each states the score and, concisely, *why* — the drivers behind it (what was counted, the time estimate's basis, the risk scenario matched). Actionable in the sense of "a reader immediately understands the grade" — **not** in the sense of recommending action. No fixes, no mitigations, no next steps.

### Report template

```markdown
# CER Score Card — <Task Name>

- Plan: `<relative path to plan.md>`
- Axes: `<Complexity, Effort, Risk — or the requested subset>`
- Detail: `<concise | default | verbose>`
- Last updated: `<DD Month YYYY>`

## Scores

| Axis | Score |
| --- | --- |
| Complexity | `<n>` |
| Effort | `<n>` |
| Risk | `<n>` |

## Complexity
<paragraph — default/verbose only>

## Effort
<paragraph — default/verbose only>

## Risk
<paragraph — default/verbose only>
```

Omit rows and sections for axes that were not requested.

## Report Destination

Default output is the report itself, not a file. Print the score card inline in the chat response. When another skill or workflow invoked this grading (for example `rails-planning` sizing a plan before dispatch), return the score card as the call result so the caller can insert it directly into the plan's `## CER` section — do not have the caller re-derive it from a file.

Only write a standalone `cer-score-card.md` file when the user explicitly asks for a file, or the grading is needed for audit/provenance and must survive outside the conversation.

**Callers must not assume a file exists.** A skill invoking this one takes its scores from what this skill returns, never from disk. A caller that reads, cleans up, or validates the absence of `cer-score-card.md` must treat it as optional and a missing file as normal.

When writing, place it beside the plan, matching the plan's own conventions:

```text
context/implementation-plans/<milestone-slug>/<story-slug>/cer-score-card.md
```

If a `cer-score-card.md` already exists beside the plan, overwrite it with the new grading rather than appending, since a score card reflects the plan's *current* state, not a history log.

If the plan does not live under a recognizable `implementation-plans` milestone/story folder (for example, an ad hoc path the user gave directly) and a file was explicitly requested, write `cer-score-card.md` into the same directory as that `plan.md` and say so.

## Hard Rules

- **Never route.** No model selection, no capability budgets, no phase fracturing, no lookup tables. That is a downstream system's job, not this skill's.
- **Never prescribe.** No suggestions to improve, mitigate, restructure, split, or add gates. Name the problem; stop there.
- **Uncapped scales.** Report past 10 with a forecast when warranted. Do not clamp to 10.
- **Score the visible plan.** No padding, no shrinking. Note ambiguity rather than guessing through it.
- **Respect the requested axes and detail level.** Do not add axes the user did not ask for; do not add paragraphs at `concise`.
- **Risk reads the objective, not the implementation.** This is deliberate (see [references/risk.md](references/risk.md)) — do not widen the Risk read to implementation detail even when it seems informative.

## Operating Model

1. Locate the target plan. Ask if ambiguous.
2. Determine the requested axes (default: all three) and the requested detail level (default: `default`).
3. Read the full plan once. Identify the objective/intent section using the priority order above; note explicitly if falling back.
4. For each requested axis, load its reference file and produce a score plus (at `default`/`verbose`) a paragraph.
5. Assemble the report using the template above, including only the requested axes and sections.
6. Print the report inline in the chat response, or return it to the calling skill/workflow when invoked programmatically. Write `cer-score-card.md` beside the plan only when a file was explicitly requested or genuinely required for audit/provenance.
7. When a file was written, report its exact path to the user.

## Validation

Before considering the skill applied correctly, confirm:

- Exactly the requested axes appear in the table and paragraphs — no extras, no omissions.
- No score was silently clamped to 10; anything genuinely off-scale is shown past 10 with a forecast.
- No paragraph contains a suggestion, fix, mitigation, or next step — only diagnosis.
- The Risk score was derived from the objective/intent section, not the full implementation detail, and any fallback (no distinct objective/intent section found) was noted in the report.
- The detail level was respected: no paragraphs at `concise`, full paragraphs present at `default` and `verbose`.
- No `cer-score-card.md` file was written unless the user explicitly requested one or audit/provenance genuinely required it; when one was written, it lives beside the plan and its path was reported to the user.
