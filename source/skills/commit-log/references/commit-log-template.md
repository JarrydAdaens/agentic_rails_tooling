---
name: commit-log-template
metadata:
  version: "1.4"
---

# Commit Log Template

Use this template for commit logs across git, perforce, mercurial, svn, and similar version-control systems.

## Required Structure

Every commit log has:

1. A one-line heading (≤72 characters, including the prefix and the `- ` separator)
2. At least one body line

This means commit logs are always at least two lines.

## Heading Formats

The heading is always a bracketed prefix, a space-dash-space separator, and a concise summary:

```text
[PREFIX] - Concise summary of the change
```

Pick the **most specific prefix that fits**. If the work maps to a tracked Jira ticket or numbered story, use that. Otherwise use one of the lightweight prefixes below.

### Tracked work

#### Jira-based work

```text
[XXX-123] - Did the thing with the code for real
```

Rules:

- Keep the Jira ticket key in square brackets.
- Base wording on the ticket intent, not a copy of the ticket title.

Optional split-work suffix:

```text
[XXX-123] - Did the thing with the code on backend (1 of 2)
```

#### Story-based work (non-Jira)

```text
[STORY X.Y] - Implemented the thing with the code for real
```

Rules:

- Use this for projects not using Jira but tracking against a numbered story hierarchy.
- `X.Y` follows the story hierarchy.

### Lightweight prefixes (no ticket, no story)

Use these for small, self-contained work that doesn't correspond to a tracked ticket or numbered story. Do **not** invent a `[STORY X.Y]` value to make untracked work look tracked.

| Prefix | When to use |
|--------|-------------|
| `[BUG]` | Fixing a defect that is not tracked against a ticket or story. |
| `[FEATURE]` | Adding new behavior that is not tracked against a ticket or story. |
| `[CONTEXT]` | Revising narrative content under the `context/` folder (plans, retrospectives, handovers, project context). |
| `[REFACTOR]` | Restructuring code with no intended behavior change. |
| `[CHORE]` | Build, CI, dependency, tooling, or repo housekeeping. |

Examples:

```text
[BUG] - Fix null deref in UserService when session is anonymous
[FEATURE] - Add JWT-based login endpoint with refresh token
[CONTEXT] - Update context/handovers/2026-05-07.md with current story state
[REFACTOR] - Extract DataService dependencies behind an interface
[CHORE] - Bump xunit to 2.7 and update test runner config
```

### Docs-only, tests-only, or non-feature work

Same heading rules as above; the summary should state the **primary** outcome, not "misc updates".

Examples:

```text
[XXX-123] - Document local build and env setup in README
[STORY 1.2] - Add regression tests for edge cases in the parser
[CHORE] - Adjust CI workflow for new test project
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
- Conveys intent, in engineering-actionable language.
- Always the first line, underneath the heading.

```text
~ Problem: Explicit description of bug, test or new feature
```

#### "Resolution" Line
- Single line description of how this changeset satisfied resolution of the problem

```text
~ Resolution: Explicit description of how the bug, test or new feature resolved the problem.
```

- If it was not satisfactory, that is stated clearly.
- Non-satisfactory resolutions may be incremental changes towards a goal.

```text
~ Resolution: Explicit description of how the attempt was unsuccessful, followed by the value this provides warranting submission.
```

### Optional callouts:
- These callouts MAY be included where appropriate

#### "NOTE" Line:
- Message to developers indicating workflow, strange solution or important notice.

```text
NOTE: An important callout, perhaps that this is changeset 1 of 2
```

## Quality Bar

- Heading: ≤72 characters end-to-end (prefix, separator, summary). State intent, not the ticket title.
- Body: one major change per line. Aim for 3–7 body lines including `~ Problem:` and `~ Resolution:`. If you need more than ~10, the change set should probably be split.
- Each `~` callout fits on a single line. No wrapped paragraphs.
- Name impacted systems, classes, files, or modules where it adds clarity. Avoid vague phrases like "misc cleanup" or "various fixes".
- Pick the most specific heading prefix that fits. Do not invent a `[STORY X.Y]` for untracked work — use a lightweight prefix instead.
