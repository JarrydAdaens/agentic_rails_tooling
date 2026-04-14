---
name: tier-4-implementation-plan-template
version: 1.0
---

# Tier 4 Implementation Plan Template

Use this template when no repository-local Tier 4 template was provided.

Tier 4 context means the plan is grounded in concrete implementation reality rather than broad product intent alone.
The plan should name likely files, modules, classes, systems, interfaces, validation surfaces, sequencing, and risks.
If exact files are unknown, name the narrowest credible subsystem and the discovery step needed to confirm it.

## Output contract

Each generated plan should be a markdown file with this structure:

```md
# <PLAN-ID> - <Short Goal Title>

## Goal

State the user-facing or system-facing outcome in one short paragraph.

## Source Context

- Source documents:
- Goal or feature id:
- Requested scope:
- Explicit constraints:

## Tier 4 Context

- Likely files or directories:
- Likely classes, functions, services, screens, or subsystems:
- Existing behaviors to preserve:
- Interfaces, data contracts, or external dependencies involved:
- Known tests, build steps, runtime surfaces, or observability points:

## Scope

### In Scope

- ...

### Out Of Scope

- ...

## Implementation Slices

1. Slice name
   - Why this slice exists
   - Concrete edits expected
   - Dependencies or ordering notes

2. Slice name
   - Why this slice exists
   - Concrete edits expected
   - Dependencies or ordering notes

## Acceptance Criteria

- Observable outcome 1
- Observable outcome 2
- Regression or compatibility guardrail

## Validation

- Tests to add or run
- Manual checks
- Logging, telemetry, or debug checks if relevant

## Risks And Open Questions

- Risk:
- Open question:
```

## Template rules

- Keep the title stable and include the goal id when one exists.
- Do not turn the plan into an essay. Be concrete, not long.
- Do not fake certainty. If a file path or dependency is uncertain, say so directly.
- Do not stop at "update backend" or "adjust UI." Name the likely edit points or the discovery work needed to identify them.
- Keep slices implementation-oriented and ordered.
- Keep validation specific to the likely change surface.
- Preserve explicit user constraints and non-goals.

## Quality bar

A good Tier 4 plan:

- is specific enough that a worker can start implementation without re-deriving the whole system shape
- is honest about unknowns
- separates scope from non-scope
- sequences the work into sensible slices
- includes concrete validation
- avoids vague filler
