---
name: complaining
description: >-
  Use this skill when an agent should record genuine blockers, friction,
  ambiguity, tool failures, bad assumptions, risky constraints, or other
  execution problems while it works. By default, complaints go into the active
  plan's `## Complaints / Friction` section or are raised directly to the user;
  a standalone complaining.md is opt-in, for explicit requests or long-running
  workflows that need durable friction tracking.
disable-model-invocation: true
metadata:
  version: "2.0"
---

# Complaining

Record real execution friction so later humans and agents can diagnose why work was slow, risky, blocked, or low quality.

This is operational visibility, not emotional theatre.

## Default Destination

**Default: raise it, or write it into the active plan.** Two defaults, not one file:

- If the friction is worth the user's attention now, say so directly in the conversation.
- If it should also survive past the conversation, and an active plan is identifiable, append it to that plan's `## Complaints / Friction` section (see `rails-planning`'s [plan-template.md](../rails-planning/references/plan-template.md)) instead of creating a separate file.

Do not create a standalone `complaining.md` for ordinary tasks. It is opt-in — see "Standalone Artifact" below.

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

## Standalone Artifact (Opt-In)

Create a standalone `complaining.md` only when:

- the user explicitly asks for a standalone complaint log, or
- the work is a long-running agentic workflow (an orchestration run, a multi-session build-out, a plan-spam or boss-execute run) where durable, separately-tracked friction tracking is genuinely needed beyond what one plan's `## Complaints / Friction` section can hold.

When justified, path selection:

1. If the target repository follows Agentic Rails and an active implementation-plan folder is identifiable, write `complaining.md` in that story folder — `context/implementation-plans/<milestone-slug>/<story-slug>/complaining.md`.
2. If the friction belongs to a planning run rather than one story, write it under that run's scoped folder — `context/implementation-plans/<milestone-slug>/_planning-runs/<run-slug>/complaining.md` — never directly under `context/`.
3. Otherwise write `complaining.md` in the target project's context or documentation folder, preferring `context/`, then `documentation/`, then `docs/`, and say plainly that it was written outside any plan or run folder because none exists.

Load [references/path-selection.md](references/path-selection.md) when the correct location is not obvious.

Initial content may be:

```markdown
# Complaining Log

This file records blockers, friction, ambiguity, tool failures, bad assumptions, and other task stressors encountered by the agent while working.

If this file is empty, there were no meaningful complaints to record.
```

## Operating Model

1. Identify the target project root, whether an active plan is identifiable, and whether a standalone log is justified (see "Standalone Artifact" above).
2. Work on the assigned task normally.
3. When a real blocker, failure, ambiguity, risky assumption, or meaningful process problem appears, raise it to the user, append it to the active plan's `## Complaints / Friction` section, or append it to the standalone `complaining.md` — whichever destination was resolved in step 1.
4. Keep existing complaints append-only unless the user explicitly asks for cleanup or the agent is correcting its own factual mistake.
5. Continue the task after logging unless the problem truly blocks progress.

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

- No standalone `complaining.md` was created unless the user explicitly requested one or a long-running workflow genuinely needed durable friction tracking beyond one plan's `## Complaints / Friction` section.
- When a standalone log exists, it lives inside the **target project**, not inside the tooling repository, and in the correct location for the detected project type:
  - Agentic Rails with an active implementation-plan folder → `<milestone-slug>/<story-slug>/complaining.md`
  - Agentic Rails, friction scoped to a planning run rather than one story → `<milestone-slug>/_planning-runs/<run-slug>/complaining.md`
  - Agentic Rails without an identifiable active plan or run → an existing context or documentation folder (`context/`, `documentation/`, `docs/`, `Docs/`), or a newly created `context/` if none exists, with the fallback stated plainly
  - Non-Agentic-Rails project → an existing context or documentation folder (`context/`, `documentation/`, `docs/`, `Docs/`), or a newly created `context/` if none exists
- No fake complaint was added when nothing meaningful went wrong.
- Any real blocker or friction was appended with enough detail for a later reader to understand it without reconstructing the whole session.
- Entries follow the format in [references/entry-format.md](references/entry-format.md): timestamp omitted when reliable time was unavailable, interpretation separated into a `What I think` section.
- Existing complaints were preserved unless there was a specific reason to edit them.
