---
name: story-42-relocate-card-buttons
description: Tier 4 implementation plan for Milestone 3 Story 42 — move the config and info buttons to the popup footer's bottom-right, freeing the top for the provider tab bar.
metadata:
  version: "1.0"
  owner: "Jarryd Adaens"
  repo: "quota_tank"
---

# Story 42: Relocate Config and Info Buttons to Card Footer

## Metadata

- Task Type: `GOAL`
- Task Name: Relocate config and info buttons to card footer
- Status: Complete
- Owner: Jarryd Adaens
- Last Updated: 2026-07-05

## Linked Context

- Design: [design.md](../../../design.md)
- Milestone: [milestone-3.md — Story 42](../../../milestones/milestone-3.md#story-42)
- Enables: [Story 43](../story-43-provider-tab-bar/plan.md).
- Applicable Evaluations: rails-eval-jobs-done; screenshot in live drive (combined with Story 43).

## Estimates (CER)

- Complexity: 3 / Effort: 3 / Risk: 2

## Objective

The About (info) and Settings (config) buttons sit at the bottom-right of the tray popup beneath the provider card, with identical command bindings, leaving the top row of the pane free for the Story 43 tab bar.

## Scope

- In scope: `TrayPopupWindow.xaml` layout only — the two buttons move from the top row into the footer row (pagination center, buttons right until Story 43 moves pagination up).
- Out of scope: changing what the buttons do; pinned-window layout (it has no config/info buttons).

## Implementation Steps

1. Remove the top button row; place the buttons at the footer's right edge.
2. Live-verify placement and that both buttons still open About/Settings.

## Verification Plan

- Build + tests; combined live drive with Story 43 (screenshot + button invoke through UIA).

## Execution Log

- 2026-07-05: Top button row removed; About/Settings buttons moved into the footer grid's right column with identical command bindings and automation names; card row margin adjusted. Build clean; 223/223 tests pass.
- Live drive screenshot confirms bottom-right placement under the provider info display with the top of the pane freed; the Settings command was separately exercised via UIA earlier in this session (Story 41 drive) with unchanged bindings.

## Completion Review

- Pure layout move as scoped; Story 43 can now claim the top row.
