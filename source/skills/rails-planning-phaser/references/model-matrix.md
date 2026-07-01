---
name: rails-planning-phaser-model-matrix
metadata:
  version: "1.0"
---

# Model Capability Matrix

A data-backed lookup of models and the CER thresholds each can safely execute, ordered cheapest/most-local first. This skill walks the table top-down and assigns each phase the first (lowest) tier whose thresholds cover all three of that phase's scores.

**Values below are provisional seeds, not yet calibrated against real completion outcomes.** `rails-planning-phaser` and `rails-grade-cer` are being introduced together partly to generate the completion data these thresholds should eventually be checked against. Treat this table as the current working assumption, not settled fact — update it here, in one place, as real thresholds are discovered, without touching the rest of the skill.

| Tier | Model | Threshold (C, E, R) | Role |
| --- | --- | --- | --- |
| 1 | qwen-3.6-local | 5, 5, 5 | Default. Local rig. Always prefer this tier. |
| 2 | haiku (light cloud) | 7, 7, 7 | Minimum remote tier. More intelligence and larger context than tier 1, still cheap. |
| 3 | claude-opus | uncapped — no ceiling | Catch-all for intractable or high-risk work. Covers anything tier 1 and tier 2 cannot, including scores that exceed 10 on any axis. |

## Assignment Rule

A phase is assigned to the **lowest tier that covers all three of its axes**. A phase scoring `(5, 4, 8)` needs a tier whose risk threshold is at least 8 — tier 3 here — even though its complexity and effort would comfortably fit tier 1. One weak axis is enough to force a phase up a tier; there is no averaging across axes.

The tier-1 threshold `(5, 5, 5)` doubles as the phasing target in `rails-planning-phaser`: natural-seam fracturing tries to land every phase inside tier 1 first, and only accepts a higher tier when no legal seam gets a phase under `(5, 5, 5)`.

It is normal and expected for a plan to phase into a mix of tiers — for example, three tier-1 phases and one tier-3 phase because that one phase is inherently high-risk. This skill does not force every phase to the same tier, and does not treat a mixed-tier manifest as a failure.

## Shape Of This Matrix

This matrix currently holds one `(C, E, R)` triple per model tier, not separate per-axis thresholds per model. A model that is strong on risk-heavy work but weak on effort-heavy work is represented by whichever single triple best reflects its overall safe operating envelope, not by axis-specific overrides. If real completion data later shows a model's competence genuinely differs enough per axis to need separate thresholds, that is a future revision to this file — it does not require changing `SKILL.md` or the phasing loop itself.

## Tier 3 Has No Ceiling

Tier 3 exists specifically to absorb work that tier 1 and tier 2 cannot: anything that would otherwise force `rails-planning-phaser` to over-cut a phase just to force a lower number. Because tier 3 has no ceiling, every phase is guaranteed to resolve to some tier — this skill should never reach a state where a phase has no tier that covers it.
