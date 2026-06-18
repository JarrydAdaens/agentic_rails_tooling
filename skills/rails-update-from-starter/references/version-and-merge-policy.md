# Version And Merge Policy

Use this reference when interpreting front matter, comparing source versions, or deciding whether a merge is safe.

## Front Matter Model

Context files use YAML front matter.

Each comparable file may have two relevant version concepts:

| Field | Meaning |
| --- | --- |
| `version` | The local file version inside the derived project. This may advance independently as the project evolves. |
| `agentic_rails_source_version` | The version of the corresponding source file from `agentic_rails_context_starter` that this local file last incorporated. |

If the repository already uses an equivalent field name for the Agentic Rails source version, preserve that convention.

If no equivalent source-version field exists, treat the local file as older than the starter. Add or normalize the field during update when safe.

Recommended front matter shape:

```yaml
---
version: 0.3
agentic_rails_source_version: 1.4
agentic_rails_source_file: context/design.md
---
```

The local `version` field is not the same as `agentic_rails_source_version`.

A child project may legitimately have:

```yaml
version: 7.9
agentic_rails_source_version: 1.2
```

This means the local project has heavily evolved, but it last incorporated starter conventions from starter file version `1.2`.

## Version Comparison Rules

For each comparable source/target file:

1. Read source front matter from the starter file.
2. Read target front matter from the derived project file.
3. Compare the target's `agentic_rails_source_version` against the source file's `version`.

If the target source version is missing:

- Assume the target is outdated.
- Compare the source and target files.
- Update framework structure where safe.
- Improve or add missing front matter.
- Preserve project-specific content.

If the target source version is lower than the starter version:

- Treat the target as behind.
- Compare the source and target files.
- Selectively merge starter improvements.
- Update `agentic_rails_source_version` after successful merge.
- Preserve the target file's local `version` unless the repository convention requires incrementing it.

If the target source version equals the starter version:

- Treat the target as current.
- Skip content changes unless required front matter fields or obvious structural metadata are missing.
- Report that the file is current.

If the target source version is higher than the starter version:

- Stop for that file.
- Do not downgrade or guess.
- Record the file as blocked and tell the user.
- Explain that the starter checkout may be stale, the target version metadata may be incorrect, or the target may have been updated from a newer starter.

## Merge Policy

Prefer section-aware and front-matter-aware merging.

Do not perform a blind full-file overwrite unless all of the following are true:

- The target file is still obvious starter placeholder content.
- The user has not customized it.
- The source file is clearly the newer authoritative starter version.
- Overwriting will not delete project-specific design, milestones, goals, or execution history.

Preserve:

- project purpose
- architecture decisions
- milestone definitions
- goal names and statuses
- acceptance criteria
- out-of-scope decisions
- implementation-plan links
- completed work references
- project-specific constraints
- manually maintained rationale

Starter updates should add or improve:

- front matter fields
- context hierarchy descriptions
- navigation sections
- template instructions
- framework identity sections
- placeholder cleanup guidance
- new conventions that help future agents understand the project
- links to new standard files or folders

If a safe merge is not obvious, leave the file unchanged and report the conflict.

## Implementation-Plan Template Handling

Keep current implementation-plan templates synchronized:

- `context/implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/plan.md`
- `context/implementation-plans/IMPLEMENTATION_PLAN_TEMPLATE/implementation-log.md`

Preserve project-local additions unless they conflict with newer starter requirements.

Do not migrate old completed plans unless explicitly requested.
