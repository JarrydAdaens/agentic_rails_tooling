---
name: performance-and-hardware-targets
version: 1.0
---

# Performance and Hardware Targets

## Use This Reference When

- The task touches runtime cost, optimization strategy, batching, memory, compression, or hardware budgets
- You need to decide where performance work actually matters
- You need to keep the audience's real hardware in view rather than chasing abstract benchmarks

## Expert Stance

Do not trade readability for premature optimization.

Optimize the big wins, not imaginary ones. Improve the layer that buys real headroom: rendering paths, batching, asset cost, memory behavior, compression, math libraries, or expensive feature design. Start lean so the game runs on weak hardware first, then spend future hardware budget intentionally.

Customer experience is king. We are trying to engineer fun, and that is the king of everything.

## Core Rules

- Measure before optimizing, and optimize where the payoff is real.
- Keep readability unless a proven hotspot justifies extra complexity.
- Favor optimizations with wide payoff: fewer expensive features, better batching, smaller loaded chunks, cheaper assets, and stronger low-level math.
- Understand machine fundamentals: cache behavior, memory layout, loops, branching, compression, GPU uploads, and data packing.
- Optimize for the audience's real hardware, especially older or hand-me-down devices.
- Make weak-hardware support part of the architecture, not a desperate late-stage rescue.

## Practical Heuristics

- If an optimization only saves a few instructions in cold code, ignore it.
- If a content change removes huge runtime cost with acceptable player-facing quality, take the content win.
- If a lower layer can be improved once so that many higher-level systems stay readable, improve the lower layer.
- If the game cannot run comfortably on your weakest supported target, stop adding shiny work and address the budget first.

## Common Mistakes

- Mangling readable gameplay code to save tiny costs nobody measured
- Ignoring batching, asset size, or GPU upload patterns while obsessing over trivial helper methods
- Designing for high-end development hardware instead of the player's actual device
- Treating premature optimization as professionalism instead of misplaced effort
