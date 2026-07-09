---
name: readme-verifiers
description: >-
  The verifiers layer of the Agentic Rails tooling repo — one folder per
  reusable acceptance check that a target project drops in and customizes to
  verify its own runtime behavior with a pass/fail verdict.
metadata:
  version: "2.0"
---

# Verifiers

`source/verifiers/` is the fourth primary layer of the tooling repo, alongside
`rules/`, `skills/`, and `agents/`. Where a **skill** says "here is how to do a
task" and an **agent** says "here is the kind of worker you are," a
**verifier** says "here is a check that delivers a pass/fail verdict on whether
a target project actually behaves correctly."

Each verifier is a self-contained, deployable folder that a consuming project
copies in and customizes at its edges. A verifier is not a document to read —
it is a check to run, with a small, clearly marked seam where the target
project plugs in its own specifics (a config file, an adapter script, a
project-defaults table) and a stable core the project does not touch.

## Why "verifiers" and not "evals"

To most AI engineers, an *eval* is an offline, scored test suite measuring
model or system quality across many cases (benchmarks, regression suites,
LLM-as-judge rubrics). The artifacts in this layer are per-task, pass/fail
acceptance checks on one change — **verifiers** (classical software testing
calls the same role a *test oracle*). The layer uses the precise term; "evals"
stays free for genuine scored suites if this repo ever grows them. See
`context/wiki/agentic-harness-lexicon.md` for the full vocabulary.

## Layout rules

- **One folder per verifier**, kebab-case, named for what it verifies (e.g.
  `game-golden-screenshot-verifier`).
- **Every verifier folder has a `README.md`** stating what it checks, how to
  run it, and exactly what the consuming project must customize. The linter
  enforces the folder name and the README (`NM001`, `ST003`).
- **Keep the customization seam small and obvious.** Ship a stub or example for
  every per-project piece (a `*.example.json` config, a stub driver, an example
  packet) and say in the README which files are meant to be replaced versus
  left alone.
- **Runnable and self-contained.** Prefer a runner that declares its own
  dependencies (e.g. `uv` inline script metadata) so a target project can run it
  without a manual install step. Keep the core logic testable on its own. When
  the behavior under test can't be scripted (e.g. judging a live desktop UI),
  the runner may instead be an evaluator sub-agent following a fixed procedure
  and report format — the verifier must still define its steps, pass criteria,
  and verdict shape precisely enough that any evaluator produces the same call.
- **Deployable.** Everything here syncs outward via Kung Fu like the rest of
  `source/`; do not leave machine-specific paths or transient run artifacts in a
  verifier folder (git-ignore per-run output).

## Current verifiers

| Verifier | Verifies |
| --- | --- |
| `game-golden-screenshot-verifier` | A game still boots and renders a deterministic scene matching a versioned golden screenshot. |
| `wpf-visual-quality-gate` | A visible WPF UI change actually works in the running app — an independent evaluator launches it, drives the interaction with real input, and screenshot-verifies the result. |
