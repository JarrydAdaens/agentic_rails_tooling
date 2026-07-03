---
name: readme-scripts
description: Guide to the repo-infrastructure scripts — the rails linter, what it enforces, how to run it, and how files opt out of rules.
metadata:
  version: "1.1"
---

# Scripts

Repo infrastructure. Nothing in this folder is deployed by Kung Fu; it exists to keep the deployable artifacts well-formed.

## rails_lint.py

Deterministic linter for Agentic Rails repositories. It enforces the authoring conventions in `AGENTS.md` (frontmatter shape, kebab-case naming, skill/agent folder structure) and the banned-vocabulary map from the six-tier reform addendum (retired sprint/seven-tier/Scrum language, legacy context paths, numbered tier references outside the canonical files).

```text
python scripts/rails_lint.py <repo-root> [...]   # lint one or more repos
python scripts/rails_lint.py --list-rules        # show every rule id
python scripts/rails_lint.py . --only VC001      # run a subset
python scripts/rails_lint.py . --skip VC005      # ignore a subset
python scripts/rails_lint.py . --include-archived
```

Exit code 0 means clean, 1 means violations, 2 means usage error. Run it on this repo, the context starter, and the memory repo; it is also the intended pre-deploy gate for Kung Fu.

Deliberate exemptions built into the rules:

- `archived/` is skipped unless `--include-archived` is passed.
- `design.md` and `agenticworkflow.md` may use numbered tiers — they hold the canonical tier table. Everything else must use tier names.
- Rules files under `source/rules/` (and `archived/rules/`) use Claude Code's shape: an optional top-level `paths:` list of quoted glob strings, or no frontmatter at all for rules that should always load. They need no `name`, `description`, or `metadata.version` — FM002 and FM005 exempt them, and FM007 checks that any `paths:` entries are quoted.
- Reference files need only `name` and `metadata.version`; `description` is required on `SKILL.md`/`AGENT.md`, where discovery happens.
- Memory learning captures (`type: session-learning`) are historical records and are fully exempt — history is not rewritten to new vocabulary.

A file can opt out of specific rules with a pragma comment anywhere in the file:

```html
<!-- rails-lint-allow: VC001 VC002 -->
<!-- rails-lint-allow: all -->
```

Use pragmas sparingly — mainly for migration notes that must name the old vocabulary on purpose.

## Tests

```text
cd scripts
python -m unittest test_rails_lint
```
