---
name: rails-memory-observation-contract
description: Versioned evidence records and the optional additive rebuild contract.
metadata:
  version: "1.1"
---

# Observation Contract

## Schema version 1

A learning carries this machine-readable block. Stable IDs are kebab-case UUIDs or
hash-based IDs, minted once and never recalculated from a curated filename. Distinct
attempts receive distinct result IDs; participants reporting the same task result reuse
its result ID. `observation_id` identifies a record, while `result_id` identifies the
shared outcome. A correction is a new observation, with a new ID and explicit evidence;
conflicting results are diagnosed rather than silently resolved.

<!-- The example is documentation, not an executable observation. -->
````markdown
<!-- rails-observation -->
```json
{
  "schema_version": 1,
  "observation_id": "obs-8ed1e6de-f2ea-4652-b4ef-8c0f9224fd0d",
  "result_id": "result-9072f523-5448-4ed4-b58a-f4c40f94a1b5",
  "project": "example-project",
  "date": "2026-10-11",
  "task": "Fix Unicode filename display",
  "outcome": "succeeded",
  "participants": [
    {
      "role": "implementation",
      "persona": "unknown",
      "requested_model": "unknown",
      "observed_model": "unknown",
      "identity_source": "unknown"
    }
  ],
  "evidence": [
    {"kind": "verified", "source": "project:context/implementation-plans/unicode/plan.md", "claim": "Relevant checks passed"}
  ],
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

Required fields stay present, including when their values are `unknown`. Evidence
labels distinguish verified observations, inferences, and user reports. The
`interpretations` list is separate selected advice. Optional fields can retain
harness, effort, provider, receipts, supersession links, and provenance limits.
Numeric tokens require telemetry availability `available`, coverage `result`, and a
nonblank string source identifying measured evidence. Unknown/unavailable placeholders,
estimates, and malformed source values cannot support numeric totals. Shared-result
reconciliation retains every known measurement across observations; an intervening
unknown cannot hide disagreement. Partial receipts remain linked evidence with unknown totals.
This script does not reconcile raw response receipts or estimate prices.

## Running the shipped tool

Resolve the script relative to the installed skill directory, not the target project's
working directory. It is shipped as `scripts/rebuild.py` beside this skill's references.
Example commands from the tooling repository root (substitute the actual instance):

```text
python source/skills/rails-memory-rebuild/scripts/rebuild.py <memory-instance> --migrate-legacy --dry-run
python source/skills/rails-memory-rebuild/scripts/rebuild.py <memory-instance> --migrate-legacy
```

New JSON observations use the Python standard library. Historical YAML import requires
PyYAML. Missing dependency or invalid input produces a diagnostic; do not improvise a
lossy parser or invent missing values. Installation remains the host's dependency policy.

All learnings beneath the instance's `memories/learnings/` are scanned, including the
archive. Existing immutable records in `memories/observations/` remain included even if
their narrative learning has moved. Each is cited by its stable filename. A legacy
source uses a SHA-256 ID of its original bytes and an embedded base64 copy of those
bytes. Curation must move those legacy files without editing bytes. Old mutable
`status` fields remain historical capture metadata; folder location expresses current
curation state. New observation records have no mutable curation status.

Imported `result_id` uses project/date/session identity when present, otherwise the
content hash. This is an explicitly inferred compatibility identity. Legacy labels are
`reported_model`, never verified runtime identities. Legacy cost estimates remain in
the preserved original; quantitative usage stays unknown. New records should use the
UUID shared result identifier provided by the delivery owner.

Output is isolated under `memories/resumes-rebuilt/`, with models, agents, and a global
summary. Original `memories/model-resumes/` and `memories/agent-resumes/` remain historical
evidence and cannot be used as inputs to quantitative rebuilding. Output includes a
managed marker; an unmarked file is protected. No timestamp enters deterministic output.
Per-group counts/costs overlap and must never be summed to produce global figures.

Golden learnings select `interpretations` by observation identity, without changing the
statistics. Original legacy prose is preserved as evidence; automatic migration does
not manufacture advice from it. Add a supported interpretation in a new observation
if useful, then curate that narrative separately.

## Failure and recovery

Parsing, identity conflicts, shared outcome/telemetry conflicts, and output ownership
are checked before writes. Observation files use exclusive creation. Summaries replace
one file at a time atomically; an interrupted run may leave a mixed generation of
summaries, so consumers should use the completed summary only after a successful run.
Rerun to converge. Generated files for groups no longer present are not automatically
deleted; use the current summary/output list as the run inventory. This is an optional
artifact pipeline, not a transactional database or a calibrated routing engine.
