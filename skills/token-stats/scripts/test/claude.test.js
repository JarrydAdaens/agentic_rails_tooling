// Claude adapter: parsing real session logs into normalized receipts.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { scan, current } from '../adapters/claude.js';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, 'fixtures', 'projects');

function scanFixtures() {
  return scan({ root });
}

function receiptFor(sessionId) {
  return scanFixtures().receipts.find((r) => r.session_id === sessionId);
}

test('scans all session files and skips empty/malformed-only sessions', () => {
  const result = scanFixtures();
  assert.equal(result.scanned, 4, 'four .jsonl files exist across two projects');
  // full, malformed (still has one valid entry), multimodel — empty produces none.
  assert.equal(result.receipts.length, 3);
});

test('counts malformed JSONL lines without dropping the file', () => {
  const result = scanFixtures();
  assert.equal(result.malformed, 1, 'one corrupt line in malformed-session.jsonl');
  const bad = result.receipts.find((r) => r.session_id === 'sess-bad');
  assert.ok(bad, 'the valid assistant entry still yields a receipt');
  assert.equal(bad.input_tokens, 5);
  assert.equal(bad.output_tokens, 7);
});

test('accumulates full input/cache/output accounting across turns', () => {
  const r = receiptFor('sess-full');
  assert.equal(r.turns, 2);
  assert.equal(r.input_tokens, 110); // 100 + 10
  assert.equal(r.cache_creation_input_tokens, 200);
  assert.equal(r.cached_input_tokens, 900); // 300 + 600 cache reads
  assert.equal(r.output_tokens, 130); // 50 + 80
  assert.equal(r.total_tokens, 1340); // 110 + 200 + 900 + 130
});

test('prices a known model and records the pricing table version', () => {
  const r = receiptFor('sess-full');
  // 110*5 + 200*5*1.25 + 900*5*0.1 + 130*25, all /1e6 → 0.0055
  assert.ok(Math.abs(r.estimated_cost_usd - 0.0055) < 1e-9);
  assert.ok(r.pricing_table_version, 'version is stamped onto the receipt');
});

test('keeps the last-seen model when a session spans multiple models', () => {
  const r = receiptFor('sess-multi');
  assert.equal(r.model, 'claude-sonnet-4-6');
  assert.equal(r.total_tokens, 600);
});

test('captures session id, project path, and time bounds', () => {
  const r = receiptFor('sess-full');
  assert.equal(r.project_path, '/home/u/proj-a');
  assert.equal(r.started_at, '2026-06-10T10:00:00.000Z');
  assert.equal(r.updated_at, '2026-06-10T10:01:05.000Z');
});

test('current() returns the most recently updated session', () => {
  const r = current({ root });
  assert.equal(r.session_id, 'sess-multi'); // 2026-06-12 is the latest updated_at
});

test('current() honours a project filter', () => {
  const r = current({ root, project: 'proj-a' });
  assert.equal(r.project_path, '/home/u/proj-a');
  assert.equal(r.session_id, 'sess-bad'); // proj-a's latest is the 06-11 session
});
