---
name: token-stats
description: >
  Use this when you need real token-usage receipts and estimated cost for agentic
  IDE sessions — current session, recent sessions, or totals by day/project/model/provider.
  Reads actual token counts from session logs (Claude Code today, Codex later); it never
  asks a model to estimate and never stores prompt text. Trigger: "/token-stats",
  "how many tokens did this session use", "token cost so far", "show my usage this week",
  "export token usage", or whenever durable token/cost accounting is wanted across IDEs.
disable-model-invocation: true
metadata:
  version: "1.1"
---

# token-stats

Agent-neutral token receipts. Real counts from logs, no AI estimation.

## What it is

A small, dependency-free Node CLI (`scripts/token-stats.js`, Node 18+) with a neutral
core plus per-provider adapters. It reads the token counts that a provider already
records in its session logs/telemetry, normalizes them into a receipt, and keeps a
durable JSONL ledger. Costs are **estimates** derived from a bundled pricing table —
never billing truth, and clearly labeled.

**Core rule:** token totals come from logs. There are no caveman/heuristic assumptions;
if caveman mode is active it is recorded as an optional `caveman:on` tag only.

- **Claude adapter** (implemented): reads `$CLAUDE_CONFIG_DIR/projects/**.jsonl`
  (default `~/.claude/projects`), summing each assistant entry's `message.usage`:
  `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`.
- **Codex adapter** (research stub): intentionally not implemented against a private
  transcript format yet. See [`references/codex-research.md`](./references/codex-research.md).

Storage default: `%LOCALAPPDATA%\token-stats\ledger.jsonl` (Windows) or
`~/.local/share/token-stats/ledger.jsonl` (POSIX). Only metadata and counters are
stored — never prompt text. Override the location with `TOKEN_STATS_DIR`.

## Trigger

- `/token-stats` (Claude Code, via the optional hook below)
- "how many tokens / how much did this session cost"
- "show usage for the last 7 days", "totals by project/model"
- "export my token usage to CSV"

## Process

1. Locate the CLI at `skills/token-stats/scripts/token-stats.js`.
2. Run the relevant command with `node` (no install step — zero dependencies):

   ```
   node skills/token-stats/scripts/token-stats.js current
   node skills/token-stats/scripts/token-stats.js summary --since 7d
   node skills/token-stats/scripts/token-stats.js summary --by project
   node skills/token-stats/scripts/token-stats.js sessions --project "MyBrain"
   node skills/token-stats/scripts/token-stats.js export --format csv
   node skills/token-stats/scripts/token-stats.js prices
   ```

   `summary`/`sessions`/`export` auto-refresh the Claude ledger first (suppress with
   `--no-scan`). `scan` refreshes without printing a report.

3. Report the output to the user. Always present dollar figures as **estimates** and
   name the pricing-table version shown in the output.

## Commands & filters

| Command | Purpose |
|---|---|
| `current` | Most recent session receipt (`--project <substr>` to scope) |
| `scan` | Refresh the ledger from live logs |
| `summary` | Totals grouped by `--by day\|project\|model\|provider` |
| `sessions` | One row per recorded session |
| `export --format csv` | Dump filtered receipts as CSV |
| `prices [update]` | Show the bundled pricing table; `update` explains how to edit it |

Filters (where applicable): `--provider <id>`, `--project <substring>`,
`--model <prefix>`, `--since <7d\|24h\|ISO>`. Add `--json` for machine-readable output.

## Optional Claude Code `/token-stats` hook

`hooks/token-stats.js` is a `UserPromptSubmit` hook that intercepts a `/token-stats`
prompt, runs the CLI, and returns the formatted receipt + recent summary as a blocked
decision — the model does not compute the numbers. Wire it in `settings.json`:

```json
{ "hooks": { "UserPromptSubmit": [ { "hooks": [
  { "type": "command",
    "command": "node \"<abs-path>/skills/token-stats/hooks/token-stats.js\"" }
] } ] } }
```

Prompt forms: `/token-stats`, `/token-stats --all`, `/token-stats --since 7d`.

## Cost model

Pricing lives in `scripts/pricing.json` (versioned, per provider/model/token-type),
kept separate from the parsers. Cache tokens are billed at the provider's write and
read multipliers; unknown models report token totals **without** a dollar cost rather
than guessing. For Codex/ChatGPT-plan usage, token totals are the primary signal —
dollars only apply under per-token (API/flexible) pricing.

## Tests

`node --test scripts/test/*.test.js` — covers full input/cache/output accounting,
malformed JSONL, multi-model sessions, empty sessions, duplicate-snapshot dedup, known
vs unknown model pricing, prefix matching, `--since`/grouping, and the pricing-table
version stamp.

## See also

- [`README.md`](./README.md) — overview and example output
- [`references/codex-research.md`](./references/codex-research.md) — Codex open questions and v1 plan
