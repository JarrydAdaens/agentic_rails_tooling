---
name: rails-grade-cer-risk
metadata:
  version: "1.0"
---

# Risk Axis

**Measures:** blast radius and recovery cost if the work fails or goes wrong. One number covering all kinds of risk collapsed together — there are no named sub-categories (technical, execution, reputational, etc.) in this design. A single score, judged against a single anchored ladder.

**Reads:** the plan's **goal/intent only**, not its full implementation detail. See the scope boundary below before treating this as an oversight — it is deliberate.

## Method: Model-As-Judge

Act as a judge. Review the goal against the anchored scenario scale below and return a single 0–10 (uncapped) score by finding the closest matching anchor, interpolating between rungs when the goal sits between two scenarios.

Establish the risk level **before** any thought of mitigation. Measuring risk and reducing risk are separate concerns; reducing it is a downstream system's job, not this skill's. Do not let "but this could be mitigated by X" pull the score down — score the risk as if no mitigation exists yet.

### Scale Anchors

| Score | Scenario |
| --- | --- |
| 0 | Cosmetic — updating comments, docs, spelling. Fails silently; working code sits beneath it. Zero blast radius. |
| 1 | Spike — one day lost, code discarded, customers do not notice. Low stakes. |
| 2 | Small bug escapes — a handful of users affected, one-day fix. |
| 3 | Moderate bug — a feature misbehaves, users notice, few-day fix. |
| 4 | Serious bug — a core flow breaks, customers lose money or time, ~week to fix. |
| 5 | Feature miss — the sprint rebalances, agreed deadlines slip, producers get told, but there is capacity to absorb it. Bad but tolerable. |
| 6 | A subsystem is at risk — an outage window is possible, recovery is painful. |
| 7 | Service degradation — revenue impact, regulators watching. |
| 8 | Experimental framework — weeks-to-months of work potentially wasted, nothing recoverable, rollback takes days to a week, a subsystem ships late or gets cut. |
| 9 | Near-total failure — cascading across systems, company in crisis mode. |
| 10 | Catastrophic — e.g. a database migration fails, transactions lock up, customers' mortgages fall overdue, regulators get involved, someone is fired, the business takes real damage. |
| >10 | Systemic catastrophe beyond recovery. Forecast where it lands (e.g. "~1000 — architecting this as one prompt is insane"). |

Note on rungs 7 and 8: rung 7 is customer-facing *harm* (revenue, regulators) and rung 8 is internal *opportunity cost* (wasted effort, nothing recoverable). These are arguably different kinds of risk sitting adjacent on one ladder rather than a strictly ordered progression — 8 is not automatically "worse" than 7 in every situation. The ladder is kept exactly as authored above; when a goal sits ambiguously between these two rungs, judge by whichever scenario description is the closer match and say so in the paragraph rather than trying to force a strict ranking.

## Scope Boundary: Goal-Only, By Design

This axis deliberately reads only the goal/intent of the plan, not the implementation approach. Two consequences follow from that, and both are accepted trade-offs, not oversights:

- Risk introduced by a *bad implementation approach* on an otherwise safe goal is invisible to this axis. A reckless plan to achieve a safe goal will not score higher on Risk than a careful plan to achieve the same goal — Risk here measures what is being attempted, not how well the plan attempts it.
- The goal is also a smaller, cheaper thing to evaluate than the full plan, which keeps this axis fast to run even on large plans.

State this scope boundary in the paragraph whenever it is materially relevant — for example, when the plan's implementation approach looks notably risky even though the goal itself reads as safe. Do not widen the read to implementation detail to compensate; name the boundary instead.

## Identifying The Goal

Locate the goal using the priority order defined in `SKILL.md`: a heading named `Objective`, `Goal`, `Intent`, or `Summary`, in that order, falling back to `Problem Summary` if none of those exist. If no usable goal section exists anywhere in the plan, fall back to reading the whole plan for this axis and state that fallback plainly in the paragraph — do not silently substitute the whole plan without flagging it.

## Writing The Paragraph

State the score and the scenario rung it matched (or the interpolation between two rungs). Explain briefly what about the goal produced that match — the nature of the failure mode, who or what is affected, and how hard it would be to recover. If the goal-only read caused something visible in the implementation to be excluded from the score, say so. Never suggest mitigations, safeguards, rollback plans, or gates — name the risk and stop.
