---
name: dependency-properties
version: 1.1
---

# Dependency Properties

## Use This Reference When

- Creating a custom control or extending an existing one in code
- Exposing bindable state to XAML
- Participating in styling, animation, templating, or value inheritance
- Adding control capabilities that should feel native to WPF

## Veteran Expert Stance

Dependency properties are the backbone of WPF's rich property system. They store values in the framework's property store rather than as ordinary fields, which enables binding, styling, animation, value precedence, inheritance, and templating behavior without forcing every control instance to carry heavyweight field state.

Use a dependency property when the value should support one or more of these:

- Data binding
- Styling and templating
- Animation
- Property value inheritance
- Dynamic resources
- Metadata-driven layout or render invalidation
- Designer and XAML visibility as part of the control's public surface

If the value is purely internal state that consumers should never bind to, style, animate, or set from XAML, use a normal CLR property or a private field instead.

If the state should be externally readable and bindable but only internally writable, use a read-only dependency property.

## What Good DP Design Looks Like

- Immaculate CLR wrappers. The wrapper should do nothing except call `GetValue` and `SetValue`.
- Correct registration and naming. The field should be a `public static readonly DependencyProperty` named with the exact property name plus the `Property` suffix.
- Smart metadata. Use `PropertyMetadata` or `FrameworkPropertyMetadata` to define default values, callbacks, coercion behavior, binding defaults, and framework-level invalidation behavior where appropriate.
- Native-feeling API design. The property name, type, and semantics should feel like they belong beside the built-in WPF property set.
- Clear ownership. The property should live on the control or attached surface where the concept actually belongs.

## Practical Heuristics

- Put change logic in `PropertyChangedCallback`, never in the CLR wrapper.
- Use `CoerceValueCallback` when one property constrains another, such as keeping a current value within `Minimum` and `Maximum`.
- Use `ValidateValueCallback` when the value should be rejected globally before it even reaches per-instance metadata processing.
- Put default values in metadata, not in the constructor.
- Use `FrameworkPropertyMetadata` when flags such as `AffectsMeasure`, `AffectsArrange`, `AffectsRender`, `BindsTwoWayByDefault`, or `Inherits` matter.
- Use read-only dependency properties for internal state that templates, triggers, or bindings should still observe.
- Keep metadata callbacks focused. They should synchronize control state, invalidate dependent values, or update visual behavior, not run application workflow logic.
- If multiple properties interact, think carefully about callback order, coercion, and re-entrancy so the control remains predictable.
- Use `AddOwner` when an existing dependency property concept should participate on a new type without inventing a parallel property surface.
- Override metadata on inherited dependency properties when a derived control needs different defaults or framework behavior instead of re-registering the concept.

## Read-Only Dependency Properties

Read-only dependency properties are the right tool when a control owns the state but the outside world still needs to observe it.

- Register them with `DependencyProperty.RegisterReadOnly`
- Keep the resulting `DependencyPropertyKey` private or tightly scoped
- Expose the public `DependencyProperty` for binding, styling, and triggers
- Update the value only from within the control using the key

This is appropriate for control-owned state such as computed status, visual mode, or interaction-derived state that should not be set externally.

## Attached Versus Standard Dependency Properties

Always ask where the concept really lives:

- Use a standard dependency property when the value is intrinsic to one control type
- Use an attached dependency property when the behavior or metadata can sensibly apply to many unrelated element types

Attached properties are often the right answer for layout participation, attachable interaction features, drag-and-drop helpers, focus behavior, or cross-cutting UI capabilities.

If the feature is a reusable modifier on arbitrary elements, `RegisterAttached` is usually the correct design.

## Metadata-Driven Design

The strongest WPF control authors lean on metadata instead of fighting the framework:

- Use default values so every instance starts from a coherent baseline
- Use metadata flags instead of manual invalidation where possible
- Use coercion to enforce invariants through the property system itself
- Use callbacks to synchronize related state when the property system changes values through binding, styling, animation, or templates
- Understand property value precedence so local values, bindings, styles, templates, animations, coercion, and defaults do not surprise you
- Remember that default style behavior for custom controls is also metadata-driven through `DefaultStyleKey`

The more your design works with the property system, the more native and reliable the control feels.

## Novel Control Work

When creating new control capabilities, think in terms of native WPF affordances:

- Should this be bindable from XAML
- Should styles be able to set it
- Should templates react to it
- Should animations target it
- Should a parent surface be able to influence it declaratively

If the answer is yes to any of these, a dependency property is often part of the correct design.

This is also how existing controls can be deeply permuted in a native-feeling way. If a control gains new bindable behavior, editable state, or templatable configuration and still feels like a first-class WPF citizen, dependency properties are usually carrying that contract.

## Smells

- Logic in CLR wrappers such as validation, event raising, or side effects
- Setting dependency property defaults in the constructor instead of registration metadata
- Incorrect backing field naming that breaks WPF conventions and tooling expectations
- Manually calling `InvalidateMeasure`, `InvalidateArrange`, or `InvalidateVisual` when metadata flags would express the intent more accurately
- Using dependency properties to store sensitive data that should not live in the public property system
- Callbacks that mutate large parts of the control tree or trigger hard-to-follow recursive property changes
- Choosing a normal dependency property when the concept is really an attached capability
- Re-registering a property concept instead of using `AddOwner` or metadata override where the property system already provides the right extension path

## Goal

Plug custom control state and configuration cleanly into the native WPF ecosystem so the resulting API fully participates in binding, styling, templating, and animation while remaining efficient, predictable, and idiomatic.
