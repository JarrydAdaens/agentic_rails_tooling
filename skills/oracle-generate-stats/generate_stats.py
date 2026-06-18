# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "tiktoken",
# ]
# ///

import sys
import os
import json
import tiktoken
from datetime import datetime, timezone
from pathlib import Path


SKIP_EXTENSIONS = {
    ".stats",
    ".pyc", ".pyo", ".pyd",
    ".exe", ".dll", ".so", ".dylib",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
    ".pdf", ".zip", ".tar", ".gz", ".7z", ".rar",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    ".db", ".sqlite", ".lock",
}

SKIP_DIRS = {
    ".git", ".hg", ".svn",
    "node_modules", "__pycache__",
    ".venv", "venv", ".env",
}


def should_skip(path: Path) -> bool:
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return True
    if path.name.startswith("."):
        return True
    return False


def collect_files(path: Path) -> list[Path]:
    files = []
    if path.is_file():
        if not should_skip(path):
            files.append(path)
    elif path.is_dir():
        for item in sorted(path.rglob("*")):
            if not item.is_file():
                continue
            if any(part in SKIP_DIRS for part in item.parts):
                continue
            if should_skip(item):
                continue
            files.append(item)
    return files


def process_file(path: Path, enc) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  SKIP  {path}  ({e})")
        return False

    stat = path.stat()
    token_count = len(enc.encode(text))

    data = {
        "file": path.name,
        "updated": datetime.now(timezone.utc).isoformat(),
        "size_bytes": stat.st_size,
        "lines": text.count("\n") + 1,
        "chars": len(text),
        "tokens": token_count,
        "tokenizer": "tiktoken cl100k_base",
    }

    stats_path = Path(str(path) + ".stats")
    stats_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"  OK    {path}  →  {token_count:,} tokens")
    return True


def main():
    if len(sys.argv) < 2:
        print("Error: nothing specified.")
        print()
        print("Usage:")
        print("  Whole directory:     generate_stats.py <directory>")
        print("  Specific file(s):    generate_stats.py <file1> <file2> ...")
        print()
        print("Please specify a directory or one or more files.")
        sys.exit(1)

    targets = [Path(arg) for arg in sys.argv[1:]]

    missing = [t for t in targets if not t.exists()]
    if missing:
        for m in missing:
            print(f"Error: not found: {m}")
        sys.exit(1)

    files = []
    for t in targets:
        files.extend(collect_files(t))

    if not files:
        print("No processable files found in the specified target(s).")
        sys.exit(0)

    enc = tiktoken.get_encoding("cl100k_base")

    print(f"Processing {len(files)} file(s)...")
    print()

    ok = sum(process_file(f, enc) for f in files)
    skipped = len(files) - ok

    print()
    print(f"Done.  {ok} written,  {skipped} skipped.")


if __name__ == "__main__":
    main()
