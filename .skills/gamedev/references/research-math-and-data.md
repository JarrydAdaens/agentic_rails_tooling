---
name: research-math-and-data
version: 1.0
---

# Research, Math, and Data

## Use This Reference When

- The task feels repetitive enough that a known algorithm probably exists
- You are solving coordinate math, deterministic comparisons, interpolation, bit packing, or data representation problems
- The current solution is turning into branch soup and wants a cleaner mathematical answer

## Expert Stance

Research first, code second.

Assume many game-development problems were solved years ago. If a problem feels repeatable, there is probably already an algorithm, mathematical identity, data-packing strategy, or representation that solves it more cleanly than improvisation.

What you want is an algorithm.

## Core Rules

- Do not start coding until you understand the problem space and the likely existing solutions.
- Prefer algorithmic and mathematical solutions over branch-heavy hacks.
- Learn enough fundamentals to recognize when existing work applies: vector math, transforms, interpolation, memory layout, compression, and packing.
- Pack data aggressively when it meaningfully reduces cost or simplifies representation.
- Use known techniques when they fit: flags, bitfields, nibble packing, pairing functions, deterministic comparisons, and SIMD-aware math.
- Wrap hard math in understandable helpers when teammates need clearer logical workflows.

## Practical Heuristics

- If the code keeps growing conditionals for geometric or numeric behavior, stop and look for the real math answer.
- If a state space can be represented as bits, flags, or compact numeric ranges, consider packing it.
- If the solution depends on hand-maintained special cases, look for a transform, lookup structure, or invariant instead.
- If a teammate would misuse the math directly, provide a small API that exposes the safe logical operation instead.

## High-Signal Quotes

- "Do not ever write before doing full research and understanding."
- "What you want is an algorithm."

## Common Mistakes

- Writing tangled conditional logic for problems that have a clean mathematical representation
- Reinventing a format or algorithm that already exists and is well understood
- Avoiding data packing and representation discipline when memory or bandwidth actually matters
- Expecting every teammate to reason directly about complex math without protective abstractions
