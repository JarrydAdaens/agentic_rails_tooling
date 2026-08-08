---
name: rails-memory-learnings
description: >-
  Use this skill at the end of a work session - after implementation, planning,
  Agentic Rails implementation-plan execution, bulk planning, orchestration, or
  a completed story - when the user asks to capture learnings, memorize the
  session, write a session learning, or deposit a memory artifact. It reflects
  on the session and writes exactly one durable learning file into the Rails
  memory repository's learnings/new/ folder, recording the outcome, what went
  well, what struggled, and full provenance: the models, harness, thinking
  effort, reasoning vs non-reasoning, fast mode, and token cost behind the work.
disable-model-invocation: true
argument-hint: "[--project <name>] [--dry-run]"
metadata:
  version: "1.3"
---

# Rails Memory Learnings

Capture the learnings from a work session as a single durable artifact and deposit it into the **Agentic Rails memory** repository (the framework's records office). This is the **write** phase of the memory feedback loop: `capture -> curate -> consume`.

This skill has exactly **one job**: reflect on the session and produce **one** learning file in `learnings/new/`. It records what happened and, critically, **what produced it** - the models, harness, thinking effort, reasoning mode, fast mode, and token cost - so a later curation run can distill these raw data points into model and agent Resumes.

## Arguments

The skill was invoked with: $ARGUMENTS

Read that line before doing anything else. It is free text, so parse it leniently.

| Token | Meaning |
| --- | --- |
| `--project <name>` | The project name used in the filename. Absent means derive it from the repository. |
| `--dry-run` | Print the learning artifact without writing it. Absent means write. |
| anything else | Extra emphasis on what the session should record. |

Empty `$ARGUMENTS` means capture this session's learning for the current project and write it — the normal case.

## Scope: One File In, One File Out

| In scope | Out of scope |
| --- | --- |
| Reflect on the session that just happened | Generating wiki pages, rules, skills, or verifiers |
| Produce one learning artifact | Curation, ranking, or promotion |
| Capture full provenance + execution profile | Rebuilding or editing any model/agent Resume |
| Write the file into `learnings/new/` | Touching `archived/` or `golden/` |
| Note un-actioned candidate signals for later | Distributing anything to other tooling |

Capture is meant to be **cheap and frequent**. It flags signals; it does not act on them. The **manage** phase (curation) and **read** phase (orchestration) are owned by separate right-rail tooling.

## Memory Repository Location

The memory repository is `agentic-rails-memory`. Write the artifact to:

```text
agentic-rails-memory/memories/learnings/new/<project>_<YYYY-MM-DD>.md
```

If the repository is not at a known path, ask the user for its location before writing. Never write learnings into the project being worked on - they belong in the memory repository only. Write to `new/` and nowhere else.

## Artifact Naming

The on-disk name stays clean and human-scannable. Heavy metadata lives **inside** the file, not in the filename.

```text
<project>_<YYYY-MM-DD>.md
```

- `<project>` - the project slug the session belonged to (kebab-case).
- `<YYYY-MM-DD>` - the session date.

If a same-day file for the same project already exists, append a numeric counter (`<project>_<YYYY-MM-DD>_2.md`, then `_3`, ...). The `session_id` and all other metadata are carried in the artifact body's frontmatter, never crammed into the name.

## Artifact Format

The file is markdown: a frontmatter block for machine-readable provenance, then a structured human-readable body. Anyone reading it later should immediately be able to tell **where it came from, when, what produced it, and why it exists** - with no external lookup.

### Frontmatter (Provenance + Execution Profile)

```yaml
---
type: session-learning
project: <project-slug>
date: <YYYY-MM-DD>
session_id: <unique session id>
captured_by: rails-memory-learnings
captured_at: <ISO 8601 timestamp>
status: new                      # new -> archived -> golden, owned by curation

session_scope: <one-task | implementation-plan | multi-story | planning-run | orchestration-run | workflow-run>
outcome: <succeeded | partial | failed | blocked>

harness: <agent harness / IDE, e.g. "claude-code", "cursor", "codex-cli", "windsurf">
harness_version: <version if known, else "unknown">

models_used:
  - name: <model id, e.g. "claude-opus-4-8">
    provider: <anthropic | openai | google | local/ollama | ...>
    role: <planning | execution | review | orchestration | ...>
    reasoning: <reasoning | non-reasoning>
    thinking_effort: <none | low | medium | high | max | unknown>
    fast_mode: <true | false | n/a>
    notes: <optional one-liner on how this model behaved>

agents_used:
  - <persona or subagent, e.g. "wpf-persona", "general-purpose">

token_cost: <approx total tokens for the session, or "unknown">
---
```

Field notes:

- **`session_id`** - unique per session; lives here, not in the filename.
- **`harness` / `harness_version`** - the tool that drove the work (the IDE or agent runtime). Required signal: capture it even if the version is unknown.
- **`models_used`** - one entry per distinct model+role. This is the raw signal curation distills into Resumes, so be precise:
  - **`reasoning`** - was the model run as a reasoning/thinking model, or non-reasoning?
  - **`thinking_effort`** - the reasoning/thinking effort level used (e.g. none, low, medium, high, max). Use `unknown` only if genuinely unrecoverable.
  - **`fast_mode`** - whether a "fast"/low-latency mode was enabled (`n/a` if the harness has no such mode).
  - If the same model ran in two roles with different settings (e.g. high-effort planning then fast-mode execution), give it two entries.
- **`agents_used`** - personas or subagents that executed work, feeding agent Resumes.
- **`token_cost`** - approximate total tokens; feeds model Resume cost-awareness. Estimate if exact figures are unavailable and say so.
- **`status`** - always `new` at write time; curation owns all transitions.

If a provenance value cannot be determined, record `unknown` rather than guessing or omitting the field. Do not fabricate model names, effort levels, or token counts.

### Body (The Learning)

Use this section set so the downstream consumer skill can parse predictably. Keep every section even if brief; if a section has nothing meaningful, say so plainly.

```markdown
# Session Learning: <project> - <YYYY-MM-DD>

## Summary
<2-4 sentences: what the session was, what was attempted, the outcome and why.>

## What Went Well
<Concrete wins: clean implementation choices, good plan adherence, effective
tooling/persona use, unexpectedly efficient outcomes. Do not force praise.>

## What Struggled
<Factual friction, proportionate: loops, failed attempts, plan drift, tool
problems, weak context, surprises, edge cases, and failure modes worth
remembering. Do not invent problems for symmetry.>

## Per-Model / Per-Agent Notes
<The signal that feeds Resumes. For each model and agent in the frontmatter,
note what it was good at and where it fell down - tied to its role, reasoning
mode, thinking effort, and fast-mode setting. Call out token-efficiency or
latency observations. This is the most important section for the memory loop.>

## Candidate Signals
<Lightweight, UN-ACTIONED flags for the downstream skill. Each is one line with
a confidence band (low / medium / high). Examples:
- (high) Smells like a reusable rule: always run X before Y.
- (medium) Possible wiki page on the Z subsystem.
- (low) An eval was missing around the W edge case.
Only NOTE these. Do not build rules, wiki pages, skills, or verifiers here.>

## Evidence Reviewed
<The sources actually consulted: plan.md, implementation-log.md, commits,
changed files, validation commands, completion reviews, persona references.>
```

## Operating Model

1. Confirm the memory repository location (ask if unknown).
2. Determine the session scope (one task, an implementation-plan folder, multiple stories, a planning run, an orchestration run, or a workflow run).
3. Reflect on the session and gather metadata: project slug, date, session id, harness + version, every model used with its role/reasoning/thinking-effort/fast-mode, agents/personas used, approximate token cost, and the outcome.
4. Review the most relevant available sources to ground the reflection (see Claim Standard).
5. Compose the artifact: frontmatter, then the structured body.
6. Resolve the filename, applying the numeric collision suffix only if a same-day file already exists.
7. Write the single file to `memories/learnings/new/`. Do not touch anything else.
8. Tell the user the path written. Leave committing to the user / harness convention - the repository is git-controlled.

## Inputs To Review

Use the most relevant available sources; missing optional files are not failures.

- Execution context: `plan.md`, `implementation-log.md`, `completion-review.md`, handover artifacts, workflow progress files, orchestration briefs, planning outputs.
- Optional provenance: `complaining.md`, `thinking.md`, `evidence.md`.
- Git history: relevant commits, messages, diffs, changed files.
- Code state: final changed files, tests, build results, documentation changes.
- Conversation context: when this is a warm capture, the session itself is a primary source for the execution profile (models, effort, fast mode, harness).

## Claim Standard

Ground the learning in reviewed sources wherever possible, and label honestly:

- **Verified** - directly supported by a source, command output, commit, or artifact.
- **Inferred** - likely from available evidence, but not directly proven.
- **Assumed** - accepted because the session context required it.
- **Unknown** - not enough evidence.

For a cold capture (no conversation context), be stricter about labeling inference and unknowns - especially for the execution profile, where reasoning mode and fast mode may not be recoverable.

## Boundaries

- Write **exactly one** file, only into `learnings/new/`.
- Do not rebuild, append to, or edit any model or agent Resume.
- Do not touch `archived/` or `golden/`, and do not run curation.
- Do not generate wiki pages, rules, skills, or verifiers - only **note** them as candidate signals.
- Do not write learnings into the project repository; they belong in the memory repository.
- Never include secrets, credentials, API keys, customer data, or proprietary source. Sanitize before writing.
- Do not expose private chain-of-thought; capture sanitized observations only.
- Do not fabricate provenance, praise, or problems. Record `unknown` when a value is genuinely unrecoverable.

## Acceptance

Observable facts about the written artifact:

- Exactly one file exists under `memories/learnings/new/`, named `<project>_<YYYY-MM-DD>.md` with a numeric suffix only on same-day collision.
- Its frontmatter carries every provenance field plus the execution profile (harness, per-model reasoning or thinking effort, fast mode, token cost).
- Its body contains every heading in the standard section set, including Per-Model / Per-Agent Notes.
- No file under `archived/` or `golden/`, and no Resume, has a modification time from this run.
- The artifact contains no credentials, tokens, or raw chain-of-thought.
