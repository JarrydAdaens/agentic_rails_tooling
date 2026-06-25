// Cost model. Kept strictly separate from the log parsers so pricing can change
// without touching adapters. Costs are estimates, never billing truth.

import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { scriptDir } from './paths.js';

let cached = null;

// Load and memoize pricing.json (sits next to the CLI entry point).
export function loadPricing() {
  if (cached) {
    return cached;
  }
  const file = join(scriptDir(), '..', 'pricing.json');
  cached = JSON.parse(readFileSync(file, 'utf8'));
  return cached;
}

// Resolve the rate entry for a model by longest-prefix match. Claude Code and
// Codex both emit dated/suffixed model ids (e.g. claude-opus-4-8-20260109), so a
// plain key lookup would miss — we match the most specific configured prefix.
function findModelRate(providerTable, model) {
  if (!providerTable || !model) {
    return null;
  }
  const keys = Object.keys(providerTable.models)
    .filter((key) => model.startsWith(key))
    .sort((a, b) => b.length - a.length);
  return keys.length ? providerTable.models[keys[0]] : null;
}

// Compute an estimated USD cost for a normalized receipt.
// Returns { cost, priced, table_version }. `cost` is null when the model is not
// in the pricing table — token totals stay valid, only the dollar figure is absent.
export function estimateCost(receipt) {
  const pricing = loadPricing();
  const provider = pricing.providers[receipt.provider];
  const rate = findModelRate(provider, receipt.model);
  const version = pricing.version;

  if (!rate) {
    return { cost: null, priced: false, table_version: version };
  }

  const cache = provider.cache || { creation_multiplier: 1.25, read_multiplier: 0.1 };
  const perToken = (rate.input || 0) / 1e6;
  const outPerToken = (rate.output || 0) / 1e6;

  const cost =
    (receipt.input_tokens || 0) * perToken +
    (receipt.cache_creation_input_tokens || 0) * perToken * cache.creation_multiplier +
    (receipt.cached_input_tokens || 0) * perToken * cache.read_multiplier +
    (receipt.output_tokens || 0) * outPerToken;

  return { cost, priced: true, table_version: version };
}

// Attach estimated_cost_usd + pricing_table_version onto a receipt (in place).
export function priceReceipt(receipt) {
  const { cost, table_version } = estimateCost(receipt);
  // Round to 6 dp so the stored ledger/CSV carries clean values, not float noise.
  receipt.estimated_cost_usd = cost === null ? null : Math.round(cost * 1e6) / 1e6;
  receipt.pricing_table_version = table_version;
  return receipt;
}
