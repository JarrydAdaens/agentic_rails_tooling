---
name: architecture-and-boundaries
version: 1.0
---

# Architecture and Boundaries

## Use This Reference When

- Defining how responsibilities should be split across the system
- Deciding where logic belongs and what should stay decoupled
- Describing the shape of the solution without dropping into file-by-file details

## Expert Stance

Replace this section with the architectural stance for the domain.

Describe the major boundaries that matter, the responsibilities each layer should own, and the kinds of coupling that should be avoided.

## Core Rules

- Replace this bullet with the domain's preferred separation of concerns.
- Replace this bullet with a rule for deciding when to add a new component versus extend an existing one.
- Replace this bullet with a rule for keeping interfaces small and ownership clear.
- Replace this bullet with a rule for cross-cutting concerns such as configuration, state, persistence, or messaging.

## Practical Heuristics

- Replace this bullet with a quick test for whether a class, module, or subsystem is taking on too much.
- Replace this bullet with guidance for when composition is better than inheritance or special-case branching.
- Replace this bullet with the preferred approach for dependency flow in this domain.

## Common Mistakes

- Replace this bullet with an example of accidental coupling that should be prevented.
- Replace this bullet with an example of boundary leakage that makes testing or maintenance harder.
