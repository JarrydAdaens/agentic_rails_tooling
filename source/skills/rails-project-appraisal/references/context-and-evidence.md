---
name: rails-project-appraisal-context-and-evidence
description: Context and Artifact-Specific Evidence.
metadata:
  version: "2.0"
---

# Context and Artifact-Specific Evidence

## Context routing

Read target instructions and entry-point README, then relevant maintained design/contract sections, the current plan if delivery matters, and adopted module instructions. Inspect only selected milestone/backlog/history areas needed for the question. Optional framework manuals do not become universal reads. Raw Dictation matters only for unsynthesized intent or an evidenced contradiction.

Core projects may lack milestone/backlog folders. Plans can use `context/current-plan.md`, standalone substantial-work folders, or adopted milestone/story folders. Follow established links rather than silently migrating paths.

## Checks by artifact

| Artifact | Useful validation |
| --- | --- |
| Documentation, starter, or templates | Metadata/schema, links, generator fixtures, rendered output where layout matters, real adoption example. |
| Skill or plugin | Declared argument/activation contract, ownership boundaries, lint, host-specific behavior/error/recovery tests, scoped trigger cases. |
| Library or CLI | Relevant tests, build/static checks, affected API/command path, compatibility and error handling. |
| Application or UI | Relevant tests/build and affected runtime behavior; UI screenshots when visual behavior is material. |
| Plan or workflow | Dependency readiness, acceptance/check definitions, scope authority, recoverable state, realistic estimates and uncertainty. |
| Service or infrastructure | Config validation, safe isolated checks, recovery evidence; no production mutation. |

Prefer existing README/AGENTS/package/CI commands. Record exactly what ran and whether it passed. `N/A` means the check does not apply; `not run` means relevant evidence is missing. Dependency restoration follows documented methods and does not silently upgrade or alter lockfiles. Log any side effects and preserve preexisting work.

## History and external evidence

Inspect status, selected log/churn, relevant diffs, and unresolved branches only as needed. Summarize contributor patterns without exposing private author data. A stale date alone is not proof of abandonment; use maintenance/adoption evidence.

Use current authoritative external sources for ecosystem, market, or comparison claims when permitted and material. Cite URLs and access dates adjacent to claims; name shallow coverage. Missing private/sibling resources reduce confidence where relevant without blocking independent conclusions.

## Visual and output evidence

For requested HTML, PDF, or another visual report, use the applicable artifact workflow and verify rendering. Screenshots belong to the report's asset folder, e.g. `context/reports/assets/<report-slug>/`, relative to the target root. Artifact presence alone is not visual verification. If rendering is unavailable, preserve the requested source artifact and report that limitation; do not silently substitute a Markdown-only deliverable.
