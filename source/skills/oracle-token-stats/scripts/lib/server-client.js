// Oracle Server HTTP client — the "live" side of the live-awareness skill.
//
// Talks to the Oracle Server usage API (M3-S1 contract, /v1) using Node 18+'s
// global fetch, so the skill stays zero-dependency. The base URL comes from
// ORACLE_SERVER_URL (default http://localhost:5140), matching the skill's
// env-var-only config convention (see lib/paths.js).
//
// Every function accepts an injectable `fetchImpl` so tests stub HTTP without
// a mocking library, and short timeouts so an absent server fails fast into
// the local-ledger fallback instead of hanging the CLI.

export const DEFAULT_SERVER_URL = 'http://localhost:5140';

// Health probes answer "is anyone there?" — keep them snappy.
export const HEALTH_TIMEOUT_MS = 1500;
// Usage queries hit a real database; allow a little longer.
export const REQUEST_TIMEOUT_MS = 5000;

// Resolve the Oracle Server base URL: ORACLE_SERVER_URL, else the localhost default.
// Trailing slashes are trimmed so path joins below stay predictable.
export function serverBaseUrl(env = process.env) {
  const raw = (env.ORACLE_SERVER_URL || '').trim();
  const url = raw || DEFAULT_SERVER_URL;
  return url.replace(/\/+$/, '');
}

// GET a JSON body with a hard timeout. Throws on network failure, timeout, or
// a non-2xx status — callers decide whether that means "fall back" or "report".
async function fetchJson(url, timeoutMs, fetchImpl) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetchImpl(url, { signal: controller.signal });
    if (!response.ok) {
      throw new Error(`GET ${url} returned HTTP ${response.status}`);
    }
    return await response.json();
  } finally {
    clearTimeout(timer);
  }
}

// Probe GET /health. Never throws: returns { reachable, status? , reason? } so
// the caller has one honest signal to branch on for the offline fallback.
export async function probeHealth({
  baseUrl = serverBaseUrl(),
  fetchImpl = fetch,
  timeoutMs = HEALTH_TIMEOUT_MS,
} = {}) {
  try {
    const body = await fetchJson(`${baseUrl}/health`, timeoutMs, fetchImpl);
    return { reachable: true, status: body.status || 'unknown' };
  } catch (error) {
    return { reachable: false, reason: error.message || String(error) };
  }
}

// GET /v1/usage/window?window=today|week. Returns the parsed contract response
// ({ window, fromUtc, toUtc, rows, totals }); throws on any failure.
export async function fetchWindowUsage(window, {
  baseUrl = serverBaseUrl(),
  fetchImpl = fetch,
  timeoutMs = REQUEST_TIMEOUT_MS,
} = {}) {
  if (window !== 'today' && window !== 'week') {
    throw new Error(`Unsupported window "${window}". Use "today" or "week".`);
  }
  return fetchJson(`${baseUrl}/v1/usage/window?window=${window}`, timeoutMs, fetchImpl);
}
