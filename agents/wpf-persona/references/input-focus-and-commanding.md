---
name: input-focus-and-commanding
version: 1.1
---

# Input, Focus, and Commanding

## Use This Reference When

- Wiring keyboard shortcuts, access keys, or routed commands to ensure a keyboard-friendly and accessible application
- Fixing focus behavior, tab order, focus scopes, or keyboard navigation
- Deciding between direct event handling, behaviors, and routed commanding in an MVVM architecture
- Ensuring pointer interaction and keyboard interaction have equivalent behavior

## Veteran Expert Stance

Great WPF interaction relies on semantic intent over device-specific events. It separates what the user wants to do from how they initiated it.

A robust UI treats the keyboard as a first-class citizen and leans on WPF's focus and commanding infrastructure instead of scattering fragile `KeyDown`, `MouseDown`, or `Click` event handlers through code-behind.

## Core Layers

- Keyboard focus versus logical focus. Keyboard focus is the one element currently receiving keyboard input. Logical focus is the remembered focused element within a focus scope.
- Commanding model. Command, command source, command target, and command binding form the native routed-command architecture.
- Behaviors. Encapsulated interaction logic attached in XAML that can bridge routed events to commands without altering a control's structure.

## Practical Heuristics

- Use access keys intentionally. Underscore-based access keys can make desktop workflows dramatically faster.
- For input controls without textual content, put the access key on a `Label` and connect it through `Target`.
- Explicitly manage tab order in complex forms. Use `TabIndex` when the default visual order is not enough, and apply `IsTabStop="False"` aggressively to decorative or non-actionable elements.
- Use `InputBindings` and `KeyBinding` for keyboard shortcuts instead of hand-rolled key event logic when the action is truly command-like.
- Use `KeyboardNavigation` attached properties to constrain or cycle focus intentionally inside dialogs, menus, and composite containers.
- Keep pointer and keyboard interaction equivalent. Hover-only or click-only behavior is incomplete if there is no keyboard path to the same outcome.

## Focus Discipline

Focus issues often come from confusing keyboard focus with logical focus or trying to set focus before the element is ready.

- Set initial focus only after the target element is in the visual tree and visible.
- Use `Loaded` or a deferred dispatcher callback when startup focus must be applied programmatically.
- Understand that focus scopes preserve logical focus even when keyboard focus moves elsewhere temporarily.
- Remember that menus, toolbars, context menus, and similar surfaces can change focus behavior in ways that are correct but surprising if you do not think in scopes.

Good focus discipline prevents "input goes nowhere" bugs and preserves editing context across composite UI.

## Behaviors Versus Routed Commanding

- Use routed commands when the action is truly coupled to focus, the element tree, or native WPF command handling. Clipboard and text editing commands are classic examples.
- Use MVVM commands plus behaviors when the command belongs to the view model and should not depend on visual-tree routing.
- Use behaviors such as event-to-command bridging when a control exposes a useful routed event but not a direct command surface.
- Prefer commands and behaviors over code-behind handlers when the behavior changes application state.

Routed commands are powerful, but they are not the right default for all business actions.

## Access Keys, Shortcuts, and Navigation

Keyboard usability is more than tabbing:

- Access keys accelerate dense desktop interfaces
- Shortcuts map recurring expert actions to gestures
- Focus scopes preserve context inside complex surfaces
- Tab behavior should match the user's mental workflow, not just the markup order

These concerns are part of the interaction model, not small polish items.

## Smells

- Non-interactive elements participating in the tab order
- Business logic implemented as routed commands when the real behavior belongs in a view model command
- Code-behind event handlers mutating application state in an MVVM screen
- Arbitrary `KeyDown` handling for behavior that should be a key binding, command, or behavior
- Focus visuals removed without an accessible replacement
- Reflection-based method-call behaviors used to avoid proper command design
- Commands that mysteriously enable or disable based on visual-tree routing side effects the architecture never meant to depend on

## Goal

Build accessible, keyboard-friendly, and maintainable WPF interaction models where user intent is cleanly expressed through commanding and behaviors, focus transitions feel natural, and business logic stays decoupled from the visual tree.
