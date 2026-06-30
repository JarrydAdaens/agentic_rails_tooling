---
name: complaining-entry-format
metadata:
  version: "1.0"
---

# Complaint Entry Format

Use this format when appending a complaint. Include a timestamp only when the environment provides a reliable current date and time.

```markdown
## YYYY-MM-DD HH:mm - Short complaint title

### What happened
A direct description of the problem.

### Why this made the task harder
Explain the friction, uncertainty, wasted time, or risk introduced.

### What I tried
List relevant attempts, commands, edits, or reasoning paths.

### What would improve this
Suggest practical fixes, clearer instructions, better tooling, different architecture, or changed workflow.
```

If reliable time is unavailable, omit the timestamp instead of pretending.

```markdown
## Short complaint title
```

## Optional Interpretation Section

When the entry includes judgment or strategic criticism, separate it from observed facts:

```markdown
### What I think
This is the agent's interpretation, risk assessment, or recommendation.
```

## Empty State

If there are no real complaints, acceptable content is:

```markdown
# Complaining Log

No complaints recorded.
```

Or:

```markdown
# Complaining Log

This file records blockers, friction, ambiguity, tool failures, bad assumptions, and other task stressors encountered by the agent while working.

If this file is empty, there were no meaningful complaints to record.
```

## Append-Only Default

Append new entries below existing content.

Edit existing entries only when:

- the user explicitly asks for cleanup
- the agent is correcting a factual mistake in its own complaint
- the file is malformed
- duplicate entries were accidentally created
