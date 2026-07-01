---
name: rails-planning-phaser-manifest-template
metadata:
  version: "1.0"
---

# Manifest Template

There are two variants. Use the Single-Unit Variant when CER graded the whole plan under the tier-1 threshold `(5, 5, 5)` — no phasing occurred. Use the Full Manifest Variant once the plan has actually been fractured into phases.

## Single-Unit Variant (No Phasing Needed)

Do not restructure the plan's body. Add one small block near the top of the existing `plan.md`, directly under its `## Metadata` section (or at the very top if the plan has no metadata section), and leave everything else untouched:

```markdown
## CER Assignment

- Graded: `<DD Month YYYY>`
- Scores: Complexity `<n>`, Effort `<n>`, Risk `<n>`
- Assigned Model: `qwen-3.6-local` (tier 1)
- Status: Single unit — no phasing needed
```

This plan is not a manifest. It has no phase registry and no phase files, so `rails-planning-phaser` may run on it again later if the plan changes enough that its CER scores change (e.g. after a revision adds scope). Update the `CER Assignment` block in place on re-grade rather than appending a second one.

## Full Manifest Variant (Phased)

Rewrite the original `plan.md` in place into this shape:

```markdown
# <Task Name> - Phased Plan Manifest

## Metadata

- Task Type: `GOAL | FEATURE | BUG | REFACTOR | SPIKE`
- Task ID: `<carried over from the original plan, if it had one>`
- Task Name: `<short task title>`
- Status: `Phased`
- Owner: `<carried over from the original plan, if known>`
- Last Updated: `<DD Month YYYY>`
- Pre-Phase CER Scores: Complexity `<n>`, Effort `<n>`, Risk `<n>` — the scores that triggered phasing

## Plan Context

<One short paragraph condensing the original plan's goal/objective and high-level scope. Not a verbatim copy of the original plan body — the full original wording remains recoverable from git history. Enough for a sub-agent or human skimming the manifest to understand what the work is for, without reconstructing it from the phase files alone.>

## Working With Phases

Phases run strictly in sequence — never out of order. Each phase is a complete, independently testable unit; after finishing a phase, the application compiles and runs. Before starting a phase, read only that phase's file (not the other phases, not this manifest's history) plus this manifest's current state. On finishing a phase, update that phase's row below: set `Status`, confirm the `Model` used, set `Validation`, and add a short `Notes` entry if useful to the next phase or to a human reviewing later.

## Phase Registry

| Phase | Status | Model | C | E | R | Validation | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| phase-1 | not started | `<assigned model>` | `<n>` | `<n>` | `<n>` | pending | |
| phase-2 | not started | `<assigned model>` | `<n>` | `<n>` | `<n>` | pending | |

- **Status:** `not started` / `in progress` / `completed` / `failed`
- **Model:** the assigned model — what the orchestrator spins up for that phase. Must match the `recommended-model` in that phase file's own frontmatter.
- **C / E / R:** that phase's re-graded CER scores, from `rails-grade-cer`, not invented.
- **Validation:** `pending` / `pass` / `fail`
- **Notes:** free text. Leave blank at phasing time unless a short phase summary is genuinely useful up front — this is left to judgment, not mandatory.

## Phasing Rationale

<Optional, brief: why the plan breached threshold (which axis, roughly how far over), and anything notable about how the seams were chosen — e.g. "cut after the migration step because that is the last point the app is guaranteed to still run before the new service integration begins." Keep this short; it explains the phasing decision, it does not restate the plan.>
```

Do not add sections beyond these. The manifest's job is to route sub-agents and track state, not to re-host the original plan's full detail.
