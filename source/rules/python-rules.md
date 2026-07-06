---
paths:
  - "**/*.py"
  - "**/pyproject.toml"
---

# Python Coding Rules

## Scope

Applies to all Python in this workspace: applications, scripts, and skill/tooling scripts (e.g. `rails_lint.py`, oracle scripts).

Intent: readable, idiomatic, type-hinted Python that follows PEP 8 and modern community tooling, so any Python developer (or agent) can pick it up without learning house dialect.

House-convention exemption: the workspace `in_` parameter prefix used in C# and TypeScript is **not** used in Python. PEP 8 naming is the dominant ecosystem standard, and fighting it would break consistency with every linter, library, and collaborator. This is a deliberate decision, not drift.

## Language

- Target modern Python (3.11+ unless the project pins otherwise). Prefer current syntax: `match` where it clarifies, `pathlib` over `os.path`, f-strings over `%` or `.format()`.
- Type-hint all function signatures (parameters and return type), including `-> None`. Use built-in generics (`list[str]`, `dict[str, int]`) and `X | None` over `Optional[X]`.
- Prefer `dataclasses` (or `NamedTuple` for small immutable records) over bare dicts and tuples for structured data crossing a function boundary.
- Use context managers (`with`) for files, locks, connections, and anything with cleanup. Never rely on garbage collection to release resources.
- Catch specific exceptions. Never use a bare `except:`; use `except Exception` only at a top-level boundary that logs and re-raises or exits.
- Raise exceptions rather than returning sentinel values (`-1`, `""`, `None`-with-meaning) for error conditions.
- Prefer comprehensions for simple transforms; use a plain loop once a comprehension needs nesting or multiple conditions to stay readable.
- Use `logging` in applications, not `print`. `print` is acceptable in CLI scripts where stdout is the interface.
- Guard script entry points with `if __name__ == "__main__":` and keep the logic in a `main()` function so it is importable and testable.

## Naming

- Modules and packages: `snake_case`, short, no hyphens.
- Functions, methods, variables, and parameters: `snake_case`.
- Classes and exceptions: `PascalCase`.
- Module-level constants: `SCREAMING_SNAKE_CASE`.
- Internal helpers: single leading underscore (`_parse_frontmatter`). Do not use double-underscore name mangling.
- Boolean names read as predicates: `is_valid`, `has_frontmatter`, `should_retry`.

## Structure

- One primary class or cohesive concern per module. Small, inseparable helper types may live beside their owner.
- Order imports: standard library, third party, local — separated by blank lines. No wildcard imports.
- Keep functions focused; extract a helper when a function needs section comments to stay navigable.
- Prefer pure functions for logic; isolate I/O, subprocess, and environment access at the edges so logic is testable without mocks.

## Tooling

- Format with `ruff format` (or `black`); lint with `ruff check`. Fix lint findings with the tool (`ruff check --fix`), not by hand-editing around them.
- Type-check with `mypy` or `pyright` where a project has type-checking configured; do not add `# type: ignore` without a reason comment.
- Configure everything in `pyproject.toml`. Do not scatter `setup.cfg`, `.flake8`, or per-tool dotfiles in new projects.
- Use `uv` for environments and dependencies in new projects (`uv run`, `uv add`); never install into the system interpreter.
- Pin dependencies for applications (lock file); keep libraries permissive with lower bounds.
- Test with `pytest`: plain `assert`, small focused tests, `tmp_path`/`monkeypatch` fixtures over hand-rolled setup.

## Do Not

- Do not use mutable default arguments (`def f(items=[])`). Default to `None` and create inside.
- Do not shadow built-ins (`list`, `dict`, `id`, `type`) with variable names.
- Do not use `assert` for runtime validation in application code — it disappears under `python -O`. Raise `ValueError`/`TypeError` instead.
- Do not build paths by string concatenation. Use `pathlib.Path`.
- Do not call `subprocess` with `shell=True` on any string containing external input; pass an argument list.
- Do not use `eval`/`exec` on external input, or `pickle` for untrusted data.
- Do not swallow exceptions silently (`except Exception: pass`). Log, handle, or re-raise.

## Examples

```python
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class LintFinding:
    path: Path
    line: int
    message: str

def collect_findings(root: Path, banned_terms: list[str]) -> list[LintFinding]:
    """Scan markdown files under root for banned vocabulary."""
    findings: list[LintFinding] = []
    for file in root.rglob("*.md"):
        for line_number, line in enumerate(file.read_text(encoding="utf-8").splitlines(), start=1):
            for term in banned_terms:
                if term in line:
                    findings.append(LintFinding(file, line_number, f"banned term: {term}"))
    return findings

def main() -> int:
    findings = collect_findings(Path.cwd(), ["TODO-REMOVE"])
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.message}")
    return 1 if findings else 0

if __name__ == "__main__":
    raise SystemExit(main())
```
