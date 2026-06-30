---
name: rails-clean-frontmatter-derived-project-mode
description: Derived-project mode for rails-clean-frontmatter — preserve agentic_rails_source_version, or add it as 0.0 when missing.
metadata:
  version: "1.2"
---

# Derived Project Mode

Use this mode when the target is a real project created from
`agentic_rails_context_starter`. Read this only after [SKILL.md](../SKILL.md)
detection selects Derived mode.

## Confirm The Mode

Strong signals:

- `context/` (or older `Documentation/`) carrying real project truth — actual
  design, milestones, and goals, not placeholders.
- An Agentic Rails marker: `AGENTIC_RAILS_README.MD`, `.agentic-rails.json`, or
  `AGENTIC_RAILS.md`.
- The repository is neither `agentic_rails_tooling` nor
  `agentic_rails_context_starter`.

This is the messy real-world case: a project where past agents left inconsistent
or missing front matter. The job is to clean junk and conform to the standard
layout without disturbing project content.

## `agentic_rails_source_version` Policy

**Keep it; it is meaningful here, and it may differ from `version`.**

This field records which starter generation the file last reconciled against. A
refined project file legitimately has a high `version` and a lower
`agentic_rails_source_version`. Never force them equal.

- If present, preserve its value (only re-quote/normalize formatting).
- If **absent, add it and set it to `"0.0"`**. That marks the file as very old or
  skipped by sloppy past agents, and flags it for a future
  `rails-update-from-starter` pass.
- Bumping `version` during cleanup does **not** change
  `agentic_rails_source_version`.

## `repo` and `owner` Policy

**Both required under `metadata`, and neither may be `"default"` in a derived project.**

These fields were inherited from the starter template where they served as known placeholders. In a real project they must hold the actual repository name and owner. A `"default"` value in a derived project is a sign that initialization was skipped or incomplete.

- If either field is absent, infer and add the real value:
  - `owner`: read from `git config user.name`; if unavailable, ask the user.
  - `repo`: read from the repository's remote URL or root folder name; if unavailable, ask the user.
- If either field is `"default"`, replace it with the inferred real value using the same inference above.
- If either field already holds a non-default real value, preserve it as-is.
- Do **not** accept `"default"` as a valid final value in a derived project — report it as a fix, not a skip.

## Resulting Shape

```yaml
---
name: <slug>
description: <one sentence>
# skill files keep their Cursor fields top-level:
disable-model-invocation: <true|false>
metadata:
  version: "X.Y"
  agentic_rails_source_version: "A.B"   # preserved, or "0.0" if it was missing
  owner: "Jarryd Adaens"                # real owner, never "default"
  repo: "my-project"                    # real repo name, never "default"
---
```

No `changelog` or `invocation`. Move any flat `version`/`owner`/`repo` under `metadata`.

## File Scope

Process Markdown front matter outside `archived/`, including:

- `context/**` or `Documentation/**` maintained project docs (design, milestones,
  goals, tier0 intake, implementation plans, logs, handovers)
- root `README.md` and any Agentic Rails framework files
- project-local skills, agents, or rules if the project carries its own

Do not touch `agents/openai.yaml` provider files. Leave completed historical
implementation-plan and provenance artifacts' content alone — fix only their
front matter.

## Notes

- Cleanup only. Removing junk and fixing layout must not edit project prose or
  invent design decisions.
- If a file has no front matter at all, add the full block: inferred `name` and
  `description`, `metadata.version: "1.0"`, `agentic_rails_source_version: "0.0"`,
  and real (non-default) `owner` and `repo` values.
