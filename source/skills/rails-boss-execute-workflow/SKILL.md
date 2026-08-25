---
name: rails-boss-execute-workflow
description: >-
  Use this orchestration skill when implementing work from design documents,
  milestone documents, backlog stories, or implementation plans. The Boss reads the
  supplied documents, builds a durable story/work queue, dispatches one subagent per
  story or tightly bound plan slice, enforces specialist agents when required, sends
  every completed story to an independent read-only verifier before accepting it,
  updates progress, and repeats until the requested work is done or blocked. Each run
  gets its own named run folder, and the Boss selects an appropriate model per worker.
disable-model-invocation: true
argument-hint: "<docs, plans, or story ids> [--serial|--parallel N] [--resume <run-slug>] [--require <skill>,...] [--verify off] [--model <name>] [--clean]"
metadata:
  version: "2.0"
---

# Rails Boss Execute Workflow

You are the **Boss**.

You read the source documents. You build the queue. You spawn the workers.
An independent verifier judges the result. You update the progress file.
You mark source stories complete. You repeat.

The Boss orchestrates and records. The Boss does not implement, and the Boss does not judge its own workers' output.

## Arguments

The skill was invoked with: $ARGUMENTS

Read that line before doing anything else. It is free text, so parse it leniently, and treat plain-language equivalents as equal to the tokens ("run them one at a time" is `--serial`; "use Fable for the workers" is `--model`).

| Token | Meaning |
| --- | --- |
| `--serial` | One active subagent at a time. Equivalent to `--parallel 1`. |
| `--parallel N` | Up to `N` active subagents. |
| `--resume <run-slug>` | Continue that existing run folder. Without it, an existing folder is never written into. |
| `--require <skill>,...` | The skills every worker must use, replacing the default. See [Required worker skills](#required-worker-skills). |
| `--verify off` | Skip the independent verifier. Must be disclosed in `briefing.md` and the final report. |
| `--model <name>` | Force every worker onto this model, bypassing band selection. Record the override in `briefing.md`. |
| `--clean` | Delete and recreate the named run folder instead of resuming it. |
| anything else | The work request — document paths, plan paths, story ids, or story ranges. This is the main payload. |

If `$ARGUMENTS` carries only a work request, every switch is unset. That is the normal case, not an error. The defaults below already cover it, so never ask the user to re-invoke with arguments.

Interpret the work request literally:

- If the user names files, read those files first.
- If the user names stories, keep that story order.
- If the user names a plan file, extract stories or plan slices from that plan file.
- If the user names both source docs and plan docs, read the source docs first and the plan docs second.

Examples:

```text
/rails-boss-execute context/design.md context/milestones/milestone-1.md then follow context/implementation-plans/milestone-1/feature-slug/plan.md
/rails-boss-execute implement STORY 1.2 and then STORY 1.3 and mark them off as you go --serial
/rails-boss-execute --resume boss-exec-1_2-to-1_5 --parallel 3
```

## Purpose

Use this workflow when:

- the user wants implementation work done from design, milestone, story, or implementation-plan documents;
- the work should go through subagents instead of one large direct implementation pass;
- the work splits naturally into stories, checklist items, milestones, or ordered plan slices.

It suits a single story, a short ordered set, or a larger multi-document delivery pass.

## Artifact root (target repository)

All paths in this section are relative to the **target** repository root — the project being implemented, not this tooling repository.

Path conventions follow the Agentic Rails context structure. If the target repository uses different context or documentation folders, adjust before dispatching workers and record the chosen path in `briefing.md`.

Every invocation gets its own **run slug** and run folder. Run artifacts are run-scoped and deletable; nothing durable lives in them.

| Path | Role |
| --- | --- |
| `context/_boss-runs/<run-slug>/briefing.md` | Run-scoped summary of source documents, constraints, required persona and skills, validation command, model policy, and the ordered queue |
| `context/_boss-runs/<run-slug>/progress.md` | Execution queue and current row state for this run |
| `context/_boss-runs/<run-slug>/logs/` | Blocked notes, verifier reports, worker failures, recovery notes |

The run folder is deliberately **flat** under `context/`, not nested under a milestone. Unlike `rails-plan-spam-workflow` — whose output path requires a milestone slug — this workflow is routinely pointed at design documents, ad-hoc story lists, or work spanning several milestones, so a milestone is not always resolvable. Record the milestone(s) and plan paths a run targets inside `briefing.md` instead of encoding them in the folder path.

Once every row in a run is `DONE`, the folder may be deleted without losing anything: the code is committed, and the source plan or backlog carries the completion markers. Offer that to the user rather than deleting it unasked.

### The run must survive the Boss being compacted

`briefing.md` and `progress.md` are the run's durable state. Everything needed to resume must be readable from them alone — a Boss whose context was compacted mid-run reads those two files and continues without loss.

This means: write state to disk **before** starting the next thing, never after. A row's status, verdict, and commit SHA land in `progress.md` before the next worker is dispatched. Never hold run state only in the conversation.

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

**Unnumbered or design-doc-driven runs** — short slug from the source document name plus the date:

```text
boss-exec-milestone-1-2026-08-03
boss-exec-auth-redesign-2026-08-03
```

Keep the slug short. Avoid vague names such as `boss-exec-run` or `boss-exec-misc`.

**Collisions are expected and must not merge runs.** Date-based slugs collide whenever the same source runs twice in a day, and story-range slugs collide on any retry. If the derived folder already exists and `--resume` did not name it, append the next free numeric suffix (`-2`, `-3`, …) and note the collision in the new run's `briefing.md`.

**Resuming is explicit.** Resume only via `--resume <run-slug>`, or when the user names the exact folder path. "Continue the boss run" without a named slug is ambiguous — list the run folders you can see and ask which to resume. Per-row resume semantics are in [references/state-model.md](references/state-model.md).

**Retention.** Separate run folders stop runs contaminating each other, but they accumulate. There is no index file tying runs together — a stale index would just become another wrong authority. Discover runs dynamically by listing `context/_boss-runs/` and reading each folder's `progress.md`, which is the only source of truth for that run's state. At the end of a fully-`DONE` run, offer to delete that folder and mention any other fully-`DONE` folders noticed while listing.

## Plan path convention

Implementation plans this workflow consumes live at:

```text
context/implementation-plans/<milestone-slug>/<story-slug>/plan.md
```

`plan.md` is the one primary artifact per story. Do not expect every plan folder to also contain `implementation-log.md`, `completion-review.md`, `questions.md`, `evidence.md`, or `complaining.md` — those stay opt-in per `rails-planning` conventions, and a plan's own `## Execution Log` and `## Completion Review` sections are frequently where that information already lives. Prefer appending to `plan.md`'s `## Execution Log` over inventing a new sidecar file, unless the story is large or phased enough that a standalone log was explicitly requested.

## Required worker skills

Every worker must produce a commit whose message came from the `commit-log` skill. That is the default, and the only default.

Resolve the run's required-skill list **once**, at briefing time. First match wins:

1. `--require` tokens in `$ARGUMENTS`.
2. Skills named as mandatory by the source documents, or by the target repository's `AGENTS.md` / `CLAUDE.md`.
3. `commit-log` alone.

Record the resolved list in `briefing.md`. Pass it to every worker and to every verifier.

**Invoke skills by name, never by path.** Tell a worker to invoke `commit-log` as a skill. Do not hand it a filesystem path: this document's paths are relative to the *target* repository, while skills live in the agent's own configuration directory. Those are different roots, and a path that resolves for the Boss will not resolve for a worker whose working directory is the target repo.

**A skill is verified by its signature, not by its invocation.** No agent can observe another agent's tool calls, so the verifier never checks *that* a skill ran — it checks that the produced artifact bears that skill's observable signature. For `commit-log` the signature is readable from `git show`:

- a heading line of the form `[PREFIX] ...`, 72 characters or fewer;
- body lines beginning `~ Problem:`, then `~ Fixed:` / `~ Changed:` / `~ Added:` / `~ Removed:` / `~ Updated:`;
- a closing `~ Resolution:` line.

When resolving a non-default list, record each skill's observable signature in `briefing.md` alongside it. If a required skill leaves no observable signature in the artifact, record it as `unverifiable` — do not guess, and do not fail the story on that basis alone.

## Skills and agent contracts

| Role | Contract |
| --- | --- |
| Commit wording for every worker | the `commit-log` skill, invoked by name |
| Independent verifier | `agents/quality-gate-persona/AGENT.md` |
| Optional specialist worker persona | `agents/<agent-name>/AGENT.md` |
| Example specialist worker persona | `agents/wpf-persona/AGENT.md` |

Supporting references:

- **State transitions**: [references/state-model.md](references/state-model.md)
- **Worker model selection**: [references/model-selection.md](references/model-selection.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

**Setup**

- Determine the run slug and create the run folder before writing any file.
- Read every user-listed design, milestone, story, and plan document before dispatching the first worker.
- Resolve the required-skill list, the target repository's validation command, and every worker's model before dispatching the first worker.
- Write `briefing.md` and `progress.md` before dispatching the first worker.
- Never write into an existing run folder unless `--resume` named that run slug.

**Models**

- Keep running on the session's own model. Do not switch the Boss's model, and do not ask to.
- Select a worker model per [references/model-selection.md](references/model-selection.md), record it in `progress.md`, and state the policy to the user before dispatch.
- Never record a worker model that was not actually applied. If selection could not be resolved, record `inherited (unresolved)` and say so.

**Dispatch**

- Spawn at least one subagent per story or tightly-bound plan slice. Never replace that worker step with Boss implementation.
- Default to one story per worker. Batch only when items are tightly bound, in the same file area, and clearly intended to land together.
- If the source material mandates a specialist agent persona, that instruction is mandatory — pass the contract path to every relevant worker.
- State the parallelism level to the user before dispatch, as a concrete maximum number of concurrently active subagents.

**Acceptance**

- Every worker that changed files must make a real commit before returning, worded by `commit-log`.
- Every completed story goes to an independent verifier before it can be marked `DONE`. The Boss does not judge worker output itself. `--verify off` is the only exception, and must be disclosed.
- Only a `PASS` or `PASS WITH NOTES` verdict may become `DONE`. A `BLOCK` becomes `BLOCKED`. An unverifiable result never becomes `DONE`.
- Mark a story complete in the source plan or backlog only after its row is `DONE`.
- When a story is blocked, mark it blocked, write a note under `logs/`, and do not pretend it is done.
- A story that has failed verification three times stops consuming the queue, not the run: mark it `BLOCKED` with the reason and the three verdicts, and dispatch the next runnable story. Do not retry a fourth. The run ends when no story is runnable, not when one story is.

## Story extraction rules

- If the plan document already has named stories, steps, milestones, or checklist items, preserve those identifiers exactly.
- If the user requested a subset of stories, queue only that subset.
- If the source documents define dependencies or order, preserve that order.
- If no explicit story ids exist, create stable synthetic ids such as `STEP-001`, `STEP-002`, `STEP-003`.
- If both a design document and a plan document exist, the design document provides context and constraints while the plan document provides execution order, unless the user says otherwise.

## Briefing file

Write or refresh `context/_boss-runs/<run-slug>/briefing.md` with:

- the run slug, and the milestone(s) or source areas this run targets;
- the exact source documents read, each with a short note on why it matters;
- any mandatory specialist agent persona;
- the resolved required-skill list, and each skill's observable signature;
- the target repository's validation command (build, test, lint), or an explicit note that none was found;
- the Boss's own model, the resolved vendor family, and the worker-model policy;
- the parallelism level and why it was chosen;
- the ordered list of stories or plan slices;
- any hard constraints, acceptance notes, or sequencing rules from the documents;
- any run-slug collision that forced a numeric suffix, any `--model` override, and whether verification is off.

Keep it concise. `briefing.md` is a run-scoped summary, not a replacement for the source documents, and it is safe to delete once the run's work has landed.

## Progress file

Write or refresh `context/_boss-runs/<run-slug>/progress.md` as a table:

| Status | Story | Source | Persona | Model | Commit | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TODO | STORY 1.2 | `context/implementation-plans/milestone-1/story-1-2-slug/plan.md` | `agents/wpf-persona/AGENT.md` | haiku (routine) |  |  | queued |

Column rules:

- **Status** — from [references/state-model.md](references/state-model.md). Only the Boss writes it.
- **Model** — the model a worker *actually ran on*, with its difficulty band in parentheses, or `inherited (unresolved)`.
- **Commit** — the worker's actual commit SHA after success.
- **Verdict** — the verifier's verdict, or `skipped` when `--verify off` is in effect. Blank until verification runs.

## Execution loop

1. **Determine the run slug.** Derive it from the work being executed. Honor `--resume`; otherwise resolve any collision with a numeric suffix.

2. **Init.** Ensure `context/`, `context/_boss-runs/<run-slug>/`, `progress.md`, `briefing.md`, and `logs/` exist on the target repository.

3. **Read source documents.** Design and milestone context first, plan and implementation files second.

4. **Extract constraints and stories.** Determine the ordered stories, any mandatory persona, sequencing constraints, any requirement to update source checklists, and the parallelism level.

5. **Resolve the run's contracts.** Establish the required-skill list and each signature, and the repository's validation command (read `AGENTS.md`, `CLAUDE.md`, `package.json`, or the equivalent — do not invent one).

6. **Resolve worker models.** Establish the Boss's model and vendor family, and whether the harness can set a worker's model at all. Classify each story into a difficulty band and map it per [references/model-selection.md](references/model-selection.md). If family or override capability cannot be resolved, fall back to inheritance and mark every row `inherited (unresolved)`.

7. **Write run state.** Refresh `briefing.md` and `progress.md`.

8. **Announce policy.** Before dispatching, tell the user the parallelism level, the worker-model policy, the required-skill list, and whether verification is on. Use concrete forms such as `Parallelism: 1 (serial)` or `Parallelism: 4`, plus the model lines shown in [references/model-selection.md](references/model-selection.md).

9. **Select next story.** The next `TODO` whose dependencies are satisfied, honoring any user-requested order exactly.

10. **Dispatch worker or batch.** Select up to the announced maximum of eligible `TODO` rows, set them to `DOING`, and spawn one subagent per story or tightly-bound slice. See [Worker dispatch requirements](#worker-dispatch-requirements).

11. **Verify.** On worker return, set the row to `VERIFYING` and dispatch the verifier. See [Verification](#verification).

12. **Update state.** Write the outcome to `progress.md` before doing anything else:
    - `PASS` → `DONE`, record the commit SHA and verdict.
    - `PASS WITH NOTES` → `DONE`, record the verdict and carry the notes into `Notes`.
    - `BLOCK` → `BLOCKED`, write the verifier report under `logs/`.
    - Unverifiable, or changed files with no acceptable commit → not `DONE`. Record why and escalate or block.
    - Model override did not take → correct `Model` to `inherited (unresolved)`.

13. **Mark source stories complete.** Update the source plan's checkbox or status marker only after the row is `DONE`.

14. **Repeat** until no `TODO` rows remain in scope, or the remainder are blocked.

15. **Report.** Give the user the run slug, where `briefing.md` and `progress.md` live, the parallelism level used, the worker models actually used, the verdicts, which stories are done, which are blocked, and which commits landed. If every row is `DONE`, offer to delete the run folder.

## Worker dispatch requirements

Every worker prompt must carry all of the following. This is a payload spec — the rules behind it are in [Non-negotiable rules](#non-negotiable-rules).

- the exact story id or step id;
- the exact source document paths to read before coding;
- the story's acceptance criteria from the plan, or the story's own description when the plan states none;
- an instruction to implement only that story or tightly-bound slice;
- the specialist agent contract path, or an explicit statement that none is required;
- the required-skill list, to be invoked **by name**;
- the repository's validation command, verbatim, with an instruction to run it before finishing;
- the selected worker model and reasoning effort, set through the dispatch tool's own parameter — not merely mentioned in the prompt text;
- an instruction to make a real commit before returning if files changed, worded by `commit-log`, and never silently skipped;
- an instruction to report commit SHA, changed files, validation output, and blockers.

Recommended wording:

> Read the listed source documents before making changes.
> Implement only STORY X.Y. Its acceptance criteria are: <criteria>.
> Use this specialist agent contract: `agents/wpf-persona/AGENT.md`.
> Run `<validation command>` before you finish.
> Invoke the `commit-log` skill by name, generate the commit message from it, and make a real commit if you changed files.
> Return the commit SHA, files changed, validation output, and blockers.

## Verification

The agent that did the work does not decide whether the work is acceptable. After a worker returns, the Boss dispatches an **independent verifier** for that story and takes its verdict.

The verifier is `agents/quality-gate-persona/AGENT.md`. It is read-only by contract: it reports findings and never repairs, commits, or expands scope. Do not restate its review workflow or report format here — dispatch it and supply its expected inputs.

**Dispatch payload** — populate the persona's `Inputs Expected`:

| Its input | What the Boss supplies |
| --- | --- |
| The changeset under review | the worker's commit SHA and changed file list |
| Statement of intended scope | the story id and its acceptance criteria |
| Project rules | the target repository's rules directory or `AGENTS.md` |
| Validation commands | the command resolved at briefing time |
| Project-specific constraints | the mandatory persona, sequencing rules, and anything else from `briefing.md` |

Add one Boss-specific check to the dispatch: **confirm each required skill's observable signature is present in the artifact.** For `commit-log`, read the commit message with `git show` and check it against the signature recorded in `briefing.md`. A missing `commit-log` signature is a blocking finding. A required skill with no observable signature is reported as a gap, not a failure.

**Verdict handling** — the persona returns `PASS`, `PASS WITH NOTES`, or `BLOCK`, plus a `GAPS / UNCERTAINTY` section:

- `PASS` → the row may become `DONE`.
- `PASS WITH NOTES` → the row may become `DONE`; carry the notes into `Notes`.
- `BLOCK` → the row becomes `BLOCKED`; write the full report under `logs/`.
- A verdict with no cited evidence, or one whose gaps mean the story's acceptance criteria were never actually checked, is **not** a pass. Treat it as unverifiable: do not mark `DONE`, record what could not be checked, and escalate to the user.

**Verifier model.** Run the verifier at the same difficulty band as its worker, and never below Standard. A skeptical verifier is the cheapest quality lever in this workflow; do not economize on it.

**Retries.** A `BLOCK` that the user asks to retry re-enters as `TODO` one difficulty band higher, per [references/model-selection.md](references/model-selection.md). After a third failed verification of the same story, stop retrying that story — three failures mean the plan is wrong, not the worker. Leave it `BLOCKED` with its verdicts recorded and continue with the stories that can still run.

**Skipping.** `--verify off` is the only way to skip verification. When it is set, write `skipped` in the `Verdict` column for every row, disclose it in `briefing.md`, and say so plainly in the final report. Never report a run as verified when it was not.

## Model selection

The Boss runs on **the model the session was started with** — whatever the user launched, in whatever IDE loaded this skill. It does not switch its own model and does not assume a family from the repository or a previous run.

What it does choose is each worker's model. Well-written plans mean most stories are cheap to execute; spending the session's top tier on every worker is waste.

The rule set — resolving the vendor family, classifying difficulty, the per-family tables, and what to do when none of it resolves — is in [references/model-selection.md](references/model-selection.md). Read it before dispatching the first worker. Three things it settles are worth naming here:

- **The most expensive tier is never auto-selected.** In the Anthropic family that means Fable: reserved for explicit user request. Ask rather than spend.
- **Difficulty is execution difficulty**, judged from the plan in front of you — not CER scores borrowed from `rails-planning-phaser`, which size plans for phasing and are explicitly uncalibrated.
- **A phased plan's assigned model is not a dispatch target.** Manifests name capability tiers, not models for this session's family. Translate the tier to a difficulty band and select from the family tables.

`--model <name>` overrides all of this for every worker. Record the override in `briefing.md`, and still apply the recording rules: if it does not take, the column reads `inherited (unresolved)`.

## Parallelism

State the parallelism level to the user before dispatch and again in the final report, as a concrete maximum number of concurrently active subagents.

- `Parallelism: 1` — serial. One active subagent at a time.
- `Parallelism: N` — up to `N` active subagents.

Default: use judgment. Choose the safest useful level after reading the source material, dependency order, file ownership, commit requirements, and user instructions.

Boss-owned state — `progress.md`, source checklist updates, and run logs — stays serialized even when workers run concurrently.

### Serial execution

`--serial`, or any request for one worker at a time, no parallelism, or Ralph-loop style execution, means `Parallelism: 1`:

- spawn one subagent for the next eligible story;
- let it finish, verify it, and require the real commit if files changed;
- dispose of that subagent's context by ending the worker interaction before starting the next;
- update `progress.md`, source story markers, and logs before spawning the next subagent;
- repeat for as many stories as needed, even across dozens of stories and hours.

This trades wall-clock speed for clean context windows, simpler review, and lower merge risk.

### High parallelism

A request for heavy or maximum-safe parallelism means the Boss works harder before dispatch:

- build the full queue first;
- identify dependencies, ordering constraints, shared files, shared tests, shared documentation checkboxes, and likely merge conflicts;
- partition stories into safe concurrent batches;
- choose and state the maximum number of active subagents that respects all of the above.

Only run workers concurrently when the stories are clearly independent, file ownership is disjoint or otherwise safe, the plan does not require strict serial order, and each worker can still commit cleanly. If those are not clearly true, lower the level. If material uncertainty remains, use `Parallelism: 1`.

## Recovery policy

- `BLOCKED` is durable state. Do not silently requeue a blocked story.
- On a user-requested retry, rewrite `BLOCKED` back to `TODO` intentionally, bump the difficulty band, and note the retry in `logs/`.
- After three failed verifications of the same story, leave it `BLOCKED` and move to the next runnable story rather than requeuing a fourth time.
- If a worker reports that no code change was needed, capture that in `Notes` and mark `DONE` only when the story really was satisfied — the verifier still runs.

## Standalone uses

One explicitly named story; an ordered list of stories; a full implementation plan; a design-doc-plus-plan sequence; or milestone-driven delivery where each milestone expands into concrete stories.
