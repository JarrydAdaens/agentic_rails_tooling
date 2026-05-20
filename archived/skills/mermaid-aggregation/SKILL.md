---
name: mermaid-aggregation
description: >-
  Use this skill when merging accepted Mermaid edge fragments into one diagram.
  It deduplicates lines, optionally sorts them, wraps them in graph TD and a
  mermaid code fence, then writes mermaid.md for the workflow or returns the
  block when used standalone.
metadata:
  version: "1.0"
  agentic_rails_source_version: "1.0"
---

# Mermaid aggregation

Combine partial mapper outputs into a single deliverable diagram.

## When to use

- Final step of the mermaid-mapper workflow after all rows are validated.
- Rebuilding `mermaid.md` from archived partials without re-running scout or mapper.
- Merging edge lists from ad-hoc mapper runs into one file.

## Inputs

- **Partials**: paths under `documentation/workflows/mermaid_mapper/partials/` and/or inline edge text from the user.
- **Optional**: sort order (for example alphabetical by left-hand node).

## Instructions

1. Collect every accepted fragment. Strip empty lines and markdown fences if someone pasted fenced content by mistake.
2. Concatenate all edge lines.
3. **Deduplicate**: identical lines count once; treat direction as part of identity (`A --> B` differs from `B --> A`).
4. Optionally sort lines for stable diffs (for example by source node name, then target).
5. Emit one markdown file containing a single fenced block:
   - First line inside the fence: `graph TD`
   - Remaining lines: the edge lines only

## Output contract

- **Workflow**: write `documentation/workflows/mermaid_mapper/mermaid.md` at the **target** repository root.
- **Standalone**: output the same fenced block in chat or write a path the user gave.

## Format reference

Wrapping and default direction match [../mermaid-mapper/references/mermaid-conventions.md](../mermaid-mapper/references/mermaid-conventions.md).

This path assumes `mermaid-aggregation` and `mermaid-mapper` are co-located as siblings under the same `skills/` parent. If deployed standalone, copy the conventions reference locally or load `mermaid-mapper/references/mermaid-conventions.md` from its installed location.

## Standalone examples

- Combine `partial_0001.md` through `partial_0004.md` into one `mermaid.md`.
- Turn this list of edges into a fenced Mermaid block for the README.
