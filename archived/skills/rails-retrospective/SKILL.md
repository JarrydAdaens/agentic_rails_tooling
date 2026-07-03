---
name: rails-retrospective
description: >-
  Use this skill after implementation work, planning work, Agentic Rails
  implementation-plan execution, bulk planning, orchestration runs, or completed
  stories when the user asks for a retrospective, lessons learned, post-work
  review, process review, plan-adherence review, or durable retrospective.md
  grounded in plans, logs, git history, changed files, and optional provenance
  artifacts.
disable-model-invocation: true
metadata:
  version: "1.1"
---

# Rails Retrospective

Produce a durable retrospective report after completed agentic work. The report should explain how the work actually went, what can be learned from it, and what should be repeated, changed, escalated, or codified next time.

This is a post-work reflection and review artifact. It is not a generic code review, a complaint dump, a handover replacement, or a private chain-of-thought transcript.

## Artifact

When this skill is active, create or update:

```text
retrospective.md
```

Path selection:

1. If the target repository follows Agentic Rails and an active implementation-plan folder is identifiable, write `retrospective.md` in that folder.
2. Otherwise, if Agentic Rails is detected, write to `context/retrospectives/retrospective.md` unless a more specific filename is needed to avoid overwriting an unrelated retrospective.
3. Otherwise, write `retrospective.md` in the target project's context or documentation folder, preferring `context/`, then `documentation/`, then `docs/`.
4. If no context or documentation folder exists outside Agentic Rails, create `context/retrospective.md`.

Prefer co-locating the retrospective with the implementation artifacts whenever possible.

## Inputs To Review

Use the most relevant available sources. Missing optional files are not failures.

- Project context: `design.md`, `milestones.md``, repository laws, rules, or local instructions.
- Execution context: `plan.md`, `implementation-log.md`, handover artifacts, workflow progress files, orchestration briefs, or planning outputs.
- Optional provenance: `complaining.md`, `thinking.md`, `evidence.md`.
- Git history: relevant commits, commit messages, diffs, changed file lists, and commit ranges.
- Code state: final changed files, tests, build configuration, generated artifacts, or documentation changes.
- Persona context: domain persona instructions or references when a persona was used or is needed for review quality.

The repository may use a `commit-log` skill that produces structured, review-friendly commit messages. Treat commit history as a meaningful evidence source, not just a list of hashes.

## Output Shape

Write the report with this structure:

```markdown
# Retrospective Report

## 1. Context

## 2. Executive Summary

## 3. What Went Well

## 4. What Went Poorly

## 5. What To Do Better Next Time

## 6. Kudos

## 7. Runners Up The Chain

## 8. Evidence Reviewed

## 9. Optional Ratings
```

Keep the sections even when a section is brief. If there is nothing meaningful to report in a section, say so directly.

## Section Guidance

### 1. Context

Identify what was reviewed:

- task, story, plan folder, workflow run, or commit range
- review date
- reviewer agent or persona
- sources consulted
- relevant commits or changed files

### 2. Executive Summary

State the overall outcome plainly: solid, mixed, weak, blocked, mundane, smooth, or problematic. Lead with what matters most.

### 3. What Went Well

Capture material positives only:

- strong implementation choices
- good plan adherence
- useful artifacts
- effective tooling or workflow use
- strong validation or commit quality
- domain persona help
- unexpectedly efficient outcomes

Do not force praise when the work was merely normal.

### 4. What Went Poorly

Capture factual negatives proportionately:

- friction, loops, delays, failed attempts, or tool problems
- weak specification, ambiguity, or missed context
- plan drift, undocumented deviations, or skipped validation
- poor code choices, fragile design, or inconsistent style
- weak logs, evidence, handover, or workflow artifacts
- meaningful issues surfaced in `complaining.md`

Do not invent problems to balance the report.

### 5. What To Do Better Next Time

Make this the most actionable section. Include recommendations to repeat, stop, improve, automate, clarify earlier, codify into a skill/template/workflow, or change in the human+AI working process.

Every recommendation should have a basis in reviewed evidence or be clearly labeled as an inference.

### 6. Kudos

Recognize people, tools, workflows, personas, or artifacts that materially helped. Keep it specific and non-fluffy.

### 7. Runners Up The Chain

Escalate only issues that need operator, leadership, system, environment, policy, or process-level attention. Ordinary execution friction belongs in "What Went Poorly", not here.

Use this section for concerns such as broken permissions, persistent environment misconfiguration, inadequate model or token budget, bad workflow policy, repeated operator-created blockers, or strategic concerns about whether the work is being done the right way.

### 8. Evidence Reviewed

List the sources actually reviewed, such as plans, logs, optional artifacts, commits, changed files, validation commands, persona references, and workflow state files.

### 9. Optional Ratings

Ratings are optional and should stay lightweight. Use them only when they add signal:

- plan adherence: High / Medium / Low
- code quality: High / Medium / Low
- execution quality: High / Medium / Low
- artifact usefulness: High / Medium / Low
- process quality: High / Medium / Low

Do not turn ratings into empty bureaucracy.

## Operating Model

1. Detect whether the scope is one task, one implementation-plan folder, one story, multiple stories, a planning run, an execution run, or a workflow run.
2. Locate the minimum relevant sources needed to review the work.
3. Compare intended work against actual execution.
4. Inspect changed files and validation evidence enough to assess implementation quality.
5. Review process, artifact, workflow, and persona use.
6. Sort findings into good, poor, better next time, kudos, and runners up the chain.
7. Write or update the selected `retrospective.md`.
8. Keep the report factual, proportionate, and actionable.

## Claim Standard

Ground the report in reviewed artifacts wherever possible.

- Verified: directly supported by source, command output, commit, or artifact.
- Inferred: likely based on available evidence, but not directly proven.
- Assumed: accepted because task context required it.
- Unknown: not enough evidence.

For cold retrospectives where conversation context is unavailable, be stricter about labeling inference and unknowns.

## Boundaries

- Do not expose private chain-of-thought.
- Do not create `complaining.md`, `thinking.md`, `evidence.md`, or handover artifacts unless those skills are also active.
- Do not replace implementation logs, evidence files, complaint logs, or handovers.
- Do not over-escalate ordinary problems into "Runners Up The Chain".
- Do not produce recommendations with no supporting basis.
- Do not assume Agentic Rails exists when detection points are absent.

## Validation

Before considering the skill applied correctly, confirm:

- `retrospective.md` exists in the selected path.
- The report follows the standard section structure.
- Evidence reviewed is listed.
- Claims are grounded or honestly labeled.
- Recommendations are actionable.
- Praise and criticism are not fabricated for symmetry.
- Systemic escalations are separated from ordinary execution friction.
