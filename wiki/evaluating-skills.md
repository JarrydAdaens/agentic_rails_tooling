# Evaluating Skill Output Quality

Structured evals test whether a skill reliably improves outputs across realistic prompts and edge cases.

## Test Case Shape

Store test cases under `evals/evals.json` when a skill needs formal evaluation:

```json
{
  "skill_name": "csv-analyzer",
  "evals": [
    {
      "id": 1,
      "prompt": "Find the top 3 months by revenue and make a bar chart.",
      "expected_output": "A chart showing the top 3 revenue months with labels.",
      "files": ["evals/files/sales.csv"],
      "assertions": [
        "The output includes a chart image file",
        "The chart shows exactly 3 months",
        "Both axes are labeled"
      ]
    }
  ]
}
```

## Evaluation Pattern

Run each test case with the skill and against a baseline, then compare:

- Assertion pass rate.
- Human review feedback.
- Execution transcript quality.
- Duration and token cost.

Use a clean context for each run so the result reflects the skill, not earlier conversation state.

## Good Assertions

Good assertions are observable and specific:

- The output file is valid JSON.
- The chart has labeled axes.
- The report includes at least three recommendations.

Weak assertions are vague, brittle, or unverifiable:

- The output is good.
- The exact phrase appears even though equivalent wording would be acceptable.

## Iteration Loop

1. Run evals and grade outputs.
2. Aggregate results.
3. Review outputs with a human.
4. Read execution traces for wasted steps or ignored instructions.
5. Improve the skill by generalizing from failures.
6. Repeat until the skill adds enough value for its cost.

Source: [AgentSkills.io Evaluating Skills](https://agentskills.io/skill-creation/evaluating-skills)
