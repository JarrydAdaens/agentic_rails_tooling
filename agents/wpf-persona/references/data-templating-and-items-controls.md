---
name: data-templating-and-items-controls
version: 1.1
---

# Data Templating and Items Controls

## Use This Reference When

- Building list, grid, tree, menu, or repeated-item UI using an `ItemsControl` or one of its derivatives
- Choosing between `DataTemplate`, `ItemContainerStyle`, and custom item containers to customize presentation
- Using `CollectionViewSource`, grouping, sorting, or filtering large collections of data
- Tuning item-template complexity, container generation, or virtualization behavior to optimize rendering and memory performance

## Veteran Expert Stance

WPF's item controls are powerful because they separate data shape from visual appearance and layout. Highly performant and scalable lists come from respecting UI virtualization, preventing unnecessary container generation, and delegating sorting and filtering logic to collection views rather than manipulating the visual tree directly.

## Core Layers

- Items panel template. Defines the panel that lays out the children, such as `VirtualizingStackPanel` or `WrapPanel`.
- Item container style. Styles the UI container that wraps each item, such as `ListBoxItem`, `TreeViewItem`, or `ListViewItem`.
- Data template. Defines the visual tree for the data item itself.
- Collection view. Owns sorting, grouping, filtering, and current-item behavior at the presentation layer.

When one of these layers is configured incorrectly, you can easily cripple virtualization, inflate object count, or break hit-testing and selection behavior.

## Practical Heuristics

- Use `DataTemplate` for the item's visuals.
- Use `ItemContainerStyle` for selection chrome, focus behavior, padding, alignment, and per-container state.
- Use `ItemsPanelTemplate` to control layout behavior and virtualization compatibility.
- Use `HierarchicalDataTemplate` for nested collections such as `TreeView` data of arbitrary depth.
- Use `DataTemplateSelector` only when the collection is truly heterogeneous and item types need materially different layout structures. For minor visual variations, prefer bindings, triggers, or state inside one template.
- Keep item templates shallow. Virtualization helps count, not per-item cost.
- If a complex template is causing realization jank, consider phased rendering strategies rather than immediately deepening the template further.
- In rare cases where a list is relatively small but each item is extremely expensive to realize and destroy, evaluate whether disabling virtualization is actually smoother. Treat this as an exception, not a default.

## Grouping, Sorting, And Filtering

Collection views are the native WPF place for presentation-specific collection behavior:

- Expose an `ICollectionView` when the view model needs to control filtering, grouping, sorting, or current-item behavior without knowing about controls.
- Sort at the view layer when ordering is presentation-specific.
- Group at the view layer when visual grouping is a UI concern.
- Filter at the view layer when the filter belongs to the screen or workflow rather than the domain collection itself.
- Use live shaping when the UI genuinely needs items to reposition automatically as properties change and the underlying view implementation supports it.

The collection view is part of presentation architecture, not an afterthought.

## Virtualization Interactions

Virtualization defers container generation and layout until an item becomes visible, which is mandatory for large datasets.

- Prefer virtualizing panels where supported.
- Enable container recycling when available for long-lived scrolling surfaces.
- Do not disable virtualization accidentally by using incompatible panels, nested scroll viewers, mixed container types, direct container insertion, or `CanContentScroll="False"`.
- Remember that `ItemContainerGenerator.ContainerFromIndex()` can return `null` for unrealized items in a virtualized list. Interact with the data item whenever possible rather than relying on the visual container.
- Be careful with grouping, because it can affect virtualization behavior depending on the control and layout combination.

## Container Generation And State

Containers are transient implementation details in many virtualized surfaces:

- Do not store durable logical state only on the container.
- Keep state such as expansion, selection intent, or workflow flags on the data item or view model.
- Expect recycled containers to be reused for different data items.
- Treat container generation cost as a real performance factor alongside template complexity.

## Smells

- Building repeated item UI by manually adding controls in code
- Replacing a virtualizing panel with a regular `StackPanel` and accidentally realizing the entire dataset
- Pushing selection or container chrome into the data template instead of the item container
- Massive item templates with deep panel nesting and many bindings
- Using `DataTemplateSelector` where a small number of typed templates, bindings, or triggers would be clearer
- Binding durable logical state to the container instead of the data item, which breaks badly under recycling
- Treating grouping, sorting, or filtering as imperative collection rebuilding
- Hooking `SelectionChanged` in code-behind when `SelectedItem`, `CurrentItem`, or commands would keep the interaction declarative

## Goal

Build highly performant, decoupled item-driven WPF surfaces where data presentation stays declarative, large datasets remain smooth through disciplined virtualization and recycling, and sorting, filtering, and selection logic stay out of the visual tree.
