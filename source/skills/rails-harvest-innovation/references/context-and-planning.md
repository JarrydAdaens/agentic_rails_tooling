---
name: rails-harvest-innovation-context-and-planning
metadata:
  version: "1.0"
---

# Context And Planning

Use this reference when confirming repository roles, loading Agentic Rails context, and preparing the destination work record.

## Repository Roles

Identify:

- `destination`: the local `WPF-Starter` repository that will receive the reusable feature.
- `source`: a WPF-Starter-derived project, or another WPF project containing the reusable innovation.

The agent usually runs inside the destination starter. If the current directory is not clearly WPF-Starter, require an explicit destination path.

Signals that a repository may be WPF-Starter:

- `README.md` names `WPF-Starter`.
- `context/wpf-starter-inventory.md` exists.
- source projects include starter-flavoured names such as `Starter.WPF` or `Starter.Shared`.
- Agentic Rails files such as `AGENTIC_RAILS_README.MD` and `context/implementation-plans/` exist.

Signals that a repository may be derived:

- it carries `context/wpf-starter-inventory.md` with modifications or intentional removals.
- WPF-Starter project names, namespaces, or architecture have been renamed.
- app-specific design, milestones, sprints, stories, deployment identity, or product branding are present.

Ask before editing when the destination/source roles are ambiguous.

## Context Loading Order

Use progressive disclosure. Start with broad signals, then open only relevant sections and files.

In the destination, inspect when present:

1. `README.md`
2. `AGENTIC_RAILS.md`
3. `.agentic-rails.json`
4. `AGENTIC_RAILS_README.MD`
5. `context/wpf-starter-inventory.md`
6. `context/laws.md`
7. `context/design.md`
8. relevant `context/milestones/*.md`
9. relevant `context/sprints/*.md` and `context/backlog/*.md` stories
10. relevant `context/implementation-plans/`

In the source, inspect only what helps locate and understand the requested feature:

- file/folder/name matches for the feature
- solution/project references
- package declarations
- bootstrap and DI registration
- usage sites
- tests
- docs and implementation plans
- source inventory notes or intentional removal logs

Project-local context is authoritative for that repository. Shared tooling supplements it; it does not override laws, design, stories, or implementation plans.

## Tier 5 Work Record

For meaningful upstreaming, create or reuse a destination folder under:

```text
context/implementation-plans/STORY_x_y_harvest-short-feature-name/
```

Use the destination's existing naming pattern when one is obvious. If there is no clear story number, use a readable folder name that includes `harvest` or `upstream`.

Maintain at minimum:

```text
plan.md
implementation-log.md
```

Create optional artifacts only when the corresponding skill is active:

- `complaining.md`
- `thinking.md`
- `evidence.md`
- `handover/`

## Plan Contents

Write or update `plan.md` before implementation for non-trivial work. Include:

- source repository path
- destination repository path
- feature being harvested
- intended reusable starter capability
- known source files and symbols
- expected destination files and symbols
- extraction boundary
- project-specific items to exclude
- dependencies to preserve, replace, or reject
- acceptance criteria
- validation strategy
- open questions

If the plan cannot be written because the feature boundary is unclear, ask the user before implementation.
