#!/usr/bin/env python3
"""Stop hook — catch broken file links in the reply before the user reads a dead path.

WHAT IT CHECKS: a markdown link `[name](href)` whose href does not resolve.
-> BLOCKS (exit 2), so the model fixes the href and answers again.

Passes silently (exit 0, no output, no tokens). Only speaks when a link is broken.
Install: Stop hook in ~/.claude/settings.json.

🔴 A STOP HOOK CANNOT RETRACT TEXT. Read this before adding anything to this file.
It fires AFTER the reply has already streamed to the terminal. Exit 2 does not replace
that text — it only prevents *stopping*, so the model appends a SECOND reply and the user
reads the answer twice. Confirmed against the hooks reference: Stop + exit 2 "prevents
Claude from stopping, continues the conversation." There is no retract-and-replace.
**So the only defect worth exit 2 is one that actively MISLEADS him.** A dead link
qualifies. Cosmetic nits do not — the double-render costs more than they save.

REMOVED 2026-08-17, on the user's instruction ("lets just delete and remove tier 2 if it
dosnt do anything"): a second tier that flagged UNLINKED PATHS — a real file written as
a code span instead of a clickable link. Its whole history is a warning about this file:
  - Added 2026-08-11 as exit 2. Within hours it was cloning nearly every long reply,
    because most long replies contain a code-span path that resolves.
  - Downgraded the same day to exit 0 + `systemMessage`, which is visible to THE USER but
    NOT to the model. So it warned the one person who could not act on it and never
    reached the one who could. It fixed nothing for six days and printed ~10 lines of
    "Stop says:" noise per reply.
  - stderr at exit 0 was also tried and rejected: invisible to both.
**All three routes were dead ends, and that is a property of Stop hooks, not of the
implementation. Do not re-add it here.** The rule it was trying to enforce — link files
as `[name](path)` — lives in ~/.claude/CLAUDE.md, which the model reads BEFORE writing.
That is the only place a "write it correctly the first time" rule can work.
"""
import json
import os
import re
import sys
import time
from urllib.parse import unquote

# Skip anything that isn't a local file path.
SKIP = re.compile(r"^(https?:|mailto:|tel:|#|data:|file:|ftp:|chrome-extension:)", re.I)
LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?\s*(?:\"[^\"]*\")?\)")


def _text_of(msg):
    """Plain text of a message, ignoring tool_use / tool_result blocks."""
    parts = msg.get("content") or []
    if isinstance(parts, str):
        return parts
    return "\n".join(
        p.get("text", "") for p in parts
        if isinstance(p, dict) and p.get("type") == "text"
    )


def scan(transcript):
    """Return every assistant text block since the last real user prompt, joined.

    Subagent (sidechain) events are skipped — they are not the reply to the user.

    WHY ALL BLOCKS, NOT JUST THE NEWEST (fixed 2026-08-10, second attempt):
    A single turn emits many assistant text events — the short narration lines
    between tool calls ("Now checking X...") — and then the real reply last.
    The previous version kept only the NEWEST block and guarded staleness with
    `last_assistant < last_user`. That predicate cannot tell "the final reply has
    not flushed yet" from "the final reply is here", because an intermediate
    narration block is also newer than the last user prompt. So the guard read
    False, the hook checked a narration line, found no links, and passed — while
    the actual reply sitting one event later carried two broken ones. That is
    exactly how the 2026-08-10 links got through a hook written to stop them.

    Checking every block since the last user prompt removes the guesswork: it does
    not matter which block the link is in, or how many have flushed so far.
    """
    try:
        with open(transcript, encoding="utf-8") as fh:
            lines = fh.readlines()
    except Exception:
        return ""

    events = []
    for line in lines:
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("isSidechain"):
            continue
        events.append(ev)

    last_user = -1
    for i, ev in enumerate(events):
        msg = ev.get("message") or {}
        if ev.get("type") == "user" and msg.get("role") == "user" and _text_of(msg).strip():
            last_user = i

    parts = []
    for ev in events[last_user + 1:]:
        msg = ev.get("message") or {}
        if ev.get("type") == "assistant" and msg.get("role") == "assistant":
            t = _text_of(msg)
            if t.strip():
                parts.append(t)
    return "\n".join(parts)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Never re-block a turn we already blocked — that loops forever.
    if payload.get("stop_hook_active"):
        sys.exit(0)

    transcript = payload.get("transcript_path")
    if not transcript or not os.path.exists(transcript):
        sys.exit(0)

    cwd = payload.get("cwd") or os.getcwd()

    # The reply is written to the JSONL asynchronously, so at Stop time the final
    # text block may not have landed yet. Wait for the file to STOP GROWING (a fact
    # we can actually observe) rather than trying to infer from event ordering
    # whether the reply is complete — that inference is what failed on 2026-08-10.
    prev = -1
    for _ in range(25):  # ~5s ceiling; hook timeout is 15s
        try:
            cur = os.path.getsize(transcript)
        except OSError:
            break
        if cur == prev:
            break
        prev = cur
        time.sleep(0.2)

    text = scan(transcript)

    if not text.strip():
        sys.exit(0)

    broken = []
    for raw in LINK.findall(text):
        href = raw.split("#", 1)[0].strip()
        if not href or SKIP.match(href):
            continue
        # Only check things that look like a file, not bare words.
        if "/" not in href and "." not in href:
            continue
        # Markdown requires spaces to be %20-encoded; the filesystem does not.
        href = unquote(href)
        target = href if os.path.isabs(href) else os.path.join(cwd, href)
        # Dropbox CloudStorage path can remount — try the other form before failing.
        alts = [target]
        if "/Library/CloudStorage/Dropbox/" in target:
            alts.append(target.replace("/Library/CloudStorage/Dropbox/", "/Dropbox/"))
        elif "/Dropbox/" in target:
            alts.append(target.replace("/Dropbox/", "/Library/CloudStorage/Dropbox/"))
        if not any(os.path.exists(a) for a in alts):
            broken.append(href)

    if not broken:
        sys.exit(0)

    lines_out = [
        "FILE REFERENCE PROBLEM(S) in your reply — do not send it as written.",
        "cwd: %s" % cwd,
        "",
    ]

    for href in broken:
        lines_out.append('  ✗ "%s"  -> no such file' % href)
        base = os.path.basename(href)
        # Same-basename files under cwd are CANDIDATES, never "the answer" — a name
        # like MEMORY.md exists in many folders and the nearest one is often wrong.
        hits = []
        for root, dirs, files in os.walk(cwd):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
            if base in files:
                hits.append(os.path.relpath(os.path.join(root, base), cwd))
                if len(hits) >= 3:
                    break
        if hits:
            lines_out.append(
                "      same filename under cwd (CANDIDATES — confirm it is the one you meant): %s"
                % ", ".join(hits)
            )
        lines_out.append(
            "      if the file lives outside cwd, run `ls <relative-path>` from cwd "
            "and paste the exact string that worked."
        )

    lines_out += [
        "",
        "Fix and resend. Hrefs are relative to THIS session's cwd — "
        "a path written in CLAUDE.md is a label, not an href.",
        "A path with a SPACE stays in backticks and is never linked (CLAUDE.md rule); "
        "this check already skips those, so anything listed above is safe to link.",
    ]
    sys.stderr.write("\n".join(lines_out) + "\n")
    sys.exit(2)


if __name__ == "__main__":
    main()
