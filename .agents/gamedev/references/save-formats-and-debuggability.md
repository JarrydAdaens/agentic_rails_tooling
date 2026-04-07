---
name: save-formats-and-debuggability
version: 1.0
---

# Save Formats and Debuggability

## Use This Reference When

- The task touches save data, runtime file formats, tooling, or inspection workflows
- You need data structures that are easy to reason about, diff, inspect, and debug
- You are deciding how runtime efficiency and human-friendly tooling should coexist

## Expert Stance

Choose formats that are easy to inspect with ordinary tools.

Lean runtime and good tooling can coexist. Use structures that help both the machine and the humans: easy to diff, easy to debug, and easy to reason about. A zipped container with plain-text internals is often better than a mysterious opaque blob when the tradeoff works for the project.

## Core Rules

- Prefer save and data formats that can be inspected without heroic tooling.
- Keep runtime data lean, but do not make debugging needlessly painful.
- Version formats intentionally so future migration work is possible.
- Separate authoring-facing structure from runtime-facing structure when that improves either side.
- Choose layouts that help debugging, diffing, and repair when something goes wrong.

## Practical Heuristics

- If the format is impossible to inspect quickly, add a debugging-friendly layer or tool.
- If a container format gives both compact packaging and readable internals, prefer it over an opaque custom blob.
- If runtime and tooling needs conflict, look for a staged format strategy instead of forcing one format to serve every audience.
- If a save bug would be painful to diagnose from player reports, add more structure and visibility before shipping.

## Common Mistakes

- Choosing a format solely for runtime neatness and forgetting that humans will need to inspect failures
- Making save data so opaque that migration, debugging, and support become miserable
- Reinventing custom storage layers when simpler container or text-based structures would do
