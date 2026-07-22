---
name: evidence
description: >-
  Use this skill when the user explicitly asks for evidence capture, provenance,
  validation evidence, source-grounded proof, or an evidence.md file during an
  agentic task. It maintains an opt-in evidence record — by default the
  `## Evidence / References` section inside the active plan.md, or a standalone
  evidence.md when explicitly requested or genuinely required for audit — that
  indexes changed files, commits, checks, planning inputs, and unverified claims.
disable-model-invocation: false
metadata:
  version: "2.0"
---

# Evidence

Maintain a durable provenance record for implementation work: what proves the work happened and what remains unverified.

This skill is opt-in and should not be created by default for every plan. When it is active, default to writing inline into the active plan, not a standalone file.

## Artifact

**Default: write into `plan.md`.** If the target repository follows Agentic Rails and an active implementation-plan folder is identifiable, record evidence inside that plan's `## Evidence / References` section (see `rails-planning`'s [plan-template.md](../../../source/skills/rails-planning/references/plan-template.md)). Do not create a standalone `evidence.md` for this case.

**Standalone `evidence.md`, only when justified.** Create a separate `evidence.md` file only when:

- the user explicitly asks for a standalone evidence file, or
- the work is high-risk enough, or needs strong enough audit/provenance, that a dedicated file is genuinely warranted (for example, a large or phased story already using standalone sidecar files).

When a standalone file is warranted, it must live beside `plan.md` in the same story folder — `context/implementation-plans/<milestone-slug>/<story-slug>/evidence.md` — never in `context/` root. Load [references/path-selection.md](references/path-selection.md) if the correct location is not obvious.

Content shape, whether inline (as subsections under `## Evidence / References`) or in a standalone file:

```markdown
## Evidence / References

### Source Files Changed

### Commits

### Validation

### Planning Inputs

### Known Unverified Claims
```

## Operating Model

1. Identify the target project root and whether an active plan is identifiable.
2. Default to recording inline in that plan's `## Evidence / References` section. Only fall back to a standalone `evidence.md` per the criteria above.
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

If `thinking.md`, `complaining.md` (or a plan's `## Complaints / Friction` section), or an execution log (`plan.md`'s `## Execution Log` section, or standalone `implementation-log.md`) exists for the same work, use them as inputs when they contain source-grounded evidence. Do not create missing optional artifacts unless their skills are active.

## Validation

- Evidence was recorded inline in `plan.md`'s `## Evidence / References` section unless a standalone `evidence.md` was explicitly requested or genuinely justified.
- Any standalone `evidence.md` lives beside `plan.md` in the same story folder, not in `context/` root.
- Validation entries distinguish passed, failed, blocked, and not-run checks.
- Unverified claims are explicitly labeled.
- Optional sibling artifacts were referenced only when present or active.
