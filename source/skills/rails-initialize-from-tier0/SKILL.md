---
name: rails-initialize-from-tier0
description: Use this skill when the user requests project initialization from Dictation, kickoff notes, or research intake; preserve the raw source and generate only the selected useful context profile.
disable-model-invocation: true
argument-hint: "<intake path or text> [--target <repo path>] [--starter <path>] [--profile core|planned-delivery|high-consequence] [--host <name>] [--dry-run]"
metadata:
  version: "3.0"
---

# Rails Initialize From Dictation

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "preview Core".

| Token | Meaning |
| --- | --- |
| `--target <repo path>` | Destination project. Absent means the current project root. |
| `--starter <path>` | Starter source checkout. Absent means discover the configured or known sibling checkout and verify its identity. |
| `--profile <name>` | `core`, `planned-delivery`, or `high-consequence`. Absent means Core for new projects, preserving an existing adopted profile. |
| `--host <name>` | Supported host selection. Absent means resolve the active host when known; otherwise use generic instructions. |
| `--dry-run` | Report exact proposed paths/content without writing. Absent means apply the reviewed safe changes. |
| anything else | Intake path or raw text. Empty arguments use already provided session intake or known named files; ask for missing material only after discovery. |

## References

- [Target and source discovery](references/validation-and-scope.md)
- [Intake synthesis](references/tier0-synthesis-policy.md)
- [Evidence and reporting](references/report-and-validation.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Initialization is explicitly requested. Preserve raw intake faithfully in the project's existing Dictation location or `context/dictations-tier-0/`, with sensitive material redacted and omissions identified; do not delete or polish away the original evidence.
- Core is the new-project default. Add a current substantial plan or high-consequence controls only when deliberately adopted. Milestones, a backlog, numerical CER, memory, advisors, personas, and per-story commits are optional.
- Preserve maintained project truth, identities, commands, published product versions, historical paths, and unrelated work. Existing real context uses selective enrichment, not blank-starter replacement. User decisions may supersede maintained context when explicit; other contradictions remain visible.
- Generate with explicit destination/profile/host and concrete identity using the verified starter generator. Preview its selected files first; obey collision refusal. Record the exact generated framework baseline before adding project content, never fabricate a baseline from enriched project bytes.
- Reconcile previously generated content through previous framework baseline, current framework source, and current project content. A version field or Git revision alone is not a baseline. Overlap and unprovable ownership remain conflicts; preserve project bytes pending resolution.
- Discovery uses session paths, project metadata, and verified known sibling checkouts before asking. Do not infer ownership from Git author configuration or a stack solely from extensions.
- Create only context that carries an actual decision, acceptance, command, or requirement. Detailed feature plans belong close to execution. Never invent setup stories or ceremonial scaffold to make initialization appear complete.
- Initialization changes context; product implementation and commits require existing session authority. Use filesystem snapshots when needed without making a commit a prerequisite.

## Workflow

1. Resolve inputs with the discovery reference. Inspect instructions, current files, dirty state, adopted profile, and baseline evidence. Resolve identity fields from explicit intake and maintained project metadata.
2. Preserve intake or identify its existing durable copy. Extract purpose, audience, constraints, architecture, commands, immediate acceptance, and material uncertainty using the synthesis reference.
3. Choose fresh generation, trustworthy-baseline reconciliation, or selective enrichment. Preview exact additions, updates, conflicts, selected profile, and omitted optional scaffold.
4. For a new collision-free destination, run the starter generator with explicit resolved inputs. For existing projects, follow the baseline/ownership rules; use `rails-update-from-starter` for framework reconciliation rather than replacing files.
5. Add supported project decisions to the generated purpose/design note and instructions. Keep the baseline as generated source bytes. Populate a current plan only for adopted delivery work, and milestone/backlog content only for an actual requested roadmap.
6. Verify identity, selected command text, relevant links, preserved project content, and unresolved placeholders in generated maintained truth. Report using the evidence reference.

## Surviving compaction

The preserved intake and maintained purpose/design note carry source and accepted decisions. For substantial initialization use the existing primary plan, or `context/implementation-plans/initialize-project-context/plan.md`, to checkpoint exact proposed paths, baseline identity, conflicts, and next step before editing another batch. It is not a default setup milestone.

## Observable output

The reported profile and generated manifest agree, raw source remains available, and current project decisions survive. A fresh Core project has concrete identity without required milestone/backlog scaffolding.
