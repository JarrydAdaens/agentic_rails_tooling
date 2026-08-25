---
name: rails-spike
description: >-
  Use this skill when an Agentic Rails story cannot proceed because the right
  implementation path is genuinely unknown - competing approaches, unclear
  documentation, uncertain dependency or API compatibility, a repeatedly failing
  approach, or a disagreement between the worker and its advisor or critic. The
  spike replaces speculation with evidence: it states the question, runs the
  smallest experiment that answers it, and returns a recommended path with a
  confidence level and the production work the answer creates. Use it instead of
  reasoning further about what might happen, and never as a way to postpone work
  whose answer is already available.
argument-hint: "<the uncertainty to resolve>"
metadata:
  version: "1.0"
---

# Rails Spike

A spike converts *"we do not know"* into *"we tried X, observed Y, and recommend Z."*

It is an evidence-generating tool, not production implementation. Its output is a decision, backed by something that actually ran.

## Arguments

The skill was invoked with: $ARGUMENTS

That is the uncertainty to resolve — a question, an error that keeps recurring, or two approaches that need separating. If it arrives as a story or plan reference instead, read that document and extract the specific unknown blocking it.

A spike answers **one** question. If the arguments carry several, pick the one whose answer unblocks the most work and say which one you took.

## When this is the right move

Reach for a spike when multiple plausible paths exist, documentation is unclear, dependency or API compatibility is uncertain, an approach has failed repeatedly, an agent is speculating about risk, or a worker and its advisor or critic disagree — and the experiment costs less than continuing to reason.

Do not spike what the available evidence already answers, and do not spike as procrastination: a spike that never risks a conclusion is reasoning with extra steps. A spike is also not a rewrite wearing a disguise. If the experiment is turning into the production solution, stop and say so — that is a finding, and it means the work was never ambiguous, only large.

## The workflow

1. **Write the contract before experimenting.** Question, why it matters, candidate hypotheses, the smallest useful experiment, success criteria, and explicit boundaries. The template is in [references/spike-record.md](references/spike-record.md). Writing it first is what keeps a spike from drifting into an unbounded investigation.
2. **Place the record.** A spike serving a story goes in that story's plan folder under `context/implementation-plans/<milestone-slug>/<story-slug>/spikes/<question-slug>.md`. A spike serving no single story goes in `context/implementation-plans/spikes/<question-slug>.md`. The record exists on disk before the experiment runs, so an interrupted spike still leaves its question behind.
3. **Run the smallest experiment that produces evidence.** A scratch project, a narrow test, a single API call, one dependency bump, one representative code path. Prefer runnable evidence — a build result, a test, a runtime observation, a benchmark, a compatibility result, a minimal prototype — over reading and inference.
4. **Record what happened, including failure.** A spike that eliminates a path succeeded. "The experiment failed" and "the work failed" are different sentences.
5. **Write the completion report** into the same record: result, evidence, conclusion, recommended path, confidence, remaining unknowns, and the production work the answer creates.
6. **Return the recommendation to the caller.** The agent that invoked the spike owns integrating it. Where independent work exists, that agent keeps working while the spike runs rather than idling on it.

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- One spike answers one question. State it in a single sentence before running anything.
- The contract is written and placed on disk before the experiment begins.
- The experiment is the smallest one that produces evidence. Prefer scratch space and throwaway code to modifying production paths.
- Nothing a spike writes is production work. Where an experiment must touch the repository, it lands on a branch or is reverted, and the record says which.
- Evidence is something observed, not something expected. Name the command, the output, the version, the error.
- A failed experiment is reported as a result, never as an absence of one.
- Every spike ends with a recommended path and a confidence level, even when the recommendation is "none of these — here is what to try next".
- A spike never concludes that the milestone should stop. It answers its question and hands the routing decision back to its caller.

## Acceptance

Observable facts, checkable by a reader who was not present:

- A spike record exists at the documented path, carrying both the contract and the completion report.
- The question in the record is answerable yes/no or this/that — not "investigate the rendering layer".
- The evidence section names commands, outputs, versions, or observations rather than conclusions.
- The recommended path is specific enough to start work from, and the production work it creates is listed.
- Any repository change the spike made is either reverted, committed on a branch identified in the record, or explicitly listed as production work created.

## Relationship to the other Rails skills

- **`rails-minion-workflow`** and **`rails-boss-execute-workflow`** invoke a spike when an obstacle turns out to be ambiguity rather than difficulty. The spike is one rung of their blocker ladder, not an alternative to it.
- **`rails-planning`** owns the plan a spike's recommendation feeds into. A spike that produces production work says so; the plan is where that work is written down.
- **`rails-planning-phaser`** splits work that is too large. Reach for the phaser when the path is known and long, and for a spike when the path is short and unknown.
