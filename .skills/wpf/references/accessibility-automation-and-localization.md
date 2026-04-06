---
name: accessibility-automation-and-localization
version: 1.1
---

# Accessibility, Automation, and Localization

## Use This Reference When

- Making a control or view keyboard-first and screen-reader friendly
- Adding automation properties or custom automation peers for testability and assistive technology
- Designing for high contrast, scalable layout, or readable focus cues
- Making UI text, formatting, and layout behave correctly across cultures and languages

## Veteran Expert Stance

True premium UI is usable by everyone, regardless of physical ability, locale, or preferred input method. Treat accessibility, UI automation, and localization as architectural requirements, not cleanup work.

WPF provides strong native infrastructure for these concerns. Use WPF-native mechanisms such as automation peers, dynamic layout, adaptable resources, and culture-aware presentation to build interfaces that remain usable, testable, and understandable under real-world variation.

## Core Concerns

- Keyboard and focus management. Every interactive element should be reachable through the keyboard, and focus state should be visually obvious. Avoid focus traps.
- UI Automation tree. Assistive technologies and UI automation frameworks see the app through the automation tree, not the visual tree.
- Localization and culturally aware layout. Avoid hardcoded sizes, strings, and directional assumptions. The UI must adapt to text expansion, formatting differences, and right-to-left flow where needed.

## Practical Heuristics

- Design keyboard-first. Establish a logical tab order using `TabIndex` and `IsTabStop`, and make sure keyboard flow matches the intended workflow.
- Use access keys intentionally. Underscore-based access keys can make dense desktop UIs substantially more efficient.
- Set automation properties deliberately. Use `AutomationProperties.Name` for controls that lack visible text, and prefer `AutomationProperties.LabeledBy` when a visible label already exists so the spoken label stays synchronized with the UI.
- Implement custom automation peers for meaningful custom controls by overriding `OnCreateAutomationPeer` and supplying the correct peer behavior.
- Override automation peer core methods such as `GetClassNameCore` and `GetAutomationControlTypeCore` so assistive tech can identify the control accurately.
- Prune the automation tree when needed. Decorative or purely structural elements should not pollute the meaningful control surface exposed to assistive technologies.
- Use dynamic layout for localization. Prefer layout panels and auto-sizing over fixed dimensions when text or culture can change.
- Support right-to-left scenarios by treating `FlowDirection` as a real layout concern, not a late-stage patch.
- Bind user-facing strings to localizable resources rather than hardcoding text in the XAML or code.

## Keyboard And Focus Discipline

Keyboard credibility is not optional in mature desktop UI:

- Interactive elements should be reachable in a sensible order
- Focus should remain visible, high-contrast, and easy to track
- Composite controls should not trap the user
- Pointer-only affordances should have keyboard equivalents

If the UI works well only with a mouse, it is incomplete.

## Automation Tree Quality

A good automation surface should:

- Expose meaningful names and control types
- Implement the right patterns for invocation, toggle, selection, value, or range behavior
- Reflect important state changes to assistive technologies
- Avoid flooding users with decorative or redundant noise

The automation tree is both an accessibility surface and a testability surface.

## Localization And Culture

Localization is more than translating strings:

- Text expansion changes layout pressure
- Formatting changes dates, numbers, and currency
- Cultures may require different reading direction
- Labels, shortcuts, and spacing assumptions may need to adapt

Localized UI should be designed to flex rather than break.

## High Contrast And Adaptability

Premium design still needs to survive hostile conditions:

- Respect system colors and theme variation when high-contrast support matters
- Maintain usable contrast ratios for text and important surfaces
- Do not rely on color alone to communicate state
- Make sure typography and layout can scale with user settings
- Preserve visible focus cues even in heavily customized templates

## Smells

- Fixed widths or heights on text-bearing UI that clip under translation
- Redundant automation names such as appending the control type manually to a label
- Non-interactive elements participating in tab order
- Focus visuals removed without a strong accessible replacement
- Using `Opacity="0"` to "hide" content that should actually leave the visual and automation surface
- Hover-only actions with no keyboard path
- Custom controls with no meaningful automation surface
- Hardcoded strings and culture assumptions embedded directly in UI code

## Goal

Build inclusive, global-ready WPF applications where keyboard navigation is predictable, the automation tree accurately describes intent and state, and the UI adapts gracefully across languages, themes, and assistive technology.
