---
name: commit-log
version: 1.1
description: >-
  Writes a standardized commit log from a fixed template for the user to copy into any VCS (git, Perforce, Mercurial, SVN, etc.). Use when the user asks for a commit message, changelog entry, or summary for version control; after completing a task or feature; when they want copy-paste wording for a check-in; or when they say commit log, commit message, or what to put in the commit.
---

# Commit log

Write a commit log that follows the template in [references/commit_log_template.md](references/commit_log_template.md) and output it in the chat so the user can copy it easily.

## When to use

- After completing work and summarizing what changed.
- When the user explicitly wants commit or check-in wording.
- Keeps the final commit step with the human (agentic safety).

## Instructions

- Review what was done in the conversation and in the codebase.
- Read [references/commit_log_template.md](references/commit_log_template.md) in full.
- Follow the template for heading, body lines, optional `NOTE:`, scoped commits (docs/tests only), and the quality bar.
- If the work is clearly **several independent change sets** (unrelated fixes, separate features, or commits that should not be squashed), output **multiple** commit logs: each with its own heading and body, separated in chat (for example with a short label like "Commit 1 / Commit 2" or horizontal rules) so the user can paste them as separate check-ins.
- Otherwise output a **single** commit log.
- Output plain text in chat; no need for a code block unless it improves readability for multiple logs.
