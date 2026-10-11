---
name: rails-milestone-planning
description: Use this skill when the user requests creation or refinement of a delivery milestone; select near-term work by dependencies, acceptance, and explicit uncertainty.
disable-model-invocation: true
argument-hint: "<milestone name or path> [--create|--refine] [--no-rescore]"
metadata:
  version: "3.0"
---

# Rails Milestone Planning

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "reorder this milestone".

| Token | Meaning |
| --- | --- |
| `--create` | Assemble a requested milestone outcome and eligible work. Absent means infer from the named artifact. |
| `--refine` | Revise the named milestone using current evidence. Absent means infer from whether it exists. |
| `--no-rescore` | Preserve existing assessments. Absent means refresh only materially changed optional assessments. |
| anything else | Milestone name/path and requested scope. Empty arguments resolve established session scope and known project files. |

## References

- [Backlog shape and ownership](references/backlog-format.md)
- [Milestone selection structure](references/milestone-selection-template.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Use milestones for deliberately chosen delivery outcomes. Do not invent one for a small change, require milestones in Core, or expand a request into the whole backlog.
- Choose one execution-status owner: existing tracker or adopted milestone. Link related backlog entries, plans, and external issues without keeping competing live ledgers.
- Dependencies precede priority. Name prerequisites, external waits, cycles, acceptance, and ownership; parallel work requires disjoint responsibility. A blocked dependency is not ready work.
- Preserve stable story IDs, historical paths, execution evidence, accepted decisions, and unrelated dirty changes. Defer excess scope with links and reasons rather than silently deleting it.
- Qualitative CER is optional through `rails-grade-cer`. Do not sum ordinal assessments, infer numerical capability thresholds, promote work automatically from a score, or prescribe model overrides.
- Forecast from actual scope and the critical dependency path with assumptions and ranges. Distinguish implementation effort, waiting, and elapsed delivery; unknowns remain unknown.
- Existing session authorization permits requested planning edits without a new sign-off ritual. A consequential unresolved outcome or scope decision remains explicit; no commit or implementation is implied by planning.

## Workflow

1. Read project instructions, selected milestone/outcome, relevant design sections, and related backlog or tracker items. Inspect existing status ownership and current changes.
2. Resolve creation or refinement. Gather only eligible named or near-term candidate work; use the backlog reference for maintained entries.
3. Map prerequisites and order the candidate stories topologically. Identify cycles and unavailable dependencies. Within eligible work use urgency, value, and concrete readiness.
4. Select a coherent outcome and acceptance bar. Keep deferred work linked at its original authoritative location. If a candidate spans multiple outcomes, record the grouping issue and a proposed split rather than creating extra milestones by numerical trigger.
5. Write the milestone using the selection reference, with story links, ownership, dependency graph/table, delivery assumptions, and optional qualitative assessments. Keep existing completed work and IDs intact.
6. Report the artifact path, selected scope, order, blocked dependencies, forecast limits, and any decision needed to finalize a changed outcome.

## Surviving compaction

The selected milestone carries accepted scope, dependencies, source links, deferred work, and next planning step. Write it before beginning another batch. When a tracker owns status, the milestone links that tracker; resume against its current state and current repository files.

## Observable output

The selected milestone describes one accepted or explicitly proposed outcome, real prerequisite ordering, and verifiable acceptance. Deferred items remain discoverable, and no cumulative numerical CER or duplicate status ledger appears.
