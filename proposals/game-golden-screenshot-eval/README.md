---
name: game-golden-screenshot-eval
description: >-
  A runtime smoke eval for games: launch the game, drive it into a
  deterministic scene, capture a screenshot, compare it against a versioned
  golden image, and return exit code 0/1. For any game project that wants
  agents to verify "the game still boots and renders correctly" without a
  human watching.
metadata:
  version: "0.1"
  status: proposed
  origin_project: block-game-2 (Block Game 2 / Craft World monorepo)
  origin_path: D:\GameDev\block-game-2 (tools/autotest-eval plus in-game EVAL* scripts and the revival report)
  proposed_on: "2026-07-09"
  suggested_destination: source/workflow-skills/ (a game-runtime-eval skill
    bundling a generalized runner script and per-game configuration), with the
    revival report retained as reference material
---

# Proposal: Game Golden-Screenshot Eval

## What This Is

A one-command runtime eval for a game project. A PowerShell runner
(`tools/autotest-eval/Run-AutoTestEval.ps1`) deploys test assets, launches the
game executable with autotest arguments, waits with a kill timeout, and parses
the game's results log for a named screenshot-similarity assertion. It has two
modes: **Golden** (capture and store a reference screenshot of a deterministic
scene, reviewed by eye and committed) and **Eval** (rebuild the same scene,
capture again, assert >= 95% similarity to the golden). Exit code 0 = pass,
1 = fail; screenshots and the log excerpt from every run land in `last-run/`
for inspection. In the origin project the scene setup, screenshot capture, and
image comparison ride on the game's own legacy in-game autotest harness
(timed `.script` command timelines, `Test_PrtScn`, `Test_ImageWithin`).

## Use Case

Agents working on a game had no runtime verification beyond "it compiles."
Visual or boot regressions — a broken shader, a world-gen change, a boot-path
NRE — sailed through builds and unit tests. The eval gives an agent a cheap,
end-to-end check after any change that could affect runtime behavior: the game
boots past the menu, loads a world, builds a known scene (fixed sky, fixed
camera, deterministic 16x16 block grid), renders it, and the render still
matches a human-approved golden. The origin owner is now starting a second
game on a completely different engine — one with **no** in-game autotest
harness — and wants this same eval shape available there, which is the direct
motivation for this proposal.

## Evidence It Works

- **Commit `1703e09` in block-game-2** ("i had fable revive the auto test
  harness from 2016") landed the runner, the three `EVAL*` scripts, the
  golden, and the knowledge report in one piece of work — a decade-dormant CI
  harness brought back to life locally.
- **The revival report** (`context/reports/2026-07-03-autotest-harness-revival.md`,
  included in this slice) documents the full code-path trace and the two
  blocker-level engine fixes (a runtime `testingmode` boot argument, recursive
  test-script lookup) that were required and verified to get end-to-end runs
  working.
- **The most recent run on the origin machine caught a real divergence.** The
  `last-run/` artifacts (not carried in this slice — transient) show a
  complete end-to-end run whose assertion row read
  `Golden_vs_Current | 79.11 | Acc > than | 95 | False` — the game launched,
  built the scene, captured the screenshot, ran the comparison, and the eval
  failed the run with exit 1 because the render had drifted from the golden.
  That is precisely the detection job the eval exists to do. (Whether that
  particular divergence was a regression or a stale golden was not
  adjudicated at slicing time.)
- **Owner attestation:** the eval "has proven its value" in day-to-day agent
  work on the origin project, to the point that its absence on the second
  game is now felt as a gap.

Evidence is honest but single-project and single-machine: no CI integration
(the original TeamCity server is gone), no adoption by other developers yet.

## Why Generalize It

The verdict architecture is engine-agnostic and hard-won: golden mode vs eval
mode, versioned goldens reviewed by eye, a kill timeout, **absence of the
expected assertion row counts as failure** (silent early death cannot fake a
pass), hang detection, and artifacts copied to `last-run/` after every run.
Any game project — any engine, any language — benefits from a "boots, renders,
matches golden" smoke eval that an agent can run unattended. The origin
implementation only reaches one engine because scene setup and screenshot
capture use that engine's in-game harness; the explicit goal of promotion is
to **replace those engine-provided pieces with regular system tools**
(OS-level window capture, system input injection, a bundled image-diff tool)
so the eval runs against any game executable. Bundling or downloading helper
tools during promotion is acceptable to the owner.

## Contents Manifest

| Path | Role |
| --- | --- |
| `tools/autotest-eval/Run-AutoTestEval.ps1` | The runner: asset deploy, launch, timeout/kill, log parsing, verdict, artifact collection. The heart of the proposal. |
| `tools/autotest-eval/README.md` | Origin usage doc: modes, what a run does, file map. |
| `tools/autotest-eval/.gitignore` | Excludes the transient `last-run/` folder from version control. |
| `tools/autotest-eval/goldens/EVALGoldenShot.png` | The committed golden screenshot (256x256 render of the deterministic block grid) — a concrete example of the golden workflow. |
| `source/Block Games/Craft World/Source Content/Other/Scripts/Tests/EVALScene.script` | Shared deterministic scene: fixed sky, teleport, block grid, camera locked looking down. Engine-specific; becomes the per-game "reach deterministic state" adapter after generalization. |
| `source/Block Games/Craft World/Source Content/Other/Scripts/Tests/EVALGolden.script` | Golden-capture timeline: run scene, `test_prtscn`, write results, exit. |
| `source/Block Games/Craft World/Source Content/Other/Scripts/Tests/EVALSmoke.script` | Eval timeline: run scene, capture, `test_imagewithin` against the golden at threshold 95, exit. |
| `context/reports/2026-07-03-autotest-harness-revival.md` | Central knowledge document: harness architecture, script format, comparison math, state assessment, eval design rationale. Provenance and the curator's best map of what each piece does. |

## Dependencies and Requirements

To run the slice **as-is** (origin form): Windows with PowerShell 5+,
`robocopy`, and the origin game itself — a built `BlockWorld.exe`
(Debug|DESKTOP, MonoGame 3.7.1, VS 2017/2022) whose engine contains the
autotest command-line arguments and `Test_*` console commands. Note that two
small engine-side C# fixes from commit `1703e09` (`testingmode` argument,
recursive script lookup) live in the origin game's source and are **not**
carried in this slice; the slice cannot run against an unpatched engine.

The **generalized** form should need only: PowerShell (or an equivalent
cross-platform runner), plus bundled/downloadable system tools for screenshot
capture and image comparison (e.g. ImageMagick `compare`, or a small
self-contained capture+diff helper). No engine cooperation required.

## Integration Sketch

Promote as a workflow skill (e.g. `source/workflow-skills/game-runtime-eval/`)
that installs a `tools/autotest-eval/`-shaped folder into a target project:

1. **Keep verbatim (engine-agnostic already):** the runner's skeleton — golden
   vs eval modes, versioned `goldens/`, transient `last-run/`, launch with
   timeout and kill, missing-result-equals-failure verdict, exit code 0/1.
2. **Replace with system tools:** screenshot capture via OS-level window
   capture of the game window (instead of the engine's `test_prtscn` render
   target); image comparison via a bundled tool (instead of the engine's
   `test_imagewithin`) — the origin's metric was
   `accuracy = 1 - meanAbsPerPixelDiff/10`, thresholded at 95, which a
   generalized diff should reproduce or consciously replace.
3. **Make per-game (config, not code):** executable path and launch
   arguments, how to reach the deterministic scene (launch flags, a save
   file, a fixed seed, scripted input injection, or an engine harness where
   one exists), capture timing/delay, window title to capture, threshold, and
   timeout — a small config file the runner reads.
4. **Do NOT carry over:** the `.script` files, the `blockgametests\` /
   `Log Always` log-parsing specifics, the robocopy content sync, the
   `.cosm` test-map deploy, or anything else in the Generalization Notes.

A target project then adds: the runner + config + its own committed golden.

## Generalization Notes

Everything below is project- or engine-specific in the slice; this is the
curator's to-do list. Nothing was altered during slicing — the copy is
verbatim.

- **The entire in-game harness dependency.** `EVAL*.script` command timelines,
  `test_prtscn` / `test_imagewithin` / `test_write*` commands, the `autotest
  testingmode fixedtimestep script <name>` launch arguments, and the
  `blockgametests\` working folder all exist only inside the origin engine.
  The generalized eval must source scene setup, capture, and comparison from
  system tools instead (this is the owner's explicit request).
- **Result parsing is bespoke.** The runner snapshots and diffs the game's
  `Log Always*.txt` files under `Documents\My Games\BlockWorld\Logs` and
  greps box-drawing result rows (`║ ... True/False ║`). Generalized: the
  runner should own the comparison itself and not depend on any game log;
  hang detection via the engine watchdog (`GAME HAS HANGED`) should be
  replaced by the runner-side timeout plus optional window-responsiveness
  checks.
- **Content deployment is origin-shaped.** The robocopy sync of
  `Source Content\Other\Scripts\`, the `.cosm` test-map deploy, and the
  `Content\Other\Maps` existence-check quirk are all Block Game 2 build-system
  workarounds. Drop entirely.
- **Hardcoded origin names/paths inside slice files:** `BlockWorld.exe`, the
  `[STEAM] BlockWorld` build path, `C:\Logs\CraftWorld\...`, the 256x256
  capture size, threshold 95, and script names `EVALGolden`/`EVALSmoke`.
  All become config.
- **Scene determinism cannot be fully generalized.** The origin gets a
  pixel-stable scene from engine commands (fixed sky, teleport, block grid).
  An arbitrary game needs a per-game answer (deterministic launch flag, menu
  screenshot, fixed save/seed, or scripted input) — the skill should present
  this as the one required per-game adapter and offer patterns, including
  masking/regions and a lower threshold for scenes with unavoidable noise.
- **Windows-only runner.** PowerShell + `System.Diagnostics.Process`; fine if
  the rail stays Windows-first, otherwise consider a cross-platform rewrite
  at promotion time.
- **Engine-side fixes are not in the slice.** The `testingmode` argument and
  recursive script lookup are C# changes inside the origin game (commit
  `1703e09`); they are irrelevant once the harness dependency is removed but
  explain why the slice alone cannot drive an unpatched origin build.
