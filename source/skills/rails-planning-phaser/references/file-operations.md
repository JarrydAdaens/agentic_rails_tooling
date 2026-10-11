---
name: rails-planning-phaser-file-operations
description: Preview, replacement, and interrupted-run recovery using the bundled helper.
metadata:
  version: "1.0"
---

# File operations

The bundled [phase-files.py](../scripts/phase-files.py) helper uses Python 3.9+
and the standard library. Locate it relative to this skill's installed bundle;
the target plan and draft directory are explicit absolute arguments.

```text
python <bundled-helper> inspect --plan <absolute-plan>
python <bundled-helper> preview --plan <absolute-plan> --drafts <absolute-drafts>
python <bundled-helper> apply --plan <absolute-plan> --drafts <absolute-drafts> --expected <fingerprint>
python <bundled-helper> apply --plan <absolute-plan> --drafts <absolute-drafts> --expected <fingerprint> --rephase
python <bundled-helper> recover --plan <absolute-plan> --dry-run
python <bundled-helper> recover --plan <absolute-plan>
```

`inspect` reports the current source fingerprint, existing phased state, and
pending recovery. Drafts live outside the target plan folder and contain `plan.md`
plus contiguous `phase-N.md` files when applicable. A single-unit revision contains
only `plan.md`. The helper maps that staged manifest onto the explicitly named
target, so ad hoc plan filenames are preserved.

A requested scorecard is staged as `cer-score-card.md` and applied with
`--scorecard`; absent that flag, the helper never touches an existing scorecard.
Preview or `apply --dry-run` has no writes and does not require `--expected`.
The preview reports exact affected names and before/after digests. Present the
phase text and assessment alongside it; digest checks do not judge plan quality.

Apply checks the expected fingerprint, stores exact current files under
`phasing-history/<run-id>/original/`, stores all replacement bytes in `staged/`,
and writes the journal/pointer before replacing anything. Each individual write
uses an atomic rename; the whole multi-file operation is recoverable, not a
single filesystem transaction. Prior history remains untouched.

Journal states are `PREPARED`, `APPLYING`, `COMMITTED`, and `ROLLED_BACK`. A pending
run blocks another apply. Recovery checks preserved/staged hashes and current
files before restoring prior bytes and removing outputs absent from the original.
It refuses files changed independently after interruption. Preserve that conflict
and diagnose it instead of automatically overwriting current work.

Recovery can be interrupted and rerun because restored files match their recorded
original digests. Symlinks, noncontiguous numbering, unknown draft artifacts,
missing outputs, and malformed or mismatched recovery identities are diagnostics.
The helper copies current bytes without consulting Git, including CRLF, Unicode,
dirty work, and files that have never been committed.

For legacy phased plans without history, explicit rephasing preserves the current
manifest and phase files. Recovering an earlier uncommitted original is impossible
if no copy survived; record that provenance gap rather than claiming Git contains
it. Do not execute archived model assignments from legacy frontmatter.
