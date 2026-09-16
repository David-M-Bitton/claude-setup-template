#!/usr/bin/env python3
"""Stop hook — block "this page can't be fetched" when the escalation ladder was never walked.

WHAT IT CHECKS: the reply, and any file written this turn, for a phrase that records a
source as unreachable ("could not be fetched", "needs a real browser", "genuinely
blocked", "won't render headless"). `Memory/Website Crawling/MEMORY.md` line 9 forbids
writing that into a file before Tier 4 headless Playwright has actually RUN and failed.
-> BLOCKS (exit 2), so the model escalates and corrects the claim.

Added 2026-08-20 on the user's instruction, after the same rule was broken on three
separate days (2026-08-09, 2026-08-14, 2026-08-19). On the third, "Florida mortgage
genuinely blocked - Clerk API 404s, SPA won't render headless" was written into a donor
brief that was about to be shared outside his org. He caught it by hand each time.

🔴 READ check-file-links.py's docstring BEFORE WIDENING ANYTHING HERE. A Stop hook
cannot retract text; exit 2 makes the model append a SECOND reply, so the user reads the
turn twice. That cost is only worth paying for a claim that actively MISLEADS him. A
sentence asserting a page is unreadable when it opens at 200 on the first headless try
qualifies. General talk about blocking does not — which is what the three gates are for.

THE FOUR GATES, ALL REQUIRED. Every one of them exists to stop a false block:
  1. The session actually tried to fetch something. A session merely DISCUSSING this
     rule (a report, a code review, this hook's own commit) never touched the network
     and must stay silent. This is the gate that keeps the hook off most replies.
  2. A give-up phrase appears outside quotes and code spans. Blockquoted and backticked
     text is nearly always the rule being cited, not a fresh claim.
  3. The give-up phrase shares its SENTENCE with a URL or an HTTP status code. A
     sentence about a file write, a permission hook or a local script refusing
     something is not a fetch claim, however it is worded. Only fire on a sentence
     that names the web thing it is giving up on.
  4. The session shows NO Tier 4+ escalation anywhere. If Playwright, a browser
     user-agent, OpenCLI, Firecrawl, Apify or a real browser was used at any point,
     the ladder was walked and the give-up may well be honest. Session-wide on purpose:
     the fight may have happened twenty turns before the sentence was written.
"""
import json
import os
import re
import sys
import time

# Gate 2 — the claim. Conclusive assertions only; a bare "blocked" is far too common.
GIVEUP = re.compile(
    r"(?:could\s*n[o']t|couldn't|could\s+not|cannot|can'?t|unable\s+to|failed\s+to)"
    r"\s+(?:be\s+)?(?:fetch|scrape|read|retrieve|access|load)"
    r"|needs?\s+a\s+real\s+browser"
    r"|requires?\s+a\s+real\s+browser"
    r"|(?:won'?t|will\s+not|does\s*n[o']t|doesn't)\s+render\s+headless"
    r"|genuinely\s+blocked"
    r"|not\s+readable|unreadable",
    re.I,
)

# Gate 1 — proof the session went to the network at all.
FETCHED = re.compile(
    r"WebFetch|WebSearch|\bcurl\b|\brequests\.get\b|urllib|httpx|aiohttp"
    r"|firecrawl|opencli|playwright|apify|scrapecreators|dataforseo"
    r"|mcp__Claude_Browser__|mcp__claude-in-chrome__|mcp__Control_Chrome__",
    re.I,
)

# Gate 3 — proof the ladder was walked past Tier 1. Any one of these clears the hook.
ESCALATED = re.compile(
    r"sync_playwright|chromium\.launch|playwright[-_ ]?cli|\bplaywright\b"
    r"|user[-_ ]?agent|-A\s+['\"]Mozilla|Mozilla/5\.0"
    r"|opencli|firecrawl"
    r"|mcp__Apify__|mcp__apify2__|scrapecreators"
    r"|mcp__Claude_Browser__|mcp__claude-in-chrome__|mcp__Control_Chrome__",
    re.I,
)

# Gate 3 — proof the sentence is about the WEB. A URL or a real HTTP status code in the
# same sentence. Without this the hook fires on file writes, permission hooks and local
# scripts that "blocked" something, which have nothing to do with fetching a page.
NEAR = re.compile(
    r"https?://|\bwww\.|\b[a-z0-9][a-z0-9-]*\.(?:com|org|net|io|ai|co|uk|gov|edu|dev|app)\b"
    r"|\b(?:100|101|200|201|202|204|301|302|303|304|307|308"
    r"|400|401|402|403|404|405|406|407|408|409|410|418|422|429"
    r"|500|501|502|503|504)(?!\d)"
    r"|status\s+code|HTTP\s*\d",
    re.I,
)

# NOT on ":" — "could not be fetched: https://..." is one claim, and splitting there
# would strip the URL that gate 3 needs off the end of the sentence.
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
    """Everything the model sent to a tool — command lines, file contents, MCP names."""
    parts = msg.get("content") or []
    if isinstance(parts, str):
        return ""
    out = []
    for p in parts:
        if isinstance(p, dict) and p.get("type") == "tool_use":
            out.append(str(p.get("name", "")))
            out.append(json.dumps(p.get("input", {})))
    return "\n".join(out)


def strip_quoted(text):
    """Drop code and blockquotes — that text is the rule being cited, not a new claim."""
    text = CODE_FENCE.sub(" ", text)
    text = CODE_SPAN.sub(" ", text)
    return "\n".join(
        ln for ln in text.splitlines() if not ln.lstrip().startswith((">", "|"))
    )


def sentences(text):
    """Blockquotes out, then one sentence per element. Code spans are LEFT IN so a
    URL written in backticks still counts as evidence under gate 3."""
    kept = "\n".join(
        ln for ln in text.splitlines() if not ln.lstrip().startswith((">", "|"))
    )
    return [s.strip() for s in SENTENCE_SPLIT.split(kept) if s.strip()]


def is_claim(sentence):
    """Gate 2 + gate 3 on one sentence: a give-up phrase outside code, next to a URL
    or an HTTP status code."""
    bare = CODE_SPAN.sub(" ", CODE_FENCE.sub(" ", sentence))
    return bool(GIVEUP.search(bare)) and bool(NEAR.search(sentence))


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

    session_blob = []   # gates 1 and 3: the whole session
    claim_text = []     # gate 2: this turn's reply + anything it wrote to a file
    for i, ev in enumerate(events):
        msg = ev.get("message") or {}
        if ev.get("type") != "assistant" or msg.get("role") != "assistant":
            continue
        tools = _tool_blob(msg)
        session_blob.append(tools)
        if i > last_user:
            claim_text.append(_text_of(msg))
            claim_text.append(tools)  # the donor-brief case: written into a file, not said

    session_blob = "\n".join(session_blob)
    claim_raw = "\n".join(claim_text)

    if not FETCHED.search(session_blob):          # gate 1
        sys.exit(0)
    line = next((s for s in sentences(claim_raw) if is_claim(s)), None)
    if line is None:                              # gates 2 and 3
        sys.exit(0)
    if ESCALATED.search(session_blob):            # gate 4
        sys.exit(0)
    sys.stderr.write(
        "BLOCKED-FETCH CLAIM with no escalation — do not send this as written.\n"
        "\n"
        "  %s\n"
        "\n"
        "Nothing in this session shows Tier 4 was tried. A 403, 404, empty body, cookie\n"
        "wall or JS-only shell means ESCALATE, not 'this page cannot be read' — and a\n"
        "default user-agent is the single most common reason a site refuses a bot.\n"
        "\n"
        "Do this before answering again:\n"
        "  1. Re-run the URL with a browser User-Agent (plain curl -A 'Mozilla/5.0 ...').\n"
        "  2. If that fails, run the 30-second headless Playwright snippet at the top of\n"
        "     Memory/Website Crawling/MEMORY.md and print the real status code.\n"
        "  3. Still failing? Escalate to OpenCLI, Firecrawl, Apify, or a real browser.\n"
        "\n"
        "Then CORRECT the claim wherever it landed — including any file you just wrote to.\n"
        "If Tier 4 genuinely ran and failed, say which tier failed and what status it\n"
        "returned; that is a finding. 'Blocked' on its own is not.\n"
        % line[:300]
    )
    sys.exit(2)


def selftest():
    """python3 check-fetch-giveup.py --selftest"""
    fires = [
        "Florida mortgage genuinely blocked - Clerk API 404s, SPA won't render headless",
        "The donor page could not be fetched: https://example.org/donors returns nothing.",
        "example.com is not readable without a real browser.",
    ]
    quiet = [
        "STEP 9 could not write: the protection hook blocked every attempt.",
        "The hook refused the write and the file cannot be read by this routine.",
        "It matched the word blocked in a sentence about a file write being refused.",
        "The rule says `could not be fetched` must never be written before Tier 4 ran.",
        "> could not be fetched",
    ]
    bad = [s for s in fires if not any(map(is_claim, sentences(s)))]
    bad += ["QUIET-FIRED: " + s for s in quiet if any(map(is_claim, sentences(s)))]
    if bad:
        print("FAIL")
        for b in bad:
            print("  ", b)
        return 1
    print("ok — %d fire cases, %d quiet cases" % (len(fires), len(quiet)))
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
