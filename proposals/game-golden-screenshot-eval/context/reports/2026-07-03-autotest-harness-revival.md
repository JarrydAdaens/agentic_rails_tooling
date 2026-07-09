---
name: autotest-harness-revival
description: Central knowledge document for the legacy in-game autotest / input-replay / screenshot-comparison smoke-test harness — how it works, its current state, how to use it, and what is needed to revive it locally.
metadata:
  version: "1.0"
  agentic_rails_source_version: "0.3"
  owner: "2.0 Studios"
  repo: "block-game-2"
  report_date: "2026-07-03"
---

# Block Game 2 — AutoTest Harness Revival

This is the central knowledge document for the game's built-in automated smoke-test harness — the system that once let TeamCity launch the game with command-line arguments, skip the main menu, load a testing world, drive the game with timed script commands, capture screenshots, compare them against a golden set, and write a pass/fail results file. The TeamCity server is gone (cold-storage restore is a separate effort); this document covers **everything needed to use the harness locally** and serves as the foundation for the agent eval built on top of it.

**Audience:** developers and AI agents working on this game who need runtime verification beyond "it compiles."

---

## 1. Architecture Overview

The harness has five cooperating layers, all still present in the codebase:

```text
BlockWorld.exe <args>
  │
  ├─ 1. Argument parsing ──────── [STEAM] BlockWorld/Source/Program_Internal.cs (Main)
  │       autotest, script, command, fixedtimestep, testingmode*, playback/record, ...
  │       → static flags in Craft World/Source/ProgramSettings.cs (class Program_Internal)
  │
  ├─ 2. Boot-to-gameplay ──────── StartModeGame.LoadToGameplayTesting
  │       BootupScreen.ExitScreen() skips the main menu, creates a local session,
  │       loads content-map header 0, and loads straight into gameplay.
  │
  ├─ 3. Script engine ─────────── DebugCommandConsole + Scripting Commands.cs
  │       .script files = timed console-command timelines
  │       (leading number = delay in seconds; variables; for-loops; nesting)
  │
  ├─ 4. Test commands ─────────── Command System/AutoTest Commands.cs
  │       Test_PrtScn (screenshot), Test_ImageWithin (golden compare),
  │       Test_PlayerWithin, Test_FloatGreater/Smaller, pool-count checks, ...
  │
  └─ 5. Results + watchdogs ───── Log.WriteAutoTest → MicroTimerRename.WriteOutAllTimes
          C:\Logs\CraftWorld\Auto Tests <date>\Test Results.log (+ perf CSV, crash logs)
          Hang watchdog exits the process; crash screen auto-exits in autotest mode.
```

### 1.1 Key files

| Concern | File |
| --- | --- |
| CLI argument parsing (`Main`) | `source/Block Games/[STEAM] BlockWorld/Source/Program_Internal.cs` |
| Static run-mode flags | `source/Block Games/Craft World/Source/ProgramSettings.cs` (`Program_Internal` class) |
| Boot mode enum | `source/Block Games/Craft World/Source/Game/StartModeGame.cs` |
| Boot mode selection | `source/Block Games/Craft World/Source/Game/BlockGameBase - Inners.cs` (`GameStartMode`, `TestingMode` define) |
| Skip-menu boot path | `source/Block Games/Craft World/Source/Screens/Splash/BootupScreen.cs` (`ExitScreen`, `LoadToGameplayTesting` case) |
| Script runner | `source/Block Games/Craft World/Source/Command System/Scripting Commands.cs` (`RunScript`) |
| Console + timers + variables | `source/Hazzah Engine/Engine Source/Debug Tools/Console/DebugCommandConsole.cs` (`ExecuteCommand`) |
| Test/assertion commands | `source/Block Games/Craft World/Source/Command System/AutoTest Commands.cs` |
| Command registrations | `source/Block Games/Craft World/Source/Command System/BlockGameCommandsManager.cs` (~lines 405–436 for `Test_*`) |
| Image diff | `source/Hazzah Engine/Engine Source/Misc Helpers/ImageHelper.cs` (`CompareImages`) |
| Screenshot writer | `source/Hazzah Engine/Engine Source/Screen Capture.cs` (`ScreenCaptureManager.SaveTextureToFileRaw`) |
| Results file writer | `source/Hazzah Engine/Engine Source/Profiling/MicroTimer.cs` (`WriteOutAllTimes`) |
| Test-result accumulator | `source/Hazzah Engine/Engine Source/Profiling/Log.cs` (`WriteAutoTest`, `AutoTestResults`) |
| Hang watchdog | `source/Block Games/Craft World/Source/World/World Async Stuff.cs` (`AutotestCode`) |
| Crash auto-exit | `source/Block Games/Craft World/Source/Game/BlockGameBase - Crash.cs` (`UpdateCrashGame`) |
| Input replay data | `source/Hazzah Engine/Engine Source/Controller/RecordableData.cs` |
| Historical test scripts | `source/Block Games/Craft World/Source Content/Other/Scripts/Tests/*.script` |

### 1.2 Command-line arguments (parsed in `Main`)

| Argument | Effect |
| --- | --- |
| `autotest` | Sets `Program_Internal.IsInAutoTestMode`. Skips splash delays, enables the hang watchdog, auto-exits the crash screen, and tags the results folder `Auto Tests`. |
| `script <name>` | Queues console command `script <name>`, executed when the gameplay screen finishes loading. |
| `command <text>` | Queues an arbitrary console command the same way. |
| `testingmode` | **Added 2026-07-03** — boots straight into gameplay (`StartModeGame.LoadToGameplayTesting`), skipping the main menu. This is the runtime replacement for the old `TestingMode` compile define. |
| `fixedtimestep` | Forces fixed-timestep updates (determinism aid). |
| `console` | Enables the in-game console. |
| `fullscreen` | Forces fullscreen. |
| `playback` / `record` / `normal` | Input-replay modes (**bit-rotted**, see §3.4). |
| `nameofrecording <name>` | Replay file name (used with the above). |
| `playspeed <float>` / `synctime <int>` | Replay tuning. |
| `physgridsize <float>` | Physics test mode. |
| `+connect_lobby <id>` | Steam invite cold-start (unrelated to testing). |

Queued commands run at `GameplayScreen` load, right after `script Startup` and `script Startup<GameType>` (`GameplayScreen.cs` ~line 440).

### 1.3 The script format

Scripts live in `Source Content\Other\Scripts\` **relative to the executable** (`StreamHelper.GetApplicationRoot()`); tests sit in the `Tests\` subfolder. One console command per line:

- `// comment` — ignored.
- A **leading number is a delay in seconds** (game time): `8 test_prtscn shot 256 256` executes at t≈8s via `CommandTimers`.
- `number <Name> <value>` — declares/edits a script variable; any later argument matching `<Name>` is substituted.
- `for ITR 20 to 30` + next line using `ITR` — schedules the next command once per value (value doubles as the delay).
- `script <OtherScript>` — nests another script (all its timers schedule relative to now).
- `_SCRIPTNAME_` → replaced with the script's own name; `PARAM1..n` → replaced with arguments passed to `script <name> <p1> <p2> ...`.
- Command lookup is case-insensitive but **exact** — unknown commands echo "Unknown Command" and are silently skipped (no test failure!).

### 1.4 The test command vocabulary (all registered and live)

| Command | Args | What it does |
| --- | --- | --- |
| `Test_PrtScn` | `name [x y]` | Renders the 3D scene (no HUD) to an `x`×`y` target (default 640×360) and saves `blockgametests\<name>.png` (CWD-relative). |
| `Test_ImageWithin` | `fileA fileB threshold testname` | Loads both PNGs from `blockgametests\`, computes similarity (see below), passes if `accuracy% > threshold`. |
| `Test_PlayerWithin` | `dist x y z testname` | Passes if the player is within `dist` of the point. |
| `Test_FloatGreater` / `Test_FloatSmaller` (+`%` variants) | `fileA fileB line threshold testname` | Compares numbers previously logged to files (FPS, positions). |
| `Test_HotCountBelow` / `Test_PoolCountBelow` | `count testname` | Region-pool memory assertions. |
| `Test_LogAverageFps` / `Test_LogPlayerPosition` | `name` | Logs values into `blockgametests\` for later comparison. |
| `Test_WriteHeading/Start/Mid/End/Note/EmptyLines/TimeStamp` | — | Formats the results box in the results log. |
| `Test_StartReplay` | `[name] [speed]` | Starts input replay (**bit-rotted**, §3.4). |
| `Exit` | — | Exits the game (flushes results via `UnloadContent`). |

Scene-driving commands used by tests (all live): `Play_Teleport x y z`, `Cam_Rotate yaw pitch`, `Cam_Fov f`, `SetSky <Dawn|Morning|Midday|...|theta>`, `BlockGrid` (places a deterministic 16×16 grid of one-of-every-block 10 above the player), `ToggleDebug_Lines`, `SetGraphicsQualityPreset`, `Play_Walk`, and the full debug-command set.

### 1.5 Screenshot comparison math

`ImageHelper.CompareImages` computes the mean absolute per-pixel difference summed over RGBA (0–1020 per pixel), then:

```
accuracy = 1 − (meanAbsDiff / 10)
```

`Test_ImageWithin` multiplies by 100 and compares against the threshold argument. In practice: identical images score 100; a mean per-pixel drift of 0.5 units scores 95. Historical scripts used thresholds of 85–99. Both images must be the same size (same `Test_PrtScn` dimensions), or the comparison throws (caught by the console, test silently skipped — see §3.6).

### 1.6 Results and watchdogs

- Every `Test_*` assertion appends a formatted pass/fail row via `Log.WriteAutoTest(...)` into the in-memory `Log.AutoTestResults`.
- On exit (`BlockGameBase.UnloadContent` → `MicroTimerRename.WriteOutAllTimes`), results are appended to:
  `C:\Logs\CraftWorld\Auto Tests <long date>\Test Results.log` (result rows end in `True` / `False`), alongside a perf-timing CSV per run.
- **Hang watchdog** (`World Async Stuff.AutotestCode`, autotest mode only): if the draw-frame counter stalls, it writes `GAME HAS HANGED` into the results and calls `Exit()`.
- **Crash handling**: in autotest mode the crash screen immediately exits the game; crash text is written to a `CrashLogs` subfolder.
- **The process exit code is always 0.** TeamCity parsed the results log; any local runner must do the same (the eval runner in §4 does).

### 1.7 Input record/replay (the second, deeper system)

Independent of scripts, the engine can record raw keyboard/mouse states plus player pos/vel per frame (`RecordableData`, wired through `BlockGameBase.cs:283 → HazzahGame.StartupGraphics → g_Controller`) and replay them (`playback` arg or `Test_StartReplay`). Recordings are Deflate-compressed XML `.replay` files. **This path is bit-rotted** (§3.4). The script-command timeline is what actually powered the CI smoke tests and is the viable revival path.

---

## 2. How To Use It (current, working procedure)

Prereqs: the game builds per [getting-started.md](../../getting-started.md) (VS 2017/2022, MonoGame 3.7.1 SDK, `Craft World.sln`, `[STEAM] BlockWorld`, Debug|DESKTOP). Steam client should be installed/running (Steam shell build; `steam_appid.txt` sits next to the exe).

### 2.1 One-command eval (recommended)

```powershell
# From the repo root — full smoke eval (build output must exist):
powershell -File tools\autotest-eval\Run-AutoTestEval.ps1

# First time / after intentional visual changes — record a fresh golden:
powershell -File tools\autotest-eval\Run-AutoTestEval.ps1 -Mode Golden
```

The runner deploys scripts + goldens, launches the game headlessly-ish, waits (with a kill timeout), parses the results log, copies artifacts to `tools\autotest-eval\last-run\`, and returns **exit code 0 = pass, 1 = fail**. See §4.

### 2.2 Manual invocation

```powershell
cd "source\Block Games\[STEAM] BlockWorld\bin\DESKTOP\Debug"
.\BlockWorld.exe autotest testingmode fixedtimestep script EVALSmoke
```

- `testingmode` boots past the menu into a Creative-Editor world (content-map header 0).
- `script EVALSmoke` queues the test script once gameplay loads.
- Screenshots and logged values land in `blockgametests\` next to the exe.
- Results append to `C:\Logs\CraftWorld\Auto Tests <date>\Test Results.log`.
- The script's final `exit` command closes the game and flushes results.

### 2.3 Writing a new test script

1. Create `source/Block Games/Craft World/Source Content/Other/Scripts/Tests/<Name>.script` (the eval runner syncs it to the build output; a plain build does **not** copy it — see §3.5).
2. Set up a deterministic scene early (fix the sky with `setsky midday`, teleport with `play_teleport`, place geometry with `blockgrid`), assert late, and always end with `N exit`.
3. Use only registered command names (check `BlockGameCommandsManager.cs`); a typo'd command is *silently skipped*.
4. Run once with `-Mode Golden` to capture goldens, review the PNG by eye, then run in eval mode.

---

## 3. State Assessment — what was broken and what was done (2026-07-03)

| # | Finding | Severity | Status |
| --- | --- | --- | --- |
| 3.1 | **No runtime path into `LoadToGameplayTesting`.** The boot mode was selectable only via the `TestingMode` compile define, disabled in every csproj (`TestingModek`). Worse, enabling the define turns `GameStartMode` into a get-only property, which breaks compilation of the `+connect_lobby` assignment in `Program_Internal.cs`. | Blocker | **Fixed** — added the `testingmode` command-line argument (runtime, no define needed). |
| 3.2 | **`script <name>` could not find test scripts.** `RunScript` enumerated only the top level of `Scripts\`; every historical test lives in `Scripts\Tests\`. | Blocker | **Fixed** — `RunScript` now uses the existing recursive `GetFilePaths` helper (same depth-3 recursion as `ListScripts`). |
| 3.3 | **Stale command names in historical scripts.** `deb_exit`, `deb_blockgrid`, `cam_aspectratio`, `prtscnnow`, `comparescreen`, `teleportplayer`, `isplayerwithin`, and `script DefaultTestSetup` (file no longer exists) don't match any registered command — they echo "Unknown Command" and are skipped, so e.g. `TESTSaveLoadBlocks` would never exit. | High | **Documented; historical scripts left untouched.** New `EVAL*` scripts use only live commands. Renames if you want to revive an old script: `deb_exit`→`exit`, `deb_blockgrid`→`blockgrid`, `prtscnnow`→`test_prtscn`, `comparescreen`→`test_imagewithin`, `teleportplayer`→`play_teleport`, `isplayerwithin`→`test_playerwithin`. |
| 3.4 | **Input record/replay is dead on desktop.** `RecordableData.LoadFromXML` ignores its name argument and hardcodes `Replays/Recording 123.replay`; `SaveToXML` is compiled only under the retired `XNA4` define, so recording is a no-op; no `Replays\` folder exists. (Also: the `MS` mouse struct's `rb/mb/xb1/xb2` getters all test the `lb` flag — pre-existing bugs.) | Medium | **Not revived** (out of scope). The scripted-command path covers the smoke-test use case. Revival checklist: fix the path in `LoadFromXML`, compile `SaveToXML` for `DESKTOP`, fix the `MS` flag getters, create `Replays\`. |
| 3.5 | **Raw content is not copied by the build.** `Source Content\` (scripts, settings, maps) next to the exe was historically copied by CI/hand — no csproj copies it. A stale copy exists in the current build output. | Medium | **Handled by the eval runner** (robocopy sync of `Scripts\` before each run). |
| 3.6 | **Silent failure modes.** Unknown commands and exceptions inside commands (e.g. missing golden PNG) echo to the in-game console but produce **no test result and no nonzero exit code**. A script that dies early looks like a pass if you only count `False` rows. | Medium | **Handled by the eval runner**: it requires the expected named test rows to be present *and* `True` — absence is failure. |
| 3.7 | **Golden images lived on a dead share** (`\\WATER\Backup\CraftworldImages`). | Medium | **Replaced** — goldens are now versioned in `tools\autotest-eval\goldens\` and deployed to `blockgametests\` per run. |
| 3.8 | **No content maps ship in the BLOCKWORLD flavor.** `LoadToGameplayTesting` loads content-map header 0; only AMP / Survival Games have `.cosm` maps in `Source Content\<title>\Other\Maps\`. Depending on the map-cache content build, header 0 may be null → NRE at boot. | Runtime risk | **Verify at runtime.** Mitigation if it NREs: have the runner deploy a `.cosm` into `Source Content\Other\Maps\` next to the exe (the content map set reads that folder), or run a Survival Games flavor build. |
| 3.9 | Results path is hardcoded to `C:\Logs\CraftWorld\...`. | Low | Accepted; runner reads from there. |
| 3.10 | TeamCity itself. | — | Out of scope per the owner; server restore from cold storage is a separate effort. Everything here is local-only. |

---

## 4. The Agent Eval

**Purpose:** give agents working on this game a cheap, end-to-end runtime check — "the game still boots to gameplay, renders the world correctly, and the world/screenshot pipeline works" — without a human watching.

### 4.1 Design

- **Runner:** `tools/autotest-eval/Run-AutoTestEval.ps1` — the only entry point an agent needs.
- **Scene script:** `EVALScene.script` — shared deterministic scene: fixed sky (`setsky midday`), teleport to a fixed point, `blockgrid`, camera locked FOV/pitch looking down at the grid.
- **Golden mode:** `EVALGolden.script` — runs the scene, captures `EVALSmoke_golden` (256×256), exits. The runner moves it into `tools/autotest-eval/goldens/`.
- **Eval mode:** `EVALSmoke.script` — runs the same scene, captures `EVALSmoke_current`, asserts `test_imagewithin EVALSmoke_golden EVALSmoke_current PassThreshold Golden_vs_Current`, exits.
- **Verdict:** the runner tails the delta of `Test Results.log`, requires the named assertion rows to exist and read `True`, fails on `False` / `GAME HAS HANGED` / missing rows / process timeout (kill). Exit code 0/1; artifacts (both PNGs + log excerpt) copied to `tools/autotest-eval/last-run/` for inspection.
- **Threshold:** default 95 (tunable in the script via `number PassThreshold 95`). The 3D-scene render target excludes HUD/UI, making it resolution- and window-independent.

### 4.2 How agents should use it

1. After any change that could affect runtime behavior: build Debug|DESKTOP, then run the eval. Treat exit 1 as a regression signal and read `last-run\`.
2. After an *intentional* visual change: re-record goldens (`-Mode Golden`), eyeball the PNG, commit the new golden alongside the change.
3. When adding a feature with visual/world impact, consider adding a dedicated `EVAL<Feature>.script` + golden and extending the runner's expected-tests list.

### 4.3 Verified status

See the Validation section of the work session that created this document (and `tools/autotest-eval/README.md`) for what was executed and what remains unverified on this machine.

---

## Revision History

| Version | Date | Notes |
| --- | --- | --- |
| 1.0 | 2026-07-03 | Initial revival document: full code-path trace, state assessment, fixes (testingmode arg, recursive script lookup), eval design. |
