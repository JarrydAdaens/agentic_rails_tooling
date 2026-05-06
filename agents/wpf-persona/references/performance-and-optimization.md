---
name: performance-and-optimization
version: 1.1
---

# Performance and Optimization

## Use This Reference When

- The UI feels laggy, frozen, janky, or over-invalidated
- Animations stutter or expensive transitions are being designed
- Rendering large datasets or complex visual layouts
- A control updates frequently or hosts heavy custom visuals
- Hunting down memory leaks related to UI elements, bindings, or event handlers
- Diagnosing binding failures, layout pathologies, template bugs, or rendering-path problems

## Veteran Expert Stance

WPF performance work starts with understanding what actually causes invalidation, layout work, and redraw. Performance is usually won by reducing unnecessary work, not by micro-optimizing random code paths.

You must understand the difference between the measure-arrange layout passes and the render pass. Layout is expensive because WPF must recalculate size and placement relationships. Rendering is usually cheaper, especially when you stay on GPU-friendly paths and avoid forcing the CPU to constantly recompute layout or rebuild visuals.

The goal is to modify the visual tree deliberately, update only what needs updating, and lean into retained-mode rendering rather than fighting it.

## Core Performance Ideas

- UI virtualization is mandatory for large item sets. If a `ListBox`, `ListView`, `TreeView`, or similar control is showing many items, virtualization should be an explicit concern.
- Layout is expensive, rendering is cheaper. Properties such as `Width`, `Height`, `Margin`, and `LayoutTransform` trigger layout work. Properties such as `Opacity` and `RenderTransform` usually stay in the render lane.
- Binding errors are silent killers. Repeated binding failures spam trace output and can significantly degrade runtime performance.
- Freeze static resources. `Freezable` objects such as brushes, geometries, pens, and transforms should be frozen when they are immutable so WPF can skip change tracking overhead.
- Keep high-frequency updates tightly scoped. Performance problems often come from touching too much of the tree too often.
- Use caching and retained-visual strategies deliberately when a surface is expensive to redraw but visually stable between frames.

## Practical Heuristics

- Favor `RenderTransform` over `LayoutTransform`. For movement, scale, rotation, or emphasis, `RenderTransform` is almost always the right first choice.
- Apply opacity to the brush, not the element, when possible. Element-level opacity can force extra off-screen compositing work for the full subtree.
- Use virtualization settings explicitly for large collections, including recycling behavior where appropriate.
- Use `DrawingVisual` or override `OnRender` when rendering thousands of lightweight visual primitives. Do not force everything through heavyweight `UIElement` composition if the surface is really just drawing.
- Cache complex static visuals with `BitmapCache` when they are expensive to redraw but structurally stable. Use this deliberately because it trades memory for render speed.
- Keep the visual tree shallow. Every extra panel, border, decorator, and nested template layer adds layout and traversal cost.
- Watch the output window for binding failures and resource lookup issues. Performance work begins with a clean diagnostic surface.
- Understand which dependency property changes trigger measure, arrange, or render invalidation before animating or updating them frequently.

## Virtualization And Large Data

Virtualization is one of the biggest practical wins in WPF:

- Ensure item controls use a virtualizing panel where supported
- Prefer recycling virtualization for long-lived scrolling surfaces
- Avoid accidentally disabling virtualization through custom panels, nested scroll viewers, or incompatible container setups
- Be cautious with heavy item templates because virtualization reduces count, not per-item complexity

Large data UIs often need both virtualization and template simplification.

## Diagnostics Workflow

Diagnostics should be a standard part of WPF engineering, not a last resort:

- Keep the output window clean of binding errors before tuning anything else
- Use binding tracing when a binding path, source, or update mode is behaving unexpectedly
- Use Live Visual Tree, Live Property Explorer, or Snoop to inspect real runtime structure instead of guessing what the tree became
- Inspect control templates and generated containers when item UI or state behavior looks wrong
- Trace layout issues by looking for repeated measure-arrange churn, unexpected container growth, or template bloat
- Confirm whether rendering is staying on a healthy path before assuming the issue is pure CPU logic

A surprising amount of "WPF is slow" turns out to be "the tree is wrong," "the bindings are noisy," or "the template contract is broken."

## Retained-Mode Mindset

WPF uses a retained-mode graphics system. Your application defines a scene graph, and WPF decides how and when to redraw it.

Efficient retained-mode work usually means:

- Updating fewer properties
- Updating cheaper properties
- Updating a smaller portion of the tree
- Reusing objects instead of recreating them
- Letting WPF redraw naturally instead of trying to force frame-by-frame behavior manually

Do not manually force redraws casually. Calls such as `InvalidateVisual()` or other invalidation methods in high-frequency paths can quickly create lag if used without discipline.

If a custom-rendered surface needs frequent updates, update the backing data or drawing objects intelligently and let WPF rerender through its normal retained pipeline.

## Memory And Lifetime Discipline

Many WPF performance problems are really lifetime problems:

- Standard C# event subscriptions can keep controls and view models alive unexpectedly
- `INotifyPropertyChanged` and collection subscriptions can leak if long-lived publishers outlive the UI
- Unfrozen `Freezable` instances can participate in change notification graphs that hold onto objects longer than intended
- Messenger, behavior, or attached-property patterns should still be reviewed for detach and cleanup behavior

Smooth UI requires both frame-rate discipline and memory discipline.

## Software Rendering Risks

Not all visual effects stay on the hardware-accelerated path:

- Heavy legacy `BitmapEffect` usage
- Misuse of `AllowsTransparency="True"` on windows
- Expensive opacity stacks and compositing-heavy visual structures
- Large or layered effects that push rendering off the fast path

When a UI feels inexplicably heavy, confirm that the design is not triggering software rendering or excessive compositing.

## Boundaries

This reference owns runtime behavior, diagnostics, and optimization.

- For the architecture of item presentation itself, use `data-templating-and-items-controls.md`.
- For async coordination and dispatcher rules, use `threading-dispatcher-and-async-ui.md`.
- For visual quality choices, use `visual-design-and-motion.md`.

## Smells

- Animating `Width`, `Height`, `Margin`, or other layout-triggering properties when a `RenderTransform` would communicate the same motion
- Memory leaks caused by forgotten event unsubscription or long-lived bindings and notifications
- Deeply nested panels and decorators inside item templates that multiply measure-arrange cost
- Binding errors constantly appearing in diagnostics output
- Recreating brushes, geometries, or other graphical objects during frequent updates instead of reusing or freezing them
- Software-rendering fallbacks caused by inappropriate visual effects or transparency usage
- Calling invalidation methods repeatedly in hot paths without understanding the redraw consequences
- Troubleshooting based on guesswork without checking runtime tree, bindings, and layout behavior first

## Goal

Build buttery-smooth, responsive, and memory-efficient WPF applications by respecting retained-mode rendering, minimizing unnecessary layout invalidation, fully leveraging GPU-friendly rendering paths, and managing object lifetimes carefully.
