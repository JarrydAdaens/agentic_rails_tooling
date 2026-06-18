---
name: rails-clean-frontmatter-context-starter-mode
description: Context-starter mode for rails-clean-frontmatter — keep agentic_rails_source_version equal to version, the starter source of truth.
metadata:
  version: "1.0"
---

# Context Starter Mode

Use this mode when the target is the left-rail template
(`agentic_rails_context_starter`). Read this only after [SKILL.md](../SKILL.md)
detection selects Starter mode.

## Confirm The Mode

Strong signals:

- `context/` with `design.md`, `milestones.md`, `goals*.md`, `tier0/`, and an
  `implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/` folder.
- That content is still template/placeholder (`Project Name`, `Milestone 1: Name`,
  `Goal 1.1 - Name`, `Describe the project`).
- `AGENTIC_RAILS_README.MD` or `README.md` identifies this as the starter /
  template / left rail.

If the context is filled with real project truth instead of placeholders, this is
a derived project — switch references.

## `agentic_rails_source_version` Policy

**Required, under `metadata`, and it MUST equal `version`.**

The starter defines the source generation. A starter file's own revision and the
generation it represents are the same thing, so the two numbers are always equal
here. A mismatch is an error to fix:

- If `agentic_rails_source_version` is missing, add it equal to `version`.
- If it differs from `version`, set it equal to `version`.
- When a change bumps `version`, bump `agentic_rails_source_version` to match.

## Resulting Shape

```yaml
---
name: <slug>
description: <one sentence>
metadata:
  version: "X.Y"
  agentic_rails_source_version: "X.Y"   # always equal to version
  owner: <name>                          # when present
  template: "true"                       # template files only
---
```

No `changelog` or `invocation`.

## File Scope

Process Markdown front matter outside `archived/`, including:

- `context/design.md`, `context/milestones.md`, `context/goals*.md`
- `context/tier0/README.md` and other maintained context docs
- `context/implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/**`
- root `README.md` and `AGENTIC_RAILS_README.MD`
- any wiki, rules, or support docs the starter ships

## Notes

- This is a template repository. Fix front matter only; never replace template
  placeholders with invented project content — that is initialization work for a
  different skill.
- New front matter starts at `version: "1.0"` with
  `agentic_rails_source_version: "1.0"`.
