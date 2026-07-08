"""PreToolUse gate: deny Write/Edit tools until the advisor has been consulted this session.

Reads the hook payload from stdin. If no consult marker exists for the current
session, emits a permissionDecision deny so the executor self-corrects by
consulting the advisor subagent first. Marker files are created by
advisor_marker.py (PostToolUse on Task/Agent).
"""

import json
import os
import sys

DENY_REASON = (
    "Quota Advisor gate: consult the advisor subagent before the first write of "
    "this session. Invoke the Task tool with subagent_type 'advisor', using the "
    "consult payload format from CLAUDE.md (TASK / STAGE / PLAN-APPROACH / "
    "EVIDENCE / QUESTION), then retry this edit."
)


def marker_path(payload: dict) -> str:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd", ".")
    session_id = payload.get("session_id", "unknown")
    return os.path.join(project_dir, ".claude", f".advisor-consulted-{session_id}")


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # malformed input: fail open rather than block all writes

    if os.path.exists(marker_path(payload)):
        sys.exit(0)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": DENY_REASON,
        }
    }))


if __name__ == "__main__":
    main()
