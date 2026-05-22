# Report And Failures

Use this reference when updating provenance, handling blockers, and producing the final user-facing report.

## Implementation Log

Update `implementation-log.md` with:

- what was inspected in the source and destination
- what was copied directly
- what was rewritten or split
- what was deliberately not copied
- decisions made during extraction
- deviations from the plan
- failed attempts
- validation performed
- remaining uncertainty

If the evidence skill is active, update `evidence.md` with changed files, commits, tests, build results, source files used, and known unverified claims.

If the complaining skill is active, append only genuine actionable friction to `complaining.md`.

If the thinking-out-loud skill is active, append useful sanitised investigation notes to `thinking.md`.

## Shallow Handover

For small upstreaming tasks, the final report can serve as a shallow handover. Include:

- feature upstreamed
- source repository used
- destination repository changed
- scope covered
- how the feature was neutralized
- where it landed
- what was deliberately excluded
- validation run and result
- risks or gaps
- implementation plan/log location

For large or production-grade upstreaming, use the handover skill when requested.

## Completion Criteria

Treat the task as complete only when:

- the requested feature exists in WPF-Starter
- source project baggage was excluded or rewritten
- starter conventions were followed
- equivalent starter functionality was reconciled instead of duplicated
- required dependencies, project references, and bootstrap paths were updated
- relevant docs or context files were updated
- `implementation-log.md` records what happened
- validation ran successfully, or the validation gap is explicit

## Failure Modes

### Feature Boundary Unclear

Stop and ask the user to identify the intended scope. Do not guess by copying broad folders.

### Source Repository Missing Or Inaccessible

Stop. The task cannot proceed without source inspection unless the user provides the relevant files directly.

### Source Depends On Project-Specific Architecture

Extract the reusable core if it is clear. Ask before recreating large supporting architecture.

### Destination Already Has A Competing System

Compare and reconcile. Do not install a duplicate system silently.

### Validation Fails

Record:

- command run
- failure output summary
- likely cause, if known
- files affected
- safest next step

Do not claim success unless the user explicitly accepts the remaining validation gap.
