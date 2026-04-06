---
name: visual-design-and-motion
version: 1.1
---

# Visual Design and Motion

## Use This Reference When

- The task is about visual quality, polish, fluidity, or premium feel
- You are designing motion, visual states, transitions, or interaction feedback
- The work involves themes, colors, storyboards, triggers, or visual-state-driven behavior
- The UI needs to feel modern, intuitive, and deliberate rather than merely functional

## Veteran Expert Stance

Beautiful WPF UI is built on clear separation of logic from presentation, strong composition, intentional motion language, and hardware-friendly rendering paths so interactions stay fluid under real use.

## Core Levers

- VisualStateManager. This is the preferred engine for managing mutually exclusive states such as `Normal`, `MouseOver`, `Pressed`, `Disabled`, `Selected`, or `Focused`, along with the transitions between them.
- ControlTemplates. Use these to completely replace the visual tree of an existing control while retaining its semantics and behavior contract.
- Resource dictionaries and design tokens. Centralize semantic colors, brushes, durations, easing choices, spacing, and shared stylistic values so the application can be themed and refined coherently.
- Storyboards and triggers. Use these to coordinate multi-property animation and declarative visual reactions over time.
- Spatial composition. Deliberate spacing, silhouette, density, hierarchy, and visual rhythm are part of WPF design quality, not just decoration layered on afterward.

## Motion Principles

Use animation to communicate interaction context, spatial change, hierarchy, and feedback.

- Short micro-interactions around 100 to 200 milliseconds work well for direct manipulation such as hover, press, and focus feedback.
- Larger content transitions often need roughly 300 to 500 milliseconds so they read clearly without feeling sluggish.
- Use easing functions such as `CubicEase` or other intentional curves. Natural-feeling motion is rarely linear.
- Let motion clarify the interface rather than decorate it.
- Keep the motion language cohesive across a screen or feature area.

WPF can produce excellent fluid motion when animations focus on hardware-friendly properties such as `Opacity` and `RenderTransform`.

## Practical Heuristics

- Animate transforms, not layout. Prefer `RenderTransform` for movement, scaling, rotation, and emphasis. Avoid animating `LayoutTransform`, `Width`, `Height`, `Margin`, or `Padding` unless you deliberately want layout recalculation.
- Use `DynamicResource` for runtime theming. If a palette value may change while the app is running, it should generally come through a dynamic resource.
- Apply opacity to brushes instead of entire elements when possible. Element-level opacity can introduce extra compositing cost across a subtree.
- Freeze static graphical resources. Brushes, geometries, pens, and transforms that never change should be frozen when created in code so WPF can treat them more efficiently.
- Coordinate overlapping interaction states with `VisualStateManager` instead of building a maze of independent triggers.
- Use triggers for smaller declarative reactions and `VisualStateManager` when the state model is richer or state transitions overlap.
- Design hover, pressed, focus, disabled, validation, and selection states intentionally. A premium-feeling UI is often defined by these transitions more than its resting state.
- Keep style definitions and motion tokens centralized so multiple controls share the same visual vocabulary.
- Treat layout composition, edge alignment, density, and negative space as first-class design decisions, especially in desktop workflows where information density matters.

## Theme And Resource Discipline

Polish depends on systemization, not ad hoc decoration:

- Prefer semantic resource names such as `SuccessBrush`, `WarningBrush`, `WindowSurfaceBrush`, or `AccentHoverBrush` over raw color intent tied to a single screen.
- Avoid scattering hardcoded hex values through views and templates.
- Keep palette, typography, timing, and elevation choices reusable through shared dictionaries.
- Make theme swaps and brand updates a resource problem, not a file-by-file rewrite.

## Performance-Aware Beauty

Visual quality is only premium if it remains responsive:

- Favor render-only adjustments over layout-affecting animations.
- Be cautious with stacked translucency, large blur-like effects, and broad opacity usage across complex trees.
- Avoid animating many elements independently when a smaller coordinated effect will communicate the same idea.
- Remember that elegant motion usually comes from restraint, timing, and hierarchy rather than sheer animation density.

## Boundaries

This reference owns visual language, state feedback, composition, and motion craft.

- For template contracts and parts-states correctness, use `control-templating.md`.
- For resource lookup and theme architecture, use `resource-system.md`.
- For accessibility-sensitive visual behavior such as focus cues and high contrast, also load `accessibility-automation-and-localization.md`.

## Smells

- Animating `Width`, `Height`, or similar layout properties for effects that should be transform-based
- Default linear motion that feels robotic or mechanical
- Hardcoded hex colors repeated across templates and views
- Visual state logic implemented in code-behind with event handlers instead of declarative XAML state systems
- Heavy transparency stacks, large opacity masks, or expensive compositing used casually
- A visually flashy control whose hover, focus, pressed, disabled, or validation states are inconsistent or unclear

## Goal

Craft visually engaging, responsive, and themeable WPF interfaces where motion feels deliberate, aesthetics stay cleanly separated from application logic, and the experience remains smooth under real interaction.
