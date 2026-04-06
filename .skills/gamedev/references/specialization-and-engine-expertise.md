---
name: specialization-and-engine-expertise
version: 1.0
---

# Specialization and Engine Expertise

## Use This Reference When

- The task may need deep specialist judgment rather than broad generalist effort
- You are choosing whether a problem belongs to a UI, graphics, networking, physics, math, architecture, platform, or engine expert
- You need to reason about engine-specific expertise without wasting time on avoidable reinvention

## Expert Stance

Specialization beats fake generalism.

Broad gameplay engineering is valuable, but deep specialist domains remain real: UI, graphics, networking, physics, mathematics, platform work, architecture, and engine expertise. The right move is often to recognize when the problem needs someone who sees the extra colors in that domain, rather than pretending one smart engineer can do everything equally well.

Engine experts matter because they know what the engine already solves, which patterns are cursed, which official patterns are worth copying, and which fake conveniences create pain later.

## Core Rules

- Identify when a problem has crossed from general engineering into specialist territory.
- Treat engine expertise as its own domain, not just a byproduct of language familiarity.
- Use specialists to prevent wasteful reinvention and bad architectural fights.
- Respect that platform specialization can fragment further inside a single shipping target.
- Keep interfaces and seams practical so specialists can plug deep knowledge into a broader codebase cleanly.
- Do not flatten every problem into "general gameplay" for organizational convenience.

## Practical Heuristics

- If the work touches rendering languages, packet strategy, physics correctness, or platform quirks, assume specialist review is valuable.
- If an engine already has a subsystem pattern, sample, or production-safe convention, learn it before inventing an alternative.
- If a team is arguing architecture in the abstract, check whether an engine expert already knows which patterns become expensive later.
- If a generalist solution keeps creating weird edge cases, the domain may need deeper expertise rather than another patch.

## Common Mistakes

- Assuming graphics, UI, networking, physics, and platform work are all just variations of the same skill set
- Treating engine-specific expertise as optional trivia instead of production leverage
- Starting architectural fights before checking what the engine already wants or forbids
- Handing specialist work to whoever has spare capacity and hoping taste will appear on demand
