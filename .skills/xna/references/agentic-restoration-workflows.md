---
name: agentic-restoration-workflows
version: 1.0
---

# Agentic Restoration Workflows

## Use This Reference When

- The task involves restoring, upgrading, or extending an older MonoGame or XNA project with agent help
- You need to turn domain familiarity into parallelizable, reviewable work packets
- The project is serving as both real game work and a proving ground for agentic engineering workflows

## Expert Stance

Old indie game projects are an excellent agentic testbed because the domain knowledge is deep and the intended outcomes are often clear.

The human expert should stay focused on architecture, intent, taste, and review, while agents take on scoped implementation, migration, cleanup, and validation work. The leverage comes from decomposing the work cleanly and preserving a strong review loop.

## Core Rules

- Separate architectural intent from mechanical execution before assigning work.
- Keep restoration, upgrade, and feature work in small slices with clear acceptance criteria.
- Prefer one subsystem boundary per work packet when possible.
- Preserve enough documentation and commit-worthy history that the reasoning survives across sessions.
- Use familiar project knowledge as leverage, not as an excuse to skip verification.
- Validate each slice before piling on the next one.

## Practical Heuristics

- If a task spans build restoration, content conversion, UI cleanup, and gameplay changes at once, split it.
- If the success condition cannot be demonstrated quickly, tighten the slice or improve the harness.
- If an agent needs a lot of hidden context to succeed, encode that context into the skill or repo docs.
- If a restored subsystem is stable, use it as a template for the next restoration packet.

## Common Mistakes

- Treating agentic restoration as vague parallel busywork instead of deliberate decomposition
- Letting one task sprawl across too many subsystems at once
- Assuming familiarity with the old codebase removes the need for verification
- Failing to capture what was learned for the next pass or the next agent
