---
name: wpf-visual-quality-gate
description: Independent sub-agent evaluation for WPF UI changes using build, tests, screenshots, and real UI interaction.
metadata:
  version: "0.1"
  agentic_rails_source_version: "0.1"
  owner: "Jarryd Adaens"
  repo: "quota_tank"
---
# WPF Visual Quality Gate

Use this evaluation for any WPF change that affects visible UI, navigation, state presentation, layout, or user interaction.

## Runner

Use an independent evaluator sub-agent when available.

Preferred runner order:

1. `quality-gate-persona`
2. `wpf-persona` when the evaluation needs deeper WPF or XAML judgement
3. Human evaluator when sub-agents or desktop screenshots are unavailable

The evaluator must not edit files. It validates only the packet criteria and reports failures.

## Evaluator Packet

The main agent must provide:

- Task goal
- Expected visible behavior
- Visual launch command
- Window title
- Interaction path
- Pass criteria
- Cleanup command
- Commands already run
- Files changed

Quota-Tank default visual launch:

```text
source\QuotaTank.WPF\bin\Debug\net8.0-windows\QuotaTank.WPF.exe --show-popup
```

Quota-Tank default window title:

```text
Quota-Tank
```

Quota-Tank default cleanup:

```text
Stop-Process -Id (Get-Process | Where-Object { $_.ProcessName -eq 'QuotaTank.WPF' }).Id
```

## Gate Steps

1. Confirm the relevant WPF build passed.
2. Confirm relevant tests passed.
3. Launch the app through the visible evaluation path.
4. Capture a screenshot of the initial state.
5. Perform the required interaction through real UI input.
6. Capture a screenshot of the target state.
7. Compare screenshots against the packet pass criteria.
8. Clean up the running WPF process.

## Pass Criteria

- App launches into the expected visible screen.
- Changed controls are visible and discoverable.
- Required interaction works through real UI input.
- Target state is visible after interaction.
- No obvious clipping, overlap, invisible controls, or misleading status is present.
- Cleanup leaves no running app process that locks build outputs.

## Attempt Loop

- Evaluation 1 fails: main agent fixes only evaluator-listed failures.
- Evaluation 2 fails: stop and escalate to a human.
- Blocked evaluation: stop and provide the human checklist.

## Report Format

The evaluator returns exactly these sections:

```text
PASS or FAIL

Observed
- <what was actually seen>

Failures
- <specific failed criterion, or None>

Screenshots inspected
- <initial state>
- <target state>

Commands run
- <command and result>

Human checklist
- <only include when failed twice or blocked>
```

## Human Checklist

Give the human:

- Original task goal
- Expected visible behavior
- Visual launch command
- Window title
- Interaction path
- Pass criteria
- Evaluator failures
- Commands run
- Files changed
