---
description: "Comparison of agentic IDE capabilities, configuration models, workflow primitives, and repository strategy implications."
metadata:
  version: "0.2"
  owner: "Jarryd Adaens"
---

# Agentic IDE Capability Comparison Report

[Back to Wiki Home](home.md)

## Executive Summary

The current landscape of agentic IDEs is converging toward a standardized "Agent Brain" model, primarily utilizing the `SKILL.md` standard for procedural knowledge and `AGENTS.md` or `.cursorrules` for high-level instructions. However, significant variations exist in configuration precedence, automation hooks, and Model Context Protocol (MCP) handling.

## Major Patterns and Strengths

**Rules & Instructions:** Cursor is transitioning from `.cursorrules` to `.cursor/rules/*.mdc` with YAML frontmatter and glob scoping. Antigravity and OpenCode use hierarchical rule systems (Global vs Workspace).

**Skills:** Most platforms adopt folder-based `SKILL.md`. Antigravity and Cursor lead in progressive disclosure (load-on-demand).

**Personas & Agents:** Antigravity supports parallel orchestration via Mission Control. Codex has experimental subagents using `.toml` definitions.

**Workflows:** Windsurf and OpenCode provide the most mature deterministic workflow systems (DAGs, approval gates).

**Hooks:** Windsurf uniquely provides lifecycle hooks capable of blocking execution.

**MCP Support:** Nearly universal, but config formats differ (TOML vs JSON).

---

## IDE Capability Comparison Table

| IDE | Project Instructions | Global Instructions | AGENTS.md | SKILL.md | Rules (Glob/Path) | Personas / Subagents | Workflows | Hooks | MCP Support | Project-local .agents | Best Use Case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Antigravity | Supported | Supported | Not Supported | Supported | Supported | Supported | Supported | Partial / Unclear | Supported | Supported | Autonomous multi-agent orchestration |
| Cursor | Supported | Supported | Workaround / Adapter | Supported | Supported | Supported | Partial / Unclear | Not Supported | Supported | Supported | Context-aware, rule-heavy development |
| OpenCode | Supported | Supported | Supported | Supported | Supported | Supported | Workaround / Adapter | Partial / Unclear | Supported | Supported | Deterministic, plugin-driven automation |
| Windsurf | Supported | Supported | Supported | Supported | Supported | Not Supported | Supported | Supported | Supported | Partial / Unclear | Enterprise governance and safety |
| Codex | Supported | Supported | Supported | Supported | Partial / Unclear | Experimental | Partial / Unclear | Not Supported | Supported | Supported | CLI-first, OpenAI-native workflows |
| Claude Code | Supported | Supported | Workaround / Adapter | Supported | Partial / Unclear | Not Supported | Partial / Unclear | Experimental | Supported | Supported | Terminal-centric coding tasks |

### Legend

| Marker | Meaning |
| --- | --- |
| Supported | Capability is supported |
| Not Supported | Capability is not supported |
| Partial / Unclear | Capability is partial or unclear |
| Experimental | Capability is experimental |
| Workaround / Adapter | Capability requires a workaround or adapter |
| Deprecated | Capability is deprecated |

---

## Individual IDE Analysis

### Google Antigravity

1. Configuration Model: Global (`~/.gemini/`) + workspace (`.agents/`)
2. Monitored Folders: `.agents/skills/`, `.agents/workflows/`
3. Rules: `GEMINI.md` (global), `.agents/rules/` (workspace)
4. Agents: Mission Control for parallel orchestration
5. Hooks & MCP: Tool-level permissions + MCP via context
6. `.agents` Compatibility: Native
7. Recommendation: Best for complex multi-agent tasks

---

### Cursor

1. Configuration Model: `.cursor/rules/*.mdc` replacing `.cursorrules`
2. Monitored Folders: `.cursor/skills/`, `.agents/skills/`
3. Rules: YAML frontmatter with glob scoping
4. Agents: Subagents + auto-applied skills
5. Hooks & MCP: MCP via `mcp.json`, no hooks
6. `.agents` Compatibility: High
7. Recommendation: Best for rule-heavy, scoped development

---

### OpenCode

1. Configuration Model: `opencode.json` + `.opencode/`
2. Monitored Folders: `.opencode/skills/`, `.agents/skills/`
3. Rules: `AGENTS.md`, hierarchical resolution
4. Workflows: Mastra-based DAG execution
5. Hooks & MCP: Tool permissions + MCP support
6. `.agents` Compatibility: Native
7. Recommendation: Best for deterministic workflows and team use

---

### Windsurf (Cascade)

1. Configuration Model: System -> User -> Workspace hierarchy
2. Monitored Folders: `.windsurf/`
3. Rules: `AGENTS.md` + rules + memories
4. Workflows: Cascade automation system
5. Hooks & MCP: Full lifecycle hooks system
6. `.agents` Compatibility: Limited
7. Recommendation: Best for enterprise control and enforcement

---

### Codex

1. Configuration Model: `%USERPROFILE%/.codex` + `AGENTS.md`
2. Monitored Folders: `.agents/skills/`, `.codex/agents/`
3. Rules: `AGENTS.md`
4. Agents: Experimental subagents via `.toml`
5. Hooks & MCP: MCP via `config.toml`
6. `.agents` Compatibility: Native
7. Recommendation: Best for CLI-driven workflows

---

### Claude Code

1. Configuration Model: `~/.claude/`
2. Monitored Folders: `.claude/`, `.agents/`
3. Rules: Installer-mapped markdown
4. Skills: `SKILL.md` support
5. Hooks & MCP: Basic hooks + MCP
6. `.agents` Compatibility: High via adapters
7. Recommendation: Best for terminal-first workflows

---

## Synthesis: Cross-IDE Repository Strategy

### Canonical Root Strategy

Maintain a single neutral repository as the source of truth and transform outputs per IDE.

```text
.agents/
|-- AGENTS.md
|-- rules/
|   `-- code-style.md
|-- skills/
|   `-- researcher/
|       |-- SKILL.md
|       `-- scripts/
`-- workflows/
    `-- deploy.yaml
```

---

## IDE Targeting Strategy

### Canonical Targets

- Antigravity
- OpenCode
- Codex

These natively support `.agents/` with minimal transformation.

### Adapter Targets

**Cursor**

- Convert rules -> `.mdc`
- Map skills -> `.cursor/skills`

**Windsurf**

- Translate rules -> `hooks.json` or memories

**Codex MCP**

- Convert JSON -> TOML (`config.toml`)

---

## Key Insight

Kung Fu should not treat IDEs as file destinations.

It should treat them as:

> Capability-driven targets with transformation requirements

Each IDE:

- Supports different primitives
- Requires different formats
- Has different execution models

Kung Fu's role becomes:

> Canonical -> Capability-aware transformation engine

This is the foundation for Milestone 3.
