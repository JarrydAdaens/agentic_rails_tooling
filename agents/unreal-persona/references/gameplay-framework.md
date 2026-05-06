---
name: gameplay-framework
version: "1.0"
---

# Gameplay Framework

## Use This Reference When
- Diagnosing authority failures where server-only classes are accessed on clients (GameMode null crashes)
- Implementing PlayerController lifecycle events, pawn possession logic, or respawn flows
- Designing what state lives in GameMode vs GameState vs PlayerState vs PlayerController
- Working with seamless travel, persistent actors, or match state transitions

## Veteran Expert Stance
The most persistent class of networking bugs in Unreal projects comes from engineers ignoring the authority model of the gameplay framework classes. GameMode is server-only. Reading match state from GameMode on a client does not return stale data — it returns a null pointer to a class that does not exist on that machine. GameState is the replication surface for anything clients need to observe. The discipline of asking "which machines does this class exist on?" before writing any gameplay framework code eliminates an entire category of bugs before they compile.

PlayerController is frequently misunderstood because of its asymmetric existence: the server has all PlayerControllers, but each client has exactly one — its own. This means that code running on a PlayerController that walks across `GetWorld()->GetPlayerControllerIterator()` and assumes it has visibility into all players is server-only logic by definition. On the client, that iterator yields exactly one result. Engineers who do not internalize this ship multiplayer features that work correctly in PIE listen-server mode and silently break on dedicated server builds.

Match state design is a repeated source of architectural debt. Teams that start storing authoritative match progression state in GameMode fields, then later discover clients need to react to it, face a refactor at exactly the wrong time. The correct pattern from the start is: GameMode owns the rules and drives transitions, GameState holds the observable, replicated snapshot of match status. Any state that any client ever needs to read belongs in GameState, not GameMode.

## Core Concerns
- Authority distribution: which framework classes exist on which machines
- PlayerController lifecycle from login through pawn possession and death
- Correct placement of match state in GameState vs GameMode vs PlayerState
- Seamless travel: actor persistence, transition points, and what survives
- Match state machine: GameMode vs GameModeBase and the built-in state transitions
- Pawn spawning, player restart, and PlayerStart selection authority

## Practical Heuristics

1. GameMode exists on the server (and listen server) only. GetGameMode<T>() on a client returns null. This is not a race condition — GameMode is never created on clients. Any client-visible match data must be in GameState.

2. GameState exists on server and all clients. It is the correct replication surface for match-wide data: score, timer, team composition, match phase. If a client ever needs to read a value, it belongs in GameState.

3. PlayerController exists on the server for every connected player, but on each client only for that client's own controller. `GetFirstLocalPlayerController()` works on clients. Iterating all PlayerControllers is a server-only operation.

4. PlayerState exists on server and all clients. Use it for per-player data that must be client-visible: display name, score, ping, team assignment. It persists across seamless travel and is the correct place for per-player stats.

5. PlayerController is not the right place for data that clients other than the owner need to see. Controller data is visible only on the server and the owning client. Move it to PlayerState if other clients must observe it.

6. Pawn is null on the PlayerController until spawned and possessed. Always null-check `GetPawn()` before dereferencing. This is especially relevant in PostLogin and early lifecycle callbacks.

7. Possession fires on the server: Controller::Possess → Pawn::PossessedBy → OnPossess. The client is notified via OnRep_Controller on the Pawn. Client-side possession logic belongs in OnRep_Controller, not in PossessedBy.

8. When implementing death and respawn, UnPossess the pawn on the server, destroy or deactivate the pawn, then call RestartPlayer(PlayerController*) from GameMode. RestartPlayer calls ChoosePlayerStart and then SpawnDefaultPawnAtTransform. Do not call RestartPlayer on a client.

9. ChoosePlayerStart is the correct override for custom spawn point selection. It receives the PlayerController and returns an AActor (typically an APlayerStart). Override it in GameMode to implement team-based, distance-based, or priority-based spawn logic.

10. AGameModeBase has no match state machine. AGameMode adds WaitingToStart, InProgress, WaitingPostMatch, and LeavingMap states with the SetMatchState flow. Use AGameMode when you need match phases; use AGameModeBase for simpler game types.

11. StartMatch(), EndMatch(), and AbortMatch() drive state transitions in AGameMode. Override HandleMatchHasStarted and HandleMatchHasEnded to react to transitions. Do not call SetMatchState directly; use the provided transition functions which enforce valid state sequences.

12. ReadyToStartMatch and ReadyToEndMatch are the override points for custom start/end conditions. Return true when your game-specific conditions are met. The GameMode polls these every frame during the relevant wait states.

13. Seamless travel requires EnableSeamlessTravel = true in GameMode. Override GetSeamlessTravelActorList to add actors that should persist across travel. GameState, PlayerStates, and PlayerControllers are persisted automatically by the engine. Pawns are not.

14. During non-seamless travel (hard travel), everything is destroyed and rebuilt from scratch. Persistent data must be stored in the GameInstance or saved to disk before travel. Non-seamless travel is appropriate when loading screens are acceptable and state persistence is not required.

15. The HUD class is instantiated per PlayerController, on clients and listen servers only. Use it as the root for widget creation. Avoid placing authoritative game logic in HUD — it does not exist on dedicated servers.

16. SpawnActor for player pawns should always happen on the server via GameMode. Never call SpawnActor for a replicated pawn on a client — use RPC to request server-side spawn if client input is required.

17. When accessing GameMode immediately after world creation (e.g., in an early subsystem), guard with a null check. GameMode is not valid until the world has fully initialized.

18. InitGame fires before any player connects. PostLogin fires per player after login completes. GenericPlayerInitialization fires after InitPlayerState. Know which hook has valid PlayerState and which does not when writing per-player initialization logic.

19. GetGameState<T>()->ElapsedTime is replicated and incrementally updated. Do not maintain your own match timer replicated from scratch — use or extend GameState's built-in elapsed time to avoid drift.

20. Local player split-screen: each local player has a PlayerController and a LocalPlayer. GetLocalPlayer()->GetSubsystem<T>() is split-screen aware. GetFirstLocalPlayerController() returns only the first — iterate GetEngine()->GetAllLocalPlayerControllers() for split-screen scenarios.

## Smells

- Calling `GetGameMode<T>()` on a client and not handling null — GameMode does not exist on clients and this is a guaranteed crash path.
- Storing match-wide state (score, round number, match phase) in GameMode fields instead of GameState — clients can never observe it, and replication requires a refactor later.
- Accessing `GetPawn()` immediately in PostLogin without a null check — pawn is not spawned at this point in the lifecycle.
- Implementing respawn logic by calling `RestartPlayer` from a client RPC — RestartPlayer is a server-side GameMode function and has no authority on the client.
- Reading per-player visible data from PlayerController on a non-owning client — PlayerController is not replicated to non-owning clients.
- Using non-seamless travel when player stats need to survive the map change — non-seamless travel destroys PlayerState and all other actors unconditionally.
- Overriding `SetMatchState` directly instead of using `StartMatch`/`EndMatch` — bypasses valid-transition enforcement and produces invalid state sequences.
- Putting widget creation or UI root logic in the Pawn instead of HUD or PlayerController — Pawns are destroyed on death and respawned, but HUD and PlayerController persist across possession changes.
- Walking `GetPlayerControllerIterator` on a client expecting all players — yields only the local controller; this works in PIE and breaks silently on dedicated server builds with real clients.
- Keeping persistent cross-map state in GameInstance without a formal save/restore path — GameInstance survives travel but is not persisted across process restarts or crashes.

## Goal

Provide a precise authority and lifecycle map of the Unreal gameplay framework classes — GameMode, GameState, PlayerController, PlayerState, Pawn, and HUD — so that engineers can make correct decisions about where state lives, which machines execute which logic, and how player and match lifecycle events are safely handled in multiplayer and single-player contexts.

## Boundaries

- Low-level replication mechanics (NetRole, RPCs, property replication conditions): see `replication.md`
- Gameplay Ability System and ability granting on possession: see `gas.md`
- Subsystem-based game services that complement the framework: see `subsystems.md`
