---
name: plan-spam-workflow
description: >-
  Use this orchestration skill when turning goals, feature descriptions,
  backlog items, or design notes into many implementation-plan documents. The
  Boss builds a durable planning queue, dispatches one subagent per goal or
  feature cluster, writes plans, updates progress, and repeats until complete.
metadata:
  version: "1.0"
---

# Plan Spam Workflow (Boss)

You are the **Boss**.

You read the source material.
You build the queue.
You locate the correct template.
You prepare the shared questions file.
You spawn the planners.
You verify the files.
You update progress.
You repeat.

Do not silently skip the worker step.
Do not silently skip the template step.
Do not silently skip the questions step.
Do not silently skip the progress update step.
Do not silently skip output verification.

## Purpose

- Use this workflow when the user wants a batch of implementation plans generated from goals, feature descriptions, backlog items, brainstorming notes, milestone checklists, or design documents.
- Use this workflow when the work should be split into one-plan-per-goal or one-plan-per-tight-feature-cluster through subagents.
- Use this workflow when the target output is a folder full of implementation-plan markdown files rather than direct code changes.
- Use this workflow when each generated plan must be grounded in concrete Tier 4 context rather than vague feature summaries.

## Artifact root (target repository)

All paths are relative to the **target** repository root (the project receiving the plans, not necessarily this tooling repository).

Path conventions below follow the [`agentic_starter`](../../agentic_starter/) project structure. If the target repository uses different documentation folder conventions, adjust these paths before dispatching workers.

| Path | Role |
| --- | --- |
| `documentation/workflows/plan_spam/briefing.md` | Durable summary of source documents, extraction choices, template source, and ordered planning queue |
| `documentation/workflows/plan_spam/progress.md` | Durable planning queue and current state |
| `documentation/workflows/plan_spam/questions.md` | Shared goal-scoped clarifying questions collected during bulk planning so the user can answer them later |
| `documentation/workflows/plan_spam/logs/` | Blocked notes, worker failures, retry notes, naming collisions |
| `documentation/implementation_plans/` | Default output folder for generated implementation-plan files |

Create these directories and files on first run.
If the target repository already has an established implementation-plans folder, preserve that location instead of forcing a rename.
Do not delete durable state on resume unless the user explicitly asks for a clean run.

## References and contracts

| Role | Path from this repository root |
| --- | --- |
| Progress state model | `skills/plan-spam-workflow/references/state-model.md` |
| Default Tier 4 implementation-plan template | `skills/plan-spam-workflow/references/tier-4-implementation-plan-template.md` |
| Shared questions file format | `skills/plan-spam-workflow/references/questions-file-format.md` |

If the user explicitly names a Tier 4 plan template inside the target repository, that template overrides the bundled default.
If the target repository already contains a clearly established Tier 4 implementation-plan template, use it instead of the bundled default.
If no repository-local template exists, use the bundled default template reference.

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
- Build or refresh `briefing.md` before dispatching the first worker.
- Build or refresh `progress.md` before dispatching the first worker.
- Build or refresh `questions.md` before dispatching the first worker.
- Resolve the Tier 4 template source before dispatching the first worker.
- Spawn at least one subagent for each goal or tightly-bound feature cluster. Do not replace the worker step with a Boss-only planning pass.
- Default to one goal or feature description per plan file.
- Only batch multiple items into one plan when the user clearly wants one combined delivery slice or the items are tightly bound and would create a worse plan if split.
- Every worker must read the exact source material for its assigned goal and the exact Tier 4 template source before writing the plan.
- Every worker must create or update exactly one target implementation-plan file unless the Boss explicitly assigned a grouped plan.
- Every worker must ask clarifying questions instead of guessing when key context is missing, ambiguous, or risky.
- Every worker must ensure those questions are recorded in the shared `documentation/workflows/plan_spam/questions.md` file with the exact goal id.
- Every worker must keep planning forward where possible, but must mark uncertainty explicitly in the plan instead of hallucinating confidence.
- Workers generate planning artifacts, not production code. Do not let the planning worker wander into direct implementation.
- After every accepted worker completion, update `progress.md`.
- After every accepted worker completion, ensure the shared questions file reflects that worker's current open questions or explicitly says none.
- If a goal is blocked, mark it blocked in `progress.md`, write a note under `logs/`, and do not pretend the plan exists.

## Goal extraction rules

- If the source material already has named goals, milestones, checklist items, backlog ids, or feature ids, preserve those identifiers exactly.
- If the user explicitly requested a subset of goals, queue only that subset.
- If the source documents define dependencies or order, preserve that order.
- If no explicit ids exist, create stable synthetic ids such as `PLAN-001`, `PLAN-002`, and `PLAN-003`.
- Prefer one output plan file per goal id.
- When the input is a plain feature paragraph with no ids, derive a short stable title and slug from the feature intent.

## Output naming rules

- Use one markdown file per queued goal or grouped plan.
- Prefer filenames in the form `NNN-short-goal-slug-implementation-plan.md`.
- If the source already uses a stable goal id, include it in the title and inside the plan body even if the filename is slug-based.
- Never overwrite an unrelated existing plan. If a collision exists, either update the matching plan intentionally or choose a new disambiguated filename and note it in `progress.md`.

## Briefing file

Write or refresh `documentation/workflows/plan_spam/briefing.md` with:

- The exact source documents read for this run
- A short note for each source document describing why it matters
- The exact Tier 4 template source selected for this run
- The ordered list of goals or feature slices selected for this run
- The output folder for generated plans
- The shared questions file path
- Any hard constraints, sequencing rules, or batching decisions

Keep `briefing.md` concise.
`briefing.md` is a durable run summary, not a replacement for the source documents.

## Progress file

Write or refresh `documentation/workflows/plan_spam/progress.md` as a table like this:

| Status | Goal | Source | Output Plan | Template | Notes |
| --- | --- | --- | --- | --- | --- |
| TODO | GOAL 2.1 | `Documentation/milestones.md` | `documentation/implementation_plans/002-goal-2-1-implementation-plan.md` | `skills/plan-spam-workflow/references/tier-4-implementation-plan-template.md` | queued |

Use the status values from [references/state-model.md](references/state-model.md).
Only the Boss updates the `Status` column.

## Shared questions file

Write or refresh `documentation/workflows/plan_spam/questions.md` using the format in [references/questions-file-format.md](references/questions-file-format.md).

Before dispatching workers, pre-create one section per queued goal or grouped plan so each worker has a stable place to record questions.
Every question entry must include the exact goal id.
If a worker has no questions, that worker should explicitly record that no open questions remain for its section.

The shared questions file exists so the user can walk away during bulk planning, then return later with answers that a regular chat agent can use to revise the plans.

## Execution loop

1. **Init**  
   Ensure `documentation/workflows/plan_spam/`, `briefing.md`, `progress.md`, `questions.md`, `logs/`, and the target implementation-plans folder exist on the target repository.

2. **Read source documents**  
   Read every source document the user named. Read higher-level design or milestone context before lower-level goal lists when both exist. Do not dispatch a worker before this step is complete.

3. **Resolve template**  
   Determine the exact Tier 4 template source for the run:
   - user-specified template path wins
   - otherwise repository-local established template wins
   - otherwise use `skills/plan-spam-workflow/references/tier-4-implementation-plan-template.md`

4. **Extract constraints and queue**  
   Determine:
   - the ordered goals or feature slices for this run
   - the output folder
   - the desired batching
   - any sequencing constraints
   - any collision handling requirements for existing plan files

5. **Write durable state**  
   Refresh `briefing.md`. Refresh or initialize `progress.md`. Refresh or initialize `questions.md` with one goal-scoped section per queued row. Resume from existing `progress.md` if a run is already in flight.

6. **Select next goal**  
   Pick the next `TODO` row whose dependencies are satisfied. If the user requested a specific order, honor that order exactly.

7. **Dispatch one worker**  
   Set that row to `DOING` in `progress.md`, then spawn one subagent for that goal or grouped slice. Pass the required source docs, the exact goal id, the exact output path, the exact template path, the shared questions file path, and the return format. Do not skip the worker.

8. **Review worker result**  
   Confirm the worker:
   - stayed inside the assigned goal or grouped slice
   - read the assigned source material
   - used the assigned Tier 4 template source
   - produced the expected implementation-plan file
   - asked clarifying questions instead of guessing when important information was missing
   - recorded those questions under the correct goal section in `questions.md`, or explicitly recorded that none were needed
   - grounded the plan in concrete Tier 4 context instead of vague restatement
   - marked uncertainty clearly inside the plan where answers are still missing
   - reported output path, files changed, and blockers

9. **Update state**  
   - Success: set the row to `DONE` and keep a brief note. A row may still be `DONE` when open questions remain, as long as the plan is useful, the uncertainty is marked honestly, and the questions were captured.
   - Blocked: set the row to `BLOCKED`, add a brief note, and write a log file under `logs/`.
   - Wrong template, wrong file, shallow plan, or missing questions capture after visible uncertainty: do not mark success. Send the work back or mark blocked.

10. **Repeat**  
      Continue until there are no `TODO` rows left for the requested scope or until the remaining rows are blocked.

11. **Report**  
      Tell the user where `briefing.md`, `progress.md`, `questions.md`, and the generated implementation-plan files live, which goals were planned, which were blocked, which template source was used, and every open clarifying question grouped by goal id.

## Worker dispatch requirements

Every worker prompt must include all of the following:

- The exact goal id or synthetic id to plan
- The exact source document paths to read before writing
- The exact output file path for the generated implementation plan
- The exact Tier 4 template path to follow
- The exact shared questions file path and the worker's assigned goal section inside it
- A plain statement that the worker must produce a plan file, not implementation code
- A plain statement that the worker must ask clarifying questions instead of guessing
- A plain statement that the worker must record those questions with the goal id in the shared questions file
- A plain statement that the worker must continue planning as far as possible while clearly marking uncertainty in the plan
- A plain statement that the worker must preserve source constraints and scope boundaries
- A plain statement that the worker must ground the plan in concrete Tier 4 context: likely files, modules, interfaces, validation surfaces, risks, and sequencing
- A plain statement that the worker must report output path, files changed, and blockers

If the runtime makes direct same-file parallel edits unsafe, the worker must still return the exact goal-scoped question block so the Boss can write it into `questions.md` immediately. The questions must still land in the shared questions file before the row is accepted.

Use concrete language.
Repeat the critical requirements in the worker prompt.

Recommended worker wording:

> Read the listed source documents before writing anything.  
> Produce only the assigned implementation plan at the exact output path.  
> Follow the exact Tier 4 template at `skills/plan-spam-workflow/references/tier-4-implementation-plan-template.md` unless another template path was assigned.  
> If anything important is unclear, ask clarifying questions instead of guessing. Record them in the assigned section of `documentation/workflows/plan_spam/questions.md` with the exact goal id.  
> Do not implement the feature. Write the plan only.  
> Keep going as far as the available context allows, but mark uncertainty explicitly in the plan anywhere those answers matter.  
> Ground the plan in concrete file-level or subsystem-level context, validation steps, sequencing, and risks.  
> Return the output path, files changed, the question block you wrote, and blockers.

## Parallelism

Default to **parallel** planning when the queued goals are clearly independent because planning files usually do not share code ownership.

Only force sequential execution when any of the following are true:

- the source material defines strict ordered dependencies
- multiple goals intentionally collapse into one grouped plan
- the output filenames or plan bodies would collide
- the same `questions.md` editing approach would create unsafe same-file write conflicts in the current runtime
- the same living source checklist must be updated in lockstep between plans

If those conditions are not clearly true, parallelize aggressively.

## Recovery policy

- `BLOCKED` is durable state.
- Do not silently requeue a blocked row.
- If the user asks to retry, rewrite `BLOCKED` back to `TODO` intentionally and note the retry in `logs/`.
- If a worker produced a shallow or duplicate plan, capture that in `Notes` and either send it back for revision or mark blocked.
- If a worker had unanswered questions but failed to record them, do not quietly patch around that omission.
- If the repository-local template changes mid-run, note the template switch in `briefing.md` and only requeue rows that must be regenerated.
- If the user later answers the collected questions, a regular chat agent can revise the affected plans without rerunning the full bulk-planning pass.

## Standalone uses

This workflow can be used for:

- one explicitly named feature request
- a backlog segment
- a milestone checklist
- a feature dump from chat notes
- a full goals document that needs to be exploded into many implementation plans
