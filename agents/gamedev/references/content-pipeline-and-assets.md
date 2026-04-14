---
name: content-pipeline-and-assets
version: 1.0
---

# Content Pipeline and Assets

## Use This Reference When

- The task touches asset preparation, authoring formats, cooked content, or runtime loading
- You need to decide how source art becomes game-ready runtime data
- You are choosing whether to invent a format, reuse a standard, or enforce stricter asset rules

## Expert Stance

Use a real content pipeline. Keep content separated by stage: source art, intermediate exports, and cooked game-ready content.

Do not load raw authoring assets directly at runtime if they should have been preprocessed into cheaper, safer, more predictable formats. Enforce constraints that help the runtime, even when they feel slightly inconvenient during authoring.

## Core Rules

- Separate source assets from intermediate exports and runtime-ready content.
- Prefer pipelines that preprocess textures, geometry, audio, and metadata into predictable runtime formats.
- Research existing formats before inventing new ones.
- Enforce constraints that support runtime performance and consistency, such as size limits, compression formats, or predictable authoring rules.
- Choose the cheapest asset representation that still delivers the player experience.
- Treat content projects and asset cooking steps as important infrastructure, not optional ceremony.

## Practical Heuristics

- If a file is expensive to parse, transform, or validate at runtime, it probably belongs in the pipeline.
- If a standard format solves the problem cleanly, use it before designing a custom one.
- If a lower-fidelity asset is dramatically cheaper and still good enough for the player, choose the cheaper asset.
- If the runtime keeps needing content-specific conditionals, push more logic into asset preparation.

## Common Mistakes

- Loading raw PSDs, high-cost source data, or editor-oriented assets directly in shipping runtime paths
- Inventing custom formats without understanding what existing formats already solve
- Treating asset constraints as "annoying rules" instead of the rails that protect runtime behavior
- Ignoring the value of a proper content pipeline because it feels old-fashioned
