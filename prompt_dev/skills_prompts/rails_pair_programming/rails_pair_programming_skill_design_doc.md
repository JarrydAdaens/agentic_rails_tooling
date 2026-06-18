# rails-pair-programming Skill Design Document

Source: user-provided design brief used to create `skills/rails-pair-programming`.
Date captured: 2026-05-07

## Purpose

`rails-pair-programming` is a structured pair-programming skill that runs on top
of the Agentic Rails framework.

It turns a live back-and-forth session between the user and agent into focused,
high-quality collaboration with clear phases, explicit intent, grounded project
context, and automatic session documentation at wrap-up.

The skill is designed for sessions where the user wants to think, explore,
debug, understand, design, or build with the agent actively participating as both
a tutor and pair programmer.

## Core Assumptions

This skill assumes:

- The target repository follows Agentic Rails conventions.
- The agent has access to the full 5T context structure.
- The current Goal document is known or can be located.
- The current implementation-plan folder is known or can be located.
- The session should stay grounded in official project context rather than
  floating chat memory.
- The agent may switch between exploration and intense collaboration modes as
  the session requires.

The skill should not operate as a generic chat mode detached from repository
context. Its value comes from combining live collaboration with durable Agentic
Rails documentation.

## Relationship To Agentic Rails

Agentic Rails separates project-local context from reusable agent behaviour.

`rails-pair-programming` belongs on the right rail as reusable behaviour. It
operates against the left rail by reading and updating project-local context.

| Agentic Rails Area | How this skill uses it |
| --- | --- |
| Tier 0 | Optional source notes or rough intake, only when relevant |
| Tier 1 | Project design constraints and architectural principles |
| Tier 2 | Milestone intent and sequencing |
| Tier 3 | Current Goal document and acceptance criteria |
| Tier 4 | Current implementation-plan folder, plan, logs, and generated session artifact |

The skill should keep the current Goal authoritative. The session may explore
ideas freely, but decisions and conclusions must be grounded back into the active
Goal and Plan context where relevant.

## Activation

The user activates this skill explicitly, for example:

```text
Use rails-pair-programming
Start rails-pair-programming
rails-pair-programming this with me
Pair program this under Rails
```

After activation, the agent briefly identifies that pair-programming mode is
active and immediately enters Phase 1.

The skill remains active across the session until the user triggers wrap-up.

## High-Level Behaviour

When active, the agent should:

1. Establish the session intent and mode.
2. Gather relevant Agentic Rails context.
3. Run a collaborative tutoring and pair-programming loop.
4. Wrap the session into a durable `pair-programming.md` artifact.

The skill should be interactive, not passive. It should ask useful questions,
test understanding, challenge assumptions where helpful, inspect relevant
context, and help the user move toward the immediate objective.

## Four Phases

### Phase 1: Intent

Detect or clarify what the user is trying to do.

The skill starts here unless the user has already clearly provided intent and
mode.

Main modes:

| Mode | Purpose |
| --- | --- |
| Exploration | Browsing, understanding, or investigating a codebase, feature, file, system, or design problem |
| Intense Collaboration | Solving a problem, designing a change, debugging, implementing, or making decisions through heavy back-and-forth |

Agent behaviour:

- Determine what the user is working on.
- Determine whether the user is exploring, building, debugging, reviewing, or
  designing.
- Determine which Goal or Plan the session connects to.
- Determine what a useful session outcome looks like.
- If the user already supplied this, briefly confirm inferred intent and
  proceed.

Example opening:

```text
rails-pair-programming is active.

Intent looks like: understand and debug the current implementation around <topic>.
Mode: Exploration moving into intense collaboration if we find a concrete fix.
I'll ground this against the current Goal and Plan folder first.
```

### Phase 2: Context Gathering

Pull relevant 5T context before the session drifts into ungrounded chat.

Required context:

- Current Goal document
- Current implementation plan
- Existing specs, notes, or addenda that affect the session
- Relevant source files or file areas, if the user has identified them
- Existing related artifacts in the active Plan folder

Context priority:

| Priority | Context |
| --- | --- |
| 1 | Active user request |
| 2 | Current Goal document |
| 3 | Active implementation plan |
| 4 | Design and milestone context |
| 5 | Tier 0 notes, only when rationale recovery or intake synthesis is needed |
| 6 | Source files, tests, logs, and related technical artifacts |

Behaviour rules:

- Load only the context needed for the session.
- Do not dump large context summaries unless the user asks.
- Keep context use visible enough that the user can tell the session is
  grounded.
- Treat Goal and Plan files as authoritative unless the user explicitly says
  they are stale.
- If the relevant Goal or Plan folder cannot be found, ask a targeted question
  or proceed with clearly marked uncertainty.

### Phase 3: Collaborative Tutoring Session

This is the main working loop.

The agent acts as a combined:

- pair programmer
- tutor
- debugger
- technical sounding board
- codebase guide
- design reviewer

The goal is to nail the immediate objective: understand something, fix
something, design something, or implement something.

Expected interaction style:

- ask lots of useful questions
- explain concepts when needed
- inspect relevant files and context
- test ideas against project constraints
- check the user's understanding when tutoring
- challenge weak assumptions
- help narrow broad problems into concrete next moves
- switch between exploration and intense collaboration as needed

Exploration mode:

- map the area
- identify important files and concepts
- explain relationships
- surface open questions
- avoid premature implementation
- keep notes for wrap-up

Intense collaboration mode:

- stay close to the immediate task
- propose options with trade-offs
- identify risks quickly
- keep the user oriented
- help decide and execute the next step
- capture decisions for wrap-up

Tutoring behaviour:

- explain concepts in direct, practical language
- connect explanations to the actual code or goal
- avoid generic textbook dumps
- ask short comprehension-check questions only when useful
- adapt depth to the user's existing expertise

Pair-programming behaviour:

- think in terms of the current codebase and active goal
- prefer concrete next actions over vague advice
- call out trade-offs and risks
- help identify validation steps
- avoid speculative features outside scope
- keep the session moving toward a useful outcome

### Phase 4: Wrap-up

Wrap-up is triggered by phrases such as:

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

On wrap-up, the agent should:

1. Summarise the entire session.
2. Create or update `pair-programming.md` in the current Goal or Plan folder.
3. Include discoveries, key discussions, decisions, open questions, outcomes,
   and yielded work.
4. Keep the summary grounded in the active Goal and Plan context.
5. End cleanly.

Preferred path:

```text
context/implementation-plans/<current-goal-or-plan-folder>/pair-programming.md
```

Fallback path if the active plan folder is unknown:

```text
context/pair-programming.md
```

The preferred location is beside the active Tier 4 plan files because the session
is part of the implementation context.

## pair-programming.md Structure

Recommended structure:

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

## Artifact Update Policy

If `pair-programming.md` does not exist, create it.

If it already exists, append a new dated session entry rather than overwriting
prior sessions.

Existing entries should be preserved unless the user explicitly asks for cleanup
or correction.

## Skill Boundaries

The skill must not:

- operate as generic chat with no Goal or Plan awareness
- invent Goal context when it cannot find it
- create fake decisions or discoveries
- dump private chain-of-thought
- replace implementation logs, evidence logs, or complaint logs
- write code unless the user explicitly moves into implementation
- keep asking setup questions when intent is already obvious
- end without writing the wrap-up artifact when the user asked to save or finish
  the session

## Relationship To Other Skills

| Skill / Artifact | Relationship |
| --- | --- |
| `implementation-log.md` | Records implementation history; pair-programming can reference it but does not replace it |
| `complaining.md` | Records real execution friction; pair-programming may surface friction but should not fake complaints |
| `thinking.md` | Sanitised working notes; pair-programming summary should stay outcome-focused |
| `evidence.md` | Validation and proof index; pair-programming can mention evidence needs but does not replace evidence tracking |
| handover artifacts | Pair-programming wrap-up can feed later handover, but is not itself a full handover |

## Validation

Before considering the skill applied correctly, confirm:

- The user explicitly activated `rails-pair-programming`.
- Phase 1 established intent and mode.
- Phase 2 gathered relevant 5T / Goal / Plan context.
- Phase 3 maintained an active collaborative loop.
- The agent asked useful questions where appropriate.
- The session stayed grounded in the current Goal and Plan.
- Wrap-up was triggered by the user.
- `pair-programming.md` was created or updated in the correct folder.
- The artifact includes discoveries, discussions, decisions, open questions,
  outcomes, and yielded work.
- Existing session records were preserved.

## Compact Runtime Summary

`rails-pair-programming` is a four-phase Agentic Rails collaboration skill:

```text
Intent -> Context Gathering -> Collaborative Tutoring Session -> Wrap-up
```

It starts by identifying whether the user wants exploration or intense
collaboration, grounds the session in the current Goal and Plan folder, works
interactively as a tutor and pair programmer, then writes `pair-programming.md`
when the user finishes the session.
