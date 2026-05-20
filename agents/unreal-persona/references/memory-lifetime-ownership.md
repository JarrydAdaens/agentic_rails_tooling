---
name: memory-lifetime-ownership
version: "1.0"
agentic_rails_source_version: "1.0"
---

# Memory, Lifetime, and Ownership in Unreal C++

## Use This Reference When
- Diagnosing crashes that involve null or dangling UObject pointers
- Designing cross-system references between actors, components, or subsystems
- Working with async operations, timers, or latent actions that hold UObject references
- Auditing a class for GC safety, memory leaks, or missing UPROPERTY anchors

## Veteran Expert Stance
Unreal's GC is a mark-and-sweep collector that traces from GC roots through UPROPERTY fields. The single most important mental model is reachability: a UObject lives as long as at least one live GC root can reach it through a chain of UPROPERTY references. Any raw `UObject*` field that lacks `UPROPERTY` is invisible to the collector. The GC will collect that object on the next sweep even if your pointer is non-null — you now hold a dangling pointer, and the crash is non-deterministic depending on when GC runs.

The upgrade to TObjectPtr in UE5 is not cosmetic. In editor and debug builds, TObjectPtr adds access tracking and lazy pointer resolution, which surfaces use-after-GC bugs at the point of access rather than at the point of crash. Treat `TObjectPtr<T>` as the canonical form for any UPROPERTY-marked owned reference. The implicit conversion to `T*` means existing code patterns still compile, but you get instrumentation for free.

Async code is where GC ownership goes wrong most often. Lambdas, timer delegates, and latent action callbacks all close over state at bind time. If that state is a raw `UObject*`, GC will not know the lambda is holding a reference and may collect the object before the callback fires. The pattern is always the same: capture a `TWeakObjectPtr<T>`, check `IsValid()` at the top of the callback, and bail out gracefully if the object is gone. This is not optional defensive coding — it is the contract the GC enforces.

## Core Concerns
- GC reachability: a UObject is only live if reachable from a root via UPROPERTY chains
- Pointer semantics: owned (TObjectPtr), non-owning (TWeakObjectPtr), deferred load (TSoftObjectPtr / TSoftClassPtr)
- Async safety: timers, delegates, and lambda captures must not hold raw UObject* references
- Outer chain: every UObject's lifetime is coupled to its Outer's lifetime
- Object validity: `IsValid()` over raw null checks; raw null misses pending-kill state
- FGCObject: the bridge for non-UObject C++ classes that must protect UObject references

## Practical Heuristics

1. **Default to `TObjectPtr<T>` for all UPROPERTY member fields.** In UE5, any `UPROPERTY UObject*` should be `TObjectPtr<T>`. The API is compatible; the tooling benefit is real.

2. **Non-UPROPERTY `UObject*` members will be GC'd.** There are no exceptions. If you cannot mark it UPROPERTY, either use `TWeakObjectPtr` (and accept the object may vanish) or inherit `FGCObject` and implement `AddReferencedObjects`.

3. **`IsValid(Ptr)` is the canonical validity check.** It returns false for null and for pending-kill objects. A raw null check passes for a pending-kill object that is about to be swept. This is the source of many hard-to-reproduce crashes.

4. **Always capture `TWeakObjectPtr` in lambdas.** When a timer, async load, or latent task closes over a UObject, capture via `TWeakObjectPtr<UMyClass> WeakThis(this)`. At callback time, call `WeakThis.Get()` or `WeakThis.IsValid()` before any dereference.

5. **Timer delegates do not prevent GC.** `FTimerManager::SetTimer` with a bound method holds a `FTimerDelegate`. If the bound UObject is GC'd between the bind and the fire, the delegate fires on a dead `this`. Always clear timers in `EndPlay` or `BeginDestroy` using `GetWorldTimerManager().ClearTimer(Handle)`.

6. **Clear timers before calling Super::EndPlay.** The timer manager is still valid at that point. After Super, the world may be shutting down.

7. **Component lifetime is coupled to actor lifetime.** After an actor's `Destroy()` or natural end-of-life, its components are pending-kill. Store component pointers only in contexts that are also bounded by actor lifetime. Never cache a component pointer in a long-lived subsystem without making it a `TWeakObjectPtr`.

8. **PIE invalidates all object pointers on session end.** Objects from a previous PIE world are non-null but belong to a dead world. The check is `IsValid(Ptr) && Ptr->GetWorld() == GetWorld()`. Caches that survive BeginPlay/EndPlay cycles must be cleared in `EndPlay`.

9. **`NewObject<T>(Outer)` — the Outer must outlive the created object.** If the Outer is destroyed first, the new object becomes orphaned and may be collected unpredictably. For objects that need to persist regardless of gameplay context, use `GetTransientPackage()` as the Outer and manage cleanup explicitly.

10. **`AddToRoot` is a last resort, not a pattern.** It makes a UObject a GC root unconditionally. Forgetting `RemoveFromRoot` before shutdown creates a permanent leak. Prefer proper UPROPERTY anchoring or `FGCObject` instead.

11. **`TSoftObjectPtr<T>` means the asset is not loaded.** Accessing `.Get()` on an unloaded TSoftObjectPtr returns null. You must resolve it via `FStreamableManager::RequestAsyncLoad` or `UAssetManager::GetStreamableManager()`. Do not call `LoadSynchronous()` on the game thread in production paths — it stalls.

12. **`TSoftClassPtr<T>` belongs in data assets for spawnable configuration.** It avoids hard references that pull the entire asset into the cook. Use it for character class configs, ability class lookups, and anything driven by data tables. Resolve to a `TSubclassOf<T>` at spawn time via `LoadSynchronous()` only if you can prove the class is already in memory (e.g., already streamed in).

13. **`TWeakObjectPtr::IsValid()` is a two-gate check: not null AND not pending-kill.** Prefer `IsValid()` over `Get() != nullptr`. The `.Get()` form returns null for pending-kill but the IsValid path reads more clearly and documents intent.

14. **Outer chain inspection via `GetOuter()` and `GetOutermost()`.** GetOutermost() gives you the UPackage. If the package is the transient package, the object is not serialized. Use this to reason about whether an object will survive PIE resets and level transitions.

15. **`FGCObject::AddReferencedObjects` must add every UObject* the class holds.** If you add a member and forget to update `AddReferencedObjects`, you have an invisible GC hole. Structure it as a flat list of `Collector.AddReferencedObject(MemberPtr)` calls that mirrors every `UObject*` field.

16. **Subsystems are GC anchors.** `UGameInstanceSubsystem`, `UWorldSubsystem`, and `UEngineSubsystem` are UPROPERTY-anchored by their owning managers. You can safely store `TObjectPtr` members inside them. Their `Initialize`/`Deinitialize` lifecycle is the correct place to set up and tear down references.

17. **`UObject::ConditionalBeginDestroy()` is not a destructor.** Do not assume the C++ destructor timing aligns with GC collection. Objects can be pending-kill while still addressable in memory. Design teardown logic around `BeginDestroy` and `FinishDestroy`, not the destructor.

18. **Avoid storing TArray<UObject*> without UPROPERTY.** Arrays of UObject pointers have the same GC visibility problem as single pointers. `UPROPERTY() TArray<TObjectPtr<UMyType>>` is the correct form.

19. **UObject references inside FStructs are GC-visible only if the struct is itself UPROPERTY-anchored.** A USTRUCT containing a `TObjectPtr<UMyType>` member is traced by GC only when the struct instance is held by a UPROPERTY. A plain heap-allocated USTRUCT is invisible.

20. **Weak references in delegates: use `CreateWeakLambda` or `CreateUObject` with appropriate guards.** `CreateUObject` on a `FSimpleDelegate` will not fire if the bound object is pending-kill — this is the correct behavior. `CreateWeakLambda` provides the same safety for arbitrary lambdas. Never bind a raw lambda that captures `this` if `this` is a UObject and the delegate lifetime exceeds the object.

21. **Async asset loading callbacks must validate the loaded asset.** `FStreamableManager::RequestAsyncLoad` callbacks fire even if the requesting object was destroyed during the load. Check `IsValid(RequestingObject)` at the top of the callback before touching any gameplay state.

22. **Do not rely on `UPROPERTY(Transient)` for GC anchoring.** Transient suppresses serialization, not GC tracing. A `UPROPERTY(Transient)` field is still a valid GC anchor — use it for runtime-only state that should not be saved but must be kept alive.

## Smells

- `UMyClass* MyRef;` as a member field with no UPROPERTY — invisible to GC, will cause non-deterministic crashes
- `if (MyPtr != nullptr)` instead of `IsValid(MyPtr)` — misses pending-kill objects
- Timer bound to `this` with no `ClearTimer` in `EndPlay` — dangling delegate after GC
- Lambda capturing raw `UObject*` in an async path — GC-invisible capture
- `AddToRoot` without a paired `RemoveFromRoot` in teardown — permanent leak
- `NewObject<T>` with a short-lived Outer, then storing the result somewhere longer-lived — mismatched lifetime contract
- Loading `TSoftObjectPtr` via `LoadSynchronous` on the game thread during gameplay — frame stall
- Accessing a component pointer after the owning actor's `Destroy()` — component is pending-kill
- FGCObject subclass with UObject* members missing from `AddReferencedObjects` — silent GC hole
- Caching actor or component pointers across PIE sessions without world validity checks — stale world reference
- Using `GetTransientPackage()` as Outer for objects that should be serialized — they will not be saved
- Storing `UObject*` inside a heap-allocated USTRUCT not anchored by any UPROPERTY — GC-invisible

## Goal
Provide authoritative, immediately actionable guidance on Unreal GC semantics, pointer type selection, and async lifetime contracts. Every heuristic must be specific enough to apply directly to a code review or a crash investigation without additional context.

## Boundaries
- For animation object lifetime (UAnimInstance, montage delegates): see `animation.md`
- For subsystem design patterns and their lifetime guarantees: see subsystem reference when available
- For async loading and asset streaming strategy: see asset-streaming reference when available
