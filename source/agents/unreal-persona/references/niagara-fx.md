---
name: niagara-fx
metadata:
  version: "1.1"
---

# Niagara FX — C++ Integration and Runtime Control

## Use This Reference When
- Spawning, parameterizing, or pooling Niagara systems from C++ gameplay code
- Diagnosing VFX lifecycle bugs: effects not appearing, not stopping, or leaking
- Designing a data-driven VFX pipeline where gameplay events drive visual parameters
- Evaluating CPU vs GPU emitter tradeoffs for particle callbacks, collision events, or readback

## Veteran Expert Stance
Niagara is not a fire-and-forget API. The most common class of bugs in production Niagara usage comes from treating `SpawnSystemAtLocation` like a sound cue — call it and forget it. In reality, the returned `UNiagaraComponent` is an actor component with its own lifecycle, and if you lose that reference you have surrendered all runtime control: you cannot cancel, rebound, reparameter, or pool the effect. Every systemic VFX spawn should evaluate whether the effect needs a held reference. One-off impacts and pickup sparks genuinely do not. Shield charges, persistent auras, and charge-up effects absolutely do.

Parameter injection is order-sensitive in a way that is not obvious from the API surface. Variables set via `SetNiagaraVariableFloat` after the system has advanced past the first tick of an emitter that samples at spawn are silently ignored. The system does not error — it simply uses the default. The correct pattern is to set all parameters on the component before activation, or design emitters to poll their inputs each frame via a Scratch Pad module that samples User-exposed parameters rather than reading at spawn-only. Know which category your emitter falls into before you integrate it.

GPU simulation is a hard architectural boundary. Any design that requires reading particle positions back to the game thread, detecting particle death, or responding to per-particle collision events requires CPU simulation. GPU particle counts can be orders of magnitude higher, but they exist entirely on the render thread. Mixing assumptions about GPU particles and game-thread callbacks is a source of silent, platform-specific failures — particularly on consoles where RHI latency between render and game thread is more pronounced.

## Core Concerns
- `UNiagaraSystem` is the spawnable asset; it owns one or more `UNiagaraEmitter`. Never try to spawn individual emitters from C++.
- `UNiagaraComponent` is the runtime instance — an actor component returned by spawn functions. Its lifetime and auto-destroy behavior must be explicitly managed.
- Parameter channels: per-component variables set via typed setters vs. `FNiagaraParameterCollection` for shared global state across many systems.
- Pooling: `UNiagaraComponent` construction is expensive. The system-level pool settings and the `bAutoDestroy` flag are the primary knobs.
- Thread boundary: CPU emitters live on task threads but interact safely with game-thread data through the Niagara tick; GPU emitters are render-thread-only and cannot participate in game-thread queries.
- Scalability: `FNiagaraSystemScalabilitySettings` and LOD distance control whether a system even ticks, making them the first line of performance defense.

## Practical Heuristics

1. Use `UNiagaraFunctionLibrary::SpawnSystemAttached` when binding to a character socket, weapon muzzle, or any component that moves. The Niagara component will follow the attachment automatically. Use `SpawnSystemAtLocation` only for world-space effects with no parent.

2. Always capture the returned `UNiagaraComponent*` in a `UPROPERTY` member when the effect has a defined end condition controlled by gameplay (end of ability, death, reload complete). Letting it go out of scope means the effect runs to natural completion regardless of gameplay state.

3. Set all required User parameters before activation. The safe sequence is: spawn with `bAutoActivate=false`, call `SetNiagaraVariableFloat` / `SetNiagaraVariableLinearColor` / `SetNiagaraVariableBool` / `SetNiagaraVariableVector`, then call `Activate()`.

4. For emitters that sample parameters each frame (poll model), you can call the setter on a running component freely. Verify in the emitter that the relevant modules use `User.Param` binding with per-frame evaluation, not a cached spawn-time value.

5. Global, cross-system parameters belong in a `FNiagaraParameterCollection`. Wind direction, weather intensity, ambient temperature — any value multiple simultaneous VFX systems need — goes into a collection. Update via `UNiagaraParameterCollectionInstance::SetVectorParameter` or equivalent once per frame instead of iterating over all active components.

6. Pooling: set `PoolPrimeSize > 0` on the system asset to pre-warm the pool at load time. Set `MaxPoolSize` to cap memory. In C++, set `SetAutoDestroy(false)` and call `Deactivate()` (not `DestroyComponent()`) to return to pool. The system handles the reset automatically.

7. Use `SetAutoDestroy(true)` only for genuinely fire-and-forget effects: bullet impacts, footstep puffs, small one-shot pickups. Anything that might need early cancellation is a candidate for `false`.

8. Do not call `SpawnSystemAtLocation` or `SpawnSystemAttached` every frame or every tick of a rapid-fire ability without rate limiting. Even pooled components have activation overhead. Aggregate or throttle high-frequency spawns.

9. GPU emitters cannot report particle events to gameplay. If a design requires "particle hit something, apply damage" — that logic must live on a CPU emitter or be solved at the projectile/trace level in C++, not inside Niagara simulation.

10. CPU emitters can use the `Particle Collision` module with callback events routed to a `UNiagaraDataInterfaceCollisionQuery`. Bind the event via `UNiagaraComponent::GetBindings` + event handler delegates. This is rare; most teams use physics notifies instead.

11. Prefer `FNiagaraSystemScalabilitySettings` with proper LOD distance tiers over manually disabling distant effects in Blueprint. The scalability system integrates with the engine's device profile pipeline, which a manual `if (Distance > X)` check does not.

12. Async tick: Niagara emitters tick on task threads by default. Do not read `UNiagaraComponent` data (active particle count, etc.) from another system's async context without verifying completion of the Niagara tick group first.

13. When an effect is attached to a destroyed actor component, Niagara does not automatically null the pointer. Guard with `IsValid(NiagaraComp)` before calling setters; a dangling raw pointer through an unprotected UPROPERTY is safe (GC nulls it), but a raw non-UPROPERTY pointer is not.

14. For the gameplay-driven VFX pattern: gameplay event fires (damage dealt, ability activated) → C++ calls `SpawnSystemAttached` to the relevant socket → immediately calls typed setters for damage magnitude, hit direction, element type → system reads these as User-exposed parameters in the emitter stack and drives particle count, scale, color. Keep parameter naming in the system asset under a documented namespace convention (e.g., `User.DamageAmount`, `User.HitNormal`) to avoid string drift.

15. To stop a looping effect early, call `UNiagaraComponent::DeactivateImmediate()` for an instant cutoff or `Deactivate()` for a graceful completion of in-flight particles before shutdown. The distinction matters for effects like smoke trails where abrupt cutoff looks wrong.

16. When profiling, use the Niagara Debugger (`ni.DebugDraw.Enabled 1`) and the Niagara Stat screen (`stat Niagara`) to distinguish between spawn overhead, tick overhead, and render cost. They scale differently and have different remedies.

17. Emissive-driven light from a Niagara system (via Light Renderer module) creates dynamic lights per particle. Cap `MaxLightCount` aggressively on any system that spawns more than a handful of particles, or you will generate hundreds of dynamic lights per frame.

18. `UNiagaraSystem::GetPlaybackSpeed` and `SetPlaybackSpeed` on the component allow time-scaling individual effects — useful for slow-motion or ability charge previews without touching global world time dilation.

## Smells

- Calling `SpawnSystemAtLocation` and discarding the return value for an effect that has a non-trivial lifetime or needs to stop when gameplay state changes.
- Setting Niagara User parameters after `Activate()` on a spawn-once emitter and wondering why the values do not appear.
- Using a `UNiagaraParameterCollection` to store values that are unique per character — collections are global singletons; per-instance data belongs on the component via typed setters.
- Spawning a new `UNiagaraComponent` each frame for a continuous effect (thruster, aura) instead of holding one component active and updating its parameters.
- GPU emitters in a design that requires death events, collision callbacks, or per-particle game-logic responses.
- Missing `bAutoDestroy=false` on pooled components, causing pool entries to self-destruct and the pool to constantly re-allocate.
- No `UPROPERTY` annotation on a held `UNiagaraComponent*`, making it invisible to GC and leaving a dangling pointer when the owning actor is destroyed.
- Emissive light renderer with no `MaxLightCount` cap on a high-spawn-rate system.
- Hardcoding parameter names as raw `FName` literals scattered through multiple CPP files instead of centralizing them as constants — the first time the VFX artist renames a parameter, every callsite silently breaks.
- Relying on `SkyLight` or `PostProcessVolume` interaction with Niagara emissive light without checking that the Light Renderer module's `Use Inverse Squared Falloff` setting matches the project's lighting model.
- Not gating Niagara spawns behind scalability checks and letting low-end hardware run full-fidelity particle budgets.
- Attaching a Niagara component to a socket that is deleted at runtime (e.g., a weapon unequip that removes the socket) without detaching the component first, causing a silent transform snap to origin.

## Goal

This reference exists to keep Niagara C++ integration correct, lifecycle-safe, and performance-conscious from the first line of code. It covers the spawn API, parameter pipeline, pooling strategy, threading constraints, and scalability integration that separate a robust VFX system from one that leaks, misses cues, or breaks under load.

## Boundaries

- See `gameplay-ability-system.md` for how Gameplay Ability System events should trigger Niagara spawns via ability tasks rather than direct component calls.
- See `performance-profiling.md` for interpreting `stat Niagara` output and correlating Niagara cost with frame budget targets.
- See `animation-notifies.md` for routing character animation events to VFX spawns without coupling the animation Blueprint to C++ VFX management directly.
