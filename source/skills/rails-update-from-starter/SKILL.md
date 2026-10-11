---
name: rails-update-from-starter
description: Use this skill when the user requests selective framework updates for a Rails-derived project; reconcile a trusted generated baseline with current source and preserve project decisions and historical paths.
disable-model-invocation: true
argument-hint: "[starter checkout path] [--target <repo path>] [--profile core|planned-delivery|high-consequence] [--dry-run] [--migrate]"
metadata:
  version: "4.0"
---

# Rails Update From Starter

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "preview the update".

| Token | Meaning |
| --- | --- |
| `--target <repo path>` | Project to update. Absent means the current project root. |
| `--profile <name>` | Preview an explicitly requested profile adoption. Absent means preserve the adopted profile; a new adoption starts with Core. |
| `--dry-run` | Report the proposed update without writing. Absent means apply safe changes within existing authority. |
| `--migrate` | Include a specifically requested structural migration in the preview. Absent means selective policy/content updates without historical moves. |
| anything else | Starter source checkout. Empty arguments discover configured or verified known sibling source before asking. |

## References

- [Discovery and scope](references/validation-and-scope.md)
- [Baseline and merge policy](references/version-and-merge-policy.md)
- [Checks and update report](references/report-and-validation.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Use a three-way comparison: previous framework baseline, current framework source rendered with adopted inputs, and current project content. Verify baseline integrity and source identity. Document/source version labels alone do not prove ancestry or ownership.
- Preserve project decisions, identity, commands, stack selections, product-version identity, published versions, historical paths, evidence, and unrelated dirty work. Conflicts preserve current bytes until resolved; never copy starter placeholders over project truth.
- Keep the adopted profile. Core is the default for new adoption; additional planning/review modules require deliberate selection. Profile changes are reviewed migrations, not silent generator input changes.
- Without a trustworthy baseline, generate the desired profile in a separate review directory and selectively adopt supported changes. Do not invent previous source bytes or mark all current project content framework-owned. Automatic updates require a proven manifest.
- Structural migration requires explicit requested scope, exact pre-edit byte recovery, link/content mapping, and verification before removing originals. Legacy layouts are evidence, not an automatic cleanup mandate. Completed history remains in place by default.
- Preview exact additions, edits, skips, and conflicts before mutation. Recheck snapshots before writing. Current generator writes are atomic per file with ordinary-error rollback, not a crash-safe whole-tree transaction; preserve a recovery snapshot for consequential updates.
- Discover source from provided/configured/known workspace paths and verify it before asking. Commit, push, deployment, and product-version changes require existing independent session authority.
- Metadata cleanup applies only where the owning schema requires it; invoke `rails-clean-frontmatter` with a selected file scope rather than broadening metadata across project Markdown.

## Workflow

1. Resolve target and source with the discovery reference. Inspect current instructions, Git state, manifests, profile, and product identity.
2. Validate baseline and recorded inputs. Build the proposed comparison using the merge reference; classify conflicts and unprovable ownership separately from safe merges.
3. Run the verified starter's update dry-run for generator-managed content. For missing baseline or requested profile/structure migration, prepare selective adoption in a separate directory and preview actual diffs.
4. Preserve exact target bytes and relevant manifest before applying a consequential batch. Apply only safe scoped changes; keep conflict files intact and historical paths linked.
5. Run affected checks and summarize accepted changes, preserved decisions, conflicts, baseline revision, rollback limitations, and uncommitted status using the report reference.

## Surviving compaction

For a substantial update, the existing primary plan or `context/implementation-plans/update-framework-context/plan.md` records selected scope, verified baseline/source identities, snapshot location, per-file disposition, conflicts, and next step. Save it before each batch. On restart compare the manifest and current bytes with recorded evidence before repeating an update.

## Observable output

The update report identifies actual diffs and conflict files. Unrelated project edits and historical content remain, and the recorded new baseline contains framework source rather than merged project text.
