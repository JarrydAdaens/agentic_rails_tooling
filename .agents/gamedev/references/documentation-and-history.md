---
name: documentation-and-history
version: 1.0
---

# Documentation and History

## Use This Reference When

- The task touches comments, design notes, markdown docs, commit logs, or knowledge transfer
- You need to preserve trust so future humans or agents can understand whether guidance is current
- A complex subsystem needs intent and rationale captured, not just code changes

## Expert Stance

Reject the myth of self-documenting code.

Games accumulate cognitive complexity in rendering, pathfinding, state flow, save systems, platform hacks, networking, and tools. Comments and external docs are part of the system. Trust matters: stale comments destroy trust, and missing history forces everyone to rediscover the same reasoning.

Commit history is part of the project's memory.

## Core Rules

- Comment class and method intent, tricky behavior, and non-obvious rationale.
- Heavily document cognitively dense systems and ugly platform workarounds.
- Update comments whenever nearby code changes.
- Maintain external docs when they carry important system knowledge, workflows, or design intent.
- Treat commit logs as important archaeological context, not disposable noise.
- Preserve enough context that a future teammate or agent can judge whether the guidance is still trustworthy.

## Practical Heuristics

- If a future reader would ask "why on earth is it like this?" then add the reason nearby.
- If a design tradeoff spans multiple files or systems, capture it in a repo-local document as well as the code.
- If a subsystem is painful to re-learn, document the mental model before more people touch it.
- If a comment is probably stale, fix or remove it immediately.

## Common Mistakes

- Treating comments as optional because the code compiles
- Leaving design knowledge only in one person's head or in chat history
- Writing commit messages that say what changed but not why it mattered
- Allowing stale docs to survive until nobody trusts any docs at all
