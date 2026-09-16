#!/usr/bin/env python3
"""Stop hook — a NEW RULE must not reach a durable file without the every-session test.

WHAT IT CHECKS: whether this turn added a rule to a file EVERY FUTURE SESSION READS — any
CLAUDE.md (including the global one), AGENTS.md, a MEMORY.md or memory file, or any skill
— or recommended that the user add one. Either path, if the reply does not already argue the
rule both ways, it is blocked (exit 2) so the argument happens before the rule sticks.

Added 2026-09-03 on the user's instruction, in his words:

  "I want to do the same thing by editing the same hook or adding another stop hook for
  anytime claude recommends updating a claude.md file anywhere, including the global
  claude.md file, or any memory file or memory.md file, or any skill. Anytime it makes a
  recommendation OR actually automatically updates it, it should ask a similar question:
  'Will those genuinely help every future session or just this one edge case? Argue
  against it and decide for yourself. If it will, or we need to narrow it, you can
  automatically apply it now. If not, ignore.'"

WHY THESE FILES. They are read in full by every session that touches their tree, forever,
and nothing ever re-reads them critically. A wrong rule is worse than no rule: it is
obeyed. `CLAUDE.md` in this ecosystem has measured itself regrowing 257 -> 388 -> 504 ->
394 lines, and each of those lines was added by a session that thought it was adding
"just one".

🔴 WHY IT IS NOT THE SAME HOOK AS check-deferred-learnings.py. That hook fires when a
learning was PARKED and goes silent when the turn wrote the file. This one fires BECAUSE
the turn wrote the file. Same question, inverted trigger — merging them makes both
unreadable. They do not double-fire: this hook ignores fold/inbox phrasing, which is the
only thing that hook fires on when there is no write.

🔴 READ check-file-links.py's docstring BEFORE WIDENING ANYTHING HERE. A Stop hook cannot
retract text; exit 2 makes the model append a SECOND reply, so the user reads the turn twice.
The cost is only worth paying when a NEW RULE is landing unexamined. Fixing a stale fact,
correcting a number, bumping a version or writing a CHANGELOG row is not a new rule, and
gate 2 exists to keep this hook off all of them.

⭐ GATE 3 IS WHAT KEEPS THIS USABLE. A turn that already argued the rule both ways and
decided has done the thing the hook asks for, and blocking it would be pure friction —
which is how a guardrail gets switched off. The hook fires only when the ARGUMENT IS
MISSING, so the cheapest way to satisfy it is to do the work, not to route around it.

THE THREE GATES, ALL REQUIRED.
  1. This turn wrote to a durable rule file, OR the reply recommends updating one.
     CHANGELOG.md and this hook's own tests are excluded — a log is not a rule surface.
  2. A WRITE must additionally be RULE-SHAPED: the written text carries normative
     language — never/always/must/do not/required/forbidden, or the 🔴 ⛔ ⚠️ markers this
     ecosystem uses for exactly that. Version bumps, date corrections, link repairs and
     deletions do not reach this gate.
     ⭐ A RECOMMENDATION SKIPS GATE 2, and the asymmetry is deliberate. the user's
     instruction covers "anytime it recommends updating" one of these files, rule or
     fact — and the every-session test applies just as well to a remembered FACT, which
     gets obeyed as readily as a rule. Firing on every WRITE regardless of shape would
     block routine maintenance, which is the alarm fatigue that gets a hook switched off;
     a recommendation is rare enough to carry no such cost.
  3. The reply does NOT already contain the argument. Naming both sides — "every future
     session" against "one edge case", a case against, a narrowing, a withdrawal — clears
     it. Doing the work is the way past this hook; there is no other.
"""
import json
import os
import re
import sys
import time

# Gate 1a — the durable files. Path-matched against everything the turn wrote.
DURABLE_PATH = re.compile(
    r"(?:^|[\\\\/])CLAUDE\.md$"
    r"|(?:^|[\\\\/])AGENTS\.md$"
    r"|(?:^|[\\\\/])MEMORY\.md$"
    r"|(?:^|[\\\\/])SKILL\.md$"
    r"|[\\\\/]memory[\\\\/][^\\\\/]+\.md$"
    r"|[\\\\/]Skills[\\\\/].+\.md$"
    r"|[\\\\/]skills?[\\\\/].+[\\\\/](?:SKILL|CLAUDE|AGENTS)\.md$",
    re.I,
)

# Gate 1a, subtracted — a log, a test, or this hook's own fixtures is not a rule surface.
NOT_A_RULE_SURFACE = re.compile(r"CHANGELOG\.md$|[\\/]test-|_test\.|\.test\.|[\\/]tmp[\\/]|[\\/]Temp[\\/]", re.I)

# Gate 1b — recommending the edit rather than making it. Deliberately does NOT match
# fold/inbox phrasing: that belongs to check-deferred-learnings.py.
RECOMMEND = re.compile(
    r"(?:recommend|suggest|propose|worth|we\s+should|you\s+should|I(?:'d| would)\s+"
    r"(?:recommend|suggest|add))"
    r"[^.!?\n]{0,80}"
    r"(?:add(?:ing)?|updat(?:e|ing)|writ(?:e|ing)|put(?:ting)?|record(?:ing)?|"
    r"document(?:ing)?|captur(?:e|ing)|encod(?:e|ing))"
    r"[^.!?\n]{0,80}"
    r"(?:CLAUDE\.md|AGENTS\.md|MEMORY\.md|SKILL\.md|\bthe\s+skill\b|\bmemory\s+file\b"
    r"|\ba\s+memory\b|\bglobal\s+instructions\b)"
    r"|(?:CLAUDE\.md|MEMORY\.md|SKILL\.md|\bthe\s+skill\b)"
    r"[^.!?\n]{0,60}"
    r"(?:should|ought\s+to|needs?\s+to)\s+(?:get|gain|carry|say|record|have)",
    re.I,
)

# Gate 2 — is it a RULE, or just maintenance? Normative language, or this ecosystem's
# own markers for it.
NORMATIVE = re.compile(
    r"\bnever\b|\balways\b|\bmust\b|\bdo not\b|\bdon'?t\b|\bshall\b"
    r"|\brequired\b|\bforbidden\b|\bnot\s+optional\b|\bnon-negotiable\b"
    r"|\bstanding\s+(?:rule|authorisation|authorization|decision)\b"
    r"|\bthe\s+rule\s+is\b|\brule:\s"
    r"|\U0001f534|\u26d4|\u26a0\ufe0f|\U0001f6ab",  # 🔴 ⛔ ⚠️ 🚫
    re.I,
)

# Gate 3 — the argument, already present. Any of these means the work was done.
ARGUED = re.compile(
    r"every\s+(?:future\s+)?session"
    r"|(?:one|single|this)\s+edge\s+case"
    r"|(?:the\s+)?case\s+(?:against|for)\b"
    r"|argu(?:e|ed|ing)\s+(?:against|both\s+ways|it\s+out|myself)"
    r"|both\s+ways"
    r"|(?:third[- ]party\s+)?outsider"
    r"|narrow(?:ed|ing)?\s+(?:it|the\s+rule|the\s+scope)"
    r"|withdrew|withdrawn|disproven"
    r"|would\s+prove\s+(?:me|it)\s+wrong",
    re.I,
)

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
CODE_FENCE = re.compile(r"```.*?```", re.S)
CODE_SPAN = re.compile(r"`[^`\n]*`")

# Tool inputs that carry a file path and new content.
WRITERS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def _text_of(msg):
    parts = msg.get("content") or []
    if isinstance(parts, str):
        return parts
    return "\n".join(
        p.get("text", "") for p in parts
        if isinstance(p, dict) and p.get("type") == "text"
    )


def _tool_uses(msg):
    parts = msg.get("content") or []
    if isinstance(parts, str):
        return []
    return [
        p for p in parts
        if isinstance(p, dict) and p.get("type") == "tool_use"
    ]


def durable_writes(tool_uses):
    """[(path, new_text)] for every write this turn that landed in a durable rule file.

    \U0001f534 FILE TOOLS ONLY. A Bash branch was here until 2026-09-03 and was REMOVED
    the second time it false-fired, both times on the same defect: it scanned the whole
    command string for anything ending in `.md` and treated a MENTION as a WRITE. So
    `cat ~/.claude/CLAUDE.md`, a grep for it, or -- the case that caught it -- writing
    DOCUMENTATION that quotes the path, all read as a rule landing in that file. The tell
    was the reported path carrying a leading markdown backtick: `` `~/.claude/CLAUDE.md ``.

    \u26d4 AND IT CANNOT BE REPAIRED WITH A REGEX, which is why it is gone rather than
    tightened. The obvious fix -- require a write token near the path -- fails the real
    write idiom in this ecosystem, `p = "<path>"` on one line and `io.open(p, "w")` forty
    lines later, where the path is bound to a variable and is nowhere near the write.
    The false positive and the true positive are indistinguishable to any pattern that
    does not actually parse shell and Python.

    \u26a0\ufe0f WHAT THIS COSTS, stated plainly: a rule written through a Bash heredoc is
    not caught here. That is a real gap and it is the common editing path. It is covered
    instead by lesson-detector.sh, which fires before the turn, and by the routing rules
    in the skill. \u2b50 The trade is deliberate: a hook that cries wolf gets switched off,
    and then it catches nothing at all.
    """
    hits = []
    for tu in tool_uses:
        if tu.get("name", "") not in WRITERS:
            continue
        inp = tu.get("input", {}) or {}
        path = str(inp.get("file_path") or inp.get("notebook_path") or "")
        if not DURABLE_PATH.search(path) or NOT_A_RULE_SURFACE.search(path):
            continue
        body = " ".join(
            str(inp.get(k, "")) for k in ("content", "new_string", "new_source")
        )
        hits.append((path, body))
    return hits


def sentences(text):
    text = CODE_FENCE.sub(" ", text)
    kept = "\n".join(
        ln for ln in text.splitlines() if not ln.lstrip().startswith((">", "|"))
    )
    return [s.strip() for s in SENTENCE_SPLIT.split(kept) if s.strip()]


def recommendation(reply):
    """Gate 1b + gate 2 on one sentence of the reply."""
    for s in sentences(reply):
        bare = CODE_SPAN.sub(" ", s)
        if RECOMMEND.search(bare):
            return s
    return None


def load(transcript):
    try:
        with open(transcript, encoding="utf-8") as fh:
            lines = fh.readlines()
    except Exception:
        return []
    events = []
    for line in lines:
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("isSidechain"):
            continue
        events.append(ev)
    return events


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if payload.get("stop_hook_active"):  # never re-block a turn we already blocked
        sys.exit(0)

    transcript = payload.get("transcript_path")
    if not transcript or not os.path.exists(transcript):
        sys.exit(0)

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

    events = load(transcript)
    if not events:
        sys.exit(0)

    last_user = -1
    for i, ev in enumerate(events):
        msg = ev.get("message") or {}
        if ev.get("type") == "user" and msg.get("role") == "user" and _text_of(msg).strip():
            last_user = i

    reply, tools = [], []
    for i, ev in enumerate(events):
        if i <= last_user:
            continue
        msg = ev.get("message") or {}
        if ev.get("type") != "assistant" or msg.get("role") != "assistant":
            continue
        reply.append(_text_of(msg))
        tools.extend(_tool_uses(msg))

    reply_raw = "\n".join(reply)

    # Gate 1 + gate 2 — a rule-shaped write, or a rule-shaped recommendation.
    what, where = None, None
    for path, body in durable_writes(tools):
        if NORMATIVE.search(body):
            what = "wrote a rule into"
            where = path
            break
    if what is None:
        # 🔴 A RECOMMENDATION NEEDS NO NORMATIVE LANGUAGE, and a write does. The
        # asymmetry is deliberate. the user's instruction covers "anytime it recommends
        # updating" one of these files, rule or fact — and the every-session test applies
        # just as well to a remembered FACT, which is obeyed as readily as a rule. But
        # firing on every WRITE regardless of shape would block version bumps, typo fixes
        # and link repairs, which is the alarm fatigue that gets a hook switched off.
        line = recommendation(reply_raw)
        if line:
            what, where = "recommended an edit to", line[:200]
    if what is None:
        sys.exit(0)

    if ARGUED.search(reply_raw):  # gate 3 — the work is already done
        sys.exit(0)

    sys.stderr.write(
        "DURABLE RULE, UNARGUED — this turn %s:\n"
        "\n"
        "  %s\n"
        "\n"
        "Every future session reads that file in full, forever, and nothing re-reads it\n"
        "critically. A wrong rule is worse than no rule, because it gets obeyed.\n"
        "\n"
        "Will it genuinely help EVERY future session, or just this one edge case?\n"
        "Argue against it, as a third-party outsider who has never seen this repo, and\n"
        "decide for yourself. Then act in the same turn:\n"
        "\n"
        "  - Helps every session -> APPLY IT NOW. You do not need to ask.\n"
        "  - Too broad           -> NARROW IT, then apply the narrow version now.\n"
        "  - One edge case       -> IGNORE IT. Say so and move on.\n"
        "\n"
        "Check it is TRUE and NOT ALREADY THERE before it lands — re-run the measurement\n"
        "and re-read the target file. On 2026-09-03 two rules about to be folded turned\n"
        "out to be one misdiagnosis and one duplicate of a rule added hours earlier.\n"
        "\n"
        "Then say which of the three you chose, and why.\n"
        % (what, where)
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
