// Provider adapter registry. Each adapter exposes the same surface:
//   name              — provider id used in receipts and on the CLI
//   scan(opts)        — { receipts, malformed, scanned, root, notImplemented? }
//   current(opts)     — a single receipt or null

import * as claude from './claude.js';
import * as codex from './codex.js';

const adapters = {
  claude,
  codex,
};

export function getAdapter(provider) {
  const adapter = adapters[provider];
  if (!adapter) {
    throw new Error(
      `Unknown provider "${provider}". Available: ${Object.keys(adapters).join(', ')}.`,
    );
  }
  return adapter;
}

export function listProviders() {
  return Object.keys(adapters);
}
