---
name: mermaid-scout
description: >-
  Use this skill when discovering files and filtering them to specific classes
  or types for a Mermaid relationship map. It writes scoutmap.md as a CSV-like
  work queue for scoped inventory or for the mermaid-mapper workflow.
metadata:
  version: "1.0"
  agentic_rails_source_version: "1.0"
---

# Mermaid Scout

Build a scoped list of files and types to map. Output is always `scoutmap.md` in the workflow output directory when used as part of the mermaid-mapper workflow, or at a path the user specifies for standalone runs.

## When to use

- You need a file-to-type inventory for a feature area, naming family (for example `*ViewModel`), or named type.
- You are running the discovery step before parallel mermaid mapping.
- You want "all relevant view models under X" without drawing the graph yet.

## Inputs

- **Target query**: type name, feature keywords, folder hint, or pattern (for example types ending in `ViewModel`).
- **Repository root**: the project whose code you are mapping.
- **Optional**: folder constraints, glob hints, maximum row count (if the user caps scope).

## Instructions

1. Translate the query into search tactics: `Glob` for paths, `Grep` for symbols and class declarations.
2. Open candidate `.cs` (or other supported) files and list declared types that are in scope.
3. **Include** classes that match the query: naming patterns, explicit names, or clear semantic fit (for example feature-specific view models).
4. **Exclude** unless explicitly targeted: `struct`, `record`, static-only helpers, constants-only types, generic noise, unrelated DTOs or persistence types, and declarations that are clearly out of scope.
5. Group types **by file**: one row per file in the output format.
6. Write `scoutmap.md` using [references/scoutmap-format.md](references/scoutmap-format.md). New rows use the **unassigned** state marker in the first column.

## Output contract

- Destination (workflow): `documentation/workflows/mermaid_mapper/scoutmap.md` under the **target** repository root (always rooted at repo root).
- Format: see [references/scoutmap-format.md](references/scoutmap-format.md).

## Standalone examples

- Find all view model classes under `src/UI/Resources` and write scoutmap.
- Build a scout map for types matching `*Resource*ViewModel` in an RTS UI folder.
- Given "UnitViewModel", locate its file and related unit view models in the same feature area.
