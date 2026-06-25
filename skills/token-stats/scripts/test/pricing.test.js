// Cost model: known models priced, unknown models report tokens without cost.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { estimateCost, loadPricing } from '../lib/pricing.js';

function receipt(overrides) {
  return {
    provider: 'claude',
    model: 'claude-opus-4-8',
    input_tokens: 0,
    cache_creation_input_tokens: 0,
    cached_input_tokens: 0,
    output_tokens: 0,
    ...overrides,
  };
}

test('known model maps tokens to the expected dollar cost', () => {
  const { cost, priced } = estimateCost(receipt({
    input_tokens: 1_000_000,
    output_tokens: 1_000_000,
  }));
  assert.equal(priced, true);
  // opus-4-8: $5/M in + $25/M out = $30 for 1M each.
  assert.ok(Math.abs(cost - 30) < 1e-9);
});

test('cache tokens are billed at write (1.25x) and read (0.1x) multipliers', () => {
  const { cost } = estimateCost(receipt({
    cache_creation_input_tokens: 1_000_000,
    cached_input_tokens: 1_000_000,
  }));
  // 1M write * $5 * 1.25 = 6.25 ; 1M read * $5 * 0.1 = 0.5 → 6.75
  assert.ok(Math.abs(cost - 6.75) < 1e-9);
});

test('a dated/suffixed model id still matches by prefix', () => {
  const { priced, cost } = estimateCost(receipt({
    model: 'claude-opus-4-8-20260109',
    output_tokens: 1_000_000,
  }));
  assert.equal(priced, true);
  assert.ok(Math.abs(cost - 25) < 1e-9);
});

test('unknown model reports tokens without a cost', () => {
  const { cost, priced } = estimateCost(receipt({ model: 'claude-2.0', input_tokens: 5000 }));
  assert.equal(priced, false);
  assert.equal(cost, null);
});

test('pricing table exposes a version string', () => {
  const { table_version } = estimateCost(receipt());
  assert.equal(typeof table_version, 'string');
  assert.equal(table_version, loadPricing().version);
});
