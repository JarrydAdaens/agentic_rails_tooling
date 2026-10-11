#!/usr/bin/env python3
"""Freeze verification evidence and reconcile completion without committing."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid


class ReceiptError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args, missing_ok=False, input=None):
    result = subprocess.run(["git", "-C", str(repo), "--literal-pathspecs", *args],
                            capture_output=True, input=input)
    if result.returncode and not missing_ok:
        raise ReceiptError(result.stderr.decode(errors="replace").strip())
    return None if result.returncode else result.stdout


def repository(value):
    path = Path(value).resolve()
    return Path(git(path, "rev-parse", "--show-toplevel").decode().strip()).resolve()


def relative(repo, value):
    path = Path(value)
    path = path if path.is_absolute() else repo / path
    # Resolve the parent, preserving a symlink's own identity rather than its target.
    path = path.parent.resolve() / path.name
    try:
        name = path.relative_to(repo).as_posix()
    except ValueError as error:
        raise ReceiptError(f"Path escapes repository: {value}") from error
    if name == ".git" or name.startswith(".git/"):
        raise ReceiptError("Git internals are not delivery artifacts")
    if path.is_dir():
        raise ReceiptError("Select explicit files, not directories")
    return name


def blob_identity(repo, name, data, filtered=True):
    # Without -w this applies Git's clean conversion without changing the index
    # or object database. Symlink targets and committed blobs are already literal.
    option = f"--path={name}" if filtered else "--no-filters"
    return git(repo, "hash-object", option, "--stdin", input=data).decode().strip()


def files_at(repo, paths, commit=None, include_committed=False):
    files = {}
    committed_files = {}
    for value in paths:
        name = relative(repo, value)
        if commit:
            tree = git(repo, "ls-tree", commit, "--", name)
            data = git(repo, "show", f"{commit}:{name}", missing_ok=True)
            kind = "absent" if data is None else "symlink" if tree.startswith(b"120000 ") else "file"
        else:
            path = repo / name
            kind = "symlink" if path.is_symlink() else "file" if path.is_file() else "absent"
            data = os.readlink(path).encode() if kind == "symlink" else path.read_bytes() if kind == "file" else None
        files[name] = {"kind": kind, "sha256": digest(data) if data is not None else None}
        if include_committed:
            committed_files[name] = {"kind": kind, "git_blob": blob_identity(
                repo, name, data, filtered=not commit and kind == "file") if data is not None else None}
    files = dict(sorted(files.items()))
    return (files, dict(sorted(committed_files.items()))) if include_committed else files


def identity(files):
    return digest(json.dumps(files, sort_keys=True).encode())


def capture(repo, paths, base=None, include_committed=False):
    repo = repository(repo)
    snapshot = files_at(repo, paths, include_committed=include_committed)
    files, committed_files = snapshot if include_committed else (snapshot, None)
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    base = base or head
    diff = git(repo, "diff", "--no-ext-diff", "--binary", base, "--", *files)
    result = {"head": head, "base": base, "files": files, "artifact_identity": identity(files),
              "diff_identity": digest(diff + json.dumps(files, sort_keys=True).encode())}
    if include_committed:
        result["committed_files"] = committed_files
    return result


def write_record(path, record):
    if path.is_symlink():
        raise ReceiptError("Receipt cannot be a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}-{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write((json.dumps(record, indent=2, sort_keys=True) + "\n").encode())
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def evidence_ok(evidence, expected, label):
    if evidence.get("artifact_identity") != expected:
        raise ReceiptError(f"{label} does not match checked artifact identity")
    if evidence.get("outcome") == "WAIVED":
        if not evidence.get("authority") or not evidence.get("reason"):
            raise ReceiptError(f"{label} waiver lacks authority/reason")
    elif evidence.get("outcome") != "PASS":
        raise ReceiptError(f"{label} lacks passing required evidence")


def begin(repo, record_path, paths, metadata_paths, evidence, policy="none", authority=None, owner=None):
    repo = repository(repo)
    name = relative(repo, record_path)
    output = repo / name
    if output.exists():
        raise ReceiptError("Receipt already exists; reconcile it instead of overwriting")
    if policy not in ("none", "single", "batch") or (policy != "none" and not authority):
        raise ReceiptError("Authorized commit policy requires recorded user authority")
    checked = capture(repo, paths)
    metadata = files_at(repo, metadata_paths)
    if name in checked["files"] or name in metadata or set(metadata) & set(checked["files"]):
        raise ReceiptError("Checked artifacts, completion metadata, and receipt must be disjoint")
    if not checked["files"] or not evidence.get("checks"):
        raise ReceiptError("Explicit checked artifacts and check evidence are required")
    for check in evidence["checks"]:
        if not check.get("command"):
            raise ReceiptError("Check evidence must name the actual command")
        evidence_ok(check, checked["artifact_identity"], "Check")
    review = evidence.get("review")
    if evidence.get("review_required") and not review:
        raise ReceiptError("Required review evidence is missing")
    if review:
        evidence_ok(review, checked["artifact_identity"], "Review")
    record = {"schema_version": 1, "transaction_id": uuid.uuid4().hex, "phase": "PREPARING",
              "repo": str(repo), "record": name, "checked": checked, "metadata_before": metadata,
              "evidence": evidence, "commit_policy": policy, "commit_authority": authority,
              "status_owner": owner, "decisions": evidence.get("decisions", [])}
    write_record(output, record)
    return record


def load(repo, record_path):
    repo = repository(repo)
    name = relative(repo, record_path)
    path = repo / name
    if path.is_symlink():
        raise ReceiptError("Receipt cannot be a symlink")
    try:
        record = json.loads(path.read_bytes())
        if record["schema_version"] != 1 or record["repo"] != str(repo) or record["record"] != name:
            raise ReceiptError("Receipt schema/repository identity mismatch")
        if record["phase"] not in ("PREPARING", "READY", "VERIFIED_UNCOMMITTED"):
            raise ReceiptError("Unknown completion phase")
        if record["commit_policy"] not in ("none", "single", "batch"):
            raise ReceiptError("Unknown commit policy")
        for item in (record["checked"]["files"], record["metadata_before"]):
            for item_name in item:
                relative(repo, item_name)
        return repo, path, record
    except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReceiptError(f"Malformed completion receipt: {error}") from error


def seal(repo, record_path):
    repo, path, record = load(repo, record_path)
    if record["phase"] != "PREPARING":
        raise ReceiptError("Receipt already sealed; reconcile instead of rewriting")
    checked = capture(repo, record["checked"]["files"], record["checked"]["base"])
    if checked["artifact_identity"] != record["checked"]["artifact_identity"]:
        raise ReceiptError("Checked content/configuration changed; renew affected evidence")
    delivery_paths = list(checked["files"]) + list(record["metadata_before"])
    delivery = capture(repo, delivery_paths, checked["base"], include_committed=True)
    final_checked = {name: delivery["files"][name] for name in record["checked"]["files"]}
    if identity(final_checked) != record["checked"]["artifact_identity"]:
        raise ReceiptError("Checked content/configuration changed; renew affected evidence")
    record["delivery"] = delivery
    record["phase"] = "VERIFIED_UNCOMMITTED" if record["commit_policy"] == "none" else "READY"
    write_record(path, record)
    return record


def reconcile(repo, record_path):
    repo, path, record = load(repo, record_path)
    checked_now = capture(repo, record["checked"]["files"], record["checked"]["base"])
    if record["phase"] == "PREPARING":
        return {"state": "PREPARING", "checked_matches": checked_now["artifact_identity"] ==
                record["checked"]["artifact_identity"], "next": "finish metadata and seal, or renew changed checks"}
    delivery = record["delivery"]
    current = capture(repo, delivery["files"], delivery["base"])
    matches = current["artifact_identity"] == delivery["artifact_identity"]
    if record["commit_policy"] == "none":
        return {"state": "VERIFIED_UNCOMMITTED" if matches else "CHANGED_REQUIRES_CHECKS",
                "current_matches": matches, "diff_identity": delivery["diff_identity"]}
    raw = path.read_bytes()
    receipt_blob = blob_identity(repo, record["record"], raw)
    commits = git(repo, "log", "--format=%H", "HEAD", "--", record["record"]).decode().splitlines()
    for commit in commits:
        committed_receipt = git(repo, "show", f"{commit}:{record['record']}", missing_ok=True)
        if committed_receipt is None or blob_identity(
                repo, record["record"], committed_receipt, filtered=False) != receipt_blob:
            continue
        committed_matches = (files_at(repo, delivery["files"], commit, include_committed=True)[1] ==
                             delivery["committed_files"]) if "committed_files" in delivery else (
                             files_at(repo, delivery["files"], commit) == delivery["files"])
        if committed_matches:
            return {"state": "COMPLETED_COMMITTED", "commit": commit, "current_matches": matches,
                    "next": "delivery only if the external status owner is still pending"}
    return {"state": "COMMIT_PENDING" if matches else "CHANGED_REQUIRES_CHECKS", "current_matches": matches,
            "next": "finish only the authorized completion commit; do not repeat implementation"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("capture", "begin", "seal", "reconcile"))
    parser.add_argument("--repo", required=True)
    parser.add_argument("--record")
    parser.add_argument("--paths", nargs="+", default=[])
    parser.add_argument("--metadata", nargs="*", default=[])
    parser.add_argument("--evidence")
    parser.add_argument("--policy", choices=("none", "single", "batch"), default="none")
    parser.add_argument("--authority")
    parser.add_argument("--owner")
    args = parser.parse_args()
    try:
        if args.command == "capture":
            result = capture(args.repo, args.paths)
        elif not args.record:
            raise ReceiptError("Explicit --record is required")
        elif args.command == "begin":
            if not args.evidence:
                raise ReceiptError("Explicit --evidence JSON is required")
            evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
            result = begin(args.repo, args.record, args.paths, args.metadata, evidence,
                           args.policy, args.authority, args.owner)
        elif args.command == "seal":
            result = seal(args.repo, args.record)
        else:
            result = reconcile(args.repo, args.record)
        print(json.dumps(result, indent=2))
        return 0
    except (ReceiptError, OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"execution-receipt: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
