---
name: harness-directory-pattern
description: >-
  The standard shape of a target project's harness/ directory — the single
  root folder holding all agentic machinery (verifiers, gates, guardrail
  seams, sensors, actuators), one self-contained module per artifact, with
  the module contract, the three-home rule, and the promotion pipeline.
metadata:
  version: "1.0"
---

# The Harness Directory Pattern

Every Agentic Rails project carries one root folder, **`harness/`**, holding
all the machinery agents use to operate, observe, and validate that project's
real behavior. The name is the classic CI sense of a *test harness*: the rig
automation uses to run checks and collect logs, evidence, and verdicts. (It
does not collide with the other sense — the executable loop between a model
and its tools — because that harness is the vendor's product and never lives
in a repository.)

The **normative** definition ships to projects via the context starter
(`agentic_rails_context_starter/harness/README-HARNESS.md`, with
`HARNESS_MODULE_TEMPLATE.md` as the module scaffold). This page is the
repo-side knowledge: the pattern at a glance, why it is shaped this way, and
where it came from. If this page and the starter disagree, the starter wins —
fix this page.

## The shape

```text
project-root/
├── AGENTS.md                          # §0.2 carries the standing harness trigger lines
├── context/                           # narrative tiers — per-story evidence goes HERE, never in harness/
└── harness/
    ├── README-HARNESS.md              # layer rules, module contract, installed-module index
    │
    ├── jobs-done-guardrail/           # SEAM module — engine is a marketplace plugin
    │   ├── config.json                #   build/test commands + relevance filters
    │   ├── eval-mode.json             #   enabled | force | ask | plan | disabled
    │   ├── runs/                      #   git-ignored: per-run logs, results, repair prompts
    │   └── state/                     #   git-ignored: passing fingerprints
    │
    ├── game-golden-screenshot/        # SEAM module — engine is a marketplace plugin
    │   ├── eval_config.json           #   the game-specific knobs
    │   ├── drivers/my_driver.py       #   deterministic-state route (replaces the shipped stub)
    │   ├── goldens/golden.png         #   committed, human-approved reference images
    │   └── last-run/                  #   git-ignored
    │
    ├── rgb-thumbstick-visual/         # LOCAL module — project-specific verifier, full engine here
    │   ├── README.md                  #   trigger, contract, setup, self-test, seam
    │   ├── config.json
    │   ├── scripts/
    │   ├── truth/                     #   committed golden data
    │   └── runs/                      #   git-ignored
    │
    └── webcam-sensor/                 # LOCAL module — an instrument (sensor/actuator), not a check
        ├── README.md
        └── scripts/
```

One self-contained, kebab-case folder per module. A module is one verifier,
gate, guardrail seam, sensor, or actuator — the unit of independent adoption
and removal. No shared `scripts/` grab-bag between modules: if two modules
need the same engine, the engine is itself a module (an instrument) or it
belongs in the marketplace.

## The three-home rule

Where a given piece of machinery lives is decided by two questions —
*reusable across projects?* and *does it have a lifecycle?*

| Reusable? | Lifecycle (hooks, engine updates)? | Home |
| --- | --- | --- |
| Yes | Yes | `agentic_rails_marketplace` plugin; the project keeps only a seam module |
| Yes | No — inert procedure/knowledge | This repo's `source/skills/` or `source/agents/`, deployed by Kung Fu |
| No — project-specific | — | A full local module in the project's `harness/` |

A **seam module** contains exactly what its plugin's README prescribes
(config, defaults, drivers, goldens) and nothing else; the engine runs from
the plugin cache and updates through the marketplace. A missing seam must
degrade to a silent skip — plugins are installed per machine but adopted per
project.

## The module contract

Every runnable module states in its README: a **trigger** (when an agent
must run it), **stable exit codes** (0 pass, 1 fail, distinct codes per
infrastructure failure — "couldn't check" is always a failure, never a
silent pass), **agent-parseable output** (one `PASS`/`FAIL` line with the
reason, plus a JSON report saying *why*), a **config-not-code tuning seam**,
and a **self-test** that needs no real app or hardware. Evaluator-run gates
(procedure documents executed by a sub-agent) meet the same spirit: explicit
trigger, pass criteria, attempt loop, fixed report format.

Two standing rules with no exceptions: per-story evidence and outcomes go in
the implementation plan under `context/`, never in a module; and secrets
live at the user level (environment variables, dotnet user-secrets,
keychains), never in a module folder.

## Wiring and enforcement

A module only exists if agents know they must run it. Advisory triggers are
the standing lines in the project's `AGENTS.md` §0.2 (shipped by the context
starter). Enforced triggers come exclusively from marketplace guardrail
plugins registering real hooks — never from hand-edited `settings.json` or
`.codex/` files, which reopen the install-without-uninstall trap.

## The promotion pipeline

```text
local harness/ module  →  proves itself  →  rails-new-proposal (this repo's proposals/ inbox)
  →  marketplace plugin  →  project module shrinks to its seam, same name, same place
```

The module keeps its name and folder across its whole life; only its
contents shrink when the engine graduates.

## Lineage

The pattern merges the two halves that each proved out separately, plus a
name that was right the first time:

- **quota_tank `verifiers/`** contributed the structure: self-contained,
  independently removable modules with README-as-contract and ignored
  `runs/`/`state/` inside. All three of its modules successfully left the
  project (two became marketplace plugins, one became the `wpf-tree-sensor`
  skill), proving the lifecycle property.
- **rog-battery-lighting `tools/`** contributed the engineering contract:
  stable exit codes, one-line agent-parseable verdicts, JSON failure
  reports, config seams, synthetic self-tests, and the instrument idea
  (webcam sensor, Home Assistant smart-plug actuator). Its role-sliced
  layout (pieces of one eval smeared across five folders) and unwired
  AGENTS.md are the counterexamples the rules above exist to prevent. It is
  deliberately grandfathered — do not migrate it.
- **fishing-line `harness/`** contributed the name, and the ancestor of the
  `jobs-done-guardrail` plugin.

Vocabulary for everything in this page — guardrail, gate, verifier, sensor,
advisor — is defined in [agentic-harness-lexicon.md](agentic-harness-lexicon.md).
