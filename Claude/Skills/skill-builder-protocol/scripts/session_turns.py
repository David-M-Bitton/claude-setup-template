#!/usr/bin/env python3
"""Extract the human turns from recent Claude Code session logs.

Why it exists: the raw session logs are ~90% assistant output and tool results.
What is worth learning from is what the user typed - the corrections, the
re-asks, the "no, do it this way". This prints only those.

Usage:
    python3 session_turns.py            # last 1 day
    python3 session_turns.py 7          # last 7 days
    python3 session_turns.py 1 --stats  # counts only, no message bodies

Reads ~/.claude/projects/**/*.jsonl. Never writes anything.
One day of turns is roughly 200 KB / 50k tokens - readable in one pass, but
check --stats first on any window wider than about 3 days.
"""
import json
import pathlib
import signal
import sys
import time

# Let `| head` close the pipe without a traceback.
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

MAX_MSG = 1200  # per-message truncation; corrections are short, pasted specs are not
ROOT = pathlib.Path.home() / ".claude" / "projects"


def human_turns(path):
    """Yield the user-authored text from one session log, skipping tool results."""
    out = []
    try:
        with path.open(errors="replace") as fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                if rec.get("type") != "user":
                    continue
                content = (rec.get("message") or {}).get("content")
                if isinstance(content, list):
                    # Tool results and images arrive as blocks; keep only real text.
                    content = "".join(
                        b.get("text", "")
                        for b in content
                        if isinstance(b, dict) and b.get("type") == "text"
                    )
                if not isinstance(content, str):
                    continue
                text = content.strip()
                # Injected context, not something the user typed.
                if not text or text.startswith("<") or "system-reminder" in text[:80]:
                    continue
                out.append(text[:MAX_MSG])
    except OSError:
        return []
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    stats_only = "--stats" in sys.argv
    days = float(args[0]) if args else 1.0
    cutoff = time.time() - days * 86400

    sessions = turns = 0
    for path in sorted(ROOT.rglob("*.jsonl")):
        try:
            if path.stat().st_mtime < cutoff:
                continue
        except OSError:
            continue
        msgs = human_turns(path)
        if not msgs:
            continue
        sessions += 1
        turns += len(msgs)
        if stats_only:
            print(f"{len(msgs):4d} turns  {path.parent.name} :: {path.stem}")
            continue
        print(f"\n===== {path.parent.name} :: {path.stem} ({len(msgs)} human turns) =====")
        for m in msgs:
            print(f"  - {m}")

    print(f"\n[{sessions} sessions, {turns} human turns, last {days} day(s)]", file=sys.stderr)


if __name__ == "__main__":
    main()
