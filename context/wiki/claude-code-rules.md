---
name: claude-code-rules
description: How Claude Code loads and scopes rule files (`paths:` frontmatter, load timing, size limits) — read before touching source/rules/.
metadata:
  version: "1.0"
---

# Claude Code Rules — Configuration & Format Reference

Purpose: reference doc for cleaning up a `~/.claude/rules/` repository. Written for a Claude Code instance to act on.

Source: official Claude Code memory docs, https://code.claude.com/docs/en/memory (fetched 03 July 2026). Version-specific behaviour noted inline.

---

## 1. The two things Claude Code loads

1. **CLAUDE.md files** — instructions you write. Loaded at session start.
2. **`.claude/rules/*.md`** — modular rule files. Loaded at session start, OR only when matching files are touched (if path-scoped).

Both are **context, not enforcement.** Claude reads them and tries to comply. Nothing guarantees compliance. To *block* an action regardless of what Claude decides, use a `PreToolUse` hook or `permissions.deny` in settings — not a rule.

---

## 2. Where rules live

| Location | Scope | Load priority |
| --- | --- | --- |
| `~/.claude/rules/*.md` | User — every project on the machine | Loaded before project rules |
| `<project>/.claude/rules/*.md` | Project — shared via source control | Loaded after user rules (higher priority) |

All `.md` files are discovered recursively, so subdirectories (`frontend/`, `backend/`) work. User-level rules are for personal, non-project-specific preferences.

---

## 3. Correct frontmatter format

Claude Code uses **one** frontmatter key for scoping: `paths`. Nothing else.

### Path-scoped rule (loads only for matching files)

```markdown
---
paths:
  - "**/*.cpp"
  - "src/**/*.h"
---

# C++ Rules
- Rule one
- Rule two
```

### Always-loaded rule (no frontmatter, or no `paths` field)

```markdown
# Global Rules
- Applies to every file, every session
```

### Multiple patterns / brace expansion

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

### Glob pattern reference

| Pattern | Matches |
| --- | --- |
| `**/*.ts` | All TypeScript files, any directory |
| `src/**/*` | All files under `src/` |
| `*.md` | Markdown files in project root only |
| `src/components/*.tsx` | React components in one directory |

Matching is plain glob-vs-filepath. No regex, no LLM judgment. File path matches a glob → rule loads. No match → rule stays out.

---

## 4. Keys that DO NOTHING in Claude Code (strip these)

These are **Cursor / Windsurf** frontmatter keys. Claude Code ignores them:

- `globs:` — Cursor's equivalent of `paths:`. Rename to `paths:`.
- `alwaysApply:` — Cursor-only. Delete. (In Claude Code, presence/absence of `paths:` controls this.)
- `description:` — Cursor-only. Delete.
- `metadata:` (version, owner, etc.) — not read by Claude Code. Delete or keep only as human reference; it costs context tokens.

A rule file with only `globs:`/`alwaysApply:` frontmatter and no `paths:` field will load **unconditionally** in Claude Code, because Claude Code sees no `paths:` key to scope it. The Cursor scoping is invisible.

---

## 5. The bug (and current status)

**Historical bug (GitHub #21858, early 2026):** rules with `paths:` frontmatter placed in `~/.claude/rules/` (user level) were silently ignored — never loaded, even for matching files. Workaround at the time: move path-scoped rules to project-level `.claude/rules/`, or make user-level rules unconditional (remove `paths:`).

**Current status (per official docs, 03 July 2026):** the docs now explicitly document `~/.claude/rules/` with `paths:` frontmatter as supported. Separately, v2.1.198 fixed path matching through symlinked checkouts. This indicates the user-level path-scoping bug is resolved in current versions.

**Action for the cleanup instance:**
1. Run `claude --version`.
2. If well past v2.1.198 (mid-2026+), treat user-level `paths:` scoping as working. Verify with step 4 below.
3. If uncertain or on an older build, fall back to the workaround: keep path-scoped rules at **project level**, keep only unconditional rules at user level.

Certainty note: the resolution is inferred from current official docs documenting the feature as supported plus the v2.1.198 symlink fix. If exact behaviour matters, verify empirically with `/memory` (below) rather than trusting this doc.

---

## 6. How to verify what actually loaded

Run `/memory` inside a session. It lists every CLAUDE.md, CLAUDE.local.md, and rules file loaded, with paths. This is the ground-truth debugging tool — never assume a rule loaded; check.

To confirm path-scoping works: open a session, `/memory` (note which rules are present), then read/edit a `.cpp` file, then `/memory` again. A correctly-scoped C++ rule should appear only after the C++ file is touched.

Optional: the `InstructionsLoaded` hook logs exactly which instruction files load, when, and why — useful for debugging path-specific rules.

---

## 7. Size limits

- Target **under 200 lines** per file. Longer reduces adherence.
- Hard limit **~40,000 characters** per memory file (`MAX_MEMORY_CHARACTER_COUNT`). Files over this are flagged and may not be fully read.
- Imports (`@path/to/file`) help organisation but do NOT save context — imported files load in full at launch.

---

## 8. The `index.md` file — delete it

An `index.md` that routes the agent to "load only relevant rule files" is a **Cursor-era pattern** and does nothing useful in Claude Code. Claude Code loads rules automatically via `paths:` glob matching by the client — it does not read a markdown index and make routing decisions. The index just burns context tokens describing a mechanism that isn't how the tool works. Remove it.

This repository's `source/rules/` followed exactly this pattern until it was fixed: `index.md` was deleted, and every rule file now carries only a `paths:` block (or no frontmatter at all for the always-loaded global rules). See [repo-alignment-notes.md](repo-alignment-notes.md) for the resulting frontmatter carve-out.

---

## 9. Cross-tool portability (context, not required for cleanup)

- **Rules are NOT a cross-tool standard.** Each tool differs: Claude Code (`paths:`), Cursor (`globs:`), Copilot (`.github/copilot-instructions.md`), Windsurf (`.windsurfrules`).
- **`AGENTS.md`** is the emerging cross-tool project-instructions standard (plain markdown, no frontmatter, read by 28+ tools). Claude Code reads it only as a fallback when no CLAUDE.md exists; it prefers CLAUDE.md. `AGENTS.md` has no glob scoping — it loads whole, so it can't do progressive disclosure on its own.
- **Skills (`SKILL.md`)** ARE a real cross-tool standard (agentskills.io), but are task-scoped ("when I run /lint"), not file-scoped ("when editing C++"). Wrong shape for language conventions.

If a single source of truth across tools is the goal: pick Claude Code `paths:` format as canonical, then write per-tool converters (e.g. `paths:` → `globs:` for Cursor). AGENTS.md handles the unscoped/global rules cleanly across all tools. In this repository, that per-tool conversion is deferred to the external `kung-fu` deployment app, which will run copy-time conversion scripts against this Claude-Code-first `source/rules/` rather than this repo hand-maintaining a duplicate file per IDE.

---

## 10. Cleanup checklist for this repository

For each rule file in the repo:

- [ ] Replace `globs:` with `paths:`.
- [ ] Delete `alwaysApply:`, `description:`, `metadata:` keys.
- [ ] Confirm glob patterns are quoted (YAML requires quoting for patterns starting with `*` or `{`).
- [ ] Global/always-on rules (global-rules, unit-testing): remove any `paths:` field entirely so they load unconditionally.
- [ ] Language/framework rules (C#, WPF, C++, Qt, React, TypeScript): keep `paths:` scoped to the right extensions.
- [ ] Delete `index.md`.
- [ ] Delete `.cursorrules` from `~/.claude/rules/` (Claude Code does not read it there; keep it only in Cursor projects if still using Cursor).
- [ ] Delete `Desktop.ini` (Windows cruft, not a rule).
- [ ] Run `/memory` to confirm the intended files load, and confirm path-scoped ones load only when matching files are touched.
- [ ] Decide user-level vs project-level placement per section 5 based on installed version.
