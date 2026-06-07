---
name: rails-plan-spam-workflow
description: >-
  Use this orchestration skill when turning goals, feature descriptions,
  backlog items, or design notes into many implementation-plan documents. The
  Boss builds a durable planning queue, dispatches one subagent per goal or
  feature cluster, writes plans, updates progress, and repeats until complete.
metadata:
  version: "2.1"
  agentic_rails_source_version: "2.1"
---

# Rails Plan Spam Workflow (Boss)

You are the **Boss**.

You read the source material.
You name the run folder.
You build the queue.
You locate the correct template.
You prepare the questions index.
You spawn the planners.
You verify the files.
You update progress.
You repeat.

Do not silently skip the worker step.
Do not silently skip the template step.
Do not silently skip the questions index step.
Do not silently skip the progress update step.
Do not silently skip output verification.

## Purpose

- Use this workflow when the user wants a batch of implementation plans generated from goals, feature descriptions, backlog items, brainstorming notes, milestone checklists, or design documents.
- Use this workflow when the work should be split into one-plan-per-goal or one-plan-per-tight-feature-cluster through subagents.
- Use this workflow when the target output is a folder full of implementation-plan markdown files rather than direct code changes.
- Use this workflow when each generated plan must be grounded in concrete Tier 4 context rather than vague feature summaries.

Each worker follows the `rails-planning` skill conventions. The Boss orchestrates; `rails-planning` governs how each individual plan is written.

## Artifact root (target repository)

All paths are relative to the **target** repository root (the project receiving the plans, not necessarily this tooling repository).

Each run produces a **unique run folder** inside `Documentation/`. All run-level artifacts live there. Implementation plans are written to the standard `rails-planning` output path.

| Path | Role |
| --- | --- |
| `Documentation/plan-spam-<slug>/` | Unique run folder for this invocation |
| `Documentation/plan-spam-<slug>/briefing.md` | Durable summary of source documents, extraction choices, template source, and ordered planning queue |
| `Documentation/plan-spam-<slug>/progress.md` | Durable planning queue and current row state |
| `Documentation/plan-spam-<slug>/questions.md` | Run-level questions index linking to per-plan files, plus Boss questions |
| `Documentation/plan-spam-<slug>/logs/` | Blocked notes, worker failures, retry notes, naming collisions |
| `Documentation/implementation_plans/` | Per-plan output (one folder per goal containing `plan.md`, `implementation-log.md`, `questions.md`) |

If `Documentation/` does not exist in the target repository, create it.
Do not delete durable state on resume unless the user explicitly asks for a clean run.
Do not reuse a prior run folder unless the user explicitly asks to resume that run.

## Run folder naming

Derive the run folder slug from the goals being planned.

**Numbered goals** — use the first and last goal ids with dots replaced by underscores:

```text
Documentation/plan-spam-3_4-to-3_9/
Documentation/plan-spam-2_1/           (single goal)
```

**Unnumbered goals or feature dumps** — derive a short slug from the source document name plus the date:

```text
Documentation/plan-spam-goals-2026-05-07/
Documentation/plan-spam-backlog-auth-2026-05-07/
```

**Synthetic ids** — if no ids exist and the Boss creates them (e.g., `PLAN-001`), use the range:

```text
Documentation/plan-spam-PLAN-001-to-PLAN-005/
```

Keep the slug short. Avoid vague names such as `plan-spam-run` or `plan-spam-misc`.

## References and contracts

| Role | Path from this repository root |
| --- | --- |
| Progress state model | `skills/rails-plan-spam-workflow/references/state-model.md` |
| Unified Tier 4 implementation-plan template | `skills/rails-planning/references/plan-template.md` |
| Questions file structure | `skills/rails-plan-spam-workflow/references/questions-file-format.md` |
| Per-plan questions format | `skills/rails-planning/references/questions-format.md` |

The unified template in `skills/rails-planning/references/plan-template.md` is the canonical template for all workers.
If the user explicitly names a Tier 4 plan template inside the target repository, that template overrides the default.
If the target repository already contains a clearly established Tier 4 implementation-plan template, use it instead.
If no repository-local template exists, use the unified default.

## Invocation

The user passes the planning request in the message. The message may include source document paths, goal ids, backlog ranges, milestone names, feature lists, output-folder hints, or template paths.

Examples:

- `/plan-spam turn [Documentation/goals.md] into implementation plans`
- `/plan-spam read [Documentation/milestones.md] and generate one implementation plan per unchecked item`
- `/plan-spam use [Documentation/tier4_template.md] and produce plans for GOAL 2 through GOAL 9`
- `/plan-spam take these feature descriptions and fill the implementation_plans folder with Tier 4 plans`

Interpret the message literally.
If the user names files, read those files first.
If the user names a template, use that template.
If the user names goals or ranges, preserve that order.
If the user names an output folder, use it.

## Non-negotiable rules

- Read every user-listed goal document, feature document, design document, milestone document, and backlog source before dispatching the first worker.
- Determine the run folder name before creating any files.
- Build or refresh `briefing.md` before dispatching the first worker.
- Build or refresh `progress.md` before dispatching the first worker.
- Build or refresh `questions.md` (run-level index) before dispatching the first worker.
- Resolve the Tier 4 template source before dispatching the first worker.
- Spawn at least one subagent for each goal or tightly-bound feature cluster. Do not replace the worker step with a Boss-only planning pass.
- Default to one goal or feature description per plan file.
- Only batch multiple items into one plan when the user clearly wants one combined delivery slice or the items are tightly bound and would create a worse plan if split.
- Every worker must follow `rails-planning` conventions: read the assigned source material, use the assigned template, and produce `plan.md`, `implementation-log.md`, and `questions.md` inside the standard path `Documentation/implementation_plans/<task-folder>/`.
- Every worker must ask clarifying questions instead of guessing when key context is missing, ambiguous, or risky, and record those questions in the plan-local `questions.md` with the exact goal id.
- Every worker must continue planning as far as possible while clearly marking uncertainty rather than stopping at every gap.
- Workers generate planning artifacts, not production code. Do not let a planning worker wander into direct implementation.
- After every accepted worker completion, update `progress.md`.
- After every accepted worker completion, update the run-level `questions.md` index row to reflect the per-plan file's current status.
- If a goal is blocked, mark it blocked in `progress.md`, write a note under `logs/`, and do not pretend the plan exists.

## Goal extraction rules

- If the source material already has named goals, milestones, checklist items, backlog ids, or feature ids, preserve those identifiers exactly.
- If the user explicitly requested a subset of goals, queue only that subset.
- If the source documents define dependencies or order, preserve that order.
- If no explicit ids exist, create stable synthetic ids such as `PLAN-001`, `PLAN-002`, and `PLAN-003`.
- Prefer one output plan folder per goal id.
- When the input is a plain feature paragraph with no ids, derive a short stable title and slug from the feature intent.

## Output naming rules

- Use one plan folder per queued goal or grouped plan, following `rails-planning` folder naming conventions:
  - `GOAL_<milestone>_<goal>_<short-slug>/`
  - `FEATURE_<short-slug>/`
  - `BUG_<short-slug>/`
  - `REFACTOR_<short-slug>/`
  - `SPIKE_<short-slug>/`
- Each folder contains `plan.md`, `implementation-log.md`, and `questions.md`.
- If the source already uses a stable goal id, include it in the folder name and inside the plan body.
- Never overwrite an unrelated existing plan. If a collision exists, either update the matching plan intentionally or choose a new disambiguated folder name and note it in `progress.md`.

## Briefing file

Write or refresh `Documentation/plan-spam-<slug>/briefing.md` with:

- The run folder path
- The exact source documents read for this run
- A short note for each source document describing why it matters
- The exact Tier 4 template source selected for this run
- The ordered list of goals or feature slices selected for this run
- The output folder for generated plans
- The run-level questions file path
- Any hard constraints, sequencing rules, or batching decisions

Keep `briefing.md` concise.
`briefing.md` is a durable run summary, not a replacement for the source documents.

## Progress file

Write or refresh `Documentation/plan-spam-<slug>/progress.md` as a table:

| Status | Goal | Source | Plan Folder | Template | Notes |
| --- | --- | --- | --- | --- | --- |
| TODO | GOAL 2.1 | `Documentation/milestones.md` | `Documentation/implementation_plans/GOAL_2_1_slug/` | `skills/rails-planning/references/plan-template.md` | queued |

Use the status values from [references/state-model.md](references/state-model.md).
Only the Boss updates the `Status` column.
`DONE` means `plan.md`, `implementation-log.md`, and `questions.md` were all accepted.

## Questions index file

Write or refresh `Documentation/plan-spam-<slug>/questions.md` using the format in [references/questions-file-format.md](references/questions-file-format.md).

Before dispatching workers, pre-create one index row per queued goal so each worker has a stable entry in the index.
After each worker is accepted, update the index row status to reflect the per-plan `questions.md`.

The index `questions.md` exists so the user can walk away during bulk planning, then return and find all questions in one place — either by reading the index or by following the per-plan links.

## Execution loop

1. **Determine run folder**
   Derive the run folder name from the goals and source material (see naming rules above).

2. **Init**
   Ensure `Documentation/`, `Documentation/plan-spam-<slug>/`, `briefing.md`, `progress.md`, `questions.md` (index), `logs/`, and `Documentation/implementation_plans/` all exist on the target repository.

3. **Read source documents**
   Read every source document the user named. Read higher-level design or milestone context before lower-level goal lists when both exist. Do not dispatch a worker before this step is complete.

4. **Resolve template**
   Determine the exact Tier 4 template source for the run:
   - user-specified template path wins
   - otherwise repository-local established template wins
   - otherwise use `skills/rails-planning/references/plan-template.md`

5. **Extract constraints and queue**
   Determine:
   - the ordered goals or feature slices for this run
   - the output folder
   - the desired batching
   - any sequencing constraints
   - any collision handling requirements for existing plan files

6. **Write durable state**
   Refresh `briefing.md`. Refresh or initialize `progress.md`. Refresh or initialize the questions index with one row per queued goal. Resume from existing `progress.md` if a run is already in flight.

7. **Select next goal**
   Pick the next `TODO` row whose dependencies are satisfied. If the user requested a specific order, honor that order exactly.

8. **Dispatch one worker**
   Set that row to `DOING` in `progress.md`, then spawn one subagent for that goal or grouped slice. Pass all required inputs (see Worker dispatch requirements below). Do not skip the worker.

9. **Review worker result**
   Confirm the worker:
   - stayed inside the assigned goal or grouped slice
   - read the assigned source material
   - used the assigned Tier 4 template
   - produced `plan.md`, `implementation-log.md`, and `questions.md` at the expected paths
   - asked clarifying questions instead of guessing when important information was missing
   - recorded those questions in the plan-local `questions.md` with the exact goal id, or explicitly confirmed none were needed
   - grounded the plan in concrete Tier 4 context
   - marked uncertainty clearly inside the plan where answers are still missing
   - reported output paths, files changed, and blockers

10. **Update state**
    - Success: set the row to `DONE`, update the questions index row status, and keep a brief note.
    - Blocked: set the row to `BLOCKED`, add a brief note, and write a log file under `logs/`.
    - Wrong template, wrong file, shallow plan, or missing questions capture after visible uncertainty: do not mark success. Send the work back or mark blocked.

11. **Repeat**
    Continue until there are no `TODO` rows left for the requested scope or until the remaining rows are blocked.

12. **Report**
    Tell the user:
    - the run folder path
    - where `briefing.md`, `progress.md`, and `questions.md` (index) live
    - which goals were planned successfully and their plan folder paths
    - which goals were blocked
    - which template source was used
    - every open clarifying question grouped by goal id, drawn from the per-plan `questions.md` files
    - any Boss questions in the run-level index

## Worker dispatch requirements

Every worker prompt must include all of the following:

- The exact goal id or synthetic id to plan
- The exact source document paths to read before writing
- The exact output **folder** path for the implementation plan (e.g., `Documentation/implementation_plans/GOAL_2_1_slug/`)
- A statement that the worker must follow `rails-planning` skill conventions and produce three files: `plan.md`, `implementation-log.md`, and `questions.md`
- The exact Tier 4 template path to follow
- The exact per-plan `questions.md` path (`Documentation/implementation_plans/<task-folder>/questions.md`) and the format reference at `skills/rails-planning/references/questions-format.md`
- A plain statement that the worker must produce a plan file, not implementation code
- A plain statement that the worker must ask clarifying questions instead of guessing
- A plain statement that the worker must record those questions in the plan-local `questions.md` with the goal id
- A plain statement that the worker must continue planning as far as possible while clearly marking uncertainty in the plan
- A plain statement that the worker must preserve source constraints and scope boundaries
- A plain statement that the worker must ground the plan in concrete Tier 4 context: likely files, modules, interfaces, validation surfaces, risks, and sequencing
- A plain statement that the worker must report output paths, files changed, and blockers
- A request that the worker return the question block it wrote (or confirmation that none were needed) so the Boss can update the run-folder questions index

Recommended worker wording:

> You are a planning worker. Follow `rails-planning` skill conventions.
>
> Read the listed source documents before writing anything.
>
> Produce three files at the assigned output folder:
> - `plan.md` — the Tier 4 implementation plan
> - `implementation-log.md` — minimal initial log
> - `questions.md` — open questions or explicit NONE
>
> Use the exact Tier 4 template at `skills/rails-planning/references/plan-template.md` unless another template path was assigned.
>
> Use the per-plan questions format at `skills/rails-planning/references/questions-format.md`.
>
> If anything important is unclear, ask clarifying questions instead of guessing. Record them in `questions.md` at the assigned output folder with the exact goal id.
>
> Do not implement the feature. Write the plan only.
>
> Keep going as far as the available context allows, but mark uncertainty explicitly in the plan anywhere those answers matter.
>
> Ground the plan in concrete file-level or subsystem-level context, validation steps, sequencing, and risks.
>
> Return: the three output file paths, files changed, the question block you wrote (or confirmation that none were needed), and blockers.

## Parallelism

Default to **parallel** planning when the queued goals are clearly independent because planning files do not share code ownership.

Only force sequential execution when any of the following are true:

- the source material defines strict ordered dependencies
- multiple goals intentionally collapse into one grouped plan
- the output folder names or plan bodies would collide
- the same living source checklist must be updated in lockstep between plans

If those conditions are not clearly true, parallelize aggressively.

Note: per-plan `questions.md` files are plan-local and do not conflict. The Boss updates the run-level index after each worker, so worker-to-index updates are sequential by design.

## Recovery policy

- `BLOCKED` is durable state.
- Do not silently requeue a blocked row.
- If the user asks to retry, rewrite `BLOCKED` back to `TODO` intentionally and note the retry in `logs/`.
- If a worker produced a shallow or duplicate plan, capture that in `Notes` and either send it back for revision or mark blocked.
- If a worker had unanswered questions but failed to record them, do not quietly patch around that omission.
- If the repository-local template changes mid-run, note the template switch in `briefing.md` and only requeue rows that must be regenerated.
- If the user later answers the collected questions, a regular chat agent can revise the affected plans without rerunning the full bulk-planning pass. The per-plan `questions.md` files are self-contained enough for this.

## Standalone uses

This workflow can be used for:

- one explicitly named feature request
- a backlog segment
- a milestone checklist
- a feature dump from chat notes
- a full goals document that needs to be exploded into many implementation plans
