// Aggregation: filtering windows and grouping.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { filterReceipts, summarize } from '../lib/summary.js';

function receipt(overrides) {
  return {
    provider: 'claude',
    session_id: Math.random().toString(36).slice(2),
    project_path: '/home/u/proj-a',
    model: 'claude-opus-4-8',
    updated_at: new Date().toISOString(),
    turns: 1,
    total_tokens: 100,
    estimated_cost_usd: 0.01,
    ...overrides,
  };
}

test('--since excludes receipts older than the window', () => {
  const old = receipt({ updated_at: '2020-01-01T00:00:00.000Z', total_tokens: 999 });
  const recent = receipt({ total_tokens: 100 });
  const kept = filterReceipts([old, recent], { since: '7d' });
  assert.equal(kept.length, 1);
  assert.equal(kept[0].total_tokens, 100);
});

test('project and model filters narrow the set', () => {
  const set = [
    receipt({ project_path: '/home/u/proj-a', model: 'claude-opus-4-8' }),
    receipt({ project_path: '/home/u/proj-b', model: 'claude-sonnet-4-6' }),
  ];
  assert.equal(filterReceipts(set, { project: 'proj-b' }).length, 1);
  assert.equal(filterReceipts(set, { model: 'claude-sonnet' }).length, 1);
});

test('summarize groups by model and totals tokens and cost', () => {
  const set = [
    receipt({ model: 'claude-opus-4-8', total_tokens: 100, estimated_cost_usd: 0.01 }),
    receipt({ model: 'claude-opus-4-8', total_tokens: 200, estimated_cost_usd: 0.02 }),
    receipt({ model: 'claude-haiku-4-5', total_tokens: 50, estimated_cost_usd: 0.001 }),
  ];
  const { groups, total } = summarize(set, 'model');
  assert.equal(groups.length, 2);
  const opus = groups.find((g) => g.key === 'claude-opus-4-8');
  assert.equal(opus.sessions, 2);
  assert.equal(opus.total_tokens, 300);
  assert.ok(Math.abs(opus.estimated_cost_usd - 0.03) < 1e-9);
  assert.equal(total.total_tokens, 350);
});

test('an unpriced receipt flags the bucket cost as approximate', () => {
  const set = [
    receipt({ estimated_cost_usd: 0.01 }),
    receipt({ estimated_cost_usd: null }),
  ];
  const { total } = summarize(set, 'provider');
  assert.equal(total.cost_known, false);
});
