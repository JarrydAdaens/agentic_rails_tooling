---
name: networking-game-architecture
metadata:
  version: "1.1"
---

# Networking: Game Architecture

## Use This Reference When
- Designing the session lifecycle, lobby-to-match flow, or matchmaking pipeline for a multiplayer game
- Implementing or extending client prediction, dead reckoning, or server reconciliation
- Defining the boundary between client-authoritative and server-authoritative state
- Evaluating rollback netcode, host migration, or deterministic simulation for a given game genre

## Veteran Expert Stance
Game network architecture is the design of trust, time, and state across machines with different views of reality. Transport delivers packets; replication delivers properties; game architecture decides what exists where, who owns it, who can change it, and how disagreements are resolved. These are three separate concerns. Engineers who merge them produce systems where changing the update rate breaks prediction, or where fixing a cheat surface requires rewriting the session model.

The fundamental architectural choice is where the server's authority boundary falls. Everything on the authoritative side must be validated, never trusted from clients. Everything on the prediction side must be reconcilable — the client can run ahead, but the server's word is final, and the client must be able to rewind and accept corrections without visible artifacts. Drawing this boundary wrong is the most expensive architectural mistake in multiplayer game development. It is also the most common one: teams ship with too much on the client side, then spend a cycle hardening against cheaters and fixing desyncs.

Unreal's framework gives you GameMode (server-only, match lifecycle), PlayerController (one per connection, straddles server and client), PlayerState (replicated, persists across transitions), and CharacterMovementComponent (has prediction and correction built in). These are load-bearing abstractions. Work with their intended model before extending or replacing them. The temptation to bypass them to ship faster is real; the cost of untangling a custom system that fights the framework is higher.

## Core Concerns
- Session lifecycle: create, start, update, end, destroy — each phase has expected server state, UI state, and transition logic
- Client prediction: clients run authoritative-looking simulation locally; the server corrects them; clients reconcile without artifacts
- Server authority boundary: which state is server-owned and validated, which is predicted and reconcilable, which is fully client-side
- Cheat surface: every piece of state the client reports rather than computes server-side is a cheat vector
- Dead reckoning and extrapolation: bridge server update intervals with local simulation between snapshots
- Match state machine: GameMode drives transitions; PlayerControllers and PlayerStates carry per-player context across them

## Practical Heuristics

1. `FOnlineSession` wraps platform-specific session concepts (Steam lobbies, EOS sessions, LAN). The lifecycle is: `CreateSession` → `StartSession` → (optional `UpdateSession`) → `EndSession` → `DestroySession`. Skipping steps or calling them out of order produces platform-specific failures that are hard to reproduce. Bind to the completion delegates (`OnCreateSessionComplete`, `OnStartSessionComplete`, etc.) and check the success parameter before advancing.

2. Separate lobby and match sessions in design and code. A lobby session holds pre-game configuration state (map vote, ready status, player list). A match session holds in-game state (score, round, alive players). They have different data, different lifetimes, and different transition conditions. Conflating them into one session object creates state management debt that accumulates throughout development.

3. Dead reckoning: when a server update arrives, compare the predicted position to the received position. If the delta is within a snap threshold, smoothly interpolate. If it exceeds the threshold, teleport (or use a fast lerp). The threshold is genre-dependent: a strategy game tolerates 50 cm; a competitive shooter tolerates 2 cm. Tune per game, not per engine default.

4. Client prediction for movement: the client sends a move (input + timestamp + duration) to the server. The client also applies the move locally and stores it in a pending moves buffer. The server applies the move authoritatively and sends back the resulting position. If client and server positions agree within tolerance, the client discards the old pending move. If they disagree, the client rewinds to the server state and re-simulates all pending moves forward. This is CMC's model — extend it, do not replace it for character movement.

5. Saved moves in CMC: `FSavedMove_Character` holds the inputs and result of one client move. Custom movement modes require a custom `FSavedMove` subclass that captures all inputs needed to reproduce the move from the server state. Forgetting to capture a custom input variable produces irreconcilable desyncs that appear only under packet loss.

6. Reconciliation artifacts (rubber-banding) are the visible symptom of a reconciliation that is too coarse or too slow. The root causes are: prediction error is too large (physics diverges), the correction is applied as a teleport (no blending), or the server-side simulation is nondeterministic (float precision, tick rate mismatch). Diagnose with `p.NetShowCorrections 1`.

7. Rollback netcode requires a deterministic simulation: given the same input and state, every machine produces exactly the same output. This rules out floating-point operations that vary across compilers, frame-rate-dependent physics, and any stochastic system (random without a shared seed). Unreal's physics engine is not deterministic across platforms by default. Rollback is architecturally viable in Unreal, but requires replacing or wrapping large subsystems to guarantee determinism. It is the right choice for fighting games and RTS; it is the wrong choice for open-world shooters.

8. The cheat surface rule: clients send intentions (move input, aim direction, ability activation). The server computes outcomes (new position, damage dealt, ability effect). Any system where the client sends an outcome rather than an intention is a cheat vector. Damage numbers from the client, position teleports from the client, item state from the client — all are exploitable. The validation pipeline must reject out-of-range values, impossible transitions, and physically unreachable positions.

9. Lag compensation for hitscan weapons: the server rewinds its collision history to the time at which the client fired (client timestamp, validated against RTT bounds), runs the trace against the rewound state, and evaluates the hit. This is the correct approach for competitive shooters. It requires a server-side position history buffer (ring buffer, 200–500 ms of depth is typical). Unreal does not provide this out of the box; it must be implemented.

10. GameMode is server-only. It should own the match state machine: WaitingToStart → InProgress → WaitingPostMatch → LeavingMap. Drive transitions via `SetMatchState`. Client-visible match state (round timer, score) belongs on `GameState`, which is replicated.

11. PlayerController is the network connection anchor. One PlayerController exists per connected client on the server. On the client, only the local PlayerController exists; remote players' controllers are not present. `PlayerController` is the correct location for server RPCs that require a verified owning connection. Avoid routing Server RPCs through Pawns, weapons, or other actors unless ownership is explicitly and correctly set.

12. PlayerState is replicated and survives pawn respawn and map transitions (with `SeamlessTravel`). It is the correct location for persistent per-player data: score, kill count, team, display name. Do not store transient gameplay state in PlayerState; it replicates to all clients and its update frequency is not tuned for high-frequency state.

13. `SeamlessTravel` allows the server to transition maps while keeping PlayerController and PlayerState alive. Non-seamless travel destroys and recreates everything, losing all in-memory state. For any game with persistent session state (score, progression), seamless travel is required. Set `bUseSeamlessTravel = true` in GameMode.

14. Host migration: in a listen-server model, the host leaving kills the session. EOS and Steam both provide host migration primitives. Unreal's `MigrateNewHost` and related machinery in the base engine provide scaffolding, but the state transfer (game state, scores, world state) is the responsibility of the game. True robust host migration is one of the most expensive features in multiplayer development. Scope it explicitly; do not assume it is a consequence of using sessions.

15. Prediction zones — the explicit design decision: identify each piece of game state and classify it as (a) fully predicted (local character movement, camera, cosmetic effects), (b) predicted with reconciliation (pawn position, character animation driven by movement), or (c) server-authoritative with no client prediction (damage, item pickup, score, ability cooldowns). Document this classification. Ambiguous state is where bugs and exploits live.

16. Matchmaking flow: the correct sequence is player searches for session → finds sessions → joins session (lobby) → lobby reaches start condition → server transitions to match → match runs → match ends → server sends players back to lobby or disconnects. Each arrow is an async operation with a failure case. Model the failure cases, not just the happy path.

17. Input sequence numbers: even when not doing full rollback, attach a monotonically increasing sequence number to every client input packet. The server can detect dropped inputs, detect replayed inputs (potential cheat), and report back the last processed sequence so the client knows what to discard from its pending buffer.

18. Time synchronization: client clock and server clock drift. For lag compensation and prediction to work correctly, the client must have an estimate of the current server time. Implement NTP-style clock sync at session start: client sends a timestamp, server echoes it back with server time, client computes RTT and offset. Rerun periodically. `AGameState::GetServerWorldTimeSeconds` provides a replicated approximation; for competitive play, a custom sync is more precise.

19. `APlayerController::GetPing()` returns a smoothed RTT estimate in quarter-milliseconds. Use it to bound lag compensation rewind depth (do not accept rewind requests deeper than `MaxPing * 1.5`). An unbounded rewind depth is an exploit vector for clients with artificially inflated reported ping.

20. Network relevancy and prediction interact. If an actor becomes relevant to a client while the client has a predicted state for it, the initial replicated state from the server must override the predicted state. Failure to handle this produces ghost actors or duplicate state at the moment of relevancy transition.

21. For abilities and game logic that fire from the client (predicted activation): use a prediction key system. The client generates a unique key, sends it with the Server RPC, and speculatively applies the ability locally. The server validates, applies authoritatively, and echoes back the key. The client confirms or reverts the speculative application when it receives the echo. GAS (Gameplay Ability System) implements this pattern.

## Smells

- Clients sending outcome data (damage dealt, item taken, new position after teleport) instead of input data — cheat surface and authoritative state violation.
- Calling `CreateSession` without binding to `OnCreateSessionComplete` — fire-and-forget session management fails silently on errors.
- Using `PlayerState` for high-frequency gameplay state — it replicates to all clients and is not frequency-tuned for per-frame data.
- Putting logic that should be server-authoritative in `GameMode` but checking it on the client because GameMode is not present there — client code that assumes server state without verification.
- Dead reckoning without a snap threshold — every server correction causes a visible pop; every interpolation lags behind a turning entity.
- Implementing CMC custom movement without overriding the saved move subclass — prediction works only in straight-line cases, desync under loss.
- No sequence numbers on client inputs — server cannot detect dropped, replayed, or reordered inputs.
- Seamless travel disabled for a game with persistent session state — player data is destroyed and recreated on every map change.
- Treating GAS ability prediction as "automatic" without understanding prediction keys — speculative effects persist past server rejection.
- Rollback netcode attempted on non-deterministic subsystems — simulations diverge, corrections are continuous, the game becomes unplayable under any packet loss.
- Lag compensation rewind depth unbounded by client RTT — clients can request arbitrarily old server state, enabling hit registration exploits.

## Goal

Provide expert-level guidance on the game architecture layer of Unreal multiplayer: session lifecycle, match state, client prediction, server authority, reconciliation, and the design boundaries that separate trustworthy from exploitable state. Keep these concerns strictly separate from transport and replication so the architecture can be evaluated, designed, and debugged as its own layer.

## Boundaries
- UDP sockets, packet encoding, reliability layer, bandwidth budgeting: see `networking-transport.md`
- Property replication, RPCs, RepNotify, replication conditions, actor channels: see `networking-replication.md`
