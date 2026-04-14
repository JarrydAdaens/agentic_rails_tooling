---
name: dependencies-and-tooling
version: 1.0
---

# Dependencies and Tooling

## Use This Reference When

- The task touches external libraries, packages, engines, frameworks, or tool choice
- You need to evaluate whether a dependency is worth its cost and risk
- You need production discipline around experimentation and language-feature churn

## Expert Stance

Use off-the-shelf standards, not off-the-shelf dependency sprawl.

Every dependency adds complexity, compatibility risk, abandonment risk, exploit risk, and opaque behavior. If the solution is small and well understood, copy the source or implement it in your own library instead of burying core understanding behind packaging.

Production is not your playground.

## Core Rules

- Prefer small, understandable dependencies over sprawling package stacks.
- Adopt external packages only when the cost-benefit is clearly favorable.
- If the solution is small and well understood, consider implementing it locally or copying source with clear provenance.
- Separate experimentation from production code. Learn new ideas in prototypes, side projects, or throwaway branches.
- Do not adopt new language features or frameworks just because they are interesting.
- Understand what a tool or framework gives you and what it costs you, especially in debugging and performance.

## Practical Heuristics

- If a dependency solves a tiny problem but introduces a large surface area, do not add it.
- If a framework hides too much performance or state behavior, assume future debugging will cost more.
- If an older solution is still direct, proven, and fast, keep it in the candidate set.
- If a package cannot be understood well enough to maintain around, treat it as a liability.

## Common Mistakes

- Reaching for NuGet or another package feed before understanding whether the problem is actually small
- Treating novelty as progress and quietly raising the maintenance burden of the project
- Experimenting directly in production code instead of in safe prototypes
- Assuming the value lives in the packaging rather than in the underlying solved problem
