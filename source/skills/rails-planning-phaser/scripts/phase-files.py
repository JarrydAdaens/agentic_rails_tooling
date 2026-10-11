#!/usr/bin/env python3
"""Byte-preserving, recoverable replacement of a plan and its phase files."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid

PHASE = re.compile(r"phase-([1-9][0-9]*)\.md$")
STATE = "phasing-state.json"
HISTORY = "phasing-history"
CARD = "cer-score-card.md"


class PhaseError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def bytes_at(path):
    if path.is_symlink():
        raise PhaseError(f"Refusing symlink: {path}")
    if path.exists() and not path.is_file():
        raise PhaseError(f"Expected a file: {path}")
    return path.read_bytes() if path.exists() else None


def atomic_write(path, data):
    temporary = path.with_name(f".{path.name}-{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_json(path, value):
    atomic_write(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())


def plan_path(value):
    path = Path(value).absolute()
    bytes_at(path)
    if not path.is_file():
        raise PhaseError(f"Plan does not exist: {path}")
    if PHASE.fullmatch(path.name) or path.name == CARD:
        raise PhaseError("Target must be a plan, not an output phase or scorecard")
    return path.resolve()


def current_files(plan):
    names = [plan.name] + sorted(p.name for p in plan.parent.iterdir() if PHASE.fullmatch(p.name))
    if (plan.parent / CARD).exists():
        names.append(CARD)
    return {name: bytes_at(plan.parent / name) for name in names}


def fingerprint(files):
    return digest(json.dumps({name: digest(data) for name, data in files.items()}, sort_keys=True).encode())


def journal_for(plan):
    pointer = bytes_at(plan.parent / STATE)
    if pointer is None:
        return None, None
    try:
        state = json.loads(pointer)
        if state["schema_version"] != 1:
            raise PhaseError("Unsupported recovery pointer schema")
        run_id = state["run_id"]
        if not re.fullmatch(r"run-[a-f0-9]{32}", run_id):
            raise PhaseError("Invalid history run identity")
        history = plan.parent / HISTORY
        run = history / run_id
        if history.is_symlink() or run.is_symlink():
            raise PhaseError("Refusing symlinked phasing history")
        for folder in (run / "original", run / "staged"):
            if folder.is_symlink() or not folder.is_dir():
                raise PhaseError("Missing or symlinked recovery content directory")
        journal = json.loads(bytes_at(run / "transaction.json"))
        if journal["schema_version"] != 1 or journal["plan"] != str(plan):
            raise PhaseError("Recovery state belongs to another plan or schema")
        if journal["status"] not in ("PREPARED", "APPLYING", "COMMITTED", "ROLLED_BACK") or \
           not isinstance(journal["operations"], dict):
            raise PhaseError("Invalid recovery status or operations")
        for name, record in journal["operations"].items():
            if name != plan.name and name != CARD and not PHASE.fullmatch(name):
                raise PhaseError("Unsafe artifact path in recovery state")
            if not isinstance(record, dict) or set(record) != {"before", "after"}:
                raise PhaseError("Malformed recovery digest record")
        return run, journal
    except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PhaseError(f"Malformed recovery state: {error}") from error


def inspect(plan):
    plan = plan_path(plan)
    files = current_files(plan)
    run, journal = journal_for(plan)
    return {"plan": str(plan), "fingerprint": fingerprint(files), "source_files": list(files),
            "phased": any(PHASE.fullmatch(name) for name in files) or
            bool(re.search(rb"^##\s+Phase Registry\s*$", files[plan.name], re.I | re.M)),
            "pending_recovery": bool(journal and journal["status"] not in ("COMMITTED", "ROLLED_BACK")),
            "history": str(run) if run else None, "status": journal["status"] if journal else None}


def drafts_at(directory, scorecard=False):
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise PhaseError("Drafts must be a real directory")
    drafts = {}
    for path in directory.iterdir():
        if path.name != "plan.md" and not PHASE.fullmatch(path.name) and not (scorecard and path.name == CARD):
            raise PhaseError(f"Unexpected draft artifact: {path.name}")
        drafts[path.name] = bytes_at(path)
    if "plan.md" not in drafts or (scorecard and CARD not in drafts):
        raise PhaseError("Draft manifest or explicitly requested scorecard is missing")
    numbers = sorted(int(PHASE.fullmatch(name)[1]) for name in drafts if PHASE.fullmatch(name))
    if numbers != list(range(1, len(numbers) + 1)):
        raise PhaseError("Draft phases must have contiguous numbering starting at 1")
    return drafts


def proposal(plan, drafts, scorecard=False):
    plan = plan_path(plan)
    state = inspect(plan)
    staged = drafts_at(drafts, scorecard)
    if Path(drafts).resolve().is_relative_to(plan.parent):
        raise PhaseError("Stage drafts outside the target plan folder")
    outputs = {plan.name if name == "plan.md" else name: data for name, data in staged.items()}
    names = {plan.name} | {name for name in state["source_files"] if PHASE.fullmatch(name)} | set(outputs)
    operations = {name: outputs.get(name) for name in sorted(names)}
    return plan, state, operations


def preview(plan, drafts, scorecard=False):
    plan, state, operations = proposal(plan, drafts, scorecard)
    return {**state, "replacement_requires_rephase": state["phased"], "changes": [
        {"file": name, "before_sha256": digest(old) if (old := bytes_at(plan.parent / name)) is not None else None,
         "after_sha256": digest(data) if data is not None else None,
         "action": "delete" if data is None else "replace" if old is not None else "create"}
        for name, data in operations.items()]}


def apply(plan, drafts, expected, rephase=False, scorecard=False, after_write=None):
    plan, state, operations = proposal(plan, drafts, scorecard)
    if state["pending_recovery"]:
        raise PhaseError("Interrupted replacement requires recovery before another apply")
    if state["phased"] and not rephase:
        raise PhaseError("Already phased; replacement requires --rephase")
    if state["fingerprint"] != expected:
        raise PhaseError("Source changed after inspection; preserve current edits and inspect again")
    originals = current_files(plan)
    history = plan.parent / HISTORY
    if history.is_symlink():
        raise PhaseError("Refusing symlinked history directory")
    history.mkdir(exist_ok=True)
    run_id = f"run-{uuid.uuid4().hex}"
    run = history / run_id
    (run / "original").mkdir(parents=True)
    (run / "staged").mkdir()
    for name, data in originals.items():
        atomic_write(run / "original" / name, data)
    records = {}
    for name, data in operations.items():
        if data is not None:
            atomic_write(run / "staged" / name, data)
        records[name] = {"before": digest(originals[name]) if name in originals else None,
                         "after": digest(data) if data is not None else None}
    journal = {"schema_version": 1, "plan": str(plan), "source_fingerprint": expected,
               "status": "PREPARED", "operations": records}
    write_json(run / "transaction.json", journal)
    write_json(plan.parent / STATE, {"schema_version": 1, "run_id": run_id})
    if fingerprint(current_files(plan)) != expected:
        raise PhaseError("Source changed during staging; recovery state retained")
    journal["status"] = "APPLYING"
    write_json(run / "transaction.json", journal)
    for name, data in operations.items():
        current = bytes_at(plan.parent / name)
        if (digest(current) if current is not None else None) != records[name]["before"]:
            raise PhaseError(f"Concurrent edit to {name}; recovery state retained")
        if data is None:
            if (plan.parent / name).exists():
                (plan.parent / name).unlink()
        else:
            atomic_write(plan.parent / name, data)
        if after_write:
            after_write(name)
    journal["status"] = "COMMITTED"
    write_json(run / "transaction.json", journal)
    return {"status": "COMMITTED", "history": str(run), "original": str(run / "original" / plan.name),
            "files": sorted(name for name, data in operations.items() if data is not None)}


def recover(plan, dry_run=False):
    plan = plan_path(plan)
    run, journal = journal_for(plan)
    if journal is None or journal["status"] in ("COMMITTED", "ROLLED_BACK"):
        raise PhaseError("No interrupted replacement to recover")
    originals = {}
    for name, record in journal["operations"].items():
        if name != plan.name and name != CARD and not PHASE.fullmatch(name):
            raise PhaseError("Unsafe artifact path in recovery state")
        live = bytes_at(plan.parent / name)
        if (digest(live) if live is not None else None) not in (record["before"], record["after"]):
            raise PhaseError(f"Concurrent edits to {name}; recovery refuses to overwrite them")
        original = bytes_at(run / "original" / name)
        staged = bytes_at(run / "staged" / name)
        if (digest(original) if original is not None else None) != record["before"] or \
           (digest(staged) if staged is not None else None) != record["after"]:
            raise PhaseError(f"Backup or staged digest mismatch for {name}")
        originals[name] = original
    if dry_run:
        return {"status": "RECOVERY_PREVIEW", "history": str(run), "files": sorted(originals)}
    for name, original in originals.items():
        live = bytes_at(plan.parent / name)
        record = journal["operations"][name]
        if (digest(live) if live is not None else None) not in (record["before"], record["after"]):
            raise PhaseError(f"Concurrent edits to {name} during recovery; current bytes preserved")
        if original is None:
            if (plan.parent / name).exists():
                (plan.parent / name).unlink()
        else:
            atomic_write(plan.parent / name, original)
    journal["status"] = "ROLLED_BACK"
    write_json(run / "transaction.json", journal)
    return {"status": "ROLLED_BACK", "history": str(run)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inspect", "preview", "apply", "recover"))
    parser.add_argument("--plan", required=True)
    parser.add_argument("--drafts")
    parser.add_argument("--expected")
    parser.add_argument("--rephase", action="store_true")
    parser.add_argument("--scorecard", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            result = inspect(args.plan)
        elif args.command == "recover":
            result = recover(args.plan, args.dry_run)
        else:
            if not args.drafts:
                raise PhaseError("--drafts is required for preview/apply")
            if args.command == "preview" or args.dry_run:
                result = preview(args.plan, args.drafts, args.scorecard)
            else:
                if not args.expected:
                    raise PhaseError("Apply requires the inspected --expected fingerprint")
                result = apply(args.plan, args.drafts, args.expected, args.rephase, args.scorecard)
        print(json.dumps(result, indent=2))
        return 0
    except (PhaseError, OSError) as error:
        print(f"phase-files: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
