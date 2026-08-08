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
# `proposals` holds verbatim slices copied from foreign projects (see the
# rails-new-proposal skill); linting them would force mutating the evidence.
EXCLUDED_DIRS = {
    ".git", "node_modules", "__pycache__", ".vs", ".idea",
    ".claude", ".cursor", ".agents", "ide_specific", "_planning-runs",
    "proposals",
}

# Files that should never be committed to a rails repo (HY001).
JUNK_FILES = {"desktop.ini", "thumbs.db", "debug.log"}

# Files allowed to state the canonical numbered tier table (VC005 exemption).
CANONICAL_TIER_FILES = {"design.md", "agenticworkflow.md"}

KEBAB_CASE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PRAGMA = re.compile(r"<!--\s*rails-lint-allow:\s*([A-Za-z0-9 ,]+?)\s*-->")
MAX_DESCRIPTION_CHARS = 1024

# Skill-authoring standard (context/wiki/skill-authoring-standard.md).
MAX_SKILL_LINES = 500
MIN_DUPLICATED_BLOCK_LINES = 4

# A heading whose only job is to ask the agent that just did the work
# whether it did the work (standard, section 4).
SELF_EVAL_HEADING = re.compile(
    r"^#{2,}\s+(validation|self[- ]check|self[- ]validation|self[- ]assessment)\s*$",
    re.IGNORECASE)

# A filesystem path addressing a markdown file inside another skill's bundle.
# Deployed skills live in the agent's configuration directory, not the target
# repo a worker runs in, so such a path resolves from neither (standard,
# section 6). Requiring the .md target keeps prose like "(skills/agents/rules)"
# out of the match.
CROSS_SKILL_PATH = re.compile(r"skills/[a-z0-9]+(?:-[a-z0-9]+)*/[^\s`)\"']*\.md")

# Markdown inline links, excluding external schemes and pure anchors.
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# A compaction-survival statement needs both stems to count (standard, section 7).
COMPACTION_STEMS = ("surviv", "compact")

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
    "FM007": "rules file 'paths:' entry is not a quoted glob string",
    "ST001": "skill folder is missing SKILL.md",
    "ST002": "agent folder is missing AGENT.md",
    "ST003": "verifier folder is missing README.md",
    "NM001": "skill/agent/verifier folder name is not kebab-case",
    "NM002": "agent folder name must end in -persona",
    "HY001": "junk file committed (Desktop.ini, Thumbs.db, debug.log)",
    "AR001": "body uses $ARGUMENTS but frontmatter has no 'argument-hint'",
    "AR002": "'argument-hint' present but body has no '## Arguments' section or no $ARGUMENTS",
    "AR003": "frontmatter 'argument-hint' is not a quoted string",
    "DS001": "frontmatter 'description' does not begin with 'Use'",
    "WF001": "-workflow skill has no compaction-survival statement",
    "WF002": "-workflow skill has no 'argument-hint'",
    "RF001": "relative link target does not exist",
    "RF002": "reference file is not linked from anywhere in its skill",
    "PT001": "cross-skill filesystem path - invoke skills by name instead",
    "SE001": "self-evaluation section - state observable acceptance or dispatch a verifier",
    "DP001": "fenced block duplicated from this skill's own references",
    "LN001": f"SKILL.md exceeds {MAX_SKILL_LINES} lines",
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
    """Parse top-level keys, the metadata block, and the paths list from
    frontmatter lines.

    Returns (fields, metadata, paths_items). fields and metadata map
    key -> (raw_value, 0-based line offset within the frontmatter block).
    paths_items is a list of (raw_value, offset) for each '- ...' entry
    under a top-level 'paths:' key (the Claude Code rules-file shape).
    """
    fields = {}
    metadata = {}
    paths_items = []
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
        elif current_top_key == "paths":
            list_match = re.match(r"^\s*-\s*(.+)$", line)
            if list_match:
                paths_items.append((list_match.group(1).strip(), offset))
    return fields, metadata, paths_items


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


def is_in_rules_dir(in_path: Path):
    """True for a file whose parent folder is 'rules' directly under source/ or archived/.

    Rules files follow Claude Code's frontmatter shape (an optional
    top-level 'paths:' list, or no frontmatter at all), not this repo's
    general name/description/metadata.version standard.
    """
    parent = in_path.parent
    return parent.name == "rules" and parent.parent.name in ("source", "archived")


def is_session_learning(in_lines):
    """True for memory-rail learning captures, which use their own schema.

    Learning files are historical session records written by the
    rails-memory-learnings skill; they are exempt from artifact frontmatter
    rules and from vocabulary rewrites (history must not be falsified).
    """
    fm_lines, _ = split_frontmatter(in_lines)
    if fm_lines is None:
        return False
    fields, _, _ = parse_frontmatter(fm_lines)
    entry = fields.get("type")
    return entry is not None and entry[0] == "session-learning"


def check_frontmatter(in_path: Path, in_lines, out_violations):
    """Run FM001-FM007 for one markdown file."""
    fm_lines, body_start = split_frontmatter(in_lines)
    is_artifact = in_path.name in ("SKILL.md", "AGENT.md")

    if fm_lines is None:
        if body_start == -1:
            out_violations.append(Violation(in_path, 1, "FM001", "unterminated frontmatter block"))
        elif is_artifact:
            out_violations.append(Violation(in_path, 1, "FM001", "missing frontmatter block"))
        return

    fields, metadata, paths_items = parse_frontmatter(fm_lines)

    # Line numbers inside the block are offset by the opening '---' line.
    def line_of(in_offset):
        return in_offset + 2

    # Rules files (source/rules/, archived/rules/) follow Claude Code's
    # 'paths:' shape or carry no frontmatter at all — either way they
    # deliberately carry no 'name', 'description', or 'metadata.version'.
    is_rules_file = is_in_rules_dir(in_path)

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
        if not is_rules_file:
            out_violations.append(Violation(
                in_path, 1, "FM005", "frontmatter has no 'metadata.version' key"))
    else:
        version_value, version_offset = version_entry
        if not re.match(r"^([\"']).+\1$", version_value):
            out_violations.append(Violation(
                in_path, line_of(version_offset), "FM005",
                f"metadata.version {version_value or '(empty)'} must be a quoted string"))

    if is_rules_file:
        for path_value, path_offset in paths_items:
            if not re.match(r"^([\"']).+\1$", path_value):
                out_violations.append(Violation(
                    in_path, line_of(path_offset), "FM007",
                    f"paths entry {path_value or '(empty)'} must be a quoted glob string"))

    if is_under_tooling_source(in_path):
        for banned_key in BANNED_TOOLING_KEYS:
            for source, entry in (("", fields.get(banned_key)), ("metadata.", metadata.get(banned_key))):
                if entry is not None:
                    out_violations.append(Violation(
                        in_path, line_of(entry[1]), "FM006",
                        f"banned key '{source}{banned_key}' in tooling repo frontmatter"))


def is_skill_file(in_path: Path):
    """True for a SKILL.md inside a skills/ bundle folder."""
    return in_path.name == "SKILL.md" and in_path.parent.parent.name == "skills"


def check_skill_conventions(in_path: Path, in_lines, out_violations):
    """Run AR001-AR003, DS001, WF001-WF002, SE001, LN001 for one SKILL.md.

    These enforce the mechanical half of the skill-authoring standard. The
    semantic half - whether a skill really takes parameters, whether its
    acceptance criteria are falsifiable - is not decidable here and is
    reviewed by quality-gate-persona instead.
    """
    if not is_skill_file(in_path):
        return

    fm_lines, body_start = split_frontmatter(in_lines)
    if fm_lines is None:
        return
    fields, _metadata, _paths = parse_frontmatter(fm_lines)
    body = "\n".join(in_lines[body_start:])

    hint_entry = fields.get("argument-hint")
    uses_arguments_token = "$ARGUMENTS" in body

    if hint_entry is None:
        if uses_arguments_token:
            out_violations.append(Violation(
                in_path, 1, "AR001", "body uses $ARGUMENTS but no argument-hint is declared"))
    else:
        hint_value, hint_offset = hint_entry
        if not re.match(r"^([\"']).*\1$", hint_value):
            out_violations.append(Violation(
                in_path, hint_offset + 2, "AR003",
                f"argument-hint {hint_value or '(empty)'} must be a quoted string"))
        if not re.search(r"^#{2,}\s+Arguments\s*$", body, re.IGNORECASE | re.MULTILINE):
            out_violations.append(Violation(
                in_path, hint_offset + 2, "AR002", "no '## Arguments' section in the body"))
        elif not uses_arguments_token:
            out_violations.append(Violation(
                in_path, hint_offset + 2, "AR002", "body never references $ARGUMENTS"))

    description_entry = fields.get("description")
    if description_entry is not None:
        full_text = folded_value(fm_lines, description_entry[1], description_entry[0])
        if full_text and not full_text.lstrip().startswith("Use"):
            out_violations.append(Violation(
                in_path, description_entry[1] + 2, "DS001",
                f"description begins '{full_text.split()[0]}', not 'Use'"))

    if in_path.parent.name.endswith("-workflow"):
        lowered = body.lower()
        if not all(stem in lowered for stem in COMPACTION_STEMS):
            out_violations.append(Violation(
                in_path, 1, "WF001",
                "orchestration skills must state how a run survives compaction"))
        if hint_entry is None:
            out_violations.append(Violation(
                in_path, 1, "WF002", "orchestration skills must declare an argument-hint"))

    for line_number, line in enumerate(in_lines, start=1):
        if SELF_EVAL_HEADING.match(line.strip()):
            out_violations.append(Violation(
                in_path, line_number, "SE001", f"self-evaluation heading '{line.strip()}'"))

    if len(in_lines) > MAX_SKILL_LINES:
        out_violations.append(Violation(
            in_path, MAX_SKILL_LINES, "LN001",
            f"{len(in_lines)} lines (max {MAX_SKILL_LINES}) - look for a section that repeats another"))


def check_paths_and_links(in_path: Path, in_lines, out_violations):
    """Run PT001 and RF001 over one markdown file under a skills/ bundle."""
    if "skills" not in {parent.name for parent in in_path.parents}:
        return

    for line_number, line in enumerate(in_lines, start=1):
        for match in CROSS_SKILL_PATH.finditer(line):
            out_violations.append(Violation(
                in_path, line_number, "PT001",
                f"path '{match.group(0)}' - invoke the skill by name instead"))
        for match in MARKDOWN_LINK.finditer(line):
            target = match.group(1).split("#", 1)[0]
            if not target or re.match(r"^(https?:|mailto:|<)", target):
                continue
            # RF001 validates links within the skill bundle only. A target
            # containing a <placeholder> or escaping the folder is describing
            # target-repo content, not addressing a file that ships here.
            if "<" in target or target.startswith("../"):
                continue
            if not (in_path.parent / target).exists():
                out_violations.append(Violation(
                    in_path, line_number, "RF001", f"link target '{target}' does not exist"))


def fenced_blocks(in_text):
    """Yield each fenced code block's whitespace-normalized body."""
    for match in re.finditer(r"^```[^\n]*\n(.*?)^```", in_text, re.DOTALL | re.MULTILINE):
        lines = [line.strip() for line in match.group(1).splitlines() if line.strip()]
        if len(lines) >= MIN_DUPLICATED_BLOCK_LINES:
            yield "\n".join(lines)


def check_skill_bundle(in_skill_dir: Path, out_violations):
    """Run RF002 and DP001 across one skill folder's files.

    Both compare SKILL.md against its own references/, so neither fits the
    single-file pass. Each respects the pragma of the file it reports against.
    """
    skill_file = in_skill_dir / "SKILL.md"
    references_dir = in_skill_dir / "references"
    if not skill_file.is_file() or not references_dir.is_dir():
        return

    try:
        skill_text = skill_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    skill_allows = collect_pragma_allows(skill_text)

    sibling_texts = {}
    for path in sorted(in_skill_dir.rglob("*.md")):
        try:
            sibling_texts[path] = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

    for reference in sorted(references_dir.glob("*.md")):
        linked = any(
            reference.name in text
            for path, text in sibling_texts.items() if path != reference)
        if linked:
            continue
        allows = collect_pragma_allows(sibling_texts.get(reference, ""))
        if "all" in allows or "RF002" in allows:
            continue
        out_violations.append(Violation(
            reference, 1, "RF002", "nothing links to this reference - delete it or link it"))

    if "all" in skill_allows or "DP001" in skill_allows:
        return
    reference_blocks = set()
    for path, text in sibling_texts.items():
        if path.parent == references_dir:
            reference_blocks.update(fenced_blocks(text))
    for block in fenced_blocks(skill_text):
        if block in reference_blocks:
            first_line = block.splitlines()[0][:40]
            out_violations.append(Violation(
                skill_file, 1, "DP001",
                f"fenced block starting '{first_line}' is copied from a reference - link instead"))


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
    """Run ST/NM checks over skill, agent, and verifier bundle folders."""
    excluded = set(EXCLUDED_DIRS)
    if not in_include_archived:
        excluded.add("archived")
    for dirpath, dirnames, _filenames in os.walk(in_root):
        dirnames[:] = sorted(d for d in dirnames if d not in excluded)
        parent = Path(dirpath)
        if parent.name not in ("skills", "agents", "verifiers"):
            continue
        for child_name in dirnames:
            child = parent / child_name
            if not KEBAB_CASE.match(child_name):
                out_violations.append(Violation(
                    child, 1, "NM001", f"folder '{child_name}' is not kebab-case"))
            if parent.name == "skills":
                if not (child / "SKILL.md").is_file():
                    out_violations.append(Violation(child, 1, "ST001", "skill folder has no SKILL.md"))
                check_skill_bundle(child, out_violations)
            if parent.name == "verifiers" and not (child / "README.md").is_file():
                out_violations.append(Violation(child, 1, "ST003", "verifier folder has no README.md"))
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
            check_skill_conventions(path, lines, file_violations)
            check_paths_and_links(path, lines, file_violations)
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
