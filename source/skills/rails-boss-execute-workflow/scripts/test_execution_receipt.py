"""Completion recovery tests use controlled races and real Git conversion."""
import hashlib
import importlib.util
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("execution_receipt", Path(__file__).with_name("execution-receipt.py"))
receipt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receipt)


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="receipt-test-", dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        (self.repo / "feature.txt").write_text("baseline\n")
        (self.repo / "story.md").write_text("in progress\n")
        self.commits = {}
        self.ancestry = []
        self.fixture_commit(["feature.txt", "story.md"])
        self.head = self.ancestry[0]
        self.staged = b"preexisting user index"
        self.addCleanup(patch.stopall)
        patch.object(receipt, "repository", return_value=self.repo).start()
        patch.object(receipt, "git", side_effect=self.git_evidence).start()
        (self.repo / "feature.txt").write_text("verified change\n")
        self.record = "receipt.json"

    def fixture_commit(self, paths):
        files = dict(self.commits[self.ancestry[0]]) if self.ancestry else {}
        for name in paths:
            file = self.repo / name
            if file.exists():
                files[name] = file.read_bytes()
            else:
                files.pop(name, None)
        commit = f"{len(self.commits) + 1:040x}"
        self.commits[commit] = files
        self.ancestry.insert(0, commit)
        return commit

    def git_evidence(self, repo, *args, missing_ok=False, input=None):
        self.assertEqual(repo, self.repo)
        if args[0] == "hash-object":
            return hashlib.sha1(b"blob " + str(len(input)).encode() + b"\0" + input).hexdigest().encode()
        if args[:2] == ("rev-parse", "HEAD"):
            return self.ancestry[0].encode()
        if args[0] == "diff":
            paths = args[args.index("--") + 1:]
            return json.dumps({name: (self.repo / name).read_text() if (self.repo / name).exists() else None
                               for name in paths}, sort_keys=True).encode()
        if args[0] == "log":
            name = args[-1]
            changed = []
            for index, commit in enumerate(self.ancestry):
                parent = self.ancestry[index + 1] if index + 1 < len(self.ancestry) else None
                previous = self.commits[parent].get(name) if parent else None
                if self.commits[commit].get(name) != previous:
                    changed.append(commit)
            return "\n".join(changed).encode()
        if args[0] == "show":
            commit, name = args[1].split(":", 1)
            data = self.commits[commit].get(name)
            if data is None and not missing_ok:
                raise receipt.ReceiptError("fixture path absent")
            return data
        if args[0] == "ls-tree":
            return b"100644 blob fixture\tfile" if args[-1] in self.commits[args[1]] else b""
        raise AssertionError(f"Unexpected or mutating Git command: {args}")

    def evidence(self, **extra):
        captured = receipt.capture(self.repo, ["feature.txt"])
        return {"checks": [{"command": "fixture behavior check", "outcome": "PASS",
                "artifact_identity": captured["artifact_identity"]}], **extra}

    def begin(self, policy="none", evidence=None):
        return receipt.begin(self.repo, self.record, ["feature.txt"], ["story.md"],
            evidence or self.evidence(), policy, "isolated fixture commit authority" if policy != "none" else None,
            "source-tracker://fixture/item")

    def seal(self, policy="none"):
        self.begin(policy)
        (self.repo / "story.md").write_text("complete; provisional until receipt delivery reconciles\n")
        return receipt.seal(self.repo, self.record)

    def test_no_commit_verified_completion_has_diff_identity_and_leaves_head(self):
        sealed = self.seal()
        result = receipt.reconcile(self.repo, self.record)
        self.assertEqual(result["state"], "VERIFIED_UNCOMMITTED")
        self.assertEqual(result["diff_identity"], sealed["delivery"]["diff_identity"])
        self.assertEqual(self.ancestry[0], self.head)

    def test_interruption_before_metadata_resumes_preparing_without_implementation(self):
        self.begin()
        result = receipt.reconcile(self.repo, self.record)
        self.assertEqual(result["state"], "PREPARING")
        self.assertTrue(result["checked_matches"])
        self.assertEqual((self.repo / "feature.txt").read_text(), "verified change\n")

    def test_failed_or_unattempted_commit_keeps_same_pending_transaction(self):
        self.seal("single")
        before = (self.repo / self.record).read_bytes()
        self.assertEqual(receipt.reconcile(self.repo, self.record)["state"], "COMMIT_PENDING")
        self.assertEqual(receipt.reconcile(self.repo, self.record)["state"], "COMMIT_PENDING")
        self.assertEqual((self.repo / self.record).read_bytes(), before)

    def test_post_commit_crash_recognizes_complete_bundle_without_second_commit(self):
        self.seal("single")
        before = (self.repo / self.record).read_bytes()
        commit = self.fixture_commit(["feature.txt", "story.md", self.record])
        result = receipt.reconcile(self.repo, self.record)
        self.assertEqual(result["state"], "COMPLETED_COMMITTED")
        self.assertEqual(result["commit"], commit)
        self.assertEqual((self.repo / self.record).read_bytes(), before)
        self.assertEqual(result["current_matches"], True)

    def test_commit_missing_terminal_metadata_cannot_complete(self):
        self.seal("single")
        self.fixture_commit(["feature.txt", self.record])
        self.assertEqual(receipt.reconcile(self.repo, self.record)["state"], "COMMIT_PENDING")

    def test_unrelated_new_head_preserves_historical_completed_result(self):
        self.seal("batch")
        accepted = self.fixture_commit(["feature.txt", "story.md", self.record])
        (self.repo / "other.txt").write_text("independent work\n")
        self.fixture_commit(["other.txt"])
        result = receipt.reconcile(self.repo, self.record)
        self.assertEqual(result["state"], "COMPLETED_COMMITTED")
        self.assertEqual(result["commit"], accepted)

    def test_changed_no_commit_content_requires_renewed_checks(self):
        self.seal()
        (self.repo / "feature.txt").write_text("new unchecked edit\n")
        self.assertEqual(receipt.reconcile(self.repo, self.record)["state"], "CHANGED_REQUIRES_CHECKS")

    def test_content_changed_before_seal_does_not_reuse_evidence(self):
        self.begin()
        (self.repo / "feature.txt").write_text("unchecked concurrent edit\n")
        with self.assertRaisesRegex(receipt.ReceiptError, "renew affected evidence"):
            receipt.seal(self.repo, self.record)

    def test_edit_between_seal_captures_preserves_preparing_and_requires_new_evidence(self):
        for policy in ("none", "single"):
            with self.subTest(policy=policy):
                (self.repo / "feature.txt").write_text("verified change\n")
                record_path = self.repo / self.record
                record_path.unlink(missing_ok=True)
                self.begin(policy)
                original = record_path.read_bytes()
                capture = receipt.capture
                calls = 0

                def concurrent_capture(*args, **kwargs):
                    nonlocal calls
                    calls += 1
                    if calls == 2:
                        (self.repo / "feature.txt").write_text("unchecked concurrent edit\n")
                    return capture(*args, **kwargs)

                with patch.object(receipt, "capture", side_effect=concurrent_capture):
                    with self.assertRaisesRegex(receipt.ReceiptError, "renew affected evidence"):
                        receipt.seal(self.repo, self.record)
                self.assertEqual(record_path.read_bytes(), original)
                result = receipt.reconcile(self.repo, self.record)
                self.assertEqual(result["state"], "PREPARING")
                self.assertFalse(result["checked_matches"])

    def test_preexisting_staged_work_is_never_modified_by_receipt_helpers(self):
        (self.repo / "other.txt").write_text("user staged work\n")
        before = self.staged
        self.seal()
        receipt.reconcile(self.repo, self.record)
        self.assertEqual(self.staged, before)

    def test_required_review_missing_and_error_results_cannot_complete(self):
        with self.assertRaisesRegex(receipt.ReceiptError, "Required review evidence"):
            self.begin(evidence=self.evidence(review_required=True))
        evidence = self.evidence()
        evidence["checks"][0]["outcome"] = "ERROR"
        with self.assertRaisesRegex(receipt.ReceiptError, "passing required evidence"):
            self.begin(evidence=evidence)

    def test_explicit_waiver_requires_authority_reason_and_exact_identity(self):
        evidence = self.evidence()
        evidence["checks"][0]["outcome"] = "WAIVED"
        with self.assertRaisesRegex(receipt.ReceiptError, "lacks authority"):
            self.begin(evidence=evidence)
        evidence["checks"][0].update(authority="fixture waiver", reason="fixture required tool unavailable")
        self.begin(evidence=evidence)
        receipt.seal(self.repo, self.record)
        self.assertEqual(receipt.reconcile(self.repo, self.record)["state"], "VERIFIED_UNCOMMITTED")

    def test_stale_check_identity_and_unauthorized_commit_policy_are_refused(self):
        evidence = self.evidence()
        evidence["checks"][0]["artifact_identity"] = "old identity"
        with self.assertRaisesRegex(receipt.ReceiptError, "does not match"):
            self.begin(evidence=evidence)
        with self.assertRaisesRegex(receipt.ReceiptError, "recorded user authority"):
            receipt.begin(self.repo, self.record, ["feature.txt"], ["story.md"], self.evidence(), policy="single")

    def test_receipt_is_not_overwritten_and_repository_escape_is_refused(self):
        self.begin()
        original = (self.repo / self.record).read_bytes()
        with self.assertRaisesRegex(receipt.ReceiptError, "already exists"):
            self.begin()
        self.assertEqual((self.repo / self.record).read_bytes(), original)
        with self.assertRaisesRegex(receipt.ReceiptError, "escapes repository"):
            receipt.capture(self.repo, ["../outside.txt"])

    def test_generated_minion_runtime_is_identical_and_self_contained(self):
        boss = Path(__file__).resolve().parents[1]
        minion = boss.parent / "rails-minion-workflow"
        for name in ("scripts/execution-receipt.py", "references/completion-contract.md"):
            self.assertEqual((boss / name).read_bytes(), (minion / name).read_bytes())


class RealGitCompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="receipt-git-test-", dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name).resolve()
        self.git("init", "--quiet")
        for key, value in (("user.name", "Receipt Fixture"), ("user.email", "receipt@example.invalid"),
                           ("core.autocrlf", "true"), ("core.safecrlf", "false"),
                           ("commit.gpgsign", "false"), ("core.hooksPath", str(self.repo / "empty-hooks"))):
            self.git("config", key, value)
        (self.repo / "feature.txt").write_bytes(b"baseline\r\n")
        (self.repo / "story.md").write_bytes(b"in progress\r\n")
        self.commit()

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        return result.stdout

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "--quiet", "-m", "isolated receipt regression fixture")
        return self.git("rev-parse", "HEAD").decode().strip()

    def prepare(self, paths=None):
        paths = paths or ["feature.txt"]
        captured = receipt.capture(self.repo, paths)
        evidence = {"checks": [{"command": "real Git WORKTREE receipt fixture check", "outcome": "PASS",
                               "artifact_identity": captured["artifact_identity"]}]}
        receipt.begin(self.repo, "receipt.json", paths, ["story.md"], evidence,
                      policy="single", authority="isolated fixture commits only")
        (self.repo / "story.md").write_bytes(b"completed\r\n")
        return receipt.seal(self.repo, "receipt.json")

    def test_real_autocrlf_commit_recognizes_crlf_artifacts_and_receipt(self):
        (self.repo / "feature.txt").write_bytes(b"verified change\r\n")
        sealed = self.prepare()
        path = self.repo / "receipt.json"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        committed = self.commit()
        self.assertNotEqual(path.read_bytes(), self.git("show", "HEAD:receipt.json"))
        self.assertNotEqual(sealed["delivery"]["files"]["feature.txt"]["sha256"],
                            receipt.digest(self.git("show", "HEAD:feature.txt")))
        index_before = (self.repo / ".git/index").read_bytes()
        record_before = path.read_bytes()
        result = receipt.reconcile(self.repo, "receipt.json")
        self.assertEqual(result["state"], "COMPLETED_COMMITTED")
        self.assertEqual(result["commit"], committed)
        self.assertTrue(result["current_matches"])
        self.assertEqual((self.repo / ".git/index").read_bytes(), index_before)
        self.assertEqual(path.read_bytes(), record_before)

    def test_real_clean_filter_normalizes_artifacts_and_receipt(self):
        filter_path = self.repo / "clean-filter.py"
        filter_path.write_text("import sys\nsys.stdout.buffer.write(sys.stdin.buffer.read().replace("
                               "b'WORKTREE', b'CANONICAL'))\n", encoding="utf-8")
        command = f'"{Path(sys.executable).as_posix()}" "{filter_path.as_posix()}"'
        self.git("config", "filter.fixture.clean", command)
        self.git("config", "filter.fixture.required", "true")
        (self.repo / ".gitattributes").write_bytes(b"feature.txt filter=fixture\nreceipt.json filter=fixture\n")
        (self.repo / "feature.txt").write_bytes(b"WORKTREE verified change\r\n")
        self.prepare(["feature.txt", ".gitattributes", "clean-filter.py"])
        committed = self.commit()
        self.assertIn(b"CANONICAL", self.git("show", "HEAD:feature.txt"))
        self.assertIn(b"CANONICAL", self.git("show", "HEAD:receipt.json"))
        result = receipt.reconcile(self.repo, "receipt.json")
        self.assertEqual(result["state"], "COMPLETED_COMMITTED")
        self.assertEqual(result["commit"], committed)
        self.assertTrue(result["current_matches"])

    def test_real_attributes_freeze_normalized_identity_and_keep_raw_dirty_detection(self):
        (self.repo / ".gitattributes").write_bytes(b"*.txt text eol=lf\n*.md text eol=lf\n*.json text eol=lf\n")
        (self.repo / "feature.txt").write_bytes(b"verified change\r\n")
        self.prepare(["feature.txt", ".gitattributes"])
        committed = self.commit()
        result = receipt.reconcile(self.repo, "receipt.json")
        self.assertEqual(result["state"], "COMPLETED_COMMITTED")
        self.assertEqual(result["commit"], committed)
        (self.repo / "feature.txt").write_bytes(b"verified change\n")
        result = receipt.reconcile(self.repo, "receipt.json")
        self.assertEqual(result["state"], "COMPLETED_COMMITTED")
        self.assertFalse(result["current_matches"])


if __name__ == "__main__":
    unittest.main()
