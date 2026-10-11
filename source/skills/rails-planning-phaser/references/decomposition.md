---
name: rails-planning-phaser-decomposition
description: Natural-seam decomposition and qualitative assessment guidance.
metadata:
  version: "2.0"
---

# Decomposition guidance

Read the plan's objective, dependencies, implementation steps, acceptance checks,
and current execution state together. A phase is a useful checkpoint with a
verifiable result, not an equal share of effort or a proxy for model capability.

Good seams include an independently usable parser, a tested migration before
consumer adoption, or a compatibility adapter before retiring its predecessor.
Keep a change and the checks needed to trust it in the same phase. Setup belongs
with the first behavior it enables unless it is independently useful.

Assess complexity through the choices and unknowns that require reasoning.
Describe effort through the concrete work and dependencies; preserve uncertainty
instead of promising a duration unsupported by evidence.

Distinguish three kinds of risk:

| Risk | What to record |
| --- | --- |
| Inherent consequences | What failure could affect, before mitigation. |
| Implementation hazards | Specific migration, concurrency, data, or integration failure modes. |
| Residual risk | What remains after the proposed checks and recovery measures. |

Use these assessments to select boundaries and verification. Numerical CER is
available by explicit request through `rails-grade-cer`; record its source and
uncertainty without translating its scores into model names or thresholds.

One coherent unit can be the right answer. Do not keep cutting until a number
falls. Separate stories need their own scope decisions, while a lengthy but
cohesive plan may legitimately have more checkpoints than an arbitrary ceiling.
