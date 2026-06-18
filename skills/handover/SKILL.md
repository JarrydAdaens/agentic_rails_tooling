---
name: handover
description: >-
  Use this skill when the user explicitly asks for a handover, ownership
  transfer, continuation note, shallow handover, or summary artifact after
  agentic work. It reviews conversation context when available, recent git
  history, plan.md, implementation-log.md, and optional thinking.md,
  evidence.md, and complaining.md to produce a grounded shallow handover file.
---

# Handover

Produce a concise ownership-transfer artifact after agentic work.

The default output is a shallow handover. It should be useful to the human now and to a future agent later.

## Artifact

When this skill is active, create or update:

```text
handover/shallow-handover.md
```

Path selection:

1. If the target repository follows Agentic Rails and an active implementation-plan folder is identifiable, write to `handover/shallow-handover.md` under that folder.
2. Otherwise write to `handover/shallow-handover.md` under the target project's context or documentation folder.
3. Load [references/path-selection.md](references/path-selection.md) if the correct location is not obvious.

## Inputs To Review

Use what is available. Missing optional files are not failures.

- Current conversation context, if available.
- Recent git commit or diff information, if available and relevant.
- `plan.md`, when present.
- `implementation-log.md`, when present.
- Optional sibling artifacts: `thinking.md`, `evidence.md`, `complaining.md`.
- Source files, test output, or documentation needed to verify claims.

## Output Shape

Write `shallow-handover.md` with these sections:

```markdown
# Shallow Handover

## Summary

## Scope Covered

## Outcome

## Evidence Reviewed

## Key Decisions

## Risks And Open Questions

## Suggested Next Step
```

## Claim Standard

Label claims honestly:

- Verified: directly supported by source, command output, commit, or artifact.
- Inferred: likely based on available evidence, but not directly proven.
- Assumed: accepted because the task context required it.
- Unknown: not enough evidence.

## Operating Model

1. Identify the target project root and handover path.
2. Review available context and artifacts.
3. Run lightweight source or git inspection if needed to avoid unsupported claims.
4. Write the shallow handover in the selected path.
5. Mention missing optional artifacts only when their absence matters to confidence.
6. Do not create `thinking.md`, `evidence.md`, or `complaining.md` unless those skills are also active.

## Validation

- `handover/shallow-handover.md` exists in the selected path.
- The handover cites the evidence reviewed.
- Claims are labeled when confidence varies.
- Missing optional files are handled gracefully.
