---
name: skill-template-advanced
description: Use this template when creating a broad Agent Skill that needs progressive disclosure, focused reference files, routing guidance, examples, and validation without loading all domain knowledge up front.
metadata:
  template: "true"
  version: "1.1"
  agentic_rails_source_version: "1.1"
---

# Advanced Progressive-Disclosure Skill Template

This template is for building large skills that represent a real expertise domain without turning the main skill file into a monolith.

Use it when the domain is broad enough that the agent needs:

- A stable high-level stance in the main skill
- A modular reference library for deeper guidance
- Selective loading so only relevant knowledge is pulled into context

This is especially useful for skills derived from layered professional expertise, such as UI engineering, game development, framework-specific architecture, tooling ecosystems, or other domains where the agent needs both breadth and restraint.

## Template Goal

Treat the main skill as the router and operating model, not the full body of knowledge.

The main file should answer:

1. What kind of domain this skill covers
2. How the agent should think when using it
3. How to choose which reference modules to load
4. What defaults, boundaries, and quality standards should shape the work

The reference files should hold the deeper domain truth in focused chunks.

## Progressive Disclosure

This template uses progressive disclosure to keep broad expertise usable.

Instead of one giant knowledge file:

- Put the shared stance, workflow, and routing logic here
- Split domain expertise into focused reference files
- Load only the smallest relevant reference set for the task

As a rule of thumb, each reference should stay tight and single-purpose. If one section starts carrying multiple concerns, split it into smaller modules. For domains built from compact knowledge slices, aim for roughly 500-character chunks of guidance where that still preserves clarity.

## Working Style

Start by identifying what kind of problem the user is actually solving. Do not load every reference file up front.

Think in this order:

1. What is the user trying to build, change, debug, evaluate, teach, or formalize?
2. Which expertise layer is actually in play: principles, architecture, workflows, implementation patterns, tooling, quality, diagnostics, or performance?
3. What belongs in the core solution, what belongs in support systems, and what belongs in process or validation?
4. Which reference files provide enough domain truth without pulling in unrelated context?

Prefer the least complex solution that still respects the domain. Treat the skill as a catalogue first and a deep reference set second.

## Default Stance

- Prefer clarity over cleverness.
- Prefer focused modules over bloated reference files.
- Prefer explicit boundaries between domain concerns.
- Prefer selective loading over broad context dumps.
- Prefer reusable guidance that can be specialized into derived skills.
- Prefer validation, diagnostics, and real acceptance checks over confidence alone.
- Prefer replacing placeholders with real domain truth when creating a concrete skill from this template.

## Included Example References

This template currently ships with three example reference files. They are examples of the structure, not final domain content.

- [references/reference_1.md](references/reference_1.md)
  Example reference module. Use it as a placeholder for one focused expertise slice, then rename and rewrite it for the real domain.
- [references/reference_2.md](references/reference_2.md)
  Example reference module. Use it to model a second domain slice that should stay separate from the first.
- [references/reference_3.md](references/reference_3.md)
  Example reference module. Use it to model a third domain slice, especially when the skill needs clear progressive loading choices.

When deriving a real skill, replace these example files with domain-specific modules such as architecture, workflows, rendering, systems design, testing, content pipelines, or framework mechanics.

## How to Use the Example References

The three example references are intentionally minimal. They exist to show how the main skill should link to modular domain files.

Typical use:

- Keep this main file generic and domain-aware
- Rename `reference_1.md`, `reference_2.md`, and `reference_3.md` to meaningful domain names
- Rewrite each file so it owns one clear concern
- Update the links and usage notes in this file once the real references exist

If the domain grows, add more references only when they represent a genuinely separate concern.

## Reference Loading Guidance

Load these references only when they are relevant to the task at hand.

- Use one reference when the task is narrow and clearly belongs to one expertise slice.
- Use two references when the task crosses a boundary, such as architecture plus implementation, or tooling plus diagnostics.
- Use three or more only when the work truly spans multiple layers and the added context is necessary.

The goal is not to prove coverage. The goal is to load just enough expertise to solve the actual problem well.

## Execution Checklist

When using this template or any skill derived from it:

1. Identify the real problem before loading references.
2. Load only the smallest reference set that gives enough domain truth.
3. Keep the main skill focused on stance, routing, and decision quality.
4. Keep detailed domain knowledge in references, not in the core file.
5. Split references when one file starts covering multiple independent concerns.
6. Verify outcomes with tests, examples, diagnostics, or another concrete check.
7. Replace placeholder example content before treating a derived skill as production-ready.

## Do Not

- Do not turn this file into a full knowledge dump.
- Do not refer to reference files that do not actually exist in the template.
- Do not load every reference module unless the task truly needs them.
- Do not keep placeholder examples in place once real domain guidance is available.
- Do not merge unrelated expertise layers into one oversized reference file.
- Do not confuse breadth of knowledge with quality of routing.
