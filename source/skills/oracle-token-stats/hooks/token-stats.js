#!/usr/bin/env node
// Optional Claude Code UserPromptSubmit hook for `/token-stats`.
//
// Wiring (settings.json):
//   {
//     "hooks": {
//       "UserPromptSubmit": [
//         { "hooks": [ { "type": "command",
//           "command": "node \"<abs>/skills/oracle-token-stats/hooks/token-stats.js\"" } ] }
//       ]
//     }
//   }
//
// When the user submits a prompt beginning with `/token-stats`, this hook runs
// the token-stats CLI and returns the formatted output as a blocked-decision
// reason — the numbers come from session logs on disk, computed by the CLI, not
// by the model. Any other prompt passes through untouched.
//
// Supported prompt forms:
//   /token-stats            current session receipt + last 7 days
//   /token-stats --all      current session receipt + all-time summary
//   /token-stats --since 7d current session receipt + a custom window

import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const cli = join(here, '..', 'scripts', 'token-stats.js');

function readStdin() {
  try {
    return readFileSync(0, 'utf8'); // fd 0 — the hook payload Claude Code pipes in
  } catch {
    return '';
  }
}

// Pass through (no decision) — let Claude Code process the prompt normally.
function passThrough() {
  process.exit(0);
}

// Block the prompt and surface `text` to the user instead.
function block(text) {
  process.stdout.write(JSON.stringify({ decision: 'block', reason: text }));
  process.exit(0);
}

function runCli(args) {
  const result = spawnSync(process.execPath, [cli, ...args], { encoding: 'utf8' });
  if (result.status !== 0) {
    return (result.stderr || result.stdout || 'token-stats failed').trim();
  }
  return (result.stdout || '').trim();
}

function main() {
  let payload = {};
  try {
    payload = JSON.parse(readStdin() || '{}');
  } catch {
    passThrough();
  }

  const prompt = (payload.prompt || '').trim();
  if (!prompt.startsWith('/token-stats')) {
    passThrough();
  }

  const rest = prompt.slice('/token-stats'.length).trim().split(/\s+/).filter(Boolean);

  let summaryArgs = ['summary', '--since', '7d'];
  if (rest.includes('--all')) {
    summaryArgs = ['summary'];
  } else {
    const sinceIdx = rest.indexOf('--since');
    if (sinceIdx !== -1 && rest[sinceIdx + 1]) {
      summaryArgs = ['summary', '--since', rest[sinceIdx + 1]];
    }
  }

  const current = runCli(['current']);
  const summary = runCli(summaryArgs);
  block(`token-stats\n\n${current}\n\n${summary}`);
}

main();
