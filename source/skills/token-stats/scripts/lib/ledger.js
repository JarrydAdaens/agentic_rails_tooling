// Normalized JSONL ledger: one latest snapshot per session, keyed by
// provider + session_id. Storing metadata and counters only — never prompt text.

import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname } from 'node:path';
import { ledgerPath } from './paths.js';

function keyOf(receipt) {
  return `${receipt.provider}:${receipt.session_id}`;
}

// Read the ledger into an array of receipts. Malformed lines are skipped so a
// single bad write never poisons the whole history.
export function readLedger(file = ledgerPath()) {
  if (!existsSync(file)) {
    return [];
  }
  const receipts = [];
  for (const line of readFileSync(file, 'utf8').split('\n')) {
    const trimmed = line.trim();
    if (!trimmed) {
      continue;
    }
    try {
      receipts.push(JSON.parse(trimmed));
    } catch {
      // Skip corrupt line; the rest of the ledger is still usable.
    }
  }
  return receipts;
}

// Merge fresh receipts into the ledger, keeping the snapshot with the latest
// updated_at per session. Returns { added, updated } counts.
export function upsertReceipts(incoming, file = ledgerPath()) {
  const byKey = new Map();
  for (const receipt of readLedger(file)) {
    byKey.set(keyOf(receipt), receipt);
  }

  let added = 0;
  let updated = 0;
  for (const receipt of incoming) {
    const key = keyOf(receipt);
    const existing = byKey.get(key);
    if (!existing) {
      byKey.set(key, receipt);
      added += 1;
    } else if (isNewer(receipt, existing)) {
      byKey.set(key, receipt);
      updated += 1;
    }
  }

  writeLedger([...byKey.values()], file);
  return { added, updated };
}

function isNewer(candidate, existing) {
  const a = Date.parse(candidate.updated_at || '') || 0;
  const b = Date.parse(existing.updated_at || '') || 0;
  // On a tie, the candidate wins — a re-scan reflects the latest totals.
  return a >= b;
}

function writeLedger(receipts, file = ledgerPath()) {
  mkdirSync(dirname(file), { recursive: true });
  const body = receipts.map((r) => JSON.stringify(r)).join('\n');
  writeFileSync(file, body ? `${body}\n` : '', 'utf8');
}
