---
name: rails-memory-learnings-learning-format
description: Concise Evidence and Provenance.
metadata:
  version: "2.1"
---

# Concise Evidence and Provenance

Honor the actual memory instance's legacy parser fields when required. Keep unknowns honest. New captures also carry observation schema version 1, described below; historical schemas remain unchanged. The narrative can be compact:

```yaml
---
type: session-learning
project: <slug>
date: <YYYY-MM-DD>
session_id: <observed id or unknown>
captured_by: rails-memory-learnings
captured_at: <observed timestamp>
status: new
session_scope: <actual bounded work>
outcome: <succeeded | partial | failed | blocked>
harness: <observed harness or unknown>
harness_version: unknown
models_used:
  - name: <observed model id or unknown>
    requested_name: <requested override or inherited/unknown>
    identity_source: <runtime observation/receipt; unknown if unavailable>
    role: <actual role>
    provider: <observed or unknown>
    reasoning: unknown
    thinking_effort: unknown
    fast_mode: unknown
agents_used: []
token_cost: unknown
usage_evidence: <receipt link, coverage, measured/estimated/unknown>
---
```

When a legacy consumer requires `models_used.name` and `token_cost`, retain them as observed identity and honest usage (unknown if absent). Add provenance as optional extension fields; do not reinterpret an old scalar as a verified bill. Exact receipts distinguish fresh input, cache creation/read, output, reasoning already included in output, and parent/child coverage. No usage telemetry means unknown, not a guessed token estimate.

The body can be short: summary/outcome, observations, relevant model/agent notes only when supported, candidate signals if useful, and evidence reviewed. Required legacy headings can remain concise with `No supported observation` where needed. Capture positive and negative findings proportionately without symmetrical filler.

Label each material statement as directly verified, inferred, user-reported, or unknown. Give inference its basis and limits. One session is a case, not a calibrated ranking or proof of economic benefit. Where a parser demands an old filename convention, preserve compatibility and explicitly record the naming exception; do not bulk rename history.

## Immutable observation block

Add this block to the learning. Replace the example IDs with newly minted UUIDs prefixed
`obs-` and `result-`. Reuse the delivery owner's result ID for one shared outcome reported
by multiple agents. Distinct attempts have distinct result IDs. Curation may move files
without editing bytes; folder location supplies current curation state. A correction is
a new observation with evidence and a link to the original, never an in-place rewrite.

````markdown
<!-- rails-observation -->
```json
{
  "schema_version": 1,
  "observation_id": "obs-8ed1e6de-f2ea-4652-b4ef-8c0f9224fd0d",
  "result_id": "result-9072f523-5448-4ed4-b58a-f4c40f94a1b5",
  "project": "example-project",
  "date": "2026-10-11",
  "task": "Actual bounded work",
  "outcome": "unknown",
  "participants": [
    {
      "role": "implementation",
      "persona": "unknown",
      "requested_model": "unknown",
      "observed_model": "unknown",
      "identity_source": "unknown"
    }
  ],
  "evidence": [{"kind": "unknown", "source": "unknown"}],
  "telemetry": {
    "availability": "unavailable",
    "coverage": "unknown",
    "source": "unknown",
    "tokens": "unknown"
  },
  "interpretations": []
}
```
````

Required values remain present even when unknown. Allowed outcomes are `succeeded`,
`partial`, `failed`, `blocked`, and `unknown`. The shared outcome is not an individual
participant's causal credit. Requested selection is intent; observed model requires
runtime evidence. User-reported labels may be retained as `reported_model`, never
substituted for observed identity. Optional effort/provider/harness fields stay unknown
when absent. Interpretations contain advice separately from observations.

Telemetry availability is `available`, `partial`, `unavailable`, or `unknown`. Numeric
tokens require measured receipt evidence covering the whole result (`coverage: result`),
reconciled across participants. Partial receipts and estimates remain evidence links
with unknown aggregate tokens. Memory capture does not require paid collection tooling.
The optional `rails-memory-rebuild` skill later freezes canonical copies and rebuilds
complete quantitative summaries without changing captures.
