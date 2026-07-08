// Human-readable and CSV rendering of receipts and summaries.

import { formatInt, formatUsd } from './util.js';

// One-session receipt, e.g. for `current`.
export function formatReceipt(receipt) {
  const lines = [];
  lines.push(`Provider: ${receipt.provider}`);
  lines.push(`Model:    ${receipt.model || 'unknown'}`);
  if (receipt.project_path) {
    lines.push(`Project:  ${receipt.project_path}`);
  }
  lines.push(`Session:  ${receipt.session_id}  (${formatInt(receipt.turns)} turns)`);
  lines.push('');
  lines.push(`Input:        ${formatInt(receipt.input_tokens)} tokens (uncached)`);
  if (receipt.cache_creation_input_tokens) {
    lines.push(`Cache write:  ${formatInt(receipt.cache_creation_input_tokens)} tokens`);
  }
  if (receipt.cached_input_tokens) {
    lines.push(`Cache read:   ${formatInt(receipt.cached_input_tokens)} tokens`);
  }
  lines.push(`Output:       ${formatInt(receipt.output_tokens)} tokens`);
  if (receipt.reasoning_output_tokens) {
    lines.push(`  reasoning:  ${formatInt(receipt.reasoning_output_tokens)} tokens`);
  }
  lines.push(`Total:        ${formatInt(receipt.total_tokens)} tokens`);
  lines.push('');
  lines.push(`Est. cost:    ${formatUsd(receipt.estimated_cost_usd)} (pricing ${receipt.pricing_table_version || 'n/a'})`);
  if (receipt.estimated_cost_usd === null) {
    lines.push(`              model not in pricing table — tokens reported without cost`);
  }
  if (receipt.tags && receipt.tags.length) {
    lines.push(`Tags:         ${receipt.tags.join(', ')}`);
  }
  return lines.join('\n');
}

// Grouped summary table.
export function formatSummary(result, by) {
  const { groups, total } = result;
  const lines = [];
  const label = { day: 'Day', project: 'Project', model: 'Model', provider: 'Provider' }[by] || 'Group';

  const header = `${label.padEnd(28)} ${'Sess'.padStart(5)} ${'Total tok'.padStart(12)} ${'Est. cost'.padStart(11)}`;
  lines.push(header);
  lines.push('-'.repeat(header.length));

  for (const row of groups) {
    lines.push(formatRow(row.key, row, by, label.length));
  }

  lines.push('-'.repeat(header.length));
  lines.push(formatRow('TOTAL', total, by, label.length));
  return lines.join('\n');
}

function formatRow(key, bucket, by, labelLen) {
  const width = Math.max(28, labelLen);
  let display = String(key);
  if (by === 'project' && display.length > width) {
    display = `…${display.slice(-(width - 1))}`; // keep the meaningful tail of a path
  } else if (display.length > width) {
    display = display.slice(0, width);
  }
  const cost = bucket.cost_known ? formatUsd(bucket.estimated_cost_usd) : `~${formatUsd(bucket.estimated_cost_usd)}`;
  return `${display.padEnd(width)} ${String(bucket.sessions).padStart(5)} ${formatInt(bucket.total_tokens).padStart(12)} ${cost.padStart(11)}`;
}

// Session listing.
export function formatSessions(receipts) {
  if (!receipts.length) {
    return 'No sessions found. Run `token-stats scan` first.';
  }
  const lines = [];
  const header = `${'Updated'.padEnd(20)} ${'Provider'.padEnd(8)} ${'Turns'.padStart(5)} ${'Total tok'.padStart(12)} ${'Est. cost'.padStart(11)}  Project`;
  lines.push(header);
  lines.push('-'.repeat(header.length));
  const sorted = [...receipts].sort((a, b) => (a.updated_at < b.updated_at ? 1 : -1));
  for (const r of sorted) {
    const when = (r.updated_at || '').replace('T', ' ').slice(0, 19);
    const project = r.project_path || '';
    lines.push(
      `${when.padEnd(20)} ${(r.provider || '').padEnd(8)} ${formatInt(r.turns).padStart(5)} ` +
      `${formatInt(r.total_tokens).padStart(12)} ${formatUsd(r.estimated_cost_usd).padStart(11)}  ${project}`,
    );
  }
  return lines.join('\n');
}

// Oracle Server /v1/usage/window response ({ window, fromUtc, toUtc, rows, totals })
// rendered as a composite (machine, source, model) table. Server figures are
// cache-inclusive totals; costUsd is null when no row carried a cost.
export function formatWindowUsage(response) {
  const lines = [];
  const bucket = `${(response.fromUtc || '').slice(0, 10)} → ${(response.toUtc || '').slice(0, 10)}`;
  lines.push(`Window: ${response.window} (UTC ${bucket})`);

  if (!response.rows || !response.rows.length) {
    lines.push('No usage recorded in this window.');
    return lines.join('\n');
  }

  const header = `${'Machine'.padEnd(14)} ${'Source'.padEnd(16)} ${'Model'.padEnd(24)} ${'Total tok'.padStart(12)} ${'Est. cost'.padStart(11)}`;
  lines.push(header);
  lines.push('-'.repeat(header.length));
  for (const row of response.rows) {
    lines.push(
      `${String(row.machine || '').padEnd(14)} ${String(row.source || '').padEnd(16)} ` +
      `${String(row.model || '').padEnd(24)} ${formatInt(row.totalTokens).padStart(12)} ` +
      `${formatUsd(row.costUsd).padStart(11)}`,
    );
  }
  lines.push('-'.repeat(header.length));
  const totals = response.totals || {};
  lines.push(
    `${'TOTAL'.padEnd(14)} ${''.padEnd(16)} ${''.padEnd(24)} ` +
    `${formatInt(totals.totalTokens).padStart(12)} ${formatUsd(totals.costUsd).padStart(11)}`,
  );
  return lines.join('\n');
}

// CSV export. Quotes only the free-text path field; counters are plain numbers.
export function formatCsv(receipts) {
  const columns = [
    'provider', 'session_id', 'project_path', 'started_at', 'updated_at', 'model',
    'turns', 'input_tokens', 'cache_creation_input_tokens', 'cached_input_tokens',
    'output_tokens', 'reasoning_output_tokens', 'total_tokens',
    'estimated_cost_usd', 'pricing_table_version', 'tags',
  ];
  const rows = [columns.join(',')];
  for (const r of receipts) {
    rows.push(columns.map((col) => csvCell(r[col])).join(','));
  }
  return rows.join('\n');
}

function csvCell(value) {
  if (value === null || value === undefined) {
    return '';
  }
  if (Array.isArray(value)) {
    value = value.join(';');
  }
  const str = String(value);
  if (/[",\n]/.test(str)) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}
