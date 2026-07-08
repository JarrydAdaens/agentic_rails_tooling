---
name: advisor-guard-rail
description: >-
  A hook-enforced "quota advisor" guard rail for Claude Code: executor models
  (Opus/Sonnet) must consult a stronger Fable advisor subagent before their
  first write of a session. For anyone running Claude Code on a Max
  subscription who wants the native advisor-tool pattern without API access.
metadata:
  version: "0.1"
  status: proposed
  origin_project: Oracle
  origin_path: >-
    Oracle repository (local workstation), files under .claude/ plus the
    Quota Advisor Protocol section of CLAUDE.md; landed in commit 80880bd
    (2026-07-08)
  proposed_on: 2026-07-09
  suggested_destination: >-
    source/skills/ - as an installer-style skill that drops the advisor
    subagent, hooks, and CLAUDE.md protocol section into a target project
---

# Proposal: Advisor Guard Rail (Quota Advisor)

## What This Is

A deterministic guard rail that pairs cheaper executor models (Opus/Sonnet) with a stronger advisor: a read-only `advisor` subagent (`.claude/agents/advisor.md`, `model: fable`, tools Read/Grep/Glob, 120-word brevity contract). Three Claude Code hooks enforce consultation: a PreToolUse hook (`advisor_gate.py`) denies the first Write/Edit/MultiEdit/NotebookEdit of each session until one advisor consult has occurred, a PostToolUse hook on Task/Agent (`advisor_marker.py`) records consults as per-session marker files, and a SessionStart hook (`advisor_cleanup.py`) removes stale markers. The consult timing rules, structured payload contract (TASK / STAGE / PLAN-APPROACH / EVIDENCE / QUESTION), and model-conditional steering live in the Quota Advisor Protocol section of `CLAUDE.md`.

## Use Case

Anthropic's native advisor tool (executor model consults a stronger model mid-task) is API-only and unavailable on a Claude Max subscription. Oracle wanted the same behavior inside Claude Code: Opus/Sonnet sessions doing the actual work, with a mandatory Fable checkpoint before substantive changes, when stuck, before pivots, and before declaring completion — with the "consult before first write" rule enforced by a hook rather than left as advisory prose. Any project where executor sessions commit to a wrong interpretation early, or declare done prematurely, faces the same situation.

## Evidence It Works

Verified in the Oracle repository:

- Commit `80880bd` (2026-07-08) landed the full feature. Its message records live end-to-end validation: the advisor resolves and runs on `claude-fable-5`; a fresh session's first Edit is denied pre-consult and succeeds post-consult; markers do not bleed across sessions. It also documents the accepted v1 enforcement hole (Bash is deliberately ungated) and the Git Bash-on-Windows assumption.
- At slicing time, Oracle's `.claude/` contained three per-session consult marker files dated 2026-07-08/09 — direct residue of the gate/marker loop firing in real working sessions. (Markers are session state and were not copied.)

User-attested (not independently verifiable from the repo):

- The pattern was adopted after a fellow developer described the advisor pattern and sent the official Anthropic advisor-tool documentation; it proved very helpful in practice in Oracle.
- It has since been hand-copied to a second workstation (an ASUS ROG Ally, working on an RGB lighting plugin that signals battery level and charger adequacy), where it is in active use.
- It was shared with that fellow developer as a zip via Discord on 2026-07-09 — the demand for this proposal's shareable form is real, not hypothetical.

Supporting provenance: `context/quota-advisor-design.md` is the design document behind the implementation (problem statement, deviations from the native tool, architecture, risks). Note it was authored for a hand-assembled share of this feature and does not exist in the Oracle repository itself.

## Why Generalize It

The guard rail is entirely project-agnostic in mechanism: nothing in the hooks, agent, or protocol depends on Oracle's domain. Any Claude Code project on a Max plan that runs Opus/Sonnet executors benefits from a hard "consult a stronger model before your first write" checkpoint — it converts a best-practice from Anthropic's advisor-tool documentation into a deterministic hook. It has already spread by hand to a second machine and a second developer; an installer-style skill in the tooling repo would replace that manual copying.

## Contents Manifest

| Path | Role |
| --- | --- |
| `README.md` | This pitch. |
| `.claude/settings.json` | Fresh settings file containing only the three hook registrations the feature needs (PreToolUse gate, PostToolUse marker, SessionStart cleanup), with `$CLAUDE_PROJECT_DIR`-relative paths. |
| `.claude/hooks/advisor_gate.py` | PreToolUse hook: denies Write/Edit/MultiEdit/NotebookEdit until the session's consult marker exists; deny reason instructs the executor to consult first. Verbatim from Oracle. |
| `.claude/hooks/advisor_marker.py` | PostToolUse hook on Task/Agent: touches the per-session marker file when the invoked subagent is `advisor`. Verbatim from Oracle. |
| `.claude/hooks/advisor_cleanup.py` | SessionStart hook: deletes consult markers older than 24 hours. Verbatim from Oracle. |
| `.claude/agents/advisor.md` | The Fable advisor subagent: read-only tools, brevity contract, checkpoint-not-explorer role. Verbatim from Oracle. |
| `CLAUDE.md` | Excerpt: only the Quota Advisor Protocol section (consult timing, payload contract, model-conditional steering). Oracle's project heading and AGENTS.md pointer were left behind. |
| `context/quota-advisor-design.md` | Design document: native-tool behavior being replicated, accepted trade-offs, architecture, risks, out-of-scope items. Authored for a prior hand-made share, not present in the Oracle repo. |
| `.gitignore` | Two-line excerpt of Oracle's `.gitignore`: the consult-marker ignore pattern. Merge into a target project's existing `.gitignore`; do not overwrite. |
| `advisor-guard-rail.zip` | Snapshot of this proposal for sharing with other developers; regenerate after any edits. |

## Dependencies and Requirements

- Claude Code with hooks (PreToolUse / PostToolUse / SessionStart), project subagents (`.claude/agents/`), and the `$CLAUDE_PROJECT_DIR` hook environment variable.
- A plan on which the `fable` subagent model alias resolves. Fallback per the design doc: `model: opus` still gives Sonnet executors a genuine capability lift.
- Python 3 available on PATH as `python` (hooks use only the standard library).
- Hook commands use POSIX-style quoting; on Windows this assumes Claude Code's Git Bash hook execution (noted in the origin commit).

## Integration Sketch

Promote as an installer-style skill under `source/skills/` (e.g. `rails-advisor-setup`) that copies `.claude/agents/advisor.md` and `.claude/hooks/` into a target project, merges the three hook entries into the target's existing `.claude/settings.json` (rather than overwriting it), appends the Quota Advisor Protocol section to the target's `CLAUDE.md`, and adds the marker ignore pattern to the target's `.gitignore`. Parametrize the advisor model (fable vs opus). Do not carry over: per-session marker files, or any assumption that the target's `CLAUDE.md` is otherwise empty. The design doc's out-of-scope list (consult budgets, per-task gating, phase-gate integration) is the natural v2 backlog.

## Generalization Notes

- `CLAUDE.md` here is an excerpt; the section opens with "This project pairs executor models..." and assumes the executor/advisor pairing described above — fine as-is, but a promoted version should be written as an appendable block for arbitrary projects.
- `.claude/settings.json` was written fresh per the slicing rules, but Oracle's own settings file contained only these hooks, so the content is identical to the origin.
- The gate's deny message points the executor at "the consult payload format from CLAUDE.md" — the protocol section must accompany the hooks or the deny message dangles.
- Marker files are written to the target project's `.claude/`; the `.gitignore` excerpt exists to keep them out of version control and must be merged, not dropped in as a whole file.
- The advisor model is hardcoded to `fable` in the agent frontmatter; availability depends on plan/version (design doc, Risks 1-2).
- Bash is deliberately ungated (accepted v1 enforcement hole, documented in the design doc and origin commit).
- Gating is per-session, not per-task (documented v1 limitation).
