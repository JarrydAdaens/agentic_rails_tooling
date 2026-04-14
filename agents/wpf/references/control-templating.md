---
name: control-templating
version: 1.1
---

# Control Templating

## Use This Reference When

- Restyling an existing WPF control without losing its semantics or accessibility behavior
- Replacing the visual tree of a built-in control while preserving its native behavior such as `Click`, focus handling, commands, validation, and routed events
- Building a platform-specific or brand-specific presentation on top of familiar controls
- Deciding whether a `Style`, `ControlTemplate`, or custom control is the right move for a visual goal

## Veteran Expert Stance

Control templating is the WPF mechanism for completely replacing the visual structure of a control without altering its underlying behavior or functionality.

The goal is to maximize visual freedom while retaining the built-in behaviors, accessibility affordances, automation support, and routed events of the standard WPF control model.

This reference is about lookless templating discipline and template correctness. The full lifecycle of authoring a reusable custom control belongs in `custom-control-authoring.md`.

## What Templates Are For

- Separating look from behavior. Standard WPF controls are designed to be lookless. The control defines what it does, while the template defines how it appears.
- Defining interactive feedback. Templates host visual states such as `Normal`, `MouseOver`, `Pressed`, `Focused`, `Disabled`, `Selected`, or validation-related states, typically coordinated with `VisualStateManager`.
- Providing flexible content slots. `ContentPresenter` and `ItemsPresenter` project control content or items into the custom visual tree without rebuilding that projection logic yourself.
- Reskinning controls without reauthoring behavior. A control can look radically different while remaining the same underlying type to the rest of the application.

## Practical Heuristics

- Use `TemplateBinding` or `RelativeSource TemplatedParent` for essential properties such as `Background`, `Foreground`, `BorderBrush`, `Padding`, `Content`, `HorizontalContentAlignment`, and `VerticalContentAlignment`.
- Respect the control contract. If a control expects named parts such as `PART_Popup`, `PART_ContentHost`, or `PART_EditableTextBox`, they must exist with the correct names or the control will lose functionality.
- Prefer starting from the default control template when working with complex controls. It is safer to adapt the shipped template than to rebuild all required parts, states, and behaviors from scratch.
- Use `VisualStateManager` over large trigger webs when the control has mutually exclusive or overlapping interaction states.
- Keep templates resource-driven. Hard-coded visual values reduce theming flexibility and make control instances harder to customize.
- Escalate from styling to custom control authoring only when the control contract itself needs to change, not merely its appearance.
- If you are defining `DefaultStyleKey`, `Generic.xaml`, or `OnApplyTemplate`, you have crossed from pure templating into custom control authoring and should load `custom-control-authoring.md`.

## Template Building Blocks

The most important template primitives are usually:

- `ContentPresenter` for `ContentControl`-based controls such as `Button`, `CheckBox`, or `Label`
- `ItemsPresenter` for `ItemsControl`-based controls such as `ListBox`, `ListView`, or `ComboBox`
- Named parts required by the control's implementation
- Visual state groups that define interaction feedback
- Resource-backed brushes, thicknesses, corner treatments, and motion tokens

If one of these is omitted carelessly, the result may look right in a screenshot while behaving incorrectly in a real UI.

## Visual States And Feedback

A beautiful template is not complete until its state model is complete:

- Define how the control looks when idle
- Define how it responds to hover, press, focus, keyboard interaction, validation, disabled state, and selection where relevant
- Ensure interaction transitions feel intentional rather than abrupt
- Treat accessibility and affordance clarity as part of the design, not as separate concerns

Controls without meaningful state feedback often feel dead even when the visuals are polished.

## Platform-Specific UI

Templates are the ideal way to reskin an application or impose a strong platform or brand identity without discarding standard WPF controls.

- Use implicit styles with `TargetType` and no `x:Key` when a control family should pick up the same template automatically within scope.
- Use shared resource dictionaries so templates draw from the same palette, spacing system, and motion language.
- Use `DynamicResource` when platform or theme values must update at runtime, such as light and dark mode swaps.

The outer control remains familiar. View models and application logic continue to interact with standard control types such as `Button`, `CheckBox`, `Slider`, or `TextBox`, while the user experiences a custom visual surface.

## Style Versus Template Versus Custom Control

Use the least invasive tool that solves the problem:

- Use a `Style` when setters and small visual adjustments are enough
- Use a `ControlTemplate` when the visual tree itself must change
- Use a custom control when you need a new reusable control contract, not just a new appearance

If the task is "make it look different," templating is usually the right answer before subclassing.

## Smells

- Creating a new `UserControl` or subclass just to change the appearance of an existing control
- Hard-coding colors, shapes, or spacing values inside the template instead of flowing them from resources or templated-parent properties
- Forgetting required parts so the control silently loses editing, popup, scrolling, or selection behavior
- Building only the resting visual and omitting hover, pressed, disabled, focused, or validation states
- Replacing a standard control with a bespoke structure that looks right but no longer behaves like the control consumers expect

## Goal

Fully use WPF's lookless architecture by applying `ControlTemplate`s to reshape the visual presentation of controls while preserving the framework's mature behavioral logic, accessibility expectations, and maintainability.
