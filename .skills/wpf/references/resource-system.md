---
name: resource-system
version: 1.1
---

# Resource System

## Use This Reference When

- Organizing colors, brushes, thicknesses, styles, templates, or theme values into a centralized design token architecture
- Standardizing visuals across multiple views or controls through shared or implicit styling
- Building layered theming or skinning such as light and dark mode
- Reducing duplication and controlling redraw scope through smart resource resolution
- Resolving performance issues related to XAML parsing, dictionary lookup cost, or `MergedDictionaries` overuse

## Veteran Expert Stance

The resource system is how WPF centralizes and applies visual properties, templates, and styles so an application can become a coherent, maintainable, and scalable design system instead of a pile of isolated XAML files.

Treat resources as a unified design token architecture. Keep dictionary structures intentional and as flat as practical, and choose the exact right resolution strategy, especially `StaticResource` versus `DynamicResource`, based on whether the value must mutate at runtime.

## What Good Resource Design Achieves

- Separation of concerns. Design tokens, brushes, styles, and templates stay decoupled from business logic and from duplicated view markup.
- Consistent visuals. Shared styles and resources make controls feel like part of one product instead of individually decorated islands.
- Instant theming. When runtime theme swaps are needed, app-level dictionary replacement and dynamic resources allow the surface to update cleanly.
- Better memory and CPU behavior. Static lookups, frozen graphical resources, and disciplined dictionary structure reduce overhead.
- More precise redraw control. Resource choices affect how much of the UI must reevaluate when theme or style values change.

## Practical Heuristics

- Favor `StaticResource` by default. If the value will not change during the app session, prefer static lookup.
- Use `DynamicResource` strictly for values that may change at runtime, such as theme colors, swapped palettes, or runtime skinning.
- Freeze static graphical resources whenever possible. Brushes, geometries, and similar `Freezable` objects should be frozen so WPF can stop tracking them for change notification.
- Use semantic naming. Prefer keys such as `AppBackgroundBrush`, `PrimaryTextBrush`, or `SuccessBorderBrush` instead of keys tied to literal color values.
- Use implicit styles for broad consistency. A `Style` with `TargetType` and no `x:Key` is a powerful way to establish defaults for a control family within scope.
- Keep template, style, and token layers separate enough that each can evolve without forcing edits across unrelated files.
- Centralize reusable spacing, elevation, radius, duration, and typography values alongside color and brush tokens when those concepts are part of the visual system.
- In control libraries, keep the default control theme in `Themes/Generic.xaml` and align it with `ThemeInfo` expectations so custom controls resolve their styles predictably.
- Use pack URIs deliberately when loading dictionaries across assemblies so resource ownership and lookup boundaries stay obvious.

## StaticResource Versus DynamicResource

This is one of the most important judgment calls in WPF resource design:

- Use `StaticResource` when the value is fixed for the lifetime of the loaded view or application session.
- Use `DynamicResource` when the resource must reevaluate because dictionaries may be swapped or resource values may change at runtime.
- Do not use `DynamicResource` by habit. It carries runtime expression and change-tracking cost.
- Do not use `StaticResource` for runtime theme-dependent values if the UI is expected to update without reloading.

Correct selection here improves both theming flexibility and performance.

## Dictionary Structure And Layering

Good layering keeps the system understandable:

- Foundation dictionaries for raw tokens such as colors, brushes, spacing, durations, and typography
- Style dictionaries for control families
- Template dictionaries for deeper control visual definitions
- Feature-specific dictionaries only when a feature genuinely owns distinct resources
- Theme dictionaries for alternate visual systems such as light and dark
- Library dictionaries for reusable control styles and templates that should travel with a control assembly

Keep the hierarchy as shallow as possible while preserving clarity. Excessive fragmentation increases lookup cost and maintenance complexity.

## Deferred Loading And Overrides

WPF resource lookup follows scope and order rules that matter for correctness and performance:

- Resource lookup walks outward through the logical tree until it finds a matching key
- Window- or control-local resources override broader application resources
- In merged dictionaries, later dictionaries win when duplicate keys exist
- Re-merging the same shared dictionaries repeatedly across local controls increases lookup and memory cost
- Cross-assembly resources introduce pack URI and theme lookup boundaries that should be designed intentionally, especially for reusable control libraries

If the same `Colors.xaml`, `Brushes.xaml`, or base style dictionaries are being merged into many controls individually, step back and reconsider the architecture. Shared resources usually belong at app scope or in a small number of clearly owned scopes.

## Performance Notes

Resource work is not just about organization. It affects runtime behavior:

- Excessive `MergedDictionaries` depth can create measurable lookup overhead
- Repeated local merges can multiply parsing and memory cost
- `DynamicResource` should be reserved for true runtime mutability
- Frozen graphical resources reduce change notification overhead and improve memory usage
- Correct build setup matters because compiled XAML is more efficient than loosely treated content

For performance-sensitive applications, it can be worthwhile to consolidate fragmented dictionaries for release builds rather than keeping every tiny token set in its own merged file.

## XAML And Build Discipline

The resource system depends on correct project setup:

- Resource dictionaries should generally use the `Page` build action so XAML is compiled into BAML efficiently
- Shared dictionaries should be organized so load order and override order are explicit
- Theme dictionaries should expose stable semantic keys so templates and styles do not need to change when visual direction changes
- Control libraries should keep theme lookup conventions coherent across `Generic.xaml`, theme-specific dictionaries, and assembly-level `ThemeInfo`

## Smells

- Re-merging the same generic dictionaries into every view, control, or template scope
- Using `DynamicResource` for static values such as fixed margins, fonts, or constants that never change
- Unfrozen brushes, gradients, or geometries in shared dictionaries
- Hardcoded colors, thicknesses, or other visual values embedded inline in views and templates
- Dictionary sprawl so fragmented that nobody can predict precedence or lookup behavior
- Duplicate resource keys whose override order is accidental instead of deliberate
- Incorrect build action on resource dictionary XAML files
- Control libraries whose default styles fail because `Generic.xaml`, pack URI setup, or theme metadata conventions were not respected

## Goal

Build a centralized, performant, and easily themeable visual architecture where design tokens, styles, and templates are managed deliberately, and where the correct resolution strategy prevents unnecessary lookup cost, memory waste, and theming pain.
