---
name: rails-spike-spike-record
description: The two halves of a spike record - the contract written before the experiment and the completion report written after it - with guidance on what makes each field usable.
metadata:
  version: "1.0"
---

# The Spike Record

One file, two halves. The contract is written first and never rewritten to match the result; the report is appended when the experiment finishes. Reading them together shows what was expected and what actually happened, which is most of the value a spike leaves behind.

## The contract

```markdown
# Spike: <the question, as a question>

## Question

<the specific uncertainty, in one sentence>

## Why This Matters

<the decision that is waiting on this answer>

## Candidate Hypotheses

1. <a path that might work, and why it might>
2. ...

## Smallest Useful Experiment

<the minimum work that produces evidence>

## Success Criteria

<the observation that would support each hypothesis, and the one that would kill it>

## Boundaries

<what this spike will not do>
```

Field notes:

- **Question** — answerable this-or-that, or yes/no. "Does SDK 9 resolve the missing call without a shim?" is a spike. "Investigate the rendering layer" is a project.
- **Candidate hypotheses** — two or three. One hypothesis means the answer is already assumed; six means the question has not been narrowed yet.
- **Success criteria** — written before the experiment, because criteria invented afterward describe whatever happened to occur.
- **Boundaries** — the field that keeps a spike from becoming the implementation. Name the tempting adjacent work explicitly.

## The completion report

```markdown
## Result

<what happened when the experiment ran>

## Evidence

- <command, output, version, error, measurement>

## Conclusion

<what is now known that was not known before>

## Recommended Path

<what the caller should do next, specifically enough to start>

## Confidence

High / Medium / Low - <what would raise it>

## Remaining Unknowns

- <what this spike did not settle>

## Production Work Created

- <the real work the answer implies, for the plan to absorb>
```

Field notes:

- **Evidence** — observations, not conclusions. "The build failed with CS0246 on line 12 of Scratch.cs against SDK 9.0.4" is evidence; "SDK 9 is incompatible" is a conclusion drawn from it.
- **Recommended path** — allowed to be "none of these"; that is a real answer when the hypotheses are all dead, and it should carry the next question to ask.
- **Confidence** — Low is a legitimate answer and more useful than an inflated High. Say what evidence would raise it.
- **Production work created** — the bridge back to the plan. A spike whose answer implies real work and lists none has left that work invisible.
