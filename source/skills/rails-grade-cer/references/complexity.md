---
name: rails-grade-cer-complexity
metadata:
  version: "1.0"
---

# Complexity Axis

**Measures:** reasoning difficulty and architectural size — trade-offs, ambiguity, decision points, interdependencies. Not volume. A plan can be enormous in file count yet trivial to reason about (a mechanical rename across 5,000 files), or tiny in file count yet reasoning-heavy (a one-file change to a concurrency primitive).

**Reads:** the full plan, including its implementation detail — steps, affected files, decision points, new abstractions, dependencies, and integrations.

## Method

Keep the unit-counting rubric below as the evidence-gathering step. Units are objective and countable directly from the plan text. Once counted, map the unit total onto the shared 0–10 scale using the band table. Units are not the score — they are the evidence that produces it.

### Unit-Counting Rubric

| Element | Units | Count Rule |
| --- | --- | --- |
| Implementation step | 1 | Each discrete action the executing agent must perform |
| Distinct file touched | 1 | Count each file once, even if several steps touch it |
| Decision point or branch | 1 | Each conditional path the executor must reason through |
| New abstraction | 2 | New class, interface, API surface, schema, module, service, or protocol |
| Cross-step dependency | 1 | A step whose correctness depends on an earlier step's output |
| External integration | 2 | New package, service, protocol, remote API, toolchain, or storage contract |

Count directly from what the plan states. If the plan is vague about a category (for example, it does not enumerate affected files), count what is visible and note in the paragraph that missing detail may hide more units than counted.

### Unit-Total → 0–10 Mapping

These bands are **provisional seed values**, not calibrated against real outcomes yet. Use them as the working scale until enough completed plans exist to check whether the bands predict actual difficulty well. Do not treat the specific boundary numbers as load-bearing precision — treat them as a reasonable first cut.

| Units | Score |
| --- | --- |
| 0 | 0 |
| 1–2 | 1 |
| 3–4 | 2 |
| 5–7 | 3 |
| 8–11 | 4 |
| 12–16 | 5 |
| 17–22 | 6 |
| 23–29 | 7 |
| 30–37 | 8 |
| 38–46 | 9 |
| 47+ | 10 (uncapped beyond — forecast) |

Past the top band, do not stop at 10. Estimate how far past the table the unit total sits and report a forecast score with a short note that it is off the chart.

### Scale Anchors

Use these to sanity-check the mapping and to write the paragraph — they describe what a score *feels like*, independent of the raw unit count:

- **0** — trivial. One file, straight implementation, no decisions.
- **5** — moderate. Several files, a few decision points, one or two new abstractions.
- **10** — architectural maze. Dozens of files, heavy interdependencies, multiple decision trees, integrations throughout.
- **>10** — redesigning a core system, codebase-wide refactor, existential trade-offs. Forecast where it lands rather than clamping.

## Writing The Paragraph

State the score, the unit total that produced it, and a short breakdown of what drove the count (e.g. "3 new abstractions, 2 external integrations, 14 steps across 9 files"). If the plan under-specifies scope, say so and note that the true complexity may be higher than what is countable today. Never suggest simplifying, splitting, or restructuring the work — that is prescription, not diagnosis.
