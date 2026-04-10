---
owner: Jarryd Adaens    
version: 1.1    
---

# Global Claude Rules — Jarryd Adaens

## Rules — Always Load First
Read and apply `~/.claude/rules/global_rules.md` before every task.

## Rules — Load by Stack
Inspect the workspace before starting. Load every file whose condition matches; skip the rest.

| Condition | Load |
|-----------|------|
| Any `.cs`, `.csproj`, or `.sln` file present | `~/.claude/rules/csharp_rules.md` |
| Task touches WPF, XAML, bindings, or view models | `~/.claude/rules/wpf_rules.md` |
| Any `.uproject` file or Unreal-style source layout present | `~/.claude/rules/cplusplus_rules.md` |
| Any Qt project file, CMake Qt config, or Qt-specific source present | `~/.claude/rules/qt_rules.md` |

## Agents
Use the named agent whenever the task clearly fits its domain. Don't wait to be asked.

| Task involves | Use agent |
|---------------|-----------|
| WPF screens, XAML, MVVM, bindings, controls, theming, WPF performance | `wpf` |

## Conflict Resolution
Project-local `CLAUDE.md` beats these global rules. More specific tech rules beat general ones.
