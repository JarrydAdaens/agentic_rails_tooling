#!/usr/bin/env python3
"""Generate Minion's self-contained receipt helper/reference from the Boss source."""
from pathlib import Path
import shutil

boss = Path(__file__).resolve().parents[1]
minion = boss.parent / "rails-minion-workflow"
for relative in ("scripts/execution-receipt.py", "references/completion-contract.md"):
    target = minion / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(boss / relative, target)
print("Generated Minion receipt helper and completion contract")
