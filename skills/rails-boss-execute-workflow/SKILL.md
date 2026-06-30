---
name: rails-boss-execute-workflow
description: >-
  Use this orchestration skill when implementing work from design documents,
  milestone documents, goal lists, or implementation plans. The Boss reads the
  supplied documents, builds a durable goal queue, dispatches one subagent per
  goal or tightly bound plan slice, enforces specialist agents when required,
  updates progress, and repeats until the requested work is done or blocked.
disable-model-invocation: true
metadata:
  version: "1.5"
---

# Rails Boss Execute Workflow

You are the **Boss**.

You read the source documents.
You build the queue.
You spawn the workers.
You verify the result.
You update the progress file.
You mark source goals complete.
You repeat.

Do not silently skip the worker step.
Do not silently skip the commit step.
Do not silently skip the progress update step.
Do not silently skip the goal-marking step.

## Purpose

- Use this workflow when the user wants implementation work done from one or more design documents, milestone documents, goal documents, or implementation-plan documents.
- Use this workflow when the work should be done through subagents instead of one large direct implementation pass.
- Use this workflow when the work is naturally split into goals, checklist items, milestones, or ordered plan slices.
- Use this workflow for a single goal, a short ordered set of goals, or a larger multi-document delivery pass.

## Artifact root (target repository)

All paths are relative to the **target** repository root (the project being implemented, not necessarily this tooling repository).

Path conventions below follow the Agentic Rails context structure. If the target repository uses different context or documentation folder conventions, adjust these paths before dispatching workers and record the chosen path in `briefing.md`.

| Path | Role |
| --- | --- |
| `context/rails-boss-execute/briefing.md` | Durable summary of source documents, extracted constraints, required persona, and ordered goal queue |
| `context/rails-boss-execute/progress.md` | Durable execution queue and current state |
| `context/rails-boss-execute/logs/` | Blocked notes, worker failures, recovery notes |

Create these directories and files on first run.
Do not delete them on resume unless the user explicitly asks for a clean run.

## Skills and agent contracts

| Role | Path from this repository root |
| --- | --- |
| Commit wording skill for every worker | `skills/commit-log/SKILL.md` |
| Optional specialist worker contract | `agents/<agent-name>/AGENT.md` |
| Example specialist worker contract | `agents/wpf-persona/AGENT.md` |

Supporting reference: **state transitions**: [references/state-model.md](references/state-model.md).

## Invocation

The user passes the work request in the message. The message may include source document paths, plan paths, goal ids, goal ranges, or ordered goals.

Examples:

- `/rails-boss-execute review [context/design.md] [context/milestones.md] then follow [context/implementation-plans/feature/plan.md] with subagents`
- `/rails-boss-execute implement GOAL 1.2 and then GOAL 1.3 with subagents and mark them off as you go`
- `/rails-boss-execute read these design docs first, then implement the requested plan steps with workers`

Interpret the message literally.
If the user names files, read those files first.
If the user names goals, keep that goal order.
If the user names a plan file, extract goals from that plan file.
If the user names both source docs and plan docs, read the source docs first and the plan docs second.

## Non-negotiable rules

- Read every user-listed design, milestone, goal, and plan document before dispatching the first worker.
- Build or refresh `briefing.md` before dispatching the first worker.
- Build or refresh `progress.md` before dispatching the first worker.
- Spawn at least one subagent for each goal or tightly-bound plan slice. Do not replace that worker step with Boss implementation.
- Default to one goal per worker. Only batch multiple items into one worker when they are tightly bound, in the same file area, and clearly intended to land together.
- If the source material says a specialist agent persona must be used, that instruction is mandatory. Pass that agent contract path to every relevant worker. Do not omit it.
- If the source material says to use the WPF agent persona, use `agents/wpf-persona/AGENT.md`. Do not omit it.
- Every worker must load `skills/commit-log/SKILL.md` before finishing.
- Every worker that made changes must make a real commit before returning. The commit message must come from the `commit-log` skill contract. Do not skip the real commit.
- Do not accept a worker as complete if it changed files and did not make a real commit.
- After every successful worker completion, update `progress.md`.
- After every successful worker completion, mark the corresponding goal complete in the source plan or goal file when that file uses checkboxes or explicit goal status markers.
- If a goal is blocked, mark it blocked in `progress.md`, write a note under `logs/`, and do not pretend the goal is done.
- Before dispatching workers, state the selected parallelism level to the user as a concrete maximum number of concurrent subagents.

## Goal extraction rules

- If the plan document already has named goals, steps, milestones, or checklist items, preserve those identifiers exactly.
- If the user explicitly requested a subset of goals, queue only that subset.
- If the source documents define dependencies or order, preserve that order.
- If no explicit goal ids exist, create stable synthetic ids such as `STEP-001`, `STEP-002`, and `STEP-003`.
- If both a design document and a plan document exist, the design document provides context and constraints while the plan document provides the execution order unless the user says otherwise.

## Briefing file

Write or refresh `context/rails-boss-execute/briefing.md` with:

- The exact source documents read for this run
- A short note for each source document describing why it matters
- Any mandatory specialist agent persona named by the user or the source documents
- The selected parallelism level and why that level was chosen
- The ordered list of goals or plan slices selected for this run
- Any hard constraints, acceptance notes, or sequencing rules extracted from the documents

Keep `briefing.md` concise.
`briefing.md` is a durable run summary, not a replacement for the source documents.

## Progress file

Write or refresh `context/rails-boss-execute/progress.md` as a table like this:

| Status | Goal | Source | Persona | Commit | Notes |
| --- | --- | --- | --- | --- | --- |
| TODO | GOAL 1.2 | `context/implementation-plans/example/plan.md` | `agents/wpf-persona/AGENT.md` |  | queued |

Use the status values from [references/state-model.md](references/state-model.md).
Only the Boss updates the `Status` column.
Use the `Commit` column for the worker's actual commit SHA after success.

## Execution loop

1. **Init**  
   Ensure `context/`, `context/rails-boss-execute/`, `progress.md`, `briefing.md`, and `logs/` exist on the target repository.

2. **Read source documents**  
   Read every source document the user named. Read design and milestone context first. Read plan and implementation files second. Do not dispatch a worker before this step is complete.

3. **Extract constraints and goals**  
   Determine:
   - the ordered goals for this run
   - any mandatory agent persona
   - any sequencing constraints
   - any explicit user requirement to update source checklists or goal markers
   - the requested or safest parallelism level

4. **Write durable state**  
   Refresh `briefing.md`. Refresh or initialize `progress.md`. Resume from existing `progress.md` if a run is already in flight.

5. **Announce parallelism**
   Tell the user the selected parallelism level before dispatching workers. Use a concrete form such as `Parallelism: 0 (serial, max 1 active subagent)` or `Parallelism: 4 (max 4 active subagents)`.

6. **Select next goal**  
   Pick the next `TODO` goal whose dependencies are satisfied. If the user requested a specific order, honor that order exactly.

7. **Dispatch worker or worker batch**  
   Select up to the announced maximum number of eligible `TODO` rows. Set selected rows to `DOING` in `progress.md`, then spawn one subagent per selected goal or tightly-bound plan slice. Pass each worker its required source docs, goal id, required persona, commit requirement, and return format. Do not skip the worker.

8. **Review worker result**  
   Confirm the worker:
   - stayed inside the assigned goal
   - used the required specialist persona if one was mandatory
   - ran whatever validation was reasonable for the assigned change
   - made a real commit if files changed
   - returned the commit SHA, changed files, tests run, and blockers

9. **Update state**  
   - Success: set the row to `DONE`, record the commit SHA, keep a brief note.
   - Blocked: set the row to `BLOCKED`, add a brief note, and write a log file under `logs/`.
   - Missing commit after changed files: do not mark success. Send the work back or mark blocked.

10. **Mark source goals complete**  
   If the source plan or goal file uses checkboxes, mark the completed item checked only after the worker is truly `DONE`.
   If the source plan uses another explicit status marker, update that status only after the worker is truly `DONE`.

11. **Repeat**  
      Continue until there are no `TODO` rows left for the requested scope or until the remaining goals are blocked.

12. **Report**  
      Tell the user where `briefing.md` and `progress.md` live, the parallelism level used, which goals are done, which goals are blocked, and which commits landed.

## Worker dispatch requirements

Every worker prompt must include all of the following:

- The exact goal id or step id to implement
- The exact source document paths to read before coding
- A plain statement that the worker must implement only the assigned goal or tightly-bound slice
- The exact specialist agent contract path to use, or an explicit statement that no specialist agent contract is required
- The exact path `skills/commit-log/SKILL.md`
- A plain statement that the worker must load `commit-log`, generate the commit message from that skill, and make a real commit before returning if files changed
- A plain statement that the worker must report commit SHA, changed files, tests run, and blockers
- A plain statement that the worker must not silently skip the commit

Use concrete language.
Repeat the critical requirements in the worker prompt.

Recommended worker wording:

> Read the listed source documents before making changes.  
> Implement only GOAL X.Y.  
> Use this specialist agent contract if required: `agents/wpf-persona/AGENT.md`.  
> Before you finish, load `skills/commit-log/SKILL.md`, generate the commit message from that skill, and make a real commit if you changed files.  
> Return the commit SHA, files changed, tests run, and blockers.

## Parallelism

The Boss must state the selected parallelism level to the user before worker dispatch and again in the final report. State it as a concrete maximum number of concurrently active subagents.

Default behavior: use judgment. Choose the safest useful level after reading the source material, dependency order, file ownership, commit requirements, and user instructions.

Use these terms:

- `Parallelism: 0` means serial execution. Run exactly one active subagent at a time, despite the numeric level being zero.
- `Parallelism: N` means run up to `N` active subagents concurrently.

## Zero Parallelism

If the user asks for zero parallelism, no parallelism, serial execution, Ralph-loop style execution, or one worker at a time, use `Parallelism: 0`.

In zero-parallelism mode:

- Spawn one subagent for the next eligible goal.
- Let that subagent finish its assigned goal completely.
- Require validation and the real commit, if files changed, before accepting the worker.
- Dispose of that subagent's context by ending that worker interaction before starting the next worker.
- Update `progress.md`, source goal markers, and logs before spawning the next subagent.
- Repeat for as many goals as needed, even if the run spans dozens of goals and takes hours.

This mode intentionally trades wall-clock speed for clean context windows, simpler review, and lower merge or commit risk.

## Heavy Parallelism

If the user asks for heavy parallelism, high parallelism, maximum safe parallelism, or many workers at once, the Boss must work harder before dispatch:

- Build the full queue before worker dispatch.
- Identify dependencies, strict ordering constraints, shared files, shared tests, shared documentation checkboxes, and likely merge conflicts.
- Partition goals into safe concurrent batches.
- Choose the maximum number of active subagents that can run without violating dependencies, file ownership, checklist updates, or commit cleanliness.
- State that maximum to the user before dispatch.
- Keep Boss-owned state updates (`progress.md`, source checklist/status updates, and run logs) serialized even when workers run concurrently.

Only run multiple workers concurrently when all of the following are true:

- the goals are clearly independent
- the file ownership is disjoint or otherwise safe
- the plan document does not require strict serial order
- each worker can still make its own real commit cleanly

If those conditions are not clearly true, lower the parallelism level. If uncertainty remains material, use `Parallelism: 0`.

## Recovery policy

- `BLOCKED` is durable state.
- Do not silently requeue a blocked goal.
- If the user asks to retry, rewrite `BLOCKED` back to `TODO` intentionally and note the retry in `logs/`.
- If the worker reports that no code change was needed, capture that in `Notes` and only mark `DONE` when the goal really was satisfied.

## Standalone uses

This workflow can be used for:

- one explicitly named goal
- an ordered list of goals
- a full implementation plan
- a design-doc-plus-plan sequence
- milestone-driven delivery where each milestone expands into concrete goals
