---
name: rails-planning
description: >-
  Use this skill when creating, revising, locating, or enforcing implementation
  plans inside an Agentic Rails project. Use for implementation plans, work
  plans, execution plans, feature plans, bug plans, repository planning before
  coding, IDE planning drift, or any planning output that should survive across
  IDEs, machines, branches, sessions, reviews, retrospectives, implementation
  logs, evidence, complaints, or handovers. The skill ensures plans are written
  into the target repository under context/implementation-plans/ using
  Tier 4 planning conventions, with implementation-log.md and questions.md
  beside every new plan.
metadata:
  version: "1.1"
  agentic_rails_source_version: "1.1"
---

# Rails Planning

Force implementation planning to live in the target repository, not in IDE-local state, hidden assistant folders, chat history, or machine-specific storage.

This is the single-plan enforcement skill for Agentic Rails. It creates or revises durable Tier 4 implementation-plan artifacts. It does not implement production code.

`rails-planning` itself belongs to the right rail: reusable agentic behavior. Its output belongs to the left rail: project-local context and provenance.

## Core Rule

When planning implementation work inside a repository, create or update these durable files:

```text
context/implementation-plans/<task-folder>/plan.md
context/implementation-plans/<task-folder>/implementation-log.md
context/implementation-plans/<task-folder>/questions.md
```

Initial log content may be minimal:

```markdown
# Implementation Log

This file records what actually happened during execution of the adjacent plan.
```

`questions.md` captures every open question discovered during planning, including the temporary assumption used in the plan until the answer arrives. If no questions exist, create the file and mark it with `Status: NONE`. See [references/questions-format.md](references/questions-format.md) for the exact format.

All three files must be normal repository files that the human can review, diff, branch, commit, copy, and preserve with the project.

## When To Apply

Apply this skill when the user asks for one implementation plan or wants IDE planning redirected into Agentic Rails. Typical triggers include:

- Planning before coding in Codex, Claude Code, Cursor, Windsurf, Cascade, or another agentic IDE.
- Creating or revising a feature, bug, refactor, spike, goal, work, task, or execution plan.
- Making planning output durable across machines, IDEs, branches, sessions, reviews, or retrospectives.
- Preparing context that will later feed `implementation-log.md`, `complaining.md`, `thinking.md`, `evidence.md`, or handover artifacts.
- Fixing hidden, scattered, disconnected, or lost IDE-local plans.

Do not apply this skill when the user explicitly wants only a quick chat outline, the plan is unrelated to repository implementation work, the task is trivial enough that a durable Tier 4 plan would be noise, or another active workflow explicitly owns the output location.

Use `rails-plan-spam-workflow` instead when the user wants many plans generated from goals, backlog items, feature dumps, or milestone checklists.

## Repository Detection

1. Identify the target repository root.
2. Treat the repository as Agentic Rails when any of these exist:
   - `AGENTIC_RAILS.md`
   - `.agentic-rails.json`
   - `AGENTIC_RAILS_README.MD`
   - `context/implementation-plans/`
   - an established five-tier `context/` structure
3. If the target repository is not clearly Agentic Rails but the user explicitly asks for this skill, still create repository-local planning artifacts using the path rules below.

## Context Loading

Load only the minimum context needed to write a grounded plan. Prefer maintained context over raw intake:

1. `context/design.md`
2. `context/milestones.md`
3. relevant `context/goals*.md`
4. existing related `context/implementation-plans/*/plan.md`
5. relevant Tier 0 source only when raw intake materially shaped the task

Tier 0 is raw intake, not final truth. If Tier 0 contradicts maintained design, milestones, or goals, prefer maintained context and record the contradiction as an open question.

## Path Selection

Prefer the canonical Agentic Rails path:

```text
context/implementation-plans/
```

Preserve an existing repository convention rather than creating duplicate folders. Accept these existing variants:

```text
context/implementation-plans/
documentation/implementation-plans/
docs/implementation-plans/
```

If an active plan already exists for the same task, update that `plan.md` instead of creating a duplicate. Preserve existing decisions unless the user asks for a revision, add a short revision note when useful, and do not overwrite `implementation-log.md`.

## Folder Naming

Use one of these folder patterns:

```text
GOAL_<milestone>_<goal>_<short-slug>/
FEATURE_<short-slug>/
BUG_<short-slug>/
REFACTOR_<short-slug>/
SPIKE_<short-slug>/
```

Slug rules:

- Use lowercase words separated by hyphens.
- Keep the slug short but recognizable.
- Avoid vague names such as `new-plan`, `task`, or `implementation`.
- Include a goal id when one exists.

Examples:

```text
context/implementation-plans/FEATURE_add-report-export-support/
context/implementation-plans/BUG_fix-login-token-refresh/
context/implementation-plans/GOAL_2_3_add-health-checks/
context/implementation-plans/SPIKE_compare-vector-store-options/
```

## Operating Model

1. Detect the target repository root and whether it follows Agentic Rails.
2. Load the minimum maintained context needed to ground the plan.
3. Decide whether the user wants a new plan, a revision, or path enforcement.
4. Search existing implementation-plan folders for related active plans.
5. Select or create the correct task folder under the implementation-plans path.
6. Create or update `plan.md` using the Tier 4 structure from [references/plan-template.md](references/plan-template.md), unless the repository has a stronger local template.
7. Ensure `implementation-log.md` exists beside a newly created `plan.md`.
8. Create `questions.md` beside a newly created `plan.md` using the format in [references/questions-format.md](references/questions-format.md). Populate it with any open questions identified during planning. If no questions exist, set `Status: NONE` and note that explicitly.
9. Preserve uncertainty. Record assumptions, constraints, risks, and open questions in both `plan.md` and `questions.md` rather than inventing certainty.
10. Do not create optional artifacts unless another active skill or workflow requires them:
    - `complaining.md`
    - `thinking.md`
    - `evidence.md`
    - `handover/`
11. Report the exact paths of `plan.md`, `implementation-log.md`, and `questions.md` to the user.

## Plan Quality Bar

A valid rails-planning plan is concrete enough that another agent or developer can execute it without reconstructing intent from chat history.

Include:

- task metadata and linked context
- objective and problem summary
- in-scope and out-of-scope boundaries
- current repository state
- assumptions and constraints
- likely files, modules, interfaces, or subsystems affected
- sequenced implementation steps
- automated and manual verification strategy
- risks, unknowns, and open questions
- acceptance or completion checklist
- notes for the implementing agent

Avoid:

- chat-only plans
- IDE-local hidden plans
- vague checklists with no repository grounding
- invented certainty
- plans that do not explain how to validate completion
- accidental duplicates of active related plans

## IDE Rule

Any IDE may keep transient internal task state, but the durable plan of record must be the repository file:

```text
context/implementation-plans/<task-folder>/plan.md
```

For Codex, Claude Code, Cursor, Windsurf, Cascade, and similar IDEs, materialize the plan file before implementation begins when the work needs durable planning.

## Validation

Before considering this skill applied correctly, confirm:

- `plan.md` exists inside the target repository.
- `plan.md` is under the repository's implementation-plans folder.
- The plan is not only in chat, IDE history, or an external folder.
- The plan follows the Tier 4 implementation-plan structure or a stronger local template.
- Relevant maintained context is linked where available.
- The plan includes scope, steps, validation, risks, and open questions.
- `implementation-log.md` exists beside `plan.md` for new plan folders.
- `questions.md` exists beside `plan.md` for new plan folders and is either populated with open questions or explicitly marked `Status: NONE`.
- Any open questions in `questions.md` are also reflected in the plan's `Risks And Open Questions` section.
- Existing related plans were reused or intentionally superseded instead of duplicated accidentally.
- The user was told the exact paths of `plan.md`, `implementation-log.md`, and `questions.md`.
