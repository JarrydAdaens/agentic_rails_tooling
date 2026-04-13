---
name: commit-log
version: 1.2
description: >-
  Writes a standardized commit log from a fixed template for the user to copy into any VCS (git, Perforce, Mercurial, SVN, etc.). Use when the user asks for a commit message, changelog entry, or summary for version control; after completing a task or feature; when they want copy-paste wording for a check-in; or when they say commit log, commit message, or what to put in the commit.
---

# Commit log

Write a commit log that follows the template in [references/commit_log_template.md](references/commit_log_template.md) and output it in the chat so the user can copy it easily.

## When to use

- After completing work and summarizing what changed.
- When the user explicitly wants commit or check-in wording.

## Default behavior

Output the commit message in chat and stop. Do not touch git. The user copies and commits themselves.

## Commit behavior (only when the user explicitly asks to commit)

If the user explicitly says to commit (e.g. "commit it", "go ahead and commit", "commit that"), do the following:

1. Write the commit log as normal per the instructions below.
2. Stage all changes made during this session: `git add` every file that was created or modified. Do not stage unrelated files.
3. Use the generated commit message as the commit message verbatim.
4. Run the commit.
5. **Do not push.** Stop after the commit.

If the work spans multiple independent change sets (see instructions below), stage and commit each set separately in order.

## Instructions

- Review what was done in the conversation and in the codebase.
- Read [references/commit_log_template.md](references/commit_log_template.md) in full.
- Follow the template for heading, body lines, optional `NOTE:`, scoped commits (docs/tests only), and the quality bar.
- If the work is clearly **several independent change sets** (unrelated fixes, separate features, or commits that should not be squashed), output **multiple** commit logs: each with its own heading and body, separated in chat (for example with a short label like "Commit 1 / Commit 2" or horizontal rules) so the user can paste them as separate check-ins.
- Otherwise output a **single** commit log.
- Output plain text in chat; no need for a code block unless it improves readability for multiple logs.
