---
paths:
  - "**/*.sh"
  - "**/*.bash"
---

# Bash and Shell Scripting Rules

## Scope

Applies to all shell scripts in this workspace: `.sh`/`.bash` files, CI steps, and hook scripts.

Intent: small, safe, ShellCheck-clean scripts following the Google Shell Style Guide. Shell is for orchestration — once a script needs real data structures, argument parsing beyond a case statement, or is trending past ~100 lines, write it in Python instead (see `python-rules.md`).

## Safety Baseline

Every script starts with:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

- `set -e` — exit on error; `set -u` — error on unset variables; `set -o pipefail` — a pipeline fails if any stage fails.
- Where a command is allowed to fail, make it explicit: `command || true` or an `if` test — never by weakening the flags for the whole script.
- Quote every expansion: `"$var"`, `"$(cmd)"`, `"$@"`. Unquoted expansions are the top shell defect class; ShellCheck flags them all.
- Use `[[ ... ]]` for tests, not `[ ... ]` or `test`.
- Use `trap 'cleanup' EXIT` for temp files and other cleanup; create temp files with `mktemp`.

## Naming and Structure

- Script files: `kebab-case.sh`, executable bit set, extension kept (this workspace favors discoverability over the Google Guide's no-extension executables).
- Functions and local variables: `snake_case`. Declare function-local variables with `local`.
- Constants and environment variables: `SCREAMING_SNAKE_CASE`; `readonly` for true constants.
- Put logic in functions and end the script with `main "$@"`. Short linear scripts (a dozen lines) may skip the ceremony.
- Start each script with a comment block stating purpose and usage. Give functions a one-line comment when the name alone doesn't carry it.

## Idioms

- `"$(cmd)"` for command substitution, never backticks.
- `printf` over `echo` for anything with escapes, variables, or `-` prefixes.
- Iterate output safely: `while IFS= read -r line; do ...; done < <(cmd)` — never `for x in $(cmd)`.
- Arithmetic in `(( ... ))` / `$(( ... ))`, not `expr` or `let`.
- Arrays for lists of arguments or files: `args=(-v --color); cmd "${args[@]}"`.
- Check dependencies up front: `command -v jq >/dev/null || { echo "jq required" >&2; exit 1; }`.
- Errors go to stderr: `echo "error: ..." >&2`. Exit nonzero on failure.

## Portability

- Target Bash explicitly via the shebang; do not write for `sh` while using Bash features.
- This workspace runs scripts on Windows (Git Bash), macOS, and Linux. Avoid GNU-only flags where a portable form exists (`sed -i` differs on macOS; prefer redirect-and-move or do the edit in Python).
- Line endings must be LF. Enforce with `.gitattributes` (`*.sh text eol=lf`) — CRLF shebangs fail cryptically on every Unix host.

## Tooling

- Every script must pass `shellcheck` with zero warnings. Fix findings rather than suppressing; a `# shellcheck disable=SCnnnn` needs a reason comment on the same line or the line above.
- Format with `shfmt` (2-space indent: `shfmt -i 2 -w`). Do not hand-format around it.

## Do Not

- Do not parse `ls` output. Use globs or `find -print0 | xargs -0`.
- Do not use `eval` on any string containing external input.
- Do not pipe `curl`/`wget` output straight into `bash` in scripts. Download, inspect or checksum, then execute.
- Do not write interactive prompts (`read -p`) into scripts meant for CI or agent execution; take arguments or environment variables instead.
- Do not silently `cd` and keep going — `cd path || exit 1`, or better, use absolute paths.
- Do not store secrets in scripts or echo them into logs.

## Examples

```bash
#!/usr/bin/env bash
# sync-rules.sh — copy rule files into the deployed rules directory.
# Usage: sync-rules.sh <source-dir> <target-dir>
set -euo pipefail

readonly REQUIRED_TOOLS=(rsync)

check_dependencies() {
  local tool
  for tool in "${REQUIRED_TOOLS[@]}"; do
    command -v "$tool" >/dev/null || { echo "error: $tool is required" >&2; exit 1; }
  done
}

main() {
  if [[ $# -ne 2 ]]; then
    echo "usage: $(basename "$0") <source-dir> <target-dir>" >&2
    exit 64
  fi
  local source_dir="$1" target_dir="$2"
  check_dependencies
  [[ -d "$source_dir" ]] || { echo "error: no such directory: $source_dir" >&2; exit 1; }
  rsync --archive --delete "$source_dir"/ "$target_dir"/
  echo "synced $(find "$source_dir" -name '*.md' | wc -l) rule files"
}

main "$@"
```
