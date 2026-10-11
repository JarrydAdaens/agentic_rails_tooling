---
name: rails-clean-frontmatter-tooling-repo-mode
description: Tooling Schemas.
metadata:
  version: "2.0"
---

# Tooling Schemas

Confirm the reusable tooling repository using its instructions and actual capability layout. Its deployable Markdown artifacts use name and quoted `metadata.version`; skills/personas also require discovery description and their owning authoring fields.

Preserve tool-consumed fields at their required level. Current skill examples include `disable-model-invocation`, `argument-hint`, `allowed-tools`, `compatibility`, and `license` where supported. Provider YAML uses its own schema and is excluded.

Rules are distinct: this repository's source rule files have only an optional top-level quoted `paths` list or no frontmatter. Do not add artifact metadata to them. A host-specific rule elsewhere follows that host's schema instead.

`agentic_rails_source_version` is inappropriate for an actually tooling-authored artifact, but removing it requires verified ownership; an imported artifact can carry valid provenance. Preserve intentional owner/license/origin metadata. Do not remove `repo` merely because a global normalization once called it junk.

Normalize flat local version/owner fields into metadata only when that transformation is required and unambiguous. Remove deprecated keys such as a redundant changelog only when the owning policy explicitly retires them. New versions begin at the owning schema's initial revision, and changed frontmatter bumps a revision only when that repo requires it. A skill's missing invocation boolean cannot be chosen mechanically from its filename.
