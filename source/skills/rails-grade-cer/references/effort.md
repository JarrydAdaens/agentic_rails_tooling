---
name: rails-grade-cer-effort
description: Effort and Dependencies.
metadata:
  version: "2.0"
---

# Effort and Dependencies

Assess the amount of implementation, discovery, verification, and delivery work. Keep it separate from elapsed waiting and reasoning difficulty.

| Band | Evidence pattern |
| --- | --- |
| Low | One bounded change using known tools and a narrow verification surface. |
| Moderate | Several implementation/check steps, integration, or a bounded investigation. |
| High | Multiple delivery increments, large migration volume, extensive verification, or substantial unknown discovery. |
| Unknown | Scope or prerequisites are insufficiently defined. |

If the user needs a forecast, give a range only when comparable work or an explicit estimator basis supports it. State operator/model assumptions, actual dependencies, critical path, external waits, and confidence. Concurrent steps must be truly independent and respect shared-file ownership. Do not add ordinal bands or infer calendar time from model branding.

Preserve historical estimates as historical; record observed effort separately after execution. Missing telemetry stays unknown.
