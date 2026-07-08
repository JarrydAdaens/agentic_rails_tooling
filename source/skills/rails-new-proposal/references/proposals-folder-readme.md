---
name: proposals-folder-readme
metadata:
  version: "1.0"
---

# Proposals Folder README

The `rails-new-proposal` skill writes this file to `proposals/README-PROPOSALS.md` the first time it bootstraps the inbox. Copy the block below verbatim (without this preamble). Never overwrite an existing `README-PROPOSALS.md`.

```markdown
---
name: readme-proposals
metadata:
  version: "1.0"
---

# Proposals

This folder is the **inbox** for proven, project-local innovations that may
deserve a place in the Agentic Rails system. Each subfolder is one
self-contained proposal created by the `rails-new-proposal` skill: a
`README.md` pitching the capability (use case, evidence it worked, manifest,
suggested destination) plus a verbatim slice of every file needed to make it
work in another project.

## How to use this folder

- **Review**: read a proposal's `README.md`; the slice beside it is the proof
  and the raw material.
- **Promote**: ask an agent to integrate the proposal into its suggested
  destination (tooling `source/`, the context starter, memory, or elsewhere),
  generalizing the slice as needed - then delete the proposal folder.
- **Delete**: if a proposal is not worth keeping, delete its folder.
- **Share**: a proposal may contain a `<slug>.zip` snapshot for sending to
  other developers; regenerate it after any edits.

## Ground rules

- Slices are **verbatim copies from foreign projects**. This folder is
  excluded from `rails_lint.py`; do not lint-conform, refactor, or otherwise
  "improve" slice files in place. Generalization happens at promotion time.
- Nothing in this folder is deployed. It is a holding area, not a rail.
```
