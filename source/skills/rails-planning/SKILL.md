---
name: rails-planning
description: >-
  Use this skill when creating, revising, locating, or enforcing implementation
  plans inside an Agentic Rails project. Use for implementation plans, work
  plans, execution plans, feature plans, bug plans, repository planning before
  coding, IDE planning drift, or any planning output that should survive across
  IDEs, machines, branches, sessions, reviews, retrospectives, execution logs,
  evidence, complaints, or handovers. The skill ensures plans are written into
  the target repository under context/implementation-plans/<milestone-slug>/
  <story-slug>/, producing one primary artifact — plan.md — with CER, questions,
  evidence, complaints, execution log, and completion review folded into it by
  default. Can also produce opt-in sidecars (evidence.md, complaining.md,
  thinking.md) beside plan.md when a story genuinely needs durable, separately
  tracked provenance.
disable-model-invocation: false
metadata:
  version: "2.0"
---

# Rails Planning

Force implementation planning to live in the target repository, not in IDE-local state, hidden assistant folders, chat history, or machine-specific storage.

This is the single-plan enforcement skill for Agentic Rails. It creates or revises durable Implementation Plan artifacts. It does not implement production code.

`rails-planning` itself belongs to the right rail: reusable agentic behavior. Its output belongs to the left rail: project-local context and provenance.

## Core Rule

Every story gets **one primary artifact**:

```text
context/implementation-plans/<milestone-slug>/<story-slug>/plan.md
```

`plan.md` integrates CER, questions/unknowns, evidence/references, complaints/friction, execution log, and completion review as sections inside the one file — see [references/plan-template.md](references/plan-template.md). Do not produce separate `questions.md`, `evidence.md`, `complaining.md`, `thinking.md`, `implementation-log.md`, or `completion-review.md` files by default. `thinking.md` is the one exception that is never a `plan.md` section — see [references/plan-template.md](references/plan-template.md)'s `thinking.md` Sidecar note.

Only create one of those sidecar files when:

- the user explicitly asks for it, or
- the story is large or phased enough that a durable, separately-tracked file is genuinely justified (the same threshold `rails-planning-phaser` uses for splitting a plan into phases is a reasonable signal).

When a sidecar file is created, it lives beside `plan.md` in the same story folder, never in `context/` root.

All artifacts must be normal repository files that the human can review, diff, branch, commit, copy, and preserve with the project.

## When To Apply

Apply this skill when the user asks for one implementation plan or wants IDE planning redirected into Agentic Rails. Typical triggers include:

- Planning before coding in Codex, Claude Code, Cursor, Windsurf, Cascade, or another agentic IDE.
- Creating or revising a story, feature, bug, refactor, spike, work item, or execution plan.
- Making planning output durable across machines, IDEs, branches, sessions, reviews, or retrospectives.
- Preparing context that will later feed the plan's `## Execution Log`, `## Completion Review`, `## Complaints / Friction`, `## Evidence / References`, or a handover artifact.
- Fixing hidden, scattered, disconnected, or lost IDE-local plans.

Do not apply this skill when the user explicitly wants only a quick chat outline, the plan is unrelated to repository implementation work, the task is trivial enough that a durable plan would be noise, or another active workflow explicitly owns the output location.

Use `rails-plan-spam-workflow` instead when the user wants many plans generated from stories, backlog items, feature dumps, or milestone checklists.

## Repository Detection

1. Identify the target repository root.
2. Treat the repository as Agentic Rails when any of these exist:
   - `AGENTIC_RAILS.md`
   - `.agentic-rails.json`
   - `AGENTIC_RAILS_README.MD`
   - `context/implementation-plans/`
   - an established context tier system under `context/`
3. If the target repository is not clearly Agentic Rails but the user explicitly asks for this skill, still create repository-local planning artifacts using the path rules below.

## Context Loading

Load only the minimum context needed to write a grounded plan. Prefer maintained context over raw intake:

1. `context/design.md`, including the Milestones Index
2. relevant `context/milestones/*.md`, including the story's own section inside the milestone
3. relevant `context/backlog/*.md` story files, when the story has not yet been pulled into a milestone
4. existing related `context/implementation-plans/**/plan.md`
5. relevant `context/dictations-tier-0/` source only when raw intake materially shaped the work

Dictation is raw intake, not final truth. If dictation contradicts maintained design, milestones, or stories, prefer maintained context and record the contradiction as an open question.

<!-- rails-lint-allow: VC004 -->
<!-- Legacy-path migration note: these are retired paths named so an agent recognizes and
     avoids them, not a live convention. Kept deliberately for that recognition purpose. -->
If an agent encounters `context/milestones.md`, `context/goals*.md`, or `context/tier0/` in an older repository, treat them as old-era migration signals to retire, not current canonical paths.

## Path Selection

Prefer the canonical Agentic Rails path, grouped by milestone:

```text
context/implementation-plans/<milestone-slug>/<story-slug>/
```

Preserve an existing repository convention rather than creating duplicate folders. Accept these existing variants:

```text
context/implementation-plans/
documentation/implementation-plans/
docs/implementation-plans/
```

If an active plan already exists for the same story, update that `plan.md` instead of creating a duplicate. Preserve existing decisions unless the user asks for a revision, add a short revision note when useful, and do not overwrite its `## Execution Log` history.

## Folder Naming

```text
context/implementation-plans/<milestone-slug>/<story-slug>/
```

Slug rules (both `milestone-slug` and `story-slug`):

- Use lowercase words separated by hyphens.
- Keep the slug short but recognizable.
- Avoid vague names such as `new-plan`, `task`, or `implementation`.
- Include a story id when one exists (e.g. `3-4-normalize-settings-loading`).
- When the story's type matters for discoverability, it may prefix the slug (`bug-fix-login-token-refresh`, `spike-compare-vector-store-options`), but the type prefix is optional — the milestone/story nesting is what matters.

Examples:

```text
context/implementation-plans/milestone-1-dockerize-app/add-report-export-support/
context/implementation-plans/milestone-1-dockerize-app/bug-fix-login-token-refresh/
context/implementation-plans/milestone-2-observability/story-2-3-add-health-checks/
```

If the story does not yet belong to a milestone (for example, it is still sitting in the backlog), resolve its target milestone first — following the Backlog → Milestone flow — before creating the plan folder, since the folder path requires a milestone slug.

## Operating Model

1. Detect the target repository root and whether it follows Agentic Rails.
2. Load the minimum maintained context needed to ground the plan.
3. Decide whether the user wants a new plan, a revision, or path enforcement.
4. Search existing implementation-plan folders for related active plans.
5. Resolve the story's milestone, then select or create the correct `<milestone-slug>/<story-slug>/` folder.
6. Create or update `plan.md` using the structure from [references/plan-template.md](references/plan-template.md), unless the repository has a stronger local template.
7. Populate CER, `## Questions / Unknowns`, and `## Risk Mitigation` inline in `plan.md`. Preserve uncertainty — record assumptions, constraints, risks, and open questions rather than inventing certainty.
8. Do not create `questions.md`, `evidence.md`, `complaining.md`, `thinking.md`, `implementation-log.md`, or `completion-review.md` unless the user explicitly requests one or the story is large/phased enough to justify it (see Core Rule). When creating any of them, use [references/questions-format.md](references/questions-format.md) for the questions format.
9. Leave `## Execution Log` and `## Completion Review` absent (or clearly marked not-yet-started) for a plan that has not begun execution — they are filled in during and after execution, not at plan-creation time.
10. Report the exact path of `plan.md` to the user, plus the path of any sidecar file actually created.

## Plan Quality Bar

A valid rails-planning plan is concrete enough that another agent or developer can execute it without reconstructing intent from chat history.

Include:

- task metadata and linked context (milestone, story, backlog source)
- CER (complexity, effort, risk) and routing intent
- objective, scope, and non-goals
- current understanding of the repository state, including likely files, modules, interfaces, or subsystems affected
- assumptions and constraints
- sequenced execution steps
- automated and manual verification strategy, plus acceptance criteria
- risks and mitigation, and open questions/unknowns
- an execution log and completion review once execution starts and finishes, respectively

Avoid:

- chat-only plans
- IDE-local hidden plans
- vague checklists with no repository grounding
- invented certainty
- plans that do not explain how to validate completion
- accidental duplicates of active related plans
- a cluster of default sidecar files where the plan's own sections would do

## IDE Rule

Any IDE may keep transient internal task state, but the durable plan of record must be the repository file:

```text
context/implementation-plans/<milestone-slug>/<story-slug>/plan.md
```

For Codex, Claude Code, Cursor, Windsurf, Cascade, and similar IDEs, materialize the plan file before implementation begins when the work needs durable planning.

## Validation

Before considering this skill applied correctly, confirm:

- `plan.md` exists inside the target repository, under the milestone/story implementation-plans path.
- The plan is not only in chat, IDE history, or an external folder.
- The plan follows the implementation-plan structure in [references/plan-template.md](references/plan-template.md) or a stronger local template.
- Relevant maintained context is linked where available.
- The plan includes CER, scope, steps, validation, risk mitigation, and open questions/unknowns.
- No `questions.md`, `evidence.md`, `complaining.md`, `thinking.md`, `implementation-log.md`, or `completion-review.md` was created unless explicitly requested or genuinely justified by story size/phasing.
- Existing related plans were reused or intentionally superseded instead of duplicated accidentally.
- The user was told the exact path of `plan.md`, plus any sidecar file actually created.
