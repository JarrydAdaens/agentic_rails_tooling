---
name: rails-plan-spam-workflow
description: >-
  Use this workflow when the user explicitly requests a bounded near-term batch
  of Agentic Rails implementation plans through delegated planners.
disable-model-invocation: true
argument-hint: "<named planning batch> [--serial|--parallel N] [--limit N] [--resume <run-slug>] [--milestone <slug>] [--template <path>] [--clean]"
metadata:
  version: "4.0"
---

# Rails Plan Spam Workflow

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and treat plain-language equivalents as equal to the tokens
("plan these next three together" means a bounded queue, with coupled work grouped).

| Token | Meaning |
| --- | --- |
| `--serial` | One active planner, the default. |
| `--parallel N` | Explicit planner cap, within runtime capacity and disjoint output ownership. Absent means one. |
| `--limit N` | Maximum plans in the named batch. Absent means the finite explicit batch; never explode an unspecified entire backlog. |
| `--resume <run-slug>` | Continue matching durable run evidence. Absent means discover a clearly requested continuation or create a new collision-free run. |
| `--milestone <slug>` | Existing milestone destination when supplied. Absent means use established project paths; do not invent a milestone just to generate a plan. |
| `--template <path>` | Explicit project-local template. Absent means established project template, then `rails-planning` conventions. |
| `--clean` | Start a fresh owned run after preserving its evidence. Absent means preserve existing outputs and state. |
| anything else | Named near-term work and destination. Empty arguments use an established planning request; otherwise resolve scope before dispatch. |

## References

- [Queue and recovery](references/state-model.md)
- [Questions and decisions](references/questions-file-format.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Generate plans only for the requested near-term batch. Combine tightly coupled
  items when one plan makes execution clearer; preserve named source identifiers.
- Resolve output paths before dispatch. Honor existing project conventions and
  explicit destinations; a milestone is optional. Never overwrite dirty or
  existing plans without an authorized revision that preserves prior content.
- Each planner owns its output files and receives scope, accepted decisions,
  source links, template, dependencies, and stop conditions. Planners share the
  codebase and preserve each other's edits.
- Invoke `rails-planning` by name. Numerical grading, dedicated personas, and
  independent review are optional unless applicable user/project requirements
  select them. Use syntax/link checks and concrete plan coverage first.
- Choose one queue/status owner. Link external tracker items rather than writing
  a second backlog. A questions overview links authoritative questions; it does
  not duplicate mutable answers.
- Record artifact identity and acceptance before selecting the next item.
  Resume checks existing outputs and pending workers before regenerating anything.
  Do not commit or execute production work as part of planning without authority.
- Respect the declared concurrency and run bounds. Repeated failure without new
  evidence records a blocker; it does not trigger unbounded paid revision cycles.

## Procedure

1. Read named sources and target instructions. Identify the finite batch, source
   status owner, dependencies, and output paths. A routine request needs no
   invented milestone or empty ceremony.
2. Record the batch and contracts in an existing plan/tracker record or, where
   needed, `context/implementation-plans/_planning-runs/<run-slug>/briefing.md`
   relative to the target root. Preserve existing legacy run paths on continuation.
3. Dispatch bounded planners with disjoint ownership. Use runtime model/effort
   inheritance unless the user authorized an available override.
4. Inspect output paths, concrete steps, acceptance checks, decisions, and
   uncertainty. Run relevant deterministic checks. Select one independent review
   only for a consequential planning boundary or an adopted requirement.
5. Record accepted plan identity and source link through the chosen owner.
   Aggregate question links only when useful; investigate discoverable facts
   before asking the user for noninferable decisions.
6. End when the named batch/budget is exhausted, with accepted paths, blocked
   items, checks, and open questions. Existing product work stays preserved.

## Surviving compaction

The source queue owner, run briefing when needed, and each accepted plan hold
durable state. Write dispatch ownership and accepted output digests before the
next step. On continuation read the recorded paths and actual Git/diff state;
skip an accepted unchanged plan, reconcile a pending output, and investigate a
changed source/template before revising affected plans.

## Observable outputs

The number and scope of plans match the explicit batch. Existing dirty plans
remain recoverable, accepted outputs have evidence identities, and the source
tracker is linked without a parallel status inventory.
