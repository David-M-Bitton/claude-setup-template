#!/usr/bin/env bash
# rc-bridge.sh — turn Remote Control on for a Claude Code session, print its web link.
#
#   rc-bridge.sh <host-session-id>        e.g. local_ea42c901-4bd1-47c2-90b2-0254d9ecfd7f
#   rc-bridge.sh                          falls back to $CLAUDE_CODE_HOST_SESSION_ID
#
# Focuses the session with the app's own deep link, types /remote-control, presses Return,
# then waits for the app to write a bridge id into the session JSON.
#
# Exit 0 = a bridge id exists and the https link is on stdout.
# Judge this on the printed link and on bridgeSessionIds, never on the exit code alone.

set -uo pipefail

SID="${1:-${CLAUDE_CODE_HOST_SESSION_ID:-}}"
[ -n "$SID" ] || { echo "usage: rc-bridge.sh <host-session-id>" >&2; exit 2; }

ROOT="$HOME/Library/Application Support/Claude/claude-code-sessions"
JSON="$(find "$ROOT" -maxdepth 4 -name "$SID.json" 2>/dev/null | head -1)"
[ -n "$JSON" ] || { echo "no session JSON for $SID under $ROOT" >&2; exit 3; }

# First id in bridgeSessionIds, or empty. Never fails: the app rewrites this file whole,
# so a read can land mid-write and see invalid JSON. That is a retry, not an error.
bridge_id() {
  python3 - "$JSON" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    sys.exit(0)
b = d.get("bridgeSessionIds") or []
print(b[0] if b else "")
PY
}

existing="$(bridge_id)"
if [ -n "$existing" ]; then
  echo "https://claude.ai/code/$existing"
  exit 0
fi

# 1. Focus the session. Only the claude:// deep link reaches one specific session.
open "claude://claude.ai/epitaxy/$SID" || { echo "deep link failed for $SID" >&2; exit 4; }
sleep 4

# 2. Refuse to type into whatever else happens to be in front.
front="$(osascript -e 'tell application "System Events" to name of first process whose frontmost is true' 2>/dev/null)"
case "$front" in
  Claude*) : ;;
  *) echo "Claude is not frontmost (front app: ${front:-unknown}) - refusing to type" >&2; exit 5 ;;
esac

# 3. Type it, then submit it.
#
# Two Returns, not one. Typing "/remote-control" opens the slash-command autocomplete;
# the first Return accepts the highlighted entry into the composer and does NOT submit it.
# The second Return submits. If the first one did submit, the second lands on an empty
# composer and does nothing.
osascript <<'APPLESCRIPT'
tell application "System Events"
  keystroke "/remote-control"
  delay 1.5
  key code 36
  delay 1.5
  key code 36
end tell
APPLESCRIPT

# 4. Wait for the app to persist it. 30s was too short in the 2026-09-18 probe: the id
# landed only after the poll had already given up, which made a working run report FAILED.
# ponytail: fixed 120s ceiling, make it a flag if a slower machine ever needs longer.
for _ in $(seq 1 60); do
  sleep 2
  id="$(bridge_id)"
  if [ -n "$id" ]; then
    echo "https://claude.ai/code/$id"
    exit 0
  fi
done

echo "typed /remote-control and pressed Return twice, but no bridge id appeared within 120s" >&2
exit 1
