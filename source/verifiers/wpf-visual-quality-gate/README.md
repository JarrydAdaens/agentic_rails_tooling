---
name: wpf-visual-quality-gate
description: >-
  Evaluator-run visual quality gate for WPF desktop apps. For any change that
  affects visible UI, an independent evaluator sub-agent launches the app,
  screenshots the initial state, performs the target interaction through real
  input, screenshots the result, and reports pass/fail against explicit
  criteria — so agents cannot declare visible UI work done on build and unit
  tests alone. Drop the gate document into a target project, fill in three
  project defaults, and wire the trigger lines into the project's AGENTS.md.
metadata:
  version: "1.0"
---

# WPF Visual Quality Gate

An agent-run verifier for WPF projects that closes the gap between "it
compiles and the tests pass" and "the change is actually visible and works in
the running app." Build and test success can miss clipping, overlap, invisible
controls, misleading status, and interactions that only fail on the live
desktop. This gate gives visible UI work a concrete stop condition: launch the
app through a declared visual path, capture the initial state, perform the
target interaction through real input, capture the target state, and compare
against explicit pass criteria — with an independent evaluator, not the
implementing agent, delivering the verdict.

Unlike `game-golden-screenshot-verifier`, the runner here is not a script — it is
an evaluator sub-agent following a fixed procedure and report format. The gate
is designed for Claude Code first (its preferred runners, the
`quality-gate-persona` and `wpf-persona` sub-agents, deploy from this repo),
with fallbacks for other agentic IDEs and for a human evaluator.

## Layout

| Path | Role |
| --- | --- |
| `wpf-visual-quality-gate.md` | The gate itself — the file a target project copies in and customizes. |
| `packet-example.md` | A filled example of the evaluator packet the implementing agent must hand over. |

## Adopting it in a target project

1. **Copy `wpf-visual-quality-gate.md`** into the target project's
   `context/evaluations/` folder.
2. **Fill in the Project Defaults table** in the copy — visual launch command,
   window title, and cleanup command. This is the per-project seam; the rest of
   the document stays as shipped.
3. **Wire the trigger into the project's `AGENTS.md`** (or `CLAUDE.md`) so the
   gate is mandatory rather than advisory:

   > - Review matching evaluation gates in `context/evaluations/` when the task
   >   touches an area covered by an evaluation.
   > - Run matching `context/evaluations/` gates when task scope triggers them,
   >   using an independent evaluator sub-agent when available.

   With those lines in place, any visible WPF UI change must run this gate or
   document why it could not.
4. Per UI story, the implementing agent writes an evaluator packet (see
   `packet-example.md`) and dispatches the evaluator.

## Requirements

- Windows desktop session able to launch and display the target WPF app.
- Screenshot capture in the active agentic IDE or evaluator environment.
- Real UI input capability — IDE-driven input, UI Automation, or manual
  evaluator steps.
- `quality-gate-persona` (preferred) or `wpf-persona` available as sub-agents;
  both ship from this repo's `source/agents/`. The gate degrades to a human
  checklist when neither is available.
- The `wpf-tree-sensor` skill (this repo's `source/skills/`) is a useful
  companion for UI Automation tree evidence, but is not required.

## Provenance

Generalized from the Quota-Tank project's local gate (promoted from the
`wpf-visual-quality-gate` proposal, 2026-07-09). In its origin run, every
visible-UI story in the Milestone 3 batch — tooltip callouts, provider tab
bar, pinned-window transparency, card-button relocation — carried screenshot
and live-drive evidence produced under this gate before commit. The origin's
launch command, window title, and cleanup command were project defaults, not
universal ones; they survive only as illustrations in `packet-example.md`.
