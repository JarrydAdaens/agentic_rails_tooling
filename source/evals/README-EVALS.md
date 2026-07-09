---
name: readme-evals
description: >-
  The evals layer of the Agentic Rails tooling repo — one folder per reusable,
  runnable evaluation that a target project drops in and customizes to verify
  its own runtime behavior.
metadata:
  version: "1.0"
---

# Evals

`source/evals/` is the fourth primary layer of the tooling repo, alongside
`rules/`, `skills/`, and `agents/`. Where a **skill** says "here is how to do a
task" and an **agent** says "here is the kind of worker you are," an **eval**
says "here is a runnable check that proves a target project still behaves
correctly."

Each eval is a self-contained, deployable folder that a consuming project copies
in and customizes at its edges. An eval is not a document to read — it is a tool
to run, with a small, clearly marked seam where the target project plugs in its
own specifics (a config file, an adapter script) and a stable, engine-agnostic
core the project does not touch.

## Layout rules

- **One folder per eval**, kebab-case, named for what it verifies (e.g.
  `game-golden-screenshot-eval`).
- **Every eval folder has a `README.md`** stating what it checks, how to run it,
  and exactly what the consuming project must customize. The linter enforces the
  folder name and the README (`NM001`, `ST003`).
- **Keep the customization seam small and obvious.** Ship a stub or example for
  every per-project piece (a `*.example.json` config, a stub driver) and say in
  the README which files are meant to be replaced versus left alone.
- **Runnable and self-contained.** Prefer a runner that declares its own
  dependencies (e.g. `uv` inline script metadata) so a target project can run it
  without a manual install step. Keep the core logic testable on its own.
- **Deployable.** Everything here syncs outward via Kung Fu like the rest of
  `source/`; do not leave machine-specific paths or transient run artifacts in an
  eval folder (git-ignore per-run output).

## Current evals

| Eval | Verifies |
| --- | --- |
| `game-golden-screenshot-eval` | A game still boots and renders a deterministic scene matching a versioned golden screenshot. |
