"""PostToolUse marker: record that the advisor subagent was consulted this session.

Fires on Task/Agent tool completions. When the invoked subagent is 'advisor',
touches a per-session marker file that advisor_gate.py checks before allowing
Write/Edit tools.
"""

import json
import os
import sys


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_input = payload.get("tool_input") or {}
    if tool_input.get("subagent_type") != "advisor":
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd", ".")
    session_id = payload.get("session_id", "unknown")
    marker_dir = os.path.join(project_dir, ".claude")
    os.makedirs(marker_dir, exist_ok=True)
    marker = os.path.join(marker_dir, f".advisor-consulted-{session_id}")
    with open(marker, "w", encoding="utf-8"):
        pass


if __name__ == "__main__":
    main()
