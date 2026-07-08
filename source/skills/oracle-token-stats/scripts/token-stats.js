#!/usr/bin/env node
// token-stats — agent-neutral token receipt CLI.
//
// Keeps durable records of conversation token usage and estimated cost across
// agentic IDEs. Reads real token counts from provider session logs/telemetry —
// it never asks a model to estimate, and never stores prompt text.
//
//   token-stats current  [--provider claude] [--project P] [--json]
//   token-stats scan     [--provider claude]
//   token-stats summary  [--since 7d] [--by day|project|model|provider] [filters]
//   token-stats sessions [--since 7d] [filters]
//   token-stats export   [--format csv] [filters]
//   token-stats prices   [update]
//   token-stats live     [--window today|week] [--json]
//
// Filters: --provider <id>  --project <substring>  --model <prefix>  --since <7d|ISO>
// Global:  --json (machine-readable output where supported)

import { getAdapter, listProviders } from './adapters/index.js';
import { readLedger, upsertReceipts } from './lib/ledger.js';
import { filterReceipts, summarize } from './lib/summary.js';
import { loadPricing } from './lib/pricing.js';
import { ledgerPath } from './lib/paths.js';
import { parseArgs } from './lib/util.js';
import { serverBaseUrl, probeHealth, fetchWindowUsage } from './lib/server-client.js';
import {
  formatReceipt, formatSummary, formatSessions, formatCsv, formatWindowUsage,
} from './lib/format.js';

function out(text) {
  process.stdout.write(`${text}\n`);
}

function fail(message) {
  process.stderr.write(`token-stats: ${message}\n`);
  process.exit(1);
}

// Refresh the ledger from a provider's live logs, returning the scan result.
function refresh(provider) {
  const adapter = getAdapter(provider);
  const result = adapter.scan();
  if (result.notImplemented) {
    return result;
  }
  upsertReceipts(result.receipts);
  return result;
}

const COMMANDS = {
  current(flags) {
    const provider = flags.provider || 'claude';
    const adapter = getAdapter(provider);
    const receipt = adapter.current({ project: flags.project });
    if (!receipt) {
      const adapterResult = adapter.scan();
      if (adapterResult.notImplemented) {
        return fail(adapterResult.guidance);
      }
      return out('No session found.');
    }
    // Keep the ledger in step with what we just read.
    upsertReceipts([receipt]);
    out(flags.json ? JSON.stringify(receipt, null, 2) : formatReceipt(receipt));
  },

  scan(flags) {
    const provider = flags.provider || 'claude';
    const result = refresh(provider);
    if (result.notImplemented) {
      return fail(result.guidance);
    }
    const malformedNote = result.malformed ? `, skipped ${result.malformed} malformed line(s)` : '';
    out(`Scanned ${result.scanned} ${provider} session log(s), recorded ${result.receipts.length} receipt(s)${malformedNote}.`);
    out(`Ledger: ${ledgerPath()}`);
  },

  summary(flags) {
    refreshIfClaude(flags);
    const by = flags.by || 'day';
    const receipts = filterReceipts(readLedger(), flags);
    const result = summarize(receipts, by);
    if (flags.json) {
      return out(JSON.stringify(result, null, 2));
    }
    if (!receipts.length) {
      return out('No receipts match. Run `token-stats scan` first, or widen --since.');
    }
    out(formatSummary(result, by));
  },

  sessions(flags) {
    refreshIfClaude(flags);
    const receipts = filterReceipts(readLedger(), flags);
    out(flags.json ? JSON.stringify(receipts, null, 2) : formatSessions(receipts));
  },

  export(flags) {
    refreshIfClaude(flags);
    const receipts = filterReceipts(readLedger(), flags);
    const format = flags.format || 'csv';
    if (format !== 'csv') {
      return fail(`Unsupported export format "${format}". Only "csv" is available.`);
    }
    out(formatCsv(receipts));
  },

  // Live burn awareness: server-sourced today/week usage when Oracle Server is
  // reachable, the existing local ledger otherwise. Output always names its
  // data source so a consumer can tell centralized truth from local receipts.
  async live(flags) {
    const windows = flags.window ? [String(flags.window)] : ['today', 'week'];
    for (const window of windows) {
      if (window !== 'today' && window !== 'week') {
        return fail(`Unsupported --window "${window}". Use "today" or "week".`);
      }
    }

    const baseUrl = serverBaseUrl();
    const probe = await probeHealth({ baseUrl });

    if (!probe.reachable) {
      return liveOffline(flags, windows, baseUrl, probe.reason);
    }

    if (flags.json) {
      const payload = { dataSource: 'server', serverUrl: baseUrl, windows: {} };
      for (const window of windows) {
        payload.windows[window] = await fetchWindowUsage(window, { baseUrl });
      }
      return out(JSON.stringify(payload, null, 2));
    }

    out(`Data source: server (Oracle Server at ${baseUrl}, health: ${probe.status})`);
    for (const window of windows) {
      const usage = await fetchWindowUsage(window, { baseUrl });
      out('');
      out(formatWindowUsage(usage));
    }
  },

  prices(flags, positionals) {
    const pricing = loadPricing();
    if (positionals[0] === 'update') {
      out('Pricing is bundled with this skill (no network fetch).');
      out('To change rates, edit pricing.json beside this CLI and bump its "version".');
      out('Authoritative Claude rates: the claude-api skill / platform.claude.com/docs/pricing.');
      return;
    }
    if (flags.json) {
      return out(JSON.stringify(pricing, null, 2));
    }
    out(`Pricing table version: ${pricing.version} (${pricing.unit}, ${pricing.currency})`);
    for (const [provider, table] of Object.entries(pricing.providers)) {
      out(`\n[${provider}]`);
      const models = Object.entries(table.models);
      if (!models.length) {
        out('  (no models priced)');
        continue;
      }
      for (const [model, rate] of models) {
        out(`  ${model.padEnd(20)} in $${rate.input}/M  out $${rate.output}/M`);
      }
    }
  },
};

// Offline half of `live`: the existing local ledger pipeline, explicitly labeled.
// Local approximations are rolling windows (last 24h / last 7d), not the server's
// UTC calendar-day / ISO-week buckets — said out loud rather than overstating.
function liveOffline(flags, windows, baseUrl, reason) {
  const sinceFor = { today: '24h', week: '7d' };
  refreshIfClaude(flags);

  if (flags.json) {
    const payload = {
      dataSource: 'offline — local ledger',
      serverUrl: baseUrl,
      serverError: reason,
      windows: {},
    };
    for (const window of windows) {
      const receipts = filterReceipts(readLedger(), { since: sinceFor[window] });
      payload.windows[window] = {
        approximation: `rolling last ${sinceFor[window]}, not a UTC calendar window`,
        summary: summarize(receipts, 'model'),
      };
    }
    return out(JSON.stringify(payload, null, 2));
  }

  out(`Data source: offline — local ledger (Oracle Server unreachable at ${baseUrl}: ${reason})`);
  for (const window of windows) {
    const since = sinceFor[window];
    const receipts = filterReceipts(readLedger(), { since });
    out('');
    out(`Window: ${window} (local approximation: rolling last ${since})`);
    if (!receipts.length) {
      out('No local receipts in this window. Run `token-stats scan` first.');
      continue;
    }
    out(formatSummary(summarize(receipts, 'model'), 'model'));
  }
}

// summary/sessions/export operate on the ledger; auto-refresh Claude so a first
// run works without a separate `scan`. Other providers read the ledger as-is.
function refreshIfClaude(flags) {
  if (flags['no-scan']) {
    return;
  }
  const provider = flags.provider || 'claude';
  if (provider === 'claude') {
    refresh('claude');
  }
}

function main() {
  const [, , command, ...rest] = process.argv;
  if (!command || command === '--help' || command === '-h' || command === 'help') {
    out('token-stats — real token receipts across agentic IDEs.');
    out('Commands: current | scan | summary | sessions | export | prices | live');
    out(`Providers: ${listProviders().join(', ')}`);
    out('See the skill README for full usage.');
    return;
  }
  const handler = COMMANDS[command];
  if (!handler) {
    return fail(`Unknown command "${command}". Try: ${Object.keys(COMMANDS).join(', ')}.`);
  }
  const { _, flags } = parseArgs(rest);
  // `live` is async (HTTP); the rest are sync. Promise.resolve covers both, and
  // a rejection (e.g. a mid-flight server error after a healthy probe) exits 1.
  Promise.resolve(handler(flags, _)).catch((error) => fail(error.message || String(error)));
}

main();
