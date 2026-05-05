---
name: thinking-out-loud
description: >-
  Use this skill when the user explicitly asks for thinking out loud, sanitized
  thinking notes, investigation notes, or a durable thinking.md file during an
  agentic task. It maintains an opt-in project-local thinking artifact that
  captures useful investigation paths, discovered constraints, observations, and
  revisit items without exposing private chain-of-thought.
---

# Thinking Out Loud

Maintain a durable project-local record of sanitized working notes. This skill exists to preserve useful investigation context without turning routine work into a mandatory artifact.

This is not a private chain-of-thought dump.

## Artifact

When this skill is active, ensure a `thinking.md` file exists in the target project.

Path selection:

1. If the target repository follows Agentic Rails and an active implementation-plan folder is identifiable, write `thinking.md` in that folder.
2. Otherwise write `thinking.md` in the target project's documentation folder.
3. Load [references/path-selection.md](references/path-selection.md) if the correct location is not obvious.

Initial content may be:

```markdown
# Thinking Notes

Capture useful engineering notes here. This is not a private chain-of-thought dump.

## Investigation Notes

## Discovered Constraints

## Useful Observations

## Things To Revisit
```

## Operating Model

1. Identify the target project root and artifact path.
2. Ensure `thinking.md` exists before substantive work begins.
3. Work normally, appending concise notes only when they will help a later human or agent.
4. Record source-grounded investigation paths, constraints, observations, and revisit triggers.
5. Keep notes sanitized. Summarize reasoning outcomes and evidence, not hidden chain-of-thought.
6. Preserve existing notes unless the user explicitly asks for cleanup or the agent is correcting its own factual mistake.

## Good Entries

- Investigation: `Documentation/agenticworkflow.md` - found that optional artifacts are skill-gated.
- Constraint: Do not write `thinking.md` unless this skill is active.
- Observation: The implementation plan uses folder-based Tier 4 context, so local artifacts should live beside `plan.md` when possible.
- Revisit: Validate path-selection behavior in a non-Agentic-Rails repository before installing globally.

## Do Not Record

- Private chain-of-thought or step-by-step hidden reasoning.
- Generic status updates that already belong in chat or an implementation log.
- Speculation without a source, decision, or follow-up.
- Routine command output unless it supports a useful observation.

## Validation

- `thinking.md` exists in the selected path.
- The file contains only sanitized, useful notes.
- Optional sibling artifacts such as `complaining.md` or `evidence.md` were referenced only if they exist or are relevant.
