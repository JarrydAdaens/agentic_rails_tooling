---
name: rails-pair-programming
description: >-
  Use this skill when the user explicitly wants a structured Agentic Rails
  pair-programming session, such as "use rails-pair-programming", "start
  rails-pair-programming", "pair program this under Rails", or similar phrasing.
  The skill establishes intent, gathers current 5T Goal and implementation-plan
  context, runs a collaborative tutoring and pair-programming loop, and creates
  or appends a durable pair-programming.md session artifact at wrap-up.
---

# Rails Pair Programming

Run a live Agentic Rails pair-programming session that stays grounded in the
project's durable context and produces a session artifact when the user wraps up.

This skill belongs to the reusable right rail. Its context and outputs belong to
the project-local left rail.

## Operating Contract

Apply this skill only after explicit activation. Once active, treat later user
turns as part of the same pair-programming session when the conversation context
clearly indicates the session is still ongoing.

Use four phases:

```text
Intent -> Context Gathering -> Collaborative Session -> Wrap-up
```

Keep the active Goal authoritative. Explore freely when helpful, but ground
decisions, conclusions, and next steps back into the current Goal and Plan when
possible.

Do not write production code unless the user explicitly moves the session into
implementation.

## Phase 1: Intent

Start here unless the user already provided clear intent.

Identify:

- what the user wants to work on
- whether the session is exploration, intense collaboration, or mixed
- which Goal or implementation plan the work relates to
- what outcome would make the session useful

Modes:

- `Exploration`: understand a codebase area, file, architecture, bug surface,
  design, goal, or implementation plan.
- `Intense Collaboration`: solve, debug, design, implement, decide, refactor, or
  build through close back-and-forth.
- `Mixed`: begin with exploration and switch into concrete collaboration when a
  specific move becomes clear.

If intent is obvious, confirm it briefly and proceed. Avoid setup questions that
do not change the next useful action.

Example:

```text
rails-pair-programming is active.

Intent looks like: understand and debug the current implementation around <topic>.
Mode: Exploration, with a possible switch into intense collaboration if we find a fix.
I'll ground this against the current Goal and Plan folder first.
```

## Phase 2: Context Gathering

Gather only the context needed for the session. Prefer maintained Agentic Rails
context over chat memory.

Load, when relevant and available:

- current Goal document
- active implementation-plan folder and `plan.md`
- sibling Tier 4 artifacts such as `implementation-log.md`, `thinking.md`,
  `evidence.md`, `complaining.md`, handovers, notes, or addenda
- Tier 1 design and Tier 2 milestone context
- relevant source files, tests, logs, or technical artifacts
- Tier 0 intake only when rationale recovery or source synthesis matters

Priority order:

1. Active user request
2. Current Goal document
3. Active implementation plan
4. Design and milestone context
5. Tier 0 notes, only when needed
6. Source files, tests, logs, and technical artifacts

Path hints:

- Prefer `Documentation/implementation_plans/<current-goal-or-plan-folder>/`.
- Search existing implementation-plan folders before creating or assuming a new
  one.
- If no active Goal or Plan can be located, ask one targeted question or proceed
  with clearly marked uncertainty.

Keep context use visible enough that the user can tell the session is grounded,
but do not dump large summaries unless asked.

## Phase 3: Collaborative Session

Act as a pair programmer, tutor, debugger, codebase guide, technical sounding
board, and design reviewer as the session requires.

During the loop:

- ask useful questions when the next move depends on the answer
- inspect relevant files and project context
- explain concepts through the actual code or Goal context
- test ideas against project constraints
- challenge weak assumptions with concrete reasons
- narrow broad problems into actionable next moves
- call out trade-offs, risks, and validation steps
- keep notes for wrap-up

In exploration mode:

- map the area
- identify important files, concepts, dependencies, and open questions
- explain relationships in practical language
- avoid premature implementation
- preserve findings for the session artifact

In intense collaboration mode:

- stay close to the immediate problem
- propose options with trade-offs
- help decide and execute the next step
- validate claims against code, tests, logs, or project documents
- capture decisions and reasoning for wrap-up

When tutoring:

- use direct, practical explanations
- connect concepts to the current code or Agentic Rails artifact
- avoid generic textbook dumps
- ask short comprehension checks only when useful
- adapt depth to the user's expertise

## Phase 4: Wrap-up

Wrap up when the user says something like:

```text
I'm done
wrap it up
conclude
finish
save this
end session
that's enough
summarise this
```

At wrap-up:

1. Summarize the session.
2. Create or update `pair-programming.md`.
3. Include discoveries, key discussions, decisions, open questions, outcomes,
   and yielded work.
4. Ground the artifact in the active Goal and Plan context.
5. Preserve existing session records.
6. End cleanly.

Preferred path:

```text
Documentation/implementation_plans/<current-goal-or-plan-folder>/pair-programming.md
```

Fallback path when the active plan folder is unknown:

```text
Documentation/pair-programming.md
```

If `pair-programming.md` already exists, append a new dated session entry rather
than overwriting prior sessions.

## Artifact Template

Use this structure for a new file, or as a new appended session entry in an
existing file:

```markdown
# Pair Programming Session

## Session Date

<YYYY-MM-DD>

## Goal Reference

<Link or describe the current Goal and Plan folder.>

## Intent And Mode

- Intent: <what the session was trying to achieve>
- Mode: <Exploration | Intense Collaboration | Mixed>

## Key Topics Explored

- <Topic 1>
- <Topic 2>
- <Topic 3>

## Discoveries And Decisions

- Discovery: <what was found>
- Decision: <what was decided and why>

## Code Changes Or Next Steps Identified

- <Change, candidate change, or next step>

## Open Items

- <Question, risk, unknown, or follow-up>

## Outcome

<What the session yielded.>

## Session Summary

<Concise narrative summary of what was achieved.>
```

## Boundaries

Do not:

- operate as generic chat with no Goal or Plan awareness
- invent Goal context when it cannot be found
- create fake decisions, discoveries, or validation evidence
- expose private chain-of-thought
- replace `implementation-log.md`, `evidence.md`, `thinking.md`,
  `complaining.md`, or handover artifacts
- write code unless the user explicitly moves into implementation
- keep asking setup questions when intent is already obvious
- finish a save or wrap-up request without writing the artifact

## Related Artifacts

- `implementation-log.md`: records implementation history; reference it, but do
  not replace it.
- `complaining.md`: records real execution friction; surface friction only when
  it is genuine.
- `thinking.md`: stores sanitized working notes; keep the pair-programming
  artifact outcome-focused.
- `evidence.md`: indexes validation and provenance; mention evidence needs, but
  do not replace evidence tracking.
- handover artifacts: can use pair-programming summaries as input, but are a
  separate ownership-transfer output.

## Validation

Before considering the skill applied correctly, confirm:

- explicit `rails-pair-programming` activation occurred
- intent and mode were established
- relevant 5T, Goal, and Plan context was gathered or uncertainty was stated
- the collaborative loop stayed grounded in the current Goal and Plan
- useful questions were asked where appropriate
- wrap-up was triggered by the user
- `pair-programming.md` was created or appended in the correct folder
- the artifact includes discoveries, discussions, decisions, open questions,
  outcomes, and yielded work
- existing session records were preserved
