---
name: scoutmap-format
version: 1.0
---

# Scoutmap format (`scoutmap.md`)

The scout writes `scoutmap.md` as a persistent discovery map and work queue. The mermaid-mapper workflow updates the first column as rows move through states; see `.workflows/mermaid-mapper/references/state-model.md` for transition rules.

## Line format

Each non-empty line is one row:

```text
<StateEmoji>,<FilePath>,<Type1>,<Type2>,<Type3>,...
```

- **StateEmoji**: one of the state markers defined in the state-model reference (unassigned when the scout first writes the file).
- **FilePath**: path to the source file, relative to the **repository root**, using forward slashes.
- **TypeN**: one or more identifier names for classes (or other in-scope types) to map from that file. No spaces around commas inside the row.

## Rules

- One row per file. If a file has no in-scope types after filtering, omit the file entirely.
- List only types that belong in the mapping scope for this job (not every type declared in the file).
- Do not wrap fields in quotes unless your tooling requires it; keep rows simple CSV-like lines.
- Header lines or comments are optional; if present, prefix comment lines with `#` so parsers can skip them.

## Example rows

```text
⬜,src/UI/Resources/ResourceViewModels.cs,WoodViewModel,GoldViewModel,FoodViewModel
⬜,src/UI/Units/UnitViewModels.cs,InfantryViewModel,CavalryViewModel
```

## Scout responsibility

When the scout creates or overwrites `scoutmap.md` for a fresh discovery run, every data row MUST start with the **unassigned** state emoji. The Boss (workflow orchestrator) updates state as work is assigned and completed.
