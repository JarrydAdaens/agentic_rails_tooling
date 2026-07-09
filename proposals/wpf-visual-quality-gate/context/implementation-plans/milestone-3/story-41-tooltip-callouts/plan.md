---
name: story-41-tooltip-callouts
description: Tier 4 implementation plan for Milestone 3 Story 41 — cap tooltip width and restyle tooltips as callouts with a pointer triangle.
metadata:
  version: "1.0"
  owner: "Jarryd Adaens"
  repo: "quota_tank"
---

# Story 41: Constrain Tooltip Width with Callout Pointer

## Metadata

- Task Type: `GOAL`
- Task Name: Constrain tooltip width with callout pointer
- Status: Complete
- Owner: Jarryd Adaens
- Last Updated: 2026-07-05

## Linked Context

- Design: [design.md](../../../design.md)
- Milestone: [milestone-3.md — Story 41](../../../milestones/milestone-3.md#story-41)
- Applicable Evaluations: rails-eval-jobs-done; screenshot check in live drive.

## Estimates (CER)

- Complexity: 4 / Effort: 4 / Risk: 3

## Objective

Tooltips are capped at a sensible max width with wrapping text and render as callouts — placed under their source element with a triangle pointing up at it — across all themes, with content unchanged.

## Problem Summary

The shared `ToolTip` style (Themes/Base/Controls.xaml) has no width cap and no wrapping, so long strings like the providers' `DataSourceDescription` render as one screen-wide line. Placement follows the mouse, so nothing anchors the tip to its element.

## Scope

- In scope: `MaxWidth` (320) + wrapping content template on the shared ToolTip style; template becomes pointer-triangle + body border; `Placement="Bottom"` so the triangle points at the source element. Theme token brushes unchanged, so all three themes inherit the callout.
- Out of scope: rewriting tooltip content; per-control placement overrides (WPF flips placement at screen edges — accepted).

## Implementation Steps

1. Restyle the shared ToolTip template (pointer Path overlapping the body border, rounded body, wrapping TextBlock content template).
2. Live-verify against the longest tooltip in the app (settings provider info glyph).

## Verification Plan

- Build + tests.
- Live drive: hover the Cursor provider's info glyph in Settings (longest description) — screenshot shows a wrapped, width-capped callout with the pointer at the glyph.

## Execution Log

- 2026-07-05: Shared ToolTip style gains MaxWidth 320, a wrapping string content template, Placement=Bottom with a small negative horizontal offset, and a callout template (pointer Path overlapping the body border by 1px, open triangle path so no seam line). All theme token brushes untouched, so Light/Dark/FrutigerAero inherit the callout.
- Live drive: short tooltip (card pin button) renders anchored under its element; the longest tooltip in the app (Cursor provider info glyph in Settings, ~450 chars) wraps inside the 320px callout with the pointer aimed at the glyph. Screenshots captured in session. 223/223 tests pass.

## Completion Review

- Placement flips at screen edges per WPF defaults, which can detach the pointer from the exact glyph at extremes - accepted and noted in scope.
- Content is unchanged; only layout/placement moved.
