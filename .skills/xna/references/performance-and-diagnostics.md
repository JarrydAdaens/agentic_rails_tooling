---
name: performance-and-diagnostics
version: 1.0
---

# Performance and Diagnostics

## Use This Reference When

- The task touches frame time, allocations, hot-path cost, content load spikes, or instrumentation
- You need to find where a MonoGame or XNA project is actually paying for its runtime behavior
- You want to keep the game healthy on weaker hardware while preserving readable code

## Expert Stance

Optimize the expensive truths, not the fashionable myths.

In XNA-style games, common wins often come from batching, asset cost, lifetime management, allocation control, simpler passes, and clearer diagnostics. Keep hot-path behavior visible, especially on older or weaker hardware.

## Core Rules

- Measure frame cost and investigate real hotspots before complicating code.
- Watch allocations in `Update`, `Draw`, and frequently called helpers.
- Treat content loading spikes, render-target churn, and texture uploads as serious suspects.
- Optimize low-level helpers or render paths when they create headroom for the rest of the game to stay readable.
- Add instrumentation that helps track frame timing, content events, and major state transitions.
- Test on weak or representative hardware instead of trusting only the development machine.

## Practical Heuristics

- If a scene hitch appears during first use, inspect asset loading and upload timing before rewriting simulation code.
- If a hot path allocates every frame, remove the churn before reaching for deeper architecture changes.
- If rendering cost is unclear, instrument pass timing or temporarily disable major passes to localize the spike.
- If the game feels fine only on the dev box, the hardware budget is not actually under control.

## Common Mistakes

- Micro-optimizing cold code while ignoring per-frame allocations and batching problems
- Trusting a powerful development PC as proof that runtime cost is acceptable
- Adding diagnostics only after the problem is already painful to reproduce
- Hiding hot-path behavior behind layers that make frame cost harder to see
