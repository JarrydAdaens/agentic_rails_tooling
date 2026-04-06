---
name: custom-control-authoring
version: 1.1
---

# Custom Control Authoring

## Use This Reference When

- Building a reusable control library rather than a one-off composed view
- Authoring controls that should be fully restylable through `ControlTemplate`
- Wiring `DefaultStyleKey`, `Generic.xaml`, named parts, or `OnApplyTemplate` to establish a control's visual contract
- Defining control states, automation peers, and default theme behavior so the custom control feels native, robust, and accessible in the WPF ecosystem

## Veteran Expert Stance

Custom control authoring is the practice of building true lookless controls by separating behavioral logic completely from visual representation.

Rather than locking visuals down inside a `UserControl`, you build a `Control` derivative that defines a strict contract of expected visual parts and states, allowing consuming developers to radically re-template the UI without breaking the core functionality.

## Full Lifecycle

The typical lifecycle is:

1. Class definition. Derive from `Control` or a more specific base such as `RangeBase` or `ItemsControl`. Add `[TemplatePart]` and `[TemplateVisualState]` attributes to define the control contract.
2. Metadata override. In the static constructor, call `DefaultStyleKeyProperty.OverrideMetadata` to tell WPF to look for the control's default style.
3. Theme definition. Define the default `ControlTemplate` and visual states inside `Themes\\Generic.xaml`.
4. Template application. Override `OnApplyTemplate` to extract named parts via `GetTemplateChild()`. Wire internal event handlers and unsubscribe from previous parts first.
5. State management. Intercept property changes and user input, and use `VisualStateManager.GoToState()` to orchestrate visual transitions.
6. Automation. Override `OnCreateAutomationPeer` to return a custom `AutomationPeer` for accessibility and UI testing.

## Core Building Blocks

- Dependency properties. The bindable and animatable properties that hold the control's configuration and state.
- `Themes\\Generic.xaml`. The framework-level resource dictionary where the fallback `Style` and `ControlTemplate` for the control live.
- `ControlTemplate`. The XAML blueprint defining the visual tree. It should use `TemplateBinding` or templated-parent bindings to map internal visuals to the control's public properties.
- Visual states and state groups. Defined in the template to dictate how the control visually reacts to logical states such as `MouseOver`, `Pressed`, `Focused`, or `Disabled`.
- Named parts. Specific expected elements inside the template that the C# code needs to interact with.

These pieces should remain loosely coupled and fault-tolerant. The control's logic should continue to execute safely even if a consumer rewrites the `ControlTemplate` and omits some or all named parts or visual states.

## Practical Heuristics

- Attribute the contract. Use `[TemplatePart]` and `[TemplateVisualState]` attributes on the class so template authors and tools can understand the control's expectations.
- Manage event subscriptions carefully. In `OnApplyTemplate`, detach from any previously captured parts before acquiring and wiring new ones.
- Check for nulls. `GetTemplateChild()` can legally return `null` when a consumer omits a part.
- Use `TemplateBinding` or `RelativeSource TemplatedParent` to flow public control properties into the default template.
- Keep behavior in the control and visuals in the template.
- Prefer state transitions through `VisualStateManager.GoToState()` instead of mutating visual properties directly in code.
- Ensure the control has a sensible default template so it is usable immediately when dropped into XAML.

## Default Style Lookup

Default style resolution is how WPF automatically finds and applies the out-of-the-box look for a custom control.

- `DefaultStyleKey` override. Override `DefaultStyleKeyProperty` metadata in the control's static constructor to point at `typeof(YourControl)`.
- `Generic.xaml`. WPF searches the control assembly's `Themes` folder for a theme-specific dictionary first and falls back to `Generic.xaml`.
- `ThemeInfoAttribute`. The assembly should define `ThemeInfo` so WPF knows where theme-specific and generic dictionaries live.

If this wiring is wrong, the control may render invisibly, inherit the wrong visuals from a base class, or fail when moved into another project or assembly.

## Template Parts And States

Named parts and visual states are how a reusable control exposes structured expectations to templates:

- Use the `PART_` prefix for named elements required by control logic.
- Keep the list of required parts as small as possible.
- Group mutually exclusive states into `VisualStateGroup`s such as `CommonStates`, `FocusStates`, or `ValidationStates`.
- Drive visual changes through `VisualStateManager.GoToState(this, "StateName", useTransitions)` rather than manually changing `Brush`, `Opacity`, or transforms in code.
- Let the template own how a state looks, while the control owns when that state is active.

## Automation And Accessibility

Reusable controls should be first-class citizens for screen readers, assistive technologies, and automated UI testing.

- Override `OnCreateAutomationPeer` and return a peer based on the closest meaningful base peer type.
- Override core peer methods such as `GetClassNameCore`, `GetAutomationControlTypeCore`, and `IsControlElementCore` so the control presents itself correctly in the automation tree.
- Implement patterns through `GetPatternCore` when the control behaves like an invokable, expandable, selectable, or value-bearing control.
- Raise automation events or property-changed notifications from the automation peer when important state changes occur.
- Preserve keyboard interaction, focus behavior, and semantic clarity even when the template changes radically.

## Smells

- Deriving from `UserControl` when the real goal is a reusable, restylable control primitive
- Throwing or crashing because `GetTemplateChild()` returned `null`
- Manipulating colors, opacity, or other visuals directly in code instead of transitioning via `VisualStateManager`
- Missing `DefaultStyleKey` override and then wondering why the control is invisible or styled like its base type
- Requiring so many parts that the control becomes fragile to re-template
- Accessibility behavior disappearing once the default template is replaced

## Goal

Construct highly flexible lookless custom components that supply rich behavior, native WPF bindings, and complete accessibility while allowing designers and consuming developers wide freedom to redesign the visual tree through `ControlTemplate`.
