"""Focused tests for generate_stats.py -- sidecar schema v2 and artifact cost stamping.

Fixtures are temp files on disk; tiktoken runs for real (already a skill dependency).
Run from this directory: uv run --with tiktoken python -m unittest test_generate_stats -v
"""

import json
import tempfile
import unittest
from pathlib import Path

import tiktoken

import generate_stats


def read_sidecar(artifact_path: Path) -> dict:
    return json.loads(Path(str(artifact_path) + ".stats").read_text(encoding="utf-8"))


class SidecarSchemaV2Tests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.artifact = Path(self._tmp.name) / "plan.md"
        self.artifact.write_text("# Plan\n\nSome content.\n", encoding="utf-8")
        self.enc = tiktoken.get_encoding("cl100k_base")

    def tearDown(self):
        self._tmp.cleanup()

    def test_sidecar_carries_v2_fields(self):
        generate_stats.process_file(self.artifact, self.enc)
        sidecar = read_sidecar(self.artifact)
        self.assertEqual(sidecar["schema_version"], generate_stats.SIDECAR_SCHEMA_VERSION)
        self.assertEqual(sidecar["precision"], "estimated")
        self.assertEqual(sidecar["tokenizer"], "tiktoken cl100k_base")

    def test_v1_fields_are_preserved(self):
        generate_stats.process_file(self.artifact, self.enc)
        sidecar = read_sidecar(self.artifact)
        for field in ("file", "updated", "size_bytes", "lines", "chars", "tokens"):
            self.assertIn(field, sidecar)
        self.assertEqual(sidecar["file"], "plan.md")

    def test_v1_sidecar_is_upgraded_on_regeneration(self):
        # A pre-versioning sidecar: no schema_version, no precision. Regeneration
        # must overwrite it to v2 without reading it -- never crash on the old shape.
        v1_sidecar = Path(str(self.artifact) + ".stats")
        v1_sidecar.write_text(
            json.dumps(
                {
                    "file": "plan.md",
                    "updated": "2026-06-18T10:30:00Z",
                    "size_bytes": 1,
                    "lines": 1,
                    "chars": 1,
                    "tokens": 1,
                    "tokenizer": "tiktoken cl100k_base",
                }
            ),
            encoding="utf-8",
        )
        generate_stats.process_file(self.artifact, self.enc)
        sidecar = read_sidecar(self.artifact)
        self.assertEqual(sidecar["schema_version"], 2)
        self.assertEqual(sidecar["precision"], "estimated")
        self.assertGreater(sidecar["tokens"], 1)


class ApplyStampTests(unittest.TestCase):
    def setUp(self):
        self.block = generate_stats.build_stamp_block(
            1234, "provider-reported", "reported", None, "2026-07-09T00:00:00Z"
        )

    def test_fresh_stamp_is_appended_as_final_entry(self):
        result = generate_stats.apply_stamp("# Doc\n\nBody.\n", self.block)
        self.assertTrue(result.endswith(self.block))
        self.assertEqual(result.count(generate_stats.STAMP_START), 1)

    def test_stamp_appends_cleanly_without_trailing_newline(self):
        result = generate_stats.apply_stamp("# Doc without newline", self.block)
        self.assertIn("# Doc without newline\n\n" + generate_stats.STAMP_START, result)

    def test_restamp_replaces_existing_stamp(self):
        once = generate_stats.apply_stamp("# Doc\n", self.block)
        new_block = generate_stats.build_stamp_block(
            9999, "tiktoken:cl100k_base", "estimated", "claude-fable-5", "2026-07-09T01:00:00Z"
        )
        twice = generate_stats.apply_stamp(once, new_block)
        self.assertEqual(twice.count(generate_stats.STAMP_START), 1)
        self.assertIn("9,999 tokens", twice)
        self.assertNotIn("1,234 tokens", twice)

    def test_restamp_removes_a_stamp_stranded_mid_document(self):
        stranded = "# Doc\n\n" + self.block + "\nTrailing section added after stamping.\n"
        result = generate_stats.apply_stamp(stranded, self.block)
        self.assertEqual(result.count(generate_stats.STAMP_START), 1)
        self.assertTrue(result.endswith(self.block))


class StampArtifactTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.artifact = Path(self._tmp.name) / "report.md"
        self.artifact.write_text("# Report\n\nFindings.\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_stamp_carries_tokens_tokenizer_and_precision(self):
        generate_stats.stamp_artifact(self.artifact, 4521, "provider-reported", "reported", "claude-fable-5")
        text = self.artifact.read_text(encoding="utf-8")
        self.assertIn("**Production cost:** 4,521 tokens", text)
        self.assertIn("provider-reported (reported)", text)
        self.assertIn("model claude-fable-5", text)
        self.assertTrue(text.rstrip("\n").endswith(generate_stats.STAMP_END))

    def test_stamping_refreshes_the_sidecar_to_v2(self):
        generate_stats.stamp_artifact(self.artifact, 4521, "provider-reported", "reported", None)
        sidecar = read_sidecar(self.artifact)
        self.assertEqual(sidecar["schema_version"], 2)
        # Sidecar counts must reflect the stamped content, not the pre-stamp file.
        self.assertEqual(sidecar["chars"], len(self.artifact.read_text(encoding="utf-8")))


class ParseStampArgsTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.artifact = Path(self._tmp.name) / "plan.md"
        self.artifact.write_text("# Plan\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_defaults_applied(self):
        parsed = generate_stats.parse_stamp_args(["--stamp-cost", "100", str(self.artifact)])
        path, tokens, tokenizer, precision, model = parsed
        self.assertEqual(tokens, 100)
        self.assertEqual(tokenizer, generate_stats.DEFAULT_STAMP_TOKENIZER)
        self.assertEqual(precision, "reported")
        self.assertIsNone(model)

    def test_invalid_precision_is_rejected(self):
        result = generate_stats.parse_stamp_args(
            ["--stamp-cost", "100", "--precision", "exact", str(self.artifact)]
        )
        self.assertIsInstance(result, str)
        self.assertIn("--precision", result)

    def test_non_markdown_target_is_rejected(self):
        other = Path(self._tmp.name) / "data.json"
        other.write_text("{}", encoding="utf-8")
        result = generate_stats.parse_stamp_args(["--stamp-cost", "100", str(other)])
        self.assertIsInstance(result, str)
        self.assertIn("markdown", result)

    def test_non_integer_cost_is_rejected(self):
        result = generate_stats.parse_stamp_args(["--stamp-cost", "lots", str(self.artifact)])
        self.assertIsInstance(result, str)
        self.assertIn("integer", result)


if __name__ == "__main__":
    unittest.main()
