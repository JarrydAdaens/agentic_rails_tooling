---
name: mermaid-mapper
description: >-
  Use this skill when converting a bounded source file or type list into
  Mermaid relationship edges for inheritance, composition, dependencies, and
  constructor-injected collaborators. Use standalone for one file/class or as a
  worker chunk in the mermaid-mapper workflow.
metadata:
  version: "1.0"
---

# Mermaid Mapper

Extract structural relationships from source into Mermaid-compatible edges. Follow [references/mermaid-conventions.md](references/mermaid-conventions.md).

## When to use

- "Make a Mermaid chart for this file" or the **current file**.
- Map one named class or a small explicit set of types.
- Workflow Boss assigned this file and type list as one scoutmap row.

## Inputs

- **File path** (absolute or repo-relative) to the compilation unit.
- **Types to map**: explicit list, or "all non-excluded classes in this file" when the user wants the whole file and scope is clear.
- **Optional**: inventory of known type names (for example from scoutmap) to judge cross-file references plausibly.

## Instructions

1. Read the file. Inspect only the requested types (or the agreed in-file scope).
2. For each mapped type, extract relationships that matter for architecture:
   - **Inheritance**: base class (use `--|>`).
   - **Composition / dependency**: references to other mapped or noteworthy types via fields, properties, constructor parameters (use `-->`).
3. **Do not** emit edges for primitives, `string`, framework-only types, or trivial constants.
4. **Omit** records and structs unless the user or assignment explicitly included them.
5. **Collections**: emit an edge only when the element type is itself a mapped or explicitly relevant type.
6. Prefer facts visible in declarations; do not infer hidden runtime dependencies.

## Output contract

- Return **only** edge lines, one per line, using the syntax in [references/mermaid-conventions.md](references/mermaid-conventions.md).
- No `graph TD`, no markdown fences, no explanatory text.
- Optional deterministic subgraphs only if explicitly allowed and unambiguous from the file.

## Workflow partial files

When running as a workflow worker, write the same edge-only content to the partial path the Boss specifies (for example `documentation/workflows/mermaid_mapper/partials/partial_0001.md`).

## Standalone examples

- Map `ResourceViewModel` and types it references in `ResourceViewModels.cs`.
- Map every in-scope class in the current buffer's file for a quick diagram.
- Map relationships starting from `UnitViewModel` only.
