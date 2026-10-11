---
name: rails-grade-cer
description: Use this skill to assess a plan's complexity, effort, and risk qualitatively, with explicit evidence and uncertainty; use it when sizing or comparing substantial work.
disable-model-invocation: true
argument-hint: "<plan path or work description> [complexity|effort|risk] [--concise|--verbose] [--file]"
metadata:
  version: "2.0"
---

# Rails Grade CER

## Arguments

The skill was invoked with: $ARGUMENTS

Parse leniently and accept plain-language equivalents such as "just risk".

| Token | Meaning |
| --- | --- |
| `complexity`, `effort`, `risk` | Assess named axes only. Absent means all three. |
| `--concise` | One evidence table. Absent means table plus brief explanation. |
| `--verbose` | Expand the requested assessment. Absent means concise supporting prose. |
| `--file` | Also save `cer-score-card.md` beside the resolved plan, or at an explicitly named destination. Absent means inline output only. |
| anything else | Plan path or work description. Empty arguments resolve the current named work from session context and known project paths. |

## References

- [Complexity](references/complexity.md)
- [Effort and dependencies](references/effort.md)
- [Consequence, hazards, and residual risk](references/risk.md)

## Non-negotiable rules

This is the canonical rule list. Nothing else in this document restates it.

- Use qualitative bands and explicit uncertainty. Historical numerical scores may remain historical evidence; they are not calibrated capability thresholds, arithmetic workload totals, or routing authority.
- Read objective and implementation for risk. Report inherent consequence, implementation hazards, safeguards with evidence, and residual risk separately. Unknown safeguards do not count as effective controls.
- Assess only requested axes. Separate confidence from magnitude; missing evidence lowers confidence rather than silently lowering consequence.
- Do not select a model, prescribe mandatory phases, or equate stronger reasoning with safe execution. Runtime inheritance and available user-authorized overrides are a caller's responsibility.
- Report the visible scope and assumptions. Duration ranges need an evidenced basis and a dependency path; do not convert an ordinal band into a promised elapsed time or sum bands.
- Save a scorecard only when requested. Preserve requested existing artifacts and history; revise an existing current scorecard with an attributable revision note rather than deleting it.

## Workflow

1. Resolve the named plan or current work. Read it once, including outcome, approach, dependencies, and recovery evidence.
2. Load only references for requested axes and produce assessments grounded in concrete drivers.
3. Return a table with columns `Axis / component`, `Assessment`, `Evidence / assumptions`, and `Confidence`. Complexity and effort use `low`, `moderate`, `high`, or `unknown`; risk uses the component bands in its reference. The Risk request produces distinct consequence, hazard, safeguard, and residual rows.
4. At normal detail, add brief explanations where the table alone would conceal an important distinction. At concise detail use the table alone. Mention unknown evidence directly.
5. When requested, write the current scorecard next to the plan and report that exact path. A caller consumes the inline result without assuming any file exists.

## Observable output

The result contains the requested axes and their evidence. Two approaches to one objective can show the same inherent consequence with different hazards and residual risk. No numerical routing or compulsory scorecard is produced.
