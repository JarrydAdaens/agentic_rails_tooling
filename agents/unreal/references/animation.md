---
name: animation
version: "1.0"
---

# Animation Systems in Unreal C++

## Use This Reference When
- Implementing or debugging Animation Blueprint C++ integration, montage playback, or notify handling
- Designing layered animation systems using linked ABP layers, slots, or Control Rig
- Diagnosing animation thread safety violations or incorrect state update patterns
- Integrating physics-based animation, ragdoll blending, or procedural IK into a character

## Veteran Expert Stance
The Animation Blueprint runs on the animation worker thread in UE5, not the game thread. This is the foundational fact that governs every architectural decision in Unreal animation code. Gameplay state — health, speed, aim direction, equipment state — lives on the game thread. Animation logic that reads that state directly from the ABP update graph introduces data races. The correct architecture separates state collection (game thread, in `NativeUpdateAnimation` or a dedicated component tick) from state consumption (animation thread, in `NativeThreadSafeUpdateAnimation`). Properties written from one thread and read from the other must be explicitly synchronized, either through cached snapshot structs or through UE's built-in `GetProxyOnGameThread`/`GetProxyOnAnyThread` pattern in UE5.2+.

Montages are the correct tool for interruptible, layered, one-shot animations: attacks, interactions, hit reactions, emotes. They are not the correct tool for continuous locomotion. Montages play into slots, and slots are nodes in the ABP graph that define where the montage output blends into the base pose. A montage without a matching slot node in the ABP graph plays silently and produces no visual result — this is one of the most common montage integration bugs. Slot node placement determines the blend topology: a slot after a state machine blends the montage on top of the entire base pose; a slot before a layered blend by bone blends only the relevant limb region.

Control Rig represents a paradigm shift from data-driven to procedural animation within the UE pipeline. Where blend spaces and state machines express intent through authored assets, Control Rig expresses it through executed code — forward kinematics, IK solvers, constraints, and secondary motion — all composited on top of the ABP output. For any animation work that requires runtime bone manipulation, physically plausible secondary motion, or adaptive IK that responds to environment geometry, Control Rig is the integration point. The C++ surface area is narrower than its Blueprint exposure, but `UControlRigComponent` provides enough to drive rigs from gameplay code.

## Core Concerns
- Thread model: game thread sets state, animation thread consumes it — these roles must never be reversed
- Montage slot topology: where the slot node sits in the ABP graph determines which bones the montage affects
- Notify lifetime: notifies fire on the animation thread; accessing gameplay objects requires thread-safe guards
- Linked ABP layers: the mechanism for modular, swappable animation logic (Lyra model) rather than monolithic ABPs
- Object lifetime in animation delegates: `OnMontageEnded` and similar delegates can outlive the montage or the mesh
- Physics-animation blending: ragdoll transition requires explicit blend weight management, not binary switching

## Practical Heuristics

1. **`NativeUpdateAnimation` runs on the animation thread in multi-threaded mode.** Do not call gameplay functions, read from `AActor` members, or use `GetOwner()` there without caching. Cache all required game state into a struct at the start of each game thread tick, then consume it from `NativeUpdateAnimation`.

2. **`NativeThreadSafeUpdateAnimation` is the UE5.1+ preferred location for animation logic.** It is guaranteed to run safely alongside the game thread. Move all blend parameter calculation and state machine condition evaluation here. `NativeUpdateAnimation` becomes the cache-population hook.

3. **Verify `bUseMultiThreadedAnimationUpdate` on the SkeletalMeshComponent.** If this is true (default in many templates), the animation thread separation is active. Setting it to false is a debug-only workaround, not a shipping solution.

4. **Montage_Play returns a float (the effective play rate), not a handle.** Check for 0.0f to detect a failed play (e.g., no valid slot node, asset not loaded, mesh not initialized). Log the failure — silent zero return is a common source of "montage didn't play" bugs.

5. **Bind `OnMontageEnded` before calling `Montage_Play`.** The delegate fires on the same frame the montage ends. If you bind after Play in the same frame, you may miss the callback for very short montages.

6. **Unbind `OnMontageEnded` in the callback or use a one-shot pattern.** The delegate is a multicast. Binding the same method twice produces two callbacks. If you bind in a `PlayMontage` wrapper that can be called repeatedly, guard with `RemoveDynamic` before `AddDynamic`.

7. **Slot nodes must exist in the ABP graph for the montage's slot name.** The mapping is by `FName` — slot names are case-sensitive. `DefaultSlot`, `UpperBody`, `FullBody` are conventions, not built-ins. Confirm the slot node name matches the montage's slot assignment. Use `UAnimMontage::GetAnimCompositeSection` to inspect slot assignments from C++.

8. **`LinkAnimClassLayers` does not replace the base ABP — it layers on top.** This is the Lyra character animation model: a base ABP handles the state machine, and swappable layer ABPs handle locomotion, combat, or traversal specifics. The layer interface (`UAnimLayerInterface`) defines the handoff points between them. Calling `SetAnimInstanceClass` replaces everything; calling `LinkAnimClassLayers` only overrides the declared layer functions.

9. **AnimNotify fires on the animation thread.** Do not access `UWorld`, call `SpawnActor`, or read mutable gameplay state directly in `UAnimNotify::Notify`. Schedule the gameplay-side response via `AsyncTask(ENamedThreads::GameThread, ...)` or broadcast a delegate that the owning actor handles on the game thread.

10. **`UAnimNotifyState::NotifyTick` is called every animation tick, not every game tick.** At high frame rates with animation update decimation enabled, the cadence differs. Do not use it for physics queries or precise timing. Use it for animation-relative blend weights or curve values only.

11. **Receiving notifies in C++ UAnimInstance: override `OnNotifyBeginReceived` or bind to the delegate.** The alternative is `NativeOnNotifyBegin(FName NotifyName)` in UE5 — simpler than the delegate pattern for single-class handling. For cross-class notification (e.g., notifying the character from the ABP), prefer the delegate to avoid coupling.

12. **Blend space input is set per-frame.** Call the generated setter (from the ABP's exposed property) or directly set the cached variable that `NativeUpdateAnimation` reads. Do not call `UBlendSpace::GetSamples` from gameplay code — that is an asset introspection path, not a runtime input path.

13. **`SetSimulatePhysics(true)` on the entire mesh enables full ragdoll.** Partial ragdoll (simulating only some bodies) requires per-body calls via `USkeletalMeshComponent::SetAllBodiesBelowSimulatePhysics(BoneName, true, true)`. Blending between animation and physics requires the `Physical Animation Component` or manual blend weight management via `USkeletalMeshComponent::SetAllBodiesBelowPhysicsBlendWeight`.

14. **Ragdoll → animation transition requires `ShouldSimulatePhysics` to be disabled, then a `SetPhysicsBlendWeight` ramp.** A hard switch produces a pop. Ramp `PhysicsBlendWeight` from 1.0 to 0.0 over several frames in a tick function while animation re-initializes at the current ragdoll pose via `SnapshotPose`.

15. **`UAnimInstance::GetCurveValue(FName CurveName)` is the runtime curve reader.** Use animation curves for blend weights, IK alpha, and procedural effect intensity. Set curve values from the ABP graph's `Set Curve Value` node, or from C++ via `UAnimInstance::AddCurveValue` (use with care — this is additive, not a set).

16. **Control Rig C++ integration uses `UControlRigComponent::SetControlValue`.** For gameplay-driven IK targets (hand placement, foot IK), set the control values on the rig component from the game thread each tick. The rig evaluates on the animation thread using the last committed values. Race conditions apply — batch updates before the animation thread reads them.

17. **`USkeletalMeshComponent::GetSocketTransform` is game-thread safe.** `GetBoneTransform` is also safe on the game thread but reflects the last completed animation frame, not the in-progress one. For precise projectile spawn positions derived from animation, one-frame lag is usually acceptable. Document when it is not.

18. **TWeakObjectPtr captured in an animation delegate is still unsafe from the animation thread.** `TWeakObjectPtr::IsValid()` internally touches the UObject header, which may be modified concurrently by GC on the game thread. Cache the resolved pointer on the game thread and pass it as a raw (non-null-checked) value only after you have confirmed validity.

19. **`Montage_Stop` fades out by default using the montage's blend-out time.** If you need an immediate stop, call `Montage_Stop(0.0f, Montage)`. If you need to stop all montages on a slot, use `StopAllMontagesByGroupName`. Be explicit — `Montage_Stop` without a specific montage reference stops all playing montages.

20. **State machine transitions in ABP are not directly addressable from C++.** You cannot force a state by name. The correct pattern is to update the boolean or enum UPROPERTY on the `UAnimInstance` subclass that the transition rule evaluates. The ABP graph is data-driven by those properties; your C++ only controls the data, not the graph execution.

21. **Anim dynamics and physics constraints in the ABP run on the animation thread.** Their output is stable but driven by the animation, not the physics engine. They do not respond to gameplay collisions. For collision-responsive secondary motion (cloth, hair hitting walls), use the physics asset + physical animation component path instead.

22. **Debugging animation thread issues: use `a.ParallelAnimEvaluation 0` to disable parallel evaluation in PIE.** This serializes animation onto the game thread, making breakpoints and logging work normally. Never ship with this disabled — it is a diagnostic tool only.

## Smells

- Calling `GetOwner()->GetActorLocation()` directly inside `NativeUpdateAnimation` — game thread data access from animation thread
- Binding `OnMontageEnded` after `Montage_Play` in the same call site — potential missed callback for short montages
- Montage plays (non-zero return) but no visual result appears — slot node name mismatch between montage and ABP
- Spawning actors or emitting sounds directly from `UAnimNotify::Notify` — game thread operations on animation thread
- `SetAnimInstanceClass` used where `LinkAnimClassLayers` is correct — replaces the entire ABP instead of layering
- Hard-switching `SetSimulatePhysics` with no blend — visible pop from animation to ragdoll
- Reading `GetCurveValue` on the game thread for a curve that is only set on the animation thread — stale-by-one-frame value in tight timing scenarios
- Lambda in a `RequestAsyncLoad` callback that dereferences `UAnimMontage*` without validity check — stale pointer after GC
- Caching `UAnimInstance*` across PIE sessions — points to dead world's instance
- Using `NativeUpdateAnimation` for logic that should be in `NativeThreadSafeUpdateAnimation` — unnecessary game thread coupling in UE5.1+
- `AddCurveValue` called every tick without resetting — curve accumulates unboundedly

## Goal
Provide authoritative, thread-aware guidance on Unreal animation architecture, covering the ABP execution model, montage integration, notify handling, layered animation systems, and physics blending. Every heuristic must be specific enough to apply directly to a code review, a threading bug investigation, or a montage integration failure without requiring additional context.

## Boundaries
- For GC safety of UAnimInstance pointers, montage delegate captures, and component lifetime: see `memory-lifetime-ownership.md`
- For character movement integration and root motion configuration: see movement reference when available
- For audio and VFX triggered from animation notifies: cross-thread safety rules in this document apply; asset loading patterns are in the asset-streaming reference when available
