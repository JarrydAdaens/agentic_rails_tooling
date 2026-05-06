---
name: networking-replication
version: "1.0"
---

# Networking: Replication

## Use This Reference When
- Implementing or debugging replicated actors, components, or properties in Unreal Engine
- Tuning replication frequency, conditions, or relevancy for performance
- Deciding whether built-in replication fits the game's fidelity and scale requirements
- Diagnosing state desync, OnRep misfires, or RPC delivery failures

## Veteran Expert Stance
Built-in Unreal replication is a property-delta system over UDP. It is well-suited for prototypes, co-op games, and casual multiplayer at modest player counts. It is NOT a production multiplayer architecture for competitive games — ranked shooters, fighting games, or anything where 16ms of authoritative error is unacceptable — without substantial custom work layered on top or alongside it. Ship with built-in replication knowing its ceiling, not assuming it scales to any design. The ceiling is lower than most engineers expect.

The mental model is: the server owns truth, clients receive snapshots. A replicated property is not a live shared variable; it is a periodic broadcast of the last known server value, compressed against what the server believes the client already has. The client's copy is always behind, potentially by several frames. Every design decision in a networked game must account for that latency and the mismatch it creates between what players experience locally and what the server considers authoritative.

RPCs are point-in-time imperative messages, not guaranteed state. They can be dropped if the connection is unreliable and the RPC is not marked Reliable. Reliable RPCs are sequenced and retransmitted, but they are not ordered relative to property updates. Treat RPCs as events, not synchronization mechanisms. If state must be consistent at the client, replicate the property; if a discrete event must fire, use an RPC or a RepNotify.

## Core Concerns
- Property-based delta replication over UDP, driven by server-side dirty tracking per connection
- RPC ownership model: clients can only call Server RPCs on actors they own via PlayerController chain
- RepNotify semantics: fires only on clients, only on change, not guaranteed on initial replication without the correct condition
- NetUpdateFrequency and bandwidth budget: replication has a cost per actor per connection per tick
- Relevancy and culling: actors only replicate to clients for whom they are relevant, controlled by distance and custom overrides
- Channel overhead: each replicated actor opens a channel per connection; at scale this is a hard constraint

## Practical Heuristics

1. Set `bReplicates = true` in the constructor, not BeginPlay. Actors that need replication must declare it before the server decides to replicate them. Setting it late causes missed initial replication windows.

2. Implement `GetLifetimeReplicatedProps` for every class that has `UPROPERTY(Replicated)` or `UPROPERTY(ReplicatedUsing=...)`. Missing this causes a runtime ensure and the property will not replicate.

3. Use `DOREPLIFETIME_CONDITION` over bare `DOREPLIFETIME` as the default choice. The condition narrows bandwidth: `COND_OwnerOnly` for personal state (health, ammo of this player), `COND_SkipOwner` for state irrelevant to the owning client, `COND_SimulatedOnly` for proxies, `COND_InitialOnly` for immutable setup data.

4. RepNotify (`ReplicatedUsing=OnRep_X`) fires on the client after the property is written from replication. It does NOT fire on the server. It does NOT fire on the initial net load unless you use `COND_InitialOrOwner` or call the function manually. Never rely on OnRep for initialization without accounting for this.

5. Server RPCs require the calling client to own the actor. The canonical ownership chain is `PlayerController → Pawn`. If a client needs to trigger a Server RPC on a non-Pawn actor (e.g., an interactable), route it through the PlayerController with a Server RPC, then forward server-side to the target actor.

6. Client RPCs only reach the owning client. Dedicated servers have no owning connection by default. Use `SetOwner(PlayerController)` explicitly on actors that need to receive Client RPCs from the server.

7. Multicast RPCs execute on all clients that have the actor as relevant. If relevancy culls the actor for a connection, that client does not receive the multicast. Never use multicast as a guarantee that all clients see an event.

8. Reliable RPCs are sequenced. If the channel backs up (packet loss spike), all subsequent reliable RPCs wait behind the backlog. Overusing Reliable RPCs can stall game-critical messages behind cosmetic ones. Tag only what is truly unrecoverable if dropped.

9. `NetUpdateFrequency` defaults are too high for many actor types. Background NPCs, environmental actors, and vehicles at distance should run 5–10 Hz. Important player-visible actors can run 20–30 Hz. High-frequency projectiles are often better handled via spawn + deterministic sim rather than replication.

10. Use `SetNetUpdateTime(GetWorld()->TimeSeconds - 1.f)` to force an immediate replication push in the next server tick. Use this after state changes that must not wait for the next scheduled window (e.g., death, round end).

11. `IsNetRelevantFor` controls the relevancy check per connection per tick. Override it for game-specific rules (line of sight, team visibility, fog of war). Use `NetCullDistanceSqrd` for the common case of distance-based relevancy cutoff; it is checked before `IsNetRelevantFor` and is cheaper.

12. `bNetLoadOnClient` controls whether a level-placed actor is spawned on the client via level streaming. Dynamically spawned actors do not use this flag; they replicate or they do not exist on the client.

13. CharacterMovementComponent replication is not property replication. CMC has its own compressed move data, client prediction, and correction pipeline. Do not add `UPROPERTY(Replicated)` to replicate character velocity or position — that fights CMC and produces double-correction. Extend CMC's `FSavedMove` system instead.

14. Actor channels have memory and CPU cost per connection. With 100 players and 500 replicated actors, you approach 50,000 active channels. At that scale the built-in system degrades. Profile channel count before shipping large-scale designs.

15. Property replication is frame-rate-independent from the replication standpoint — updates are sent at `NetUpdateFrequency`, not every game tick. Client interpolation and smoothing must bridge the gaps. Design visual state to tolerate the update interval.

16. Subobject replication requires registering subobjects via `AddReplicatedSubObject` (UE5) or `GetReplicationList` (pre-UE5). UActorComponents with `SetIsReplicated(true)` handle registration automatically when attached to a replicated actor. Bare `UObject` subobjects require explicit registration.

17. The server never receives its own property replication. The server also never fires OnRep. If you rely on OnRep to drive server logic, you have a design error. Server state must be managed independently.

18. For competitive accuracy where built-in replication falls short: use custom server-authoritative movement with lag compensation, server-side rewind buffers, and explicit hit validation. Replication gives you a scaffold; it does not give you the validation pipeline.

19. Debug replication with `Net.Stats 1`, `p.NetShowDebug`, and the Network Profiler. Measure actual bytes per actor per second before tuning. Intuition about what is expensive is often wrong.

20. `COND_InitialOnly` properties are sent once when the actor first becomes relevant to a connection. If a client disconnects and reconnects, or if relevancy resets, the server sends them again. Use for immutable configuration (team assignment, archetype type) not for state that changes.

## Smells

- Adding `UPROPERTY(Replicated)` without implementing `GetLifetimeReplicatedProps` — silent failure.
- Using bare `DOREPLIFETIME` for all properties regardless of audience — wastes bandwidth and leaks information to clients that should not have it.
- Calling a Server RPC on an actor the client does not own — silently dropped, no error in shipping builds.
- Relying on OnRep firing on the server — it does not; this creates a server-client logic split that is hard to trace.
- Using Multicast RPC as a substitute for reliable state delivery — it is not reliable and relevancy can exclude clients.
- Replicating raw position/velocity on a character actor that uses CMC — conflicts with prediction and correction.
- Setting `NetUpdateFrequency` uniformly across all actor types — background actors should update far less frequently.
- Trusting a Client RPC to reach a dedicated server-spawned actor that has no owner set — Client RPCs require owning connection.
- Treating replication as a synchronous call — it is not; the client sees state after one or more network round-trip delays.
- Never profiling channel count or bytes-per-second before going to scale — the system looks fine in playtests with 4 players and collapses at 64.
- Putting business logic inside OnRep functions — OnRep is a notification callback, not a state machine driver.
- Using `COND_InitialOnly` for mutable state — the client's copy becomes stale and the condition prevents future updates.

## Goal

Provide precise, actionable guidance on Unreal Engine's built-in property replication and RPC system, covering correct usage, known limitations, and the architectural ceiling that should drive decisions about whether built-in replication fits the game's design. Enable engineers to implement correct replicated actors and identify when the system needs to be augmented or replaced.

## Boundaries
- Transport layer concerns (UDP, sockets, packet encoding): see `networking-transport.md`
- Session lifecycle, matchmaking, prediction architecture, host migration: see `networking-game-architecture.md`
- CharacterMovementComponent internals: covered in movement-specific references
