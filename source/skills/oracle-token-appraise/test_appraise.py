"""Focused tests for appraise.py -- server mode, local fallback, and output labeling.

All HTTP is stubbed via the `opener` injection point (appraise_file/probe_health/
request_estimate all accept one); no live Oracle Server is needed or contacted.
"""

import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path

import appraise


class FakeResponse:
    """Minimal urlopen()-response stand-in: status + a JSON-encoded body, as a context manager."""

    def __init__(self, body, status=200):
        self._body = json.dumps(body).encode("utf-8")
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def read(self):
        return self._body


def make_opener(estimate_body, health_status=200):
    """Build an opener that answers /health with health_status and /v1/estimate with estimate_body.

    Mirrors the real call pattern: probe_health calls opener(url, timeout=...); request_estimate
    calls opener(request_object, timeout=...) where request_object has a full_url attribute.
    """

    def opener(target, timeout=None):
        url = target if isinstance(target, str) else target.full_url
        if url.endswith("/health"):
            return FakeResponse({"status": "healthy"}, status=health_status)
        if url.endswith("/v1/estimate"):
            return FakeResponse(estimate_body)
        raise AssertionError(f"unexpected URL: {url}")

    return opener


def make_unreachable_opener():
    """An opener whose every call raises, simulating a server that refuses connections."""

    def opener(target, timeout=None):
        raise urllib.error.URLError("connection refused")

    return opener


class ServerBaseUrlTests(unittest.TestCase):
    def test_defaults_to_localhost_5140(self):
        self.assertEqual(appraise.server_base_url(env={}), appraise.DEFAULT_SERVER_URL)

    def test_honors_oracle_server_url_env_var(self):
        env = {"ORACLE_SERVER_URL": "http://oracle-box:9999"}
        self.assertEqual(appraise.server_base_url(env=env), "http://oracle-box:9999")

    def test_trims_trailing_slash(self):
        env = {"ORACLE_SERVER_URL": "http://oracle-box:9999/"}
        self.assertEqual(appraise.server_base_url(env=env), "http://oracle-box:9999")

    def test_blank_env_var_falls_back_to_default(self):
        env = {"ORACLE_SERVER_URL": "   "}
        self.assertEqual(appraise.server_base_url(env=env), appraise.DEFAULT_SERVER_URL)


class ClassifyVerdictTests(unittest.TestCase):
    def test_boundaries_match_server_banding(self):
        self.assertEqual(appraise.classify_verdict(0), "SMALL")
        self.assertEqual(appraise.classify_verdict(9.9), "SMALL")
        self.assertEqual(appraise.classify_verdict(10), "MEDIUM")
        self.assertEqual(appraise.classify_verdict(39.9), "MEDIUM")
        self.assertEqual(appraise.classify_verdict(40), "LARGE")
        self.assertEqual(appraise.classify_verdict(79.9), "LARGE")
        self.assertEqual(appraise.classify_verdict(80), "HUGE")


class AppraiseFileServerModeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.file_path = Path(self._tmp.name) / "sample.md"
        self.file_path.write_text("hello world\n" * 20, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_uses_server_estimate_when_reachable(self):
        estimate_body = {
            "targetModel": "claude",
            "tokenizer": {"id": "tiktoken:cl100k_base", "tokenizerMatch": "proxy", "note": "stand-in"},
            "precision": "estimated",
            "items": [{"kind": "path", "ref": str(self.file_path), "tokens": 55, "bytes": 240}],
            "totalTokens": 55,
            "window": {"tokens": 40000, "source": "caller"},
            "usagePercent": 0.1,
            "verdict": "SMALL",
        }
        opener = make_opener(estimate_body)

        report = appraise.appraise_file(str(self.file_path), opener=opener, env={})

        self.assertEqual(report["source"], "Oracle Server (targetModel=claude)")
        self.assertEqual(report["tokenizer_label"], "tiktoken:cl100k_base (proxy)")
        self.assertEqual(report["token_count"], 55)
        self.assertEqual(report["verdict"], appraise.VERDICT_DESCRIPTIONS["SMALL"])

    def test_names_heuristic_tokenizer_honestly_when_registry_is_empty(self):
        # An unconfigured server-side model registry degrades every model to the
        # characters-per-token heuristic (EstimationModelRegistry.Resolve) -- the skill must
        # surface that honestly rather than implying cl100k_base accuracy it didn't get.
        estimate_body = {
            "targetModel": "claude",
            "tokenizer": {
                "id": "heuristic:chars-per-token-4",
                "tokenizerMatch": "heuristic",
                "note": "No tokenizer registered for this model; characters-per-token heuristic (4 chars/token) applied.",
            },
            "precision": "estimated",
            "items": [{"kind": "path", "ref": str(self.file_path), "tokens": 60, "bytes": 240}],
            "totalTokens": 60,
            "window": {"tokens": 40000, "source": "caller"},
            "usagePercent": 0.2,
            "verdict": "SMALL",
        }
        opener = make_opener(estimate_body)

        report = appraise.appraise_file(str(self.file_path), opener=opener, env={})

        self.assertEqual(report["tokenizer_label"], "heuristic:chars-per-token-4 (heuristic)")

    def test_sends_callers_window_so_verdict_always_resolves(self):
        captured = {}

        def opener(target, timeout=None):
            url = target if isinstance(target, str) else target.full_url
            if url.endswith("/health"):
                return FakeResponse({"status": "healthy"})
            captured["body"] = json.loads(target.data.decode("utf-8"))
            return FakeResponse(
                {
                    "targetModel": "claude",
                    "tokenizer": {"id": "tiktoken:cl100k_base", "tokenizerMatch": "proxy", "note": ""},
                    "precision": "estimated",
                    "items": [],
                    "totalTokens": 10,
                    "window": {"tokens": 8000, "source": "caller"},
                    "usagePercent": 0.1,
                    "verdict": "SMALL",
                }
            )

        appraise.appraise_file(str(self.file_path), window=8000, opener=opener, env={})

        self.assertEqual(captured["body"]["window"], 8000)
        self.assertEqual(captured["body"]["targetModel"], "claude")


class AppraiseFileFallbackTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.file_path = Path(self._tmp.name) / "sample.md"
        self.file_path.write_text("hello world\n" * 20, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_falls_back_to_local_tiktoken_when_server_unreachable(self):
        report = appraise.appraise_file(str(self.file_path), opener=make_unreachable_opener(), env={})

        self.assertEqual(report["source"], "local tiktoken (server unreachable)")
        self.assertEqual(report["tokenizer_label"], "tiktoken:cl100k_base")
        self.assertGreater(report["token_count"], 0)

    def test_falls_back_to_local_tiktoken_on_server_side_path_error(self):
        # Health is up but the estimate call itself fails (e.g. the server 400s the path --
        # too large, or a path it cannot see under the same-machine assumption).
        def opener(target, timeout=None):
            url = target if isinstance(target, str) else target.full_url
            if url.endswith("/health"):
                return FakeResponse({"status": "healthy"})
            error = urllib.error.HTTPError(url, 400, "Bad Request", {}, io.BytesIO(b""))
            error.close()
            raise error

        report = appraise.appraise_file(str(self.file_path), opener=opener, env={})

        self.assertTrue(report["source"].startswith("local tiktoken ("))
        self.assertEqual(report["tokenizer_label"], "tiktoken:cl100k_base")

    def test_falls_back_when_file_over_size_cap_would_400_whole_request(self):
        # Mirrors the server's 10 MB per-path cap (EstimateEndpoint.MaxPathFileSizeBytes):
        # a whole-request 400 must fall back cleanly, not crash the script.
        def opener(target, timeout=None):
            url = target if isinstance(target, str) else target.full_url
            if url.endswith("/health"):
                return FakeResponse({"status": "healthy"})
            error = urllib.error.HTTPError(url, 400, "over the byte estimation cap", {}, io.BytesIO(b""))
            error.close()
            raise error

        report = appraise.appraise_file(str(self.file_path), opener=opener, env={})

        self.assertTrue(report["source"].startswith("local tiktoken ("))

    def test_falls_back_when_200_response_is_missing_expected_fields(self):
        # A 200 whose body doesn't match the contract (missing totalTokens/tokenizer/verdict,
        # or an unknown verdict token) must fall back, never crash with a KeyError.
        malformed_bodies = [
            {"unexpected": "shape"},
            {"totalTokens": 10, "tokenizer": {"id": "x"}},  # no tokenizerMatch, no verdict
            {
                "totalTokens": 10,
                "tokenizer": {"id": "x", "tokenizerMatch": "proxy"},
                "usagePercent": 1.0,
                "verdict": "GIGANTIC",  # not a known verdict token
            },
        ]
        for body in malformed_bodies:
            with self.subTest(body=body):
                report = appraise.appraise_file(str(self.file_path), opener=make_opener(body), env={})

                self.assertTrue(report["source"].startswith("local tiktoken ("))
                self.assertEqual(report["tokenizer_label"], "tiktoken:cl100k_base")

    def test_fallback_verdict_and_percentage_computed_locally(self):
        report = appraise.appraise_file(
            str(self.file_path), window=1, opener=make_unreachable_opener(), env={}
        )

        self.assertEqual(report["verdict"], appraise.VERDICT_DESCRIPTIONS["HUGE"])


class FormatReportTests(unittest.TestCase):
    def test_report_never_contains_file_content(self):
        report = {
            "file_path": "design.md",
            "file_size": 100,
            "line_count": 5,
            "char_count": 95,
            "source": "local tiktoken (server unreachable)",
            "tokenizer_label": "tiktoken:cl100k_base",
            "token_count": 30,
            "window": 40000,
            "usage_percent": 0.1,
            "verdict": appraise.VERDICT_DESCRIPTIONS["SMALL"],
        }
        rendered = appraise.format_report(report)

        for field in ("file_path", "source", "tokenizer_label", "token_count", "verdict"):
            self.assertIn(str(report[field]), rendered)


if __name__ == "__main__":
    unittest.main()
