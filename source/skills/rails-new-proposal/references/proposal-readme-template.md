---
name: rails-new-proposal-proposal-readme-template
description: Proposal README Structure.
metadata:
  version: "2.0"
---

# Proposal README Structure

The proposal README stands alone and belongs to the proposal, not the copied artifacts. Adapt optional headings to the capability rather than requiring empty ceremony.

```markdown
---
name: <capability-slug>
description: <capability and intended user>
metadata:
  version: "0.1"
  status: proposed
---

# Proposal: <Capability>

## Use case and contract
<Trigger, intended behavior, supported hosts/runtimes, installation and removal.>

## Evidence and limits
<Actual observations/checks, source links, negative results, confidence; no invented proof.>

## Contents and provenance
| Proposal path | Role | Source repo / relative path | Revision / source hash | Output hash / transformation |
| --- | --- | --- | --- | --- |
| <path> | <role> | <origin> | <evidence> | <same or documented transformation> |

## Dependencies and verification
<Declared external runtime/package versions, install steps, checks and actual results.>

## Suggested destination and generalization
<Owning layer, project-specific assumptions, portability limitations, license/notices.>
```

Use source-relative paths and public/approved repository identity for portable attribution; do not expose private usernames or machine paths unnecessarily. Source Git revision describes committed content; dirty source needs a current-byte hash too. Excerpts/redactions have distinct output hashes and exact transformation notes.

Settings snapshots contain only adopted capability keys, with host schema intact. Captured command paths resolve relative to installation/project roots supported by that host. Shared installation instructions must not rely on the packaging machine's drive letters.
