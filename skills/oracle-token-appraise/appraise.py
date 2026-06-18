# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "tiktoken",
# ]
# ///

import sys
import os
import tiktoken


def main():
    if len(sys.argv) < 2:
        print("Usage: appraise.py <file_path> [--window N]")
        sys.exit(1)

    file_path = sys.argv[1]

    window = 40000
    if "--window" in sys.argv:
        idx = sys.argv.index("--window")
        if idx + 1 < len(sys.argv):
            window = int(sys.argv[idx + 1])

    if not os.path.exists(file_path):
        print(f"Error: file not found: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    file_size = os.path.getsize(file_path)
    char_count = len(text)
    line_count = text.count("\n") + 1

    enc = tiktoken.get_encoding("cl100k_base")
    token_count = len(enc.encode(text))

    pct = (token_count / window) * 100

    if pct < 10:
        verdict = "SMALL  — safe to read whole file"
    elif pct < 40:
        verdict = "MEDIUM — read whole file with care"
    elif pct < 80:
        verdict = "LARGE  — consider reading in sections"
    else:
        verdict = "HUGE   — do not read whole file; summarise or chunk"

    print(f"File:       {os.path.basename(file_path)}")
    print(f"Size:       {file_size:,} bytes")
    print(f"Lines:      {line_count:,}")
    print(f"Characters: {char_count:,}")
    print(f"Tokens:     {token_count:,}  (tiktoken cl100k_base)")
    print(f"Window:     {window:,} tokens")
    print(f"Usage:      {pct:.1f}%")
    print(f"Verdict:    {verdict}")


if __name__ == "__main__":
    main()
