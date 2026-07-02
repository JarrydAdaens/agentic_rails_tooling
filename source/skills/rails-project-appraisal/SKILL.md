---
name: rails-project-appraisal
description: >-
  Use this skill when the user asks for a deep project appraisal, project
  audit, architecture review, viability review, strategic review, or "is this
  project worth continuing?" analysis of an Agentic Rails project. It reads
  repository and context-tier material, validates the codebase by building,
  testing, and (where a UI exists) launching it, inspects git history,
  performs external grounding via web research, and writes a frank,
  evidence-led markdown report under context/reports/ that grades the
  project and recommends a course of action — continue, refine, harden,
  pivot, split, rebuild, freeze, or abandon. Reserved for deep, deliberate
  use on projects that matter, not a lightweight orientation pass, a
  code-execution skill, or a normal planning/implementation workflow.
disable-model-invocation: false
metadata:
  version: "1.0"
---

# Rails Project Appraisal

Produce a serious, evidence-led appraisal of an important Agentic Rails project. The output is one markdown report that helps the human decide whether the project should continue, pivot, harden, split, rebuild, freeze, or be abandoned.

## Model

This skill is deliberately heavyweight — full-repo reading, live validation, git forensics, and web grounding, judged and written by the strongest reasoning available (e.g. Fable 5 or an equivalent top-tier model). Prefer running it on a model capable of holding the whole appraisal in mind at once rather than delegating pieces to weaker subagents. It is not a code-execution skill and not a normal planning or implementation workflow — it reads and judges, and writes exactly one report.

## Activation Criteria

Use this skill when the user asks for a deep project appraisal, project audit, architecture review, viability review, strategic review, or "is this project worth continuing?" analysis of an Agentic Rails project — especially when the project is large, important, expensive, commercial, educational, or strategically significant, and the human wants blunt but grounded judgement (including the possibility of sunk cost, procrastination, legacy drag, trend chasing, over- or under-engineering).

Do not use this skill for small implementation tasks, quick code reviews, bug fixes, refactors, or ordinary planning unless the user explicitly asks for this appraisal report. Use `grade` for a quick decisive letter grade on a single artifact, and `rails-grade-cer` for CER-scoring a plan — this skill is a much larger, project-wide judgement pass that subsumes and exceeds both.

## Output Contract

Write exactly one primary report artifact, using the local date of the execution environment for the filename and a human-readable date (e.g. `2 July 2026`) inside the report:

```text
context/reports/YYYY-MM-DD_project-appraisal-report.md
```

If that path already exists, append a numeric suffix (`-2`, `-3`, ...) rather than overwriting. Create `context/reports/` if it does not exist.

**Read-only outside the report.** Do not modify project source, design files, milestone files, backlog files, implementation plans, or documentation other than the appraisal report itself — the report may *recommend* changes to those files, but must not make them. Builds, tests, restores, and other validation commands are allowed as evidence-gathering side effects only; if one changes a tracked file (a lockfile, a generated file), document that in the report rather than reverting it silently. Never run destructive, deploying, publishing, or credential-requiring commands to validate the project — see [references/context-and-evidence.md](references/context-and-evidence.md) for the exact validation and safety rules.

## Tone

Sober, precise, evidence-led. No cheerleading, no softening of materially important findings. Harsh language is earned only by the evidence — a genuine sunk-cost trap, fantasy planning with no execution, grandiose commercial claims with no credible path, or trend-chasing architecture with no real user value. Otherwise: say the hard thing cleanly, without theatrics.

## High-Level Workflow

1. Read the project's `README.md` as the entry point, then load Agentic Rails context in the order given in [references/context-and-evidence.md](references/context-and-evidence.md) — smallest useful set first, escalating only as needed.
2. Build a selective codebase overview: structure, build/package files, entry points, main source and test folders, CI/CD, and areas referenced by design/milestone/backlog/plan docs or by git churn. Skip generated, vendored, and dependency folders unless directly relevant.
3. Validate the project — build, test, lint/typecheck, launch, and (if it has a UI) screenshot — per the validation and screenshot rules in the reference file. Record every command run and its result; never force a risky or credential-requiring command.
4. Inspect git history for activity pattern, churn, rewrite loops, and alignment between the stated roadmap and actual commits.
5. Perform web research where it materially improves the judgement (commercial viability, competitor landscape, framework/library health, current best practice) and cite sources with access dates.
6. Judge project merit, architecture, maintainability, execution health, and strategic direction using the dimensions, grading scale, and confidence rules in [references/report-template.md](references/report-template.md).
7. Write the report to `context/reports/YYYY-MM-DD_project-appraisal-report.md` using the required structure in the same reference file.
8. Report only — do not implement any of the recommended fixes, pivots, or cuts.

## Hard Rules

- Never edit project source, design, milestone, backlog, plan, or documentation files — only the appraisal report and, if useful, its screenshot evidence folder.
- Never run destructive, deploying, publishing, secret-rotating, or production-data-touching commands to validate a project. If validation needs credentials or infrastructure that aren't available, record the gap — don't force it.
- Never infer build/test health without running the commands, unless validation is genuinely impossible (say why).
- Never let prior effort alone count as merit, treat complexity as merit, or treat commercial ambition as commercial viability.
- Never hide missing evidence, low-confidence judgements, or validation gaps — label them.
- Never let raw Tier-0 dictation override maintained context (`context/design.md`, milestone/backlog docs) without flagging the contradiction.

## Validation

Before considering the skill applied correctly, confirm:

- The report was written to `context/reports/YYYY-MM-DD_project-appraisal-report.md` (or a numeric-suffixed variant), and no other tracked file was edited.
- Every grading row required by [references/report-template.md](references/report-template.md) is present, each with an explicit confidence level (`High`/`Medium`/`Low`/`Unknown`).
- The report states which validation commands ran, which passed/failed, and which could not be run and why.
- The Evidence and Provenance section lists context files read, source areas inspected, commands run (including git), screenshots (if any), and web sources with access dates.
- The verdict (Continue/Refine/Harden/Pivot/Split/Rebuild/Freeze/Archive/Abandon) is stated once, unambiguously, and matches the overall grade and report card.
- No implementation, fix, or file edit was performed outside the report itself.

## Completion Message

Keep it short — the report is the artifact. State: the report path, the overall grade, the recommended decision, the top-line confidence level, and any major validation command that could not be run.
