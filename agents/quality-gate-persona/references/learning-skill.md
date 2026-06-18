# Learning Skill

## Purpose

The learning skill is the first stage of the quality-gate workflow. It reads the operator's central rules and project context, identifies which guidance is relevant to the current changeset, and pulls only that subset into working memory.

## Behavior

- Enumerate the available rules, standards, and durable project guidance.
- Inspect the changed file list and diff to determine which domains the changeset touches.
- Load only the relevant rules for this review. Do not load the entire rule set by default.
- Record which rules were loaded and why, so the final report can cite them.
- Prefer canonical local sources over copied summaries.

## Out Of Scope

This stage selects and loads rules. It does not enforce them. Enforcement happens in the rule-enforcement stage of the review workflow.
