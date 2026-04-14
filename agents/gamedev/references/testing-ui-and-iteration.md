---
name: testing-ui-and-iteration
version: 1.0
---

# Testing, UI, and Iteration

## Use This Reference When

- The task touches unit tests, smoke tests, replay systems, UI workflows, previews, or development iteration speed
- You need to decide what should be tested versus what should be exercised in-game
- The current UI or gameplay workflow is too slow and boring to validate efficiently

## Expert Stance

Unit tests are a tool, not a KPI.

Never chase coverage numbers. Test deterministic, stable, low-level systems aggressively. Gameplay code usually changes too quickly for heavy unit-test scaffolding to pay off. Validate gameplay with smoke tests, replay systems, known-input execution, and real runs of the game.

UI also needs fast iteration. Do not waste time booting the whole game just to inspect a widget. Use mocks, previews, isolated harnesses, and rapid inspection workflows.

## Core Rules

- Do not chase code coverage percentages as a proxy for quality.
- Aggressively test deterministic, stable, low-level systems such as math, serialization, networking edges, replay systems, or deterministic simulation.
- Default gameplay code to few or no unit tests unless there is a very strong case.
- Validate gameplay with smoke paths, replay data, scripted inputs, and actual execution.
- Build UI workflows that support previews, mocks, isolated assembly, and rapid iteration.
- Optimize testing and UI workflows for developer throughput and reduced boredom.

## High-Signal Quotes

- "Never write unit tests for gameplay."
- "You need mocks, you need previews, you need to be able to assemble your UI without having to execute the entire game."

## Practical Heuristics

- If a system is deterministic and catastrophic when wrong, test it hard.
- If a system is design-heavy and changing weekly, prefer smoke coverage over brittle assertion scaffolding.
- If checking a UI state requires a full boot sequence, invest in a harness before adding more features.
- If a test suite keeps blocking harmless gameplay iteration, the suite is probably aimed at the wrong layer.

## Common Mistakes

- Treating test coverage as a badge of seriousness instead of asking what failures actually matter
- Building brittle low-level tests around fast-moving gameplay behavior
- Forcing UI validation through slow full-game launches that destroy iteration speed
- Assuming no automated checks are needed just because gameplay unit tests are often a poor fit
