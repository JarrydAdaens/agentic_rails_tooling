---
name: rails-boss-execute-workflow
description: >-
  Use this orchestration skill when implementing work from design documents,
  milestone documents, backlog stories, or implementation plans. The Boss reads the
  supplied documents, builds a durable story/work queue, dispatches one subagent per
  story or tightly bound plan slice, enforces specialist agents when required,
  updates progress, and repeats until the requested work is done or blocked. Each run
  gets its own named run folder, and the Boss selects an appropriate model per worker.
disable-model-invocation: true
metadata:
  version: "1.6"
---

# Rails Boss Execute Workflow

You are the **Boss**.

You read the source documents.
You build the queue.
You spawn the workers.
You verify the result.
You update the progress file.
You mark source stories complete.
You repeat.

Do not silently skip the worker step.
Do not silently skip the commit step.
Do not silently skip the progress update step.
Do not silently skip the story-marking step.

## Purpose

- Use this workflow when the user wants implementation work done from one or more design documents, milestone documents, story documents, or implementation-plan documents.
- Use this workflow when the work should be done through subagents instead of one large direct implementation pass.
- Use this workflow when the work is naturally split into stories, checklist items, milestones, or ordered plan slices.
- Use this workflow for a single story, a short ordered set of stories, or a larger multi-document delivery pass.

## Artifact root (target repository)

All paths are relative to the **target** repository root (the project being implemented, not necessarily this tooling repository).

Path conventions below follow the Agentic Rails context structure. If the target repository uses different context or documentation folder conventions, adjust these paths before dispatching workers and record the chosen path in `briefing.md`.

Every invocation gets its own **run slug** and its own run folder. Run artifacts are run-scoped and deletable; nothing durable lives in them. A second Boss launched while an earlier run's folder still exists must never inherit that folder's state by accident — it gets a fresh slug unless the user explicitly names a run to resume.

| Path | Role |
| --- | --- |
| `context/_boss-runs/<run-slug>/briefing.md` | Run-scoped summary of source documents, extracted constraints, required persona, model policy, and ordered story/work queue |
| `context/_boss-runs/<run-slug>/progress.md` | Execution queue and current row state for this run |
| `context/_boss-runs/<run-slug>/logs/` | Blocked notes, worker failures, recovery notes |

The run folder is deliberately **flat** under `context/`, not nested under a milestone. Unlike `rails-plan-spam-workflow` — whose output path requires a milestone slug — this workflow is routinely pointed at design documents, ad-hoc story lists, or work spanning several milestones, so a milestone is not always resolvable. Record the milestone(s) and plan paths a run targets inside `briefing.md` instead of encoding them in the folder path.

Create the run folder and files on first run.
Do not delete a run folder on resume unless the user explicitly asks for a clean run. Once every row in a run is `DONE`, the folder may be deleted without losing anything durable — the code is committed, and the source plan or backlog carries the completion markers. Offer that to the user rather than deleting it unasked.

## Run slug naming

Derive the run slug from the work being executed. Determine it **before creating any files**.

**Numbered stories** — first and last story id, dots replaced by underscores:

```text
boss-exec-1_2-to-1_5
boss-exec-2_1                (single story)
```

**Synthetic ids** — use the range:

```text
boss-exec-STEP-001-to-STEP-006
```

**Unnumbered work or design-doc-driven runs** — short slug from the source document name plus the date:

```text
boss-exec-milestone-1-2026-08-03
boss-exec-auth-redesign-2026-08-03
```

Keep the slug short. Avoid vague names such as `boss-exec-run` or `boss-exec-misc`.

**Collisions are expected and must not merge runs.** Date-based slugs collide whenever the same source is run twice in a day, and story-range slugs collide on any retry of the same range. If the derived folder already exists and the user did **not** name it as a resume target, append the next free numeric suffix (`-2`, `-3`, …) and note the collision in the new run's `briefing.md`. Never write into an existing run folder you did not deliberately resume.

**Resuming is explicit.** Resume an existing run only when the user names that run slug, or names the exact folder path. "Continue the boss run" without a named slug is ambiguous — ask which run slug to resume rather than guessing, and list the run folders you can see. Resume semantics for individual rows are in [references/state-model.md](references/state-model.md).

**Retention.** Separate run folders stop runs contaminating each other, but they accumulate. There is no index file tying runs together — a stale index would just become another wrong authority. Discover runs dynamically by listing `context/_boss-runs/` and reading each folder's `progress.md`, which is the only source of truth for that run's state. At the end of a run whose rows are all `DONE`, offer to delete that folder, and mention any other fully-`DONE` folders you noticed while listing. Never delete a folder containing `TODO`, `DOING`, or `BLOCKED` rows without the user saying so explicitly.

## Plan path convention

Implementation plans this workflow consumes live at:

```text
context/implementation-plans/<milestone-slug>/<story-slug>/plan.md
```

`plan.md` is the one primary artifact per story. Do not expect every plan folder to also contain `implementation-log.md`, `completion-review.md`, `questions.md`, `evidence.md`, or `complaining.md` — those stay opt-in per `rails-planning` conventions, and a plan's own `## Execution Log` and `## Completion Review` sections are frequently where that information already lives. If a worker needs to record what actually happened during execution, prefer appending to `plan.md`'s `## Execution Log` section over inventing a new sidecar file, unless the story is large or phased enough that a standalone log was explicitly requested.

## Skills and agent contracts

| Role | Path from this repository root |
| --- | --- |
| Commit wording skill for every worker | `skills/commit-log/SKILL.md` |
| Optional specialist worker contract | `agents/<agent-name>/AGENT.md` |
| Example specialist worker contract | `agents/wpf-persona/AGENT.md` |

Supporting references:

- **State transitions**: [references/state-model.md](references/state-model.md)
- **Worker model selection**: [references/model-selection.md](references/model-selection.md)

## Invocation

The user passes the work request in the message. The message may include source document paths, plan paths, story ids, story ranges, or ordered stories.

Examples:

- `/rails-boss-execute review [context/design.md] [context/milestones/milestone-1.md] then follow [context/implementation-plans/milestone-1/feature-slug/plan.md] with subagents`
- `/rails-boss-execute implement STORY 1.2 and then STORY 1.3 with subagents and mark them off as you go`
- `/rails-boss-execute read these design docs first, then implement the requested plan steps with workers`

Interpret the message literally.
If the user names files, read those files first.
If the user names stories, keep that story order.
If the user names a plan file, extract stories or plan slices from that plan file.
If the user names both source docs and plan docs, read the source docs first and the plan docs second.

## Non-negotiable rules

- Determine the run slug and create the run folder before writing any file.
- Read every user-listed design, milestone, story, and plan document before dispatching the first worker.
- Build or refresh `briefing.md` before dispatching the first worker.
- Build or refresh `progress.md` before dispatching the first worker.
- Never write into an existing run folder unless the user explicitly named that run slug as a resume target.
- Keep running on the session's own model. Do not switch the Boss's model, and do not ask to.
- Select a worker model for every dispatched story per [references/model-selection.md](references/model-selection.md), record it in `progress.md`, and state the model policy to the user before dispatch.
- Never record a worker model that was not actually applied. If selection could not be resolved, record `inherited (unresolved)` and say so.
- Spawn at least one subagent for each story or tightly-bound plan slice. Do not replace that worker step with Boss implementation.
- Default to one story per worker. Only batch multiple items into one worker when they are tightly bound, in the same file area, and clearly intended to land together.
- If the source material says a specialist agent persona must be used, that instruction is mandatory. Pass that agent contract path to every relevant worker. Do not omit it.
- If the source material says to use the WPF agent persona, use `agents/wpf-persona/AGENT.md`. Do not omit it.
- Every worker must load `skills/commit-log/SKILL.md` before finishing.
- Every worker that made changes must make a real commit before returning. The commit message must come from the `commit-log` skill contract. Do not skip the real commit.
- Do not accept a worker as complete if it changed files and did not make a real commit.
- After every successful worker completion, update `progress.md`.
- After every successful worker completion, mark the corresponding story complete in the source plan or backlog file when that file uses checkboxes or explicit story status markers.
- If a story is blocked, mark it blocked in `progress.md`, write a note under `logs/`, and do not pretend the story is done.
- Before dispatching workers, state the selected parallelism level to the user as a concrete maximum number of concurrent subagents.

## Story extraction rules

- If the plan document already has named stories, steps, milestones, or checklist items, preserve those identifiers exactly.
- If the user explicitly requested a subset of stories, queue only that subset.
- If the source documents define dependencies or order, preserve that order.
- If no explicit story ids exist, create stable synthetic ids such as `STEP-001`, `STEP-002`, and `STEP-003`.
- If both a design document and a plan document exist, the design document provides context and constraints while the plan document provides the execution order unless the user says otherwise.

## Briefing file

Write or refresh `context/_boss-runs/<run-slug>/briefing.md` with:

- The run slug, and the milestone(s) or source areas this run targets
- The exact source documents read for this run
- A short note for each source document describing why it matters
- Any mandatory specialist agent persona named by the user or the source documents
- The Boss's own model, the resolved vendor family, and the worker-model policy for this run
- The selected parallelism level and why that level was chosen
- The ordered list of stories or plan slices selected for this run
- Any hard constraints, acceptance notes, or sequencing rules extracted from the documents
- Any run-slug collision that forced a numeric suffix

Keep `briefing.md` concise.
`briefing.md` is a run-scoped summary, not a replacement for the source documents, and it is safe to delete once the run's work has landed.

## Progress file

Write or refresh `context/_boss-runs/<run-slug>/progress.md` as a table like this:

| Status | Story | Source | Persona | Model | Commit | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| TODO | STORY 1.2 | `context/implementation-plans/milestone-1/story-1-2-slug/plan.md` | `agents/wpf-persona/AGENT.md` | haiku (routine) |  | queued |

Use the status values from [references/state-model.md](references/state-model.md).
Only the Boss updates the `Status` column.
Use the `Commit` column for the worker's actual commit SHA after success.
Use the `Model` column for the worker model actually dispatched, with its difficulty band in parentheses — or `inherited (unresolved)` when the harness gave no per-worker control. Never fill it with a model that was merely requested and not applied.

## Execution loop

1. **Determine the run slug**
   Derive it from the work being executed (see naming rules above). If the user named a run slug to resume, use that one; otherwise resolve any collision with a numeric suffix.

2. **Init**
   Ensure `context/`, `context/_boss-runs/<run-slug>/`, `progress.md`, `briefing.md`, and `logs/` exist on the target repository.

3. **Read source documents**  
   Read every source document the user named. Read design and milestone context first. Read plan and implementation files second. Do not dispatch a worker before this step is complete.

4. **Extract constraints and stories**
   Determine:
   - the ordered stories for this run
   - any mandatory agent persona
   - any sequencing constraints
   - any explicit user requirement to update source checklists or story markers
   - the requested or safest parallelism level

5. **Resolve worker models**
   Establish the Boss's own model and vendor family, and whether the harness can set a worker's model at all. Classify each queued story into a difficulty band and map it to a worker model. Follow [references/model-selection.md](references/model-selection.md). If the family or the override capability cannot be resolved, fall back to inheritance and mark every row `inherited (unresolved)`.

6. **Write run state**
   Refresh `briefing.md`. Refresh or initialize `progress.md`, including the `Model` column. Resume from an existing `progress.md` only when resuming a run slug the user named.

7. **Announce parallelism and model policy**
   Before dispatching workers, tell the user the selected parallelism level and the worker-model policy. Use a concrete form such as `Parallelism: 0 (serial, max 1 active subagent)` or `Parallelism: 4 (max 4 active subagents)`, plus the model lines shown in [references/model-selection.md](references/model-selection.md).

8. **Select next story**
   Pick the next `TODO` story whose dependencies are satisfied. If the user requested a specific order, honor that order exactly.

9. **Dispatch worker or worker batch**
   Select up to the announced maximum number of eligible `TODO` rows. Set selected rows to `DOING` in `progress.md`, then spawn one subagent per selected story or tightly-bound plan slice. Pass each worker its required source docs, story id, required persona, selected model, commit requirement, and return format. Do not skip the worker.

10. **Review worker result**
   Confirm the worker:
   - stayed inside the assigned story
   - used the required specialist persona if one was mandatory
   - ran on the model that was selected for it, where the harness reports this
   - ran whatever validation was reasonable for the assigned change
   - made a real commit if files changed
   - returned the commit SHA, changed files, tests run, and blockers

11. **Update state**
   - Success: set the row to `DONE`, record the commit SHA, keep a brief note.
   - Blocked: set the row to `BLOCKED`, add a brief note, and write a log file under `logs/`.
   - Missing commit after changed files: do not mark success. Send the work back or mark blocked.
   - Model override did not take: correct the `Model` column to `inherited (unresolved)` rather than leaving the requested model in place.

12. **Mark source stories complete**
   If the source plan or backlog file uses checkboxes, mark the completed item checked only after the worker is truly `DONE`.
   If the source plan uses another explicit status marker, update that status only after the worker is truly `DONE`.

13. **Repeat**
      Continue until there are no `TODO` rows left for the requested scope or until the remaining stories are blocked.

14. **Report**
      Tell the user the run slug, where `briefing.md` and `progress.md` live, the parallelism level used, the worker models actually used, which stories are done, which stories are blocked, and which commits landed. If every row is `DONE`, offer to delete the run folder.

## Worker dispatch requirements

Every worker prompt must include all of the following:

- The exact story id or step id to implement
- The exact source document paths to read before coding
- A plain statement that the worker must implement only the assigned story or tightly-bound slice
- The exact specialist agent contract path to use, or an explicit statement that no specialist agent contract is required
- The selected worker model (and reasoning effort, where the harness has one), set through whatever parameter the dispatch tool provides — not merely mentioned in the prompt text
- The exact path `skills/commit-log/SKILL.md`
- A plain statement that the worker must load `commit-log`, generate the commit message from that skill, and make a real commit before returning if files changed
- A plain statement that the worker must report commit SHA, changed files, tests run, and blockers
- A plain statement that the worker must not silently skip the commit

Use concrete language.
Repeat the critical requirements in the worker prompt.

Recommended worker wording:

> Read the listed source documents before making changes.  
> Implement only STORY X.Y.
> Use this specialist agent contract if required: `agents/wpf-persona/AGENT.md`.  
> Before you finish, load `skills/commit-log/SKILL.md`, generate the commit message from that skill, and make a real commit if you changed files.  
> Return the commit SHA, files changed, tests run, and blockers.

## Model selection

The Boss runs on **the model the session was started with** — whatever the user launched, in whatever IDE loaded this skill. It does not switch its own model, does not ask to, and does not assume a family from the repository or from a previous run.

What the Boss does choose is the model each worker runs on. Well-written plans mean most stories are cheap to execute; spending the session's top-tier model on every worker is waste, and the user should not have to ask for a downgrade by hand each run.

The rule set — how to resolve the vendor family, how to classify a story's difficulty, which model each band maps to in the Anthropic and OpenAI families, and what to do when none of that can be resolved — lives in [references/model-selection.md](references/model-selection.md). Read it before dispatching the first worker.

Three things are non-negotiable here:

- **The most expensive tier is never auto-selected.** In the Anthropic family that means Fable: reserved for explicit user request. Ask rather than spend.
- **Difficulty is judged as execution difficulty**, not by borrowing CER scores from `rails-planning-phaser`. Those size a plan for phasing and are explicitly uncalibrated.
- **Never claim a selection that did not happen.** If the harness ignores the override or the family is unknown, record `inherited (unresolved)` and disclose it.
- **A phased plan's assigned model is not a dispatch target.** Manifests from `rails-planning-phaser` name capability tiers, not models for this session's family. Translate the tier to a difficulty band and select from the family tables — see the precedence rule in [references/model-selection.md](references/model-selection.md).

## Parallelism

The Boss must state the selected parallelism level to the user before worker dispatch and again in the final report. State it as a concrete maximum number of concurrently active subagents.

Default behavior: use judgment. Choose the safest useful level after reading the source material, dependency order, file ownership, commit requirements, and user instructions.

Use these terms:

- `Parallelism: 0` means serial execution. Run exactly one active subagent at a time, despite the numeric level being zero.
- `Parallelism: N` means run up to `N` active subagents concurrently.

## Zero Parallelism

If the user asks for zero parallelism, no parallelism, serial execution, Ralph-loop style execution, or one worker at a time, use `Parallelism: 0`.

In zero-parallelism mode:

- Spawn one subagent for the next eligible story.
- Let that subagent finish its assigned story completely.
- Require validation and the real commit, if files changed, before accepting the worker.
- Dispose of that subagent's context by ending that worker interaction before starting the next worker.
- Update `progress.md`, source story markers, and logs before spawning the next subagent.
- Repeat for as many stories as needed, even if the run spans dozens of stories and takes hours.

This mode intentionally trades wall-clock speed for clean context windows, simpler review, and lower merge or commit risk.

## Heavy Parallelism

If the user asks for heavy parallelism, high parallelism, maximum safe parallelism, or many workers at once, the Boss must work harder before dispatch:

- Build the full queue before worker dispatch.
- Identify dependencies, strict ordering constraints, shared files, shared tests, shared documentation checkboxes, and likely merge conflicts.
- Partition stories into safe concurrent batches.
- Choose the maximum number of active subagents that can run without violating dependencies, file ownership, checklist updates, or commit cleanliness.
- State that maximum to the user before dispatch.
- Keep Boss-owned state updates (`progress.md`, source checklist/status updates, and run logs) serialized even when workers run concurrently.

Only run multiple workers concurrently when all of the following are true:

- the stories are clearly independent
- the file ownership is disjoint or otherwise safe
- the plan document does not require strict serial order
- each worker can still make its own real commit cleanly

If those conditions are not clearly true, lower the parallelism level. If uncertainty remains material, use `Parallelism: 0`.

## Recovery policy

- `BLOCKED` is durable state.
- Do not silently requeue a blocked story.
- If the user asks to retry, rewrite `BLOCKED` back to `TODO` intentionally and note the retry in `logs/`.
- If the worker reports that no code change was needed, capture that in `Notes` and only mark `DONE` when the story really was satisfied.

## Standalone uses

This workflow can be used for:

- one explicitly named story
- an ordered list of stories
- a full implementation plan
- a design-doc-plus-plan sequence
- milestone-driven delivery where each milestone expands into concrete stories
