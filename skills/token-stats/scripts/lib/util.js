// Small dependency-free helpers: argument parsing, duration windows, formatting.

// Parse `argv` (after the subcommand) into { _: [positionals], flags: {...} }.
// Supports `--key value`, `--key=value`, and bare `--flag` (boolean true).
export function parseArgs(argv) {
  const flags = {};
  const positionals = [];

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const body = token.slice(2);
      const eq = body.indexOf('=');
      if (eq !== -1) {
        flags[body.slice(0, eq)] = body.slice(eq + 1);
      } else if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
        flags[body] = argv[i + 1];
        i += 1;
      } else {
        flags[body] = true;
      }
    } else {
      positionals.push(token);
    }
  }

  return { _: positionals, flags };
}

// Resolve a `--since` value to an epoch-millis lower bound, or null for "all time".
// Accepts relative windows (`7d`, `24h`, `90m`, `2w`) or any Date-parseable string.
export function sinceToEpochMs(since) {
  if (since === undefined || since === null || since === '') {
    return null;
  }
  const relative = String(since).trim().match(/^(\d+)\s*([smhdw])$/i);
  if (relative) {
    const amount = Number(relative[1]);
    const unitMs = { s: 1e3, m: 6e4, h: 36e5, d: 864e5, w: 6048e5 }[relative[2].toLowerCase()];
    return Date.now() - amount * unitMs;
  }
  const parsed = Date.parse(since);
  return Number.isNaN(parsed) ? null : parsed;
}

// UTC calendar day (YYYY-MM-DD) for grouping. Falsy/invalid input → 'unknown'.
export function dayKey(isoOrMs) {
  if (!isoOrMs) {
    return 'unknown';
  }
  const ms = typeof isoOrMs === 'number' ? isoOrMs : Date.parse(isoOrMs);
  if (Number.isNaN(ms)) {
    return 'unknown';
  }
  return new Date(ms).toISOString().slice(0, 10);
}

// Thousands-separated integer, e.g. 12304 -> "12,304".
export function formatInt(n) {
  return Math.round(n || 0).toLocaleString('en-US');
}

// Dollar amount to 4 decimal places, or "—" when cost is unknown.
export function formatUsd(amount) {
  if (amount === null || amount === undefined) {
    return '—';
  }
  return `$${amount.toFixed(4)}`;
}

// Compact token count for badges/inline use, e.g. 12345 -> "12.3k".
export function formatCompact(n) {
  const value = Math.round(n || 0);
  if (value < 1000) {
    return String(value);
  }
  return `${(value / 1000).toFixed(1)}k`;
}
