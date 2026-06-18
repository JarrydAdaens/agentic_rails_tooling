# Certainty Labels

## Purpose

Certainty labels keep review findings honest about what is actually known.

## Labels

`verified` means a tool run, compile, test, repro, or direct inspection confirms the finding.

Examples:

- A build command failed on the changed project.
- A test failure directly exercises changed behavior.
- A linter or analyzer flagged the specific line.
- The diff clearly removes required behavior named in the plan.

`inferred` means the finding comes from reasoning about code, architecture, rules, or the plan without tooling directly confirming it.

Examples:

- A new dependency appears to violate module layering.
- A missing null check looks reachable from the surrounding flow.
- A UI state update is not wired to the view model notification path.

`unverified` means the reviewer suspects a risk but could not confirm it with tooling or confident reasoning.

Examples:

- A platform-specific behavior may break but cannot be tested locally.
- A performance concern needs profiling.
- A migration appears risky but the target dataset is unavailable.

Never promote a finding to a stronger label to sound more confident. A false `verified` finding erodes trust in the whole quality gate.
