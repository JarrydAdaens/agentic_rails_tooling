---
name: game-loop-timing-and-state
version: 1.0
---

# Game Loop, Timing, and State

## Use This Reference When

- The task touches `Game`, `Update`, `Draw`, `GameTime`, fixed timestep, or frame pacing
- You are deciding where simulation belongs versus where presentation belongs
- The code has timing bugs, hitching, double-updates, or confused state flow

## Expert Stance

Keep simulation in `Update` and rendering in `Draw`.

The XNA and MonoGame model is explicit for a reason. The more clearly simulation, input sampling, interpolation, rendering, and content loading are separated, the easier the game is to reason about and debug.

## Core Rules

- Sample input, advance simulation, timers, and gameplay state in `Update`.
- Render current presentation state in `Draw`.
- Be deliberate about `IsFixedTimeStep`, `TargetElapsedTime`, and how `GameTime` is interpreted across the codebase.
- Keep content loading and heavy setup out of hot rendering paths.
- Make state transitions explicit, especially around pause, loading, menus, cutscenes, and screen changes.
- If interpolation or catch-up behavior exists, document the model clearly.

## Practical Heuristics

- If a bug depends on frame rate, inspect timestep assumptions first.
- If rendering code mutates gameplay state, separate the responsibilities before adding more features.
- If a timer or animation system mixes absolute and frame-delta semantics, unify the model.
- If a screen transition is hard to reason about, make the state machine more explicit rather than more magical.

## Common Mistakes

- Putting gameplay mutations in `Draw` because the data was already there
- Letting different subsystems interpret elapsed time differently
- Hiding timing policy in helper code until frame-pacing bugs become mysterious
- Treating fixed timestep as a checkbox rather than a system-wide behavior choice
