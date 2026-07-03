---
name: complaining-logging-policy
metadata:
  version: "1.0"
---

# Logging Policy

Log real friction when it meaningfully affects execution quality, confidence, time, or risk.

Do not log filler. No problem means no complaint.

## Log These

- Permission errors, file locks, missing access rights, unavailable tools, missing dependencies, flaky scripts, or conflicting tool output.
- Repeated command failures or implementation attempts that force a strategy change.
- Unclear requirements, conflicting goals, impossible constraints, or vague success criteria.
- Misleading, absent, or broken tests and validation paths.
- Confusing project structure, hidden coupling, excessive indirection, stale documentation, or naming that makes correct work harder.
- Risky assumptions made because the agent must continue without enough information.
- Strategic concerns where the requested approach appears low value, aimed at the wrong problem, or likely to create rework.

## Do Not Log These

- Routine work taking normal effort.
- Tiny mistakes that were immediately corrected and did not matter.
- Complaints invented to satisfy the skill.
- Insults, jokes, or theatrical negativity.
- Private speculation that is not tied to the task.

## Tone

Be blunt, precise, and useful.

Separate:

- what happened
- why it made the task harder
- what was tried
- what would improve the situation
- what is interpretation rather than observed fact

Direct criticism is acceptable when it is grounded. The log may criticize the task, request, architecture, workflow, tooling, or assumptions if those things are actually causing friction.

## Timing

Append during the task when the issue matters, especially before or after:

- abandoning an approach
- switching strategies
- skipping validation
- producing a workaround
- making a risky assumption
- continuing despite missing information
- failing repeatedly on the same command or implementation area
