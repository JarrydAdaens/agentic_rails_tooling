"""SessionStart cleanup: delete stale advisor-consult markers.

Markers are per-session, so old sessions leave orphaned files behind. Anything
older than 24 hours can never belong to a live session and is removed.
"""

import glob
import os
import sys
import time

MAX_AGE_SECONDS = 24 * 60 * 60


def main() -> None:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    pattern = os.path.join(project_dir, ".claude", ".advisor-consulted-*")
    cutoff = time.time() - MAX_AGE_SECONDS
    for marker in glob.glob(pattern):
        try:
            if os.path.getmtime(marker) < cutoff:
                os.remove(marker)
        except OSError:
            pass  # another session may have removed it; never block startup


if __name__ == "__main__":
    main()
    sys.exit(0)
