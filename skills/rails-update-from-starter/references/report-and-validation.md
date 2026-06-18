---
name: rails-update-from-starter-report-and-validation
metadata:
  version: "1.0"
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

## Updated
| File | From Source Version | To Source Version | Notes |
| --- | --- | --- | --- |

## Current / Skipped
| File | Reason |
| --- | --- |

## Blocked
| File | Reason | Required User Action |
| --- | --- | --- |

## Historical Plans
- Completed implementation plans were left untouched.

## Validation
- Front matter checked: yes/no
- Source path validated: yes/no
- Target path validated: yes/no
- Historical implementation plans preserved: yes/no
```

Keep the report concise and concrete.

## Completion Checklist

Before considering the skill complete, confirm:

- The source starter path was provided and validated.
- The target project path was validated.
- Root framework files were inspected before documentation files.
- `context/design.md` was checked.
- `context/milestones.md` was checked.
- All target `context/goals*.md` files were checked.
- Implementation-plan templates were checked.
- Completed implementation-plan folders were not rewritten.
- Missing `agentic_rails_source_version` metadata was treated as outdated.
- Files with target source versions newer than the supplied starter were blocked, not downgraded.
- Project-specific content was preserved.
- A factual update report was produced.

## Example Trigger

```text
Use rails-update-from-starter on this project. The starter is at D:\Code Projects\agentic_rails_context_starter.
```

## Example Missing Source Path Response

```text
Where is your local agentic_rails_context_starter repository? Please provide the exact directory path on disk.
```

## Example Version Interpretation

Starter `context/design.md`:

```yaml
version: 1.4
```

Target `context/design.md`:

```yaml
version: 7.9
agentic_rails_source_version: 1.2
```

Interpretation:

```text
The target design document has evolved locally to 7.9, but it only incorporated starter design conventions up to 1.2. It is behind the starter's 1.4 design template and should be compared and selectively updated.
```

## Example Unsafe Source Version

Starter `context/milestones.md`:

```yaml
version: 1.4
```

Target `context/milestones.md`:

```yaml
version: 2.1
agentic_rails_source_version: 1.6
```

Interpretation:

```text
The target says it already incorporated starter version 1.6, but the supplied starter file is only 1.4. Do not proceed for this file. The starter checkout is probably stale or the version metadata is wrong.
```
