# WPF Feature Guides

Use this reference only for the feature type being harvested.

## Configuration Systems

When harvesting configuration:

- identify where settings are stored and how defaults are created
- check AppData folder names, file names, JSON shape, versioning, and migration behavior
- remove derived-app-specific keys
- preserve extensibility so future derived apps can add settings safely
- keep JSON if that is the established WPF-Starter pattern
- reconcile with `AppSettings`, `IAppSettingsService`, `AppSettingsService`, configuration view models, and shell theme state when present
- document extension points in `Documentation/wpf-starter-inventory.md`

Ask before changing persisted schema strategy, default AppData folder naming, or major compatibility behavior.

## Shared Projects

When harvesting shared-project changes:

- inspect all source and destination `.sln` and `.csproj` files
- determine whether each source shared project is genuinely reusable
- add missing shared projects only when the feature requires them
- keep WPF-free logic in shared projects and WPF-specific code in WPF projects
- update project references deliberately
- avoid assuming the starter will only ever have one front end or one shared library

Ask before restructuring assemblies, moving namespaces broadly, or merging large project trees.

## UI Controls And XAML

When harvesting controls, views, resources, or templates:

- copy only generic controls, styles, templates, converters, behaviors, and resources that belong to the feature
- remove app-specific visual branding unless it is intentionally becoming a starter default
- preserve binding correctness, accessibility, and resource lookup behavior
- verify merged resource dictionaries and dynamic resources
- avoid hidden coupling to source view models
- update the starter inventory with extension notes

Ask before replacing root shell layout, removing existing resource keys, or changing default visual identity.

## Services And Infrastructure

When harvesting services:

- prefer interfaces when they make derived extension easier
- align with WPF-Starter's DI and Generic Host conventions
- avoid concrete services that depend on source-only systems
- keep registration explicit
- document lifetime ownership and startup order
- keep cross-cutting infrastructure generic

Ask before changing bootstrap order, global service access patterns, logging architecture, or lifecycle ownership.

## Theming

When harvesting theming changes:

- compare token dictionaries, Material Design integration, theme swap code, and resource merge order
- keep token names stable where existing starter XAML consumes them
- preserve `DynamicResource` behavior for runtime theme changes
- verify light/dark or package-specific marker keys used for cleanup
- update any custom control styles that depend on new tokens

Ask before replacing broad theme dictionaries, changing default theme, or removing token keys.

## Docking And Shell Layout

When harvesting AvalonDock, shell, or pane-management changes:

- compare package versions, root layout, docking services, persisted layout format, pane reopen patterns, and theme integration
- preserve starter sample panes unless intentionally replacing them with better generic examples
- keep derived-app document/tool-pane concepts out unless they are generic examples
- verify resource dictionaries for docking chrome still load

Ask before replacing `MainWindow`, changing persisted layout format, or adding a new shell architecture.

## Packages And Dependencies

When a feature requires a dependency:

- check whether WPF-Starter already has an equivalent dependency
- prefer existing destination packages and abstractions
- add a new dependency only when it is necessary for the reusable feature
- pin versions consistently with destination project conventions
- document why the dependency is needed
- avoid dragging in source architecture through transitive convenience

Ask before adding a major third-party package, UI framework, persistence stack, hosting model, or dependency that affects future derived projects.
