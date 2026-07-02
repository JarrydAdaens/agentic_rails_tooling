---
name: rails-plan-spam-workflow
description: >-
  Use this orchestration skill when turning stories, feature descriptions,
  backlog items, or design notes into many implementation-plan documents. The
  Boss builds a durable planning queue, dispatches one subagent per story or
  feature cluster, writes plans, updates progress, and repeats until complete.
disable-model-invocation: true
metadata:
  version: "3.0"
---

# Rails Plan Spam Workflow (Boss)

You are the **Boss**.

You read the source material.
You resolve each item's target Milestone.
You name the run.
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

- Use this workflow when the user wants a batch of implementation plans generated from stories, feature descriptions, backlog items, brainstorming notes, milestone checklists, or design documents.
- Use this workflow when the work should be split into one-plan-per-story or one-plan-per-tight-feature-cluster through subagents.
- Use this workflow when the target output is a folder full of implementation-plan markdown files rather than direct code changes.
- Use this workflow when each generated plan must be grounded in concrete Implementation Plan context rather than vague feature summaries.

Each worker follows the `rails-planning` skill conventions. The Boss orchestrates; `rails-planning` governs how each individual plan is written, and produces one primary artifact — `plan.md` — per story.

## Artifact root (target repository)

All paths are relative to the **target** repository root (the project receiving the plans, not necessarily this tooling repository).

Durable plans are grouped by milestone. Every queued item must resolve to a target Milestone before it can be queued, because the plan's own path requires the milestone slug — see "Resolve milestone" below.

Each run gets a **run slug**. Temporary, run-scoped artifacts live in a `_planning-runs/<run-slug>/` folder nested under each milestone the run touches, never directly under `context/`. A run that only touches one milestone produces exactly one such folder; a run spanning several milestones produces one per milestone, all sharing the same run slug for traceability.

| Path | Role |
| --- | --- |
| `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/` | Temporary, deletable run-scoped artifacts for this invocation, scoped to one milestone |
| `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/briefing.md` | Durable-for-the-run summary of source documents, extraction choices, template source, and ordered planning queue for this milestone's slice of the run |
| `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/progress.md` | Planning queue and current row state for this milestone's slice of the run |
| `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/questions.md` | Run-level questions index aggregated from each plan's `## Questions / Unknowns` section, plus Boss questions |
| `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/logs/` | Blocked notes, worker failures, retry notes, naming collisions |
| `context/implementation-plans/<milestone-slug>/<story-slug>/plan.md` | The durable per-story output — one primary artifact per story |

Deleting a `_planning-runs/<run-slug>/` folder after the run is done must never damage a durable `plan.md`. Everything durable that a worker learned belongs inside the plan itself (CER, objective, scope, questions/unknowns, evidence, complaints), not the run-scoped index.

If `context/implementation-plans/` does not exist in the target repository, create it.
Do not delete durable state on resume unless the user explicitly asks for a clean run.
Do not reuse a prior run's artifacts unless the user explicitly asks to resume that run.

## Resolve milestone (before building the queue)

Every queued story needs a milestone-slug before it can be assigned an output path. Resolve it up front:

- If the source material is already a milestone document (`context/milestones/<slug>.md`), that milestone owns every story pulled from it.
- If the source material is a backlog file or feature dump, follow the Backlog → Milestone flow: identify the milestone each story belongs to (an existing one, or one the user names), and note that the story is being pulled from the backlog into that milestone as part of this run.
- If a story's milestone is genuinely ambiguous, ask the user which milestone it belongs to before queuing it. Do not guess a milestone slug.
- Group the queue by resolved milestone-slug. Most runs resolve to a single milestone; treat multi-milestone runs as several milestone-scoped sub-runs sharing one run slug.

## Run slug naming

Derive the run slug from the stories being planned. The same run slug is reused across every milestone-scoped `_planning-runs/` folder this invocation touches.

**Numbered stories** — use the first and last story ids with dots replaced by underscores:

```text
plan-spam-3_4-to-3_9
plan-spam-2_1                (single story)
```

**Unnumbered stories or feature dumps** — derive a short slug from the source document name plus the date:

```text
plan-spam-backlog-2026-05-07
plan-spam-backlog-auth-2026-05-07
```

**Synthetic ids** — if no ids exist and the Boss creates them (e.g., `PLAN-001`), use the range:

```text
plan-spam-PLAN-001-to-PLAN-005
```

Keep the slug short. Avoid vague names such as `plan-spam-run` or `plan-spam-misc`.

## References and contracts

| Role | Path from this repository root |
| --- | --- |
| Progress state model | `skills/rails-plan-spam-workflow/references/state-model.md` |
| Unified implementation-plan template | `skills/rails-planning/references/plan-template.md` |
| Questions index structure | `skills/rails-plan-spam-workflow/references/questions-file-format.md` |

The unified template in `skills/rails-planning/references/plan-template.md` is the canonical template for all workers.
If the user explicitly names a plan template inside the target repository, that template overrides the default.
If the target repository already contains a clearly established implementation-plan template, use it instead.
If no repository-local template exists, use the unified default.

## Invocation

The user passes the planning request in the message. The message may include source document paths, story ids, backlog ranges, milestone names, feature lists, output-folder hints, or template paths.

Examples:

- `/plan-spam turn [context/backlog/backlog-1.md] into implementation plans`
- `/plan-spam read [context/milestones/milestone-1.md] and generate one implementation plan per ready story`
- `/plan-spam use [context/plan_template.md] and produce plans for every story in milestone 2`
- `/plan-spam take these feature descriptions and fill the implementation-plans folder with plans`

Interpret the message literally.
If the user names files, read those files first.
If the user names a template, use that template.
If the user names stories or ranges, preserve that order.
If the user names an output folder, use it.

## Non-negotiable rules

- Read every user-listed story document, feature document, design document, milestone document, and backlog source before dispatching the first worker.
- Resolve each queued item's target milestone before it is added to any queue.
- Determine the run slug before creating any files.
- Build or refresh each involved milestone's `briefing.md` before dispatching the first worker for that milestone.
- Build or refresh each involved milestone's `progress.md` before dispatching the first worker for that milestone.
- Build or refresh each involved milestone's `questions.md` (run-level index) before dispatching the first worker for that milestone.
- Resolve the plan template source before dispatching the first worker.
- Spawn at least one subagent for each story or tightly-bound feature cluster. Do not replace the worker step with a Boss-only planning pass.
- Default to one story or feature description per plan file.
- Only batch multiple items into one plan when the user clearly wants one combined delivery slice or the items are tightly bound and would create a worse plan if split.
- Every worker must follow `rails-planning` conventions: read the assigned source material, use the assigned template, and produce one primary artifact, `plan.md`, inside the standard path `context/implementation-plans/<milestone-slug>/<story-slug>/`.
- Every worker must ask clarifying questions instead of guessing when key context is missing, ambiguous, or risky, and record those questions in the plan's own `## Questions / Unknowns` section with the exact story id.
- Every worker must continue planning as far as possible while clearly marking uncertainty rather than stopping at every gap.
- Workers generate planning artifacts, not production code. Do not let a planning worker wander into direct implementation.
- After every accepted worker completion, update that milestone's `progress.md`.
- After every accepted worker completion, update that milestone's run-level `questions.md` index row from the plan's `## Questions / Unknowns` section.
- If a story is blocked, mark it blocked in `progress.md`, write a note under that milestone's `logs/`, and do not pretend the plan exists.

## Story extraction rules

- If the source material already has named stories, milestones, checklist items, backlog ids, or feature ids, preserve those identifiers exactly.
- If the user explicitly requested a subset of stories, queue only that subset.
- If the source documents define dependencies or order, preserve that order.
- If no explicit ids exist, create stable synthetic ids such as `PLAN-001`, `PLAN-002`, and `PLAN-003`.
- Prefer one output plan folder per story id.
- When the input is a plain feature paragraph with no ids, derive a short stable title and slug from the feature intent.

## Output naming rules

- Use one plan folder per queued story or grouped plan, nested under its resolved milestone:
  ```text
  context/implementation-plans/<milestone-slug>/<story-slug>/
  ```
- `<story-slug>` is a short kebab-case slug; include the source story id inside it when one exists (e.g. `3-4-normalize-settings-loading`), otherwise derive it from the feature intent.
- Each folder contains one primary artifact, `plan.md`. Do not create sidecar files (`questions.md`, `evidence.md`, `complaining.md`, standalone `implementation-log.md` / `completion-review.md`) by default — those stay opt-in per `rails-planning` conventions.
- If the source already uses a stable story id, include it in the folder name and inside the plan body.
- Never overwrite an unrelated existing plan. If a collision exists, either update the matching plan intentionally or choose a new disambiguated folder name and note it in `progress.md`.

## Briefing file

Write or refresh `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/briefing.md` with:

- The milestone this briefing covers, and the run slug
- The exact source documents read for this run
- A short note for each source document describing why it matters
- The exact template source selected for this run
- The ordered list of stories or feature slices selected for this milestone
- The output folder for generated plans
- The run-level questions file path
- Any hard constraints, sequencing rules, or batching decisions

Keep `briefing.md` concise.
`briefing.md` is a run-scoped summary, not a replacement for the source documents, and it is safe to delete once the run's plans are all accepted.

## Progress file

Write or refresh `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/progress.md` as a table:

| Status | Story | Source | Plan Folder | Template | Notes |
| --- | --- | --- | --- | --- | --- |
| TODO | STORY 2.1 | `context/backlog/backlog-1.md` | `context/implementation-plans/milestone-1/story-2-1-slug/` | `skills/rails-planning/references/plan-template.md` | queued |

Use the status values from [references/state-model.md](references/state-model.md).
Only the Boss updates the `Status` column.
`DONE` means `plan.md` was accepted.

## Questions index file

Write or refresh `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/questions.md` using the format in [references/questions-file-format.md](references/questions-file-format.md).

Before dispatching workers, pre-create one index row per queued story so each worker has a stable entry in the index.
After each worker is accepted, update the index row status by reading that plan's `## Questions / Unknowns` section.

The index `questions.md` exists so the user can walk away during bulk planning, then return and find all open questions in one place — either by reading the index or by following the per-plan links straight into each `plan.md`. It is a run-scoped convenience artifact: deleting it loses the aggregated overview, never the underlying questions, which live durably inside each plan.

## Execution loop

1. **Determine run slug**
   Derive the run slug from the stories and source material (see naming rules above).

2. **Resolve milestones**
   Determine the target milestone for every queued item (see "Resolve milestone" above). Group the queue by milestone-slug.

3. **Init**
   For each involved milestone, ensure `context/implementation-plans/<milestone-slug>/`, `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/`, `briefing.md`, `progress.md`, `questions.md` (index), and `logs/` all exist on the target repository.

4. **Read source documents**
   Read every source document the user named. Read higher-level design or milestone context before lower-level backlog story lists when both exist. Do not dispatch a worker before this step is complete.

5. **Resolve template**
   Determine the exact template source for the run:
   - user-specified template path wins
   - otherwise repository-local established template wins
   - otherwise use `skills/rails-planning/references/plan-template.md`

6. **Extract constraints and queue**
   Determine:
   - the ordered stories or feature slices for this run, grouped by milestone
   - the output folder for each
   - the desired batching
   - any sequencing constraints
   - any collision handling requirements for existing plan files

7. **Write durable state**
   For each involved milestone, refresh `briefing.md`. Refresh or initialize `progress.md`. Refresh or initialize the questions index with one row per queued story. Resume from existing `progress.md` if a run is already in flight.

8. **Select next story**
   Pick the next `TODO` row whose dependencies are satisfied. If the user requested a specific order, honor that order exactly.

9. **Dispatch one worker**
   Set that row to `DOING` in `progress.md`, then spawn one subagent for that story or grouped slice. Pass all required inputs (see Worker dispatch requirements below). Do not skip the worker.

10. **Review worker result**
    Confirm the worker:
    - stayed inside the assigned story or grouped slice
    - read the assigned source material
    - used the assigned template
    - produced `plan.md` at the expected path under the resolved milestone
    - asked clarifying questions instead of guessing when important information was missing
    - recorded those questions in the plan's own `## Questions / Unknowns` section with the exact story id, or explicitly confirmed none were needed
    - grounded the plan in concrete implementation context
    - marked uncertainty clearly inside the plan where answers are still missing
    - reported the output path, files changed, and blockers

11. **Update state**
    - Success: set the row to `DONE`, update the questions index row status from the plan's `## Questions / Unknowns` section, and keep a brief note.
    - Blocked: set the row to `BLOCKED`, add a brief note, and write a log file under that milestone's `logs/`.
    - Wrong template, wrong file, shallow plan, or missing questions capture after visible uncertainty: do not mark success. Send the work back or mark blocked.

12. **Repeat**
    Continue until there are no `TODO` rows left for the requested scope or until the remaining rows are blocked.

13. **Report**
    Tell the user:
    - the run slug and which milestone(s) it touched
    - where each involved milestone's `briefing.md`, `progress.md`, and `questions.md` (index) live under `_planning-runs/<run-slug>/`
    - which stories were planned successfully and their plan folder paths
    - which stories were blocked
    - which template source was used
    - every open clarifying question grouped by story id, drawn from each plan's `## Questions / Unknowns` section
    - any Boss questions in the run-level index

## Worker dispatch requirements

Every worker prompt must include all of the following:

- The exact story id or synthetic id to plan
- The resolved milestone-slug for this story
- The exact source document paths to read before writing
- The exact output **folder** path for the implementation plan (e.g., `context/implementation-plans/milestone-1/story-2-1-slug/`)
- A statement that the worker must follow `rails-planning` skill conventions and produce one primary artifact, `plan.md` — no sidecar files by default
- The exact template path to follow
- A plain statement that the worker must produce a plan file, not implementation code
- A plain statement that the worker must ask clarifying questions instead of guessing
- A plain statement that the worker must record those questions in the plan's own `## Questions / Unknowns` section with the story id
- A plain statement that the worker must continue planning as far as possible while clearly marking uncertainty in the plan
- A plain statement that the worker must preserve source constraints and scope boundaries
- A plain statement that the worker must ground the plan in concrete implementation context: likely files, modules, interfaces, validation surfaces, risks, and sequencing
- A plain statement that the worker must report the output path, files changed, and blockers
- A request that the worker return the contents of its `## Questions / Unknowns` section (or confirmation that none were needed) so the Boss can update the run-folder questions index

Recommended worker wording:

> You are a planning worker. Follow `rails-planning` skill conventions.
>
> Read the listed source documents before writing anything.
>
> Produce one primary artifact at the assigned output folder:
> - `plan.md` — the implementation plan, following the unified template
>
> Do not create standalone `questions.md`, `evidence.md`, `complaining.md`, `implementation-log.md`, or `completion-review.md` files. Record open questions in the plan's own `## Questions / Unknowns` section.
>
> Use the exact template at `skills/rails-planning/references/plan-template.md` unless another template path was assigned.
>
> If anything important is unclear, ask clarifying questions instead of guessing. Record them in `## Questions / Unknowns` with the exact story id.
>
> Do not implement the feature. Write the plan only.
>
> Keep going as far as the available context allows, but mark uncertainty explicitly in the plan anywhere those answers matter.
>
> Ground the plan in concrete file-level or subsystem-level context, validation steps, sequencing, and risks.
>
> Return: the output file path, files changed, the contents of `## Questions / Unknowns` (or confirmation that none were needed), and blockers.

## Parallelism

Default to **parallel** planning when the queued stories are clearly independent because planning files do not share code ownership.

Only force sequential execution when any of the following are true:

- the source material defines strict ordered dependencies
- multiple stories intentionally collapse into one grouped plan
- the output folder names or plan bodies would collide
- the same living source checklist must be updated in lockstep between plans

If those conditions are not clearly true, parallelize aggressively.

Note: each plan's `## Questions / Unknowns` section is plan-local and does not conflict with any other plan. The Boss updates the run-level index after each worker, so worker-to-index updates are sequential by design.

## Recovery policy

- `BLOCKED` is durable state.
- Do not silently requeue a blocked row.
- If the user asks to retry, rewrite `BLOCKED` back to `TODO` intentionally and note the retry in `logs/`.
- If a worker produced a shallow or duplicate plan, capture that in `Notes` and either send it back for revision or mark blocked.
- If a worker had unanswered questions but failed to record them, do not quietly patch around that omission.
- If the repository-local template changes mid-run, note the template switch in `briefing.md` and only requeue rows that must be regenerated.
- If the user later answers the collected questions, a regular chat agent can revise the affected plans without rerunning the full bulk-planning pass. Each plan's `## Questions / Unknowns` section is self-contained enough for this.
- Once every row for a milestone is `DONE`, the `_planning-runs/<run-slug>/` folder for that milestone may be deleted without touching any durable plan; offer this to the user rather than deleting it unasked.

## Standalone uses

This workflow can be used for:

- one explicitly named feature request
- a backlog segment
- a milestone checklist
- a feature dump from chat notes
- a full backlog story document that needs to be exploded into many implementation plans
