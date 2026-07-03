---
name: rails-clean-frontmatter-tooling-repo-mode
description: Tooling-repo mode for rails-clean-frontmatter — strip agentic_rails_source_version and conform every file to the metadata.version standard.
metadata:
  version: "1.3"
---

# Tooling Repo Mode

Use this mode when the target is the reusable right-rail tooling library
(`agentic_rails_tooling`). Read this only after [SKILL.md](../SKILL.md) detection
selects Tooling mode.

## Confirm The Mode

Strong signals:

- A `source/` tree holding `source/skills/`, `source/agents/`, `source/rules/`.
- A supporting `context/` with `templates/`, `prompt-dev/`, `wiki/`, and a
  `design.md` that describes the tooling library itself.
- `AGENTIC_RAILS_README.MD` Repository Model row calls this the right rail /
  reusable tooling.
- The repo is the product (skills/agents/rules), not a project with the
  context tier system's `context/` project structure (milestones, backlog,
  implementation-plans).

If it instead carries real project context under the context tier system, it is
a derived project — switch references.

## `agentic_rails_source_version`, `repo`, and `owner` Policy

**`agentic_rails_source_version` and `repo`: remove them entirely.** Neither applies to tooling artifacts.

`agentic_rails_source_version` records which starter generation a derived project's context file last synced to — tooling artifacts are not synced against the starter, so it is meaningless here and was a past mistake. Strip it wherever it appears in front matter.

`repo` is a project-identity placeholder used by the starter and derived projects. The tooling repo is a shared library, not a project, so this field has no meaning here. Strip it if found.

`owner` is optional and may remain under `metadata` when present — it identifies a maintainer, which is useful on agents and personas.

That field records which starter generation a *derived project's* context file
last synced to. Tooling artifacts are not synced against the starter, so carrying
it is meaningless and was a past mistake. Strip it wherever it appears in front
matter (top-level or under `metadata`).

## Resulting Shape

```yaml
---
name: <slug>
description: <one sentence>
# skill files keep their Cursor fields top-level:
disable-model-invocation: <true|false>
metadata:
  version: "X.Y"
  owner: <name>          # when present
  template: "true"       # template files only
---
```

No `agentic_rails_source_version`, `repo`, `changelog`, or `invocation`.

## Rules Files Exception

Files under `source/rules/` (and `archived/rules/`) do **not** follow the
Resulting Shape above — they are authored for Claude Code's rule-loading spec,
not this repo's general standard. Never add `name`, `description`, or
`metadata.version` to one. There are exactly two valid shapes:

- **Path-scoped** — a top-level `paths:` list of quoted glob strings, nothing
  else:
  ```yaml
  ---
  paths:
    - "**/*.cs"
  ---
  ```
- **Unconditional** — no frontmatter block at all, so the rule loads every
  session (used by `global-rules.md` and `unit-testing-rules.md`).

If this skill encounters a rules file already in one of these two shapes,
leave it untouched.

## File Scope

Process every Markdown file outside `archived/`, including:

- `source/skills/**/SKILL.md` and `source/skills/**/references/**`
- `source/agents/**/AGENT.md`, persona `references/**`, and design documents
- `source/rules/**` — do **not** apply the standard shape here. Rules files
  carry only an optional top-level `paths:` list of quoted glob strings, or no
  frontmatter at all. Never add `name`, `description`, or `metadata.version`.
  Leave `paths:`-only or frontmatter-less rules files untouched (see Rules
  Files Exception above).
- `context/templates/**` (keep the `template` field under `metadata`)
- `context/wiki/**`, `context/prompt-dev/**`, and `context/design.md`
- root `README.md` and `AGENTIC_RAILS_README.MD`

Do not touch `agents/openai.yaml` provider files.

## Naming Conventions Here

- Skill and persona references use a unique `name`: the plain stem when it is
  already unique, otherwise skill- or persona-prefixed (e.g. `path-selection`
  appears in several skills, so `complaining-path-selection`).
- Rules files carry no `description` at all — see Rules Files Exception above.

## Notes

- This mode is the reference implementation. The canonical written standard lives
  in `context/wiki/repo-alignment-notes.md` under "Front Matter Standard"; keep this mode
  aligned with it.
- New front matter starts at `version: "1.0"`.
