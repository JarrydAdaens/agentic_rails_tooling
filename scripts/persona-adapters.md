---
name: persona-adapters
description: Authoring, generation, validation, and runtime limits of portable Codex persona adapters.
metadata:
  version: "1.0"
---

# Portable Codex persona adapters

The five `source/agents/*.toml` files are generated deployment artifacts. Their
canonical behavior comes from each bundle's `AGENT.md`: Best Fit, Use Another
Primary Agent When, Default Stance (Operating Principles for Quality Gate),
Typical Reference Combinations, and Avoid. Edit those sections to change behavior.
The shared lookup and fallback instructions live in `persona-adapter-template.txt`;
`persona-adapters.json` preserves the existing native discovery names and descriptions.
All authoring and generation infrastructure stays outside the deployed `source/` tree.

```text
python scripts/generate_persona_adapters.py
python scripts/generate_persona_adapters.py --check
python -m unittest discover -s scripts -p test_persona_adapters.py
```

The generator defaults to its own repository, independent of the working directory.
`--repo-root` selects a relocated authoring checkout. Generation validates all five
inputs and focused reference filenames before writing UTF-8 files with LF line
endings. `--check` compares content bytes after normalizing Git's optional Windows
CRLF checkout endings, reports missing files or drift, and writes nothing. All
other content differences count as drift. Exit codes are 0 for success, 1 for parity
drift, and 2 for invalid inputs.
Python 3.11 or later is required; there are no third-party dependencies.

Deploy each TOML alongside its matching persona bundle through the existing outward
deployment flow. The adapter instructs the agent to look beside the adapter when
its location is exposed, in workspace `source/agents/` or `agents/`, under the runtime
`CODEX_HOME`, and under the actual user home's `.codex/agents/` or `.agents/agents/`.
TOML does not expand environment variables here: the host or agent must resolve
those values. References are relative to the chosen bundle, preventing mixed-root
reference loading. A standalone adapter still contains activation exclusions,
core stance, and avoid guidance, and must disclose that the full bundle is missing.

Tests cover exact parity, repeated generation, relocation with spaces, missing
outputs, invalid inputs before writes, canonical behavior changes, portable lookup
instructions, and positive and negative activation guidance for every persona.
These are static package contracts; they do not prove that a native host selects
the correct persona or reads its bundle. Live host discovery, actual invocation,
and focused reference reads remain deployment smoke checks. This generator neither
installs nor registers personas and makes no host-version support claim.
