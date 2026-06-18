---
name: actors-components
metadata:
  version: "1.1"
---

# Actors and Components

## Use This Reference When
- Debugging initialization order failures, null component pointers, or transform corruption on spawn
- Deciding where to put initialization logic across constructor, PostInitializeComponents, and BeginPlay
- Working with component attachment, tick groups, or runtime-spawned components
- Diagnosing replication issues related to actor spawning or component registration

## Veteran Expert Stance
The constructor in Unreal is not what most C++ engineers expect. It runs on the CDO (Class Default Object) and during asset loading — not at gameplay time. This means no world context, no valid sibling components, no GameState. Engineers who put cross-component initialization in the constructor and wonder why they get null pointer crashes are fighting the CDO model. PostInitializeComponents is the first place where all native components are guaranteed to exist and the actor has a valid world context, making it the correct seam for inter-component wiring.

Tick is a frequently abused hook. Every ticking actor pays CPU budget even at low framerates, and the scheduler has no awareness of what your tick actually does. Before enabling tick on any actor or component, ask whether the state change driving the tick is event-based. If a delegate, a timer, or a gameplay message can replace the tick, that is always the right call. The marginal cost of tick batching and cache misses across hundreds of actors adds up in ways that only profile data makes visible.

Understanding attachment rules is non-negotiable for any actor that changes parent, teleports, or attaches at runtime. KeepRelative and KeepWorld have opposite semantics and produce dramatically different results in the same scenario. Treating AttachmentRules as boilerplate rather than a deliberate transform contract is a consistent source of subtle world-space corruption that is difficult to reproduce outside of specific runtime conditions.

## Core Concerns
- Actor lifecycle ordering: which hooks have a world context, which have sibling components, which are replicated
- Component registration: constructor-created vs runtime-created components follow different registration paths
- Attachment rules and transform preservation during parent changes
- Tick group selection and the cost of unnecessary ticking
- Deferred spawning vs immediate spawning and the window for pre-BeginPlay initialization
- Replication authority: which side may call SpawnActor for replicated actors

## Practical Heuristics

1. Never access sibling components in the constructor. The order of CDO construction is not the order of gameplay initialization. Use PostInitializeComponents for cross-component wiring.

2. PostInitializeComponents fires after all native components are initialized and attached. This is the correct place to cache component pointers, register delegates between components, and set initial state that depends on component configuration.

3. BeginPlay fires once, at gameplay start, after replication is set up. Put runtime-only state initialization here. Do not duplicate editor-visible state here — it will not reflect in the editor's Construction Script preview.

4. The Construction Script (OnConstruction) runs in editor on every property change. Keep it idempotent and side-effect free. Never initialize gameplay-critical state exclusively in OnConstruction; it will not run in packaged builds when expected.

5. Components created via CreateDefaultSubobject in the constructor are auto-registered and part of the CDO. Components created at runtime (e.g., NewObject<UActorComponent>) must call RegisterComponent() explicitly; forgetting this is the most common source of "component exists but doesn't tick or replicate."

6. Runtime-created scene components must call SetupAttachment before RegisterComponent, not after. Reversing the order produces an unattached component that may register successfully but will not participate in the attachment hierarchy.

7. AttachToComponent with EAttachmentRule::KeepWorld preserves the component's current world transform, adjusting the relative transform to compensate. KeepRelative preserves the relative transform, which changes the world transform. SnapToTarget zeroes the relative transform. Know which you want before writing the call.

8. SpawnActor should only be called on the server for replicated actors. The replication system propagates the actor to clients. Calling SpawnActor on a client for a replicated actor produces a client-only ghost that will conflict when the server's version arrives.

9. Use SpawnActorDeferred + FinishSpawning when spawn parameters must be set before BeginPlay fires. The window between SpawnActorDeferred and FinishSpawning is the only safe time to configure properties that BeginPlay reads on the spawned actor.

10. PrimaryActorTick.bCanEverTick defaults to true for AActor and false for most UActorComponent subclasses. Set it explicitly in the constructor and disable it when not needed. Do not rely on the default.

11. Tick group TG_PrePhysics is the default. Use TG_PostPhysics when your tick reads physics results (e.g., post-simulation bone positions). Use TG_PostUpdateWork for logic that must run after all gameplay ticks. Using TG_PrePhysics for physics-result-dependent logic produces one-frame-stale reads.

12. Ordering between actors in the same tick group is non-deterministic. If Actor A's tick must run before Actor B's tick, use AddTickPrerequisiteActor or AddTickPrerequisiteComponent to declare the dependency explicitly.

13. GetOwner() from a component can return null in the CDO context and during component construction. GetWorld() can return null in CDO context, during asset loading, and in some editor operations. Always guard both in non-gameplay code paths.

14. Disable tick on components that do not need it. A USceneComponent with bCanEverTick = true and an empty TickComponent override is wasted scheduler overhead on every frame.

15. For event-driven state changes, prefer FTimerManager (GetWorldTimerManager), multicast delegates, or UGameplayMessageSubsystem over per-frame polling. Tick is appropriate for smooth per-frame interpolation, physics, and animation — not for "check if something changed."

16. Lifecycle order during destruction: EndPlay → BeginDestroy → FinishDestroy. EndPlay is the safe point to unregister delegates and timers. BeginDestroy starts the garbage collection process — do not rely on other objects being valid here.

17. When using Deferred Spawning, the actor is not registered with the world until FinishSpawning. Do not attempt to find the actor via overlaps, line traces, or actor iteration between SpawnActorDeferred and FinishSpawning.

18. UActorComponent has no transform and cannot attach to other components. USceneComponent inherits from UActorComponent and adds a transform and attachment support. If a component needs a position in the world, it must be a USceneComponent or subclass.

19. SetActorHiddenInGame does not affect collision. SetActorEnableCollision does not affect visibility. Treating these as coupled is a common mistake when implementing "deactivate this actor."

20. For pooled actors, call SetActorTickEnabled(false) and SetActorHiddenInGame(true) rather than destroying and respawning. Destruction and respawn incur UObject allocation, replication overhead, and BeginPlay re-initialization cost.

## Smells

- Accessing `GetOwner()` or `GetWorld()` in a component constructor without a null guard — CDO context makes both valid failure points.
- Putting cross-component initialization in the actor constructor instead of PostInitializeComponents — sibling components are not guaranteed to be initialized yet.
- Calling `RegisterComponent()` after `SetupAttachment()` is skipped — produces an unattached, floating component with no attachment parent.
- Enabling tick on every actor subclass without profiling — tick overhead compounds across hundreds of actors and is rarely justified for state that could be event-driven.
- Using `SpawnActor` on a client for a replicated actor — produces a duplicate client-local actor that conflicts with the server-replicated version.
- Using `FinishSpawning` immediately after `SpawnActorDeferred` with no property assignments in between — defeats the purpose of deferred spawning entirely.
- Setting `AttachmentRule` to `KeepRelative` when the intent is to preserve world position — produces silent world-space drift that is only visible in motion.
- Skipping `EndPlay` cleanup of timers and delegates and relying on `BeginDestroy` for teardown — delegate handles and timer handles outlive the actor, causing crashes on callback.
- Using `TG_PrePhysics` for a tick that reads physics simulation results — produces stale-by-one-frame data every tick.
- Hardcoding tick ordering assumptions without `AddTickPrerequisiteActor` — breaks silently when actor spawn order changes or async loading shifts initialization timing.
- Putting gameplay-critical initialization exclusively in `OnConstruction` — does not run at the expected time in packaged builds when actors are placed in a level.

## Goal

Provide expert-level reference on Unreal actor and component initialization, registration, attachment, and tick semantics for engineers who need precise answers about lifecycle ordering, replication safety, and performance contracts — not introductory descriptions of what actors are.

## Boundaries

- Replication mechanics (RPCs, property replication, NetRole): see `replication.md`
- Gameplay Ability System components and attribute sets: see `gas.md`
- Physics simulation setup and collision channels: see `physics.md`
