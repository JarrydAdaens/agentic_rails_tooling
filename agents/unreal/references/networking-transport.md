---
name: networking-transport
version: "1.0"
---

# Networking: Transport

## Use This Reference When
- Implementing or evaluating a custom transport layer, socket integration, or low-level network protocol in Unreal Engine
- Designing packet encoding, reliability, ordering, or flow control below the game-logic level
- Debugging raw connection issues, silent disconnects, packet loss, or bandwidth overruns
- Choosing between Unreal's built-in IpNetDriver and a custom transport backend

## Veteran Expert Stance
Transport is packet delivery. It is not game state, not session management, not replication — it is bytes moving between machines with some defined reliability and ordering contract. Keep this boundary sharp. Engineers who conflate transport with game architecture build systems that cannot be reasoned about, cannot be replaced, and cannot be profiled in isolation. A transport layer should be replaceable without touching game logic; if it is not, the abstraction has failed.

UDP is the correct protocol for real-time gameplay state. Its latency profile is predictable because it has no head-of-line blocking. A lost packet does not stall all subsequent packets the way a TCP retransmit does. This property is more important than the reliability guarantee. Reliability, ordering, and flow control are all implementable on top of UDP; they are not implementable on top of TCP's head-of-line blocking without adding latency you cannot remove. Use TCP for authentication handshakes, matchmaking API calls, and other high-latency-tolerant control flows where ordering and reliability matter more than speed.

Unreal's built-in IpNetDriver provides a functional UDP transport with a thin reliability layer, connection management, and integration with the actor replication system. It is adequate for most games. When it is not adequate — custom transport needed for relay infrastructure, deterministic lockstep, ultra-low-latency competitive play, or multi-platform peer-to-peer — the extension point is `UIpNetDriver` and `UIpConnection`. Do not fight the existing driver from within; replace or extend it at the right abstraction level.

## Core Concerns
- UDP as the gameplay transport primitive: fire-and-forget, no ordering guarantee, no head-of-line blocking
- Reliability as a layer on top of UDP: sequence numbers, ack windows, retransmit queues — not a freebie from the OS
- Packet size discipline: stay under the effective MTU (~1400 bytes) to avoid IP fragmentation, which destroys latency predictability
- Bit-level encoding: small packets mean less bandwidth; quantized, delta-encoded, bit-packed values are the tool
- Connection state machine: all connections must handle handshake, keepalive, and silent-disconnect detection explicitly
- Bandwidth budgeting: plan bytes-per-second-per-connection at target player count before writing a line of replication code

## Practical Heuristics

1. Default to UDP for any state that updates more than once per second. TCP introduces queued retransmits that can spike latency by hundreds of milliseconds during packet loss. For gameplay state this is unacceptable.

2. Unreal's `IpNetDriver` runs UDP with a custom reliability layer. When extending it, implement `UIpNetDriver` and override `ProcessRemoteFunction` and `TickDispatch`/`TickFlush` to intercept send and receive paths cleanly.

3. `FSocket` is Unreal's platform-abstracted socket. Create it via `ISocketSubsystem::Get()->CreateSocket(NAME_DGram, TEXT("GameSocket"), false)`. Always close and destroy it via the subsystem, not directly. Never call platform socket APIs directly in cross-platform code.

4. Run socket IO on a dedicated `FRunnable` thread. Non-blocking receive loops on the game thread will cause frame spikes during packet bursts. Use a ring buffer or thread-safe queue to pass packets between the IO thread and the game thread.

5. Use `FMemoryWriter` and `FMemoryReader` backed by a `TArray<uint8>` for in-memory binary serialization. The `<<` operator handles `int32`, `float`, `FVector`, `FQuat`, `FName`, `FString`, `bool`, and all standard UE types with correct endian handling.

6. Bit-pack small fields using `FBitWriter`/`FBitReader`. A boolean costs 1 bit, not 1 byte. A team index 0–7 costs 3 bits. Enum values with known ranges cost `FMath::CeilLogTwo(MaxValue)` bits. For high-frequency packets this difference compounds.

7. Quantize floats before sending. Position delta of ±512 cm at 0.5 cm precision fits in a uint16 (10 bits usable, 16 for alignment). Rotation at 1-degree precision fits in a uint8 per axis. Use `FRotator::CompressAxisToByte` and `FVector_NetQuantize` for common cases; the built-in quantization types are already tuned for gameplay scale.

8. Stay under 1400 bytes per packet. Ethernet MTU is 1500 bytes; subtract IP and UDP headers. Packets exceeding the effective MTU are fragmented at the IP layer. Fragmented packets have a much higher loss rate and reassembly adds latency. Fragment at the application layer if you must split data across packets, with your own sequence and reassembly.

9. For the reliability layer: assign each reliable packet a sequence number (uint16 wraps at 65535 — handle the wraparound). Receiver sends back an ack bitfield covering the last N sequences. Sender retransmits any sequence not acked within a timeout proportional to estimated RTT. The ACK bitfield approach (used by Quake and many others) is well-understood and cheap.

10. Unreliable send is the default for high-frequency gameplay state. If the packet is lost, the next update supersedes it. Only mark a message Reliable if missing it permanently breaks game state (spawn, death, round transition, score change). Reliable messages under sustained loss cause retransmit queues to grow and effective latency to spike.

11. Sequence numbers on unreliable packets still matter for discard. UDP can deliver packets out of order. An unreliable packet with a sequence number lower than the last processed sequence should be discarded, not applied — applying stale state causes visual jitter and potential desync.

12. A jitter buffer absorbs network timing variance at the cost of intentional latency. Hold incoming timestamped packets for 1–3 frames before consuming them. This smooths delivery without requiring retransmit. Use it on simulation-driven state (positions, animations); do not apply it to event-driven messages (damage, pickups).

13. Implement heartbeat / keepalive. Silent disconnects — the OS closes the connection without a FIN, or a NAT mapping expires — are invisible to the application layer without probing. Send a small keepalive packet every 2–5 seconds on idle connections. If no packet (keepalive or data) is received within a threshold (15–30 seconds), treat the connection as dropped.

14. The connection state machine has at minimum: Unconnected → Handshaking → Connected → Closing → Closed. Every state transition has an expected packet format and a timeout. Code that does not model the state machine explicitly accumulates edge-case bugs at handshake boundaries and under rapid connect/disconnect cycling.

15. Measure actual bytes per second per connection in production-representative conditions before shipping. The theoretical budget calculation is: `PacketsPerSecond * AverageBytesPerPacket * ConnectionCount`. Add 20% headroom for retransmits and overhead. If the budget does not fit the target platform's uplink, the encoding strategy is wrong — not the update rate.

16. Apply compression (LZ4 preferred for speed; zlib for ratio) only on payloads that are both large and compressible. Small fixed-size gameplay packets compress poorly and the compression overhead (CPU, latency) exceeds the savings. Profile before enabling.

17. Bandwidth asymmetry: typical consumer connections have much less uplink than downlink. Server-to-client bandwidth is your primary constraint for large player counts. Client-to-server is a constraint for input-heavy designs (high-frequency input streams). Plan both directions.

18. For custom peer-to-peer transport, STUN/TURN infrastructure is required for NAT traversal. EOS (Epic Online Services) provides relay and NAT punch-through. Rolling your own NAT traversal without platform support is an underestimated scope risk.

19. `OnlineSubsystem` (OSS) owns the connection establishment layer above the raw socket. It drives the `INetDriver` via session join/host flows. Custom transports that bypass OSS must replicate its handshake contract or the actor replication system will not initialize correctly.

20. Use Unreal's Network Profiler (`-networkprofiler` flag, or `NetworkProfiler.exe`) to capture per-frame bytes, bunch counts, and per-actor bandwidth. This is the ground truth for transport optimization, not intuition.

## Smells

- Using TCP for gameplay state under the assumption that reliability is worth the head-of-line blocking cost — it is not.
- Blocking socket reads on the game thread — causes frame spikes proportional to packet burst size and network timing variance.
- Sending packets larger than 1400 bytes without application-layer fragmentation — IP fragmentation silently destroys latency predictability.
- Using Reliable RPCs or reliable sends for every message regardless of whether loss is actually unrecoverable — retransmit queues spike latency under loss precisely when the game is most stressed.
- No sequence number on unreliable packets — out-of-order delivery applies stale state and causes visible jitter.
- No heartbeat or keepalive — silent disconnects go undetected for seconds or minutes, blocking reconnect logic.
- Applying zlib compression to small fixed-size packets — the compression header overhead exceeds the savings.
- Ignoring UDP wraparound on uint16 sequence numbers — causes spurious discard of valid packets after 65535 sequences.
- Conflating transport reliability with game-state consistency — reliable delivery does not mean state is correct; server authority is a separate concern.
- Not measuring actual bandwidth at target connection count before launch — the system looks fine at 4 players and collapses at 64.

## Goal

Provide precise, low-level guidance on the transport concerns relevant to Unreal Engine multiplayer: UDP socket usage, packet encoding, reliability and ordering layers, connection state management, and bandwidth budgeting. Keep transport concerns strictly separated from game architecture and replication so each layer can be reasoned about, profiled, and replaced independently.

## Boundaries
- Actor replication, RPCs, RepNotify, property delta encoding: see `networking-replication.md`
- Session lifecycle, matchmaking, prediction, rollback, game state architecture: see `networking-game-architecture.md`
