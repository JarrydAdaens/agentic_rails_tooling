---
name: game-golden-screenshot-verifier
description: >-
  Engine-independent runtime smoke verifier for games. Launches a game, drives it
  into a deterministic state, captures a screenshot from the outside, and
  compares it against a versioned golden — exit 0 pass / 1 fail. Drop it into
  any game project, fill in one config file, and replace the stub input driver
  with your game's route to a repeatable scene.
metadata:
  version: "1.1"
---

# Game Golden-Screenshot Verifier

A one-command runtime verifier an agent can run unattended to answer "does the game
still boot and render correctly?" It launches the game, puts it into a
deterministic state, captures the screen, and asserts the render still matches a
human-approved golden image. Exit code `0` = pass, `1` = fail.

This is the generalized form of the Block Game 2 autotest eval. The origin used
the game engine's own in-engine harness for scene setup, screenshot capture, and
image comparison. Here those three engine-provided pieces are replaced by regular
system tools — an input driver, an OS-level screen grab, and a local image diff —
so the verifier runs against **any** game executable with no engine cooperation.

## What is preserved from the origin (the hard-won part)

- **Golden mode vs eval mode**, with goldens versioned in `goldens/` and reviewed by eye.
- **A launch timeout** that kills a hung game.
- **"Couldn't capture" always counts as failure** — if the game crashes or exits before the screenshot is taken, that is a hard fail, never a silent pass.
- **Every run's artifacts land in `last-run/`** (git-ignored) for inspection.

## Layout

| Path | Role |
| --- | --- |
| `run_eval.py` | The runner — the only entry point. Launch, drive, capture, compare, verdict, exit 0/1. |
| `eval_config.example.json` | Copy to `eval_config.json` and fill in for your game. |
| `drivers/input_stub.py` | **Stub** deterministic-state driver. Replace its body for your game. |
| `lib/compare.py` | Similarity metric (reproduces the origin's `accuracy = 1 − meanAbsDiff/10`). |
| `lib/capture.py` | Screen capture (window / region / fullscreen). |
| `lib/config.py` | Config loading and validation. |
| `goldens/` | Versioned golden screenshots (committed). |
| `last-run/` | Artifacts from the most recent run (git-ignored). |
| `tests/test_compare.py` | Focused tests for the similarity metric. |

## Requirements

Python 3.10+ and [`uv`](https://docs.astral.sh/uv/). Dependencies (Pillow, NumPy,
mss, PyGetWindow, PyAutoGUI) are declared inline in `run_eval.py` and installed
automatically on first `uv run` — nothing to install by hand. Without uv:
`pip install pillow numpy mss pygetwindow pyautogui`. Screen capture and input
injection are OS-level, so the verifier runs on a real desktop session (Windows-first,
matching the origin; the capture and input libraries also support macOS/Linux).

## Usage

```bash
# 0. Verify the install and metric (no game needed)
uv run run_eval.py --self-test

# 1. Capture a golden (after the first setup, or an intentional visual change)
uv run run_eval.py --config eval_config.json --mode golden
#    → review goldens/golden.png by eye, then commit it

# 2. Run the verifier — exit 0 = pass, 1 = fail
uv run run_eval.py --config eval_config.json
```

## Adapting it to your game (the one required step)

The runner is engine-agnostic; two things are yours to provide.

1. **Fill in `eval_config.json`** — the executable path, launch arguments, the
   window title to capture, capture size, threshold, timeout, and warmup/settle
   delays. See `eval_config.example.json`.

2. **Replace `drivers/input_stub.py`** — this is the deterministic-state adapter,
   the piece that cannot be fully generalized because "put the game in the same
   visual state every time" is game-specific. The stub just moves the mouse in a
   square and presses Shift a few times; it does **not** produce a meaningful
   scene. Swap its `drive()` body for your game's real route to a repeatable
   state. Good options, most robust first:
   - launch straight into a fixed scene via a launch flag, saved game, or fixed
     seed (put it in `launch_args`, and the driver can do nothing);
   - script a deterministic menu/input path (as the stub sketches);
   - capture a static screen (menu/splash) where no input is needed.

For scenes with unavoidable noise (animation, particles), lower the `threshold`
or capture a region that excludes the noisy area.

## The similarity metric

`lib/compare.py` reproduces the origin engine's comparison so thresholds carry
over: the mean absolute per-pixel RGBA difference (0–1020 per pixel) maps to
`accuracy = 1 − meanAbsDiff/10`, scored out of 100. Identical images score 100; a
mean per-pixel drift of 0.5 units scores 95 (the default threshold). It is a
sensitive metric — tune the threshold to your scene. Both images must share
dimensions (the runner resizes the capture to `capture.size`), or the comparison
fails loudly rather than scoring a mismatch.

## Provenance

Generalized from the `game-golden-screenshot-eval` proposal (origin project
Block Game 2 / Craft World). The proposal's revival report is the deep background
on how the original in-engine harness worked and why each piece was replaced.
