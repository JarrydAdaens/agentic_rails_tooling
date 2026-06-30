---
name: wpf-tree-sensor
description: Inspect the Windows UI Automation tree of a running WPF or Windows desktop app. Use when verifying runtime UI state, expected controls, accessibility names, automation IDs, enabled/offscreen state, window presence, dialogs, popups, or structural UI evidence without screenshots, debugger attachment, Snoop, or app modification.
metadata:
  version: "2.0"
---

# WPF Tree Sensor

Use this skill when UI verification needs structured runtime evidence from a running WPF app. This skill acts as a global reusable sensor that can automatically detect and analyze WPF applications matching the current repository workspace.

## Command Usage

Run the sensor script in one of these modes:

```powershell
# Project-aware auto detection with a concise view summary (recommended)
powershell -NoProfile -ExecutionPolicy Bypass -File "source\skills\wpf-tree-sensor\scripts\Invoke-WpfTreeSensor.ps1" -ProjectAuto -Summarize

# List all top-level windows matching project filters to resolve ambiguity
powershell -NoProfile -ExecutionPolicy Bypass -File "source\skills\wpf-tree-sensor\scripts\Invoke-WpfTreeSensor.ps1" -ProjectAuto -ListWindows

# Explicit targeting with summary output
powershell -NoProfile -ExecutionPolicy Bypass -File "source\skills\wpf-tree-sensor\scripts\Invoke-WpfTreeSensor.ps1" -ProcessName "QuotaTank.WPF" -Summarize

# Full JSON capture for a specific window
powershell -NoProfile -ExecutionPolicy Bypass -File "source\skills\wpf-tree-sensor\scripts\Invoke-WpfTreeSensor.ps1" -WindowTitleContains "Quota-Tank Settings" -MaxDepth 8 -IncludeBoundingRectangles -IncludePatterns -OutputPath "tree-snapshot.json"
```

## Project Auto-Detection

When `-ProjectAuto` is provided, the sensor:
1. Searches upwards for a project-local `.wpf-tree-sensor.json` config file.
2. If not found, searches for `.sln` or `.csproj` files to detect WPF projects (checking for `<UseWPF>true</UseWPF>` or `Microsoft.NET.Sdk.WindowsDesktop`).
3. Infers likely process names (e.g. `QuotaTank.WPF`, `KungFu.WPF`) and window title substrings (e.g. `Quota-Tank`, `Quota Tank`) from the project file names.

### Project Config Format

You can place a `.wpf-tree-sensor.json` file in your repository root:

```json
{
  "appNames": ["QuotaTank.WPF"],
  "windowTitleContains": ["Quota-Tank", "QuotaTank"],
  "preferredWindowTitleContains": "Quota-Tank Settings",
  "ignoreWindowTitleContains": ["Microsoft Visual Studio"],
  "defaultMaxDepth": 8
}
```

## Modes of Operation

- **Full Mode (Default)**: Outputs the full UI Automation hierarchy down to `-MaxDepth` in JSON format.
- **`-ListWindows` Mode**: Lists all running top-level windows with their `Name`, `ProcessId`, `ProcessName`, `ClassName`, `AutomationId`, and `IsOffscreen` state (optionally filtered by other parameters).
- **`-Summarize` Mode**: Emits a lightweight JSON summary containing the top-level window, headings, visible buttons, active selection/toggle states, modal/dialog presence, and the probable current view.

## Heuristics for View Detection

In summary mode, the sensor parses the tree and scores potential views based on:
- Active dialog titles or child window names.
- Selected tab item names.
- Controls with automation IDs containing `View`, `Page`, `Dialog`, or `Content`.
- Word patterns inside the top-level window title.
- Prominent heading/banner text blocks.

## Safety & Security

- **Passive Only**: Do not click, type, inject, attach a debugger, launch Snoop, or modify the target app.
- **Credentials Redaction**: Active values on edit, document, password, or textbox controls containing names or automation IDs matching sensitive keywords (e.g., `password`, `secret`, `token`, `apikey`, `credential`) are automatically redacted with `[REDACTED]` to prevent leakage.

