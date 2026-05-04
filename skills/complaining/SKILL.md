---
name: complaining
description: >-
  Use this skill when an agent should maintain a project-local complaint log for
  genuine blockers, friction, ambiguity, tool failures, bad assumptions, risky
  constraints, or other execution problems while it works.
metadata:
  version: "1.0"
---

# Complaining

Maintain a durable project-local log of real execution friction. This skill exists to expose hidden blockers and bad task conditions so later humans and agents can diagnose why work was slow, risky, blocked, or low quality.

This is operational visibility, not emotional theatre.

## When to use

- The user explicitly asks the agent to use the `complaining` skill.
- A project workflow requires a complaint, blocker, friction, or diagnostic log.
- The agent is doing work where failed attempts, bad assumptions, tool failures, unclear requirements, or risky compromises should be recorded.
- A prior run failed or looped and the next run needs better visibility into what made the work difficult.

## Do not use

- Do not invent complaints to prove the skill is active.
- Do not log generic mood, roleplay, entertainment, or personal diary entries.
- Do not use the complaint log instead of normal user-facing status updates.
- Do not stop doing the assigned work just because a complaint was recorded.
- Do not treat minor inconveniences as catastrophic. Log proportionally.

## Artifact

When this skill is active, ensure a complaints file exists in the target project documentation folder.

Default path:

```text
documentation/complaining.md
```

If the project already uses a different documentation folder, follow that convention instead. Load [references/path-selection.md](references/path-selection.md) when the correct location is not obvious.

Initial content may be:

```markdown
# Complaining Log

This file records blockers, friction, ambiguity, tool failures, bad assumptions, and other task stressors encountered by the agent while working.

If this file is empty, there were no meaningful complaints to record.
```

## Operating Model

1. Identify the target project root and its documentation folder.
2. Ensure the complaint log exists before substantive work begins.
3. Work on the assigned task normally.
4. Append a complaint when a real blocker, failure, ambiguity, risky assumption, or meaningful process problem appears.
5. Keep existing complaints append-only unless the user explicitly asks for cleanup or the agent is correcting its own factual mistake.
6. Continue the task after logging unless the problem truly blocks progress.

## Reference Loading

Load only the references needed for the current moment.

- [references/path-selection.md](references/path-selection.md): use when choosing or creating the complaints file path.
- [references/logging-policy.md](references/logging-policy.md): use when deciding whether an issue is worth logging or how blunt to be.
- [references/entry-format.md](references/entry-format.md): use when appending a complaint entry or initializing the file.

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

- The complaint log exists in the target project's documentation folder.
- No fake complaint was added when nothing meaningful went wrong.
- Any real blocker or friction was appended with enough detail for a later reader to understand it without reconstructing the whole session.
- Existing complaints were preserved unless there was a specific reason to edit them.
