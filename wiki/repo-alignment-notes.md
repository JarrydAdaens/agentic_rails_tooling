---
metadata:
  version: "1.2"
---

# Repository Alignment Notes

This repository separates reusable context into layers:

- `rules/`: concise standards and style-shaping constraints.
- `skills/`: reusable task capabilities and workflow modules.
- `agents/`: specialist worker definitions with operating contracts and references.
- `prompt_dev/`: source prompt material used to create or refine artifacts.

## Front Matter Standard

Every Markdown file that carries front matter follows one shape:

- A `metadata:` block with `version` as its first child. `version` is the file's
  own revision (see [versioning.md](versioning.md)).
- **`name` and `description` are required** on every file. If either is missing,
  infer and add it from the file's content.
- **Tool-consumed fields stay top-level**, because IDEs read them directly:
  `name`, `description`, and the Cursor rule fields `globs` and `alwaysApply`.
- **Local or custom data lives under `metadata`**: `version`, `owner`, and
  `template` (for template files).
- Do **not** use these anywhere in this repo's front matter:
  `agentic_rails_source_version` (context-file only — never on tooling
  artifacts), `changelog` (git is the changelog), or `invocation` (not an
  IDE-consumed field).
- `agents/openai.yaml` provider files use their own `interface:` schema and are
  not Markdown front matter; leave their shape alone.

The `rails-clean-frontmatter` skill applies and repairs this standard across an
Agentic Rails repository, including the starter and derived-project variants of
the `agentic_rails_source_version` rule.

Example:

```yaml
---
name: my-skill
description: Use this skill when ...
metadata:
  version: "1.2"
  owner: Jarryd Adaens
---
```

## Skill Rules For This Repository

- Every skill directory must contain `SKILL.md`.
- The folder name and `name` frontmatter must match.
- Skill names use lowercase letters, numbers, and hyphens.
- Put nonstandard data such as local version, owner, or template status under `metadata`.
- Skills and agents use only `metadata.version` for their own revision. Do not add `agentic_rails_source_version` to tooling artifacts — that field is for derived-project context files only (see [versioning.md](versioning.md)).
- Descriptions should use "Use this skill when..." style when it helps activation.
- Keep workflow-style skills under `skills/` for now, but make their orchestration role explicit.

## Agent Rules For This Repository

Agents are not Agent Skills, but they should follow similar hygiene:

- Use concise trigger-oriented descriptions.
- Put local version and owner information under `metadata`.
- Keep reference maps explicit so agents load only relevant files.
- Keep provider-facing `agents/openai.yaml` metadata aligned with `AGENT.md`.

## Migration Notes

- The discovery-test skill was renamed to `check-dot-agent` for strict Agent Skills compatibility.
- `skill-template` now has valid YAML frontmatter and is a concrete starter template.
- `skill-template-advanced` now has a spec-compliant name matching its folder.
