---
name: screens-ui-and-tooling
version: 1.0
---

# Screens, UI, and Tooling

## Use This Reference When

- The task touches screen managers, menus, HUDs, overlays, or UI iteration workflows
- You need to keep screen flow understandable without booting the entire game for every small change
- You need a stronger split between UI visuals, underlying data, and the glue that mediates them
- You want practical tooling around a hand-built XNA or MonoGame UI stack

## Expert Stance

Simple screen stacks are often the right answer in XNA-style games, but UI still needs real architecture.

Keep a clear split between the visuals, the underlying state, and the glue layer that feeds the visuals. What matters is explicit ownership, fast iteration, and enough tooling to inspect UI state without turning every small tweak into a full-game launch. Use debug overlays, isolated harnesses, mock data, and direct screen entry points wherever they reduce friction.

## Core Rules

- Keep screen transitions, modal state, loading state, overlay ownership, and UI glue explicit.
- Do not let screen code turn into a muddy mix of rendering, gameplay state, and ad hoc widget logic.
- Use simple screen-manager patterns if they keep flow understandable.
- Provide isolated entry points, harnesses, or debug paths for UI-heavy work when possible.
- Use mock data and forced states so menus, widgets, and HUD states can be exercised quickly.
- Treat debug overlays and developer-only inspection tools as valuable production support.
- Keep UI iteration optimized for fast human feedback, not architectural elegance contests.

## Practical Heuristics

- If a menu tweak needs a full game session to verify, invest in a direct entry path or harness.
- If you cannot tell whether a UI bug is in drawing code, data state, or the glue between them, the split is too muddy.
- If overlay rules are getting confusing, document and centralize the layer ordering model.
- If a UI widget depends on too much surrounding game state, narrow the required inputs or add a better mock seam.
- If debugging a HUD requires guessing invisible values, add an overlay or diagnostics panel.

## Common Mistakes

- Treating full boot as the default way to inspect every UI change
- Hiding screen ownership behind too many indirection layers
- Letting gameplay state couple directly into draw code because it feels faster in the moment
- Building a UI stack that is theoretically pure but miserable to iterate on
- Forgetting that debug tooling for UI can save huge amounts of human time
