---
name: historical_commit_entry_template
version: 2.0
agentic_rails_source_version: 2.0
---

# Historical Commit Entry Template

Use this template for reconstructing repository history from old commits during a
research workflow.

This is not a modern commit-message template. Do not use Jira keys, goal IDs, or
invented planning context.

## Required historical entry shape

Rendered entry:

```text
[CATEGORY] - Concise historical summary
Author: Name
Date: YYYY-MM-DD HH:MM:SS +/-TZ
SHA: fullsha

Original subject: raw original subject

~ Changed: Factual change summary
~ Notes: Optional historical note
```

## Required fields

Every emitted entry must have:

- `category`
- `summary`
- `author`
- `author_date`
- `sha`
- `original_subject`
- at least one `body_lines` entry

## Allowed categories

- `GAME`
- `ART`
- `BUILD`
- `DOCS`
- `TEST`
- `MERGE`
- `DATA`
- `MISC`

Use `MISC` when the commit cannot be classified confidently.

## Body line guidance

Prefer factual lines such as:

```text
~ Changed: Updated build configuration for the desktop target.
~ Changed: Added missing collision data content.
~ Notes: Commit subject says the deployment GUID warning was not a real error.
```

Rules:

- Prefer `~ Changed:` for primary factual statements.
- Use `~ Notes:` only for important supporting context directly grounded in the
  commit subject, metadata, or diff.
- Avoid `~ Problem:` / `~ Resolution:` unless a future workflow explicitly calls
  for that structure.
- Avoid line-by-line mechanical narration.
- Avoid speculative reasoning about product goals or intent.

## Merge entries

Merge commits should render as full historical entries using category `MERGE`.

Include:

- `parent_shas`
- `changed_file_count`

Suggested merge body line:

```text
~ Changed: Merged parent histories with 31 changed files in the merge commit.
```

## Quality bar

- Be specific when the diff clearly supports specificity.
- Stay factual and concise.
- Prefer provenance and traceability over stylistic flourish.
- Preserve the original subject exactly.
