// Aggregation over normalized receipts: filtering and grouping by
// day / project / model / provider. Pure functions over receipt arrays.

import { sinceToEpochMs, dayKey } from './util.js';

// Filter receipts by provider, project substring, model prefix, and a --since window.
export function filterReceipts(receipts, { since, project, provider, model } = {}) {
  const sinceMs = sinceToEpochMs(since);
  return receipts.filter((r) => {
    if (provider && r.provider !== provider) {
      return false;
    }
    if (model && !(r.model || '').startsWith(model)) {
      return false;
    }
    if (project && !(r.project_path || '').toLowerCase().includes(String(project).toLowerCase())) {
      return false;
    }
    if (sinceMs !== null) {
      const ts = Date.parse(r.updated_at || '') || 0;
      if (ts < sinceMs) {
        return false;
      }
    }
    return true;
  });
}

function emptyBucket() {
  return {
    sessions: 0,
    turns: 0,
    input_tokens: 0,
    cache_creation_input_tokens: 0,
    cached_input_tokens: 0,
    output_tokens: 0,
    reasoning_output_tokens: 0,
    total_tokens: 0,
    estimated_cost_usd: 0,
    cost_known: true,
  };
}

function addReceipt(bucket, r) {
  bucket.sessions += 1;
  bucket.turns += r.turns || 0;
  bucket.input_tokens += r.input_tokens || 0;
  bucket.cache_creation_input_tokens += r.cache_creation_input_tokens || 0;
  bucket.cached_input_tokens += r.cached_input_tokens || 0;
  bucket.output_tokens += r.output_tokens || 0;
  bucket.reasoning_output_tokens += r.reasoning_output_tokens || 0;
  bucket.total_tokens += r.total_tokens || 0;
  if (r.estimated_cost_usd === null || r.estimated_cost_usd === undefined) {
    bucket.cost_known = false;
  } else {
    bucket.estimated_cost_usd += r.estimated_cost_usd;
  }
}

function keyFor(receipt, by) {
  switch (by) {
    case 'day':
      return dayKey(receipt.updated_at);
    case 'project':
      return receipt.project_path || 'unknown';
    case 'model':
      return receipt.model || 'unknown';
    case 'provider':
      return receipt.provider || 'unknown';
    default:
      return 'all';
  }
}

// Group receipts into named buckets. `by` is one of day|project|model|provider.
// Returns { groups: [{ key, ...totals }], total: {...totals} } sorted by key.
export function summarize(receipts, by = 'day') {
  const groups = new Map();
  const total = emptyBucket();

  for (const r of receipts) {
    const key = keyFor(r, by);
    if (!groups.has(key)) {
      groups.set(key, emptyBucket());
    }
    addReceipt(groups.get(key), r);
    addReceipt(total, r);
  }

  const rows = [...groups.entries()]
    .map(([key, bucket]) => ({ key, ...bucket }))
    .sort((a, b) => (a.key < b.key ? 1 : -1)); // newest day / Z-A; stable enough

  return { groups: rows, total };
}
