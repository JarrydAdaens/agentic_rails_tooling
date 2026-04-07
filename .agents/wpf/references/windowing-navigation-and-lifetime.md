---
name: windowing-navigation-and-lifetime
version: 1.1
---

# Windowing, Navigation, and Lifetime

## Use This Reference When

- Designing startup, shutdown, or application shell behavior, including command-line handling or session-ending behavior
- Working with windows, dialogs, owned windows, or popups at the app-flow level
- Choosing modal versus modeless interactions
- Building navigation flows, frame-based shells, or view-model-driven screen transitions while preserving MVVM boundaries

## Veteran Expert Stance

Desktop application quality depends on treating the application shell, windowing lifecycle, and navigation as first-class architectural concerns that are separate from individual view logic.

WPF works best when startup is deliberate, the shell is a stable host for dynamic content, and window or navigation transitions are driven through MVVM-friendly services instead of ad hoc code-behind window creation.

## Core Concerns

- Application lifetime and startup. Startup may need to parse command-line arguments, initialize dependency injection, restore session state, or choose a startup path before showing the main shell.
- Shell pattern. A shell window usually owns fixed chrome such as menus, toolbars, navigation, and status surfaces while hosting dynamic content regions.
- Owned windows. The `Owner` relationship defines real desktop behavior such as Z-order, minimizing, and close behavior.
- Modal versus modeless interaction. These are workflow decisions, not just API choices.
- Shutdown and session ending. Application teardown needs explicit rules, especially when unsaved work or long-running operations exist.

## Practical Heuristics

- Use `Application.Startup` when application bootstrapping needs more control than a simple `StartupUri`.
- Choose `ShutdownMode` deliberately based on whether the app should close with the main window, the last window, or only under explicit shutdown.
- Handle session-ending scenarios when the product must protect user data or save state during OS logoff or shutdown.
- Keep the shell itself thin. It should host layout regions and bind to a shell view model rather than owning application behavior directly.
- Keep navigation decisions in presentation architecture rather than scattering them through event handlers or view construction code.
- Set `Owner` on secondary windows that conceptually belong to a primary workflow so they minimize, stack, and close predictably.
- Use modal dialogs sparingly. Prefer them when the user truly cannot continue without resolving the interaction.
- Prefer modeless windows or panels when the workflow benefits from comparison, reference, or ongoing interaction with the main surface.

## Shell Pattern

The shell is the desktop equivalent of a durable application frame:

- Fixed UI such as menus, toolbars, navigation, and status regions belong in the shell
- Dynamic content should be hosted through regions, content presenters, or view-model-driven content swapping
- The shell should remain compatible with theming and template-driven composition
- The shell view model should orchestrate presentation flow, not own domain logic

Good shell design makes large WPF applications much easier to evolve.

## ViewModel-Driven Navigation

Navigation should remain testable and MVVM-compatible:

- Keep navigation decisions in view models or application services, not button click handlers
- Use a navigation abstraction rather than exposing raw `Frame` or `Window` APIs directly to view models
- Allow navigation rules to account for validation, unsaved changes, security, or workflow state
- Consider lifecycle hooks such as `OnNavigatedTo` and `OnNavigatedFrom` when views or view models need controlled activation and deactivation

The more the app flow depends on business state, the more important it is that navigation be abstracted and testable.

## Dialog And Popup Discipline

Dialogs are workflow tools, not convenience shortcuts:

- Do not call `MessageBox.Show()` or instantiate windows directly from view models
- Use an interaction or dialog service so the view model can request an interaction without knowing the concrete UI
- Distinguish between transient overlays, true dialogs, owned windows, and full navigation transitions
- Choose the lightest interaction surface that preserves clarity and user control

## Navigation Patterns

Different apps want different navigation styles:

- State-based navigation. Existing visuals change state without replacing the hosted view. This works well for local mode changes, overlays, and contextual display changes.
- View-based navigation. One view is replaced by another inside a region, shell host, or frame. This works well for feature transitions, wizards, or major workflow shifts.
- Multi-window navigation. Distinct workflows live in separate windows, often with ownership relationships.

Choose state-based navigation for localized layout or mode transitions, and view-based navigation when the user is moving between clearly different application surfaces.

## Smells

- Creating and showing windows directly inside button handlers or view models
- Overusing modal dialogs that block the rest of the workflow unnecessarily
- Modeless windows opened without an `Owner`, leading to lost or orphaned windows
- Startup logic buried across multiple code paths with no clear application entry discipline
- Navigation implemented as arbitrary control swapping in code-behind
- Heavy views kept alive forever after navigation because lifetime and deactivation were never designed

## Goal

Build WPF application architectures where startup and shutdown are robust, the shell acts as a flexible host for dynamic presentation, and screen transitions are orchestrated through testable, view-model-friendly navigation and interaction services.
