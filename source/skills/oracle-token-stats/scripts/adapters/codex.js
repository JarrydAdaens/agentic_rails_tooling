// Codex adapter — research stub.
//
// This adapter is intentionally NOT implemented against a private transcript
// format. Codex's stable, documented token surfaces (OpenTelemetry
// `turn.token_usage`, config.toml lifecycle hooks, `/status`) differ from Claude
// Code's readable JSONL, and the public docs do not establish a stable
// transcript-parsing contract. Shipping a scraper now would be guesswork.
//
// See ../../references/codex-research.md for the open questions that must be
// answered before this becomes a real adapter, and the conservative v1 plan
// (prefer official telemetry / hooks over private log parsing).
//
// The seam exists so the core CLI is provider-neutral: when a stable Codex data
// source is confirmed, implement scan()/current() here to return the same
// normalized receipt shape the Claude adapter produces, then register it in
// adapters/index.js.

export const name = 'codex';

const GUIDANCE =
  'The Codex adapter is not implemented yet. Codex needs a confirmed, stable token ' +
  'source (official telemetry/hooks preferred over private transcript parsing). ' +
  'See references/codex-research.md.';

export function scan() {
  return { receipts: [], malformed: 0, scanned: 0, root: null, notImplemented: true, guidance: GUIDANCE };
}

export function current() {
  return null;
}
