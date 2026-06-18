---
name: optimizing-descriptions
description: How to craft skill descriptions that trigger reliably without becoming too broad.
metadata:
  version: "1.1"
---

# Optimizing Skill Descriptions

The `description` field is the main trigger signal for a skill. At startup, compatible clients usually load only `name` and `description`; the full `SKILL.md` is read only after the agent decides the task matches.

## Description Principles

- Use action-oriented wording such as "Use this skill when..."
- Describe user intent, not internal implementation.
- Be explicit about near-miss phrasing and situations where the user may not name the domain directly.
- Stay concise and under the 1024-character limit.

## Trigger Evaluation Queries

Create realistic prompts labeled with whether the skill should trigger:

```json
[
  {
    "query": "Can you clean up this sales CSV and chart the top months?",
    "should_trigger": true
  },
  {
    "query": "Can you write a loader that imports CSV rows into Postgres?",
    "should_trigger": false
  }
]
```

Use a mix of:

- Casual and formal phrasing.
- Explicit and implicit domain mentions.
- Short and context-heavy prompts.
- Near-miss negative examples that share keywords but need a different skill.

## Optimization Loop

1. Run trigger evals several times per query.
2. Identify false negatives and false positives.
3. Revise the description for the general category of failure, not a single phrase.
4. Keep a validation set separate from the train set.
5. Select the description with the best validation pass rate.

Source: [AgentSkills.io Optimizing Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
