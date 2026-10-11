"""Behavior tests for preview, exact provenance, rephasing, and recovery."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("phase_files", Path(__file__).with_name("phase-files.py"))
phase_files = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase_files)


class PhaseFilesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="phase-test-", dir=Path(__file__).parent)
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.target = root / "story"
        self.target.mkdir()
        self.plan = self.target / "plan.md"
        self.original = b"# Dirty original\r\n\r\nUncommitted decision: \xe2\x9c\x93\r\n"
        self.plan.write_bytes(self.original)
        self.drafts = root / "drafts"
        self.drafts.mkdir()
        (self.drafts / "plan.md").write_bytes(b"# Manifest\n## Phase registry\n")
        (self.drafts / "phase-1.md").write_bytes(b"# First independently usable increment\n")
        (self.drafts / "phase-2.md").write_bytes(b"# Second increment\n")

    def expected(self):
        return phase_files.inspect(self.plan)["fingerprint"]

    def snapshot(self):
        return {str(p.relative_to(self.target)): p.read_bytes()
                for p in self.target.rglob("*") if p.is_file()}

    def apply(self, **options):
        return phase_files.apply(self.plan, self.drafts, self.expected(), **options)

    def interrupt(self):
        def stop(_name):
            raise RuntimeError("simulated interruption after first replacement")
        with self.assertRaisesRegex(RuntimeError, "simulated interruption"):
            self.apply(after_write=stop)

    def test_preview_has_no_target_mutations(self):
        before = self.snapshot()
        result = phase_files.preview(self.plan, self.drafts)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(len(result["changes"]), 3)
        self.assertFalse((self.target / phase_files.HISTORY).exists())

    def test_apply_preserves_exact_dirty_bytes_without_git(self):
        unrelated = self.target / "user-notes.md"
        unrelated.write_bytes(b"User-owned content\r\n")
        result = self.apply()
        self.assertEqual(Path(result["original"]).read_bytes(), self.original)
        self.assertEqual(unrelated.read_bytes(), b"User-owned content\r\n")
        self.assertEqual(phase_files.inspect(self.plan)["status"], "COMMITTED")
        self.assertEqual(self.plan.read_bytes(), (self.drafts / "plan.md").read_bytes())

    def test_rephase_authorization_overrides_default_refusal(self):
        self.apply()
        previous = self.snapshot()
        with self.assertRaisesRegex(phase_files.PhaseError, "requires --rephase"):
            self.apply()
        self.assertEqual(previous, self.snapshot())
        (self.drafts / "phase-2.md").unlink()
        before_rephase = self.plan.read_bytes()
        result = self.apply(rephase=True)
        self.assertFalse((self.target / "phase-2.md").exists())
        self.assertEqual(Path(result["original"]).read_bytes(), before_rephase)
        self.assertEqual(len(list((self.target / phase_files.HISTORY).iterdir())), 2)

    def test_preview_of_phased_plan_does_not_require_replacement_permission(self):
        self.apply()
        before = self.snapshot()
        self.assertTrue(phase_files.preview(self.plan, self.drafts)["replacement_requires_rephase"])
        self.assertEqual(before, self.snapshot())

    def test_stale_source_fingerprint_preserves_concurrent_edits(self):
        expected = self.expected()
        self.plan.write_bytes(b"Independent newer edit\r\n")
        before = self.snapshot()
        with self.assertRaisesRegex(phase_files.PhaseError, "Source changed"):
            phase_files.apply(self.plan, self.drafts, expected)
        self.assertEqual(before, self.snapshot())

    def test_existing_scorecard_is_preserved_and_explicit_card_is_retained(self):
        card = self.target / phase_files.CARD
        card.write_bytes(b"Previously requested scorecard\r\n")
        self.apply()
        self.assertEqual(card.read_bytes(), b"Previously requested scorecard\r\n")
        (self.drafts / phase_files.CARD).write_bytes(b"New explicitly requested scorecard\n")
        result = self.apply(rephase=True, scorecard=True)
        self.assertEqual(card.read_bytes(), b"New explicitly requested scorecard\n")
        self.assertEqual((Path(result["history"]) / "original" / phase_files.CARD).read_bytes(),
                         b"Previously requested scorecard\r\n")

    def test_unknown_scorecard_draft_requires_explicit_request(self):
        (self.drafts / phase_files.CARD).write_text("Unexpected grading artifact")
        before = self.snapshot()
        with self.assertRaisesRegex(phase_files.PhaseError, "Unexpected draft artifact"):
            self.apply()
        self.assertEqual(before, self.snapshot())

    def test_interrupted_replacement_restores_exact_original_and_removes_new_outputs(self):
        self.interrupt()
        self.assertTrue(phase_files.inspect(self.plan)["pending_recovery"])
        before_preview = self.snapshot()
        self.assertEqual(phase_files.recover(self.plan, dry_run=True)["status"], "RECOVERY_PREVIEW")
        self.assertEqual(before_preview, self.snapshot())
        self.assertEqual(phase_files.recover(self.plan)["status"], "ROLLED_BACK")
        self.assertEqual(self.plan.read_bytes(), self.original)
        self.assertFalse((self.target / "phase-1.md").exists())

    def test_pending_recovery_blocks_another_apply(self):
        self.interrupt()
        before = self.snapshot()
        with self.assertRaisesRegex(phase_files.PhaseError, "requires recovery"):
            self.apply(rephase=True)
        self.assertEqual(before, self.snapshot())

    def test_interrupted_rephase_restores_dirty_prior_phases_including_removed_files(self):
        self.apply()
        (self.target / "phase-1.md").write_bytes(b"Uncommitted phase revision\r\n")
        original_files = {name: (self.target / name).read_bytes()
                          for name in ("plan.md", "phase-1.md", "phase-2.md")}
        (self.drafts / "phase-2.md").unlink()
        def stop_after_removal(name):
            if name == "phase-2.md":
                raise RuntimeError("interrupted after old phase removal")
        with self.assertRaisesRegex(RuntimeError, "old phase removal"):
            self.apply(rephase=True, after_write=stop_after_removal)
        self.assertFalse((self.target / "phase-2.md").exists())
        phase_files.recover(self.plan)
        for name, original in original_files.items():
            self.assertEqual((self.target / name).read_bytes(), original)

    def test_recovery_itself_can_be_interrupted_and_repeated(self):
        self.interrupt()
        original_write = phase_files.atomic_write
        def write_then_interrupt(path, data):
            original_write(path, data)
            if path.parent == self.target:
                raise RuntimeError("recovery interrupted after restoring one file")
        with patch.object(phase_files, "atomic_write", side_effect=write_then_interrupt):
            with self.assertRaisesRegex(RuntimeError, "recovery interrupted"):
                phase_files.recover(self.plan)
        self.assertTrue(phase_files.inspect(self.plan)["pending_recovery"])
        phase_files.recover(self.plan)
        self.assertEqual(self.plan.read_bytes(), self.original)
        self.assertFalse((self.target / "phase-1.md").exists())

    def test_no_arbitrary_model_threshold_or_phase_count_ceiling(self):
        for number in range(3, 9):
            (self.drafts / f"phase-{number}.md").write_text(f"Usable checkpoint {number}\n")
        result = self.apply()
        self.assertEqual(len([name for name in result["files"] if name.startswith("phase-")]), 8)

    def test_recovery_refuses_new_user_edits_without_overwriting(self):
        self.interrupt()
        (self.target / "phase-1.md").write_bytes(b"User corrected interrupted output\n")
        before = self.snapshot()
        with self.assertRaisesRegex(phase_files.PhaseError, "Concurrent edits"):
            phase_files.recover(self.plan)
        self.assertEqual(before, self.snapshot())

    def test_recovery_verifies_backup_digest(self):
        self.interrupt()
        state = phase_files.inspect(self.plan)
        (Path(state["history"]) / "original" / self.plan.name).write_bytes(b"Damaged backup")
        before = self.plan.read_bytes()
        with self.assertRaisesRegex(phase_files.PhaseError, "digest mismatch"):
            phase_files.recover(self.plan)
        self.assertEqual(before, self.plan.read_bytes())

    def test_noncontiguous_phases_and_missing_manifest_are_diagnostics(self):
        (self.drafts / "phase-1.md").unlink()
        with self.assertRaisesRegex(phase_files.PhaseError, "contiguous"):
            self.apply()
        (self.drafts / "plan.md").unlink()
        with self.assertRaisesRegex(phase_files.PhaseError, "manifest"):
            self.apply()

    def test_single_unit_revision_preserves_ad_hoc_filename(self):
        self.plan.rename(self.target / "feature-plan.md")
        self.plan = self.target / "feature-plan.md"
        (self.drafts / "phase-1.md").unlink()
        (self.drafts / "phase-2.md").unlink()
        result = self.apply()
        self.assertEqual(result["files"], ["feature-plan.md"])
        self.assertTrue(self.plan.exists())
        self.assertFalse((self.target / "plan.md").exists())

    def test_cli_dry_run_wins_over_apply_rephase_and_scorecard(self):
        self.apply()
        (self.drafts / phase_files.CARD).write_text("Requested grading")
        before = self.snapshot()
        result = subprocess.run([sys.executable, str(Path(__file__).with_name("phase-files.py")),
            "apply", "--plan", str(self.plan), "--drafts", str(self.drafts),
            "--rephase", "--scorecard", "--dry-run"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_malformed_recovery_state_is_a_diagnostic(self):
        (self.target / phase_files.STATE).write_text('{"schema_version":1}')
        with self.assertRaisesRegex(phase_files.PhaseError, "Malformed recovery state"):
            phase_files.inspect(self.plan)


if __name__ == "__main__":
    unittest.main()
