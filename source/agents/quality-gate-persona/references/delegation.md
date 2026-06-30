---
name: delegation
metadata:
  version: "1.0"
---

# Delegation

## Purpose

This reference explains when and how Quality Gate should split a large review across focused sub-agents.

## When To Delegate

Run the core pass directly for small changesets.

Delegate when the changeset crosses multiple domains, has many changed files, or requires independent validation of tooling, rule enforcement, and architecture.

Good delegation boundaries include:

- Static analysis and tool-output interpretation.
- Scope and plan conformance.
- Rule enforcement against selected project rules.
- Domain architecture review.
- Test adequacy review.

## Sub-Agent Contract

Each delegated reviewer should:

- Wear the Quality Gate persona with a narrowed remit.
- Load only the references and rules required for its remit.
- Return findings in the standard report format.
- Label each finding with severity and certainty.
- Report tooling gaps and assumptions.

## Consolidation

The orchestrator de-duplicates findings, resolves conflicting severity calls, preserves uncertainty, and produces one final report with a single verdict.

Model selection belongs in provider metadata or invocation settings, not in prose that locks future tools into a specific model.
