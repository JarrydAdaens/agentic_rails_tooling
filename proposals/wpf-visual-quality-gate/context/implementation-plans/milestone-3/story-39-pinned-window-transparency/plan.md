---
name: story-39-pinned-window-transparency
description: Tier 4 implementation plan for Milestone 3 Story 39 — settings slider controlling pinned-window opacity with a hard visibility floor.
metadata:
  version: "1.0"
  owner: "Jarryd Adaens"
  repo: "quota_tank"
---

# Story 39: Pinned-Window Transparency Slider

## Metadata

- Task Type: `GOAL`
- Task Name: Pinned-window transparency slider
- Status: Complete
- Owner: Jarryd Adaens
- Last Updated: 2026-07-05

## Linked Context

- Design: [design.md](../../../design.md)
- Milestone: [milestone-3.md — Story 39](../../../milestones/milestone-3.md#story-39)
- Coupled with: [Story 40](../story-40-click-through-mode/plan.md) (the user's "transparency mode" combines both).
- Applicable Evaluations: rails-eval-jobs-done; WPF Visual Quality Gate (pinned-window drive shared with Story 40).

## Estimates (CER)

- Complexity: 4 / Effort: 4 / Risk: 3

## Objective

A settings slider controls pinned-window opacity, applied live to open pinned windows and to new ones, persisted in `AppSettings` and clamped in `Normalize()` so a window can never drop below 10% opacity (the story's "never under 10%" assumption read as an opacity floor).

## Scope

- In scope: `PinnedWindowOpacityPercent` (default 100, clamp 10–100) on `AppSettings` incl. equality/hash; `ConfigurationViewModel` + settings slider (Pinned windows section); `App` applies opacity on pin creation and on settings save.
- Out of scope: per-provider opacity; popup transparency (the popup is a transient glance surface — the story's value is on the persistent overlays; noted as the "where appropriate" decision).

## Implementation Steps

1. Settings model + Normalize clamp + equality members.
2. VM property, load/save wiring; slider UI with live value label.
3. `App.ShowPinnedWindow` sets `window.Opacity`; `OnConfigurationSettingsSaved` re-applies to open pins.
4. Tests: clamp below/above/default and settings round-trip.

## Verification Plan

- Build + tests.
- Live drive (with Story 40): pin a provider, set slider to a low value, save — pinned window becomes translucent immediately; floor prevents invisibility.

## Execution Log

- 2026-07-05: `PinnedWindowOpacityPercent` added (default 100, Normalize clamps 10-100, equality/hash updated); settings slider (10-100, snap 5) with live % label and floor explanation; `App` applies opacity to new pins and re-applies to open pins on settings save.
- Tests: clamp theory (0/9/10/55/100/150) + default; 223/223 pass.
- Live drive (shared with Story 40): pinned Codex window, slider set to 40 via UIA RangeValue, Save - screenshot shows desktop content clearly bleeding through the translucent pinned window while it stays readable.
- Incidental fix: the drive exposed that owned windows (settings) are not returned by UIA root-children enumeration - automation scripts now resolve them via EnumWindows; `OpenConfigurationWindow` gained lifecycle logging and no longer strands its single-instance guard if window creation throws.

## Completion Review

- The popup was deliberately left opaque (transient glance surface); the story's value is on persistent overlays - recorded as the "where appropriate" decision.
- Diagnosis detour: an apparent settings-window failure turned out to be a UIA enumeration quirk, not an app bug; the added logging makes any real future failure visible.
