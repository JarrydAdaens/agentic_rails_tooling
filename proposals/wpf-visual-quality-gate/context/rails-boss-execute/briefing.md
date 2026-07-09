---
name: rails-boss-execute-briefing
description: Durable briefing for the Milestone 3 execution runs (Stories 29-31, then the 2026-07-05 Stories 32-43 batch).
metadata:
  version: "0.3"
---
# Rails Boss Execute Briefing

## Run Scope

This run implements the **three remaining Not Started stories** in `context/milestones/milestone-3.md`: Story 29 (Cursor), Story 30 (Claude probe hardening), Story 31 (Antigravity probe replace-or-harden). Stories 1-28 are already Complete (Stories 8-28 were delivered in the prior boss run recorded in the git history and the superseded `goals3.md` queue).

> **Run 2026-07-05 addendum:** a follow-up run delivered Stories 32-43 (post-use feedback batch: provider-data enrichment + UX refinement), executed serially in-session rather than via subagents, under the same hard constraints below (data-source proof first, no estimation, build + full tests + live probe/UIA app-drive evidence before each commit, no push). See `progress.md` for the per-story record and `context/implementation-plans/milestone-3/` for the plans. Milestone 3 is now Complete.

## Source Documents Read

| Document | Why It Matters |
| --- | --- |
| `context/milestones/milestone-3.md` | Authoritative story list, statuses, acceptance criteria, and Interdependency Order for this run. |
| `context/implementation-plans/GOAL_3_33_implement-cursor-quota-provider/plan.md` | Execution plan for Story 29 — spike-gated Cursor provider; branches B1 (implement on a compliant source) or B2 (remain unsupported). |
| `context/implementation-plans/GOAL_3_31_harden-claude-quota-probe-reliability/plan.md` | Execution plan for Story 30 — harden the Claude ConPTY probe without changing its data source. |
| `context/implementation-plans/GOAL_3_32_harden-or-replace-antigravity-probe/plan.md` | Execution plan for Story 31 — spike-gated Antigravity probe; branches B1 (local Connect-RPC replace) or B2 (harden). |
| `CLAUDE.md` + global/WPF/unit-testing rules | Project law: never estimate quota; keep WPF out of Shared; `in_` params; commit-log format; test-budget discipline. |

## Specialist Persona

`agents/wpf-persona/AGENT.md` (the `wpf-persona` subagent) is used for **all three** workers. Story 29 is a WPF provider feature. Stories 30/31 are PowerShell/C# probe hardening, but every worker in this run must launch and drive the running WPF tray app to validate, which requires WPF platform + UI-automation knowledge.

## Parallelism

Parallelism: 0 (serial, max 1 active subagent).

Forced serial for two independent reasons: (1) the user requires each worker to execute the app and control the PC (mouse/keyboard) to exercise the feature before committing — only one process can drive the desktop at a time; (2) Stories 30 and 31 both edit the shared `scripts/ConPtyCapture.ps1`, so concurrent edits would clobber each other.

## Hard Constraints (from user invocation + project law)

- Implement only the assigned story per worker; follow that story's linked plan.
- Spike-gated stories (29, 31) must run Phase A first and record the go/no-go decision before touching a B1/B2 branch; only one branch is executed.
- **Never estimate, fabricate, infer, or approximate quota.** Low confidence => `ParseResult.Failure` / visible unsupported state.
- No reading of plaintext credential files, no undocumented remote endpoints, no client-identity/User-Agent spoofing (Stories 30, 31, and 29's rejected path).
- Before finishing, each worker that changed files must: build (`dotnet build source/QuotaTank.sln`), run tests (`dotnet test source/QuotaTank.sln`), **and execute the app for >= 30 seconds, controlling the PC to actually use the feature**, then load `skills/commit-log/SKILL.md` and make a real commit.
- The Boss updates `progress.md`, marks the milestone story status/acceptance boxes, and logs blockers — only after accepting a worker result.
- Do not run `git pull` or `git push`.

## Ordered Story Queue

1. Story 30 - Harden Claude Quota Probe Reliability (`GOAL_3_31_harden-claude-quota-probe-reliability`)
2. Story 31 - Replace or Harden Antigravity Quota Probe (`GOAL_3_32_harden-or-replace-antigravity-probe`) — shares `ConPtyCapture.ps1` with Story 30; runs after it.
3. Story 29 - Implement Cursor Quota Provider (`GOAL_3_33_implement-cursor-quota-provider`) — independent; heaviest/riskiest; runs last.
