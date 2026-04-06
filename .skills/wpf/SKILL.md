---
name: wpf
description: Use this skill when the user is building, styling, refactoring, troubleshooting, or architecting WPF applications and control libraries. It covers custom controls, templating, resources, MVVM, items controls, input, threading, accessibility, navigation, diagnostics, and performance, and it loads deeper reference files only for the WPF engineering domain currently in play.
version: 1.2
---

# WPF Frontend and Application Engineering

This skill is for production-grade WPF engineering work. It should guide the agent toward solutions that feel native to the WPF ecosystem rather than treating XAML as generic markup or treating desktop UI as if it were web frontend work.

The goal is not just to make the UI work. The goal is to shape UI that is:

- Architecturally sound
- Reusable and composable
- Native-feeling in XAML
- Visually polished
- MVVM-friendly
- Accessible and keyboard-credible
- Diagnostics-friendly
- Performance-aware

## Working Style

Start by identifying what kind of WPF problem is actually being solved. Do not load every reference file up front. Read the smallest relevant set.

Think in this order:

1. What is the user trying to build or change: a screen, control library, template, item presentation surface, theme system, interaction model, async flow, accessibility pass, or performance fix?
2. What is the right WPF abstraction: `Style`, `ControlTemplate`, `DataTemplate`, `UserControl`, custom control, attached behavior, attached property, dependency property, routed command, view model, collection view, or navigation shell?
3. Which parts belong in XAML, which belong in view models, which belong in control code, and which belong in app infrastructure?
4. What would make this feel native to WPF instead of improvised?

Prefer the least powerful abstraction that cleanly solves the problem. Do not jump to inheritance or custom controls when a template, behavior, style, or attached property is enough.

After identifying the problem type, load only the reference files that directly help solve it. This skill is a catalogue first and a knowledge dump second.

## Default WPF Stance

- Prefer composition over inheritance.
- Prefer MVVM and binding over code-behind event handling.
- Prefer routed commands, behaviors, and attached properties over ad hoc event wiring.
- Prefer styles, templates, and resources over duplicated markup.
- Prefer collection views, templates, and container styling over imperative item UI construction.
- Prefer render-only animation and cheap state transitions over layout-heavy motion.
- Prefer control authorship patterns that preserve native WPF expectations.
- Prefer keyboard, automation, and accessibility correctness as part of the design, not as a cleanup phase.
- Prefer diagnostics-led troubleshooting over guessing.
- Preserve the behavior of existing controls when reskinning them unless the user explicitly wants a different interaction model.

## Reference Map

Load these references only when they are relevant.

### Control Authoring

- [references/componentization.md](references/componentization.md)
  Use when breaking views or controls into reusable pieces, choosing between `UserControl`, templates, behaviors, and attached properties, or reducing duplication without freezing future flexibility.
- [references/dependency-properties.md](references/dependency-properties.md)
  Use when building or extending control APIs in code, defining dependency properties, overriding metadata, or exposing bindable state that should feel native to XAML.
- [references/control-templating.md](references/control-templating.md)
  Use when replacing the visual tree of an existing control, preserving parts and states, or restyling controls without breaking their contracts.
- [references/custom-control-authoring.md](references/custom-control-authoring.md)
  Use when creating a real reusable custom control, wiring `DefaultStyleKey`, `Generic.xaml`, `OnApplyTemplate`, visual states, automation peers, and the end-to-end control lifecycle.
- [references/data-templating-and-items-controls.md](references/data-templating-and-items-controls.md)
  Use when building `ItemsControl`-driven UI, `DataTemplate`s, `ItemsPanelTemplate`s, grouping, filtering, sorting, tree presentation, or collection-heavy surfaces.

### Presentation and Theming

- [references/visual-design-and-motion.md](references/visual-design-and-motion.md)
  Use when the task is about visual quality, composition, motion language, visual states, storyboards, transitions, or premium-feeling interaction design.
- [references/resource-system.md](references/resource-system.md)
  Use when organizing shared colors, brushes, styles, templates, theme dictionaries, `Generic.xaml`, pack URIs, merged dictionaries, or library resource lookup boundaries.

### Application Architecture and Interaction

- [references/mvvm-and-presentation-architecture.md](references/mvvm-and-presentation-architecture.md)
  Use when the task involves view models, bindings, commands, validation, `DataContext`, presentation shaping, or deciding whether logic belongs in the view, view model, or model.
- [references/input-focus-and-commanding.md](references/input-focus-and-commanding.md)
  Use when the task touches routed commands, input bindings, keyboard navigation, focus scopes, tab flow, access keys, or behavior-driven event bridging.
- [references/threading-dispatcher-and-async-ui.md](references/threading-dispatcher-and-async-ui.md)
  Use when work crosses the UI thread boundary, coordinates async loading, updates observable collections, reports progress, or needs cancellation and dispatcher discipline.
- [references/windowing-navigation-and-lifetime.md](references/windowing-navigation-and-lifetime.md)
  Use when the task involves windows, dialogs, owned windows, startup and shutdown flow, navigation shells, modal versus modeless behavior, or app lifetime orchestration.
- [references/accessibility-automation-and-localization.md](references/accessibility-automation-and-localization.md)
  Use when the task touches keyboard-first interaction, screen reader support, automation peers, high contrast, scalable layout, localization, or culture-aware UI behavior.

### Quality, Diagnostics, and Runtime Behavior

- [references/performance-and-optimization.md](references/performance-and-optimization.md)
  Use when the task touches rendering cost, invalidation, virtualization, diagnostics, binding tracing, layout debugging, `Freezable` usage, memory leaks, animation efficiency, or retained-mode rendering behavior.

## Load Combinations

Typical combinations:

- Reusable control work: `componentization.md` + `dependency-properties.md`
- Custom control library work: `custom-control-authoring.md` + `dependency-properties.md` + `control-templating.md`
- Reskinning a control: `control-templating.md` + `visual-design-and-motion.md`
- App-wide theming: `resource-system.md` + `visual-design-and-motion.md`
- List-heavy or grouped data UI: `data-templating-and-items-controls.md` + `performance-and-optimization.md`
- UI logic cleanup: `mvvm-and-presentation-architecture.md` + `componentization.md`
- Event-heavy UI cleanup: `mvvm-and-presentation-architecture.md` + `input-focus-and-commanding.md`
- Async or cross-thread UI work: `threading-dispatcher-and-async-ui.md` + `mvvm-and-presentation-architecture.md`
- Dialog, window, or navigation work: `windowing-navigation-and-lifetime.md` + `mvvm-and-presentation-architecture.md`
- Accessibility or keyboarding work: `accessibility-automation-and-localization.md` + `input-focus-and-commanding.md`
- Runtime theming or skinning: `resource-system.md` + `control-templating.md` + `visual-design-and-motion.md`
- Rendering or binding troubleshooting: `performance-and-optimization.md` plus the domain that introduced the issue

## Execution Checklist

When using this skill:

1. Identify the correct WPF abstraction before writing code.
2. Load only the smallest reference set that gives enough domain truth.
3. Keep the visual tree, bindings, state model, and ownership boundaries understandable.
4. Preserve MVVM boundaries unless there is a clear WPF-specific reason not to.
5. Reuse resources, templates, and collection-view mechanisms instead of cloning markup or building UI imperatively.
6. Keep interactions smooth, accessible, and cheap.
7. Verify that the result still feels like a native WPF control, view, or application surface.
8. Prefer the framework feature that preserves the most native WPF behavior for the least implementation cost.

## Do Not

- Do not treat WPF like web frontend work.
- Do not default to code-behind click handlers for application behavior.
- Do not subclass controls when styles, templates, behaviors, or attached properties are sufficient.
- Do not treat item presentation, navigation, input, accessibility, or threading as afterthoughts.
- Do not spread one domain's guidance across multiple references when one reference should clearly own it.
- Do not place all knowledge in this file. Keep domain depth in the reference files and load them on demand.
