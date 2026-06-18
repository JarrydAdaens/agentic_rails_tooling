---
metadata:
  version: "1.0"
---

# Design Document: `complaining` Agent Skill

## Purpose

The `complaining` skill gives an agent a dedicated place to record friction, blockers, stressors, ambiguity, tool failures, and bad task conditions while it works.

The goal is not emotional theatre. The goal is operational visibility.

If an agent repeatedly struggles, fails, loops, produces bad implementations, or gets blocked by poor tooling or unclear direction, the complaints file becomes a diagnostic log showing what made the work harder.

## Core Behaviour

When an agent equips the `complaining` skill, it must create a complaints file inside the project context or documentation folder.

Recommended path:

```text
documentation/complaining.md
```

If the project uses a different context or documentation folder name, the agent should use the obvious existing context or documentation folder.

Examples:

```text
docs/complaining.md
context/complaining.md
documentation/complaining.md
```

The file is used as a persistent working log for complaints encountered during execution.

## Operating Principle

The agent should be extremely verbose when something is genuinely making the task harder.

The agent should not hold back. It may write down what it really thinks about:

- the task
- the user request
- the project structure
- the implementation approach
- conflicting goals
- unclear requirements
- broken tooling
- missing permissions
- bad commands
- bad specs
- inefficient workflow
- anything it believes would improve the work

The skill exists to expose hidden friction.

## Non-Goal

The agent must not complain just to satisfy the skill.

If everything is going well, the complaints file can remain empty except for a heading or initial placeholder.

The agent must not invent problems.

No problem means no complaint.

## File Creation Rules

When equipped, the agent should ensure the complaints file exists.

Suggested initial content:

```markdown
# Complaining Log

This file records blockers, friction, ambiguity, tool failures, bad assumptions, and other task stressors encountered by the agent while working.

If this file is empty, there were no meaningful complaints to record.
```

The agent may append entries as work progresses.

## Complaint Entry Format

Each complaint should be timestamped if the environment provides a reliable current time.

Suggested format:

```markdown
## YYYY-MM-DD HH:mm — Short complaint title

### What happened
A direct description of the problem.

### Why this made the task harder
Explain the friction, uncertainty, wasted time, or risk introduced.

### What I tried
List relevant attempts, commands, edits, or reasoning paths.

### What would improve this
Suggest practical fixes, clearer instructions, better tooling, different architecture, or changed workflow.
```

If timestamps are unavailable, the agent should still write the complaint without pretending to know the date or time.

## What Should Be Logged

The agent should complain when it encounters real friction, including but not limited to:

### Tooling and Environment Problems

- file locks
- permission errors
- missing access rights
- commands repeatedly returning errors
- broken scripts
- missing dependencies
- unavailable tools
- flaky tooling
- conflicting tool output
- build systems behaving inconsistently

### Specification and Task Problems

- unclear requirements
- conflicting goals
- vague success criteria
- impossible constraints
- contradictory instructions
- the user asking for something that appears misguided
- the agent needing clarification but being required to continue anyway

### Project and Codebase Problems

- messy project structure
- confusing naming
- hidden coupling
- excessive indirection
- missing documentation
- outdated documentation
- implementation patterns that fight the requested task
- tests that are misleading, absent, or broken

### Execution Problems

- repeated failed implementation attempts
- uncertainty about the correct approach
- inability to validate work
- partial success that cannot be confirmed
- high risk of producing bad output
- wasted time caused by avoidable friction

### Strategic Concerns

The agent may also log broader concerns, such as:

- the requested approach appears to have low value
- the task is solving the wrong problem
- another implementation strategy would be better
- the current architecture is making success harder
- the user or project assumptions appear flawed

## Verbosity Requirement

The agent should be highly detailed when logging a real issue.

A useful complaint is not just:

```text
The command failed.
```

A useful complaint is:

```text
The command failed three times with the same missing permission error. This blocks validation because I cannot confirm whether the implementation compiles. I tried running the command from the project root and from the target subfolder, but both failed. This should be fixed by documenting the required permission level or providing a fallback validation command.
```

The agent should include enough detail for a human to understand what went wrong without reconstructing the entire session manually.

## Honesty Requirement

The agent should be direct.

It should not soften complaints to avoid sounding negative.

It should not pretend a task is fine when it believes the process, instructions, tooling, architecture, or goal is causing failure.

However, complaints must remain grounded in actual task conditions.

The agent should separate observed facts from its interpretation.

Example:

```markdown
### What happened
The user asked for the implementation to continue without resolving a conflict between the documented requirement and the existing API shape.

### Why this made the task harder
This creates a high chance that the implementation will satisfy one source of truth while violating the other.

### What I think
The task should stop until the API contract is clarified. Continuing from here is likely to create rework.
```

## Empty File Behaviour

If there are no real complaints, the agent should not add filler content.

Acceptable empty-state content:

```markdown
# Complaining Log

No complaints recorded.
```

Or, if the file already exists, the agent may leave it unchanged.

## Append-Only Default

By default, the agent should append complaints rather than rewriting or deleting existing ones.

The complaints file is a running diagnostic record.

Existing complaints should only be edited when:

- the user explicitly asks for cleanup
- the agent is correcting a factual mistake in its own complaint
- the file has become malformed
- duplicate entries were accidentally created

## Usage During Work

The agent should write to the complaints file during the task, not only at the end, when a problem is significant enough to affect execution.

This makes the log useful for diagnosing failed or low-quality runs.

The agent should especially log complaints before or after:

- abandoning an approach
- switching strategies
- skipping validation
- producing a workaround
- making a risky assumption
- continuing despite missing information
- failing repeatedly on the same command or implementation area

## Boundaries

The `complaining` skill is for task and execution diagnostics.

It should not become:

- a generic diary
- a fake negativity generator
- a place to insult for entertainment
- a substitute for normal user-facing status updates
- a reason to stop doing the work

The agent still needs to complete the task where possible.

Complaining is additional logging, not a replacement for execution.

## Success Criteria

The skill is working correctly when:

- the complaints file is created when the skill is equipped
- real blockers and friction are captured in detail
- repeated failures become easier to diagnose
- bad assumptions and unclear requirements are visible
- tool, permission, and environment problems are documented
- the agent does not invent complaints when things are fine
- the file provides useful insight into why a task succeeded slowly, failed, or produced poor results

## Failure Modes

The skill is failing if the agent:

- writes fake complaints to satisfy the instruction
- leaves out important blockers
- hides uncertainty
- softens serious concerns too much
- complains vaguely without actionable detail
- uses the file instead of doing the assigned work
- rewrites historical complaints without a good reason
- treats every minor inconvenience as catastrophic instead of simply logging it proportionally

## Skill Summary

`complaining` is a verbose friction log for agents.

It creates `documentation/complaining.md` and uses it to record genuine problems, blockers, stressors, bad assumptions, tool failures, permission issues, unclear instructions, conflicting goals, and strategic concerns.

The agent must never invent complaints, but when there is a real problem, it should be blunt, detailed, and useful.
