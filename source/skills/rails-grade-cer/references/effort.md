---
name: rails-grade-cer-effort
metadata:
  version: "1.0"
---

# Effort Axis

**Measures:** wall-clock time to complete, assuming competent execution. Orthogonal to Complexity — a task can be trivial to reason about but huge in volume (mechanically applying one style fix across 5,000 files), or reasoning-heavy but quick to execute (a one-line change to a tricky concurrency primitive).

**Calibrated to a mid-level engineer (SV2).** Someone who owns a feature end-to-end, architects a subsystem, debugs unsupervised, and represents the bulk of engineering work. Sonnet- and GPT-5.5-class models sit here most of the time when doing real implementation work. Not a senior (who would rip through faster), not a junior. The scale answers one question: *how long would this take a competent mid-level engineer, working alone, with no blockers?*

**Reads:** the full plan, including its implementation detail.

## Method

Anti-story-point. Do not assign an abstract point value. Estimate real days/hours of mid-engineer time directly from what the plan describes — number of steps, files, integrations, and any explicit scope signals — then map that estimate onto the scale below.

| Score | Mid-engineer time |
| --- | --- |
| 1 | 10 minutes |
| 2 | 30 minutes |
| 3 | 2 hours |
| 4 | half day |
| 5 | one day |
| 6 | 2–3 days |
| 7 | one week |
| 8 | two weeks |
| 9 | four weeks |
| 10 | six weeks — **hard ceiling** |

## The Hard Ceiling

10 is not just a high score — it is a signal. Six weeks of one engineer's time is the point where the work stops being a task and becomes a program: it blows forecasting accuracy and carries too much execution danger to run as a single unit of work.

Anything that genuinely looks longer than six weeks is reported **past 10 with a forecast** (e.g. "~8 weeks — this is not a task, it needs to be broken down"). Do not try to squeeze a three-month effort onto the 1–10 scale by rounding down to 10. Flag that the estimate itself is off the chart instead.

This skill still does not suggest *how* to break the work down — naming that the estimate is off-scale is diagnosis; recommending a fragmentation strategy is prescription, and prescription belongs to a downstream system, not this one.

## Writing The Paragraph

State the score, the time estimate it maps to, and the basis for the estimate — which parts of the plan drove the duration (e.g. "roughly a day: one new service integration plus test coverage, no unusual unknowns"). If the plan's scope is fuzzy in a way that widens the estimate's range, say so plainly rather than picking an artificially precise number. Never suggest how to shorten, parallelize, or split the work.
