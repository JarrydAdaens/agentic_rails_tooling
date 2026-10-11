---
name: rails-project-appraisal-report-template
description: Assessment and Report Structure.
metadata:
  version: "2.0"
---

# Assessment and Report Structure

Use one primary output in the requested format. This structure describes information, not a required Markdown wrapper. HTML/PDF reports may express it through designed sections/tables; inline output remains inline.

## Dimensions

Assess overall merit, strategic clarity, practical/commercial value where relevant, learning value when requested/material, architecture/contract fitness, maintainability, quality, verification health, execution readiness, risk, and evidence quality. Adapt labels to the artifact. A documentation repository has information architecture and template behavior, not an invented application runtime. Use `N/A` with a reason for irrelevant dimensions; use `unknown` for relevant but unavailable evidence.

If a grade is requested or useful, use S/A/B/C/D/E/F with a concrete rationale. S means exceptional with unusually strong evidence; A strong; B sound with clear issues; C viable but compromised; D weak; E severe concern; F failing in its current form. Complexity and prior investment are not grade bonuses.

Confidence is `high`, `medium`, `low`, or `unknown`, supported by coverage and source quality. Negative findings may have low confidence and must say so.

## Information structure

1. Verdict and decision: concrete recommendation such as continue, refine, harden, pivot, split, rebuild, freeze, archive, or abandon; highest-impact finding and confidence.
2. Assessment table: relevant dimension, assessment/grade, evidence, confidence, and any N/A reason.
3. Findings: concrete trigger/behavior, evidence, impact, uncertainty, and ordered intervention. Distinguish user-set boundaries from proposed changes.
4. Validation: actual commands/results, relevant not-run checks, N/A checks, visual evidence, and side effects.
5. Delivery/history evidence: actual progress, adopted status owner, patterns grounded in commits/artifacts rather than speculation.
6. External grounding when material: authoritative sources with access dates and causal limits.
7. Risk: inherent consequences, approach-specific hazards, verified/proposed safeguards, and residual exposure where relevant.
8. Provenance and limits: files/areas inspected, source/diff identity, excluded scope, missing evidence, requested/observed appraiser identity when available.

Keep evidence adjacent to claims and use links to avoid dumping code or transcripts. Recommendations are reviewable proposals; do not perform them. The report's usefulness depends on answering the user's decision with supported conclusions, not filling every generic heading.

## Output delivery

Use the explicit destination or the project's existing report convention. New file artifacts may use `context/reports/YYYY-MM-DD-project-appraisal.<extension>` relative to target root, with a collision suffix instead of overwriting. Do not create another primary report in a different format unless requested. Separate necessary rendering assets from unrelated project source and report any rendering limitations.
