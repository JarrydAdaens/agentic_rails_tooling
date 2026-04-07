---
name: mermaid-validation
version: 1.0
description: >-
  Validates a Mermaid graph fragment for structure, scope, and reference plausibility. Returns pass or fail with reasons. Use before accepting mapper output or when sanity-checking edges manually.
---

# Mermaid validation

Check mapper output before the Boss accepts it or before you merge fragments into a final diagram.

## When to use

- After a mapper returns a partial fragment.
- Before pasting edges into documentation.
- As a gate in the mermaid-mapper workflow (Boss runs these checks inline).

## Inputs

- **Fragment**: the proposed Mermaid body lines (edge lines only).
- **Assigned types**: the set of type names that must be covered (for workflow rows, the types in that scoutmap row).
- **Optional inventory**: full scoutmap or type list from the project for reference checks.

## Structural checks

- Content looks like valid Mermaid graph line syntax (edges with `-->` or `--|>`), not prose.
- No markdown fences, headings, or bullet explanations mixed into the fragment.
- Node identifiers are plausible type-name tokens (no full sentences).

## Scope checks

- Every **assigned** type appears at least once as a node (either side of an edge) unless the file truly contains no relationships; if omitted, fail with reason.
- No invented types that are clearly outside the assignment (unless the user allowed cross-file discovery explicitly).
- Fragment does not assert relationships that contradict obvious facts if the Boss already loaded the file (when verification is possible).

## Reference checks

- Types mentioned as endpoints should exist in the inventory when an inventory was provided, **or** be clearly justified as same-file / visible cross-references.
- Fail or warn (per policy) when an edge names a type that appears nowhere in the codebase and was not in scope.

## Output format

Respond with:

1. **Verdict**: `pass` or `fail`.
2. **Reasons**: if `fail`, a short numbered list of specific problems.
3. Optional **warnings** that do not fail the run (for example plausible but unverified cross-file types).

## Standalone examples

- Validate this fragment against assigned types `{FooViewModel, BarViewModel}`.
- Check these edges against the current scoutmap before aggregation.
