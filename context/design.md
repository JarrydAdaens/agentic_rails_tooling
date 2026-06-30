---
name: agentic-rails-tooling-design
description: The purpose, structure, and design decisions behind agentic_rails_tooling, the right rail of the Agentic Rails framework.
metadata:
  version: "1.0"
  owner: Jarryd Adaens
---

# Agentic Rails Tooling — Design

This document explains *why* this repository is shaped the way it is. `README.md` describes
the layout for day-to-day use; this file records the intent and the design decisions behind
it so the structure can be maintained or changed deliberately rather than by accident.

## Purpose

`agentic_rails_tooling` is the **right rail** of Agentic Rails. Its job is to hold reusable,
portable agent capability — the durable "how an agent should behave while working" knowledge
that is not specific to any one project. It answers a single question:

> How should agents behave while working, and what reusable machinery do they have to do it?

It deliberately contains almost no executable application code. The artifacts are Markdown
(`SKILL.md`, `AGENT.md`, rules, references) plus prompt source material and a few supporting
scripts. There is no build, test, or lint step. "Correctness" means well-formed artifacts
that obey the naming and frontmatter conventions.

## Place In The Framework

Agentic Rails is a framework name, not a single repository. Three rails divide the work, and
each rail has one responsibility it must not hand to another:

- **Left rail — `agentic_rails_context_starter`**: project-local context and provenance.
  Where project knowledge lives (design, milestones, sprints, stories, plans, handovers).
- **Right rail — `agentic_rails_tooling` (this repo)**: reusable behaviour. Rules, skills,
  workflow-skills, personas, and the logic that captures, curates, and rebuilds memory.
- **Center rail — `agentic-rails-memory`**: durable, markdown-only cross-project artifacts
  (learnings and Resumes). Artifacts only — never the logic that produces or consumes them.

The split matters because it keeps responsibilities clean. Project-local context stays
authoritative for a project; this repository supplements it with reusable behaviour but never
overrides a project's design, plans, or decisions. The memory rail stores the track record;
the *logic* that reads and writes that record lives here, in the right rail, so routing
decisions remain self-owned and data-driven.

## The `source/` And `context/` Split

The most important structural decision is the separation of deployable artifacts from
everything else.

- **`source/`** is the only tree that is deployed. It holds `rules/`, `skills/`, and
  `agents/`. The external `kung-fu` WPF app syncs `source/` outward into the folder layouts
  that different IDEs expect, or into the shared `%USERPROFILE%\.agents` workspace.
- **`context/`** holds everything *about* the repository: this design document, scaffolds
  (`templates/`), prompt source history (`prompt-dev/`), and local spec notes (`wiki/`). None
  of it is deployed.

This split exists so that the deploy boundary is obvious and mechanical: a tool can sync
`source/` without needing rules about which subfolders to skip. Supporting material that would
only add noise to a deployed IDE configuration stays in `context/`, `archived/`, or
`ide_specific/`.

## The Three Primary Layers

Inside `source/`, capability is placed in the narrowest layer that fits.

- **`source/rules/`** — short, prescriptive engineering standards and style guidance, routed
  by `index.md`. If a rule file grows into procedural expertise, it has outgrown the layer and
  belongs in a skill.
- **`source/skills/`** — portable, task-shaped capability. A skill says "here is how to do this
  task." Large orchestrations that coordinate subagents, queues, or durable artifacts use the
  `-workflow` suffix so they remain discoverable in ordinary skill pickers.
- **`source/agents/`** — named specialist personas. A persona says "here is the kind of worker
  you are." Folder name and `name` end in `-persona`. Each bundle carries `AGENT.md`, an
  optional vendor adapter (`<persona>.toml` plus provider metadata), and a `references/`
  library loaded on demand.

Skills and personas are intentionally distinct primitives: a skill is a verb (do this task), a
persona is a noun (be this worker). Conflating them erodes progressive disclosure.

## Progressive Disclosure

The whole repository is built around the Agent Skills model of discovery → activation →
execution. An agent should see cheap metadata (`name`, `description`) first, then load full
instructions, references, and scripts only when a task needs them. This is why long detail
lives in `references/` files and why descriptions are written as "Use this when…": the
description is often the only thing an agent reads before deciding whether to engage.

## Naming Conventions

- File and folder names use **kebab-case** (`commit-log-template.md`, `wpf-rules.md`), not
  `snake_case` or `PascalCase`.
- Tool-recognized fixed names are preserved: `SKILL.md`, `AGENT.md`, `README.md`,
  `SECURITY.md`, `AGENTS.md`, `CLAUDE.md`, `AGENTIC_RAILS_README.MD`, `.cursorrules`, and
  `.gitkeep`.
- Code files keep their language idioms; Python and JavaScript follow the conventions their
  ecosystems expect rather than being forced into kebab-case.
- Persona folders and `name` fields end in `-persona`; orchestration skills end in `-workflow`.
- Every artifact carries YAML frontmatter with a quoted `metadata.version`. The
  `rails-clean-frontmatter` skill normalizes frontmatter across the repo.

## Supporting Areas

- **`archived/`** preserves artifacts that still have reference value but are superseded or no
  longer worth exposing. It mirrors the main categories (`agents/`, `skills/`, `rules/`) and is
  never part of the normal sync set.
- **`ide_specific/`** is a deliberate junk pile for nonportable vendor files. It accommodates
  the messiness of real tools without letting any single IDE define the architecture.
- **`context/templates/`** holds blank scaffolds. Authors copy a template into a `source/`
  folder, then rename and fill it in.
- **`context/prompt-dev/`** preserves the prompt source material behind generated artifacts —
  often the real design history of a skill or persona.
- **`context/wiki/`** captures the parts of the AgentSkills.io specification this repository
  relies on, plus local alignment decisions.

## Key Design Decisions

- **No standalone `workflows/` folder.** A separate workflow primitive was an early mistake
  carried over from another IDE's mental model. Agentic IDEs generally do not understand it, so
  workflows now live in `source/skills/` with a `-workflow` suffix. This keeps them
  discoverable through normal autocomplete while still signalling their orchestration role.
- **Deploy boundary is a single folder.** Moving the active artifacts under `source/` makes the
  one-way `source/ -> Kung Fu -> IDE` sync trivial to reason about.
- **Context is consolidated.** Templates, prompt history, and wiki notes are all *about* the
  repository, so they live together under `context/` instead of cluttering the root.
- **Artifacts only in memory.** The right rail owns the logic that operates on memory; the
  center rail stores the resulting artifacts. Keeping logic and data apart is what makes the
  framework's routing decisions trustable.

## Boundaries

This repository should contain reusable agentic machinery and the logic that captures, ranks,
curates, and rebuilds memory artifacts. It should **not** contain project-local context (that
is the left rail), memory artifacts themselves (that is the center rail), or secrets,
credentials, and proprietary source pulled from any project.
