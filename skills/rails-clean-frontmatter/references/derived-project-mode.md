---
name: rails-clean-frontmatter-derived-project-mode
description: Derived-project mode for rails-clean-frontmatter — preserve agentic_rails_source_version, or add it as 0.0 when missing.
metadata:
  version: "1.0"
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

## Resulting Shape

```yaml
---
name: <slug>
description: <one sentence>
metadata:
  version: "X.Y"
  agentic_rails_source_version: "A.B"   # preserved, or "0.0" if it was missing
  owner: <name>                          # when present
---
```

No `changelog` or `invocation`. Move any flat `version`/`owner` under `metadata`.

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
  `description`, `metadata.version: "1.0"`, and
  `agentic_rails_source_version: "0.0"`.
