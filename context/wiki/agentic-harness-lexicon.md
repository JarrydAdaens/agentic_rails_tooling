---
name: agentic-harness-lexicon
description: >-
  The industry-standard vocabulary for the machinery this repo builds around
  agentic IDEs — harnesses, guardrails, gates, verifiers, sensors, and
  advisor/critic patterns — and how each term maps onto this repo's layers.
metadata:
  version: "1.0"
---

# Agentic Harness Lexicon

This repo builds machinery that makes agentic IDE output better: hook-enforced
gates, runtime feedback loops, and multi-model advisory pairings. This page
names that machinery in industry-standard vocabulary, so conversations with
agents, other IDEs, and other agentic engineers use words everyone parses the
same way — and so this repo's own layer names stay honest.

## Umbrella terms

- **Agent harness** (or just **harness**) — the whole apparatus around the
  model: tools, hooks, prompts, sensors, gates, memory. Claude Code is itself
  a harness; this repo extends harnesses.
- **Scaffolding** — the older, more academic synonym for harness machinery.
- **Context engineering** — the discipline of deciding what enters the model's
  context and when; the successor term to "prompt engineering," and the best
  one-phrase description of what Agentic Rails is.
- **AgentOps / LLMOps** — the operational practice around all of it:
  monitoring, evaluation, cost control.

## The three layers of harness machinery

### 1. Enforcement — gates on hooks

Checks that fire at a boundary (commit, task-done) and can *block*.

- **Quality gate** — a pass/fail checkpoint work must clear before it
  proceeds; borrowed from CI/CD (SonarQube popularized it).
- **Advisory vs. enforced** — the load-bearing distinction. Anything in a
  prompt *can* be ignored; a lifecycle hook that denies the call cannot. Also
  phrased **soft vs. hard guardrails**, or in security language,
  **probabilistic vs. deterministic controls**. Prompts, rules, and skills are
  advisory; hooks are enforced.
- **Guardrails** — the general umbrella for constraints on agent behavior
  (OpenAI's Agents SDK and NVIDIA NeMo made it a first-class API concept).
  A guard rail is not a separate artifact category: it is what a rule, skill,
  or verifier becomes when bolted to a hook.
- **Policy-as-code** — encoding the constraints as executable configuration
  rather than prose.
- **Safety interlock** — classical engineering term for a hard block on a
  dangerous action; the machine will not run with the guard open. A hook that
  denies commit until the gate passes is an interlock.

### 2. Grounding — closed-loop feedback while the agent works

Machinery that feeds environment ground truth back into the loop mid-task.

- **Open-loop vs. closed-loop** — an agent building UI blind is open-loop;
  screenshots and UI Automation captures **close the loop**: act, observe,
  correct.
- **Grounding** — anchoring the model in observed environment state instead of
  its own beliefs about that state.
- **Sensor / perception / instrumentation / observability** — the
  data-gathering side (e.g. `wpf-tree-sensor`); robotics and DevOps borrows,
  both idiomatic.
- **Verifier** — the component that decides whether observed output is
  *correct*; currently a prominent term via reinforcement learning with
  verifiable rewards. Classical software testing calls the same role a
  **test oracle**.

**Terminology caution — "eval" vs. "verifier":** to most AI engineers, an
*eval* is an offline, scored test suite measuring model or system quality
across many cases (benchmarks, regression suites, LLM-as-judge rubrics). A
per-task, pass/fail verdict on one change — this repo's
`wpf-visual-quality-gate`, the golden-screenshot check — is a **verifier** or
**acceptance gate**, not an eval in that dominant sense. The word "eval" is
stretching to cover both in casual use, but "verifier" lands more precisely
with other engineers.

### 3. Judgment — multi-model advisory pairings

A second model reviewing, steering, or grading the working model.

- **Actor–critic** (or generator–critic) — the structural name: one model
  produces, another judges. An executor/advisor split is exactly this.
- **Advisor pattern** — Anthropic's name for the specific mechanism of an
  executor consulting a stronger model at decision points.
- **LLM-as-judge** — when the second model's job is grading output.
- **Model routing / cascading / tiered inference** — the cost framing: cheap
  models do volume work, expensive models handle high-leverage moments.
- **Debate / adversarial collaboration** — deliberately antagonistic critics;
  "AI safety via debate" is the research lineage.
- **Heterogeneous ensemble / cross-model verification** — using a critic from
  a different model family, because models from one lineage share
  **correlated errors** (blind spots) that a different lineage breaks.
- **Human-in-the-loop (HITL)** — the human as the final judge in an
  escalation chain.

## The classifying frame

The three layers are the components of a **closed-loop control system**:
sensors (grounding), a controller (judgment), and hard limits (enforcement).
Any new harness artifact can be classified along three axes:

| Axis | Question | Range |
| --- | --- | --- |
| **Timing** | When does it fire? | In-flight (sensor feedback, advisor consults) ↔ at a boundary (pre-commit, pre-done) |
| **Bindingness** | Can the agent ignore it? | Advisory (prompts, rules, skills) ↔ enforced (hooks) |
| **Judge** | Who decides pass/fail? | Deterministic code (lint, hooks) → LLM judge (evaluator personas, advisors) → human (escalation checklists) |

In one sentence: *a harness layers deterministic guardrails on lifecycle hooks
for enforcement, closed-loop verifiers with sensors for grounding, and
actor–critic advisory patterns with model routing for judgment — escalating
from code to LLM judge to human-in-the-loop.*

## Mapping to this repo's layers

The repo's `source/` taxonomy sits mostly on the **bindingness** and **judge**
axes:

| Repo layer | Lexicon role |
| --- | --- |
| `source/rules/` | Advisory context — soft guardrails. |
| `source/skills/` | Advisory procedure — how to do a task. |
| `source/agents/` | Judges and workers — including evaluator and advisor personas. |
| Verifiers (now plugins in `agentic_rails_marketplace`) | Verifiers / acceptance gates — per-task pass/fail checks on a target project. The layer was renamed from `evals/` for exactly the terminology reason above, then extracted to the marketplace repo in July 2026 because verifiers are lifecycle artifacts. |
| Hooks (shipped inside marketplace plugins) | The enforcement delivery mechanism that turns any of the above from advisory into deterministic. Hook-wired artifacts live in `agentic_rails_marketplace`, never in this repo. |
