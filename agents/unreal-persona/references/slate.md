---
name: slate
version: "1.0"
---

# Slate UI Framework

## Use This Reference When
- Writing custom editor tooling, detail panels, or property customizations in C++
- Implementing a custom SWidget subclass for editor or runtime use
- Diagnosing Slate rendering, invalidation, or attribute-binding issues
- Auditing code that mixes Slate and UMG, or that places Slate in runtime modules

## Veteran Expert Stance
Slate is a fully immediate-mode UI framework dressed in a declarative construction syntax. There is no retained scene graph in the sense of a DOM — every visible widget repaints every frame via OnPaint. The declarative SNew() construction syntax is syntactic sugar over a builder pattern; it constructs the widget tree once, then Slate drives it through attribute polling and explicit invalidation. Understanding this distinction is the key to avoiding both performance problems (over-invalidating, doing expensive work in attribute getters) and correctness problems (expecting the tree to update automatically when no attribute is polling for a change).

The TSharedPtr/TSharedRef ownership model is completely separate from UObject GC. Slate widgets are reference-counted C++ objects. Storing one in a UPROPERTY does nothing useful — the GC does not track it, and the widget will be kept alive or destroyed purely by TSharedPtr reference counts. Conversely, a SWidget that is owned only by the Slate tree will be destroyed when it is removed from the tree, which is frequently surprising when an outer scope holds a raw pointer. Always hold a TSharedPtr to any widget you need to reference after construction, and hold a TWeakPtr when you need to query existence without extending lifetime.

The editor/runtime boundary is a hard architectural line. Slate and SlateCore are editor modules in the module dependency sense — they can be loaded in editor builds but including them in a runtime module creates a packaging failure on non-editor targets. Runtime game UI belongs in UMG, which provides the SObjectWidget bridge between the UObject world and the Slate tree. Custom editor tooling — detail panels, asset editors, toolbar extensions — lives in editor modules that declare a dependency on Slate, SlateCore, and (for property editing) PropertyEditor.

## Core Concerns
- Ownership model: TSharedPtr/TSharedRef, not UObject GC
- Attribute vs Argument: live-updating bound values vs one-time construction values
- Immediate-mode rendering: OnPaint fires every frame, attribute getters should be cheap
- Editor/runtime module boundary: Slate is not available in packaged runtime modules
- Widget class hierarchy: SLeafWidget, SCompoundWidget, SPanel for single, one-child, multi-child
- Invalidation discipline: explicit Invalidate() calls required when state changes outside attribute polling

## Practical Heuristics

1. Use TSharedRef when a widget must not be null. Use TSharedPtr when the widget may be absent or conditionally constructed. Use TWeakPtr when you need to observe a widget without extending its lifetime — common in editor callbacks and async operations.

2. Never store a SWidget pointer in a UPROPERTY. UObject reflection does not understand TSharedPtr, and the field will not participate in GC tracking. It also will not appear correctly in memory profiling.

3. SLATE_BEGIN_ARGS / SLATE_END_ARGS defines the named argument struct. Every SWidget subclass that accepts construction arguments must declare this pair. Arguments are set once at SNew() time and do not update after construction.

4. SLATE_ARGUMENT(Type, Name) declares a plain value argument. It is copied at construction time. Use for values that are set once and do not change: text, initial sizes, flags.

5. SLATE_ATTRIBUTE(Type, Name) declares a TAttribute<Type> argument. It can wrap either a plain value or a getter delegate. If a getter delegate is bound, Slate polls it on every relevant tick or paint. Use for values that must reflect live game state: health, ammo, timer countdowns.

6. TAttribute<FText>::Create with a UObject getter:
   ```cpp
   TAttribute<FText>::Create(
       TAttribute<FText>::FGetter::CreateUObject(this, &UMyClass::GetLabel)
   )
   ```
   The getter runs on the game thread during Slate's pre-pass. Keep it O(1). Do not allocate, lock, or do I/O inside a TAttribute getter.

7. SLeafWidget: no children, implements OnPaint directly. Use for custom-drawn primitives, icons, simple text. Must implement ComputeDesiredSize.

8. SCompoundWidget: exactly one child slot. Use when you are wrapping a single subtree with additional logic or custom input handling. The child is set via ChildSlot inside Construct().

9. SPanel: arbitrary number of named child slots. Use when building layout containers (horizontal box, grid, overlay). Must implement OnArrangeChildren and ComputeDesiredSize.

10. SBox is a fixed-size constraint wrapper — use to enforce width, height, min/max. SOverlay stacks children with ZOrder. SHorizontalBox and SVerticalBox distribute children along an axis with slot padding and fill ratios. These four containers cover the vast majority of layout needs.

11. OnPaint receives a FPaintGeometry and FSlateRect clip region. Draw calls are batched by Slate's renderer — do not assume draw order within a single widget's OnPaint implementation. Return the highest LayerId used.

12. Explicit invalidation is required when widget state changes outside an attribute getter. Call:
    - `Invalidate(EInvalidateWidgetReason::Layout)` when size or arrangement changes.
    - `Invalidate(EInvalidateWidgetReason::Paint)` when only visual appearance changes.
    - `Invalidate(EInvalidateWidgetReason::LayoutAndVolatility)` when volatility changes.
    Failing to invalidate means Slate will not repaint the widget, and the old visual persists.

13. Custom detail panels implement IDetailCustomization. Register them in the editor module's StartupModule via:
    ```cpp
    FPropertyEditorModule& PropertyModule =
        FModuleManager::LoadModuleChecked<FPropertyEditorModule>("PropertyEditor");
    PropertyModule.RegisterCustomClassLayout(
        UMyClass::StaticClass()->GetFName(),
        FOnGetDetailCustomizationInstance::CreateStatic(&FMyClassCustomization::MakeInstance));
    ```
    Unregister in ShutdownModule. Failing to unregister produces crashes on hot reload.

14. IDetailCustomization::CustomizeDetails receives an IDetailLayoutBuilder. Use it to hide categories, reorder properties, and insert custom rows via AddCustomRow. Prefer AddProperty over manual widget construction when you only need to reorder or annotate existing properties.

15. Custom property type customizations implement IPropertyTypeCustomization and are registered with RegisterCustomPropertyTypeLayout. Use these when a struct type needs bespoke editor UI across all instances of that struct type regardless of which class owns the property.

16. SObjectWidget is the bridge Slate widget that UMG uses to embed a UUserWidget into the Slate tree. Do not instantiate it directly — it is an implementation detail of UMG. Understanding it explains why UMG widgets have both a UObject side and a Slate side with separate lifetimes.

17. To invoke a Slate widget from a UMG widget's C++ side, use TakeWidget() on the UWidget subclass. This materializes the underlying SWidget. The SWidget is owned by the Slate tree; the UWidget UPROPERTY chain keeps the UObject side alive.

18. Slate input handling: override OnMouseButtonDown, OnKeyDown, OnMouseMove etc. on SWidget. Return FReply::Handled() to consume the event, FReply::Unhandled() to let it propagate. FReply also carries focus capture and mouse capture requests.

19. FSlateApplication::Get() provides access to the Slate application singleton: SetKeyboardFocus, ForEachUser, GetPlatformCursor. Use carefully in editor code; use SetUserFocus on the local player's user index in game code.

20. Volatile widgets (IsVolatile() returns true) are repainted every frame regardless of invalidation. Use sparingly — only for widgets where TAttribute polling alone is insufficient and you need per-frame repaint. Mark via SWidget::SetVolatile(true).

## Smells

- `UPROPERTY() TSharedPtr<SMyWidget> Widget;` — nonsensical, GC ignores TSharedPtr; widget lifetime is unaffected by this annotation.
- Storing a raw SWidget* anywhere — no reference count, pointer dangles when the Slate tree releases it.
- Expensive operations (file I/O, string parsing, lock acquisition) inside a TAttribute getter — runs every Slate tick on the game thread.
- `#include "Widgets/SMyWidget.h"` in a runtime module — Slate headers in non-editor modules cause packaging failures.
- Registering an IDetailCustomization in a runtime module's StartupModule — PropertyEditor is editor-only; this crashes non-editor builds.
- Calling Slate APIs directly on a non-game thread without using Async(EAsyncExecution::GameThread, ...) — Slate is not thread-safe.
- Constructing a widget with SNew inside a TAttribute getter — allocates a new widget subtree every tick.
- Forgetting to unregister a custom detail layout in ShutdownModule — produces use-after-free crashes on hot reload or editor shutdown.
- Using SIGNAL/SLOT-style string delegates instead of TAttribute for live-updating label text — values never update after initial construction.
- Implementing a custom SPanel without correctly implementing OnArrangeChildren — children render at position zero, overlap, or are clipped incorrectly.
- Using SWidget::SNew outside of a widget's Construct() without assigning the result to a TSharedRef — the constructed widget is immediately destroyed.

## Goal

Applying these patterns produces editor tooling and custom UI widgets that are correctly owned, efficiently rendered, and cleanly separated from runtime code. Detail panels and property customizations register and unregister without leaking, TAttribute bindings stay live without forcing full repaints, and the editor/runtime module boundary is never crossed.

## Boundaries

- See `umg-widgets.md` for the UObject layer above Slate — UUserWidget lifecycle, BindWidget, and viewport management.
- See `mvvm-preview-mode.md` for ViewModel-driven data binding that replaces manual TAttribute wiring in data-heavy UIs.
