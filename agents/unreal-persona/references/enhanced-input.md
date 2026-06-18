---
name: enhanced-input
metadata:
  version: "1.1"
---

# Enhanced Input System

## Use This Reference When
- Implementing or refactoring input handling in UE5 using the Enhanced Input plugin
- Diagnosing input not firing, input conflicts between UI and gameplay, or rebinding failures
- Designing IMC stacking strategies for UI overlays, vehicles, or context-sensitive gameplay modes
- Migrating from the legacy UE4 input system or adding runtime rebinding support

## Veteran Expert Stance
Enhanced Input is not a thin wrapper over the legacy system — it is a fundamentally different model. The legacy system hardcodes bindings to physical keys in project settings and routes them through `PlayerController::SetupInputComponent`. Enhanced Input separates the semantic action (UInputAction) from the physical mapping (UInputMappingContext), and routes all binding through the Local Player subsystem rather than the controller. Any port that treats EI as "same wiring, new API" will produce subtly wrong behavior, especially around context switching and UI/game input isolation.

IMC priority stacking is the mechanism that replaces the legacy "bind override" pattern. When the player opens a menu, you do not disable the game input component — you add a high-priority UI IMC that consumes the relevant inputs before the game IMC sees them. When the menu closes, you remove the UI IMC and the game IMC takes effect again. This composable model is more correct than toggling input modes for everything except full modal UI lockout, and it scales cleanly to vehicles, cutscenes, and ability-specific input contexts.

Trigger type selection is where most Enhanced Input implementations go wrong. Developers reach for `Triggered` by default and then fight to implement hold-to-charge or press-vs-hold disambiguation. The trigger pipeline — Started, Ongoing, Triggered, Completed, Canceled — maps directly to the phases of a physical input and should be read as a state machine. Design which trigger events your action needs before writing the binding, not after.

## Core Concerns
- **Action/mapping separation**: UInputAction defines the semantic contract (what and what type of value); UInputMappingContext binds physical inputs to that contract — these two concerns must stay cleanly separated
- **Local Player subsystem as the binding surface**: inputs are registered to the local player, not to the PlayerController or the Pawn, which means binding survives controller changes and works correctly in split-screen
- **IMC priority and context switching**: multiple IMCs compose via priority; context transitions (menus, vehicles, abilities) are managed by adding and removing IMCs, not by reconfiguring bindings
- **Trigger state machine**: each input action progresses through Started → Ongoing → Triggered → Completed (or Canceled); binding to the wrong trigger event is the primary source of hold/press behavioral bugs
- **Modifier pipeline**: raw axis values pass through an ordered modifier stack before triggers evaluate — modifier order matters and affects all downstream trigger and binding logic
- **UI/game input isolation**: PlayerController input mode and IMC stacking are complementary but distinct mechanisms; conflating them causes mouse capture, UI interaction, and game input to misbehave simultaneously

## Practical Heuristics

1. **Add IMCs via the Enhanced Input Local Player Subsystem, not via the PlayerController directly.** The correct access pattern in C++ is:
   ```cpp
   if (UEnhancedInputLocalPlayerSubsystem* Subsystem =
       ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(GetLocalPlayer()))
   {
       Subsystem->AddMappingContext(IMC_Default, 0);
   }
   ```
   Accessing this through `GetLocalPlayer()` requires the PlayerController to have a valid local player — call it in `BeginPlay` or after `OnPossess`, never in the constructor.

2. **Bind input actions in `SetupPlayerInputComponent`, not in `BeginPlay`.** `SetupPlayerInputComponent` is called after the input component is created and ready. Attempting to bind in `BeginPlay` may execute before the component exists, especially on remotely controlled pawns.

3. **Cast to `UEnhancedInputComponent` with `CastChecked` in `SetupPlayerInputComponent`.** If Enhanced Input is active, the component is always the enhanced type. A failed cast is a configuration error, not a runtime condition to handle gracefully:
   ```cpp
   UEnhancedInputComponent* EIC = CastChecked<UEnhancedInputComponent>(InputComponent);
   EIC->BindAction(IA_Jump, ETriggerEvent::Started, this, &AMyCharacter::OnJumpStarted);
   EIC->BindAction(IA_Jump, ETriggerEvent::Completed, this, &AMyCharacter::OnJumpReleased);
   ```

4. **Choose trigger event type deliberately.** `Triggered` fires once per activation cycle (press-and-release). `Started` fires on the first frame of activation. `Ongoing` fires every frame while active. `Completed` fires on release. `Canceled` fires when a hold threshold is not met. A charge attack wants `Started` to begin charging, `Ongoing` to tick the charge, and `Completed` or `Triggered` to release.

5. **Use `ETriggerEvent::Started` for jump, dodge, and other instant-response actions** where you want one callback on the first input frame, not one callback per frame while the key is held.

6. **UInputAction value type must match what the binding delivers.** A gamepad left stick must map to an Axis2D action. Mapping a stick to a bool action silently discards the axis data. Mapping a key to an Axis2D delivers a unit vector on X, which may not be what you expect. Define the value type in the UInputAction asset and ensure every mapping targeting it delivers compatible data.

7. **Apply `Swizzle Input Axis Values` modifier to gamepad sticks when your movement code expects Y-up.** Gamepad right stick X maps to yaw (as expected), but the Y axis may need to be swizzled to route to the correct component of the FVector2D. Verify in the Input Debugger (`showdebug enhancedinput`) before assuming the axis order is correct.

8. **Add `Dead Zone` modifier to any analog axis action before other modifiers.** Dead Zone must come first in the modifier stack because subsequent modifiers (Scale, Negate) operate on the post-deadzone value. A Negate before Dead Zone produces negative deadzone, which breaks the deadzone purpose entirely.

9. **Modifier order in the stack is execution order.** Modifiers in the IMC mapping execute top-to-bottom. Dead Zone → Swizzle → Negate → Scale is the conventional order for gamepad sticks feeding a 2D movement action. Validate in the Input Debugger.

10. **For UI/game input isolation, use IMC priority stacking as the primary mechanism and `SetInputMode` for mouse capture semantics.** When a menu opens: add the UI IMC at priority 100 (or any value above the game IMC). Call `SetInputModeUIOnly` or `SetInputModeGameAndUI` based on whether the game should remain interactive. When the menu closes: remove the UI IMC and call `SetInputModeGameOnly`. These two mechanisms are complementary: IMC stacking controls which actions fire; `SetInputMode` controls mouse cursor visibility and capture.

11. **`SetInputModeUIOnly` stops all game IMC actions because the controller stops consuming input, not because the IMC was removed.** Do not rely on this as a substitute for removing IMCs — the IMC stack still exists and will be active again the moment input mode changes. Always pair input mode changes with the corresponding IMC add/remove.

12. **For chorded actions (Shift+Click, Ctrl+Ability), use the `Chorded Action` trigger dependency** rather than polling modifier key state in code. Define a modifier-key action (IA_Shift as a bool action), then set the primary action's trigger to require IA_Shift to be in `Triggered` state. This is evaluated in the trigger pipeline without any C++ polling.

13. **Runtime rebinding requires flushing and re-adding the IMC after changes.** The subsystem caches the resolved mappings. Modifying a mapping without flushing produces no visible effect:
    ```cpp
    Subsystem->RemoveMappingContext(IMC_Default);
    // Modify the mapping...
    Subsystem->AddMappingContext(IMC_Default, 0);
    ```

14. **Use `UEnhancedInputUserSettings` (UE5.3+) for player-facing rebind persistence.** It handles save/load of `FPlayerMappableKeySlot` changes and integrates with the `PlayerMappableInputConfig` asset. Do not hand-roll rebind serialization against raw FKey values — the user settings API provides conflict detection, default restoration, and profile support.

15. **`PlayerMappableInputConfig` is the asset-side contract for rebindable actions.** Mappings inside this config are what surfaces to the UI rebind screen. Actions that should not be rebindable by players must not be in a PlayerMappableInputConfig — put them in a non-mappable IMC.

16. **In split-screen, each local player has an independent subsystem instance.** Always resolve the subsystem from `GetLocalPlayer()` on the specific PlayerController, not from a shared reference. Binding on the wrong player's subsystem in split-screen is a silent bug that only manifests when two players are active.

17. **The Input Debugger is the first tool to reach for.** `showdebug enhancedinput` in the console shows active IMCs, their priorities, all bound actions, current trigger states, raw and processed axis values, and which action consumed each input frame. This resolves 90% of "why isn't my input firing" questions without a debugger.

18. **For ability systems using GAS, route ability activation through `TryActivateAbilitiesByInputID` or a GameplayEvent triggered from the Enhanced Input callback.** Do not wire GAS ability activation directly in the EIC bind lambda — it couples two systems at the wrong layer and bypasses prediction key allocation.

19. **Enhanced Input works correctly on simulated proxies only for UI-level visual feedback** (e.g., displaying the bound key). Simulated proxies do not process input — input is local-player-only. Never attempt to activate an Enhanced Input action on a non-locally-controlled pawn.

20. **When porting from the legacy system, remove all `AxisMappings` and `ActionMappings` from `DefaultInput.ini`.** The enhanced system and legacy system can coexist in the same project, which means stale legacy bindings can silently fire alongside enhanced input, producing duplicate or conflicting callbacks.

## Smells

- Binding actions in `BeginPlay` before the input component is guaranteed to exist
- Using `CastChecked` bypass — casting to `UInputComponent` instead of `UEnhancedInputComponent` and silently failing to bind
- Adding IMCs in the constructor or CDO, where there is no valid local player subsystem
- Polling `IsKeyDown` or `GetAxisValue` in `Tick` instead of binding to the appropriate trigger event
- Using `SetInputModeUIOnly` as a substitute for removing the game IMC, then wondering why game actions fire when input mode is restored
- Applying `Negate` or `Scale` modifiers before `Dead Zone` in the modifier stack, breaking deadzone behavior
- Mapping a gamepad stick axis to a bool UInputAction value type, silently discarding the analog data
- Hand-rolling rebind serialization instead of using `UEnhancedInputUserSettings` and `PlayerMappableInputConfig`
- Forgetting to flush and re-add the IMC after a runtime mapping change, leaving the cached resolution stale
- Calling `GetSubsystem<UEnhancedInputLocalPlayerSubsystem>` off a shared or wrong PlayerController in split-screen

## Goal
Serve as an authoritative quick reference for the Enhanced Input system in UE5, covering the action/mapping architecture, IMC priority stacking, trigger state machine semantics, modifier pipeline ordering, UI/game input isolation, and runtime rebinding patterns. Enable an experienced Unreal developer to implement correct input handling and diagnose failures without consulting engine source.

## Boundaries
- For ability activation triggered by input, see `gameplay-ability-system.md`
- For PlayerController lifecycle, possession, and input component setup timing, see `unreal-player-framework.md`
- For general Unreal C++ naming and module conventions, see `unreal-cpp-conventions.md`
