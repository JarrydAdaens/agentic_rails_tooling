# token-stats

Durable, agent-neutral token receipts and estimated cost for agentic IDE sessions.
Real counts from logs — no AI estimation, no stored prompt text.

## What it does

`token-stats` is a small Node CLI (stdlib only, Node 18+) with a provider-neutral core
and per-provider adapters. It reads the token counts a provider already records in its
session logs, normalizes them into a receipt, keeps a JSONL ledger in your user profile,
and reports current/recent/aggregate usage with **estimated** cost.

It is the general-purpose successor to the caveman-specific `caveman-stats` skill: the
caveman coupling is gone. Token totals always come from logs; caveman mode, if active,
is recorded only as a `caveman:on` tag.

## Providers

- **Claude Code** (implemented) — reads `$CLAUDE_CONFIG_DIR/projects/**.jsonl`
  (default `~/.claude/projects`), with full accounting of fresh input, cache-write,
  cache-read, and output tokens.
- **Codex** (research stub) — deliberately not implemented against a private transcript
  format. See [`references/codex-research.md`](./references/codex-research.md).

## Install / run

No install — zero dependencies. Run with `node`:

```
node skills/token-stats/scripts/token-stats.js <command> [flags]
```

Optionally `npm link` inside `scripts/` to expose a global `token-stats` binary.

## Commands

```bash
token-stats current  --provider claude            # current session receipt
token-stats scan     --provider claude            # refresh the ledger from logs
token-stats summary  --since 7d                   # totals for the last 7 days
token-stats summary  --by project                 # totals grouped by project
token-stats sessions --project "MyBrain"          # session rows for one project
token-stats export   --format csv                 # CSV of filtered receipts
token-stats prices                                # show the bundled pricing table
```

Filters: `--provider`, `--project <substring>`, `--model <prefix>`, `--since <7d|24h|ISO>`.
`--json` gives machine-readable output. `summary`/`sessions`/`export` auto-refresh the
Claude ledger first; pass `--no-scan` to read the ledger as-is.

## Example output

```
Provider: claude
Model:    claude-opus-4-8
Project:  D:\Code Projects\MyBrain
Session:  3f9c…  (47 turns)

Input:        12,304 tokens (uncached)
Cache write:   8,900 tokens
Cache read:  211,400 tokens
Output:        3,891 tokens
Total:       236,495 tokens

Est. cost:    $0.2143 (pricing 2026-06-18)
```

## Storage

- Windows: `%LOCALAPPDATA%\token-stats\ledger.jsonl`
- macOS/Linux: `~/.local/share/token-stats/ledger.jsonl`
- Override with `TOKEN_STATS_DIR`.

Only metadata and token counters are stored — never prompt text.

## Cost model

Rates live in [`scripts/pricing.json`](./scripts/pricing.json), versioned and kept
separate from the parsers. Cache tokens use the provider's write/read multipliers.
Unknown models report tokens **without** a dollar cost. Every report names the pricing
table version. Dollars are estimates, not billing truth.

## Tests

```
node --test skills/token-stats/scripts/test/*.test.js
```

## See also

- [`SKILL.md`](./SKILL.md) — trigger, workflow, and hook contract
- [`references/codex-research.md`](./references/codex-research.md) — Codex open questions and v1 plan
- [`../caveman-stats/`](../caveman-stats/) — the caveman-specific predecessor
