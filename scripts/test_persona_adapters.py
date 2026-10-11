"""Portable package contracts; these tests do not claim native host activation."""

from contextlib import redirect_stdout, redirect_stderr
import io
from pathlib import Path
import shutil
import tempfile
import tomllib
import unittest

import generate_persona_adapters as adapters


ROOT = adapters.DEFAULT_ROOT
TRIGGERS = {
    "quality-gate-persona": ("Pre-commit", "user wants implementation", "Report; do not silently repair"),
    "unreal-persona": ("Gameplay systems", "generic C++ with no Unreal context", "GC-safe pointers"),
    "web-persona": ("React components", "mostly C# service", "validate before use"),
    "wpf-persona": ("WPF screens", "generic C# backend", "MVVM and binding"),
    "xna-persona": ("Restoring", "native desktop WPF engineering", "simulation in `Update`"),
}


class PersonaAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="persona-fixture-", dir=ROOT / "scripts")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "relocated tooling with spaces"
        shutil.copytree(ROOT / "source" / "agents", self.root / "source" / "agents")
        (self.root / "scripts").mkdir()
        for filename in ("persona-adapters.json", "persona-adapter-template.txt"):
            shutil.copyfile(ROOT / "scripts" / filename, self.root / "scripts" / filename)

    def run_cli(self, *args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return adapters.main(["--repo-root", str(self.root), *args])

    def test_committed_parity(self):
        for path, content in adapters.generate().items():
            with self.subTest(persona=path.stem):
                self.assertEqual(path.read_bytes().replace(b"\r\n", b"\n"), content.encode("utf-8"))

    def test_repeatable_and_relocated(self):
        original = {path.name: content for path, content in adapters.generate().items()}
        relocated = {path.name: content for path, content in adapters.generate(self.root).items()}
        self.assertEqual(original, relocated)
        self.assertEqual(relocated, {p.name: c for p, c in adapters.generate(self.root).items()})

    def test_check_reports_drift_without_writing(self):
        path = self.root / "source" / "agents" / "wpf-persona.toml"
        path.write_bytes(b"intentional drift\n")
        self.assertEqual(self.run_cli("--check"), 1)
        self.assertEqual(path.read_bytes(), b"intentional drift\n")
        self.assertEqual(self.run_cli(), 0)
        self.assertEqual(self.run_cli("--check"), 0)

    def test_check_reports_missing_output_without_writing(self):
        path = self.root / "source" / "agents" / "web-persona.toml"
        path.unlink()
        self.assertEqual(self.run_cli("--check"), 1)
        self.assertFalse(path.exists())

    def test_windows_checkout_line_endings_are_not_drift(self):
        path = self.root / "source" / "agents" / "web-persona.toml"
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        before = path.read_bytes()
        self.assertEqual(self.run_cli("--check"), 0)
        self.assertEqual(path.read_bytes(), before)

    def test_missing_reference_rejects_all_writes(self):
        (self.root / "source/agents/wpf-persona/references/componentization.md").unlink()
        before = {p: p.read_bytes() for p in (self.root / "source/agents").glob("*.toml")}
        self.assertEqual(self.run_cli(), 2)
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_missing_activation_exclusion_rejected(self):
        path = self.root / "source/agents/web-persona/AGENT.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "## Use Another Primary Agent When", "## Removed exclusion"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Use Another Primary Agent When"):
            adapters.generate(self.root)

    def test_activation_contracts_and_fallback(self):
        self.assertEqual({p.stem for p in adapters.generate()}, set(TRIGGERS))
        for path, content in adapters.generate().items():
            with self.subTest(persona=path.stem):
                data = tomllib.loads(content)
                self.assertEqual(data["name"], path.stem)
                instructions = data["developer_instructions"]
                for expected in TRIGGERS[path.stem]:
                    self.assertIn(expected, instructions)
                self.assertIn("If the bundle is absent", instructions)
                self.assertIn("without inventing reference", instructions)
                self.assertIn("Read only the smallest relevant reference set", instructions)

    def test_portable_lookup_and_no_machine_paths(self):
        for path, content in adapters.generate().items():
            with self.subTest(persona=path.stem):
                self.assertNotRegex(content, r"[A-Za-z]:[/\\]|/Users/|/home/|\\\\[^\s]+\\")
                self.assertNotIn("Jarry", content)
                for candidate in ("containing this adapter", "source/agents/", "CODEX_HOME",
                                  ".codex/agents/", ".agents/agents/", "actual\nuser home"):
                    self.assertIn(candidate, content)
                self.assertIn("not TOML variable interpolation", content)
                self.assertIn("relative to that same\nbundle", content)

    def test_canonical_stance_change_updates_output(self):
        before = adapters.generate(self.root)
        path = self.root / "source/agents/wpf-persona/AGENT.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "Prefer composition over inheritance.", "Prefer composition with a fixture constraint."),
            encoding="utf-8")
        after = adapters.generate(self.root)
        changed = [p.name for p in before if before[p] != after[p]]
        self.assertEqual(changed, ["wpf-persona.toml"])


if __name__ == "__main__":
    unittest.main()
