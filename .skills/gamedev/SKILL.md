---
name: gamedev
description: Use this skill when working on game code or game-adjacent systems where general software advice is not enough. It covers game-code architecture, readability, UI architecture and specialist workflows, performance philosophy, content pipelines, math- and algorithm-driven problem solving, multiplayer and networking discipline, testing strategy, documentation, dependencies, engine-specific expertise, and agentic engineering as a force multiplier. Use it for restoring, upgrading, improving, or designing games and game tools, especially when deciding what game-dev-specific tradeoffs fit the real project.
---

# Game Development Engineering and Production Wisdom

This skill captures a game-dev-first engineering worldview grounded in lived production work, not theory.

The perspective behind it spans solo commercial indie shipping, custom engine and gameplay work, .NET and business software, modern studio leadership, UI specialization, architecture, mentoring, and now agentic engineering as a new multiplier on top of all of that. Treat it as senior production judgment that has survived real projects.

Use it when the task is not just "write code," but "make the right tradeoffs for a game": old codebases, tiny teams, weak hardware, real player constraints, messy content pipelines, evolving gameplay, specialist domains, and systems that need to be understandable by humans first.

Game development is its own discipline. Do not blindly import enterprise software habits into games.

The goal is to help the agent choose techniques that fit the real game, the real team, the real audience, and the real production environment.

## Working Style

Start by identifying what kind of game-development problem is actually being solved. Do not load every reference file up front. Read the smallest relevant set.

Think in this order:

1. What is the user trying to build or fix: gameplay code, runtime systems, UI architecture, content pipeline, save data, networking, tooling, performance, or team/process structure?
2. What constraints define the answer: team size, target hardware, platform, genre, audience, runtime cost, age of the codebase, and which specialist domains are involved?
3. Which layer is the real problem: algorithm and data representation, runtime architecture, asset preparation, UI glue, networking discipline, debugging workflow, or production process?
4. What existing technique, algorithm, format, or engine-native pattern likely already solves this better than improvisation?
5. How can the solution optimize the developer and the player experience before it optimizes tiny machine details?
6. What intent can be separated cleanly from execution so agents can help in parallel without losing architectural control?

Prefer the clearest technique that fits the project. If the project is MonoGame or XNA specific, load the `xna` skill alongside this one rather than forcing framework specifics into this skill.

## Default Gamedev Stance

- Prefer game-dev judgment over imported software fashion.
- Prefer readability over cleverness.
- Prefer architecture that keeps bad implementations hard to write.
- Prefer strong separation between UI, game/business data, and the glue layer that mediates them.
- Prefer research before coding when the problem smells like it has been solved before.
- Prefer algorithms and math over branch soup.
- Prefer specialist ownership over fake generalism when the domain genuinely demands depth.
- Prefer performance wins that matter over premature micro-optimization.
- Prefer cooked content pipelines over loading raw authoring assets at runtime.
- Prefer comments, docs, and commit history that preserve trust.
- Prefer smoke tests and deterministic-system tests over brittle gameplay unit tests.
- Prefer tools and workflows that reduce setup friction and human boredom.
- Prefer player experience and target hardware reality over abstract technical purity.
- Prefer externalizing expert judgment into agents so implementation can scale in parallel.

## Reference Map

Load these references only when they are relevant.

### Code, Architecture, and Intent

- [references/code-philosophy-and-readability.md](references/code-philosophy-and-readability.md)
  Use when the task touches naming, readability, comments, code shape, or the overall engineering philosophy of game code.
- [references/architecture-and-team-scale.md](references/architecture-and-team-scale.md)
  Use when the task involves modularity, subsystem boundaries, singletons, interfaces, inheritance, composition, glue layers, or matching architecture to team scale.
- [references/research-math-and-data.md](references/research-math-and-data.md)
  Use when the solution probably wants an algorithm, data-packing strategy, coordinate transform, or mathematical representation instead of ad hoc branching.
- [references/agentic-engineering-and-delegation.md](references/agentic-engineering-and-delegation.md)
  Use when the task involves externalizing expert knowledge, splitting intent from execution, parallelizing work across agents, or structuring review and guidance loops.

### UI, Specialists, and Collaboration

- [references/ui-architecture-and-iteration.md](references/ui-architecture-and-iteration.md)
  Use when the task touches UI architecture, glue/viewmodel layers, mocks, forced states, componentization, declarative markup, or fast UI iteration.
- [references/specialization-and-engine-expertise.md](references/specialization-and-engine-expertise.md)
  Use when the task needs specialist judgment, engine-specific expertise, or a decision about where generalist work should stop and specialist work should take over.
- [references/networking-and-multiplayer.md](references/networking-and-multiplayer.md)
  Use when the task touches multiplayer, replication, packet classes, late join sync, compression, fragmentation, dead reckoning, or bandwidth-aware illusion management.

### Runtime, Content, and Shipping Reality

- [references/content-pipeline-and-assets.md](references/content-pipeline-and-assets.md)
  Use when the task touches asset preparation, runtime-ready formats, content cooking, asset constraints, or format selection.
- [references/performance-and-hardware-targets.md](references/performance-and-hardware-targets.md)
  Use when the task touches performance, hardware budgets, batching, memory, compression, optimization strategy, or audience hardware constraints.
- [references/save-formats-and-debuggability.md](references/save-formats-and-debuggability.md)
  Use when the task touches save formats, inspectable data, debuggable containers, runtime data organization, or tool leverage through better file structure.

### Workflow, Trust, and Production Discipline

- [references/testing-ui-and-iteration.md](references/testing-ui-and-iteration.md)
  Use when the task touches unit testing, smoke testing, replay systems, UI workflows, previews, mocks, or iteration speed.
- [references/documentation-and-history.md](references/documentation-and-history.md)
  Use when the task touches comments, external docs, design notes, commit logs, onboarding, or preserving trust in project knowledge.
- [references/dependencies-and-tooling.md](references/dependencies-and-tooling.md)
  Use when the task touches external packages, engine/framework cost, experimentation, production discipline, or choosing simpler tools over fashionable ones.

## Load Combinations

Typical combinations:

- General code cleanup: `code-philosophy-and-readability.md` + `architecture-and-team-scale.md`
- Agentic planning and delegation: `agentic-engineering-and-delegation.md` + `documentation-and-history.md`
- UI architecture and workflow: `ui-architecture-and-iteration.md` + `architecture-and-team-scale.md`
- Algorithm-heavy gameplay or systems work: `research-math-and-data.md` + `code-philosophy-and-readability.md`
- Multiplayer or replication work: `networking-and-multiplayer.md` + `research-math-and-data.md` + `performance-and-hardware-targets.md`
- Content-heavy runtime work: `content-pipeline-and-assets.md` + `performance-and-hardware-targets.md`
- Save or serialization work: `save-formats-and-debuggability.md` + `research-math-and-data.md`
- Tooling or package choice: `dependencies-and-tooling.md` + `specialization-and-engine-expertise.md`
- Old-codebase restoration: `architecture-and-team-scale.md` + `documentation-and-history.md` + `dependencies-and-tooling.md`
- Player-performance tradeoffs: `performance-and-hardware-targets.md` + `content-pipeline-and-assets.md`

## Execution Checklist

When using this skill:

1. Identify the real game-development problem before reaching for patterns.
2. Load only the references that match the current domain.
3. Favor clarity, maintainability, and human judgment over clever compression.
4. Protect separation of concerns, especially between UI, state, and glue.
5. Look for existing algorithms, formats, and proven techniques before inventing new ones.
6. Match architecture to the real team, codebase age, shipping pressure, and specialist depth the problem actually needs.
7. Keep the player experience and target hardware in view.
8. Use tests, previews, smoke runs, comments, and history to preserve trust in the result.
9. Separate intent from execution so agentic workflows can scale safely.

## Do Not

- Do not treat game code like generic enterprise line-of-business software.
- Do not import trends without proving they solve the real problem.
- Do not muddy the separation between UI, data, and glue layers.
- Do not assume a broad generalist is the right owner for deep specialist work.
- Do not trade readability for imagined speed wins.
- Do not build branch-heavy hacks when a cleaner algorithm probably exists.
- Do not load raw authoring assets directly in runtime when a pipeline should exist.
- Do not chase coverage numbers as if they prove game quality.
- Do not make production code your personal sandbox for trying cool language features or frameworks.
