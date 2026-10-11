---
name: rails-project-appraisal
description: Use this skill when the user requests a deep evidence-led appraisal of a Rails project or artifact; evaluate its actual type and deliver the requested report format with clear confidence and limits.
disable-model-invocation: true
argument-hint: "[repo or artifact path] [--format <format>] [--output <path>] [--no-web] [--no-run]"
metadata:
  version: "2.0"
---

# Rails Project Appraisal

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "give me an HTML report".

| Token | Meaning |
| --- | --- |
| `--format <format>` | Requested report format, including inline, Markdown, HTML, PDF, or another supported artifact. Absent means use the user's established format; otherwise Markdown. |
| `--output <path>` | Explicit report destination. Absent means the requested location or a collision-free artifact in `context/reports/` relative to the target root. |
| `--no-web` | Skip external research. Absent means use it only where current external evidence materially informs judgment. |
| `--no-run` | Skip executable validation. Absent means run relevant safe checks for the actual artifact type. |
| anything else | Repository, artifact, and appraisal question. Empty arguments use current project and established scope. |

## References

- [Context and artifact-specific evidence](references/context-and-evidence.md)
- [Assessment and report structure](references/report-template.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Respect requested scope, output format, and destination. Produce one primary appraisal artifact plus only necessary rendered assets; do not force an extra Markdown report when another format was requested.
- Evaluate the actual artifact: application, library, CLI, documentation/template repository, skill, plugin, or plan. A docs-only repository does not need an invented build, launch, UI, or market case. `N/A` with a reason differs from unavailable evidence.
- Appraise without implementing recommendations. Preserve source, maintained project truth, status files, history, and unrelated dirty changes. Record validation side effects; do not silently revert them.
- Select documented safe checks for the affected contract. Never deploy, publish, migrate production data, delete unrelated state, rotate secrets, or force unavailable credentialed/paid checks for an appraisal.
- Ground claims in reviewed evidence and separate direct observation, inference, user reports, uncertainty, and missing coverage. Prior effort or complexity alone is not merit; market ambition is not market validation.
- Honor settled user decisions and exclusions. Raw Dictation does not override maintained truth without an explicit superseding decision. Recommendations may flag scope tension but cannot require forbidden implementation.
- Inherit configured model/effort. Strongest-model assumptions and numerical routing are not requirements; record requested and observed runtime identities separately if relevant. Use one scoped independent review only where consequence justifies it.
- Existing authorization governs commits and external messages; writing a report neither authorizes them nor expands the implementation scope.

## Workflow

1. Resolve question, target, format, destination, and accepted decisions. Inspect instructions and current state; load the smallest relevant maintained context via the evidence reference.
2. Identify the artifact type, actual contracts, dependencies, and useful evidence. Bound the investigation to the decision the report must support.
3. Run relevant documented checks when enabled. Record commands, pass/fail/unavailable/not-applicable outcomes, and side effects. Use external sources for current factual claims when materially needed and permitted.
4. Assess merit, technical fitness, execution health, and interventions using the report reference with confidence per judgment. Separate inherent consequence, implementation hazards, and residual risk when applicable.
5. Write the requested primary artifact. For visual output, render and inspect representative/full pages as supported by the relevant artifact workflow; fix report layout errors without changing the appraised source.
6. Report the artifact path or complete inline result, overall assessment, recommended decision, confidence, and material validation gaps.

## Surviving compaction

A long appraisal uses its selected primary report draft to checkpoint scope, source links, accepted decisions, commands/results, findings, unknowns, and next step before investigating another area. Mark the draft incomplete until delivered. Necessary report assets carry visual evidence; no second planning/status ledger is required.

## Observable output

The delivered artifact uses the requested format, evaluates the actual artifact type, distinguishes unavailable from inapplicable checks, and cites evidence/confidence for material findings. Recommendations remain report content.
