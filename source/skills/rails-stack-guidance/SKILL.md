---
name: rails-stack-guidance
description: Use when an Agentic Rails project explicitly selects Qt, Unreal, or WPF stack guidance in .agentic-rails.json, or when the user asks to adopt one of those stacks. Load only the selected domain reference; never infer WPF from XAML or Qt or Unreal from C++ alone.
disable-model-invocation: false
metadata:
  version: "1.0"
---

# Agentic Rails stack guidance

The starter records explicitly selected stack packs in `.agentic-rails.json` under `stack_packs`. Read that field, or use a direct user selection. If neither names a stack, do not load a domain pack. Host selection by itself is not stack adoption.

| Selected pack | Guidance |
| --- | --- |
| `unreal` | [Unreal C++](references/unreal.md) |
| `qt` | [Qt C++](references/qt.md) |
| `wpf` | [WPF](references/wpf.md) |

Read only the selected reference. If a project selects more than one pack, apply each only to its actual framework files and follow project-local instructions where they differ. A `.uproject` or Unreal build module supports the Unreal classification; Qt project metadata or Qt modules support Qt; `UseWPF` in the project file supports WPF. A file extension alone is insufficient to select any of these packs.

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Honor the project's explicit stack selection and higher-priority project instructions.
- Never apply Unreal conventions to generic or Qt C++ solely because a file ends in `.cpp` or `.h`.
- Never apply WPF conventions solely because a file ends in `.xaml`.
- Keep these references on demand; do not add their full bodies to always-required project instructions.
