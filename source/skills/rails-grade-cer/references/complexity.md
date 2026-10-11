---
name: rails-grade-cer-complexity
description: Complexity Assessment.
metadata:
  version: "2.0"
---

# Complexity Assessment

Assess reasoning difficulty from the approach, interactions, ambiguity, and decision burden. File count and task volume alone are not complexity.

| Band | Evidence pattern |
| --- | --- |
| Low | Familiar local change with a clear contract and few interactions. |
| Moderate | Several connected components or meaningful design choices within known boundaries. |
| High | Uncertain contracts, concurrency/distribution, cross-system invariants, or consequential architecture choices. |
| Unknown | The approach or important dependencies are too vague to assess. |

Name the specific drivers and confidence. A mechanical change across many files can be low complexity with high effort. A one-line concurrency change can be high complexity. These are descriptive bands, not calibrated scales or model ceilings.
