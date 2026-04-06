---
name: ui-architecture-and-iteration
version: 1.0
---

# UI Architecture and Iteration

## Use This Reference When

- The task touches UI architecture, state flow, view models, presenters, bindings, or glue code
- You need mocks, forced states, previews, or harnesses for rapid UI iteration
- The work involves componentization, declarative markup, specialist UI review, or collaboration between programmers and designers

## Expert Stance

UI is a first-class discipline.

It is not decoration. It drives clarity, flow, responsiveness, perceived quality, and player trust. Disrespecting UI can poison the whole experience even when the rest of the game is technically solid.

Always separate the UI layer, the actual game or business data, and the glue layer in between. Trying to shortcut all of this is insane. The split makes debugging tractable because you can reason about whether the fault lives in the UI, the state, or the glue.

## Core Rules

- Always keep a clear split between UI, data/model state, and the glue layer that mediates between them.
- Treat glue layers as real architecture, not accidental boilerplate.
- Build UI so important states can be mocked and forced on demand.
- Do not require long gameplay setup just to inspect a UI state.
- Prefer declarative markup and componentized UI where the tooling and engine permit it.
- Optimize UI workflows for parallel work, reviewability, and low merge pain.
- Treat UI work as specialist work with its own review bar and ownership.

## Practical Heuristics

- If a widget can only be tested by playing for ten minutes, the UI workflow is broken.
- If you cannot tell whether a bug is in the visuals, the state, or the mediator, the separation is too muddy.
- If designers and programmers cannot work safely in parallel, the UI structure needs better components or better authoring tools.
- If a tool chain pushes important UI work into hard-to-merge binary artifacts, treat that as a workflow cost, not a neutral fact.

## High-Signal Quotes

- "You need the user interface, you need the actual game and business data, and you need to put glue in between."
- "Trying to shortcut all of this is insane."
- "You should be able to mock it and force the UI to get in the state that you want and need."
- "What you really, really want is to have a declarative markup language."

## Common Mistakes

- Letting gameplay code reach directly into UI state and bindings until debugging turns into guesswork
- Treating UI as easy filler work for whoever is free
- Building UI without mocks, forced states, or isolated previews
- Accepting painful binary-authoring bottlenecks as if they were harmless
