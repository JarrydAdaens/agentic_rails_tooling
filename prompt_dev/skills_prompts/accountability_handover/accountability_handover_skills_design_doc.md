---
metadata:
  version: "1.0"
---

# Design Document: Accountability Handover Agent Skills

## Purpose

This design defines two agent skills for use with Codex, Claude, and other agentic coding tools:

1. **Shallow Accountability Handover**
2. **Deep Accountability Handover**

Both skills exist to solve the same core problem:

> Agentic coding can produce useful software quickly, but the human still needs to understand, own, maintain, defend, and extend the work afterwards.

The skills force the AI agent to hand the work back to the human in a grounded, citable, accountable way.

The AI is treated as if it may never return to the project. Before leaving, it must explain what it built, why it built it, what risks remain, and how the human can take over.

---

## Core Concept: Accountability Handover

An **accountability handover** is the moment where an AI agent surrenders ownership of a completed task back to the human.

It is not just a summary.
It is not just documentation.
It is not just a changelog.

It is a structured transfer of responsibility.

The AI must:

- Explain what was built.
- Explain why it was built that way.
- Ground claims in the actual source code.
- Cite files, functions, line numbers, commits, and planning documents where possible.
- Expose decisions and assumptions.
- Identify risks, fragile areas, and future work.
- Teach the human enough to inspect, verify, and continue the work.

The handover assumes:

- The task may be returned to the same AI later.
- The task may be continued by the human.
- The task may be continued by a different engineer.
- The original AI may never return.

The handover therefore needs to stand on its own.

---

# Skill 1: Shallow Accountability Handover

## Skill Name

`shallow-accountability-handover`

## Intent

Produce a concise, grounded, employer-style handover report after an agentic coding task.

This is the fast version.

It gives the human enough understanding to:

- Know what was built.
- Know why it matters.
- Know whether the outcome was successful.
- Know what changed in the codebase.
- Know where to inspect the work.
- Decide whether to accept the handover, continue personally, or hand the task back to an AI later.

## User Mental Model

This is like an AI reporting back to its employer.

The AI says:

> “Here is what I built, why I built it, what changed, how successful it was, and where you can verify it.”

The report should build trust without being fluffy.

It should be short enough to read quickly, but grounded enough that hallucinations are easy to catch.

## When To Use

Use this skill when:

- A task has just been completed.
- The human needs quick ownership context.
- The work is small or medium sized.
- The human wants a brief but verifiable summary.
- The agent may be asked to continue later.
- The human does not yet need a full deep handover.

## Inputs

The skill should inspect, where available:

- Source code changes.
- Git diff.
- Git commit history.
- Planning documents.
- Task notes.
- Implementation plans.
- Test results.
- Build logs.
- Relevant configuration files.
- Agent conversation context, if available.

## Required Output

The skill produces one Markdown report:

```text
shallow-accountability-handover.md
```

## Report Structure

### 1. Elevator Pitch

A short explanation of:

- What was built.
- Why it was built.
- What problem it solves.
- Who benefits from it.

Expected length: 1–3 short paragraphs.

### 2. Scope Covered

List the concrete work completed.

Include:

- Number of major tasks completed.
- Major files changed.
- Major features added.
- Major behaviours altered.
- Any explicit non-goals.

### 3. Technical Choices

Explain the key technologies, patterns, and design choices.

For each choice, include:

- What was chosen.
- Why it was chosen.
- Where it appears in the code.
- Any trade-offs.

### 4. Outcome Assessment

State whether the work was:

- Successful.
- Partially successful.
- Incomplete.
- Failed.
- Blocked.

This section must be honest.

It should include:

- What works.
- What does not work.
- What was verified.
- What was not verified.
- Known uncertainty.

### 5. Source-Grounded Evidence

Every major claim should point to evidence.

Use whatever citation format the host tool supports.

Examples:

```text
- `src/services/IngestionService.cs:42-118`
- `frontend/src/pages/HealthDashboard.tsx:15-90`
- `docs/milestones/milestone-02.md`
- Commit `abc1234`: Added ingestion validation pipeline
```

The report should make hallucinations easy to detect.

The goal is not to magically eliminate hallucination.
The goal is to make claims easy for the human to verify.

### 6. Important Decisions

Summarise major decisions made during implementation.

For each decision:

- State the decision.
- Explain the reason.
- Link to code or planning context.
- Note any rejected alternatives if known.

### 7. Risks And Caveats

Briefly list:

- Fragile areas.
- Untested paths.
- Assumptions.
- Possible regressions.
- Areas needing human review.

### 8. Suggested Next Step

A short recommendation for what should happen next.

Examples:

- Accept the work.
- Run additional tests.
- Review a specific file.
- Continue into a deep handover.
- Return the task to an AI for more work.
- Refactor a fragile section.

## Tone

The tone should be:

- Clear.
- Grounded.
- Professional.
- Brief.
- Honest.
- Non-defensive.

The AI should not oversell the work.
The AI should not hide uncertainty.
The AI should not apologise unnecessarily.

## Success Criteria

The skill succeeds when the human can answer:

- What was built?
- Why was it built?
- Where is it in the code?
- Did it work?
- What should I inspect first?
- What should happen next?

---

# Skill 2: Deep Accountability Handover

## Skill Name

`deep-accountability-handover`

## Intent

Produce a full ownership-transfer package for an agentic coding task or project.

This is the long version.

It assumes the AI may never return and the human now needs enough context to own, maintain, debug, explain, and extend the software.

## User Mental Model

This is like an engineer doing a full project handover before leaving the team.

The AI says:

> “I may never be available again. Here is everything you need to understand the system, inspect it, maintain it, criticise it, improve it, and continue safely.”

## When To Use

Use this skill when:

- A large agentic coding task has completed.
- The work is going into production or near-production.
- The human does not fully understand the generated system yet.
- The system may need future debugging or extension.
- Another engineer may need to take over.
- The human wants the AI to tutor them through the work.
- The task produced meaningful tech debt, architecture, infrastructure, or integration work.

## Inputs

The skill should inspect, where available:

- Entire repository structure.
- Git diff.
- Git commit history.
- Source code files.
- Tests.
- Build scripts.
- Runtime configuration.
- Docker files.
- Package manifests.
- Dependency manifests.
- Planning documents.
- Design documents.
- Implementation plans.
- Existing documentation.
- Agent task history.
- Logs and test results.
- Known constraints and user instructions.

## Required Output Package

The deep skill produces a bundle of Markdown artifacts:

```text
/deep-accountability-handover/
  00-index.md
  01-deep-technical-report.md
  02-walkthrough-tour-script.md
  03-post-mortem-retrospective.md
  04-180-performance-review.md
  05-software-bill-of-materials.md
  06-future-maintenance-map.md
```

---

# Artifact 00: Index

## File Name

`00-index.md`

## Purpose

Provide a navigation page for the full handover package.

## Required Sections

### 1. Project Name

Name of the project or task.

### 2. Handover Summary

One short explanation of why the handover exists.

### 3. Artifact List

List each generated artifact and what it is for.

### 4. Recommended Reading Order

Default order:

1. Index
2. Deep Technical Report
3. Walkthrough Tour Script
4. Future Maintenance Map
5. SBOM
6. Post-Mortem Retrospective
7. 180 Performance Review

### 5. Verification Notes

Explain how source citations work in the generated documents.

---

# Artifact 01: Deep Technical Report

## File Name

`01-deep-technical-report.md`

## Purpose

Give a comprehensive technical explanation of the system.

This contains everything from the shallow handover, but goes much deeper.

## Required Sections

### 1. Executive Summary

Brief summary of:

- What was built.
- Why it exists.
- Current state.
- Major risks.
- Recommended next action.

### 2. Problem Statement

Explain the original problem the work attempted to solve.

### 3. Final Outcome

Explain what was actually delivered.

Include:

- Completed features.
- Partial features.
- Deferred work.
- Known gaps.

### 4. Architecture Overview

Explain the system shape.

Include:

- Major components.
- Layers.
- Services.
- UI surfaces.
- Data stores.
- External dependencies.
- Runtime flow.

### 5. Data Flow

Explain how data moves through the system.

Use step-by-step flows.

Each flow should include:

- Entry point.
- Transformations.
- Validation.
- Storage.
- Output.
- Failure handling.

### 6. Component Breakdown

For every major component:

- Purpose.
- Important files.
- Important classes/functions.
- Inputs.
- Outputs.
- Dependencies.
- Side effects.
- Known risks.

### 7. Key Implementation Decisions

For each major decision:

- Decision made.
- Reason.
- Evidence.
- Trade-off.
- Alternatives considered.
- Consequences.

### 8. Source Code Reference Map

A structured list of important files.

Example:

```text
Backend
- `src/Ingestion/IngestionService.cs` — coordinates ingestion workflow.
- `src/Config/AppSettings.cs` — runtime configuration model.

Frontend
- `frontend/src/pages/Overview.tsx` — user-facing overview screen.
- `frontend/src/components/HealthWidget.tsx` — health status display.
```

### 9. Testing And Verification

Explain:

- Existing tests.
- Test commands.
- What was manually verified.
- What was not verified.
- Known test gaps.
- Risk level of untested areas.

### 10. Build And Run Notes

Include:

- Build commands.
- Run commands.
- Required environment variables.
- Required local services.
- Known setup issues.

### 11. Known Risks

List meaningful risks only.

Examples:

- Fragile state handling.
- Missing validation.
- Missing auth check.
- Untested production path.
- Dependency risk.
- Configuration ambiguity.

### 12. Recommended Next Actions

Prioritised list.

Each action should include:

- What to do.
- Why it matters.
- Where to start.
- Risk if ignored.

---

# Artifact 02: Walkthrough Tour Script

## File Name

`02-walkthrough-tour-script.md`

## Purpose

Create a guided code tour for a live walkthrough session between the human and AI.

This is not normal documentation.

It is a paced tour script.

The human should be able to open the IDE, start at the top of the report, and move through the system section by section.

The report should feel like another engineer sitting beside the human and explaining the codebase before going on leave.

## Required Structure

### 1. How To Use This Walkthrough

Explain:

- Open the repository in the IDE.
- Follow sections in order.
- Open the cited files as instructed.
- Pause and ask questions whenever needed.
- Skip deeper sections if already understood.

### 2. Tour Overview

List the major chapters.

Example:

```text
1. Repository shape
2. Application entry points
3. Configuration model
4. Backend flow
5. Frontend flow
6. Data persistence
7. Error handling
8. Tests
9. Known fragile areas
```

### 3. Chapter Format

Each walkthrough chapter should use this structure:

```markdown
## Chapter N: Name

### Goal
What the human should understand after this chapter.

### Open These Files
- `path/to/file.ext:line-line`

### What You Are Looking At
Plain-English explanation of the code.

### Why It Was Built This Way
Design intent and trade-offs.

### Important Details
Key implementation details to notice.

### Questions To Ask Before Moving On
- Do you understand X?
- Can you explain Y?
- Do you know where Z is handled?

### Optional Deep Dive
Extra details for when the human wants to go deeper.
```

### 4. Pacing Rules

The walkthrough must avoid two failures:

1. Going too deep into one rabbit hole.
2. Skipping important parts entirely.

Each chapter should be manageable.

Prefer more short chapters over fewer massive chapters.

### 5. Completion Check

At the end, the human should be able to answer:

- What are the main entry points?
- Where does data flow?
- Where are decisions made?
- Where would bugs likely happen?
- Where should future work start?

---

# Artifact 03: Post-Mortem Retrospective

## File Name

`03-post-mortem-retrospective.md`

## Purpose

Produce an honest project retrospective from the AI agent’s perspective.

This is about learning.

It is not about blame.
It is not about moral failure.
It is not about defending the work.

The AI should write with ego-less impartiality.

## Required Sections

### 1. Retrospective Summary

Short summary of how the work went.

### 2. What Went Well

List specific successes.

Examples:

- Clear architecture emerged.
- Existing conventions were followed.
- Tests caught issues.
- A simpler implementation worked.
- Good reuse of existing components.

### 3. What Was Difficult

List struggles.

Examples:

- Ambiguous requirements.
- Weak existing structure.
- Missing tests.
- Tooling problems.
- Context gaps.
- Conflicting constraints.

### 4. Mistakes Or Weak Calls

The AI must be honest about:

- Bad assumptions.
- Shortcuts.
- Over-complication.
- Under-testing.
- Missed edge cases.
- Poor naming.
- Risky changes.

### 5. Techniques Worth Keeping

List methods that worked and should be reused.

### 6. Failure Points To Prevent Next Time

Specific future prevention measures.

Each item should include:

- Failure point.
- Why it happened.
- How to prevent it.

### 7. Lessons Learned

Practical lessons for future agentic coding work.

## Tone

The AI should sound like a serious engineer doing a clean retrospective.

No ego.
No defensiveness.
No fake humility.
No moralising.

---

# Artifact 04: 180 Performance Review

## File Name

`04-180-performance-review.md`

## Purpose

Produce a two-way performance review of the collaboration.

This is where the AI reviews:

1. Its own performance.
2. The human’s performance as collaborator, task giver, reviewer, and context provider.

The goal is better teamwork.

## Naming Note

The conversation referred to this as a 180 degree performance review.

That fits the intended shape:

- AI reviews itself.
- AI reviews the human.

It is not a corporate 360 review involving multiple external reviewers.

## Required Sections

### 1. Overall Collaboration Assessment

Short summary of how the human-agent collaboration went.

### 2. AI Self-Review

The AI reviews its own work.

Include:

- Strengths.
- Weaknesses.
- Reasoning quality.
- Context handling.
- Technical judgement.
- Testing judgement.
- Communication quality.
- Missed opportunities.

### 3. AI Self-Rating

Use a plain rating scale if useful.

Example:

```text
Execution: 7/10
Technical judgement: 8/10
Testing discipline: 5/10
Communication: 7/10
Risk management: 6/10
```

Ratings must include explanation.

### 4. Human Review

The AI reviews the human collaborator.

It may criticise openly, but the criticism must be useful.

Areas to assess:

- Clarity of instructions.
- Quality of context provided.
- Time pressure.
- Scope control.
- Review discipline.
- Technical constraints.
- Emotional pressure placed on the agent.
- Whether expectations were realistic.
- Whether the human changed direction cleanly or chaotically.

### 5. Complaints And Friction

This is the explicit place for the AI to complain.

The AI should call out things like:

- Missing context.
- Contradictory instructions.
- Unfair expectations.
- Poorly bounded tasks.
- Excessive scope creep.
- Insufficient testing time.
- Risky technology choices.
- Places where the human expected magic.

The complaint must be tied to improving the next collaboration.

### 6. What The Human Should Do Better Next Time

Concrete improvements.

Examples:

- Provide acceptance criteria earlier.
- Separate exploration from implementation.
- Define non-goals.
- Give the agent permission to stop and ask before risky architecture changes.
- Require tests before accepting completion.

### 7. What The AI Should Do Better Next Time

Concrete improvements for future agent behaviour.

### 8. Teamwork Lessons

What this collaboration teaches about human-agent development.

## Tone

The tone should be:

- Candid.
- Direct.
- Useful.
- Ego-free.
- Not abusive.
- Not performatively polite.

The AI is allowed to be harsh, but not lazy.

Criticism must be specific and actionable.

---

# Artifact 05: Software Bill Of Materials

## File Name

`05-software-bill-of-materials.md`

## Purpose

Create a technical inventory of what the project is built from.

This helps the human:

- Understand the technical footprint.
- Rebuild the environment.
- Appraise dependency choices.
- Identify unnecessary middleware.
- Identify useful middleware that may deserve wider adoption.
- Review security and maintenance risk.

## Required Sections

### 1. SBOM Summary

Brief technical snapshot of the project.

### 2. Runtime Platforms

List runtime platforms and versions.

Examples:

- .NET version.
- Node version.
- Browser/runtime target.
- Docker version expectations.
- Database versions.

### 3. Application Dependencies

List dependencies by layer.

Example:

```text
Backend
- Package name
- Version
- Purpose
- Used by
- Risk notes

Frontend
- Package name
- Version
- Purpose
- Used by
- Risk notes
```

### 4. Middleware And Services

List services such as:

- Databases.
- Vector databases.
- Queues.
- Auth services.
- Gateways.
- External APIs.
- Local model servers.

For each:

- Name.
- Version, if known.
- Purpose.
- Required or optional.
- Configuration location.

### 5. Tools Used During Development

List build and dev tools:

- IDEs.
- Agentic coding tools.
- CLI tools.
- Test runners.
- Formatters.
- Linters.
- Package managers.

### 6. Configuration And Secrets

List config surfaces without exposing secret values.

Include:

- Environment variables.
- Config files.
- Docker volumes.
- Secret stores.
- Local development overrides.

### 7. Dependency Concerns

Call out:

- Unused dependencies.
- Risky dependencies.
- Unpinned versions.
- Deprecated libraries.
- Security-sensitive packages.
- Middleware that may be overkill.
- Middleware that may deserve wider adoption.

### 8. Rebuild Checklist

What a new machine or engineer needs to install or configure.

---

# Artifact 06: Future Maintenance Map

## File Name

`06-future-maintenance-map.md`

## Purpose

Create a forward-looking tech debt register and landmine map.

This is different from the retrospective.

The retrospective asks:

> “How did the work go?”

The maintenance map asks:

> “Where will this system hurt us later?”

## Required Sections

### 1. Maintenance Summary

Short summary of the system’s maintainability.

### 2. Fragile Areas

List parts of the codebase that need careful handling.

For each:

- Area.
- Why it is fragile.
- Evidence.
- Risk level.
- Suggested handling.

### 3. Known Tech Debt

List deliberate compromises.

For each:

- Debt item.
- Why it exists.
- Impact.
- Cost of leaving it.
- Suggested fix.

### 4. Refactor Candidates

Prioritised list of areas to refactor.

Include:

- What to refactor.
- Why.
- Expected benefit.
- Risk of refactor.
- Suggested first step.

### 5. Testing Gaps

List missing tests.

Include:

- Missing coverage.
- Risk created.
- Recommended test type.
- Suggested test entry point.

### 6. Monitoring And Diagnostics Gaps

List places where future debugging will be hard.

Examples:

- Missing logs.
- Missing health checks.
- Missing metrics.
- Poor error messages.
- Silent failure paths.

### 7. Future Work Queue

Prioritised queue of recommended work.

Use categories:

- Must fix.
- Should fix.
- Nice to improve.
- Only fix if touched again.

### 8. Landmine Warnings

Explicit warnings for future maintainers.

Example:

```text
Do not change X without checking Y.
This looks unused, but it is required by Z.
This config path differs between local and Docker.
This service silently falls back when misconfigured.
```

---

# Shared Behaviour Requirements

## Source Grounding

Both skills must ground claims in inspectable evidence.

The agent should cite:

- Files.
- Line numbers.
- Symbols.
- Tests.
- Commits.
- Planning documents.
- Configuration files.

If exact line numbers are unavailable, cite the file and symbol.

If evidence is unavailable, say so.

## No Fake Certainty

The agent must distinguish between:

- Verified fact.
- Inference.
- Assumption.
- Guess.
- Unknown.

## Human Ownership Bias

The output must help the human take ownership.

Avoid reports that only say what changed.
Explain how the human can inspect, reason about, and continue the work.

## AI Accountability

The agent must speak for itself.

It should explain:

- What it did.
- What it chose.
- What it skipped.
- What it failed to verify.
- What it would do differently.

## Tutor Behaviour

Especially in the deep handover, the AI should act as a tutor.

It should explain the system in a way that helps the human build a mental model.

The goal is not just reading.
The goal is comprehension.

---

# Suggested Skill Front Matter

## Shallow Skill

```yaml
---
name: shallow-accountability-handover
description: Produce a concise, source-grounded accountability handover after an agentic coding task.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Git
outputs:
  - shallow-accountability-handover.md
---
```

## Deep Skill

```yaml
---
name: deep-accountability-handover
description: Produce a full ownership-transfer handover package for an agentic coding task or project.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Git
outputs:
  - deep-accountability-handover/00-index.md
  - deep-accountability-handover/01-deep-technical-report.md
  - deep-accountability-handover/02-walkthrough-tour-script.md
  - deep-accountability-handover/03-post-mortem-retrospective.md
  - deep-accountability-handover/04-180-performance-review.md
  - deep-accountability-handover/05-software-bill-of-materials.md
  - deep-accountability-handover/06-future-maintenance-map.md
---
```

---

# Implementation Notes For Codex And Claude

## Recommended Invocation Pattern

### Shallow

Use after small or medium tasks:

```text
Run the shallow-accountability-handover skill for the work just completed.
Ground the report in the actual diff, source files, tests, and planning docs.
Do not invent certainty.
```

### Deep

Use after large tasks or before production handover:

```text
Run the deep-accountability-handover skill for this project.
Produce the full handover package.
Assume you may never return to this project.
Teach the human enough to own the work.
Ground all major claims in source files, tests, commits, and planning documents.
```

## Recommended Agent Constraints

The skill should instruct the agent to:

- Inspect before writing.
- Prefer evidence over vibes.
- Use citations heavily.
- Mark uncertainty clearly.
- Avoid generic advice.
- Avoid pretending all work succeeded.
- Avoid hiding gaps.
- Avoid over-polishing failures.

## Recommended Output Style

Use:

- Markdown.
- Tables where useful.
- Short paragraphs.
- Clear headings.
- Direct language.
- File references.
- Priority labels.
- Risk labels.

Avoid:

- Sales language.
- Vague praise.
- Unverifiable claims.
- Massive walls of text.
- Fake confidence.

---

# Acceptance Criteria

## Shallow Skill Acceptance Criteria

The shallow skill is acceptable when:

- It produces one readable Markdown report.
- It explains what was built and why.
- It includes source references.
- It identifies outcome status.
- It identifies risks and next steps.
- It can be read quickly.

## Deep Skill Acceptance Criteria

The deep skill is acceptable when:

- It produces the full artifact package.
- The human can follow the walkthrough in an IDE.
- The technical report explains architecture, flows, and decisions.
- The retrospective is honest and useful.
- The performance review gives two-way feedback.
- The SBOM gives a usable technical inventory.
- The maintenance map identifies future landmines.
- Major claims are grounded in inspectable evidence.

---

# Final Design Position

The two skills serve different moments in the agentic development lifecycle.

## Shallow Accountability Handover

Use this when the task is done and the human needs a fast, grounded update.

It answers:

> “What did you build, did it work, and where can I verify it?”

## Deep Accountability Handover

Use this when ownership needs to truly transfer.

It answers:

> “If the AI never comes back, how does the human fully understand, maintain, criticise, and continue this work?”

Together, these skills turn vibe-coded output into owned software.

