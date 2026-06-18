---
description: Unit testing limits — keep tests scoped to the task, proportionate to risk, and avoid test-chasing.
globs: []
alwaysApply: true
metadata:
  version: "1.0"
  owner: Jarryd Adaens
---

# Unit Testing Limits Rule

## Scope

Applies to every agentic IDE or coding agent working in this workspace, across all languages and frameworks.

Intent: keep unit tests in service of the assigned task. Tests are an engineering tool for confidence, not the objective. This rule exists to stop agents from disappearing into test repair, test expansion, mock construction, and coverage polishing instead of delivering the requested change.

This is a portable rule. It must not depend on any specific IDE, test runner, or language. Copy it into any agentic environment unchanged.

---

## Core Principle

Prioritize the requested behaviour first. Use tests to prove that behaviour, protect an important invariant, reproduce a bug, or make isolated development possible.

Prefer **useful confidence** over **maximum coverage**. Tests should accelerate delivery, not consume it. When tests help the agent move faster and safer, use them. When they become a token sink, stop.

---

## What Makes a Test Worth Writing

A good test does at least one of these:

- proves the requested behaviour works
- protects against a realistic regression
- isolates stable logic from unstable environments (hardware, services, runtime state)
- documents a critical rule in executable form
- gives fast feedback without excessive setup

A bad test does mainly these:

- exists only to raise a coverage number
- locks down incidental implementation details and makes refactoring harder
- requires heavy mocks for trivial glue code
- tests framework behaviour instead of project behaviour
- costs more effort than the risk justifies

---

## When Tests Are Required

Create or update tests when the change involves any of the following:

1. **Bug fixes** — reproduce the bug with a failing test when practical, then make it pass with the smallest correct fix.
2. **Stable business logic** — rules, calculations, validation, mapping, parsing, permissions, state transitions, or deterministic algorithms.
3. **Critical behaviour** — code where failure is expensive, dangerous, data-corrupting, security-sensitive, or likely to break production workflows.
4. **Regression-prone logic** — areas with prior bugs, tricky edge cases, or behaviour future agents are likely to damage by accident.
5. **Environment isolation** — when a test lets development continue without physical hardware, live services, cloud dependencies, game runtime state, or slow manual setup.

---

## When Tests Are Optional or Discouraged

**Optional** (allowed, but justify the value before spending time): simple UI glue, layout/styling/markup-only work, trivial wiring between already-tested systems, generated boilerplate, configuration-only work, and logging/comments/naming/documentation. Optional does not mean forbidden; it means manual, integration, smoke, or runtime validation is often the better tool.

**Discouraged** (do not add a test whose main subject is): private implementation details, framework behaviour, obvious property assignment, shallow getters/setters, dependency-injection registration without real logic, visual layout better checked by eye, volatile prototype code expected to change immediately, or emergent gameplay/UX behaviour that depends on real interaction.

Never build an elaborate mock system to unit test code that should be validated at a higher level.

---

## Scope Limits

Keep test work inside the scope of the assigned change.

**Allowed:**

- add focused tests for the changed behaviour
- update tests directly broken by the change
- add a regression test for a fixed bug
- run targeted tests related to the changed files or feature

**Not allowed without explicit instruction:**

- broad test-suite refactors or mass snapshot updates
- large mock-framework rewrites
- converting unrelated code to be more testable
- adding coverage for nearby untouched systems
- fixing unrelated failing tests
- chasing full-suite cleanliness when the task only needs targeted validation

---

## Effort Budget

Before writing tests, estimate whether the effort is proportionate to the risk. Use this default unless the user or project says otherwise:

| Situation | Default Limit |
| --- | --- |
| Small change | 1 to 3 focused tests |
| Bug fix | 1 regression test plus nearby affected cases |
| Medium feature | Core happy path plus important edge cases |
| Critical logic | Enough to protect the invariant, but no speculative coverage |
| UI / layout / glue | Prefer manual or smoke validation unless there is meaningful logic |

If test setup becomes larger than the implementation, stop and reassess. Do not spend more effort building the test harness than solving the actual task, unless the task is explicitly about test infrastructure.

---

## Test Selection Order

Run the cheapest useful checks first:

1. Targeted unit tests for the changed files or feature
2. Focused integration or smoke tests, when unit tests are not the right level
3. Build or compile checks
4. The relevant package or module test group
5. The full test suite only when the change is broad, risky, release-bound, or explicitly requested

Do not start with the full suite by default if a smaller surface gives useful signal.

---

## Failure, Retry, and Stop Conditions

Agents must not loop indefinitely on tests.

1. **First failure** — inspect it. Decide whether it is caused by the current change, stale tests, the environment, or unrelated existing breakage.
2. **Second failure** — try one focused correction if the cause is clear, kept inside the assigned scope.
3. **Third failure** — stop broad repair. Report clearly. Do not keep burning tokens unless the user explicitly asks for deeper test repair.

Also stop and report immediately when any of these occur, regardless of attempt count:

- the failure appears unrelated to the assigned change
- test setup would require broad architecture changes
- mocks are growing larger than the production change
- you are updating snapshots or expected values without understanding why
- the only remaining goal is better coverage rather than better confidence
- the suite depends on unavailable services, hardware, credentials, or environment state

---

## Existing and Unrelated Failures

If unrelated tests are already failing, that is not permission to repair the world. The agent must:

1. Identify whether the failure relates to the current change.
2. Fix it only if the current change caused it.
3. Otherwise report it as pre-existing or unrelated, when the evidence supports that.
4. Continue with targeted validation where possible.

Never hide unrelated failures. Never claim full validation passed when only targeted validation passed.

---

## Manual Validation Is Allowed

Manual validation is acceptable when it is the right tool: visual UI behaviour, animation/layout/interaction feel, gameplay feel or emergent behaviour, editor workflows, hardware-dependent behaviour, and flows where automated tests would be brittle or fake.

When using manual validation, state exactly what was checked and what remains unverified.

---

## Coverage

Coverage is a signal, not a target. Do not add tests just to satisfy a percentage unless the project explicitly requires that threshold.

Optimize for meaningful behavioural coverage, regression protection, fast feedback, maintainability, and low brittleness — not for maximum line coverage, exhaustive branch testing, snapshot churn, mocking everything, or proving trivial code is trivial.

---

## Refactoring for Testability

Refactor for testability only when it directly improves the assigned change.

**Good reasons:** extracting deterministic logic from IO/UI/hardware/framework boundaries; making a bug fix safely testable; reducing coupling in a touched area; isolating a critical rule behind a stable seam.

**Bad reasons:** restructuring unrelated code to ease tests; introducing abstractions only for mocks; changing architecture to satisfy a test-style preference; making broad codebase changes without approval.

If testability requires architectural change, stop and report the trade-off before proceeding.

---

## Decision Checklist

Before adding or expanding tests, answer:

- Does this test protect behaviour the user actually asked for?
- Would it catch a realistic future regression?
- Is this behaviour stable enough to lock down?
- Is unit testing the right level, or would manual / integration / smoke validation be better?
- Is the setup cost proportionate to the risk?
- Am I testing project behaviour rather than implementation detail?

If the answer is mostly no, do not add the test.

---

## Required Reporting Format

At the end of a task, report validation in this form. Never write vague claims like "all good" or "tests passed" without saying which tests, and always include what was tried and what remains unverified.

```markdown
## Validation

- Targeted tests: `<command or description>` — `<passed / failed / not run>`
- Build/compile: `<command or description>` — `<passed / failed / not run>`
- Manual checks: `<what was checked>` — `<result>`
- Full suite: `<run / not run>` — `<reason>`
- Remaining uncertainty: `<anything not proven>`
```
