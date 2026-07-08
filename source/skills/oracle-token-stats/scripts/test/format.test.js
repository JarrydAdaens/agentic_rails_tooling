// Rendering of server window-usage responses (the live command's server table).

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { formatWindowUsage } from '../lib/format.js';

test('formatWindowUsage renders composite rows, totals, and the UTC bucket', () => {
  const text = formatWindowUsage({
    window: 'today',
    fromUtc: '2026-07-08T00:00:00Z',
    toUtc: '2026-07-09T00:00:00Z',
    rows: [
      {
        machine: 'dev-jarryd', source: 'ccusage:claude', model: 'claude-fable-5',
        recordCount: 3, inputTokens: 100, outputTokens: 200, totalTokens: 31240998, costUsd: 51.204112,
      },
      {
        machine: 'dev-jarryd', source: 'llama.cpp', model: 'qwen3.6-27b-q4km',
        recordCount: 118, inputTokens: 1, outputTokens: 2, totalTokens: 1071241, costUsd: null,
      },
    ],
    totals: { inputTokens: 101, outputTokens: 202, totalTokens: 32312239, costUsd: 51.204112 },
  });

  assert.match(text, /Window: today \(UTC 2026-07-08 → 2026-07-09\)/);
  assert.match(text, /ccusage:claude/);
  assert.match(text, /31,240,998/);
  assert.match(text, /—/, 'null cost renders as the unknown-cost dash');
  assert.match(text, /TOTAL.*32,312,239/s);
});

test('formatWindowUsage says so when the window is empty', () => {
  const text = formatWindowUsage({
    window: 'week',
    fromUtc: '2026-07-06T00:00:00Z',
    toUtc: '2026-07-13T00:00:00Z',
    rows: [],
    totals: { inputTokens: 0, outputTokens: 0, totalTokens: 0, costUsd: null },
  });
  assert.match(text, /Window: week/);
  assert.match(text, /No usage recorded in this window\./);
});
