// Claude Code adapter.
//
// Reads Claude Code's local JSONL session logs (one file per session under
// $CLAUDE_CONFIG_DIR/projects, defaulting to ~/.claude/projects) and produces
// normalized token receipts. Token counts come straight from each assistant
// entry's `message.usage` — nothing is estimated.
//
// Full accounting: input_tokens (fresh/uncached), cache_creation_input_tokens,
// cache_read_input_tokens (→ cached_input_tokens), and output_tokens.

import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join, basename } from 'node:path';
import { claudeProjectsDir } from '../lib/paths.js';
import { priceReceipt } from '../lib/pricing.js';

export const name = 'claude';

// Find every *.jsonl session log under the projects root (one level of project dirs).
function findSessionFiles(root) {
  if (!existsSync(root)) {
    return [];
  }
  const files = [];
  for (const projectEntry of readdirSync(root, { withFileTypes: true })) {
    if (!projectEntry.isDirectory()) {
      continue;
    }
    const projectDir = join(root, projectEntry.name);
    for (const fileEntry of readdirSync(projectDir, { withFileTypes: true })) {
      if (fileEntry.isFile() && fileEntry.name.endsWith('.jsonl')) {
        files.push(join(projectDir, fileEntry.name));
      }
    }
  }
  return files;
}

// Parse a single session log into a normalized, priced receipt (or null if the
// file holds no assistant usage). `malformed` counts unparseable lines.
function parseSessionFile(file) {
  const usage = {
    input: 0,
    cacheCreation: 0,
    cacheRead: 0,
    output: 0,
    reasoning: 0,
  };
  let turns = 0;
  let malformed = 0;
  let model = '';
  let sessionId = '';
  let projectPath = '';
  let firstTs = null;
  let lastTs = null;

  const raw = readFileSync(file, 'utf8');
  for (const line of raw.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed) {
      continue;
    }
    let entry;
    try {
      entry = JSON.parse(trimmed);
    } catch {
      malformed += 1;
      continue;
    }

    if (entry.sessionId && !sessionId) {
      sessionId = entry.sessionId;
    }
    if (entry.cwd) {
      projectPath = entry.cwd; // last writer wins — reflects the session's working dir
    }
    if (entry.timestamp) {
      const ts = Date.parse(entry.timestamp);
      if (!Number.isNaN(ts)) {
        if (firstTs === null || ts < firstTs) {
          firstTs = ts;
        }
        if (lastTs === null || ts > lastTs) {
          lastTs = ts;
        }
      }
    }

    const u = entry.type === 'assistant' && entry.message && entry.message.usage;
    if (u) {
      turns += 1;
      if (entry.message.model) {
        model = entry.message.model;
      }
      usage.input += u.input_tokens || 0;
      usage.cacheCreation += u.cache_creation_input_tokens || 0;
      usage.cacheRead += u.cache_read_input_tokens || 0;
      usage.output += u.output_tokens || 0;
      // Claude folds reasoning into output today; surface the field if present.
      usage.reasoning += u.reasoning_output_tokens || 0;
    }
  }

  if (turns === 0) {
    return { receipt: null, malformed };
  }

  const stat = statSync(file);
  const mtimeIso = stat.mtime.toISOString();
  const startedAt = firstTs !== null ? new Date(firstTs).toISOString() : mtimeIso;
  const updatedAt = lastTs !== null ? new Date(lastTs).toISOString() : mtimeIso;

  const receipt = {
    provider: 'claude',
    session_id: sessionId || basename(file, '.jsonl'),
    project_path: projectPath,
    started_at: startedAt,
    updated_at: updatedAt,
    model,
    turns,
    input_tokens: usage.input,
    cache_creation_input_tokens: usage.cacheCreation,
    cached_input_tokens: usage.cacheRead,
    output_tokens: usage.output,
    reasoning_output_tokens: usage.reasoning,
    total_tokens: usage.input + usage.cacheCreation + usage.cacheRead + usage.output,
    source_file: file,
    tags: cavemanTags(projectPath),
  };

  priceReceipt(receipt);
  return { receipt, malformed };
}

// Optional caveman metadata: presence of a `.caveman-active` marker in the
// project directory is recorded as a tag only. It never affects token totals.
function cavemanTags(projectPath) {
  if (projectPath && existsSync(join(projectPath, '.caveman-active'))) {
    return ['caveman:on'];
  }
  return [];
}

// Scan every Claude session log. Returns { receipts, malformed, scanned, root }.
export function scan({ root = claudeProjectsDir() } = {}) {
  const files = findSessionFiles(root);
  const receipts = [];
  let malformed = 0;
  for (const file of files) {
    const result = parseSessionFile(file);
    malformed += result.malformed;
    if (result.receipt) {
      receipts.push(result.receipt);
    }
  }
  return { receipts, malformed, scanned: files.length, root };
}

// The "current" session = the most recently modified log, optionally filtered by
// a project-path substring. Returns a receipt or null.
export function current({ root = claudeProjectsDir(), project } = {}) {
  const { receipts } = scan({ root });
  const candidates = project
    ? receipts.filter((r) => (r.project_path || '').toLowerCase().includes(String(project).toLowerCase()))
    : receipts;
  if (!candidates.length) {
    return null;
  }
  return candidates.sort((a, b) => (a.updated_at < b.updated_at ? 1 : -1))[0];
}
