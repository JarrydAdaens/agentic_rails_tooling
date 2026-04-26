---
name: commit-history-workflow
description: >-
  Use this skill when summarizing exactly one existing commit from repository
  history for research-grade commit-history stitching. It inspects commit
  metadata, diffs, and changed files, then returns one structured JSON record.
  Do not use it for new commit messages or branch summaries.
metadata:
  version: "2.0"
---

# Commit History Workflow

This is an orchestration-style skill with a narrow input contract: exactly one
historical commit. Keep it deterministic so a larger stitching workflow can
compose many results safely.

Review exactly one historical commit and return exactly one JSON object for that
commit.

Use the rules in
[references/commit_log_template.md](references/commit_log_template.md). This
template is for historical research output, not for modern Jira or goal-based
commit messages.

## When to use

- When given one specific historical commit to summarize.
- When the commit already exists in version control and must be interpreted from
  Git metadata and diffs.
- When this output will be consumed by a stitching workflow.

## Do not use

- For summarizing an entire branch or commit range.
- For writing a new commit message for work done in the current session.
- For orchestration, batching, or progress tracking.

## Required workflow

1. Inspect exactly one commit from history.
2. Review commit metadata, author, author date, subject, parent SHAs, and
   changed files.
3. Ignore binary-only changes when reasoning about historical summary text.
4. Ignore empty, whitespace-only, formatting-only, and layout-only changes that
   do not affect behavior or compilation.
5. Classify the commit before writing the result.
6. Output exactly one JSON object, with no Markdown fence and no extra
   commentary.

## Categories

These categories are tuned for game-development codebases. For non-game repositories, prefer `MISC` when no category fits cleanly, or adapt this skill with a custom category set before using it on a different domain.

Use exactly one category from this fixed set:

- `GAME`
- `ART`
- `BUILD`
- `DOCS`
- `TEST`
- `MERGE`
- `DATA`
- `MISC`

If the commit is ambiguous, use `MISC`.

Category guidance:

- `GAME`: gameplay code, engine code, runtime logic, platform-specific game
  source, engineering work that is mainly code.
- `ART`: images, models, audio, authored assets, and non-engineer content work.
- `BUILD`: solution files, project files, dependency wiring, content pipeline
  setup, packaging, compile fixes, build scripts, and environment configuration.
- `DOCS`: documentation, notes, README, or explanatory text.
- `TEST`: tests, test fixtures, regression coverage, or test-only infrastructure.
- `MERGE`: merge commits.
- `DATA`: structured game data, content data, generated content artifacts, or
  large data-centric updates.
- `MISC`: ambiguous or mixed changes that do not cleanly fit a more specific
  category.

## Special-case handling

### Empty commits

If the commit has no meaningful file changes, return:

```json
{"status":"skipped","skip_reason":"empty"}
```

### Noisy commits

If the commit is only whitespace, formatting, layout, indentation, or other
non-behavioral cleanup with no effect on behavior or compilation, return:

```json
{"status":"skipped","skip_reason":"noisy"}
```

### Binary-only commits

If the commit is binary-only after ignoring text changes, return:

```json
{"status":"skipped","skip_reason":"binary_only"}
```

### Rename-only commits

If the commit only renames files without meaningful content changes, still emit
an `emitted` historical record. Prefer category `MISC` unless the renamed files
make another category obvious.

Body example:

```text
~ Changed: Renamed 3 files without substantive content changes.
```

### Merge commits

Merge commits must be emitted as full historical entries, not bare one-line
summaries.

Requirements:

- Use category `MERGE`.
- Preserve the original subject.
- Include parent SHAs.
- Include `changed_file_count`.
- Count changed files with merge-aware inspection. Do not assume `0` just because
  a simple diff-tree command returns nothing for the merge commit itself.
- Keep the summary factual and concise.

### Massive vendor imports

Vendor or third-party imports should still emit a full historical record using
the normal JSON schema.

Prefer:

- category `DATA` for data/content/vendor drops
- category `BUILD` for package/dependency/tooling updates

If the version is visible, include it in the summary or `~ Notes:` line.

## Historical entry rules

For emitted results:

- Use factual reconstruction, not speculative product-management language.
- Do not use Jira keys, goals, or invented planning context.
- Do not output `[GOAL x.y]`.
- Prefer `~ Changed:` lines.
- Add `~ Notes:` only when there is useful historical context directly supported
  by the commit subject or diff.
- Keep the summary grounded in the actual diff, not just the subject line.
- Preserve the original subject exactly as historical evidence.
- Use the author date as the historical date.

## Output contract

Return exactly one JSON object.

### Emitted result

```json
{
  "status": "emitted",
  "category": "GAME",
  "summary": "Restore the desktop XNA build",
  "author": "Jarryd",
  "author_date": "2015-04-02 13:57:29 +11:00",
  "sha": "fullsha",
  "original_subject": "raw original subject",
  "body_lines": [
    "~ Changed: Updated the desktop XNA build configuration so the target compiled again."
  ]
}
```

Optional emitted fields:

- `parent_shas`: array of parent SHAs
- `changed_file_count`: integer

### Failed result

If you cannot classify or summarize the commit reliably, return:

```json
{
  "status": "failed",
  "error_summary": "Short explanation of what made this commit unreliable to summarize."
}
```

## Final reminders

- Output JSON only.
- Do not wrap the JSON in a code block.
- Do not output analysis notes before or after the JSON.
- For skipped commits, return only the small skip object.
