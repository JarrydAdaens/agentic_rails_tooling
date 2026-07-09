---
name: rails-advisor-setup
description: >-
  Use this skill when the user asks to install, enable, or set up the advisor
  guard rail (quota advisor) in a Claude Code project — pairing executor
  models (Opus/Sonnet) with a stronger advisor sub-agent whose consultation is
  deterministically enforced by hooks. Triggers: "install the advisor",
  "set up the quota advisor", "add the advisor guard rail", "make this project
  consult a stronger model before writing". It copies the advisor agent and
  three hooks into the target project, merges hook registrations into
  settings.json, appends the consult protocol to CLAUDE.md, and validates the
  gate end to end.
metadata:
  version: "1.0"
---

# Rails Advisor Setup

Install the **advisor guard rail** into the current project: an actor–critic
pairing where executor sessions (Opus/Sonnet) must consult a stronger,
read-only `advisor` sub-agent at decision points — with the "consult before
your first write" rule enforced by a deterministic PreToolUse hook rather
than left as advisory prose. This replicates Anthropic's API-only advisor
tool inside Claude Code on a Max subscription. Full design rationale, native
tool comparison, and accepted trade-offs live in
`references/quota-advisor-design.md`.

This is an **installer skill**: its job is to copy and merge the payload in
`assets/` into the target project, not to teach a procedure. Never edit the
deployed copies in a target project to change the design — change the assets
here and reinstall.

## What gets installed

| Asset | Installs to | Role |
| --- | --- | --- |
| `assets/advisor.md.template` | `.claude/agents/advisor.md` | The advisor sub-agent: read-only tools (Read/Grep/Glob), 120-word brevity contract, checkpoint-not-explorer role. |
| `assets/hooks/advisor_gate.py` | `.claude/hooks/advisor_gate.py` | PreToolUse: denies the session's first Write/Edit/MultiEdit/NotebookEdit until a consult marker exists. |
| `assets/hooks/advisor_marker.py` | `.claude/hooks/advisor_marker.py` | PostToolUse on Task/Agent: touches the per-session marker when the invoked sub-agent is `advisor`. |
| `assets/hooks/advisor_cleanup.py` | `.claude/hooks/advisor_cleanup.py` | SessionStart: removes markers older than 24 hours. |
| `assets/settings-hooks.json` | merged into `.claude/settings.json` | The three hook registrations, `$CLAUDE_PROJECT_DIR`-relative. |
| `assets/advisor-protocol.md` | appended to `CLAUDE.md` | The Quota Advisor Protocol: consult timing, payload contract, model-conditional steering. |
| `assets/gitignore-snippet.txt` | merged into `.gitignore` | Ignore pattern for per-session consult markers. |

## Preconditions

- Claude Code with hooks (PreToolUse/PostToolUse/SessionStart), project
  sub-agents (`.claude/agents/`), and `$CLAUDE_PROJECT_DIR`.
- Python 3 on PATH as `python` (hooks use only the standard library).
- On Windows, hook commands assume Claude Code's Git Bash hook execution
  (POSIX-style quoting).

## Install procedure

1. **Choose the advisor model.** Default is `fable`. If the user's plan or
   Claude Code version does not resolve the `fable` alias, use `opus` — a
   Sonnet-executor/Opus-advisor pairing is still a genuine capability lift.
   Ask the user only if there is a real reason to deviate from the default.
2. **Copy the agent.** Create `.claude/agents/` if needed and copy
   `assets/advisor.md.template` to `.claude/agents/advisor.md`. If the chosen
   model is not `fable`, edit the `model:` frontmatter line in the copy.
3. **Copy the hooks** to `.claude/hooks/` (create the folder if needed).
   Copy verbatim; the scripts are project-agnostic.
4. **Merge hook registrations.** If `.claude/settings.json` does not exist,
   copy `assets/settings-hooks.json` to it wholesale. If it exists, merge:
   append each of the three entries into the matching `hooks.PreToolUse` /
   `hooks.PostToolUse` / `hooks.SessionStart` arrays, creating keys as
   needed. **Never overwrite an existing settings file**, and skip any entry
   whose command is already registered (idempotent re-install).
5. **Append the protocol.** Append the full contents of
   `assets/advisor-protocol.md` to the target's `CLAUDE.md` as its own
   section (create `CLAUDE.md` if the project has none). Do not assume the
   file is empty; do not duplicate the section if it is already present.
6. **Merge the gitignore lines** from `assets/gitignore-snippet.txt` into the
   target's `.gitignore`, skipping lines already present.
7. **Validate** (see below) and report what was installed, merged, and
   skipped.

## Validation

- Smoke-test the gate without a session: pipe a fake payload through each
  hook — `advisor_gate.py` with no marker present must emit a
  `permissionDecision: deny` JSON; `advisor_marker.py` with
  `tool_input.subagent_type: "advisor"` must create the marker file;
  `advisor_gate.py` must then exit clean. Delete the test marker afterward.
- Confirm the three registrations appear in `.claude/settings.json` and the
  agent file parses (frontmatter `name: advisor`, chosen `model:`).
- Full proof needs a fresh session: the first Edit is denied with the
  instructive reason, and succeeds after one advisor consult. Tell the user
  to expect exactly that behavior — the deny is the feature working, not an
  error.

## Known limitations (accepted v1 trade-offs)

- **Bash is deliberately ungated** — reliably classifying read-only vs.
  state-changing shell commands in a hook is fragile; the protocol text
  covers Bash advisorily. Do not "fix" this during install.
- **Per-session, not per-task**: a long multi-task session only forces one
  consult.
- The advisor sees only the structured consult payload, not the transcript;
  thin payloads produce poor advice. The payload contract in the protocol is
  the mitigation.
