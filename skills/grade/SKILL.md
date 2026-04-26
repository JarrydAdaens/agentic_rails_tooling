---
name: grade
description: >-
  Use this skill when the user asks to grade, rate, assess, or compare the
  quality of an artifact such as code, design, persona, workflow, document, or
  plan. It returns a decisive letter grade (S, A-F) with concise evidence.
metadata:
  version: "1.0"
---

# Grade

Evaluate the provided artifact and return a decisive letter grade with a short justification. Optimized for rapid iteration and engineering workflows.

## When to use

- The user asks to grade, rate, or assess an artifact.
- Quick quality check before committing, merging, or shipping.
- Comparing alternatives or deciding whether to iterate further.

## Do not use

- Do not use for a full code review unless the user asks for a grade.
- Do not provide implementation steps or fixes unless the user explicitly asks.

## Grading scale

| Grade | Meaning | Threshold |
|-------|---------|-----------|
| **S** | Exceptional | Industry-leading; innovative; sets a benchmark. |
| **A** | Excellent | Production-ready; no improvements needed. |
| **B** | Good | Solid and usable; minor issues; improvements recommended but non-blocking. |
| **C** | Functional but flawed | Works, but with clear issues or compromises; acceptable only under pressure. |
| **D** | Poor | Barely acceptable; buggy, clunky, or unstable; requires rework. |
| **E** | Near failure | Severe issues; not worth keeping in current form. |
| **F** | Failure | Negative value; causes damage or regression; must be removed. |

## Evaluation criteria

Weight each criterion by relevance to the context provided:

- **Correctness** - does it do what it claims?
- **Clarity** - readable and understandable at a glance?
- **Maintainability** - easy to change and extend?
- **Architecture** - sound structure and separation of concerns?
- **Fitness for purpose** - right tool/approach for the job?
- **User experience** - ergonomic for its audience?
- **Risk / fragility** - how likely is it to break?
- **Engineering balance** - neither over- nor under-engineered?

## Instructions

1. Read and understand the artifact and any context the user provides about what success looks like.
2. Determine whether the artifact is a **single concern** or **multiple components/domains**.
3. **Single concern -> Standard mode**: return one letter grade followed by one paragraph of reasoning.
4. **Multiple components -> Expanded mode**: return a Markdown table (`Grade | Component`) followed by a short summary paragraph.
5. Be **decisive** - no hedging, no vague averages.
6. **Justify the grade** by referencing specific strengths or weaknesses in the artifact.
7. Align reasoning to the user's stated context and concerns; avoid generic feedback.
8. Do **not** provide implementation steps or fixes unless the user explicitly asks.

## Output contract

- Lead with the grade.
- Keep the written report concise.
- Include concrete evidence for the grade.
- Use expanded table mode only when separate components deserve separate grades.

## Examples

### Standard mode

**User:** `grade this agent persona. I want to know if it's useful or if I've conflated it with what a skill or rule should be.`

**Response:**

> **B**
>
> The persona is directionally correct and provides useful structure, but it overlaps significantly with what would be better expressed as rules or constraints. The abstraction boundary is unclear, which will cause confusion in reuse and agent behavior. Usable as-is, but needs a cleaner separation of concerns.

### Expanded mode

**User:** `grade this feature end to end - API, UI, and test coverage.`

**Response:**

> | Grade | Component |
> |-------|-----------|
> | A | API design |
> | C | UI polish |
> | B | Test coverage |
>
> The API is clean and well-structured. Test coverage is solid for the happy path but thin on edge cases. The UI works but feels unfinished - inconsistent spacing and missing loading states hurt perceived quality.
