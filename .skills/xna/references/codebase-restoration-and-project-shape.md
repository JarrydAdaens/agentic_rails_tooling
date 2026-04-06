---
name: codebase-restoration-and-project-shape
version: 1.0
---

# Codebase Restoration and Project Shape

## Use This Reference When

- Restoring, reviving, or modernizing an older XNA or MonoGame project
- Deciding what project structure and module boundaries fit a small indie game
- Porting older XNA-era code while preserving the parts that still work well
- Using an older project as a safe, controlled environment for agentic engineering experiments

## Expert Stance

Restore the build and the codebase shape before redesigning the whole architecture.

Older XNA-style games often contain direct patterns that are still appropriate: central game access, screen managers, content-project assumptions, explicit rendering flow, and small project counts. Preserve what keeps the code understandable, then modernize surgically where the codebase actually hurts.

These projects are also useful testbeds for agentic engineering because the domain is familiar, the systems are tangible, and the expert judgment is already well formed. That only works if the restoration path stays staged and reviewable.

## Core Rules

- Get the project building, booting, and loading content before chasing architectural polish.
- Prefer small numbers of projects and modules unless compile times, ownership, or platform pressure justify more fragmentation.
- Preserve stable naming, folder layout, content identifiers, and central access patterns when they still serve the project.
- Replace unavailable APIs or platform seams surgically instead of using a port as an excuse to rewrite the whole game.
- Use partial classes or small platform-specific seams when one conceptual system needs different backend slices.
- Keep restoration work explainable so future contributors know what was preserved and why.
- Break restoration into checkpoints that agents and humans can review confidently.

## Practical Heuristics

- If the project is old but coherent, translate it forward rather than reinventing it.
- If a subsystem only hurts because of a platform dependency, isolate the seam and leave the rest alone.
- If a modernization step forces many unrelated files to change, the step is probably too broad.
- If the game logic is still understandable, avoid architecture cleanup that mainly satisfies taste.
- If an agentic restoration task cannot be reviewed in a small slice, the slice is too big.

## Common Mistakes

- Treating a restoration effort as a license for a full rewrite
- Splitting a small indie project into too many modules because it looks more sophisticated
- Removing direct engine-native patterns that were helping the original code stay simple
- Porting blindly without documenting what changed and what old assumptions still remain
- Turning a familiar old project into an experimental sandbox with no safe checkpoints
