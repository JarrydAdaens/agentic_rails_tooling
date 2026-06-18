---
metadata:
  version: "1.0"
---

# Versioning: `version` vs `agentic_rails_source_version`

Agentic Rails front matter carries two version numbers that answer two different
questions. They are independent on purpose. Confusing them breaks context sync.

## The two fields

| Field | Question it answers | Where it lives |
| --- | --- | --- |
| `version` | "What revision is *this file* at, on its own terms?" | Any maintained file (context files, skills, agents). |
| `agentic_rails_source_version` | "Which starter generation was this file's *layout* last reconciled against?" | Derived-project context files (e.g. `design.md`, `milestones.md`, `goals*.md`) and the context starter itself. |

### `version` — local evolution

A file's own revision counter. Bump it (major or minor) whenever the file
changes, including hours of local refinement that have nothing to do with the
starter. A well-loved project's `design.md` can sit at `version: 7.9` while the
starter's `design.md` is still at `1.4`. That gap is expected and healthy — it
just means the file has been refined heavily in that project.

`version` is **not** used to decide whether to sync from the starter.

### `agentic_rails_source_version` — sync baseline

The starter generation whose *layout and conventions* this file last
incorporated. This is the field that drives context updates.

To check whether a project's context layout is behind the starter:

1. Read `agentic_rails_source_version` in the project's context file (e.g. the
   `design.md` of a WPF utility project).
2. Read the current source generation for that file in the
   `agentic_rails_context_starter` repository.
3. If the project's value is **lower**, the project's layout is outdated — run
   `rails-update-from-starter` (or let the Dark Factory do it). If equal, it's
   current.

The local `version` stays whatever it is; only `agentic_rails_source_version`
moves up to the starter generation after a successful reconcile.

## Why both exist

Keeping the two numbers separate lets a project's context **content** diverge
freely (high `version`) while its **layout** stays synced to a shared shape
(`agentic_rails_source_version`). That shared shape is what lets agentic
automation — including the Dark Factory that consumes work across many
projects — rely on a consistent context structure no matter how much any single
project has been refined.

## Scope: where each field belongs

- **Derived-project context files** and the **context starter**: carry both
  fields. `agentic_rails_source_version` is meaningful here because it is
  compared against the starter.
- **Tooling artifacts in this repo** (`skills/`, `agents/`): use only
  `metadata.version` for their own local revision. Do **not** add
  `agentic_rails_source_version` to a skill or agent — nothing consumes it
  there, and it would falsely imply the artifact is sync-tracked against the
  context starter.
