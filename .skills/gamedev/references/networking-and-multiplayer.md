---
name: networking-and-multiplayer
version: 1.0
---

# Networking and Multiplayer

## Use This Reference When

- The task touches multiplayer, replication, sync, late joins, packet budgets, recovery, or approximation strategies
- You need to classify traffic by importance, timeliness, and acceptable loss
- The current design is trying to synchronize too much state too literally

## Expert Stance

Networking is a bandwidth, reliability, and illusion-management problem.

Do not synchronize full state naïvely just because it is convenient. Decide what must arrive, what may be dropped, and what can be approximated or reconstructed. Use dead reckoning and other illusion-preserving strategies where exactness is unnecessary for the experience.

## Core Rules

- Classify traffic deliberately as reliable or unreliable based on gameplay need.
- Decide consciously between TCP-like and UDP-like delivery strategies rather than defaulting blindly.
- Optimize for bandwidth cost, arrival relevance, and packet usefulness.
- Avoid full-state synchronization when approximation or event streams can carry the experience.
- Plan for late-join sync, fragmentation, compression, and recovery as first-class concerns.
- Treat the network model as part of the game design, not just a transport detail.

## Practical Heuristics

- If a packet is useless after a short delay, treat it as disposable rather than fighting to preserve it forever.
- If a late join requires a full world snapshot, decide what can be compressed, fragmented, or replayed as edits.
- If the game feels wrong without exact arrival ordering, be very explicit about which packet classes actually require it.
- If the wire format is bulky, question the replicated representation before trying to outsmart the transport.

## Common Mistakes

- Trying to mirror full game state across the network because it feels conceptually simple
- Treating all packets as equally important or equally durable
- Ignoring late-join recovery until the rest of multiplayer is already built
- Forgetting that approximation is often the correct player-facing solution
