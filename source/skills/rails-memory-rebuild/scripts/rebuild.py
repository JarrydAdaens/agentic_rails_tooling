"""Optional Rails memory import/rebuild. New records use JSON inside Markdown.

Only legacy YAML import needs PyYAML (pip install PyYAML). Existing observations
and unmanaged resumes are never overwritten. No curation or routing is performed.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import tempfile

SCHEMA = 1
MANAGED = "<!-- generated-by: rails-memory-rebuild/v1 -->"
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BLOCK = re.compile(r"<!-- rails-observation -->\s*```json\s*\n(.*?)\n```", re.S)
OUTCOMES = {"succeeded", "partial", "failed", "blocked", "unknown"}
UNMEASURED_SOURCES = {"unknown", "none", "null", "unavailable", "unmeasured", "not recorded",
                      "not-recorded", "n/a", "na", "estimate", "estimated", "guess", "guessed"}


def digest(data):
    return sha256(data).hexdigest()


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def encode(record):
    return json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False)


def validate(record):
    if not isinstance(record, dict):
        raise ValueError("observation must be an object")
    if type(record.get("schema_version")) is not int or record.get("schema_version") != SCHEMA:
        raise ValueError("unsupported observation schema")
    for key in ("observation_id", "result_id"):
        if not isinstance(record.get(key), str) or not ID.fullmatch(record[key]):
            raise ValueError(f"invalid {key}")
    for key in ("project", "task", "date", "outcome"):
        if not isinstance(record.get(key), str) or not record[key]:
            raise ValueError(f"missing {key}; use unknown explicitly")
    if record["outcome"] not in OUTCOMES:
        raise ValueError("invalid outcome")
    if not isinstance(record.get("evidence"), list) or not record["evidence"]:
        raise ValueError("evidence must include a source or explicit unknown")
    if not isinstance(record.get("participants"), list) or not record["participants"]:
        raise ValueError("participants must include a role")
    for participant in record["participants"]:
        if not isinstance(participant, dict):
            raise ValueError("participant must be an object")
        for key in ("role", "persona", "requested_model", "observed_model", "identity_source"):
            if not isinstance(participant.get(key), str) or not participant[key]:
                raise ValueError(f"participant missing {key}")
        if participant["observed_model"] != "unknown" and participant["identity_source"] == "unknown":
            raise ValueError("observed model needs identity evidence")
    telemetry = record.get("telemetry", {})
    if not isinstance(telemetry, dict):
        raise ValueError("telemetry must be an object")
    if telemetry.get("availability") not in {"available", "partial", "unavailable", "unknown"}:
        raise ValueError("invalid telemetry availability")
    for key in ("coverage", "source", "tokens"):
        if key not in telemetry:
            raise ValueError(f"telemetry missing {key}")
    tokens = telemetry["tokens"]
    if tokens != "unknown" and (type(tokens) is not int or tokens < 0):
        raise ValueError("tokens must be measured integer or unknown")
    source = telemetry["source"]
    valid_source = (isinstance(source, str) and bool(source.strip())
                    and source.strip().casefold() not in UNMEASURED_SOURCES)
    if tokens != "unknown" and (telemetry["availability"] != "available"
                                or telemetry["coverage"] != "result" or not valid_source):
        raise ValueError("numeric tokens require available result-level measured evidence with valid source")
    if not isinstance(record.get("interpretations"), list) or any(not isinstance(note, str) for note in record["interpretations"]):
        raise ValueError("interpretations must be separate from observations")
    return record


def read_record(path):
    match = BLOCK.search(path.read_text(encoding="utf-8-sig"))
    if not match:
        raise ValueError(f"missing observation block: {path}")
    return validate(json.loads(match.group(1)))


def observation_text(record, legacy_bytes=None):
    text = (f'---\nname: {record["observation_id"]}\ndescription: Immutable memory observation.\nmetadata:\n  version: "1.0"\ntype: memory-observation\nschema_version: "1"\n'
            f'observation_id: {record["observation_id"]}\n---\n\n'
            f'# Observation: {record["observation_id"]}\n\n'
            f'<!-- rails-observation -->\n```json\n{encode(record)}\n```\n')
    if legacy_bytes is not None:
        # Base64 preserves exact original bytes, including CRLF and Unicode.
        import base64
        text += '\n## Legacy source bytes\n\n```base64\n' + base64.b64encode(legacy_bytes).decode() + '\n```\n'
    return text


def learning_paths(root):
    return sorted((root / "memories/learnings").rglob("*.md"))


def legacy_record(path):
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    if not text.startswith("---"):
        return None
    front = text.split("---", 2)[1]
    if not re.search(r"^type:\s*session-learning\s*$", front, re.M):
        return None
    try:
        import yaml
    except ImportError as error:
        raise ValueError("legacy import requires PyYAML; no files were replaced") from error
    try:
        data = yaml.safe_load(front)
    except yaml.YAMLError as error:
        raise ValueError(f"malformed legacy YAML: {path}") from error
    if not isinstance(data, dict) or not isinstance(data.get("models_used") or [], list):
        raise ValueError(f"malformed legacy fields: {path}")
    fingerprint = digest(raw)
    session = str(data.get("session_id", "unknown"))
    # Legacy task identity is only as strong as the old session record. Date and
    # project distinguish reused placeholder session IDs. Keep this limitation.
    result_basis = (str(data.get("project", "unknown")), str(data.get("date", "unknown")), session)
    result = fingerprint if session in {"unknown", "None", ""} else digest(json.dumps(result_basis).encode())
    participants = []
    for model in data.get("models_used") or []:
        if isinstance(model, str):
            model = {"name": model}
        if not isinstance(model, dict):
            raise ValueError(f"malformed legacy model: {path}")
        participants.append({"role": str(model.get("role") or "unknown"), "persona": "unknown",
                             "requested_model": str(model.get("requested_name") or "unknown"),
                             "observed_model": "unknown", "identity_source": "unknown",
                             "reported_model": str(model.get("name") or "unknown")})
    if not participants:
        participants = [{"role": "unknown", "persona": "unknown", "requested_model": "unknown",
                         "observed_model": "unknown", "identity_source": "unknown"}]
    outcome = str(data.get("outcome", "unknown"))
    if outcome not in OUTCOMES:
        outcome = "unknown"
    record = {"schema_version": SCHEMA, "observation_id": "legacy-" + fingerprint,
              "result_id": "legacy-result-" + result, "project": str(data.get("project") or "unknown"),
              "date": str(data.get("date") or "unknown"), "task": str(data.get("session_scope") or "unknown"),
              "outcome": outcome, "participants": participants,
              "evidence": [{"kind": "legacy-report", "sha256": fingerprint}],
              "telemetry": {"availability": "unknown", "coverage": "unknown", "source": "unknown", "tokens": "unknown"},
              "interpretations": [], "legacy_source_sha256": fingerprint,
              "legacy_limits": "Historical claims retained; runtime identities and usage unverified. Shared result identity inferred from project/date/session; distinct attempts need new result IDs."}
    return validate(record), raw


def materialize(root, migrate=False, dry_run=False, expected=None):
    """Freeze records into stable locations; never mutate the source learning."""
    candidates = {}
    for path in learning_paths(root):
        if BLOCK.search(path.read_text(encoding="utf-8-sig")):
            record, raw = read_record(path), None
        elif migrate:
            legacy = legacy_record(path)
            if legacy is None:
                continue
            record, raw = legacy
        else:
            # A quantitative rebuild must not silently drop old observations.
            front = path.read_text(encoding="utf-8-sig").split("---", 2)
            if len(front) > 2 and re.search(r"^type:\s*session-learning\s*$", front[1], re.M):
                frozen = root / "memories/observations" / ("legacy-" + digest(path.read_bytes()) + ".md")
                if frozen.is_file():
                    continue
                raise ValueError("unmigrated legacy learning; use --migrate-legacy for complete coverage")
            continue
        identity = record["observation_id"]
        if identity in candidates and candidates[identity][0] != record:
            raise ValueError(f"conflicting observation identity: {identity}")
        candidates[identity] = (record, raw)
    observations = root / "memories/observations"
    for path in sorted(observations.glob("*.md")):
        if path.name.startswith("README"):
            continue
        record = read_record(path)
        identity = record["observation_id"]
        if path.name != identity + ".md":
            raise ValueError("observation filename must match stable identity")
        if identity in candidates and candidates[identity][0] != record:
            raise ValueError(f"immutable observation changed: {identity}")
        candidates.setdefault(identity, (record, None))
    selected = [item[0] for _, item in sorted(candidates.items())]
    if expected is not None and selected != expected:
        raise ValueError("observation corpus changed during rebuild; rerun")
    # All conflicts are checked before creating any observations.
    if not dry_run:
        observations.mkdir(parents=True, exist_ok=True)
        for identity, (record, raw) in sorted(candidates.items()):
            target = observations / (identity + ".md")
            if not target.exists():
                with target.open("x", encoding="utf-8", newline="\n") as handle:
                    handle.write(observation_text(record, raw))
    return selected


def unique_results(records):
    results = {}
    measurements = defaultdict(set)
    for record in records:
        key = record["result_id"]
        if key in results:
            previous = results[key]
            if any(previous[field] != record[field] for field in ("outcome", "project", "task", "date")):
                raise ValueError(f"conflicting shared result: {key}")
        tokens = record["telemetry"]["tokens"]
        if tokens != "unknown":
            measurements[key].add(tokens)
            if len(measurements[key]) > 1:
                raise ValueError(f"conflicting shared-result telemetry: {key}")
        results[key] = record
    return results


def metrics(records):
    results = unique_results(records)
    counts = Counter(record["outcome"] for record in results.values())
    # Exactly one measured receipt per shared result, regardless of participants.
    measurements = {}
    for record in records:
        tokens = record["telemetry"]["tokens"]
        if tokens != "unknown":
            measurements[record["result_id"]] = tokens
    return results, counts, measurements


def citation(root, output, record):
    path = root / "memories/observations" / (record["observation_id"] + ".md")
    return f'[{record["observation_id"]}]({Path(os.path.relpath(path, output)).as_posix()})'


def render_resume(root, target, identity, records, roles, golden_ids):
    results, counts, measured = metrics(records)
    lines = [MANAGED, f'# Resume: {identity}', '', '## Snapshot', '',
             f'- Unique shared results: {len(results)}', f'- Observation records: {len(records)}',
             '- Outcome scope: shared task result; contribution attribution is unknown.',
             '- Routing: uncalibrated; no inferred model ranking or effort threshold.', '',
             '## Empirical Metrics', '', '| Outcome | Unique results |', '| --- | --- |']
    lines += [f'| {outcome} | {counts[outcome]} |' for outcome in sorted(OUTCOMES)]
    lines += ['', f'Measured result-level tokens: {sum(measured.values()) if measured else "unknown"}; '
              f'coverage {len(measured)}/{len(results)} results. Shared costs are not attributed to individual agents.',
              '', '## Roles and Tasks', '', '| Role | Unique results |', '| --- | --- |']
    lines += [f'| {role.replace(chr(124), chr(47))} | {len(ids)} |' for role, ids in sorted(roles.items())]
    lines += ['', '## Selected Qualitative Guidance', '',
              'Golden selection affects this section only. Interpretations below are reported advice, not measured capability.']
    for record in records:
        if record["observation_id"] in golden_ids:
            lines += [f'- {note} ({citation(root, target.parent, record)})' for note in record["interpretations"]]
    lines += ['', '## Source Observations', '']
    for record in records:
        lines.append(f'- {citation(root, target.parent, record)} — result `{record["result_id"]}`')
    return generated_header("resume-" + target.stem) + '\n'.join(lines) + '\n'


def generated_header(name):
    return f'---\nname: {name}\ndescription: Deterministic memory evidence summary.\nmetadata:\n  version: "1.0"\n---\n\n'


def is_managed(text):
    return MANAGED in text.split('\n')[:10]


def rebuild(root, migrate=False, dry_run=False):
    root = Path(root).resolve()
    if not (root / "memories/learnings").is_dir():
        raise ValueError("memory root must contain memories/learnings")
    records = materialize(root, migrate, dry_run=True)
    results, counts, measurements = metrics(records)
    golden_ids = set()
    for path in (root / "memories/learnings/golden").glob("*.md"):
        if BLOCK.search(path.read_text(encoding="utf-8-sig")):
            golden_ids.add(read_record(path)["observation_id"])
        elif migrate:
            legacy = legacy_record(path)
            if legacy:
                golden_ids.add(legacy[0]["observation_id"])
    groups, roles = defaultdict(dict), defaultdict(lambda: defaultdict(set))
    for record in records:
        for participant in record["participants"]:
            keys = [("model", participant["observed_model"])]
            if participant["persona"] != "unknown":
                keys.append(("agent", participant["persona"]))
            for kind, identity in keys:
                # Hash avoids collisions between model identifiers with punctuation.
                key = (kind, identity)
                groups[key][record["observation_id"]] = record
                roles[key][participant["role"]].add(record["result_id"])
    output = root / "memories/resumes-rebuilt"
    targets = {}
    for key, sources in sorted(groups.items()):
        kind, identity = key
        filename = slug(identity) + '-' + digest(identity.encode())[:12] + '.md'
        target = output / (kind + 's') / filename
        targets[target] = render_resume(root, target, identity, list(sources.values()), roles[key], golden_ids)
    verified_results = {record["result_id"] for record in records
                        if any(p["observed_model"] != "unknown" for p in record["participants"])}
    summary = (generated_header("rebuild-summary") + f'{MANAGED}\n# Rebuild Summary\n\n'
               f'Observation schema: {SCHEMA}\n\nRecords: {len(records)}; unique shared results: {len(results)}.\n\n'
               f'Outcomes: {json.dumps(dict(sorted(counts.items())))}\n\n'
               f'Measured result-level token sum: {sum(measurements.values()) if measurements else "unknown"}; '
               f'coverage {len(measurements)}/{len(results)}.\n\n'
               f'Runtime-verified model identity coverage: {len(verified_results)}/{len(results)} shared results.\n\n'
               'Group counts overlap; never sum model/persona counts or costs to obtain global totals.\n'
               'Runtime identity unknown is excluded from claims about verified model performance.\n')
    summary += '\n## Current Outputs\n\n'
    for target in sorted(targets):
        summary += f'- [{target.stem}]({target.relative_to(output).as_posix()})\n'
    targets[output / "summary.md"] = summary
    for target in targets:
        if target.exists() and not is_managed(target.read_text(encoding="utf-8")):
            raise ValueError(f"refusing unmanaged output: {target}")
    if not dry_run:
        materialize(root, migrate, expected=records)
        for target, text in targets.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=target.parent, delete=False) as handle:
                handle.write(text)
                temp = Path(handle.name)
            temp.replace(target)
    return {"records": len(records), "results": len(results), "outcomes": dict(counts), "outputs": len(targets), "dry_run": dry_run}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("memory", type=Path)
    parser.add_argument("--migrate-legacy", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(rebuild(args.memory, args.migrate_legacy, args.dry_run), sort_keys=True))
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == "__main__":
    main()
