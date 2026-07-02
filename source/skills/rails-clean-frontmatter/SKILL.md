---
name: rails-clean-frontmatter
description: >-
  Use this skill to normalize and repair YAML front matter across an Agentic
  Rails repository: remove junk fields, enforce one metadata.version shape,
  guarantee name and description, and apply the correct agentic_rails_source_version
  policy. It auto-selects one of three modes — tooling repo, context starter, or a
  project derived from the starter — and aborts in repositories that do not use
  Agentic Rails.
disable-model-invocation: true
metadata:
  version: "1.2"
---

# Rails Clean Front Matter

Standardize Markdown YAML front matter across one Agentic Rails repository so it is
consistent, minimal, and machine-checkable.

This is a maintenance skill, not a content rewrite. It edits only the leading
front matter block of each file and never touches body prose. The exact rules for
`agentic_rails_source_version` and the file scope depend on which repository the
skill is run in, so detect the mode first.

## Required Input

Default the target to the current repository root. Accept a target path if the
user provides one.

No other input is required. The skill infers everything else from the repository.

## Mode Detection (do this first)

Decide which repository you are in before editing anything. Read the matching
reference for the full rules.

| Mode | Repository | Reference |
| --- | --- | --- |
| Tooling | the reusable right-rail tooling library (`agentic_rails_tooling`) | [references/tooling-repo-mode.md](references/tooling-repo-mode.md) |
| Starter | the left-rail template (`agentic_rails_context_starter`) | [references/context-starter-mode.md](references/context-starter-mode.md) |
| Derived | a real project created from the starter | [references/derived-project-mode.md](references/derived-project-mode.md) |

Detection signals:

- **Tooling**: a `source/` tree holding `source/skills/`, `source/agents/`, and
  `source/rules/`, supported by `context/` (with `templates/`, `prompt-dev/`,
  `wiki/`, and a `design.md` describing the tooling library itself);
  `AGENTIC_RAILS_README.MD` describes this as the right rail / reusable tooling.
  The repo *is* the product (skills/agents/rules), not a project with the
  context tier system's `context/` structure below.
- **Starter**: `context/` with `design.md`, `milestones/`,
  `backlog/`, `dictations-tier-0/`, and an implementation-plans folder, where
  that content is still template/placeholder; identified as the starter /
  template / left rail.
- **Derived**: `context/` carrying real project truth (the context tier system's
  design/milestones/backlog/implementation-plans structure), plus an
  Agentic Rails marker (`AGENTIC_RAILS_README.MD`, `.agentic-rails.json`, or
  `AGENTIC_RAILS.md`); it has no reusable `source/` capability library of its
  own and is neither of the two repositories above.

Resolve like this:

1. If no Agentic Rails signal is present at all, **abort** and tell the user:
   `rails-clean-frontmatter only runs inside Agentic Rails repositories (the tooling repo, the context starter, or a project derived from the starter). This target is none of those, so the skill cannot be applied.`
2. If exactly one mode matches, proceed with that mode's reference.
3. If signals are ambiguous or two modes both seem plausible, **stop and ask**
   the user which mode to apply. Do not guess.

## The Standard (all modes)

Every processed file ends with this shape. Tool-consumed fields stay top-level;
local data lives under `metadata`.

```yaml
---
name: <kebab-slug>
description: <one concise sentence>
# skill files only:
disable-model-invocation: <true|false>
# rules files only:
globs: [<patterns>]
alwaysApply: <true|false>
metadata:
  version: "X.Y"
  # mode-specific fields — see the mode reference:
  agentic_rails_source_version: "X.Y"   # starter and derived only
  owner: <owner>                         # starter: "default"; derived: real name
  repo: <repo>                           # starter: "default"; derived: real repo name
  template: "true"                       # template files only
---
```

Rules that hold in every mode:

- **`name` and `description` are required.** If either is missing, add and
  populate it by inferring from the file: derive `name` as a kebab-case slug from
  the filename or H1 (skill-prefix reference files so the slug is unique), and
  `description` as a one-line summary of the file's purpose.
- **Always remove** `changelog` (git is the changelog) and `invocation` (not an
  IDE-consumed field) from front matter.
- **`metadata.version` is required**, listed first under `metadata`. Keep
  `owner`, `repo`, and `template` under `metadata` when applicable to the mode.
- **`disable-model-invocation` is required on every `SKILL.md`.** It is a
  top-level Cursor skill field, not local metadata. If a processed `SKILL.md`
  is missing it, stop and ask the user whether the value should be `true` or
  `false`; do not infer, default, or choose from context. Preserve an existing
  boolean value unless the user explicitly asks to change it.
- **Keep top-level** only the tool-consumed fields: `name`, `description`, the
  Cursor skill field `disable-model-invocation`, and the Cursor rule fields
  `globs` and `alwaysApply`. Move anything else that is local data (`version`,
  `owner`, `repo`, `template`) under `metadata`.
- **Unknown field → stop and ask.** If a front matter carries a field this skill
  does not recognize (not `name`, `description`, `globs`, `alwaysApply`,
  `disable-model-invocation`, `metadata`, `version`, `owner`, `repo`, `template`,
  `agentic_rails_source_version`, `changelog`, or `invocation`), halt and ask
  the user what to do with it. Do not drop or keep it silently.
- **Exclusions**: never process anything under `archived/`, and never rewrite
  `agents/openai.yaml` provider files — those use a separate `interface:` schema,
  not Markdown front matter.

## Method (run it safely)

What this skill learned the hard way:

1. **Front matter only.** Edit just the first `---` block. Many files mention
   `agentic_rails_source_version`, `changelog`, etc. in body prose or fenced
   examples — those must be preserved untouched.
2. **Dry run, review, apply.** For bulk passes, compute the new front matter for
   every file and review the proposed changes before writing. A reviewed script
   is appropriate; this is exactly the kind of repetitive edit it suits.
3. **Indent-aware removal.** When removing a key like `changelog`, also remove
   its deeper-indented child lines, or they leak into `metadata`.
4. **Preserve encoding and line endings.** Read and write UTF-8; do not corrupt
   em-dashes or other non-ASCII. Preserve each file's existing newline style.
5. **Bump on real change only.** When a file's front matter is actually modified,
   bump the last numeric component of `version` (e.g. `1.2` → `1.3`). Files
   already compliant are left untouched. Re-running the skill on a clean repo
   makes no changes — it is idempotent.
6. **New front matter starts at `version: "1.0"`** (mode references state the
   `agentic_rails_source_version` value to pair with it).

## Verification

Before reporting done:

- Re-run the detection and transform; confirm a clean pass reports zero changes.
- Scan that no `changelog:`, `invocation:`, or out-of-policy
  `agentic_rails_source_version:` remains as a key in any front matter block.
- Confirm `name` and `description` exist in every processed file.
- Confirm every processed `SKILL.md` has top-level
  `disable-model-invocation: true` or `disable-model-invocation: false`.
- Spot-check a non-ASCII file to confirm encoding survived.

## Report

Produce a short factual report: detected mode, files changed (with old → new
version), files created, fields removed, any unknown fields that forced a stop,
and the verification result. Do not claim a file changed unless it did.

## Safety Rules

- Never edit body prose; front matter only.
- Never process `archived/` or `agents/openai.yaml`.
- Never silently keep or drop an unrecognized field — stop and ask.
- Never force `agentic_rails_source_version` to equal `version` outside the
  starter; in derived projects the two legitimately differ.
- Never invent project content while adding `name`/`description`; infer only what
  the file already makes obvious.
- Never run in a non-Agentic-Rails repository; abort with the message above.
