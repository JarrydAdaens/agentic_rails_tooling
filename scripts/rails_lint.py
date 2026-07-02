#!/usr/bin/env python3
"""Deterministic linter for Agentic Rails repositories.

Checks Markdown artifacts against the framework's authoring conventions
(frontmatter shape, naming, folder structure) and the six-tier reform's
banned-vocabulary map (agentic-rails-six-tier-addendum, section 16).

Usage:
    python rails_lint.py [paths ...] [--skip IDS] [--only IDS]
                         [--include-archived] [--list-rules]

Exit codes: 0 = clean, 1 = violations found, 2 = usage error.

A file can opt out of specific rules with an HTML comment pragma anywhere
in the file:

    <!-- rails-lint-allow: VC001 VC005 -->
    <!-- rails-lint-allow: all -->

Use pragmas for archived-model migration notes and legacy references that
must keep the old vocabulary on purpose.
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Directories never scanned. `archived` is also skipped unless --include-archived.
EXCLUDED_DIRS = {
    ".git", "node_modules", "__pycache__", ".vs", ".idea",
    ".claude", ".cursor", ".agents", "ide_specific", "_planning-runs",
}

# Files that should never be committed to a rails repo (HY001).
JUNK_FILES = {"desktop.ini", "thumbs.db", "debug.log"}

# Files allowed to state the canonical numbered tier table (VC005 exemption).
CANONICAL_TIER_FILES = {"design.md", "agenticworkflow.md"}

KEBAB_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PRAGMA = re.compile(r"<!--\s*rails-lint-allow:\s*([A-Za-z0-9 ,]+?)\s*-->")
MAX_DESCRIPTION_CHARS = 1024

# Frontmatter keys banned in the tooling repo (rails-clean-frontmatter, tooling mode).
BANNED_TOOLING_KEYS = ("agentic_rails_source_version", "repo", "changelog", "invocation")

# Vocabulary rules from the six-tier addendum's terminology replacement map.
# Each entry: (rule id, compiled pattern, message).
VOCAB_RULES = [
    ("VC001", re.compile(r"\bsprints?\b", re.IGNORECASE),
     "retired vocabulary 'sprint' - milestones own this function now"),
    ("VC002", re.compile(r"\bseven[- ]tier\b|\b7-tier\b", re.IGNORECASE),
     "retired vocabulary 'seven-tier' - say 'the context tier system'"),
    ("VC003", re.compile(r"\bscrum\b", re.IGNORECASE),
     "Scrum is not the operating model - use milestone-centric language"),
    ("VC004", re.compile(r"context/(?:goals[^/\s`)\"]*\.md|milestones\.md|tier0)", re.IGNORECASE),
     "legacy context path - goals*.md, milestones.md, and tier0/ are retired"),
    ("VC005", re.compile(r"\bTier\s+\d\b"),
     "numbered tier reference - use tier names; numbers live only in the canonical table"),
    ("VC006", re.compile(r"\bTier\s+\d\s*[-–—:]\s*Task\b|\btask\s+tier\b", re.IGNORECASE),
     "'task' is banned as a tier name"),
]

ALL_RULES = {
    "FM001": "frontmatter block missing or unterminated",
    "FM002": "frontmatter 'name' missing or not kebab-case",
    "FM003": "frontmatter 'name' does not match its folder name",
    "FM004": "frontmatter 'description' missing or over 1024 characters",
    "FM005": "frontmatter 'metadata.version' missing or not a quoted string",
    "FM006": "banned frontmatter key in tooling repo (agentic_rails_source_version, repo, changelog, invocation)",
    "ST001": "skill folder is missing SKILL.md",
    "ST002": "agent folder is missing AGENT.md",
    "NM001": "skill/agent folder name is not kebab-case",
    "NM002": "agent folder name must end in -persona",
    "HY001": "junk file committed (Desktop.ini, Thumbs.db, debug.log)",
    **{rule_id: message for rule_id, _, message in VOCAB_RULES},
}


@dataclass
class Violation:
    path: Path
    line: int
    rule: str
    message: str


def find_files(in_root: Path, in_include_archived: bool):
    """Yield every file under in_root, pruning excluded directories."""
    excluded = set(EXCLUDED_DIRS)
    if not in_include_archived:
        excluded.add("archived")
    for dirpath, dirnames, filenames in os.walk(in_root):
        dirnames[:] = sorted(d for d in dirnames if d not in excluded)
        for filename in sorted(filenames):
            yield Path(dirpath) / filename


def split_frontmatter(in_lines):
    """Return (frontmatter_lines, body_start_index) or (None, 0).

    body_start_index is the 0-based index of the first line after the
    closing delimiter. Returns (None, -1) for an unterminated block.
    """
    if not in_lines or in_lines[0].strip() != "---":
        return None, 0
    for index in range(1, len(in_lines)):
        if in_lines[index].strip() == "---":
            return in_lines[1:index], index + 1
    return None, -1


def parse_frontmatter(in_fm_lines):
    """Parse top-level keys and the metadata block from frontmatter lines.

    Returns (fields, metadata) where each maps key -> (raw_value, 0-based
    line offset within the frontmatter block).
    """
    fields = {}
    metadata = {}
    current_top_key = None
    for offset, line in enumerate(in_fm_lines):
        top_match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if top_match:
            current_top_key = top_match.group(1)
            fields[current_top_key] = (top_match.group(2).strip(), offset)
            continue
        if current_top_key == "metadata":
            nested_match = re.match(r"^\s+([\w-]+):\s*(.*)$", line)
            if nested_match:
                metadata[nested_match.group(1)] = (nested_match.group(2).strip(), offset)
    return fields, metadata


def folded_value(in_fm_lines, in_offset, in_inline_value):
    """Resolve a possibly block-folded YAML scalar to its full text."""
    if in_inline_value not in (">", ">-", "|", "|-"):
        return in_inline_value
    parts = []
    for line in in_fm_lines[in_offset + 1:]:
        if re.match(r"^\s+\S", line):
            parts.append(line.strip())
        elif line.strip() == "":
            continue
        else:
            break
    return " ".join(parts)


def collect_pragma_allows(in_text):
    """Return the set of rule ids the file opts out of via pragma comments."""
    allows = set()
    for match in PRAGMA.finditer(in_text):
        for token in re.split(r"[\s,]+", match.group(1).strip()):
            if token:
                allows.add(token.upper() if token.lower() != "all" else "all")
    return allows


def is_under_tooling_source(in_path: Path):
    """True when the file lives under a repo root that has source/skills/."""
    for ancestor in in_path.parents:
        if (ancestor / "source" / "skills").is_dir():
            return True
    return False


def is_session_learning(in_lines):
    """True for memory-rail learning captures, which use their own schema.

    Learning files are historical session records written by the
    rails-memory-learnings skill; they are exempt from artifact frontmatter
    rules and from vocabulary rewrites (history must not be falsified).
    """
    fm_lines, _ = split_frontmatter(in_lines)
    if fm_lines is None:
        return False
    fields, _ = parse_frontmatter(fm_lines)
    entry = fields.get("type")
    return entry is not None and entry[0] == "session-learning"


def check_frontmatter(in_path: Path, in_lines, out_violations):
    """Run FM001-FM006 for one markdown file."""
    fm_lines, body_start = split_frontmatter(in_lines)
    is_artifact = in_path.name in ("SKILL.md", "AGENT.md")

    if fm_lines is None:
        if body_start == -1:
            out_violations.append(Violation(in_path, 1, "FM001", "unterminated frontmatter block"))
        elif is_artifact:
            out_violations.append(Violation(in_path, 1, "FM001", "missing frontmatter block"))
        return

    fields, metadata = parse_frontmatter(fm_lines)

    # Line numbers inside the block are offset by the opening '---' line.
    def line_of(in_offset):
        return in_offset + 2

    # Rules files use the Cursor shape (description/globs/alwaysApply) and
    # deliberately carry no 'name' key.
    is_rules_file = "globs" in fields or "alwaysApply" in fields

    name_entry = fields.get("name")
    if name_entry is None:
        if not is_rules_file:
            out_violations.append(Violation(in_path, 1, "FM002", "frontmatter has no 'name' key"))
    else:
        name_value, name_offset = name_entry
        if not KEBAB_CASE.match(name_value):
            out_violations.append(Violation(
                in_path, line_of(name_offset), "FM002",
                f"name '{name_value}' is not kebab-case"))
        elif is_artifact and name_value != in_path.parent.name:
            out_violations.append(Violation(
                in_path, line_of(name_offset), "FM003",
                f"name '{name_value}' does not match folder '{in_path.parent.name}'"))

    # Only discovery-surface artifacts require a description; reference and
    # supporting files carry name + version only.
    description_entry = fields.get("description")
    if description_entry is None:
        if is_artifact:
            out_violations.append(Violation(
                in_path, 1, "FM004", "frontmatter has no 'description' key"))
    else:
        description_value, description_offset = description_entry
        full_text = folded_value(fm_lines, description_offset, description_value)
        if not full_text:
            out_violations.append(Violation(
                in_path, line_of(description_offset), "FM004", "description is empty"))
        elif len(full_text) > MAX_DESCRIPTION_CHARS:
            out_violations.append(Violation(
                in_path, line_of(description_offset), "FM004",
                f"description is {len(full_text)} chars (max {MAX_DESCRIPTION_CHARS})"))

    version_entry = metadata.get("version")
    if version_entry is None:
        out_violations.append(Violation(
            in_path, 1, "FM005", "frontmatter has no 'metadata.version' key"))
    else:
        version_value, version_offset = version_entry
        if not re.match(r"^([\"']).+\1$", version_value):
            out_violations.append(Violation(
                in_path, line_of(version_offset), "FM005",
                f"metadata.version {version_value or '(empty)'} must be a quoted string"))

    if is_under_tooling_source(in_path):
        for banned_key in BANNED_TOOLING_KEYS:
            for source, entry in (("", fields.get(banned_key)), ("metadata.", metadata.get(banned_key))):
                if entry is not None:
                    out_violations.append(Violation(
                        in_path, line_of(entry[1]), "FM006",
                        f"banned key '{source}{banned_key}' in tooling repo frontmatter"))


def check_vocabulary(in_path: Path, in_lines, out_violations):
    """Run VC001-VC006 over every line of one markdown file."""
    exempt_from_tier_numbers = in_path.name.lower() in CANONICAL_TIER_FILES
    for line_number, line in enumerate(in_lines, start=1):
        if PRAGMA.search(line):
            continue
        for rule_id, pattern, message in VOCAB_RULES:
            if rule_id == "VC005" and exempt_from_tier_numbers:
                continue
            for match in pattern.finditer(line):
                out_violations.append(Violation(
                    in_path, line_number, rule_id, f"{message}: '{match.group(0)}'"))


def check_structure(in_root: Path, in_include_archived: bool, out_violations):
    """Run ST/NM checks over skill and agent bundle folders."""
    excluded = set(EXCLUDED_DIRS)
    if not in_include_archived:
        excluded.add("archived")
    for dirpath, dirnames, _filenames in os.walk(in_root):
        dirnames[:] = sorted(d for d in dirnames if d not in excluded)
        parent = Path(dirpath)
        if parent.name not in ("skills", "agents"):
            continue
        for child_name in dirnames:
            child = parent / child_name
            if not KEBAB_CASE.match(child_name):
                out_violations.append(Violation(
                    child, 1, "NM001", f"folder '{child_name}' is not kebab-case"))
            if parent.name == "skills" and not (child / "SKILL.md").is_file():
                out_violations.append(Violation(child, 1, "ST001", "skill folder has no SKILL.md"))
            if parent.name == "agents":
                if not (child / "AGENT.md").is_file():
                    out_violations.append(Violation(child, 1, "ST002", "agent folder has no AGENT.md"))
                if not child_name.endswith("-persona"):
                    out_violations.append(Violation(
                        child, 1, "NM002", f"agent folder '{child_name}' must end in -persona"))


def lint_paths(in_roots, in_include_archived):
    """Lint every root and return the combined violation list."""
    violations = []
    for root in in_roots:
        check_structure(root, in_include_archived, violations)
        for path in find_files(root, in_include_archived):
            if path.name.lower() in JUNK_FILES:
                violations.append(Violation(path, 1, "HY001", f"junk file '{path.name}'"))
            if path.suffix.lower() not in (".md", ".mdc"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError as error:
                violations.append(Violation(path, 1, "FM001", f"unreadable file: {error}"))
                continue
            allows = collect_pragma_allows(text)
            lines = text.splitlines()
            if is_session_learning(lines):
                continue
            file_violations = []
            check_frontmatter(path, lines, file_violations)
            check_vocabulary(path, lines, file_violations)
            if "all" not in allows:
                violations.extend(v for v in file_violations if v.rule not in allows)
    return violations


def print_rules():
    for rule_id in sorted(ALL_RULES):
        print(f"{rule_id}  {ALL_RULES[rule_id]}")


def main(in_argv=None):
    parser = argparse.ArgumentParser(description="Lint Agentic Rails repositories.")
    parser.add_argument("paths", nargs="*", default=["."], help="repo roots to lint (default: cwd)")
    parser.add_argument("--skip", default="", help="comma-separated rule ids to skip")
    parser.add_argument("--only", default="", help="comma-separated rule ids to run exclusively")
    parser.add_argument("--include-archived", action="store_true",
                        help="also lint archived/ folders")
    parser.add_argument("--list-rules", action="store_true", help="list rule ids and exit")
    args = parser.parse_args(in_argv)

    if args.list_rules:
        print_rules()
        return 0

    roots = [Path(p).resolve() for p in args.paths]
    for root in roots:
        if not root.exists():
            print(f"error: path does not exist: {root}", file=sys.stderr)
            return 2

    violations = lint_paths(roots, args.include_archived)

    skipped = {r.strip().upper() for r in args.skip.split(",") if r.strip()}
    only = {r.strip().upper() for r in args.only.split(",") if r.strip()}
    if skipped:
        violations = [v for v in violations if v.rule not in skipped]
    if only:
        violations = [v for v in violations if v.rule in only]

    violations.sort(key=lambda v: (str(v.path).lower(), v.line, v.rule))
    for violation in violations:
        print(f"{violation.path}:{violation.line}: {violation.rule} {violation.message}")

    if violations:
        counts = {}
        for violation in violations:
            counts[violation.rule] = counts.get(violation.rule, 0) + 1
        summary = ", ".join(f"{rule}={count}" for rule, count in sorted(counts.items()))
        affected_files = len({violation.path for violation in violations})
        print(f"\n{len(violations)} violation(s) in {affected_files} file(s): {summary}")
        return 1

    print("clean: no violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
