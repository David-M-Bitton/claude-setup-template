#!/usr/bin/env python3
"""Stop hook — block a reply that PARKS a learning instead of deciding it.

WHAT IT CHECKS: this turn's reply for a sentence announcing that lessons, findings or
learnings are pending, awaiting, or need folding into a skill or a doc. Reporting a
parked learning is the failure: it hands the user a decision that is Claude's to make, and
the finding then rots in an inbox nobody reads.
-> BLOCKS (exit 2), so the model argues the learning both ways and either folds it now,
   narrows it, or withdraws it.

Added 2026-09-03 on the user's instruction, in their words:

  "Anytime you tell me about learnings like 'Two learnings need folding' or 'Two process
  learnings await folding into the <skill> skill' I want you to use a hook that asks
  something like, 'Will those learnings genuinely help every future session or just this
  one edge case? Argue against it and decide for yourself. If it will, or we need to
  narrow it, fold it into the skill now, don't wait.'"

WHY IT EARNS A BLOCK. Measured on the session that prompted it (2026-09-03, a ticket and
a ticket). Two learnings were written to the a project inbox and reported as pending. When
the user asked the question this hook now asks:
  - the first was WRONG. "gh project item-list reports a clean negative on a freshly
    added item" was indexing lag of seconds, disproven by a 30-second re-check that had
    never been run. Folding it would have shipped a false rule.
  - the second was ALREADY in the doc, folded by another session hours earlier.
Both were generalised from a single bruise and neither survived contact with the
question. The cost of parking them was a round trip; the cost of folding them unexamined
would have been a false rule in a file every session reads.

🔴 READ check-file-links.py's docstring BEFORE WIDENING ANYTHING HERE. A Stop hook cannot
retract text; exit 2 makes the model append a SECOND reply, so the user reads the turn twice.
That is only worth paying when the reply hands him work that was Claude's to do. A turn
that DECIDED — folded it, narrowed it, withdrew it, deleted the inbox file — must stay
silent, which is what gate 3 is for.

THE THREE GATES, ALL REQUIRED.
  1. A deferral phrase appears outside code and blockquotes. Quoted text is nearly always
     this rule being cited (a report, a code review, this hook's own commit), not a fresh
     deferral. NEGATIVES are subtracted first, so "nothing to fold", "fold nothing" and
     "already folded" never reach the gate.
  2. The same SENTENCE names the thing being deferred: a learning, a finding, a lesson,
     an inbox, a skill, a CHANGELOG. Without this the hook fires on "two tests are
     pending", which is not this rule at all.
  3. The turn shows no folding WORK. If it edited a SKILL.md, a CHANGELOG, a reference
     file or an agents doc, or removed a file from a learnings inbox, the decision was
     made and reporting it is correct. Scoped to THIS turn, not the session: a turn that
     folds one learning and parks another should still be caught.
"""
import json
import os
import re
import sys
import time

# Gate 1 — the deferral. Conclusive parking only; a bare "later" is far too common.
DEFER = re.compile(
    r"(?:needs?|need|await(?:s|ing)?|pending|waiting|remains?|left|still)"
    r"\s+(?:to\s+be\s+)?(?:folding|folded|fold\b)"
    # ⛔ NOT a bare "to". "to fold" appears in ordinary prose ABOUT folding -- it
    # false-fired on "they have no inbox and no skill to fold into" within an hour of
    # shipping (2026-09-03). The intent-carrying words are the ones left here.
    r"|(?:should|could|worth|want\s+to|ought\s+to|plan\s+to|going\s+to)\s+(?:be\s+)?fold(?:ed|ing)?\b"
    r"|fold(?:ed|ing)?\s+(?:it|them|these|those)?\s*(?:in\s+)?(?:later|next\s+time|"
    r"when\s+(?:you|the user|he)|on\s+the\s+next|at\s+the\s+next|in\s+a\s+later)"
    r"|for\s+the\s+(?:next\s+)?(?:fold|folder)\b"
    r"|(?:in|into)\s+the\s+(?:learnings\s+)?inbox\b"
    r"|left\s+(?:it|them|these)\s+(?:in|for)\s+the\b"
    r"|say\s+the\s+word\s+and\s+I(?:'ll| will)\s+write",
    re.I,
)

# Gate 1, subtracted FIRST — a decision is not a deferral. These phrasings mean the work
# is done or deliberately dropped, and they contain the word "fold" too.
DECIDED = re.compile(
    r"fold(?:ing)?\s+nothing"
    r"|nothing\s+(?:left\s+)?to\s+fold"
    r"|(?:already|now)\s+fold(?:ed)?"
    r"|fold(?:ed)?\s+(?:it|them|these|those|both|all)\s+(?:in|into|now)"
    r"|(?:withdrew|withdrawn|dropped|deleted|disproven|retracted)"
    r"|decided\s+(?:not\s+)?to\s+fold"
    r"|no\s+learnings?\b"
    r"|inbox\s+is\s+(?:empty|clear)",
    re.I,
)

# Gate 2 — proof the sentence is about a LEARNING, not some other pending thing.
SUBJECT = re.compile(
    r"\blearning|\bfinding|\blesson|\binbox\b|SKILL\.md|CHANGELOG"
    r"|\bskill\b|CLAUDE\.md|AGENTS\.md|\bapp-docs\b|\bplaybook\b|\bMEMORY\.md",
    re.I,
)

# Gate 3 — proof this turn actually folded something. Any of these clears the hook.
FOLDED = re.compile(
    r"SKILL\.md|CHANGELOG\.md|references/|/learnings/|unattended\.md"
    r"|session-prompts\.md|the-gate\.md|issue-tracker\.md|codebase\.md"
    r"|Version:\s*v\d|\bversion\s+bump",
    re.I,
)
# ...but only when the turn WROTE, not merely mentioned. Paired with FOLDED.
WROTE = re.compile(r"\brm\b|\bmv\b|>\s*\S|tee\b|\.write\(|open\([^)]*[\"\']w[\"\']", re.I)

FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def folded_this_turn(tool_uses):
    """Did this turn actually fold something, PER TOOL CALL?

    \U0001f534 FIXED 2026-09-03. FOLDED and WROTE used to be matched independently over one
    concatenated blob of the whole turn, so ANY write anywhere plus ANY mention of a skill
    path anywhere cleared the gate. Measured: a turn that parked a learning, wrote an
    unrelated file with the Write tool, and merely `cat`-ed a SKILL.md was silenced. That
    is the ordinary shape of a skill-editing turn, so the hook was closer to switched off
    than to occasionally wrong -- and a silenced Stop hook is invisible, which is what
    makes it worth fixing even though the failure direction is the safe one.

    \u2b50 The Bash arm is KEPT DELIBERATELY. Folding through a `python3 - <<PY` heredoc is
    the common editing path here, and requiring a file tool would block a session that did
    the work -- the expensive failure. So Bash clears only when the SAME command both
    names a folding target and carries a write indicator.

    \u26a0\ufe0f Residual, accepted: `grep never SKILL.md > /tmp/x` clears the gate, because
    the command names a target and contains `>`. It is contrived, and it errs toward
    silence rather than toward a wrongful block.
    """
    for tu in tool_uses:
        name = tu.get("name", "")
        inp = tu.get("input", {}) or {}
        if name in FILE_TOOLS:
            path = str(inp.get("file_path") or inp.get("notebook_path") or "")
            if FOLDED.search(path):
                return True
        elif name == "Bash":
            cmd = str(inp.get("command", ""))
            if FOLDED.search(cmd) and WROTE.search(cmd):
                return True
    return False

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
CODE_FENCE = re.compile(r"```.*?```", re.S)
CODE_SPAN = re.compile(r"`[^`\n]*`")


def _text_of(msg):
    parts = msg.get("content") or []
    if isinstance(parts, str):
        return parts
    return "\n".join(
        p.get("text", "") for p in parts
        if isinstance(p, dict) and p.get("type") == "text"
    )


def _tool_blob(msg):
    """Everything the model sent to a tool — tool names, paths, file contents."""
    parts = msg.get("content") or []
    if isinstance(parts, str):
        return ""
    out = []
    for p in parts:
        if isinstance(p, dict) and p.get("type") == "tool_use":
            out.append(str(p.get("name", "")))
            out.append(json.dumps(p.get("input", {})))
    return "\n".join(out)


def sentences(text):
    """Blockquotes and fences out, then one sentence per element."""
    text = CODE_FENCE.sub(" ", text)
    kept = "\n".join(
        ln for ln in text.splitlines() if not ln.lstrip().startswith((">", "|"))
    )
    return [s.strip() for s in SENTENCE_SPLIT.split(kept) if s.strip()]


def is_deferral(sentence):
    """Gates 1 and 2 on one sentence, with the decision phrasings subtracted first."""
    bare = CODE_SPAN.sub(" ", sentence)
    if DECIDED.search(bare):
        return False
    return bool(DEFER.search(bare)) and bool(SUBJECT.search(bare))


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

    # The reply lands in the JSONL asynchronously — wait for the file to stop growing
    # rather than guessing from event order. Same fix as check-file-links.py.
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

    reply, turn_tools = [], []
    for i, ev in enumerate(events):
        if i <= last_user:
            continue
        msg = ev.get("message") or {}
        if ev.get("type") != "assistant" or msg.get("role") != "assistant":
            continue
        reply.append(_text_of(msg))
        parts = msg.get("content") or []
        if not isinstance(parts, str):
            turn_tools.extend(
                p for p in parts
                if isinstance(p, dict) and p.get("type") == "tool_use"
            )

    reply_raw = "\n".join(reply)

    line = next((s for s in sentences(reply_raw) if is_deferral(s)), None)
    if line is None:                                          # gates 1 and 2
        sys.exit(0)
    if folded_this_turn(turn_tools):  # gate 3
        sys.exit(0)

    sys.stderr.write(
        "PARKED LEARNING — do not hand the user this decision. It is yours.\n"
        "\n"
        "  %s\n"
        "\n"
        "Will that genuinely help EVERY future session, or just this one edge case?\n"
        "Argue against it, as a third-party outsider who has never seen this repo, and\n"
        "decide for yourself. Then act in the same turn:\n"
        "\n"
        "  - Holds as written  -> FOLD IT NOW. Version bump + CHANGELOG row.\n"
        "  - Too broad         -> NARROW IT, then fold the narrow version now.\n"
        "  - One-off, or wrong -> WITHDRAW it and say so. Delete the inbox file.\n"
        "\n"
        "Before folding, CHECK THE CLAIM IS STILL TRUE — re-run the measurement, and\n"
        "re-read the target file. On 2026-09-03 one parked learning was indexing lag\n"
        "misread as a defect, and the other was already in the doc. Neither survived.\n"
        "\n"
        "Do not reply with the deferral. Reply with the decision and the edit.\n"
        % line[:400]
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
