---
name: commit-log
description: >-
  Use this skill when the user asks for a commit message, commit log, changelog
  entry, version-control summary, or copy-paste check-in wording after work is
  completed. It writes a standardized commit log from a fixed template for git,
  Perforce, Mercurial, SVN, or similar VCS workflows.
disable-model-invocation: false
argument-hint: "[--commit] [scope or ticket hint]"
metadata:
  version: "1.7"
---

# Commit log

Write a commit log that follows the template in [references/commit-log-template.md](references/commit-log-template.md) and output it in the chat so the user can copy it easily.

## When to use

- After completing work and summarizing what changed.
- When the user explicitly wants commit or check-in wording.

## Arguments

The skill was invoked with: $ARGUMENTS

Read that line before doing anything else. It is free text, so parse it leniently:

| Token | Meaning |
| --- | --- |
| `--commit` | Explicit permission to run the commit after writing the log. Absent means write only. |
| anything else | A scope or ticket hint (e.g. `BUG-441`, `only the parser changes`). Use it to pick the heading prefix or narrow which files the log covers. |

If that line is blank, both are simply unset — that is the normal case, not an error. Never ask the user to re-invoke with arguments; the defaults below already cover it.

## Default behavior

Output the commit message in chat and stop. Do not touch git. The user copies and commits themselves.

## Heading prefix selection

Pick the most specific prefix the work warrants. Do **not** fabricate a `[STORY X.Y]` value to make untracked work look tracked.

- `[XXX-123]` — Jira-tracked work.
- `[STORY X.Y]` — work tied to a numbered story in a non-Jira project.
- `[BUG]` — defect fix not tracked against a ticket or story.
- `[FEATURE]` — new behavior not tracked against a ticket or story.
- `[CONTEXT]` — revisions to narrative content under `context/`.
- `[REFACTOR]` — code restructuring with no intended behavior change.
- `[CHORE]` — build, CI, dependency, tooling, or repo housekeeping.

Heading line is capped at 72 characters end-to-end.

## Commit behavior (requires explicit permission)

Committing is opt-in. Treat exactly one of these as permission, and nothing else:

- `--commit` appeared in the invocation line above.
- The user says so in plain language in the conversation (e.g. "commit it", "go ahead and commit", "commit that").

A scope hint, an urgent tone, or work that obviously wants committing are **not** permission. When in doubt, write the log and stop — the user can always say "commit it" afterward, and that costs them one line. Committing unasked costs them a `git reset`.

Once permission is established, do the following:

1. Write the commit log as normal per the instructions below.
2. Stage all changes made during this session: `git add` every file that was created or modified. Do not stage unrelated files.
3. Use the generated commit message as the commit message verbatim.
4. Run the commit.
5. **Do not push.** Stop after the commit.

If the work spans multiple independent change sets (see instructions below), stage and commit each set separately in order.

## Instructions

- Review what was done in the conversation and in the codebase.
- Read [references/commit-log-template.md](references/commit-log-template.md) in full.
- Follow the template for heading, body lines, optional `NOTE:`, scoped commits (docs/tests only), and the quality bar.
- If the work is clearly **several independent change sets** (unrelated fixes, separate features, or commits that should not be squashed), output **multiple** commit logs: each with its own heading and body, separated in chat (for example with a short label like "Commit 1 / Commit 2" or horizontal rules) so the user can paste them as separate check-ins.
- Otherwise output a **single** commit log.
- Output plain text in chat; no need for a code block unless it improves readability for multiple logs.
