---
name: commit_log_template
version: 1.1
---

# Commit Log Template

Use this template for commit logs across git, perforce, mercurial, svn, and similar version-control systems.

## Required Structure

Every commit log has:

1. A one-line heading
2. At least one body line

This means commit logs are always at least two lines.

## Heading Formats

### Jira-based work

```text
[XXX-123] - Did the thing with the code for real
```

Rules:

- Keep the Jira ticket key in square brackets.
- Use a concise one-line summary of the change set.
- Base wording on the ticket intent, not a copy of the ticket title.

Optional split-work suffix:

```text
[XXX-123] - Did the thing with the code on backend (1 of 2)
```

### Goal-based work (non-Jira)

```text
[GOAL X.Y] - Implemented the thing with the code for real
```

Rules:

- Use this for projects not using Jira.
- `X.Y` follows the goal hierarchy.
- Keep the summary concise and intent-focused.

### Docs-only, tests-only, or non-feature work

Same heading rules as above; the summary should state the **primary** outcome, not "misc updates".

Examples:

```text
[XXX-123] - Document local build and env setup in README
[GOAL 1.2] - Add regression tests for edge cases in the parser
[XXX-456] - Adjust CI workflow for new test project
```

Rules:

- Prefer `~ Updated:` / `~ Added:` for docs; `~ Added:` / `~ Changed:` for tests or CI as appropriate.
- If production code did not change, say so in the body (first line is enough) so reviewers know scope.

## Body Line Format

Use one major change per line:

```text
~ Problem: Null pointer being dereferenced without check
~ Fixed: A terrible bug in the code
~ Changed: A system to allow for a future dependency more easily
~ Added: A new feature that does a thing
~ Removed: Some big chunk of code that was bad
~ Updated: Some documentation to match the current implementation
~ Resolution: Comparison to null with an early out
```

### Mandatory callouts:
- These callouts MUST be included without exception

#### "Problem" Line
- Single line description of the problem this changeset fixes.
- Convers intent, in engineering actionable language
- Always the first line, underneath the heading

```text
~ Problem: Explicit description of bug, test or new feature
```

#### "Resolution" Line
- Single line description of how this changeset satisfied resolution of the problem

```text
~ Resolution: Explicit description of how the bug, test or new feature resolved the problem.
```

- If it was not satisfactory, that is stated clearly.
- Non-statisfactory resolutions may be incremental changes towards a goal.

```text
~ Resolution: Explicit description of how the attempt was unsuccesful, followed by the value this provides warranting submission.
```

### Optional callouts:
- These callouts MAY be included where appropriate

#### "NOTE" Line:
- Message to developers indicating workflow, strange solution or important notice.

```text
NOTE: An important callout, perhaps that this is changeset 1 of 2
```

## Quality Bar

- Be specific about impacted systems, classes, and intent.
- Keep messages concise and readable.
- Avoid uselessly short messages.
- Avoid long report-style commit logs.
