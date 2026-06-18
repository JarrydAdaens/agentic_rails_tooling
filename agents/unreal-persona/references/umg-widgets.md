---
name: umg-widgets
metadata:
  version: "1.1"
---

# UMG Widgets

## Use This Reference When
- Implementing or auditing HUD, menus, or any UUserWidget subclass in C++
- Diagnosing null crashes, lifecycle ordering bugs, or widget visibility issues
- Designing widget ownership, pooling, or viewport management strategies
- Handling input mode transitions between UI and gameplay

## Veteran Expert Stance
UMG is a thin UObject wrapper over Slate. Understanding that means recognizing the two distinct lifetime domains at play: the UObject graph (GC-managed, must be kept alive via UPROPERTY) and the Slate widget tree (TSharedPtr-managed, constructed on demand). Most widget bugs — dangling pointers, null BindWidget crashes, widgets that outlive their actors — trace back to misunderstanding where an object actually lives and who is responsible for keeping it alive.

The lifecycle callback sequence (NativeOnInitialized, NativePreConstruct, NativeConstruct) is not a simple ordered progression. Each fires under different conditions with different validity guarantees. Conflating them is the single most common source of widget initialization bugs in production codebases. NativeOnInitialized is the true constructor analog: it fires once per widget instance creation and is safe for one-time setup. NativeConstruct fires every time the widget enters the viewport and is the correct place for per-show initialization. NativePreConstruct is an editor-only callback used for thumbnail and preview rendering — world state is unavailable there.

Widget pooling is not an optimization — it is a correctness requirement at scale. CreateWidget allocates, initializes, and constructs a full UObject and Slate hierarchy. Calling it on every frame for frequently toggled HUD elements (damage numbers, waypoint markers, ammo counters) will crater frame time. The correct pattern is allocate once, toggle visibility. Collapsed widgets skip layout and paint entirely. Hidden widgets still participate in layout. Remove from parent only when the widget will not be reused.

## Core Concerns
- Widget ownership and GC safety — UPROPERTY is not optional
- Lifecycle callback semantics — OnInitialized vs Construct vs PreConstruct
- Viewport attachment scope — AddToViewport vs AddToPlayerScreen for split-screen correctness
- Input mode management — UI/game input ownership lives on PlayerController
- BindWidget contract — name matching between C++ field and designer widget is strictly enforced
- Widget pooling discipline — CreateWidget cost and visibility-based recycling

## Practical Heuristics

1. Store all UUserWidget pointers in UPROPERTY fields. A raw pointer or TSharedPtr<UUserWidget> is invisible to GC and will dangle after a collection cycle.

2. Call CreateWidget with the correct outer. For widgets tied to a single player's session, pass the owning ULocalPlayer or APlayerController. For session-persistent widgets, pass the UGameInstance. The outer determines GC reachability upstream.

3. Never call AddToViewport or CreateWidget in a UObject constructor or CDO initialization. The world is not valid at that point. Use BeginPlay or a dedicated UI manager service.

4. NativeOnInitialized: fires once at creation. Safe for: binding delegates, caching BindWidget child pointers, one-time initialization. BindWidget children are already valid here.

5. NativeConstruct: fires every time the widget is added to the viewport. Safe for: refreshing displayed data, starting animations, subscribing to game events. Do not assume this fires only once.

6. NativeDestruct: fires every time the widget is removed from the viewport. Unsubscribe event delegates here — symmetric with NativeConstruct subscriptions.

7. NativePreConstruct: fires in editor only, during thumbnail and preview generation. World, GameInstance, and owning player are all null. Guard any access with `if (!IsDesignTime())` or `if (GetWorld() && GetWorld()->IsGameWorld())`.

8. UPROPERTY(meta=(BindWidget)) requires the C++ field name to exactly match the designer-placed widget name in the UMG editor. A mismatch produces a null pointer and a crash in NativeConstruct when the pointer is first dereferenced. Always validate field names against the UMG hierarchy panel.

9. UPROPERTY(meta=(BindWidgetOptional)) suppresses the compile-time name-match enforcement. Use for widgets that may or may not be present depending on the widget variant. Always null-check before use.

10. AddToViewport adds the widget to the shared global viewport layer — correct for fullscreen UIs and single-player. Use AddToPlayerScreen for any widget that must be scoped to a specific local player in split-screen. Mixing these causes widgets to appear on the wrong player's viewport.

11. ZOrder in AddToViewport is an integer priority within the same viewport layer. Higher value renders on top. Avoid hardcoding magic numbers; define an enum or named constants for HUD, Menu, Overlay, Debug layers.

12. SetVisibility(ESlateVisibility::Collapsed) is the correct pooling toggle — collapsed widgets skip both layout and paint. SetVisibility(ESlateVisibility::Hidden) skips paint but still participates in layout. Never use RemoveFromParent for widgets you intend to reuse.

13. Input mode must be set on the APlayerController, not on the widget itself. SetInputModeUIOnly: disables game input, locks cursor to viewport. SetInputModeGameOnly: game input only, hides cursor. SetInputModeGameAndUI: both active, cursor visible. Always pair input mode changes with bShowMouseCursor on the PlayerController.

14. Flush input mode back to game-only on widget close. Failing to do so leaves the game in UI input mode after a menu closes, which is a common bug in shipping titles.

15. Widget animation (UWidgetAnimation) is played via PlayAnimation, PlayAnimationForward, PlayAnimationReverse. Get references via UPROPERTY(Transient, meta=(BindWidgetAnim)) — same name-matching rules as BindWidget apply.

16. A widget can outlive the actor that created it if it is still held by the viewport or by a UPROPERTY chain rooted elsewhere. Always call RemoveFromParent and clear owning references in the actor's EndPlay. Failing to do so causes widgets to persist on screen with stale actor pointers.

17. For widgets owned by player state or game state, prefer routing creation through a dedicated HUD class or UI manager subsystem. Centralizing widget lifecycle in one place prevents ownership ambiguity in multiplayer scenarios.

18. GetOwningPlayer() returns the APlayerController that owns the widget. GetOwningLocalPlayer() returns the ULocalPlayer. Prefer GetOwningLocalPlayer for subsystem access; prefer GetOwningPlayer for gameplay API calls. Both can be null if the widget is constructed with a non-player outer.

19. FocusWidget / SetFocus on individual child widgets is necessary for keyboard/gamepad navigation. SetIsFocusable(true) must be set on the widget that should receive focus. Focus order follows the widget hierarchy by default; override with custom focus rules if needed.

20. Don't create per-instance bindings in NativeConstruct if the widget is pooled and the delegate target can change. Bind once in NativeOnInitialized or validate and rebind on each NativeConstruct.

## Smells

- `UMyWidget* Widget;` — raw pointer UPROPERTY missing, widget is invisible to GC and will be collected.
- CreateWidget called in a class constructor or field initializer — world is not valid, this will crash or silently construct a broken widget.
- AddToViewport inside a constructor or field initializer — same timing violation.
- NativePreConstruct accessing GetWorld(), GetGameInstance(), or GetOwningPlayer() without an IsDesignTime guard — crashes in editor thumbnail generation.
- A UPROPERTY(meta=(BindWidget)) field whose C++ name differs from the designer widget name by even one character — silent null, guaranteed crash on first access.
- Calling RemoveFromParent on a frequently toggled widget instead of toggling visibility — allocates and destroys the Slate tree on every toggle.
- SetInputModeUIOnly called on widget open with no corresponding SetInputModeGameOnly on widget close — game is left non-interactive after the menu closes.
- AddToViewport used for a split-screen secondary player's HUD — widget appears on the wrong player's screen or is absent entirely.
- Subscribing to a game event delegate in NativeConstruct without unsubscribing in NativeDestruct — duplicate subscriptions accumulate across show/hide cycles.
- Storing a TSharedPtr<SWidget> in a UPROPERTY — TSharedPtr is not a UObject pointer, UPROPERTY on it is meaningless and confuses the GC.
- Calling PlayAnimation before NativeConstruct completes — animation asset references are not yet bound, this returns without error and plays nothing.
- Accessing widget children (BindWidget fields) in NativePreConstruct — they are null in preview contexts that do not go through full construction.

## Goal

Correctly applied, these patterns produce a widget system where ownership is unambiguous, lifecycle callbacks are used for their precise intended purpose, and pooling prevents per-frame allocation. The result is a HUD and menu layer that is stable across PIE, split-screen, and shipping builds with no GC-induced null crashes and no residual input-mode bugs.

## Boundaries

- See `slate.md` for the underlying Slate widget system that UMG compiles down to.
- See `mvvm-preview-mode.md` for ViewModel binding patterns that replace manual setter calls in data-driven UIs.
