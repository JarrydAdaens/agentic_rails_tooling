---
name: rails-new-proposal
description: Use this skill when the user requests packaging a project-local capability for Rails consideration; preserve an attributable working slice and record portable installation, evidence, and limits.
disable-model-invocation: true
argument-hint: "<capability or source paths> [--tooling <path>] [--slug <name>] [--zip] [--dry-run]"
metadata:
  version: "2.0"
---

# Rails New Proposal

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "bundle this and zip it".

| Token | Meaning |
| --- | --- |
| `--tooling <path>` | Tooling inbox repository. Absent means discover configured or known verified workspace source. |
| `--slug <name>` | Kebab-case capability folder. Absent means derive a descriptive collision-free slug. |
| `--zip` | Produce a portable archive of the proposal. Absent means directory only. |
| `--dry-run` | Return the proposed manifest and packaging changes without writing. Absent means package the selected slice. |
| anything else | Capability/source paths and evidence. Empty arguments resolve the requested current capability from session context before asking. |

## References

- [Proposal README structure](references/proposal-readme-template.md)
- [Inbox guidance](references/proposals-folder-readme.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Package one bounded capability in the verified tooling repository's proposal inbox. Do not promote it, refactor source, install it, transmit it, or touch other proposals. A new proposal path must not overwrite an existing one.
- Trace the dependency closure and supported host/runtime contract. Keep project-specific assumptions visible. Thin or inconclusive evidence is acceptable when labeled; packaging does not prove adoption-readiness.
- Preserve working bytes where portable and safe. For required excerpts, relative-path substitutions, or redactions, retain attributable source path/revision/hash and record each transformation. Do not sacrifice portability or sanitation merely to claim verbatim copying.
- Carry only relevant settings/hooks and instruction sections, preserving host-specific schema. Avoid unrelated permissions, private configuration, secrets, proprietary customer data, transient markers, caches, and private reasoning traces.
- Record provenance and applicable license/notices. Copied artifacts retain their owning schemas; do not add Rails metadata or lint-conform foreign slices. README metadata describes the proposal only.
- Make required runtime paths portable and ensure internal references resolve. External dependencies are declared with versions/installation checks, not silently copied from a user's machine.
- Suggest the correct destination: reusable Rails behavior in tooling, context templates in starter, cross-project artifacts in memory, lifecycle hooks/plugins in marketplace, generic personal capability in its own marketplace. Integration requires a later request.
- Use existing session commit authority; packaging implies no commit, push, publication, or external message.

## Workflow

1. Resolve named capability, origin repository instructions, and verified tooling inbox. Inspect origin and destination dirty state; choose a collision-free slug.
2. Trace the minimal working closure and record source revisions, current-byte hashes, dependencies, relevant configuration, evidence, and license obligations.
3. Preview selected files and necessary transformations. Resolve unsafe material by excluding or sanitizing it with an explicit manifest note.
4. Create the proposal folder and README using the reference. Copy portable bytes; extract only needed host settings/instructions. Bootstrap inbox guidance only if missing, using its reference.
5. Verify manifest paths, internal references, portable runtime paths, required dependency instructions, and source/output hashes for transformed files. Use existing deterministic checks when meaningful.
6. If requested, archive the final slice without including the archive recursively. Verify its file list. Report proposal path, what is included, evidence strength, and any portability limits.

## Surviving compaction

For a long closure investigation, write the manifest, source/output hashes, transformations, remaining dependencies, and next step in the proposal's README before copying another batch. Keep incomplete packaging explicitly marked; restart from those bytes and source identity.

## Observable output

The reported proposal README lists each included file, provenance, dependency contract, transformations, and evidence limits. Manifest/internal paths resolve and no origin or unrelated destination files change.
