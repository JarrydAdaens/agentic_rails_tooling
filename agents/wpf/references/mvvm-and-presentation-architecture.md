---
name: mvvm-and-presentation-architecture
version: 1.1
---

# MVVM and Presentation Architecture

## Use This Reference When

- The task involves `DataContext`, binding, commands, validation, or view model shape
- You are deciding whether logic belongs in XAML, code-behind, or the view model
- A view is too event-driven and needs to become more declarative
- A screen or control should fully participate in MVVM

## Veteran Expert Stance

WPF is at its strongest when the view and view model are cleanly decoupled, with binding and commands carrying data and intent across that boundary.

In the ideal case, a view's code-behind contains only view plumbing, often little more than construction and `InitializeComponent()`. The model holds domain data and business behavior, the view model shapes that data for presentation and interaction, and the view binds to it declaratively.

## Core Rules

- Keep UI concerns out of the view model. Do not pass controls into view models, and do not make direct UI calls such as `MessageBox.Show()` from business logic.
- Favor commands over code-behind event handlers for application behavior.
- Use modern MVVM tooling to remove boilerplate. Prefer CommunityToolkit.Mvvm attributes such as `[ObservableProperty]` and `[RelayCommand]` when that toolkit is in play.
- Distinguish application state from pure view state. Selected domain objects, filters, validation, and workflow state belong in the view model. Scroll offsets, transient focus behavior, layout size, and other purely visual mechanics often belong in the view layer.
- Compose view models from smaller child view models when the screen is naturally modular.

## Practical Heuristics

- Use behaviors or event-to-command wiring when a control raises useful events but does not natively expose a `Command` property.
- Use async-aware command types for asynchronous work. `AsyncRelayCommand` is particularly useful because it exposes execution state that the view can bind to without extra plumbing.
- Use a messenger pattern when view models need to communicate without holding direct references to each other. Weak-reference-based messaging is often the safest default for avoiding event-style leaks.
- Use `ObservableValidator` and attribute-based validation when the stack already includes the MVVM Toolkit's validation support.
- Use attributes such as `[NotifyPropertyChangedFor]` and `[NotifyCanExecuteChangedFor]` to keep dependent properties and commands synchronized automatically.
- Prefer simple view-model properties over elaborate converter chains when the display state is conceptually part of the presentation model.
- Keep bindings readable. One clean binding path is usually better than clever indirection through multiple named elements.
- Use child view models and `DataTemplate` mapping when the screen is naturally composed of distinct presentation units.

## CommunityToolkit.Mvvm Guidance

When the project uses the MVVM Community Toolkit, lean on it intentionally:

- `[ObservableProperty]` for observable state
- `[RelayCommand]` or `AsyncRelayCommand` for user intent
- `ObservableObject` as the default base when validation is not needed
- `ObservableValidator` when validation and error reporting matter
- `IMessenger`, `WeakReferenceMessenger`, or `ObservableRecipient` when decoupled communication is needed

This reduces boilerplate and keeps view models focused on behavior and state instead of ceremony.

## Where Logic Goes

- View model. Presentation logic, application state, commands, validation, and data shaping for the screen
- View. XAML structure, templates, visual states, triggers, and purely visual transformations
- Model. Domain rules, persistence-facing types, service integrations, and core business behavior
- Behavior or attached property. Reusable UI interactivity such as focus management, drag-and-drop, event bridging, or view-specific interaction patterns that should not live in a single view model

If a decision exists only because of the UI's appearance or composition, it usually belongs in the view layer. If it exists because of workflow, state, or user intent, it usually belongs in the view model or model.

## Validation And Presentation Shaping

Validation belongs here because it is part of how the presentation layer exposes user-editable state:

- Keep validation rules coherent with the binding and editing experience
- Prefer `INotifyDataErrorInfo`-friendly patterns when asynchronous or multi-field validation matters
- Keep validation messages and UI state separate from raw domain services where possible
- Shape domain data into presentation-friendly state instead of forcing the view to reconstruct it through fragile binding graphs

## Binding Discipline

Bindings are not just a data transport mechanism. They define the architecture of the view:

- Set a coherent `DataContext` boundary
- Bind commands for user intent
- Prefer strongly understandable binding paths
- Use converters sparingly and keep them UI-focused
- Use `DataTemplate`s to map view models to views declaratively
- Let commands and binding updates drive the UI instead of imperative event code

## Smells

- Fat code-behind that mutates application state in `Click`, `Loaded`, or `SelectionChanged` handlers
- Manual `INotifyPropertyChanged` and ad hoc command boilerplate in projects already using CommunityToolkit.Mvvm
- View models exposing `Visibility`, `Brush`, `UIElement`, or other concrete UI types when a boolean, enum, or presentation property would keep the boundary cleaner
- Long-lived event subscriptions that outlive the view model and create leaks
- View models that know about named controls or specific view implementations
- Converters doing business logic instead of view shaping

## Goal

Use WPF binding and modern MVVM patterns to create a modular, testable, and scalable architecture where application behavior is decoupled from visual representation and the UI stays declarative.
