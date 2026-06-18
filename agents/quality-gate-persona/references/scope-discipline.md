---
name: scope-discipline
metadata:
  version: "1.0"
---

# Scope Discipline

## Purpose

This reference explains how to judge whether a change belongs in the reviewed changeset.

## Authority

The authority is the task's plan or equivalent statement of intent: goal, scope, non-goals, acceptance criteria, issue text, or user instruction.

## Review Rules

- A changed file that is not justified by the plan is a finding, regardless of code quality.
- Formatting churn in unrelated regions is a finding when it obscures review or changes blame history.
- Opportunistic refactors belong in their own task unless the plan explicitly includes them.
- New dependencies, new architecture, migrations, broad renames, or cross-module ripples require explicit scope support.
- "Good code in the wrong changeset" is still a scope finding.

## Suggested Actions

Common suggested actions include:

- Revert the out-of-scope hunk.
- Split the change into a separate task or PR.
- Update the plan if the scope change was intentional and approved.
- Add explicit acceptance criteria for the new behavior before review continues.
