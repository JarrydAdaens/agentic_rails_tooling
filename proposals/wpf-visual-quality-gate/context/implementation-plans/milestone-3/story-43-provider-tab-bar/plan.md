---
name: story-43-provider-tab-bar
description: Tier 4 implementation plan for Milestone 3 Story 43 — provider icon tab bar with top pagination in the tray popup.
metadata:
  version: "1.0"
  owner: "Jarryd Adaens"
  repo: "quota_tank"
---

# Story 43: Provider Icon Tab Bar with Top Pagination

## Metadata

- Task Type: `GOAL`
- Task Name: Provider icon tab bar with top pagination
- Status: Complete
- Owner: Jarryd Adaens
- Last Updated: 2026-07-05

## Linked Context

- Design: [design.md](../../../design.md)
- Milestone: [milestone-3.md — Story 43](../../../milestones/milestone-3.md#story-43)
- Depends on: [Story 42](../story-42-relocate-card-buttons/plan.md) (top area freed).
- Applicable Evaluations: rails-eval-jobs-done; WPF Visual Quality Gate (screenshot + tab navigation via UIA).

## Estimates (CER)

- Complexity: 6 / Effort: 6 / Risk: 4

## Objective

Pagination moves to the top of the popup: each enabled provider renders its platform icon as a clickable tab with its pagination dot beneath it, prev/next chevrons flank the bar, the active provider is highlighted, and clicking a tab navigates directly to that provider — making the machine's enabled provider set legible at a glance.

## Scope

- In scope: `SelectProviderCommand(ProviderStateViewModel)` on `TrayPopupViewModel`; `IconKeyToImageSourceConverter` (maps `IconResourceKey` → app resource, avoiding a duplicate trigger table); top tab bar in `TrayPopupWindow.xaml`; footer keeps only the relocated config/info buttons.
- Out of scope: reordering or enabling/disabling providers from the tab bar (navigation only).

## Implementation Steps

1. VM command + test-free wiring (thin index assignment; navigation logic already covered by Next/Previous behavior).
2. Converter for icon resource lookup.
3. Tab bar layout: chevrons + ItemsControl (icon button, dot beneath, active highlight via the existing `CurrentItemToBrushConverter`; inactive icons dimmed).
4. Live drive: screenshot; click a non-active tab via UIA and confirm the card switches.

## Verification Plan

- Build + tests; live drive with UIA tab click navigating to the target provider (card DisplayName changes) and screenshot evidence.

## Execution Log

- 2026-07-05: `SelectProviderCommand` added to `TrayPopupViewModel`; `IconKeyToImageSourceConverter` + `CurrentItemToOpacityConverter` added; top tab bar built (chevrons flanking icon tabs, dot beneath each icon, active tab full-opacity with filled dot, hover chrome); bottom paginator removed leaving the Story 42 footer buttons.
- Live drive: clicked the "Select Google Antigravity Provider" tab via UIA - the card switched directly to Antigravity; screenshot shows all four enabled providers' icons at a glance with the active tab indicated. Build clean; 223/223 tests pass.

## Completion Review

- The icon lookup went through a converter against application resources instead of duplicating ProviderCard's per-provider trigger table - one place to extend when providers are added.
- Tab bar is navigation-only per scope; enabled-set legibility (the story's driving need across three workstations) is delivered by the icon row itself.
