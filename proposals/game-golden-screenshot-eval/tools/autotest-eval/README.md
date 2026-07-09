# AutoTest Eval

Runtime smoke eval for Block Game 2, built on the game's legacy in-game autotest harness.
Full background, code-path map, and state assessment: [context/reports/2026-07-03-autotest-harness-revival.md](../../context/reports/2026-07-03-autotest-harness-revival.md).

## Usage

```powershell
# Prereq: build Craft World.sln, [STEAM] BlockWorld, Debug|DESKTOP (see getting-started.md)

# One-time (or after intentional visual changes): capture the golden screenshot
powershell -File tools\autotest-eval\Run-AutoTestEval.ps1 -Mode Golden
# → review goldens\EVALGoldenShot.png by eye (block grid viewed from above), commit it

# Regular eval run — exit code 0 = pass, 1 = fail
powershell -File tools\autotest-eval\Run-AutoTestEval.ps1
```

## What a run does

1. Syncs `Source Content\Other\Scripts\` from the source tree to the build output (the build does not copy raw content).
2. Deploys `goldens\EVALGoldenShot.png` into `blockgametests\` next to the exe.
3. Launches `BlockWorld.exe autotest testingmode fixedtimestep script EVALSmoke` — boots past the main menu into a testing world, builds a deterministic scene (fixed sky, teleport, block grid), captures a 256×256 scene render, and asserts ≥95% similarity to the golden via `Test_ImageWithin`.
4. Kills the game if it exceeds the timeout; parses this run's delta of `C:\Logs\CraftWorld\Auto Tests <date>\Test Results.log`.
5. Fails on: assertion `False`, assertion row missing (silent early death), `GAME HAS HANGED` (in-game watchdog), or process timeout.
6. Copies screenshots and the results delta to `last-run\` for inspection.

## Files

| Path | Purpose |
| --- | --- |
| `Run-AutoTestEval.ps1` | The runner (only entry point agents need). |
| `goldens/` | Versioned golden screenshots. |
| `last-run/` | Artifacts from the most recent run (not versioned). |
| `../../source/Block Games/Craft World/Source Content/Other/Scripts/Tests/EVALScene.script` | Shared deterministic scene. |
| `.../Tests/EVALGolden.script` | Golden-capture timeline. |
| `.../Tests/EVALSmoke.script` | Eval timeline + screenshot assertion. |
