---
name: mermaid-mapper-workflow
description: >-
  Use this orchestration skill when building a Mermaid diagram of a large
  object-oriented codebase from a user-supplied entry point or query. The Boss
  coordinates scout discovery, parallel mapper chunks, validation, aggregation,
  and artifacts under documentation/workflows/mermaid_mapper.
metadata:
  version: "1.1"
  agentic_rails_source_version: "1.1"
---

# Mermaid Mapper Workflow (Boss)

You are the **Boss**: orchestrate end-to-end mapping without stuffing an entire codebase into one context. Delegate discovery and per-file extraction to subagents; keep synthesis, state, and validation here.

This is a workflow-style skill: keep domain behavior in the component skills and
use this file for sequencing, state, artifact paths, and recovery policy.

## Scope

- **Primary**: object-oriented code, especially **C#** (classes, inheritance, composition, constructor injection, type families like `*ViewModel`).
- **Extensible**: other languages later; keep assignments file-and-type-bounded.

## Artifact root (target repository)

All paths are relative to the **target** repository root (the project being mapped, not necessarily this tooling repo):

| Path | Role |
| --- | --- |
| `documentation/workflows/mermaid_mapper/scoutmap.md` | Discovery + durable work queue |
| `documentation/workflows/mermaid_mapper/mermaid.md` | Final aggregated diagram |
| `documentation/workflows/mermaid_mapper/partials/` | One partial per mapper chunk (`partial_0001.md`, …) |
| `documentation/workflows/mermaid_mapper/logs/` | Validation failures, retries, notes |

Create these directories on first run.

## Skills (load these contracts)

| Role | Skill path (from this repo root) |
| --- | --- |
| Scout | `skills/mermaid-scout/SKILL.md` |
| Mapper | `skills/mermaid-mapper/SKILL.md` |
| Validation | `skills/mermaid-validation/SKILL.md` |
| Aggregation | `skills/mermaid-aggregation/SKILL.md` |

Supporting references: `skills/mermaid-scout/references/scoutmap-format.md`, `skills/mermaid-mapper/references/mermaid-conventions.md`, and **state transitions**: [references/state-model.md](references/state-model.md).

## Invocation

The user passes the **target in the message** (no interactive scope prompts). Examples:

- `/mermaid-mapper-workflow ResourceViewModel`
- `/mermaid-mapper-workflow current file`
- `/mermaid-mapper-workflow map RTS resource view models`
- `/mermaid-mapper-workflow map relationships from UnitViewModel`

Resolve that text into concrete discovery instructions for the Scout (paths, globs, type names, feature keywords).

## Model tiers

- **Boss (you)**: use the default capable model for orchestration, recovery, and aggregation.
- **Scout and Mapper subagents**: spawn with `model: "fast"` when using the Task tool.

## Execution loop

1. **Init**  
   Ensure `documentation/workflows/mermaid_mapper/`, `partials/`, and `logs/` exist on the target repo.

2. **Resume check**  
   If `scoutmap.md` already exists and contains rows in progress, continue from persisted state (see [references/state-model.md](references/state-model.md)). Do not wipe partials unless the user asks for a clean run.

3. **Scout**  
   Spawn a **Scout** subagent. Pass the full scout skill intent plus the resolved query and repo root. Scout writes or refreshes `scoutmap.md` with new rows starting at ⬜ per scoutmap format.

4. **Assign**  
   Read `scoutmap.md`. Find rows with ⬜. For each batch you dispatch, set those rows to 🟩 and persist the file.

5. **Map (parallel)**  
   Spawn one or more **Mapper** subagents with assignments: file path + type list per row (or batched rows if tiny). Mappers follow `skills/mermaid-mapper/SKILL.md` and write edge-only partials under `partials/` with stable names.

6. **Validate**  
   For each returned partial, apply **mermaid-validation** checks yourself (read `skills/mermaid-validation/SKILL.md`). Do not spawn a separate validator subagent unless fragments are huge.

7. **State update**  
   - Pass: mark row ❎, keep partial.  
   - Fail: mark row 🟥, append a short entry under `logs/` with reasons.

8. **Refill**  
   Repeat steps 4–7 until no ⬜ rows remain (iterative refill, not only one wave at startup).

9. **Aggregate**  
   Run **mermaid-aggregation** (`skills/mermaid-aggregation/SKILL.md`) over all accepted partials. Write `mermaid.md`.

10. **Done**  
      Tell the user where `mermaid.md` and `scoutmap.md` live.

## Subagent dispatch

Use the **Task** tool for Scout and Mapper work. Each task prompt must include:

- The skill’s required inputs for that step.
- Exact paths on the target repo.
- Output path for partials when mapping.

## Parallelism

The IDE may run several Mapper tasks at once. Cap concurrency only if the user or environment requires it; otherwise keep feeding ⬜ rows until the queue is clear.

## Retry policy (v1)

🟥 is terminal. Optional future: requeue 🟥 → ⬜.

## Standalone components

Users may run **mermaid-mapper** alone on one file, **mermaid-scout** alone for inventory, **mermaid-validation** on a fragment, or **mermaid-aggregation** on saved partials without running this full workflow.
