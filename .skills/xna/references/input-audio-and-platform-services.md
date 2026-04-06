---
name: input-audio-and-platform-services
version: 1.0
---

# Input, Audio, and Platform Services

## Use This Reference When

- The task touches keyboard, mouse, gamepad, touch, audio playback, or platform-specific services
- You are deciding how input state should be sampled and exposed
- You need stable access points for platform-specific behavior without drowning the project in abstraction

## Expert Stance

Poll input in `Update`, keep edge detection explicit, and use platform seams only where they buy something real.

Game code benefits from central access patterns. Small interfaces, partial classes, or subsystem swaps can help when platform differences matter, but they should stabilize a seam rather than hide the whole game from itself.

## Core Rules

- Sample current and previous input states in `Update` and derive pressed, released, and held semantics explicitly.
- Keep input policy clear: raw device state, interpreted actions, and rebinding logic should not be scrambled together.
- Centralize audio and platform services enough that gameplay code stays readable.
- Use interfaces or partial implementations when backend swaps or platform differences are real.
- Keep service access practical and visible rather than burying simple systems under ceremony.
- Document platform-specific assumptions around input devices, focus behavior, audio, and deployment.

## Practical Heuristics

- If input bugs are intermittent, inspect sampling order and previous-state management first.
- If platform differences are isolated to a small area, keep the seam local.
- If gameplay code keeps reaching into device-specific details, introduce a clearer action layer.
- If audio playback logic is duplicated across screens and systems, centralize the policy without overengineering it.

## Common Mistakes

- Sampling input in scattered places so edge detection becomes inconsistent
- Abstracting every device interaction before a real platform problem exists
- Hiding platform assumptions until deployment-specific bugs become surprising
- Letting audio policy sprawl across unrelated systems
