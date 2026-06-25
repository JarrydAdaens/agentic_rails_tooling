// Ledger: upsert keeps one latest snapshot per session.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { readLedger, upsertReceipts } from '../lib/ledger.js';

function tempLedger() {
  const dir = mkdtempSync(join(tmpdir(), 'token-stats-test-'));
  return { file: join(dir, 'ledger.jsonl'), dir };
}

function receipt(overrides) {
  return {
    provider: 'claude',
    session_id: 'sess-1',
    updated_at: '2026-06-10T10:00:00.000Z',
    total_tokens: 100,
    ...overrides,
  };
}

test('reading a missing ledger returns an empty array', () => {
  const { file, dir } = tempLedger();
  assert.deepEqual(readLedger(file), []);
  rmSync(dir, { recursive: true, force: true });
});

test('first write adds receipts; re-scan with newer totals updates in place', () => {
  const { file, dir } = tempLedger();

  let result = upsertReceipts([receipt()], file);
  assert.deepEqual(result, { added: 1, updated: 0 });

  result = upsertReceipts([receipt({
    updated_at: '2026-06-10T11:00:00.000Z',
    total_tokens: 250,
  })], file);
  assert.deepEqual(result, { added: 0, updated: 1 });

  const ledger = readLedger(file);
  assert.equal(ledger.length, 1, 'duplicate session is not appended');
  assert.equal(ledger[0].total_tokens, 250, 'latest snapshot wins');

  rmSync(dir, { recursive: true, force: true });
});

test('distinct sessions and providers coexist', () => {
  const { file, dir } = tempLedger();
  upsertReceipts([
    receipt({ session_id: 'a' }),
    receipt({ session_id: 'b' }),
    receipt({ provider: 'codex', session_id: 'a' }),
  ], file);
  assert.equal(readLedger(file).length, 3);
  rmSync(dir, { recursive: true, force: true });
});

test('a stale snapshot does not overwrite a newer one', () => {
  const { file, dir } = tempLedger();
  upsertReceipts([receipt({ updated_at: '2026-06-10T12:00:00.000Z', total_tokens: 500 })], file);
  const result = upsertReceipts([receipt({ updated_at: '2026-06-10T09:00:00.000Z', total_tokens: 1 })], file);
  assert.deepEqual(result, { added: 0, updated: 0 });
  assert.equal(readLedger(file)[0].total_tokens, 500);
  rmSync(dir, { recursive: true, force: true });
});
