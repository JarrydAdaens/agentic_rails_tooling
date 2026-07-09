---
name: wpf-visual-quality-gate
description: >-
  Proposal to promote Quota-Tank's screenshot-based WPF visual quality gate into
  reusable Agentic Rails tooling for visible desktop UI changes.
metadata:
  version: "0.1"
  status: proposed
  origin_project: quota_tank
  origin_path: quota_tank
  proposed_on: 2026-07-09
  suggested_destination: source/evals/wpf-visual-quality-gate
---

# Proposal: WPF Visual Quality Gate

## What This Is

This proposal captures Quota-Tank's project-local WPF visual quality gate: a reusable evaluation document that requires visible WPF UI changes to be verified by launching the app, taking screenshots, driving real UI interactions, and checking for visible layout failures before an agent calls the work done. It is deliberately evaluator-oriented: the implementing agent provides a packet, an independent evaluator inspects the running UI, and the evaluator reports pass/fail without editing files.

The slice does not include the WPF tree sensor, because that capability has already been generalized into global skills. This proposal is specifically the screenshot and real-interaction visual quality gate.

## Use Case

Quota-Tank is a WPF tray application where many changes are visually meaningful but not fully covered by unit tests: tooltip layout, provider-card pagination, pinned-window transparency, button placement, and tab navigation. Build and test success can still miss clipping, overlap, invisible controls, misleading status, or interactions that only fail in the running desktop app.

This gate gives WPF projects a concrete stop condition for UI work: run the app through a declared visual launch path, capture the initial state, perform the target interaction through real input, capture the target state, and compare the result against explicit pass criteria.

## Evidence It Works

Evidence from Quota-Tank is strong enough to justify proposal, though the original screenshots themselves are not copied because they are transient run evidence.

- `context/evaluations/wpf-visual-quality-gate.md` defines the operational gate: use it for WPF changes affecting visible UI, navigation, state presentation, layout, or interaction; then build, test, launch, screenshot, interact, screenshot again, inspect, and clean up.
- `context/rails-boss-execute/briefing.md` records the 2026-07-05 follow-up run as using hard constraints of data-source proof, no estimation, build, full tests, and live probe/UIA app-drive evidence before commit.
- `context/rails-boss-execute/progress.md` records that every Story 32-43 item in that run had build clean, full test suite green, and live probe and/or UIA app-drive evidence before commit.
- `context/implementation-plans/milestone-3/story-39-pinned-window-transparency/plan.md` records a live drive where a pinned provider window was made translucent through UIA RangeValue input and screenshot evidence showed desktop content bleeding through while readability remained intact.
- `context/implementation-plans/milestone-3/story-41-tooltip-callouts/plan.md` records screenshot validation for both a short tooltip and the longest settings tooltip, confirming width capping, wrapping, and pointer placement.
- `context/implementation-plans/milestone-3/story-42-relocate-card-buttons/plan.md` records screenshot confirmation of bottom-right button placement and UIA exercise of unchanged Settings behavior.
- `context/implementation-plans/milestone-3/story-43-provider-tab-bar/plan.md` records a live UIA tab click plus screenshot evidence showing all enabled provider icons and active-tab indication.

## Why Generalize It

This belongs in shared Agentic Rails tooling because WPF and desktop UI projects commonly suffer from a false sense of completion when agents stop at compilation and unit tests. The pattern is not Quota-Tank-specific: any visible desktop UI change benefits from a reusable gate that forces agents to look at the running UI, exercise the interaction path, and report screenshot-backed evidence.

It also fits the existing tooling repo shape: `source/evals/` is for reusable evaluations, and the gate already depends on shared evaluator personas that exist in tooling (`quality-gate-persona` and `wpf-persona`).

## Contents Manifest

| Path | Role |
| --- | --- |
| `AGENTS.md` | Excerpt of the origin instructions that make matching evaluation gates mandatory when task scope triggers them. |
| `context/evaluations/wpf-visual-quality-gate.md` | The proposed evaluation gate copied verbatim from Quota-Tank. |
| `context/rails-boss-execute/briefing.md` | Provenance showing the hard constraint to use live probe/UIA app-drive evidence in the relevant run. |
| `context/rails-boss-execute/progress.md` | Provenance summary showing stories completed with build, tests, and live-drive evidence. |
| `context/implementation-plans/milestone-3/story-39-pinned-window-transparency/plan.md` | Evidence plan/log for screenshot-backed pinned-window transparency validation. |
| `context/implementation-plans/milestone-3/story-41-tooltip-callouts/plan.md` | Evidence plan/log for screenshot-backed tooltip visual validation. |
| `context/implementation-plans/milestone-3/story-42-relocate-card-buttons/plan.md` | Evidence plan/log for screenshot-backed layout and UIA command validation. |
| `context/implementation-plans/milestone-3/story-43-provider-tab-bar/plan.md` | Evidence plan/log for screenshot-backed tab navigation validation. |

## Dependencies and Requirements

- Windows desktop environment capable of launching the target WPF app.
- A project-specific visual launch command, window title, interaction path, pass criteria, and cleanup command.
- Build and test commands appropriate to the target project.
- Screenshot capture ability in the active agentic IDE or evaluator environment.
- Real UI input capability, either through the IDE, UI Automation, manual evaluator steps, or another approved desktop-driving path.
- `quality-gate-persona` preferred for independent evaluation; `wpf-persona` preferred when deeper WPF/XAML judgment is needed. Both personas already exist in Agentic Rails tooling.

## Integration Sketch

Promote the gate into `source/evals/wpf-visual-quality-gate/README.md` or an equivalent eval package under `source/evals/`. During promotion, give it a small project adapter seam for launch command, window title, cleanup command, and expected interaction packet. Target projects should be able to copy or reference the eval and then define their own packet per UI story.

Do not carry over Quota-Tank-specific launch defaults as universal defaults. Do not promote the evidence implementation plans into the deployed eval; they are proposal proof only. Do not fold the WPF tree sensor into this proposal, because it has already been generalized separately.

## Generalization Notes

- The gate currently names Quota-Tank defaults: `source\QuotaTank.WPF\bin\Debug\net8.0-windows\QuotaTank.WPF.exe --show-popup`, window title `Quota-Tank`, and a Quota-Tank cleanup command. Promotion should turn these into configurable project packet fields or examples.
- The gate assumes independent evaluator sub-agents may be available, but provides a human-evaluator fallback. Promotion should keep both paths.
- The copied evidence files contain Quota-Tank-specific story names, provider concepts, and commit/run notes. They are proof, not reusable runtime material.
- The proposal intentionally excludes screenshots and transient runtime outputs.
- The proposal intentionally excludes the WPF tree sensor because the user confirmed it now lives outside this repo in global skills.
