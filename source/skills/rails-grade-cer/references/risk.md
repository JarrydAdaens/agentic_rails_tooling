---
name: rails-grade-cer-risk
description: Consequence, Hazards, and Residual Risk.
metadata:
  version: "2.0"
---

# Consequence, Hazards, and Residual Risk

A Risk assessment reads the whole plan. Separate four components:

| Component | Question |
| --- | --- |
| Inherent consequence | What harm could failure cause before safeguards: data loss, privacy exposure, availability, physical or financial harm, recovery cost? |
| Implementation hazards | How does this particular approach create failure modes: destructive operations, unsafe ordering, concurrent writes, untested rollback, partial state? |
| Safeguards and evidence | Which controls exist, which were tested, and which are proposed or unknown? |
| Residual risk | What risk remains given the implemented and evidenced controls, including irreducible consequence? |

Use `low`, `moderate`, `high`, `critical`, or `unknown` for consequence and residual magnitude, with confidence and rationale. Describe hazards concretely instead of pretending their count is a score. Safeguards are `verified`, `proposed`, `partial`, or `unknown`, supported by evidence.

## Same objective, different approach

Objective: migrate customer records to a new schema. Both approaches carry high inherent consequence if records are lost.

- Approach A drops the old table first, transforms in place, and has an untested backup. Hazards include irreversible loss and partial migration. Backup effectiveness is unknown; residual risk remains high with limited confidence.
- Approach B copies into a new table, checks record counts and invariants, performs a rehearsed rollback, and switches readers after validation. It has fewer destructive hazards and verified controls. Residual risk can be lower, with remaining cutover/concurrency hazards stated explicitly.

A smaller phase or stronger model does not change the consequence of losing those records. Assessment cannot claim controls were tested merely because the plan describes them.
