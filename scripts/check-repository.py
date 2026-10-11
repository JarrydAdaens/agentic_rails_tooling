"""Run the right rail's read-only source and component checks from any directory."""

from __future__ import annotations

import subprocess
import sys
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    checks = [
        ("repository lint", [sys.executable, str(ROOT / "scripts/rails_lint.py"), str(ROOT)]),
        ("persona adapter parity", [sys.executable, str(ROOT / "scripts/generate_persona_adapters.py"), "--check"]),
        ("infrastructure tests", [sys.executable, "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"]),
        ("execution receipt tests", [sys.executable, "-m", "unittest", "discover", "-s", "source/skills/rails-boss-execute-workflow/scripts", "-p", "test_*.py"]),
        ("phase file tests", [sys.executable, "-m", "unittest", "discover", "-s", "source/skills/rails-planning-phaser/scripts", "-p", "test_*.py"]),
    ]
    failed = []
    # Some host sandboxes expose a temporary path that exists but rejects writes.
    # Fixtures get a disposable, repository-owned temp directory instead.
    with tempfile.TemporaryDirectory(prefix="rails-check-", dir=ROOT / "scripts") as temporary:
        environment = os.environ.copy()
        environment.update({"TMP": temporary, "TEMP": temporary, "TMPDIR": temporary})
        for label, command in checks:
            print(f"\n=== {label} ===", flush=True)
            result = subprocess.run(command, cwd=ROOT, env=environment, check=False)
            if result.returncode:
                failed.append(f"{label} (exit {result.returncode})")
    if failed:
        print("Failed: " + ", ".join(failed), file=sys.stderr)
        return 1
    print("\nAll tooling repository checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
