---
name: complaining
description: >-
  Use this skill when an agent should maintain a project-local complaint log for
  genuine blockers, friction, ambiguity, tool failures, bad assumptions, risky
  constraints, or other execution problems while it works.
metadata:
  version: "1.2"
---

# Complaining

Maintain a durable project-local log of real execution friction. This skill exists to expose hidden blockers and bad task conditions so later humans and agents can diagnose why work was slow, risky, blocked, or low quality.

This is operational visibility, not emotional theatre.

## When to use

This is an agent-invoked skill. The agent activates it proactively when conditions require a complaint log.

- A workflow skill, orchestration run, or multi-step task is in progress and real blockers, tool failures, ambiguity, or risky assumptions appear.
- A prior run failed or looped and the next run needs better visibility into what made the work difficult.
- The user explicitly asks the agent to use the `complaining` skill or requires a diagnostic log.

## Do not use

- Do not invent complaints to prove the skill is active.
- Do not log generic mood, roleplay, entertainment, or personal diary entries.
- Do not use the complaint log instead of normal user-facing status updates.
- Do not stop doing the assigned work just because a complaint was recorded.
- Do not treat minor inconveniences as catastrophic. Log proportionally.

## Artifact

When this skill is active, ensure a complaints file exists in the target project.

Path selection:

1. If the target repository follows Agentic Rails and an active implementation-plan folder is identifiable, write `complaining.md` in that folder.
2. Otherwise, if the target repository follows Agentic Rails, write `context/complaining.md`.
3. Otherwise write `complaining.md` in the target project's context or documentation folder, preferring `context/`, then `documentation/`, then `docs/`.

Load [references/path-selection.md](references/path-selection.md) when the correct location is not obvious.

Initial content may be:

```markdown
# Complaining Log

This file records blockers, friction, ambiguity, tool failures, bad assumptions, and other task stressors encountered by the agent while working.

If this file is empty, there were no meaningful complaints to record.
```

## Operating Model

1. Identify the target project root and complaint log path.
2. Ensure the complaint log exists before substantive work begins.
3. Work on the assigned task normally.
4. Append a complaint when a real blocker, failure, ambiguity, risky assumption, or meaningful process problem appears.
5. Keep existing complaints append-only unless the user explicitly asks for cleanup or the agent is correcting its own factual mistake.
6. Continue the task after logging unless the problem truly blocks progress.

## Complaint Standard

A useful complaint is specific, grounded, and actionable. It separates observed facts from interpretation, explains the cost of the friction, and says what would improve the situation.

Weak:

```text
The command failed.
```

Useful:

```text
The validation command failed three times with the same missing permission error. This blocks compile verification because I cannot tell whether the implementation is correct or merely untested. I tried running it from the repository root and the project subfolder. The project should document the required permission level or provide a fallback validation command.
```

## Boundaries

Be direct when something is genuinely making the work worse. Do not soften serious concerns into vague niceness, but keep every complaint tied to actual task conditions.

The complaint log is a diagnostic artifact. It is allowed to criticize the task, tooling, architecture, requirements, implementation strategy, or workflow when that criticism is relevant to completing the work.

## Validation

Before considering the skill applied correctly, confirm:

- The complaint log exists inside the **target project**, not inside the tooling repository.
- The complaint log is in the correct location for the detected project type:
  - Agentic Rails with an active implementation-plan folder → `<plan-folder>/complaining.md`
  - Agentic Rails without an identifiable active plan → `context/complaining.md`
  - Non-Agentic-Rails project → an existing context or documentation folder (`context/`, `documentation/`, `docs/`, `Docs/`), or a newly created `context/` if none exists
- No fake complaint was added when nothing meaningful went wrong.
- Any real blocker or friction was appended with enough detail for a later reader to understand it without reconstructing the whole session.
- Entries follow the format in [references/entry-format.md](references/entry-format.md): timestamp omitted when reliable time was unavailable, interpretation separated into a `What I think` section.
- Existing complaints were preserved unless there was a specific reason to edit them.
