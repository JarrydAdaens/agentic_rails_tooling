---
name: subsystems
metadata:
  version: "1.1"
---

# Subsystems

## Use This Reference When
- Choosing between UGameInstanceSubsystem, UWorldSubsystem, ULocalPlayerSubsystem, or UEngineSubsystem for a new service
- Diagnosing initialization order failures or circular dependency crashes between subsystems
- Replacing manual singleton patterns with the correct Unreal subsystem type
- Designing cross-system event broadcasting or service registries

## Veteran Expert Stance
Subsystems are Unreal's answer to the singleton problem, and they are the right answer. Manually managed singletons — static instance pointers, global TOptional fields, custom Get() functions — are fragile in PIE (multiple worlds, multiple game instances, multiple editor contexts) and leak across world boundaries in ways that are painful to reproduce. The subsystem API provides lifetime scoping backed by the GC, initialization ordering guarantees relative to the owning object, and PIE-correct per-instance isolation. There is almost no scenario where a manual singleton is preferable to a correctly chosen subsystem type.

The common mistake with subsystems is choosing the wrong lifetime scope. A UWorldSubsystem for data that must survive map transitions is wrong — it will be destroyed on unload and rebuilt empty. A UGameInstanceSubsystem for data that is world-specific and should reset on map load is wrong — it will retain stale state across travel. Choosing the subsystem type is a contract: it binds the service's lifetime to its owner's lifetime, and that contract must match the service's actual data coherence requirements.

Subsystems are also natural broadcast hubs. Because they outlive individual actors and have well-defined lifetimes, multicast delegates declared on a subsystem solve the "who do I notify when X happens" problem with loose coupling. Systems that need to react to a gameplay event subscribe to the subsystem's delegate at initialization; the subsystem fires the broadcast; subscribers handle it without requiring direct references between systems. This pattern scales better than event dispatchers on individual actors, which require the subscriber to hold a pointer to the specific actor instance.

## Core Concerns
- Four subsystem types and their exact lifetime scopes relative to their owning objects
- Initialization ordering: subsystems initialize after their owner, not before
- Circular dependency risk during Initialize() when subsystems call each other
- Correct access patterns for each subsystem type and their null-safety requirements
- ShouldCreateSubsystem as the gating mechanism for server, editor, and world-type filtering
- Deinitialize as the canonical cleanup point, not the destructor

## Practical Heuristics

1. UGameInstanceSubsystem lifetime matches the UGameInstance. It survives seamless and non-seamless map travel. Use it for data and services that must persist across the full play session: save state caches, cross-map player progression, global audio managers, session services.

2. UWorldSubsystem lifetime matches the UWorld. It is destroyed when the world is unloaded and created fresh when a new world loads. Use it for services that are world-scoped and should reset on map transition: spatial query caches, world-level event buses, per-level economy systems.

3. ULocalPlayerSubsystem lifetime matches the ULocalPlayer. It is split-screen aware — each local player gets its own instance. Use it for per-player UI state, input configuration, and local-player-specific settings that must survive world transitions but remain isolated per seat.

4. UEngineSubsystem lifetime matches GEngine. It exists from engine startup to shutdown and survives editor restarts in-process. Use it for engine-wide services: asset registry extensions, platform abstraction layers, global diagnostics. Use sparingly — most game logic does not belong at engine scope.

5. Access pattern for each type:
   - GameInstance: `GetGameInstance()->GetSubsystem<UMySubsystem>()`
   - World: `GetWorld()->GetSubsystem<UMySubsystem>()`
   - LocalPlayer: `GetLocalPlayer()->GetSubsystem<UMySubsystem>()` or `PC->GetLocalPlayer()->GetSubsystem<UMySubsystem>()`
   - Engine: `GEngine->GetEngineSubsystem<UMySubsystem>()`

6. Never call GetSubsystem in a constructor. Subsystems are initialized after their owning object is fully constructed. Calling GetSubsystem during construction is undefined behavior — the subsystem may not yet exist.

7. Initialize() is called after the owning object is fully initialized. Override it (with a Super:: call) to perform setup that requires the owner to be valid. Avoid heavy work or blocking calls here — Initialize is synchronous on the game thread.

8. Deinitialize() is the correct cleanup point. Override it to unregister delegates, cancel async operations, and release resources. Do not rely on the destructor for cleanup that must happen before sibling subsystems are destroyed — destructor order relative to other subsystems is not guaranteed.

9. Circular dependencies during Initialize: if Subsystem A calls `GetSubsystem<B>()` during A's Initialize, and B's Initialize calls `GetSubsystem<A>()`, the result is a crash or deadlock depending on initialization state. Break the cycle by moving one access to PostInitialize or lazy-initializing on first use rather than in Initialize.

10. PostInitialize() fires after all subsystems of the same owner have completed Initialize(). Use it for cross-subsystem wiring that would otherwise create circular dependency in Initialize. This is the safe window for "I need both A and B to exist before I connect them."

11. Override ShouldCreateSubsystem to skip subsystem creation in contexts where the service is irrelevant. Common filters:
    - Dedicated server: `World->GetNetMode() == NM_DedicatedServer` — skip client-only subsystems
    - Editor worlds: `World->WorldType == EWorldType::Editor` — skip runtime subsystems in editor
    - PIE: allow or skip based on whether the subsystem is PIE-safe

12. In PIE, each PIE world gets its own UWorldSubsystem instance. GameInstance subsystems may be shared or per-PIE depending on editor settings (each PIE player can have their own GameInstance). Do not assume GameInstance subsystems are singletons across PIE sessions.

13. UEngineSubsystem instances are true singletons in-process. They are shared between PIE sessions and the editor world. Any mutable state in an EngineSubsystem must be explicitly reset or PIE-session-scoped to avoid cross-session contamination.

14. Subsystem references do not need to be stored. GetSubsystem<T>() is a fast O(1) lookup by type against the owner's subsystem collection. It is safe to call repeatedly rather than caching the pointer in a member variable — though caching is fine if the call site is in a hot path.

15. Subsystems as event buses: declare multicast delegates on the subsystem. Systems that care about an event call `GetSubsystem<UMySubsystem>()->OnEventFired.AddDynamic(this, &UMyClass::HandleEvent)` at initialization and remove in their destructor or EndPlay. The subsystem fires the broadcast when the event occurs. No direct pointer between the event source and subscribers is required.

16. A UWorldSubsystem that needs to react to actor events (e.g., OnActorSpawned) should register the delegate in Initialize using `GetWorld()->AddOnActorSpawnedHandler(...)` and unregister in Deinitialize. Do not assume the world is valid in the destructor.

17. Do not use UGameInstanceSubsystem as a cross-world actor registry. Actors belong to a world; the GameInstance subsystem outlives any given world. Holding strong references to world actors in a GameInstance subsystem will prevent garbage collection of the old world after travel.

18. For server-only subsystems in a networked game, use ShouldCreateSubsystem to return false on clients, or gate access with `GetWorld()->GetNetMode() != NM_Client`. Client code that calls GetSubsystem<ServerOnlySubsystem>() will get null if ShouldCreateSubsystem correctly filters it out.

19. Async operations started in Initialize must be cancelled or awaited in Deinitialize. Background tasks that hold a reference to the subsystem will keep it alive past its intended lifetime or access a stale pointer after Deinitialize returns.

20. Prefer subsystems over custom UObject singletons rooted on the GameInstance directly. The subsystem API provides a standardized initialization contract, automatic cleanup, and PIE isolation that manually-rooted objects do not.

## Smells

- Calling `GetSubsystem<T>()` in a class constructor — the owning object is not initialized yet and the subsystem does not exist at that point in the lifecycle.
- Using UGameInstanceSubsystem to cache world-scoped actors across map transitions — actor pointers become stale after travel and the GameInstance subsystem will hold dangling references.
- Storing mutable per-session state on a UEngineSubsystem — state leaks between PIE sessions and editor restarts, producing non-reproducible behavior.
- Implementing circular Initialize dependencies without using PostInitialize — produces initialization crashes that only surface under specific subsystem registration order.
- Skipping Deinitialize override and relying on destructor for delegate and async cleanup — destructor ordering relative to other subsystems is not guaranteed, and delegates may fire against a partially-destroyed object.
- Using a manual static singleton instead of the appropriate subsystem type — breaks PIE isolation, leaks between worlds, and does not participate in the GC lifecycle.
- Choosing UWorldSubsystem for data that must survive map travel — it is destroyed with the world; use UGameInstanceSubsystem for persistent data.
- Choosing UGameInstanceSubsystem for world-specific data that should reset on map load — stale state from a prior world persists into the new world's lifetime.
- Not overriding ShouldCreateSubsystem for client-irrelevant server subsystems — creates unnecessary overhead and produces misleading GetSubsystem non-null results on clients.
- Iterating all actors from inside a UEngineSubsystem without a world reference — engine subsystems have no inherent world context and GetAllActorsOfClass requires a valid UWorld.

## Goal

Provide a precise reference on Unreal's four subsystem types — their lifetimes, initialization contracts, access patterns, and design roles — so engineers can replace manual singleton patterns with correctly-scoped subsystems and design loosely-coupled service architectures that are PIE-safe, lifecycle-correct, and server/client aware.

## Boundaries

- Gameplay framework class lifetimes (GameMode, GameState, PlayerController): see `gameplay-framework.md`
- Actor and component initialization ordering: see `actors-components.md`
- Replication of subsystem-managed state to clients: see `replication.md`
