---
name: rails-memory-rebuild
description: Use this skill when explicitly requested to rebuild Rails memory summaries from the complete observation corpus or safely import historical learnings without replacing existing records.
disable-model-invocation: true
argument-hint: "[--memory <path>] [--migrate-legacy] [--dry-run]"
metadata:
  version: "1.1"
---

# Rails Memory Rebuild

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "preview the import".

| Token | Meaning |
| --- | --- |
| `--memory <path>` | Actual memory repository. Absent means discover the configured instance or known workspace instance. |
| `--migrate-legacy` | Add immutable copies of historical session learnings; absent means refuse an incomplete legacy corpus. |
| `--dry-run` | Preview counts and conflicts without writing. Absent means perform the requested rebuild. |
| anything else | Requested memory scope or emphasis. Empty arguments use the established memory instance. |

## Reference

- [Observation schema, migration, and execution](references/observation-contract.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Memory work is optional and explicitly requested. A rebuild does not adopt routing, schedule later work, commit, or curate.
- Quantitative summaries use all relevant immutable observations and historical learnings across new, archived, and golden locations. Golden selection supplies qualitative interpretations only.
- Keep stable observation IDs and shared result IDs. A shared result counts once globally and once in each relevant group, regardless of the number of participants or duplicate copies; group totals overlap.
- Preserve source bytes, historical claims, unknown identities, and unknown telemetry. Requested model selection is distinct from observed runtime identity; imported historical labels are unverified reports.
- Write immutable observation copies and isolated managed summaries. Refuse conflicting IDs, conflicting shared results, unsupported schemas, and replacement of unmanaged output. Never overwrite existing learnings, reports, or historical resumes.
- Advice remains uncalibrated unless a separate evidenced calibration establishes its limits. Session outcomes describe shared results, not individual causal contributions or model superiority.

## Workflow

1. Resolve the actual memory instance and read its repository instructions. Inspect the selected corpus and existing outputs.
2. Consult the reference for the shipped script's invocation and dependency. Run a dry preview to expose conflicts and coverage.
3. Execute the authorized import/rebuild. Resolve any conflict through a new correction observation with evidence; immutable observations remain historical facts about what was recorded.
4. Report record count, unique results, verified identity/telemetry coverage, output location, and source preservation. A later curation may move the learning while its stable observation copy keeps citations resolvable.

## Surviving compaction

The durable state is the memory instance's immutable observation files and managed rebuild summary. Each observation is created exclusively before a summary is replaced. An interrupted summary rebuild can be rerun from those files; no pending curation state is held in conversation.

## Observable output

The rebuild summary contains unique shared-result counts and coverage; every resume source citation resolves to an immutable observation file. Repeating the same rebuild produces the same output bytes and preserves original source bytes.
