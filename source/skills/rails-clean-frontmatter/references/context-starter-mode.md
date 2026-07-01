---
name: rails-clean-frontmatter-context-starter-mode
description: Context-starter mode for rails-clean-frontmatter — keep agentic_rails_source_version equal to version, the starter source of truth.
metadata:
  version: "1.2"
---

# Context Starter Mode

Use this mode when the target is the left-rail template
(`agentic_rails_context_starter`). Read this only after [SKILL.md](../SKILL.md)
detection selects Starter mode.

## Confirm The Mode

Strong signals:

- `context/` with `design.md`, `milestones/`, `sprints/`, `backlog/`, `dictations-tier-0/`, and an
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

## `repo` and `owner` Policy

**Both required under `metadata`, and both must be `"default"` in this repository.**

`repo` and `owner` serve as identity anchors that derived projects overwrite during initialization. The starter ships them as `"default"` intentionally — they are the known placeholder values that `rails-initialize-from-tier0` and future agents use to find and replace stale identity before the project goes live.

- If either field is missing, add it with the value `"default"`.
- If either field holds a real name (not `"default"`), something has gone wrong — reset it to `"default"` and note it in the report.
- Do **not** infer real values from git or the filesystem here. `"default"` is the correct value for the starter template.

## Resulting Shape

```yaml
---
name: <slug>
description: <one sentence>
# skill files keep their Cursor fields top-level:
disable-model-invocation: <true|false>
metadata:
  version: "X.Y"
  agentic_rails_source_version: "X.Y"   # always equal to version
  owner: "default"
  repo: "default"
  template: "true"                       # template files only
---
```

No `changelog` or `invocation`.

## File Scope

Process Markdown front matter outside `archived/`, including:

- `context/design.md`, `context/milestones/`, `context/sprints/`, `context/backlog/`
- `context/dictations-tier-0/README-DICTATIONS-TIER-0.md` and other maintained context docs
- `context/implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/**`
- root `README.md` and `AGENTIC_RAILS_README.MD`
- any wiki, rules, or support docs the starter ships

## Notes

- This is a template repository. Fix front matter only; never replace template
  placeholders with invented project content — that is initialization work for a
  different skill.
- New front matter starts at `version: "1.0"` with `agentic_rails_source_version: "1.0"`,
  `owner: "default"`, and `repo: "default"`.
