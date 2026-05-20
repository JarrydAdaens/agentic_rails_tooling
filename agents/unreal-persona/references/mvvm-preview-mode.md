---
name: mvvm-preview-mode
version: "1.0"
agentic_rails_source_version: "1.0"
---

# MVVM and UMG Preview Mode

## Use This Reference When
- Implementing or auditing data-driven UI using the UMG Viewmodel plugin
- Diagnosing silent binding failures or stale widget data in ViewModel-backed UIs
- Setting up UMG preview mode with mock ViewModel data to avoid PIE dependency
- Evaluating the Lyra-pattern UI architecture for a new project's HUD system

## Veteran Expert Stance
The UMG Viewmodel plugin is not part of the engine's default feature set — it is an optional plugin that must be explicitly enabled, and its runtime behavior differs significantly from what the UMG designer suggests. The FIELD_NOTIFY system is a code-generation pipeline: the macros expand into boilerplate that wires property setters to a notification dispatcher. The contract is non-negotiable — if the backing field is mutated directly rather than through UE_MVVM_SET_PROPERTY_VALUE, the notification chain is bypassed and bound widgets never update. This is the most common silent bug in MVVM-backed UIs and the first thing to audit when a widget appears stuck at its initial value.

ViewModel lifecycle is a first-class design decision that most teams get wrong on the first pass. ViewModels are UObjects and must obey GC rules, but they also represent logical session state that outlives individual widget instances. The correct ownership pattern is for ViewModels to live on a PlayerController subsystem or GameInstance subsystem — stable, accessible, clearly scoped. Assigning ViewModels to widgets via SetViewModel (called from the widget's owning system, not from the widget itself) keeps the widget passive and the ViewModel authoritative. Widgets that create their own ViewModels in NativeConstruct are tightly coupled and untestable.

Preview mode is the practical payoff for the additional architecture overhead. A correctly configured ViewModel with preview data eliminates the requirement to PIE just to see data-driven UI changes. For teams iterating on HUD or menu layouts, this reduces the iteration loop from 20–30 seconds (compile + PIE) to the UMG designer's live preview. The investment in UE_MVVM_SET_PROPERTY_VALUE discipline and CDO-context preview setup pays back immediately. The divergence between NativePreConstruct (fires in preview) and NativeConstruct (does not) means any code that must run in preview must live in NativePreConstruct and guard against missing world state.

## Core Concerns
- Plugin enablement — the Viewmodel plugin is opt-in and not present by default
- FIELD_NOTIFY contract — notifications only fire through the generated setter, never direct field mutation
- ViewModel ownership and GC safety — must be rooted in a stable UObject chain
- ViewModel assignment — driven externally by a manager, not self-constructed by the widget
- Preview mode divergence — NativePreConstruct vs NativeConstruct fires under different conditions
- Source resolution — ViewModel lookup context (LocalPlayer, PlayerController, GameInstance, custom) set in designer

## Practical Heuristics

1. Enable the plugin in the `.uproject` file under the Plugins array:
   ```json
   { "Name": "ModelViewViewModel", "Enabled": true }
   ```
   Without this entry, UMVVMViewModelBase is undefined, and the Bindings panel in the UMG designer is absent.

2. UMVVMViewModelBase is the required base class for all ViewModels. It inherits from UObject and implements INotifyFieldValueChanged, which is the interface the binding system polls.

3. Declare a ViewModel field using the FieldNotify macro pattern:
   ```cpp
   UPROPERTY(BlueprintReadWrite, FieldNotify)
   float Health = 0.0f;
   ```
   The UPROPERTY must include FieldNotify in its metadata. Without it, the Bindings panel will not surface the field as a bindable source.

4. Implement the setter using UE_MVVM_SET_PROPERTY_VALUE:
   ```cpp
   void UMyViewModel::SetHealth(float in_newHealth)
   {
       UE_MVVM_SET_PROPERTY_VALUE(Health, in_newHealth);
   }
   ```
   This macro expands to a value-comparison check followed by assignment and a broadcast to INotifyFieldValueChanged. If the value is unchanged, the broadcast is skipped. Direct assignment (`Health = in_newHealth;`) bypasses the broadcast entirely.

5. FIELD_NOTIFY_IMPLEMENT (placed in the .cpp) generates the backing implementation for the notification dispatch. Its absence causes linker errors or silent broadcast failures depending on the engine version.

6. For computed fields (fields derived from other fields), declare a UFUNCTION(BlueprintPure, FieldNotify) and call BroadcastFieldValueChanged manually after mutating the source fields:
   ```cpp
   UE_MVVM_BROADCAST_FIELD_VALUE_CHANGED(ComputedPropertyName);
   ```

7. Assign ViewModels to widgets via the widget's UMG ViewModel Settings panel (designer) or at runtime via UMVVMView::SetViewModel. The preferred runtime pattern is an external manager — a PlayerController subsystem or HUD class — that constructs the ViewModel and calls SetViewModel on the widget after creation.

8. ViewModel source resolution in the designer's ViewModel Settings supports four contexts: LocalPlayer, PlayerController, GameInstance, and custom resolver class. Set this to the scope where the ViewModel instance actually lives. A mismatch between resolution context and actual ownership means the widget gets null and all bindings silently do nothing.

9. For preview mode, implement CreatePreviewViewModels in the ViewModel CDO context or override it in the widget's NativePreConstruct. Return an array of FMVVMViewModelContext structs mapping ViewModel class to a preview instance populated with representative data. This makes the UMG editor render the widget with real-looking values.

10. NativePreConstruct fires in editor preview and thumbnail generation — world, GameInstance, and PlayerController are all null. Any preview-mode initialization must guard against these:
    ```cpp
    void UMyWidget::NativePreConstruct()
    {
        Super::NativePreConstruct();
        if (IsDesignTime())
        {
            // Safe to access ViewModel preview data here.
            return;
        }
        // Runtime-only initialization.
    }
    ```

11. NativeConstruct does not fire during editor preview. Code that must run for the widget to display correctly in-editor must live in NativePreConstruct (with appropriate null guards), not NativeConstruct.

12. Conversion functions (FunctionBinding) in the Bindings panel map a ViewModel field of one type to a widget property of another type. The function must be a UFUNCTION on the widget or a BlueprintFunctionLibrary, returning the target property type and accepting the source field type as a parameter. Example: converting `float Health` to `FText HealthLabel` for a text block.

13. The Bindings panel supports one-way (ViewModel to Widget) and two-way (ViewModel to Widget and Widget to ViewModel) binding modes. Two-way binding is appropriate for editable fields. For display-only properties, use one-way to avoid accidental ViewModel mutation from widget state changes.

14. Binding evaluation order is not guaranteed across multiple bindings on the same widget. Do not rely on one binding having already applied when evaluating another. If display logic depends on multiple ViewModel fields, expose a computed UFUNCTION(FieldNotify) property that encapsulates the combination.

15. The Lyra HUD pattern: ULyraHUDLayout is the root widget activated via a GameFeature action. Individual feature panels are pushed onto it via the UIExtension system using UUIExtensionSubsystem::RegisterExtensionAsWidget. ViewModels are injected through the same GameFeature activation path, not hardcoded in the widget. This keeps each feature's HUD contribution isolated and independently activatable.

16. ViewModels should be constructed once per logical session scope (a match, a menu session, a player's lifetime) and reused across widget show/hide cycles. Constructing a ViewModel in NativeConstruct and destroying it in NativeDestruct throws away state on every visibility toggle, which is both wasteful and incorrect.

17. When a PlayerController is replaced (travel, respawn), ViewModels owned by the old PlayerController subsystem are destroyed. Widgets that outlive the PlayerController will hold a stale ViewModel reference. Always validate ViewModel pointers in widget code after a world transition or player controller swap.

18. For testability, construct ViewModel instances in unit tests with NewObject<UMyViewModel>() and call setters directly. The FieldNotify system fires notifications on any UObject with the interface; no engine subsystem or world is required for basic setter/notification testing.

19. Binding panel changes in the UMG designer are stored in the UMG asset, not in C++. When reviewing code, also inspect the .uasset via source control diffs or the Bindings panel in-editor. Silent binding breakage can occur when a ViewModel field is renamed without updating the asset binding.

20. When a ViewModel field rename is required, update the UPROPERTY declaration, update all callers of the setter, rebuild, then open each affected UMG asset and verify the Binding panel shows no broken (red) entries. Broken bindings are silent at runtime — the widget simply never updates.

## Smells

- Direct field assignment `ViewModel->Health = NewValue;` instead of calling the setter — bypasses FIELD_NOTIFY, bound widgets never update.
- ViewModel constructed inside NativeConstruct — tightly coupled, recreated on every show/hide cycle, incompatible with stable session state.
- ViewModel source resolution set to PlayerController when the ViewModel actually lives on GameInstance — resolution returns null, all bindings silently do nothing.
- Accessing GetWorld() or GetOwningPlayer() in NativePreConstruct without an IsDesignTime guard — crashes editor thumbnail generation.
- A UFUNCTION used as a conversion function that returns void or has the wrong parameter signature — Bindings panel accepts it at design time but produces no output at runtime.
- Missing FIELD_NOTIFY_IMPLEMENT in the .cpp — linker error or silent broadcast failure depending on engine version.
- Two-way binding on a display-only property (health bar fill amount) — widget state changes can mutate the ViewModel unexpectedly during layout passes.
- Renaming a ViewModel UPROPERTY without auditing UMG asset bindings — binding silently breaks, widget displays only its initial default value.
- ViewModel owned by the widget itself via a UPROPERTY — ViewModel is destroyed and recreated with the widget; session state is lost on every RemoveFromParent/AddToViewport cycle.
- Binding a computed property that calls GetWorld() in its body — crashes in preview context where the computed property getter is invoked by the Bindings panel.
- CreatePreviewViewModels not implemented — designers must PIE to see any data-driven content, eliminating the primary productivity benefit of the MVVM architecture.

## Goal

Correctly applied, this architecture produces a clean separation between game state (ViewModel), UI structure (Widget), and display logic (bindings and conversion functions). ViewModels update once via typed setters, notifications propagate automatically to all bound widgets, and the UMG editor previews realistic data without requiring PIE. The result is a HUD and menu system where iteration is fast, ownership is unambiguous, and feature teams can add UI contributions via GameFeature actions without modifying shared widget assets.

## Boundaries

- See `umg-widgets.md` for widget lifecycle details, BindWidget, and AddToViewport patterns that govern the widget layer above the ViewModel.
- See `slate.md` for the underlying rendering system; Slate attribute polling is the mechanism MVVM bindings use internally to propagate ViewModel field changes to Slate widget properties.
