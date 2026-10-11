---
name: rails-clean-frontmatter-context-starter-mode
description: Starter Schemas.
metadata:
  version: "2.0"
---

# Starter Schemas

Verify the actual starter README, profiles, templates, and contributor instructions. It has both source documentation and generated template material; they have different identity roles.

Maintained source docs may carry real repository identity. Do not reset contributor/source owner fields to `default`. Renderable templates may intentionally use declared generator tokens; cleanup preserves those tokens rather than inventing an owner or repo.

Apply name/description/quoted metadata.version only to starter artifacts whose instructions require them. A source-version label equals the source revision where the owning schema explicitly defines that relation; this is not a blanket mandate for all Markdown. A generated baseline manifest follows its JSON schema and is never repaired by Markdown frontmatter cleanup.

When a required source-label field changes on a genuinely owned source artifact, record the verified source revision. Do not change product-version policy or mutate template bodies. Generator tokens and copied output need their own rendering checks.
