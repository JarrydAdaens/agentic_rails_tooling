---
name: componentization
version: 1.1
---

# Componentization

## Use This Reference When

- Deciding how to encapsulate duplicated XAML or UI logic into reusable pieces
- Choosing the right architectural tool such as `UserControl`, custom `Control`, `DataTemplate`, `ControlTemplate`, or behavior for a specific UI requirement
- Applying MVVM principles so modular UI components remain decoupled from business logic and are easy to test
- Designing performant visual trees by avoiding deep nesting and heavy unoptimized elements

## Veteran Expert Stance

Good WPF componentization is built on composition over inheritance, strictly separates control logic from visual representation through lookless design where appropriate, and prioritizes the lightest feature that cleanly solves the problem.

Start by asking what is actually being reused:

- Is it just the visual layout for a data object: use an implicit `DataTemplate` linked to the view model
- Is it a visual alteration of an existing control: use a `Style` or `ControlTemplate` to change appearance without changing core behavior
- Is it a repeatable interaction or event hookup: use a behavior or attached property to encapsulate UI logic without introducing a derived class
- Is it an aggregate of existing controls with straightforward layout needs: create a `UserControl`
- Is it core behavior that requires maximum consumer flexibility in how it looks: build a custom `Control` based on the parts-and-states model

## Preferred Decision Order

1. DataTemplates. Use implicit data templates defined by `DataType` without an `x:Key` to render view models automatically. This keeps XAML declarative and cleanly separates data from presentation.
2. Styles and ControlTemplates. Use these to radically change how existing WPF controls look instead of subclassing them for visual reasons.
3. Behaviors and attached properties. Use `Microsoft.Xaml.Behaviors` when you need reusable interaction logic such as event-to-command wiring, drag-and-drop, focus rules, or attachable view behavior. Behaviors are often preferable when instance-level state and clean attach-detach lifecycle management matter.
4. UserControls. Use a `UserControl` when grouping existing controls into a reusable chunk of UI such as a card, editor panel, or form section. This is a composition tool, not a highly styleable control primitive.
5. Custom Controls. Write a custom `Control` when building reusable functionality whose consumers must be able to replace the visual tree completely through a `ControlTemplate`.

## Practical Heuristics

- Expose public configuration through dependency properties so the component participates naturally in binding, styling, animation, and designer tooling.
- If a reusable surface needs arbitrary content slots such as a header, icon, footer, or body, use `ContentControl`, `ContentPresenter`, or dependency properties of type `object` rather than hard-coding fixed child content.
- When building a `ControlTemplate`, use `{TemplateBinding}` or `RelativeSource TemplatedParent` to flow control properties into the template cleanly.
- Use `VisualStateManager` for controls with meaningful overlapping states such as `Normal`, `MouseOver`, `Pressed`, `Disabled`, or `Selected`.
- Use routed events when a component must notify parent containers in a WPF-native way.
- Keep visual trees shallow. Prefer a clear `Grid` or similarly efficient layout over deeply nested panel stacks that multiply measure and arrange cost.
- Keep code-behind limited to view plumbing, focus control, view-only state coordination, or animation hooks. Move application behavior into commands, view models, behaviors, or control logic as appropriate.
- If the reuse point is really item presentation, prefer `DataTemplate` and `ItemsControl` techniques over inventing a new view type. See `data-templating-and-items-controls.md`.
- If the reuse point is a true reusable control contract, hand off to `custom-control-authoring.md` rather than trying to stretch `UserControl` too far.
- If the reuse point is interaction policy, check `input-focus-and-commanding.md` before introducing more event handlers.

## Behaviors Versus Attached Properties

Both are valid tools, but they solve slightly different problems:

- Prefer a behavior when the feature needs instance state, event subscriptions, attach-detach lifecycle control, or multiple coordinated hooks on one element.
- Prefer an attached property when the feature is naturally expressed as a small attached capability or declarative flag that should feel like part of the property system.
- Prefer either of these over inheritance when the goal is reusable attachable functionality rather than a new control type.

## UserControl Versus Custom Control

This is one of the most important WPF judgment calls:

- Choose `UserControl` when you want to package a known composition of child controls and you control the internal layout.
- Choose a custom `Control` when the behavior is the reusable asset and consumers should be free to fully reskin it through templates.
- A `UserControl` is usually faster to build.
- A custom `Control` is usually the better long-term primitive when design freedom for consumers matters.

## MVVM Alignment

Componentization should reinforce MVVM, not fight it:

- Use `DataTemplate`s to map view models to views declaratively.
- Keep business logic out of views and `UserControl` code-behind.
- Use commands instead of click handlers for application behavior.
- Avoid components that require consumers to reach into named internal elements.
- Keep component APIs bindable and view-model-friendly.

## Performance Notes

Componentization is not automatically a performance win. Poor modularization can create bloated trees and expensive layout:

- Avoid wrapping simple content in unnecessary container layers.
- Reuse styles, templates, and resources instead of cloning markup trees.
- Be careful with nested `ItemsControl` structures and deeply recursive templates.
- Remember that every extra visual and every extra panel participates in layout and rendering cost.

## Smells

- Duplicated XAML copied across multiple views instead of extracted into a `DataTemplate`, `UserControl`, style, or reusable behavior
- Business logic in code-behind that changes application state, coordinates workflows, or talks to services
- Subclassing `Button`, `TextBox`, or similar controls just to change shape, color, spacing, or visuals
- Dependency property CLR wrappers containing logic that should live in metadata callbacks
- Components that leak memory because event handlers, subscriptions, or behaviors are not detached correctly
- `UserControl`s that should have been custom controls because consumers need real template freedom
- Components whose only public API is "go find this named child and manipulate it"

## Goal

Build a modular, performant, and maintainable WPF UI architecture where views stay loosely coupled to business logic, behaviors can be attached cleanly to many elements, and reusable controls separate their logic from their visual templates when that level of flexibility is needed.
