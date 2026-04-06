---
name: architecture-and-team-scale
version: 1.0
---

# Architecture and Team Scale

## Use This Reference When

- The task involves system structure, subsystem boundaries, access patterns, or modularity
- You are deciding whether singletons, subsystems, interfaces, inheritance, or composition fit the job
- You need architecture guidance that matches a real game team instead of a software textbook

## Expert Stance

Game architectures are highly interconnected, and central points of access are often the practical answer. Do not force dependency-injection purity everywhere just because software culture says so.

Use architecture to reduce human error. The correct path should feel natural, and the dangerous path should require extra effort. Match modularity to real pressures such as compile time, ownership, platform differences, and team size.

## Core Rules

- Treat singletons, subsystems, and central services as tools, not sins.
- Use interfaces strategically when they help swap platform-specific or backend-specific implementations behind a stable access point.
- Treat inheritance and composition as tools. Use whichever one fits the actual hierarchy and maintenance pressure.
- Fragment projects and modules only when real pressures justify it. Small indie teams can drown in too many modules.
- Build stable conventions, helpers, and guide rails that reduce teammate mistakes.
- Architect for the humans you actually have, not for an imaginary perfect team.

## Practical Heuristics

- If every change requires touching too many disconnected places, the architecture is probably fighting the team.
- If a small team is spending more time maintaining boundaries than building the game, simplify the structure.
- If a backend or platform swap is likely, stabilize the seam with an interface and keep the rest of the code direct.
- If a math-heavy or cognitively dense subsystem blocks teammates, wrap it in clearer logical primitives.

## Common Mistakes

- Forcing heavyweight DI and over-isolation into gameplay code until basic work becomes brittle and annoying
- Fragmenting a small codebase into too many projects because modularity sounds mature
- Declaring inheritance or singletons forbidden on principle rather than judging the real tradeoff
- Designing architecture around ideology instead of shipping pressure and team skill
