---
name: rails-planning-phaser
description: >-
  Use this skill when an Agentic Rails implementation plan needs sequential,
  independently verifiable phases. Choose natural seams, preview the proposed
  structure, preserve the exact original including uncommitted changes, and
  replace phased output through recoverable file operations. Existing phases
  require explicit rephasing. Assess complexity, effort, and risk in words;
  numerical CER scorecards are optional and never select executor models.
disable-model-invocation: false
argument-hint: "<plan path> [--dry-run] [--rephase] [--cer] [--file] [--recover]"
metadata:
  version: "2.0"
---

# Rails Planning Phaser

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and treat plain-language equivalents as equal to the tokens
("show the proposed cut" means `--dry-run`; "redo these phases" means `--rephase`).

| Token | Meaning |
| --- | --- |
| `--dry-run` | Preview boundaries, assessments, and file changes; write nothing in the target plan folder. Absent means apply. Takes precedence over all write requests. |
| `--rephase` | Authorize replacing existing phased output after preserving its exact current contents. Absent means refuse an already-phased target. |
| `--cer` | Also request numerical grading through `rails-grade-cer`. Absent means qualitative assessments only. |
| `--file` | Retain a requested CER scorecard beside the plan; implies `--cer`. Absent means do not create a scorecard file. |
| `--recover` | Restore an interrupted phasing replacement instead of generating new phases. Absent means ordinary phasing. |
| anything else | The target plan path or identifiable plan request. Empty arguments use the plan already identified in the session; investigate known paths before asking if the target remains ambiguous. |

## Purpose

Turn substantial work into coherent checkpoints. Routine work can remain one plan.
Read [decomposition guidance](references/decomposition.md) for seam selection and
assessment, and the [manifest](references/manifest-template.md) and
[phase](references/phase-template.md) templates for output structure.

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Phases are sequential increments with artifact-specific acceptance checks.
  Keep tightly coupled work together; a checkpoint must leave the affected artifact
  usable or explicitly document a preexisting failure.
- Complexity, effort, and risk inform decomposition and checks, never a fixed
  capability threshold or model roster. Executors inherit the active runtime
  model unless the user has authorized a supported override for this run.
- `--dry-run` wins over `--rephase`, `--file`, and `--recover`: report the proposed
  action without changing the target folder. Existing phased targets require
  `--rephase` for replacement; previewing them does not authorize replacement.
- Preserve byte-exact current source and prior phases before replacement,
  including dirty or untracked content. Git history is additional provenance,
  not a substitute for that backup. Historical copies are evidence, never active
  plans or another status owner.
- Preserve unrelated files and requested scorecards. Generate no transient
  scorecard for ordinary grading; consume `rails-grade-cer` inline output when
  numerical grading was requested. Do not delete an existing scorecard.
- Stage all outputs and record durable recovery state before the first target
  change. Apply only against the inspected source fingerprint. Stop on concurrent
  changes, pending recovery, or an ambiguous ownership contract.
- The manifest owns phase execution status. Phase files describe work and checks;
  backups and journals record phasing operations, not execution status.
- Do not execute the implementation, commit, or dispatch workers merely because
  the plan was phased.

## Procedure

1. Resolve the target and inspect it using the bundled file helper described in
   [file operations](references/file-operations.md). Check pending recovery before
   deciding whether existing output is a normal phased plan.
2. If recovery was requested, follow the helper's recovery operation. Otherwise,
   read the current plan and any registered phase state. For rephasing, use the
   current manifest, phases, and preserved source together; account for completed
   work and current user decisions instead of resurrecting obsolete steps.
3. Assess the whole request in words. Split only where checkpoints improve
   execution, recovery, or verification. If no useful cut exists, retain one unit
   and update its decomposition note. Invoke `rails-grade-cer` by name only for
   `--cer` or `--file`, obtaining inline results.
4. Prepare a proposed manifest and phase contents using the templates. State
   dependencies, acceptance commands, unresolved assumptions, and the reason for
   each seam. There is no mandatory number of phases. When the work spans separate
   stories, report that scope and keep the current plan intact unless restructuring
   those stories was authorized.
5. Present the proposed files and assessments for a preview. For an apply request,
   stage the complete output set outside the target plan folder. Include a
   scorecard only when `--file` was requested. Record the inspected fingerprint and
   apply through the helper; report its backup and recovery paths.
6. Report the manifest and phase paths, preserved original path, actual checks,
   and any unresolved risks. Distinguish file replacement checks from acceptance
   tests for the future implementation.

## Surviving compaction

The target folder's `phasing-state.json` points to
`phasing-history/<run-id>/transaction.json`. That journal records the exact source
fingerprint, preserved bytes, staged outputs, and replacement state before writes.
The active manifest and phase files carry the executable plan. Resume by reading
the pointer and journal, then inspect before another mutation. Pending replacement
requires recovery or a conflict diagnosis; do not rerun phasing over it.

## Observable outputs

- A preview leaves the target folder byte-for-byte unchanged.
- An applied output has one active plan and contiguous `phase-N.md` files when
  phases were chosen, with exact previous content in the reported history folder.
- No output assigns a model from a numeric score. Requested scorecards remain.
- Interrupted replacement can restore preserved files; concurrent edits produce
  a diagnostic without overwriting those edits.
