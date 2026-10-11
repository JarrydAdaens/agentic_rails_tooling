"""Regression checks for immutable evidence, complete denominators, and safe migration."""
import copy
from hashlib import sha256
import importlib.util
from itertools import permutations
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "source/skills/rails-memory-rebuild/scripts/rebuild.py"
spec = importlib.util.spec_from_file_location("memory_rebuild", SCRIPT)
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)


def record(identity="obs-one", result="result-one", outcome="succeeded"):
    return {"schema_version": 1, "observation_id": identity, "result_id": result,
            "project": "fixture", "date": "2026-10-11", "task": "bug fix", "outcome": outcome,
            "participants": [{"role": "worker", "persona": "web-persona", "requested_model": "model-a",
                              "observed_model": "model-b", "identity_source": "fixture runtime receipt"}],
            "evidence": [{"kind": "verified", "source": "fixture receipt"}],
            "telemetry": {"availability": "unavailable", "coverage": "unknown", "source": "unknown", "tokens": "unknown"},
            "interpretations": ["Reported advice with a specific limit"]}


class RebuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="memory-fixture-", dir=Path(__file__).resolve().parent)
        self.root = Path(self.temp.name)
        for location in ("new", "archived", "golden"):
            (self.root / "memories/learnings" / location).mkdir(parents=True)

    def tearDown(self):
        assert self.root.resolve().is_relative_to(Path(__file__).resolve().parent)
        self.temp.cleanup()

    def add(self, item, location="new", name=None):
        path = self.root / "memories/learnings" / location / ((name or item["observation_id"]) + ".md")
        path.write_text(memory.observation_text(item), encoding="utf-8")
        return path

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_repeated_rebuild_preserves_bytes_counts_and_citations_after_move(self):
        source = self.add(record())
        failed = self.add(record("obs-failure", "result-failure", "failed"), "archived")
        original = (source.read_bytes(), failed.read_bytes())
        first = memory.rebuild(self.root)
        snapshot = self.snapshot()
        self.assertEqual(memory.rebuild(self.root), first)
        self.assertEqual(self.snapshot(), snapshot)
        shutil.move(source, self.root / "memories/learnings/golden/moved.md")
        moved = memory.rebuild(self.root)
        self.assertEqual(moved["results"], 2)
        self.assertEqual(moved["outcomes"], {"succeeded": 1, "failed": 1})
        self.assertEqual(failed.read_bytes(), original[1])
        self.assertEqual((self.root / "memories/learnings/golden/moved.md").read_bytes(), original[0])
        for resume in (self.root / "memories/resumes-rebuilt").rglob("*.md"):
            import re
            for target in re.findall(r"\]\(([^)]+)\)", resume.read_text()):
                self.assertTrue((resume.parent / target).resolve().is_file())
        self.assertEqual((self.root / "memories/observations/obs-one.md").read_bytes(), snapshot["memories/observations/obs-one.md"])

    def test_shared_results_deduplicated_across_agents_and_copies(self):
        first = record()
        first["participants"] *= 3
        first["telemetry"] = {"availability": "available", "coverage": "result", "source": "receipt", "tokens": 100}
        self.add(first)
        self.add(first, "golden", "duplicate")
        second = copy.deepcopy(first)
        second["observation_id"] = "obs-two"
        second["participants"][0]["persona"] = "review-persona"
        self.add(second)
        result = memory.rebuild(self.root)
        self.assertEqual(result["records"], 2)
        self.assertEqual(result["results"], 1)
        summary = (self.root / "memories/resumes-rebuilt/summary.md").read_text()
        self.assertIn("token sum: 100; coverage 1/1", summary)

    def test_immutable_identity_conflict_refuses_before_writes(self):
        source = self.add(record())
        memory.rebuild(self.root)
        item = record()
        item["outcome"] = "failed"
        source.write_text(memory.observation_text(item))
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "immutable observation changed"):
            memory.rebuild(self.root)
        self.assertEqual(before, self.snapshot())

    def test_shared_outcome_conflict_has_no_partial_writes(self):
        self.add(record())
        self.add(record("obs-two", outcome="failed"))
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "conflicting shared result"):
            memory.rebuild(self.root)
        self.assertEqual(before, self.snapshot())

    def test_requested_identity_does_not_override_runtime_identity(self):
        self.add(record())
        memory.rebuild(self.root)
        models = list((self.root / "memories/resumes-rebuilt/models").glob("*.md"))
        self.assertEqual(len(models), 1)
        self.assertTrue(models[0].name.startswith("model-b-"))

    def test_legacy_import_preserves_untracked_work_and_exact_crlf(self):
        legacy = self.root / "memories/learnings/archived/old_name.md"
        data = ("---\r\ntype: session-learning\r\nproject: fixture\r\ndate: 2026-01-01\r\n"
                "session_id: old\r\nsession_scope: one-task\r\noutcome: failed\r\nmodels_used:\r\n"
                "  - name: reported-model\r\n    role: worker\r\ntoken_cost: 12345\r\n---\r\nHistorical failure.\r\n").encode()
        legacy.write_bytes(data)
        old_resume = self.root / "memories/model-resumes/reported-model.md"
        old_resume.parent.mkdir(parents=True)
        old_resume.write_bytes(b"untracked user work\r\n")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "unmigrated"):
            memory.rebuild(self.root)
        memory.rebuild(self.root, migrate=True)
        for name, content in before.items():
            self.assertEqual((self.root / name).read_bytes(), content)
        immutable = self.root / "memories/observations" / ("legacy-" + sha256(data).hexdigest() + ".md")
        item = memory.read_record(immutable)
        self.assertEqual(item["participants"][0]["observed_model"], "unknown")
        self.assertEqual(item["participants"][0]["reported_model"], "reported-model")
        self.assertEqual(item["telemetry"]["tokens"], "unknown")
        import base64
        self.assertIn(base64.b64encode(data).decode(), immutable.read_text())
        frozen = self.snapshot()
        memory.rebuild(self.root, migrate=True)
        self.assertEqual(frozen, self.snapshot())
        self.assertEqual(memory.rebuild(self.root)["results"], 1)
        self.assertEqual(frozen, self.snapshot())
        shutil.move(legacy, self.root / "memories/learnings/golden/curated.md")
        self.assertEqual(memory.rebuild(self.root, migrate=True)["results"], 1)

    def test_unmanaged_output_and_dry_run_are_protected(self):
        self.add(record())
        before = self.snapshot()
        memory.rebuild(self.root, dry_run=True)
        self.assertEqual(before, self.snapshot())
        target = self.root / "memories/resumes-rebuilt/summary.md"
        target.parent.mkdir(parents=True)
        target.write_text("user-authored summary")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "unmanaged output"):
            memory.rebuild(self.root)
        self.assertEqual(before, self.snapshot())

    def test_partial_telemetry_cannot_be_promoted_to_measured_total(self):
        item = record()
        item["telemetry"] = {"availability": "partial", "coverage": "child-only", "source": "receipt", "tokens": 100}
        with self.assertRaisesRegex(ValueError, "result-level"):
            memory.validate(item)

    def test_conflicting_shared_usage_refuses_without_writes(self):
        first = record()
        first["telemetry"] = {"availability": "available", "coverage": "result", "source": "receipt", "tokens": 100}
        second = copy.deepcopy(first)
        second["observation_id"] = "obs-two"
        second["telemetry"]["tokens"] = 200
        self.add(first)
        self.add(second)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "conflicting shared-result telemetry"):
            memory.rebuild(self.root)
        self.assertEqual(before, self.snapshot())

    def test_unknown_between_conflicting_measurements_refuses_all_orderings(self):
        for values in permutations((100, "unknown", 200)):
            with self.subTest(values=values):
                for index, value in enumerate(values):
                    item = record(f"obs-{index}")
                    if value != "unknown":
                        item["telemetry"] = {"availability": "available", "coverage": "result",
                                             "source": "receipts/task-result.json", "tokens": value}
                    self.add(item)
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, "conflicting shared-result telemetry"):
                    memory.rebuild(self.root)
                self.assertEqual(before, self.snapshot())
                self.assertFalse((self.root / "memories/observations").exists())
                self.assertFalse((self.root / "memories/resumes-rebuilt").exists())

    def test_unknown_between_matching_measurements_keeps_one_total(self):
        for index, value in enumerate((100, "unknown", 100)):
            item = record(f"obs-{index}")
            if value != "unknown":
                item["telemetry"] = {"availability": "available", "coverage": "result",
                                     "source": "receipts/task-result.json", "tokens": value}
            self.add(item)
        result = memory.rebuild(self.root)
        self.assertEqual(result["results"], 1)
        summary = (self.root / "memories/resumes-rebuilt/summary.md").read_text()
        self.assertIn("token sum: 100; coverage 1/1", summary)

    def test_numeric_total_requires_available_telemetry(self):
        for availability in ("partial", "unavailable", "unknown"):
            with self.subTest(availability=availability):
                item = record()
                item["telemetry"] = {"availability": availability, "coverage": "result",
                                     "source": "receipts/task-result.json", "tokens": 100}
                self.add(item)
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, "available result-level measured evidence"):
                    memory.rebuild(self.root)
                self.assertEqual(before, self.snapshot())

    def test_numeric_total_requires_valid_measured_source(self):
        for source in (None, 100, False, [], {}, "", " \t\n", "unknown", " Unknown ",
                       "unavailable", "none", "null", "unmeasured", "estimated", "guess"):
            with self.subTest(source=source):
                item = record()
                item["telemetry"] = {"availability": "available", "coverage": "result",
                                     "source": source, "tokens": 100}
                self.add(item)
                before = self.snapshot()
                with self.assertRaisesRegex(ValueError, "valid source"):
                    memory.rebuild(self.root)
                self.assertEqual(before, self.snapshot())

    def test_unsupported_and_malformed_observation_diagnostics(self):
        for invalid in (None, [], {"schema_version": True}, {"schema_version": 2}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                memory.validate(invalid)
        item = record()
        item["telemetry"] = []
        with self.assertRaisesRegex(ValueError, "telemetry must be an object"):
            memory.validate(item)

    def test_golden_selection_changes_advice_without_changing_denominator(self):
        self.add(record(), "golden")
        self.add(record("obs-failure", "result-failure", "failed"), "archived")
        result = memory.rebuild(self.root)
        self.assertEqual(result["results"], 2)
        models = list((self.root / "memories/resumes-rebuilt/models").glob("*.md"))
        text = models[0].read_text()
        self.assertIn('| failed | 1 |', text)
        self.assertEqual(text.count('Reported advice with a specific limit'), 1)

    def test_corpus_edit_between_preview_and_write_cannot_publish_stale_summary(self):
        source = self.add(record())
        original = memory.materialize
        calls = 0

        def interleaved(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                item = record()
                item["outcome"] = "failed"
                source.write_text(memory.observation_text(item))
            return original(*args, **kwargs)

        with patch.object(memory, "materialize", side_effect=interleaved):
            with self.assertRaisesRegex(ValueError, "corpus changed"):
                memory.rebuild(self.root)
        self.assertFalse((self.root / "memories/observations").exists())
        self.assertFalse((self.root / "memories/resumes-rebuilt").exists())


if __name__ == "__main__":
    unittest.main()
