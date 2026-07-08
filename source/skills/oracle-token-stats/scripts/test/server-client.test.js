// Oracle Server client: URL config, health probing, and window usage fetches.
// All HTTP is stubbed via the injectable fetchImpl — no live server needed.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  serverBaseUrl, probeHealth, fetchWindowUsage, DEFAULT_SERVER_URL,
} from '../lib/server-client.js';

// Minimal fetch-Response stand-in: just the surface fetchJson touches.
function jsonResponse(body, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  };
}

test('serverBaseUrl defaults to localhost:5140 and honors ORACLE_SERVER_URL', () => {
  assert.equal(serverBaseUrl({}), DEFAULT_SERVER_URL);
  assert.equal(serverBaseUrl({ ORACLE_SERVER_URL: 'http://oracle-box:9999' }), 'http://oracle-box:9999');
  assert.equal(serverBaseUrl({ ORACLE_SERVER_URL: '  ' }), DEFAULT_SERVER_URL, 'blank falls back');
});

test('serverBaseUrl trims trailing slashes so path joins stay clean', () => {
  assert.equal(serverBaseUrl({ ORACLE_SERVER_URL: 'http://oracle-box:9999/' }), 'http://oracle-box:9999');
});

test('probeHealth reports reachable with the server health status', async () => {
  const fetchImpl = async (url) => {
    assert.equal(url, 'http://stub/health');
    return jsonResponse({ status: 'healthy', databaseReachable: true });
  };
  const probe = await probeHealth({ baseUrl: 'http://stub', fetchImpl });
  assert.deepEqual(probe, { reachable: true, status: 'healthy' });
});

test('probeHealth reports unreachable when the connection fails, never throws', async () => {
  const fetchImpl = async () => {
    throw new Error('connect ECONNREFUSED 127.0.0.1:5140');
  };
  const probe = await probeHealth({ baseUrl: 'http://stub', fetchImpl });
  assert.equal(probe.reachable, false);
  assert.match(probe.reason, /ECONNREFUSED/);
});

test('probeHealth aborts a hung server within the timeout', async () => {
  // A fetch that only settles when its abort signal fires — a hung socket.
  const fetchImpl = (url, { signal }) => new Promise((resolve, reject) => {
    signal.addEventListener('abort', () => reject(new Error('This operation was aborted')));
  });
  const probe = await probeHealth({ baseUrl: 'http://stub', fetchImpl, timeoutMs: 20 });
  assert.equal(probe.reachable, false);
});

test('fetchWindowUsage returns the parsed contract response for a 200', async () => {
  const body = {
    window: 'today',
    fromUtc: '2026-07-08T00:00:00Z',
    toUtc: '2026-07-09T00:00:00Z',
    rows: [{
      machine: 'dev-jarryd', source: 'ccusage:claude', model: 'claude-fable-5',
      recordCount: 3, inputTokens: 10, outputTokens: 20, totalTokens: 500, costUsd: 1.25,
    }],
    totals: { inputTokens: 10, outputTokens: 20, totalTokens: 500, costUsd: 1.25 },
  };
  const fetchImpl = async (url) => {
    assert.equal(url, 'http://stub/v1/usage/window?window=today');
    return jsonResponse(body);
  };
  const usage = await fetchWindowUsage('today', { baseUrl: 'http://stub', fetchImpl });
  assert.deepEqual(usage, body);
});

test('fetchWindowUsage throws on a non-2xx status', async () => {
  const fetchImpl = async () => jsonResponse({ title: 'boom' }, 500);
  await assert.rejects(
    fetchWindowUsage('week', { baseUrl: 'http://stub', fetchImpl }),
    /HTTP 500/,
  );
});

test('fetchWindowUsage rejects windows outside the contract', async () => {
  await assert.rejects(fetchWindowUsage('month', { baseUrl: 'http://stub' }), /Unsupported window/);
});
