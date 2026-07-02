---
name: rails-project-appraisal-report-template
metadata:
  version: "1.0"
---

# Appraisal Dimensions, Grading, and Report Structure

Supporting detail for `rails-project-appraisal`. Load this file when judging evidence and writing the report.

## Appraisal Dimensions

Every report must judge at least these:

### Project Merit

Is the project worth existing? Consider: stated purpose vs. actual user/developer value; commercial value and learning value, where relevant; opportunity cost; strategic clarity; scope realism; and whether the evidence shows execution or fantasy planning — productive work vs. procrastination, vanity, or sunk-cost preservation.

### Technical and Architectural Quality

Is it well built? Consider: architectural coherence and fit to stated purpose; SOLID/DRY alignment where relevant, without forcing harmful abstraction; separation of concerns and encapsulation; testability and maintainability; dependency discipline; build/test/runtime health; and whether implementation quality matches the project's ambition — legacy drag, current best practice, or trend-chasing riff-raff.

### Strategic Feedback and Interventions

Concrete, ordered recommendations: defects and fixes, pivots or scope cuts, hardening steps, architectural simplifications, testing/documentation improvements, milestone or backlog recommendations (described, never made directly), and a kill/archive/abandon call if the evidence justifies it. Order by: positive impact if fixed, negative impact if ignored, urgency, then feasibility.

## Grading Scale

Same scale and meanings as the `grade` skill, applied here at project scope:

| Grade | Meaning |
| --- | --- |
| S | Exceptional. Rare. Strong purpose, strong execution, strong evidence, unusually good leverage. |
| A | Strong. Worth continuing with minor or moderate refinements. |
| B | Good. Fundamentally sound, but with clear issues to address. |
| C | Viable but compromised. Needs deliberate correction before serious expansion. |
| D | Weak. Some value exists, but defects, confusion, or execution risk dominate. |
| E | Severe concern. Likely needs major pivot, freeze, or rebuild before more investment. |
| F | Failed proposition or execution. Not worth continuing in current form — abandonment may be correct. |

Required scorecard rows: Overall, Project merit, Strategic clarity, Commercial or practical value (or `N/A` with reason), Learning value (or `N/A` with reason), Architecture, Maintainability, Code quality, Test health, Build/runtime health, Execution readiness, Risk profile, Evidence quality.

## Confidence Rules

Every major judgement carries a confidence level — never hide uncertainty, but label it:

- `High` — strong direct evidence, validation performed, few unknowns.
- `Medium` — enough evidence for a useful judgement, some gaps remain.
- `Low` — limited evidence, partial validation, missing resources, or uncertain assumptions.
- `Unknown` — cannot responsibly judge from available evidence.

Low-confidence negative findings are allowed; they must be labelled as such, not hidden or upgraded to look more certain.

## Required Report Structure

Use this structure unless the project demands a small adaptation:

```markdown
# Project Appraisal Report: <Project Name>

**Generated:** <D Month YYYY>
**Repository:** <repo name or path>
**Appraiser:** <model / agent if known>
**Report type:** Agentic Rails Project Appraisal

---

## 1. Executive Verdict

### Verdict

<Continue | Refine | Harden | Pivot | Split | Rebuild | Freeze | Archive | Abandon>

### One-paragraph judgement

<Frank summary.>

### Highest-impact finding

<The one thing that matters most.>

### Confidence

<High | Medium | Low | Unknown> — <reason>

---

## 2. Report Card

| Dimension | Grade | Confidence | Rationale |
| --- | --- | --- | --- |
| Overall | <S-F> | <...> | <...> |
| Project merit | <S-F> | <...> | <...> |
| Strategic clarity | <S-F> | <...> | <...> |
| Commercial / practical value | <S-F/N/A> | <...> | <...> |
| Learning value | <S-F/N/A> | <...> | <...> |
| Architecture | <S-F> | <...> | <...> |
| Maintainability | <S-F> | <...> | <...> |
| Code quality | <S-F> | <...> | <...> |
| Test health | <S-F> | <...> | <...> |
| Build / runtime health | <S-F> | <...> | <...> |
| Execution readiness | <S-F> | <...> | <...> |
| Risk profile | <S-F> | <...> | <...> |
| Evidence quality | <S-F> | <...> | <...> |

---

## 3. Project Merit Appraisal

### Purpose and reason to exist

<Assessment.>

### User, commercial, or learning value

<Assessment.>

### Scope realism

<Assessment.>

### Sunk-cost / procrastination risk

<Assessment.>

### Merit conclusion

<Assessment.>

---

## 4. Technical and Architectural Appraisal

### Architectural coherence

<Assessment.>

### SOLID / DRY / separation of concerns

<Assessment.>

### Maintainability

<Assessment.>

### Dependency and trend discipline

<Assessment.>

### Code quality

<Assessment.>

### Testability

<Assessment.>

### Technical conclusion

<Assessment.>

---

## 5. Validation Results

### Build / compile

- Command(s): `<commands>`
- Result: `<pass/fail/not run>`
- Notes: <...>

### Tests

- Command(s): `<commands>`
- Result: `<pass/fail/not run>`
- Notes: <...>

### Lint / type / static checks

- Command(s): `<commands>`
- Result: `<pass/fail/not run>`
- Notes: <...>

### Runtime / launch

- Command(s): `<commands>`
- Result: `<pass/fail/not run>`
- Notes: <...>

### Screenshot / UI evaluation

- Screenshot(s): `<paths or none>`
- Result: `<pass/fail/not run>`
- Notes: <...>

---

## 6. Git and Project-History Findings

### Repository state

<Current branch, dirty state, notable untracked files.>

### Activity pattern

<Recent activity, age, commit shape.>

### Churn and stability

<High-churn areas, rewrite loops, abandoned sections.>

### History conclusion

<Assessment.>

---

## 7. Market / External Grounding

### Research performed

<Searches, sources, accessed dates.>

### Relevant external findings

<Competitors, market signals, framework health, ecosystem facts.>

### External-grounding conclusion

<Assessment.>

---

## 8. Defects, Risks, and Recommended Interventions

| Rank | Defect / opportunity | Evidence | Recommended intervention | Positive impact if fixed | Negative impact if ignored | Difficulty | Urgency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | <...> | <...> | <...> | <...> | <...> | <Low/Med/High> | <Low/Med/High> |

---

## 9. Authority-Level Recommendation

If given full authority, I would:

1. <Action>
2. <Action>
3. <Action>

### Recommended decision

<Continue / Refine / Harden / Pivot / Split / Rebuild / Freeze / Archive / Abandon>

### Rationale

<Why this decision is justified.>

---

## 10. Confidence and Uncertainty

### High-confidence findings

- <Finding>

### Medium-confidence findings

- <Finding>

### Low-confidence findings

- <Finding>

### Unknowns and missing evidence

- <Missing evidence>

### What would improve confidence

- <Additional resource, repo, test, stakeholder answer, market data, etc.>

---

## 11. Evidence and Provenance

### Context files read

- `<path>` — <why it mattered>

### Source areas inspected

- `<path>` — <why it mattered>

### Commands run

| Command | Purpose | Result |
| --- | --- | --- |
| `<command>` | <...> | <...> |

### Git commands run

| Command | Purpose | Result |
| --- | --- | --- |
| `<command>` | <...> | <...> |

### Screenshots captured

- `<path>` — <what it shows>

### Web searches and external sources

| Query / source | Purpose | Date accessed | Finding |
| --- | --- | --- | --- |
| <...> | <...> | <...> | <...> |

### Files deliberately not inspected

- `<path or pattern>` — <reason>

### Unverified claims

- <Claim> — <why unverified>
```

## Report Quality Bar

A good report is frank, useful, evidence-led, specific, actionable, properly uncertain where evidence is weak, clear about what was and wasn't inspected, brave enough to recommend abandonment when justified, and disciplined enough not to perform fixes while appraising.

A bad report is generic, motivational, vibes-based, overconfident, too polite to be useful, full of unsupported market claims, silent about validation gaps, a disguised implementation plan, or a dump of codebase facts without judgement.

## Failure Modes to Avoid

- Calling the project valuable merely because work has already been spent on it.
- Treating complexity as merit, or fashionable-but-unnecessary architecture as quality.
- Punishing boring architecture that genuinely fits the job.
- Mistaking learning value for commercial value, or commercial ambition for commercial viability.
- Inferring build/runtime health without running build or test commands, unless validation is genuinely impossible.
- Hiding missing evidence instead of labelling it.
- Making source, design, milestone, backlog, or plan changes while producing the appraisal.
- Letting raw Tier-0 dictation override maintained context without saying so.
