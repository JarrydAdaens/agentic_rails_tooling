---
name: rails-execution-completion-contract
description: Recoverable verified completion under explicit commit policy.
metadata:
  version: "1.1"
---

# Completion transaction

The bundled [execution-receipt.py](../scripts/execution-receipt.py) helper captures
file/diff identities and reconciles delivery against Git. It requires Python 3.9+
and Git. It never stages, commits, runs acceptance commands, or updates a tracker.
The coordinator supplies observed evidence and retains authority over delivery.

Choose the one status owner, an explicit receipt path inside the target repository,
the checked implementation/configuration files, and separate completion-metadata
files. Include relevant configuration in checked identity and accepted user
decisions in evidence. Paths are explicit individual files; directory guesses
and repository escapes are refused.

```text
python <bundled-helper> capture --repo <target-root> --paths <checked-files>
python <bundled-helper> begin --repo <target-root> --record <receipt-path> --paths <checked-files> --metadata <status-files> --evidence <evidence-json> --policy none --owner <source-link>
python <bundled-helper> seal --repo <target-root> --record <receipt-path>
python <bundled-helper> reconcile --repo <target-root> --record <receipt-path>
```

Evidence contains `checks` with the actual `command`, `outcome`, and captured
`artifact_identity`. Selected `review` uses that same identity. Set
`review_required` for an adopted required review; its missing evidence blocks
preparation. Outcomes are `PASS` or an explicitly supported `WAIVED` with `authority`
and `reason`. `FAIL` and `ERROR` cannot approve completion. No optional reviewer is
required. An evidence file records observations; it does not authenticate a claim
or execute the command on the coordinator's behalf.

## Sequence

1. Inspect preexisting dirty/staged/untracked work before implementation. Preserve
   unrelated work and record ownership. Run applicable checks against the final
   implementation, relevant configuration, and accepted scope.
2. Capture identity and create `PREPARING` before editing terminal status metadata.
   With `single` or `batch` policy also supply `--authority` recording existing
   user commit authorization. A policy string is evidence, not permission by itself.
3. Prepare terminal source metadata with a link to the pending receipt. The status
   is provisional while the delivery transaction is pending. Update only owned
   completion fields; no worker resets another owner's tracker state. Inspect the
   metadata diff before sealing. The metadata exception covers status/provenance
   fields only; changed requirements, code, configuration, or executable examples
   require renewed applicable checks and a new checked identity.
4. Seal. Checked content/configuration must still match its verified identity.
   The final delivery capture checks that identity again before writing the seal;
   an intervening edit leaves the receipt `PREPARING` and requires renewed evidence.
   The sealed receipt freezes raw implementation and metadata fingerprints plus
   Git blob identities using the repository's attributes and clean filters.
5. Under `none`, reconciliation returns `VERIFIED_UNCOMMITTED` while fingerprints
   match. Report verified delivery and its diff identity; a commit is unnecessary.
   Under an authorized commit policy, stage only accepted owned changes and the
   sealed receipt, preserving unrelated staged work. Use `commit-log` by name for
   wording and commit the coherent completion bundle through normal Git controls.
6. Reconcile against Git. The Git-normalized sealed receipt and final artifacts in one
   ancestor commit prove `COMPLETED_COMMITTED`. Report that SHA without mutating
   the sealed receipt to add its own commit SHA, which would create another dirty
   terminal record. No extra bookkeeping commit is required.

For a batch, prepare and seal one receipt for the coherent accepted batch and its
owned terminal metadata. Do not run overlapping completion transactions in one
index. If an external tracker owns status, the local receipt records its link and
delivery evidence. Publish completion through that tracker's supported interface
after reconciliation; API failure leaves pending external delivery, never a
competing local story-state claim.

## Recovery

`PREPARING` resumes metadata/sealing, not implementation. `COMMIT_PENDING` can
represent an interruption before commit or a failed commit; diagnose the Git
result and retry only already-authorized delivery. `COMPLETED_COMMITTED` after an
interruption skips implementation and commit. `CHANGED_REQUIRES_CHECKS` preserves
new edits and renews affected evidence. An unrelated new HEAD can still contain
the accepted ancestor commit; a current difference is reported separately.
Raw fingerprints continue to detect worktree changes, including line endings.
Git identities recognize committed content after CRLF conversion or clean filters.
Receipts sealed by older helpers without Git identities retain their original
literal artifact comparison; create a new receipt with renewed evidence if that
comparison cannot establish completion.

A receipt does not own or automatically restore source edits. Preserve dirty
baselines and exact backups when a step needs destructive replacement. Resolve
metadata conflicts rather than resetting files from HEAD. Source status remains
provisional while a required delivery transaction is pending.

Sealed receipts are immutable evidence. Superseding content gets a new receipt
with a link to the previous result. Keep receipts while they are the only durable
evidence for verified uncommitted work. Their stages describe completion delivery,
not another work tracker.
