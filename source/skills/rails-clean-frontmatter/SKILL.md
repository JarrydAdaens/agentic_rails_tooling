---
name: rails-clean-frontmatter
description: Use this skill when the user requests scoped YAML frontmatter maintenance in Rails-owned artifacts; follow each owning schema and preserve unknown fields, bodies, and provenance.
disable-model-invocation: true
argument-hint: "[target paths] [--mode tooling|starter|derived] [--dry-run] [--all-owned]"
metadata:
  version: "2.0"
---

# Rails Clean Frontmatter

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "preview these files".

| Token | Meaning |
| --- | --- |
| `--mode <name>` | Select tooling, starter, or derived policy. Absent means detect the owning repository/schema from instructions and markers. |
| `--dry-run` | Report proposed changes without writing. Absent means apply unambiguous scoped repairs. |
| `--all-owned` | Explicit repository-wide pass over artifacts whose schemas require frontmatter. Absent means named or session-selected files only. |
| anything else | Selected paths. Empty arguments use established scope; absent scope produces an inventory/preview without broad mutation. |

## References

- [Tooling schemas](references/tooling-repo-mode.md)
- [Starter schemas](references/context-starter-mode.md)
- [Derived project schemas](references/derived-project-mode.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Edit only selected Rails-owned leading frontmatter. Do not expand name/version/owner requirements to every Markdown file, raw intake, historical plan, memory record, copied proposal, vendor artifact, or host configuration.
- The owning schema governs valid keys and requirements. Preserve tool-consumed fields such as argument hints, allowed tools, compatibility, licensing, and host-specific fields. Unknown keys are preserved and reported, never silently dropped or moved.
- Preserve exact body bytes, encoding, newline style, and unrelated dirty work. Parse YAML structurally; malformed or duplicate keys that cannot be safely resolved are per-file conflicts, not permission to rewrite the body.
- Required missing values may be inferred only from unambiguous artifact evidence. Ambiguous owner, invocation policy, identity, or version remains a reported conflict; process independent safe files without forcing a repository-wide stop.
- Document revision and proven starter provenance are independent. Do not invent source-version labels, replace project ownership from Git author settings, or turn template placeholders into maintained project identity.
- Preserve historical source versions and baselines. Frontmatter repair does not reconcile the starter or product versions and does not authorize a commit.
- Exclude archives, generated outputs, provider YAML, rules with separate schemas, copied proposals, and historical evidence unless a specific schema-aware repair is requested.
- Prepare a preview before a bulk write, recheck source bytes, and retain recovery copies for substantive batches. A repeated pass on repaired files produces zero edits.

## Workflow

1. Resolve target, selected paths, and repository instructions. Inventory matched files and detect owning schemas using the references. In ambiguous mode, report possible policies without mutation.
2. Parse each selected leading block and construct the smallest schema repair. Leave unrelated/unknown fields in place. Record unsafe files with exact conflicts.
3. Preview path-level diffs and old/new local versions when applicable. Apply safe repairs within the selected scope, preserving snapshots and body bytes.
4. Run the owning parser/linter and a second transform pass to establish idempotence. Report changed files, skipped schemas, preserved unknown fields, conflicts, and check results.

## Observable output

Only selected leading blocks change, body byte comparisons match, schema checks pass for repaired artifacts, and a second pass proposes zero changes. Unknown fields and existing provenance survive.
