# Codex adapter — research notes and v1 plan

The Codex adapter (`scripts/adapters/codex.js`) is a deliberate stub. This file records
why, what must be confirmed before implementing it, and the conservative path to a v1.

## Why it isn't implemented yet

Claude Code writes readable per-session JSONL with a stable `message.usage` shape, so the
Claude adapter can read real token counts directly. Codex's situation is different:

- Its stable, **documented** surfaces (telemetry, hooks, `/status`) are not the same as a
  readable transcript file.
- The public docs do **not** establish a stable contract for parsing Codex's saved local
  history. Building a scraper against an undocumented file shape would be guesswork and
  would break silently when the format changes.

The framework rule applies: **prefer official telemetry or hook-accessible usage data;
treat private transcript parsing as a documented fallback only after a stable file shape
and compatibility story are confirmed.**

## Known Codex surfaces (from official docs)

- `/status` displays session configuration and token usage.
- The TUI statusline can show token counters.
- `config.toml` supports lifecycle hooks when `features.hooks` is enabled.
- Codex telemetry includes `turn.token_usage` with token types: `total`, `input`,
  `cached_input`, `output`, and `reasoning_output`.
- Codex saves local history when `history.persistence = "save-all"`, but the public docs
  do not establish a stable transcript-parsing contract.

## Open questions (answer before implementing)

1. Is there a stable local transcript or SQLite location, and is its schema documented and
   versioned?
2. What is the best token source: OpenTelemetry metrics, `config.toml` hooks, an
   app-server API, `/status` output, or saved local history?
3. Can a Codex plugin register a true slash command (`/token-stats`-style), or should the
   integration rely on a skill plus hooks?
4. For ChatGPT-plan usage, can usage map to per-token USD at all, or should the report show
   token totals and usage pressure only (dollars reserved for API / flexible-pricing setups)?

## Recommended v1 path

1. Prefer official telemetry or hook-accessible usage data over transcript scraping.
2. Map Codex's token types onto the normalized receipt:
   - `input` → `input_tokens`
   - `cached_input` → `cached_input_tokens`
   - `output` → `output_tokens`
   - `reasoning_output` → `reasoning_output_tokens`
   - `total` → `total_tokens`
3. Package as a Codex **plugin** when distribution needs scripts, hooks, and a skill
   together. Include a `token-stats` skill for explicit `$token-stats` use and scripts that
   summarize any collected receipts.
4. Distinguish tokens from dollars in cost reporting (see open question 4).
5. Implement `scan()` / `current()` in `codex.js` to return the same normalized receipt
   shape the Claude adapter produces, then register the adapter (already wired in
   `adapters/index.js`). Add fixture tests for the `input` / `cached_input` / `output` /
   `reasoning_output` / `total` token types.

Only add private-transcript parsing as a documented fallback once a stable file shape and
compatibility story are confirmed.
