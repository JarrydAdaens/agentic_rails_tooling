---
name: using-scripts
description: How to reference one-off commands and bundle reusable executable scripts in Agent Skills.
metadata:
  version: "1.1"
---

# Using Scripts In Skills

Skills can reference one-off commands or bundle reusable executable scripts under `scripts/`.

## One-Off Commands

Use direct commands when an existing package already does the job and the invocation is simple:

```bash
uvx ruff@0.8.0 check .
npx eslint@9.0.0 .
```

Pin versions so repeated runs behave predictably. State runtime requirements in the skill, or use the `compatibility` frontmatter field if the requirement is broad.

## Referencing Bundled Scripts

List available scripts in `SKILL.md` and use paths relative to the skill root:

```markdown
## Available scripts

- `scripts/validate.sh` validates configuration files.
- `scripts/process.py` processes input data.
```

```bash
bash scripts/validate.sh "$INPUT_FILE"
python3 scripts/process.py --input results.json
```

## Script Design For Agents

Scripts should be easy for a non-interactive agent to run and recover from:

- Avoid prompts; accept flags, environment variables, files, or stdin.
- Provide concise `--help` output with examples.
- Write helpful errors that say what failed and what to try.
- Send structured data to stdout and diagnostics to stderr.
- Use meaningful exit codes.
- Support `--dry-run` for destructive or stateful operations.
- Keep output bounded or require an explicit `--output` path for large results.

## Self-Contained Python Scripts

Python scripts can use PEP 723 inline dependencies and run with `uv run`:

```python
# /// script
# dependencies = [
#   "beautifulsoup4>=4.12,<5",
# ]
# ///
```

Source: [AgentSkills.io Using Scripts](https://agentskills.io/skill-creation/using-scripts)
