---
name: save-data-and-debuggable-formats
version: 1.0
---

# Save Data and Debuggable Formats

## Use This Reference When

- The task touches save files, runtime data persistence, migration, or debugging-friendly storage
- You need to decide how much structure and visibility save data should keep
- You want runtime data that is practical for both shipping and support

## Expert Stance

Use save formats that humans can reason about when something goes wrong.

Shipping runtime data does not need to be crude or opaque. It can be compact, versioned, and still reasonably inspectable. Favor structures that help debugging, support, and future migration without turning runtime persistence into a black box.

## Core Rules

- Version save data intentionally from the start.
- Prefer structures that can be inspected, diffed, or at least decoded with ordinary tooling.
- Separate runtime content assets from mutable player data and save-state concerns.
- Keep save ownership explicit so screens, profiles, worlds, and settings do not trample each other.
- Add debug helpers, exporters, or internal tools when the raw format is not friendly enough on its own.
- Document migration assumptions whenever the format changes.

## Practical Heuristics

- If support would struggle to inspect a broken save, add more structure or better tools.
- If a format needs to be compact but still debuggable, consider containers with readable internals.
- If a save bug would be catastrophic, make the write path and backup behavior more explicit.
- If multiple systems mutate the same file indirectly, clarify ownership before adding more fields.

## Common Mistakes

- Treating save files as opaque blobs until migration or debugging becomes painful
- Mixing mutable save state with static content assumptions
- Changing formats silently and hoping old data still works
- Leaving no developer-side tooling for inspecting live player data
