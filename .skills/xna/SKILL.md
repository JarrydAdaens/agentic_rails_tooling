---
name: xna
description: Use this skill when working on XNA or MonoGame game codebases, especially older indie projects being restored, upgraded, debugged, or extended. It covers Game lifecycle, Update/Draw separation, fixed-timestep behavior, content pipeline and MGCB workflows, SpriteBatch and render targets, UI architecture and forced-state workflows, input and audio services, save data, and performance diagnostics. Use it together with gamedev when you need both game-dev judgment and XNA/MonoGame-specific implementation guidance, especially for reviving old indie games as a controlled testbed for agentic engineering workflows.
---

# XNA and MonoGame Game Engineering

This skill is for practical, production-minded XNA and MonoGame work.

It is aimed at the kinds of codebases that many indie games actually have: explicit `Game` loops, `SpriteBatch` rendering, content projects, screen managers, hand-built save systems, central services, platform-specific slices, and years of accumulated real-world tradeoffs.

It also assumes an important use case: returning to older indie games to restore, upgrade, improve, and extend them while using those codebases as a controlled testbed for agentic engineering workflows.

Prefer straightforward engine-native patterns over framework fashion. Preserve the codebase's useful old-school simplicity unless there is a real reason to replace it.

## Working Style

Start by identifying what kind of XNA or MonoGame problem is being solved. Do not load every reference file up front. Read the smallest relevant set.

Think in this order:

1. What is the task really about: restoration, project bootstrapping, timing, rendering, content build, screen flow, UI glue, input, save data, or performance?
2. Is the codebase pure XNA, modern MonoGame, or a mixed old project carrying forward older patterns?
3. Which boundary owns the problem: the `Game` lifecycle, a content project, a rendering path, a screen manager, a UI glue layer, a platform abstraction, or a debug workflow?
4. What should stay explicit and direct instead of being "cleaned up" into unnecessary abstraction?
5. Which existing subsystem can be improved surgically instead of rewritten?
6. What intent can be separated cleanly from implementation so agents can help restore or extend the project safely?

If the task is really a broader game-development tradeoff rather than an XNA/MonoGame implementation detail, load the `gamedev` skill alongside this one.

## Default XNA Stance

- Prefer explicit `Game` lifecycle flow over hidden framework layers.
- Keep simulation in `Update` and rendering in `Draw`.
- Prefer cooked content pipelines such as MGCB and `ContentManager` over raw runtime asset loading.
- Accept central services and subsystem access patterns when they fit the codebase.
- Preserve old codebase character unless a rewrite buys real value.
- Prefer surgical restoration over fashion-driven modernization.
- Prefer strong separation between UI visuals, state, and the glue layer that drives UI behavior.
- Prefer forced states, mocks, and isolated harnesses for UI iteration.
- Prefer platform-specific slices, partial classes, or small interfaces over sprawling abstraction towers.
- Prefer inspectable save data and debuggable runtime state.
- Prefer low-allocation, weak-hardware-friendly runtime behavior.
- Prefer using these projects as safe places to refine agentic workflows without turning production code into a toy.

## Reference Map

Load these references only when they are relevant.

### Runtime and Project Structure

- [references/codebase-restoration-and-project-shape.md](references/codebase-restoration-and-project-shape.md)
  Use when restoring an older game, porting XNA code to MonoGame, deciding project/module shape, or preserving practical old-codebase patterns.
- [references/game-loop-timing-and-state.md](references/game-loop-timing-and-state.md)
  Use when the task touches `Game`, `Update`, `Draw`, fixed timestep behavior, `GameTime`, simulation ownership, or frame pacing.
- [references/input-audio-and-platform-services.md](references/input-audio-and-platform-services.md)
  Use when the task touches input polling, audio services, platform-specific implementation slices, or service access patterns.

### Content, Rendering, and UI

- [references/content-pipeline-and-mgcb.md](references/content-pipeline-and-mgcb.md)
  Use when the task touches content projects, MGCB, `ContentManager`, asset cooking, content naming, or runtime asset boundaries.
- [references/rendering-spritebatch-and-render-targets.md](references/rendering-spritebatch-and-render-targets.md)
  Use when the task touches `SpriteBatch`, render state, batching, atlases, render targets, effects, GPU uploads, or 2D draw-path cost.
- [references/screens-ui-and-tooling.md](references/screens-ui-and-tooling.md)
  Use when the task touches screen managers, menu flow, HUD work, UI glue layers, forced states, debug overlays, or isolated tooling for UI development.

### Data, Performance, and Workflow

- [references/save-data-and-debuggable-formats.md](references/save-data-and-debuggable-formats.md)
  Use when the task touches save files, runtime data formats, versioning, or human-inspectable storage.
- [references/performance-and-diagnostics.md](references/performance-and-diagnostics.md)
  Use when the task touches frame cost, allocations, content load spikes, batching issues, instrumentation, or weak-hardware diagnostics.
- [references/agentic-restoration-workflows.md](references/agentic-restoration-workflows.md)
  Use when the task involves reviving an old project through staged, reviewable, agent-friendly restoration and extension workflows.

## Load Combinations

Typical combinations:

- Reviving an old project: `codebase-restoration-and-project-shape.md` + `content-pipeline-and-mgcb.md` + `agentic-restoration-workflows.md`
- Game-loop bug or timing cleanup: `game-loop-timing-and-state.md` + `performance-and-diagnostics.md`
- Rendering path work: `rendering-spritebatch-and-render-targets.md` + `performance-and-diagnostics.md`
- Menu, HUD, or UI-glue work: `screens-ui-and-tooling.md` + `input-audio-and-platform-services.md`
- Save-system work: `save-data-and-debuggable-formats.md` + `codebase-restoration-and-project-shape.md`
- Platform-specific input or backend swaps: `input-audio-and-platform-services.md` + `codebase-restoration-and-project-shape.md`
- Content build failures: `content-pipeline-and-mgcb.md` + `performance-and-diagnostics.md`
- Agentic restoration planning: `agentic-restoration-workflows.md` + `codebase-restoration-and-project-shape.md`

## Execution Checklist

When using this skill:

1. Identify the real XNA or MonoGame subsystem before changing code.
2. Keep `Update`, `Draw`, content, rendering, UI glue, and save boundaries explicit.
3. Preserve direct, understandable engine-native patterns unless there is a strong reason to replace them.
4. Use cooked content and stable asset naming instead of raw runtime loading.
5. Make important UI states forceable so menus and HUDs can be validated quickly.
6. Watch allocations, state changes, and hardware budgets in hot paths.
7. Break restoration and upgrade work into reviewable slices so agentic workflows stay safe and useful.
8. Modernize surgically so the restored project stays understandable.

## Do Not

- Do not flatten every old pattern into modern framework fashion just because it looks newer.
- Do not mix simulation and rendering responsibilities casually.
- Do not bypass the content pipeline for convenience if the runtime will pay for it forever.
- Do not let UI behavior couple directly to gameplay state without a clear glue layer.
- Do not hide direct engine behavior behind abstractions that make debugging harder.
- Do not ignore frame allocations, batching, and upload costs in hot paths.
- Do not require full-game startup for every tiny UI or screen iteration when a harness would do.
