---
name: rails-update-from-starter-report-and-validation
metadata:
  version: "3.0"
---

# Report And Validation

<!-- rails-lint-allow: VC004 -->
<!-- Justification: the Example Migration Interpretation section below
     illustrates rails-update-from-starter's compatibility layer against a
     concrete legacy target. It must name the literal retired paths
     (`context/milestones.md`, `context/goals1.md`, `context/goals2.md`,
     `context/tier0/`) that the skill's migration mode detects and ports,
     since that is the exact scenario the example exists to document. -->

Use this reference before finishing `rails-update-from-starter`.

## Required Report Format

Produce this factual report. Do not claim a file was updated unless it was actually changed.

```markdown
# Agentic Rails Update Report

## Source
- Starter path: `<path>`
- Starter version evidence: `<files / versions inspected>`

## Target
- Project path: `<path>`
- Detected era / mode: `<current-layout alignment / legacy migration / mixed — describe>`
- Checkpoint: `<git commit / git status noted / filesystem checkpoint / not created and why>`

## Updated
| File | From Source Version | To Source Version | Notes |
| --- | --- | --- | --- |

## Migrated (legacy layout to current layout)
| Old surface | New surface | What was ported |
| --- | --- | --- |

## Current / Skipped
| File | Reason |
| --- | --- |

## Blocked
| File | Reason | Required User Action |
| --- | --- | --- |

## Historical Plans
- Completed implementation plans (legacy-named or `<milestone-slug>/<story-slug>/` folders) were left untouched.

## Superseded Originals
| File | Status | Recommended Action |
| --- | --- | --- |

## Validation
- Front matter checked (nested metadata.* shape): yes/no
- Source path validated as current starter: yes/no
- Target path validated and era detected: yes/no
- Every goal or legacy scheduled story mapped to a story, either inside its milestone or in the backlog (migration only): yes/no/n-a
- Every milestone mapped to a doc, containing its stories directly, and a Milestones Index row (migration only): yes/no/n-a
- Any legacy scheduling folder was folded into milestone Stories sections and retired rather than recreated (migration only): yes/no/n-a
- Historical implementation plans preserved: yes/no
- Preserved links resolve: yes/no
```

Keep the report concise and concrete.

## Completion Checklist

Before considering the skill complete, confirm:

- The source starter path was provided and validated as the current starter (not a stale checkout).
- The target project path was validated and its era detected.
- The correct mode was chosen (alignment for targets already on the current milestone-centric layout, migration for older legacy targets).
- A recovery checkpoint was created before any structural migration, or its deferral was recorded.
- Root framework files were inspected before documentation files.
- `context/design.md` (and its Milestones Index) was checked.
- The milestones surface was checked (`milestones/` folder with stories inside, an index-only `milestones/` plus legacy scheduling folder, or a single `milestones.md` in migration mode).
- The story surface was checked (`backlog/` and each milestone's Stories section, or every `goals*.md` in migration mode).
- In migration mode: every goal or legacy scheduled story became a story — inside its milestone if already scheduled, otherwise in the backlog — with content and plan links preserved, every milestone became a doc containing its stories directly plus an index row, and any legacy scheduling folder was retired rather than recreated.
- Completed implementation-plan folders were not rewritten or renamed.
- Missing `metadata.agentic_rails_source_version` was treated as outdated and normalized to the nested, quoted shape.
- Files with target source versions newer than the supplied starter were blocked, not downgraded.
- Project-specific content was preserved, and no retired vocabulary or retired layout shape was reintroduced.
- No optional sidecar files (`questions.md`, `evidence.md`, `complaining.md`, `research.md`) were scaffolded into any plan folder by default.
- A factual update report was produced.

## Example Trigger

```text
Use rails-update-from-starter on this project. The starter is at D:\Code Projects\agentic_rails\agentic_rails_context_starter.
```

## Example Missing Source Path Response

```text
Where is your local agentic_rails_context_starter repository? Please provide the exact directory path on disk.
```

## Example Version Interpretation

Starter `context/design.md`:

```yaml
metadata:
  version: "2.0"
```

Target `context/design.md`:

```yaml
metadata:
  version: "7.9"
  agentic_rails_source_version: "1.2"
```

Interpretation:

```text
The target design document has evolved locally to 7.9, but it only incorporated starter design conventions up to 1.2. It is behind the starter's 2.0 design template, predates the current milestone-centric layout, and should be compared and selectively updated — including adding the Milestones Index subsection.
```

## Example Migration Interpretation

Target shows `context/milestones.md` and `context/goals1.md`, `context/goals2.md`, with top-level unquoted `version:` fields.

```text
This is a legacy target from the earliest layout generation. Run in migration mode: split milestones.md into context/milestones/milestone-N.md and add a Milestones Index to design.md; convert each goal in goals1.md and goals2.md into a story — placed directly inside its milestone's Stories section if it was already scheduled for delivery, otherwise staged in context/backlog/ — preserving names, statuses, acceptance criteria, and plan links; rename context/tier0/ to context/dictations-tier-0/ if present; and leave any GOAL_* plan folders untouched as history. Checkpoint first; report the old files as superseded.
```

## Example Unsafe Source Version

Starter `context/design.md`:

```yaml
metadata:
  version: "2.0"
```

Target `context/design.md`:

```yaml
metadata:
  version: "3.1"
  agentic_rails_source_version: "2.4"
```

Interpretation:

```text
The target says it already incorporated starter version 2.4, but the supplied starter file is only 2.0. Do not proceed for this file. The starter checkout is probably stale or the version metadata is wrong.
```
