"""Focused tests for rails_lint.py — rule regexes, pragmas, and structure checks."""

import tempfile
import unittest
from pathlib import Path

import rails_lint

GOOD_FRONTMATTER = (
    "---\n"
    "name: {name}\n"
    "description: Use this when testing the linter.\n"
    "metadata:\n"
    "  version: \"1.0\"\n"
    "---\n"
)


def lint_text(in_tmp: Path, in_relative_path: str, in_text: str):
    """Write one file into the temp repo and lint the repo root."""
    target = in_tmp / in_relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(in_text, encoding="utf-8")
    return rails_lint.lint_paths([in_tmp], False)


def rule_ids(in_violations):
    return {violation.rule for violation in in_violations}


class VocabularyTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_sprint_flagged_with_word_boundary(self):
        body = GOOD_FRONTMATTER.format(name="doc") + "Plan the sprint now.\n"
        self.assertIn("VC001", rule_ids(lint_text(self.root, "doc.md", body)))

    def test_sprinting_not_flagged(self):
        body = GOOD_FRONTMATTER.format(name="doc") + "The runner was sprinting home.\n"
        self.assertNotIn("VC001", rule_ids(lint_text(self.root, "doc.md", body)))

    def test_tier_number_flagged_outside_canonical_file(self):
        body = GOOD_FRONTMATTER.format(name="doc") + "This is a Tier 5 plan.\n"
        self.assertIn("VC005", rule_ids(lint_text(self.root, "doc.md", body)))

    def test_tier_number_allowed_in_canonical_design_file(self):
        body = GOOD_FRONTMATTER.format(name="design") + "| Tier 2 | Milestone |\n"
        self.assertNotIn("VC005", rule_ids(lint_text(self.root, "design.md", body)))

    def test_legacy_path_flagged_but_milestones_folder_is_not(self):
        body = (GOOD_FRONTMATTER.format(name="doc")
                + "Old: context/milestones.md and context/goals1.md.\n"
                + "New: context/milestones/milestone-1.md is fine.\n")
        violations = [v for v in lint_text(self.root, "doc.md", body) if v.rule == "VC004"]
        self.assertEqual(len(violations), 2)

    def test_pragma_allows_named_rules(self):
        body = (GOOD_FRONTMATTER.format(name="doc")
                + "<!-- rails-lint-allow: VC001 VC003 -->\n"
                + "Legacy note: the sprint model was Scrum-aligned.\n")
        ids = rule_ids(lint_text(self.root, "doc.md", body))
        self.assertNotIn("VC001", ids)
        self.assertNotIn("VC003", ids)

    def test_pragma_all_silences_the_file(self):
        body = ("<!-- rails-lint-allow: all -->\n"
                "Seven-tier sprint Scrum Tier 4 - Task context/goals1.md\n")
        self.assertEqual(lint_text(self.root, "doc.md", body), [])


class FrontmatterTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_unquoted_version_flagged(self):
        body = GOOD_FRONTMATTER.format(name="my-skill").replace("\"1.0\"", "1.0")
        violations = lint_text(self.root, "source/skills/my-skill/SKILL.md", body)
        self.assertIn("FM005", rule_ids(violations))

    def test_name_folder_mismatch_flagged_for_skill(self):
        body = GOOD_FRONTMATTER.format(name="wrong-name")
        violations = lint_text(self.root, "source/skills/my-skill/SKILL.md", body)
        self.assertIn("FM003", rule_ids(violations))

    def test_clean_skill_passes(self):
        body = GOOD_FRONTMATTER.format(name="my-skill") + "Milestone planning content.\n"
        self.assertEqual(lint_text(self.root, "source/skills/my-skill/SKILL.md", body), [])

    def test_banned_tooling_key_flagged_under_source(self):
        body = GOOD_FRONTMATTER.format(name="my-skill").replace(
            "metadata:\n", "repo: some-project\nmetadata:\n")
        violations = lint_text(self.root, "source/skills/my-skill/SKILL.md", body)
        self.assertIn("FM006", rule_ids(violations))

    def test_reference_file_without_description_passes(self):
        body = ("---\n"
                "name: some-reference\n"
                "metadata:\n"
                "  version: \"1.1\"\n"
                "---\n"
                "Reference content.\n")
        violations = lint_text(self.root, "source/skills/my-skill/references/some-reference.md", body)
        self.assertNotIn("FM004", rule_ids(violations))

    def test_rules_file_shape_needs_no_name(self):
        body = ("---\n"
                "description: C# coding rules for .NET projects.\n"
                "globs: [\"**/*.cs\"]\n"
                "alwaysApply: false\n"
                "metadata:\n"
                "  version: \"1.3\"\n"
                "---\n"
                "Rules content.\n")
        violations = lint_text(self.root, "source/rules/csharp-rules.md", body)
        self.assertNotIn("FM002", rule_ids(violations))

    def test_session_learning_file_is_fully_exempt(self):
        body = ("---\n"
                "type: session-learning\n"
                "project: example\n"
                "---\n"
                "The session planned a sprint under the seven-tier Scrum model.\n")
        self.assertEqual(lint_text(self.root, "memories/learnings/new/example.md", body), [])

    def test_folded_description_length_counted(self):
        long_text = ("  " + "x" * 80 + "\n") * 15
        body = ("---\n"
                "name: doc\n"
                "description: >-\n"
                f"{long_text}"
                "metadata:\n"
                "  version: \"1.0\"\n"
                "---\n")
        self.assertIn("FM004", rule_ids(lint_text(self.root, "doc.md", body)))


class StructureAndHygieneTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_skill_folder_without_skill_md_flagged(self):
        (self.root / "source" / "skills" / "empty-skill").mkdir(parents=True)
        self.assertIn("ST001", rule_ids(rails_lint.lint_paths([self.root], False)))

    def test_agent_folder_needs_persona_suffix(self):
        agent_dir = self.root / "source" / "agents" / "helper"
        agent_dir.mkdir(parents=True)
        (agent_dir / "AGENT.md").write_text(
            GOOD_FRONTMATTER.format(name="helper"), encoding="utf-8")
        self.assertIn("NM002", rule_ids(rails_lint.lint_paths([self.root], False)))

    def test_junk_file_flagged(self):
        (self.root / "Desktop.ini").write_text("[junk]\n", encoding="utf-8")
        self.assertIn("HY001", rule_ids(rails_lint.lint_paths([self.root], False)))

    def test_archived_skipped_by_default(self):
        archived = self.root / "archived" / "old-doc.md"
        archived.parent.mkdir(parents=True)
        archived.write_text("sprint planning under the seven-tier Scrum model\n", encoding="utf-8")
        self.assertEqual(rails_lint.lint_paths([self.root], False), [])
        self.assertNotEqual(rails_lint.lint_paths([self.root], True), [])


if __name__ == "__main__":
    unittest.main()
