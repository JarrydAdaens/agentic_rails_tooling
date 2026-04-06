---
name: content-pipeline-and-mgcb
version: 1.0
---

# Content Pipeline and MGCB

## Use This Reference When

- The task touches content projects, MGCB, asset cooking, or `ContentManager`
- You are deciding which assets belong in the runtime content pipeline versus custom loaders
- You need predictable runtime asset formats and naming for a MonoGame or XNA-style project

## Expert Stance

Use a real content pipeline.

MGCB and `ContentManager` are not relics to apologize for. They are valuable because they turn runtime loading into a predictable, cooked-content workflow. Keep source assets, intermediate exports, and shipping content distinct.

## Core Rules

- Keep source authoring assets separate from content-pipeline inputs and built runtime outputs.
- Prefer MGCB or an equivalent cooked-content workflow for textures, audio, fonts, and other standard runtime assets.
- Keep content names stable and intentional so runtime code stays straightforward.
- Avoid raw runtime loading of authoring assets when pipeline cooking would make cost, validation, or portability better.
- Use scoped `ContentManager` ownership when different screens or levels need controlled asset lifetime.
- Document any custom importers, processors, or exceptions to the normal content flow.

## Practical Heuristics

- If an asset format is expensive or inconsistent at runtime, push more work into the build step.
- If a screen or level owns a clear asset set, consider scoped content lifetime instead of one giant always-live manager.
- If a file keeps failing only after deployment, verify pipeline inputs, build actions, and content naming before rewriting code.
- If an asset needs custom loading, make sure the benefit outweighs losing standard pipeline predictability.

## Common Mistakes

- Loading loose authoring assets in production runtime paths because it was convenient during development
- Letting content identifiers drift until runtime paths become fragile and typo-prone
- Treating the content pipeline as optional clutter instead of a runtime protection system
- Mixing ownership of loaded assets until unload behavior becomes hard to reason about
