---
metadata:
  version: "1.0"
---

# Accountability Handover Skills And Agents

## Summary

Create one fast handover skill and one deep orchestration skill:

- `shallow-accountability-handover`: a single-pass skill that produces `shallow-accountability-handover.md`.
- `deep-accountability-handover`: a Boss/meta skill that spawns artifact-focused subagents and assembles the full `deep-accountability-handover/` package.

Add one reusable accountability agent contract plus six artifact worker skills. The deep Boss equips each worker with the shared accountability agent contract and the specific artifact skill for its output.

## Key Changes

- Add shared agent contract: `agents/accountability-handover/AGENT.md`.
  - Defines the evidence-first posture: inspect before writing, cite files/lines/commits/tests, label fact vs inference vs assumption vs unknown, avoid fake certainty, and teach the human to own the work.
  - Includes worker return contract: artifact path, evidence inspected, claims that remain uncertain, risks found, and blockers.

- Add shallow skill: `skills/shallow-accountability-handover/SKILL.md`.
  - Produces one concise Markdown report.
  - Requires sections from the design doc: elevator pitch, scope covered, technical choices, outcome assessment, source-grounded evidence, important decisions, risks/caveats, suggested next step.
  - Uses local inspection sources in this order: user context, git diff/status/log, changed files, tests/build logs if available, planning docs, relevant config.

- Add deep Boss skill: `skills/deep-accountability-handover/SKILL.md`.
  - Creates durable workflow state under `documentation/workflows/deep_accountability_handover/` with `briefing.md`, `progress.md`, and `logs/`.
  - Creates final output under `deep-accountability-handover/`.
  - Dispatches one worker per artifact, validates each artifact against the design doc, then writes `00-index.md` last.
  - Defaults to parallel workers after the evidence briefing is built because artifact outputs are independent files.

- Add deep artifact worker skills:
  - `skills/deep-technical-report-handover`: writes `01-deep-technical-report.md`.
  - `skills/walkthrough-tour-handover`: writes `02-walkthrough-tour-script.md`.
  - `skills/post-mortem-retrospective-handover`: writes `03-post-mortem-retrospective.md`.
  - `skills/performance-review-180-handover`: writes `04-180-performance-review.md`.
  - `skills/sbom-handover`: writes `05-software-bill-of-materials.md`.
  - `skills/future-maintenance-map-handover`: writes `06-future-maintenance-map.md`.

## Deep Workflow Design

- Boss first builds an evidence briefing:
  - repository shape
  - changed files and commits in scope
  - planning/design docs found or provided
  - test/build commands and known validation results
  - dependency/config surfaces
  - user-stated task intent and acceptance criteria from available context

- Boss initializes `progress.md` with artifact rows:
  - `TECHNICAL_REPORT`
  - `WALKTHROUGH`
  - `RETROSPECTIVE`
  - `PERFORMANCE_REVIEW`
  - `SBOM`
  - `MAINTENANCE_MAP`
  - `INDEX`

- Each worker receives:
  - `agents/accountability-handover/AGENT.md`
  - its specific artifact skill
  - the evidence briefing path
  - exact output file path
  - exact required sections
  - instruction to cite evidence and mark uncertainty

- Boss accepts an artifact only when:
  - the expected file exists
  - required sections are present
  - major claims are source-grounded or marked uncertain
  - no artifact pretends unverified work was verified
  - the worker reports evidence inspected and unresolved risks

- Boss writes `00-index.md` after all accepted artifacts, with reading order, artifact descriptions, and citation/verification notes.

## Skill Structure

Each new skill folder should contain only:

- `SKILL.md`
- optional `agents/openai.yaml`
- optional `references/` only when the artifact rules are too large for the core skill

Do not create READMEs or extra documentation files. Keep `SKILL.md` concise and put long artifact templates in `references/` if needed.

Use only standard skill frontmatter fields:

```yaml
---
name: skill-name
description: Clear trigger and purpose.
---
```

Avoid the design doc's suggested `allowed-tools` and `outputs` fields because the local `skill-creator` guidance says Codex only relies on `name` and `description`.

## Test Plan

- Validate every new skill with `quick_validate.py`.
- Dry-run shallow against this repository's current diff or a small completed task and confirm it produces exactly one report with citations.
- Dry-run deep against a small repo/task and confirm it creates all seven files.
- Inspect deep artifacts for:
  - required section coverage
  - source citations
  - uncertainty labels
  - no secret leakage in SBOM/config sections
  - useful, specific maintenance risks
  - candid but non-abusive 180 review language
- Forward-test the deep Boss with at least one subagent pass to ensure artifact workers can operate from the shared briefing without hidden context.

## Assumptions

- Implement these as repo-local assets under `D:\Code Projects\agentic_tooling\skills` and `D:\Code Projects\agentic_tooling\agents`.
- Keep the public skill names from the design doc: `shallow-accountability-handover` and `deep-accountability-handover`.
- Treat the deep handover as a meta/orchestration skill, not a monolithic writing skill.
- The artifact worker skills are reusable directly, but their primary intended use is through the deep Boss.
