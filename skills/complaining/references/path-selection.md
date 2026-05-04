# Complaint Log Path Selection

Choose the complaint log path inside the target project, not inside the reusable tooling repository unless the tooling repository itself is the target.

## Selection Order

1. Use the documentation folder named by the user or active project instructions.
2. If no folder is named, use an obvious existing documentation folder in this order:
   - `documentation/`
   - `Documentation/`
   - `docs/`
   - `Docs/`
3. If no documentation folder exists, create `documentation/`.

The complaint log filename is always:

```text
complaining.md
```

## Examples

```text
documentation/complaining.md
Documentation/complaining.md
docs/complaining.md
Docs/complaining.md
```

## Existing Files

If the file already exists, leave its current content in place and append future entries.

If the file exists but is empty, add at least:

```markdown
# Complaining Log
```

If the file has another reasonable heading or existing log structure, preserve it.

## Unclear Roots

When operating from a nested folder, inspect nearby project markers such as `.git`, solution files, package manifests, `AGENTS.md`, or existing documentation folders to identify the project root.

If multiple plausible roots exist and the choice affects where the complaint log will be written, choose the root that owns the current task. If that cannot be inferred safely, ask the user.
