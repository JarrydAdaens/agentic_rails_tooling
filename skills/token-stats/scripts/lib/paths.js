// Cross-platform path resolution for token-stats storage and provider log roots.
//
// Storage default:
//   Windows:      %LOCALAPPDATA%\token-stats\ledger.jsonl
//   macOS/Linux:  ~/.local/share/token-stats/ledger.jsonl
//
// Everything here is pure path math plus environment lookups — no file content
// is read, so importing this module is cheap and side-effect free.

import { homedir, platform } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const isWindows = platform() === 'win32';

// Root directory for token-stats' own durable data (the global ledger).
export function dataDir() {
  if (process.env.TOKEN_STATS_DIR) {
    return process.env.TOKEN_STATS_DIR;
  }
  if (isWindows) {
    const local = process.env.LOCALAPPDATA || join(homedir(), 'AppData', 'Local');
    return join(local, 'token-stats');
  }
  const xdg = process.env.XDG_DATA_HOME || join(homedir(), '.local', 'share');
  return join(xdg, 'token-stats');
}

// The normalized cross-provider receipt ledger.
export function ledgerPath() {
  return join(dataDir(), 'ledger.jsonl');
}

// Root directory that holds Claude Code's per-project JSONL session logs.
// Honors CLAUDE_CONFIG_DIR so non-default installs are picked up.
export function claudeProjectsDir() {
  const base = process.env.CLAUDE_CONFIG_DIR || join(homedir(), '.claude');
  return join(base, 'projects');
}

// Directory of the running script — used to locate pricing.json next to the CLI.
export function scriptDir() {
  return dirname(fileURLToPath(import.meta.url));
}
