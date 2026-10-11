---
name: rails-boss-execute-model-selection
description: Runtime model selection and identity evidence for Boss workers.
metadata:
  version: "2.0"
---

# Worker model selection

The default worker model and reasoning effort are inherited from the active session. A story's score or a phased plan never implies a model name. Choose a different model only when the user authorizes it for this run or supplies a budget, the host exposes that exact choice, and the work gives a concrete reason to use it.

Before dispatch, inspect the active host's worker controls. Record the requested model and effort separately from the observed worker identity. A successful spawn proves that a request was accepted; it does not prove which model executed it. If the host does not surface observed identity, record `unknown` and do not claim a verified override. If the requested choice is unavailable, inherit; do not silently substitute a different model.

Estimate complexity, effort, and consequences in words. Use those assessments to decide whether to split work, add checks, or request independent review. They are not calibrated capability thresholds and must not be translated into a fixed model roster.

When a phased plan names a legacy model or tier, treat it as historical planning context. Use the phase's objective, acceptance criteria, dependencies, and risk to make a current dispatch decision. Preserve the old name in the record if it matters for provenance, but never pass it to a host without checking availability and authorization.

For each worker, record at least:

| Field | Meaning |
| --- | --- |
| Requested model and effort | Exact override sent, or `inherit` |
| Observed model and effort | Runtime evidence, or `unknown` |
| Reason | Why this worker needed an override, if one was used |
| Telemetry | Source and limits of any usage or cost measurement |

Review total task outcomes before claiming that delegation saved time or money. Usage, cache accounting, worker latency, and coordinator overhead can differ across hosts and sessions.
