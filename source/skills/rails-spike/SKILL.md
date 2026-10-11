---
name: rails-spike
description: >-
  Use this skill when one unresolved technical question blocks Agentic Rails
  work and a bounded experiment can provide evidence, including an honest
  inconclusive result.
disable-model-invocation: false
argument-hint: "<question> [--attempts N] [--timebox <duration>] [--output <path>]"
metadata:
  version: "2.0"
---

# Rails Spike

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and treat plain-language equivalents as equal to the tokens
("try once for ten minutes" supplies the attempt and time bounds).

| Token | Meaning |
| --- | --- |
| `--attempts N` | Maximum experiment attempts. Absent means one minimal experiment and at most one changed follow-up justified by new evidence. |
| `--timebox <duration>` | User-specified experiment bound. Absent means a bounded question/attempt contract, without inventing an elapsed-time promise. |
| `--output <path>` | Explicit record location. Absent means the active plan's spike section, or an established project research location. |
| anything else | One technical question, error, or source work item. Empty arguments use the established blocking question; investigate before asking if it is still unclear. |

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- State one question, hypotheses, scope, success/inconclusive conditions, and
  attempt/time bounds before experimenting. Follow the [record template](references/spike-record.md).
- Preserve preexisting dirty, staged, and untracked work. Prefer disposable
  scratch space. If touching a production path is necessary, snapshot exact
  current bytes and restore only experiment-owned changes; do not use broad
  checkout/reset/clean operations as cleanup.
- Record observed commands, versions, results, and limitations. Do not run
  commands from an untrusted plan merely because the plan lists them.
- Respect the bound. Evidence can reject a hypothesis or remain inconclusive;
  no forced recommendation, invented certainty, or unbounded retry is required.
- The caller owns any production scope change. Experiments do not authorize
  commits, dependency upgrades, architectural replacement, or paid delegation
  beyond the existing request.

## Procedure

1. Read available evidence first. If it already answers the question, report it
   without an experiment.
2. Record the bounded contract and preservation plan before writing experiment
   code. Use the active plan or explicitly resolved research record, with a
   source tracker link when it owns the work.
3. Run the smallest useful experiment. Diagnose an environment failure before
   treating it as evidence against the implementation hypothesis.
4. Record supported, rejected, or inconclusive findings. Include confidence,
   remaining uncertainty, next useful question, and any production work implied.
5. Restore owned experiment changes from the exact snapshot when required,
   preserve user changes, and return the evidence to the caller.

## Surviving compaction

The resolved spike record contains the question, bound, original fingerprints or
backup paths, observed attempts, and cleanup state before the next step. Reload
that record and actual file state after interruption; do not restart the same
experiment blindly or assume cleanup completed.

## Observable results

The record names what ran and what it established, even when inconclusive.
Preexisting dirty work is preserved and experiment-owned residue is identified.
