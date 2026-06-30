---
name: rails-update-from-starter-report-and-validation
metadata:
  version: "2.0"
---

# Report And Validation

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
- Detected era / mode: `<seven-tier alignment / five-tier migration / mixed — describe>`
- Checkpoint: `<git commit / git status noted / filesystem checkpoint / not created and why>`

## Updated
| File | From Source Version | To Source Version | Notes |
| --- | --- | --- | --- |

## Migrated (five-tier to seven-tier)
| Old surface | New surface | What was ported |
| --- | --- | --- |

## Current / Skipped
| File | Reason |
| --- | --- |

## Blocked
| File | Reason | Required User Action |
| --- | --- | --- |

## Historical Plans
- Completed implementation plans (`GOAL_*/`, `STORY_*/`) were left untouched.

## Superseded Originals
| File | Status | Recommended Action |
| --- | --- | --- |

## Validation
- Front matter checked (nested metadata.* shape): yes/no
- Source path validated as current seven-tier starter: yes/no
- Target path validated and era detected: yes/no
- Every goal mapped to a backlog story (migration only): yes/no/n-a
- Every milestone mapped to a doc and a Milestones Index row (migration only): yes/no/n-a
- Historical implementation plans preserved: yes/no
- Preserved links resolve: yes/no
```

Keep the report concise and concrete.

## Completion Checklist

Before considering the skill complete, confirm:

- The source starter path was provided and validated as the current seven-tier starter (not a stale checkout).
- The target project path was validated and its era detected.
- The correct mode was chosen (alignment for seven-tier targets, migration for older five-tier targets).
- A recovery checkpoint was created before any structural migration, or its deferral was recorded.
- Root framework files were inspected before documentation files.
- `context/design.md` (and its Milestones Index) was checked.
- The milestones surface was checked (`milestones/` folder, or a single `milestones.md` in migration mode).
- The story surface was checked (`backlog/`, or every `goals*.md` in migration mode).
- Sprint scaffolding exists or was created when migrating.
- In migration mode: every goal became a backlog story with content and plan links preserved, and every milestone became a doc plus an index row.
- Completed implementation-plan folders (`GOAL_*/`, `STORY_*/`) were not rewritten or renamed.
- Missing `metadata.agentic_rails_source_version` was treated as outdated and normalized to the nested, quoted shape.
- Files with target source versions newer than the supplied starter were blocked, not downgraded.
- Project-specific content was preserved, and no retired vocabulary was reintroduced.
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
The target design document has evolved locally to 7.9, but it only incorporated starter design conventions up to 1.2. It is behind the starter's 2.0 design template, predates the seven-tier layout, and should be compared and selectively updated — including adding the Milestones Index subsection.
```

## Example Migration Interpretation

Target shows `context/milestones.md` and `context/goals1.md`, `context/goals2.md`, with top-level unquoted `version:` fields.

```text
This is a five-tier target. Run in migration mode: split milestones.md into context/milestones/milestone-N.md and add a Milestones Index to design.md; convert each goal in goals1.md and goals2.md into a story in context/backlog/, preserving names, statuses, acceptance criteria, and plan links; create context/sprints/ scaffolding; rename context/tier0/ to context/dictations-tier-0/ if present; and leave any GOAL_* plan folders untouched as history. Checkpoint first; report the old files as superseded.
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
