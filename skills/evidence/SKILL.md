---
name: evidence
description: >-
  Use this skill when the user explicitly asks for evidence capture, provenance,
  validation evidence, source-grounded proof, or an evidence.md file during an
  agentic task. It maintains an opt-in project-local evidence artifact that
  indexes changed files, commits, checks, planning inputs, and unverified claims.
metadata:
  version: "1.0"
---

# Evidence

Maintain a durable project-local provenance index for implementation work.

This skill records what proves the work happened and what remains unverified. It is opt-in and should not be created by default for every plan.

## Artifact

When this skill is active, ensure an `evidence.md` file exists in the target project.

Path selection:

1. If the target repository follows Agentic Rails and an active implementation-plan folder is identifiable, write `evidence.md` in that folder.
2. Otherwise write `evidence.md` in the target project's context or documentation folder.
3. Load [references/path-selection.md](references/path-selection.md) if the correct location is not obvious.

Initial content may be:

```markdown
# Evidence

Use this file as the provenance index for the implementation work.

## Source Files Changed

## Commits

## Validation

## Planning Inputs

## Known Unverified Claims
```

## Operating Model

1. Identify the target project root and artifact path.
2. Ensure `evidence.md` exists before substantive verification work begins.
3. Record changed files with short source-grounded summaries.
4. Record commits when commits exist; use `pending` when work is not committed.
5. Record commands, tests, builds, manual checks, and review passes with pass/fail/blocked/not-run status.
6. Record planning inputs that materially shaped the work.
7. Record important unverified claims instead of presenting them as proven.

## Evidence Standard

Useful evidence is specific and inspectable:

- Link or name the file, command, commit, plan, or manual check.
- Include the result, not just that a check was attempted.
- Mark blocked or skipped validation honestly.
- Separate verified facts from inferred or unverified claims.

## Optional Sibling Artifacts

If `thinking.md`, `complaining.md`, or `implementation-log.md` exists for the same work, use them as inputs when they contain source-grounded evidence. Do not create missing optional artifacts unless their skills are active.

## Validation

- `evidence.md` exists in the selected path.
- Validation entries distinguish passed, failed, blocked, and not-run checks.
- Unverified claims are explicitly labeled.
- Optional sibling artifacts were referenced only when present or active.
