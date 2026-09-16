#!/usr/bin/env python3
"""Stop hook: block the turn if Claude handed the user a shell command that will
fail from his terminal's working directory.

WHY THIS EXISTS. Measured five times, most recently 2026-09-02:

    fatal: not a git repository (or any of the parent directories): .git

Claude keeps emitting a bare `git branch -D <name>` for the user to paste. The bare
form is correct for CLAUDE's OWN Bash tool -- `dangerous-bash-guard.sh` refuses
the force form if it carries a `cd`, a `&&` or a `-C`, because the guard resolves
branches in its own cwd and a directory change would check one repo and delete
from another. Claude copied that shape into a command for THE USER, whose shell is
not in the repo. The constraint is real; applying it to the wrong shell is the
bug.

THE RULE: any fenced ```bash block Claude shows the user that runs a
repo-scoped tool must begin with an absolute `cd` into the repo.

Scope is deliberately narrow, because a noisy hook gets disabled and then you
have a guardrail you believe in and do not have:
  - Only ```bash fenced blocks, which is what the app puts a Run button on.
  - Only unambiguously repo-scoped tools. `gh` is NOT included: it takes
    `--repo` and `gh auth login` is global, so requiring a cd would be wrong.
  - `git clone` and `git config --global` are exempt -- both are correct from
    anywhere, and `clone` is wrong INSIDE a repo.
  - A block already starting with `cd /...`, `cd ~...` or `cd "$..."` passes.

Exit 2 + stderr blocks the turn and hands the text back to Claude, the same
mechanism `check-file-links.py` uses.
"""
import json
import os
import re
import sys

# Tools whose behaviour depends on which directory you are standing in, with no
# flag in common use that overrides it.
REPO_TOOLS = ("git", "npm", "npx", "pnpm", "yarn", "wrangler", "tsx", "eslint", "tsc")

# Correct from any directory, so a `cd` would be noise or actively wrong.
EXEMPT = (
    re.compile(r"^git\s+clone\b"),
    re.compile(r"^git\s+config\s+--global\b"),
    re.compile(r"^npm\s+(install|i)\s+-g\b"),
    re.compile(r"^npm\s+login\b"),
)

FENCE = re.compile(r"^[ \t]*```[ \t]*(?:bash|sh|shell|zsh)[ \t]*$", re.M)
STARTS_WITH_CD = re.compile(r"""^cd\s+(?:["']?[/~]|["']?\$(?:HOME|\{HOME\}))""")


def blocks(text):
    """Yield the body of every bash-tagged fenced block."""
    out, pos = [], 0
    while True:
        opener = FENCE.search(text, pos)
        if not opener:
            return out
        closer = re.compile(r"^[ \t]*```[ \t]*$", re.M).search(text, opener.end())
        if not closer:
            return out
        out.append(text[opener.end() : closer.start()])
        pos = closer.end()


def effective_lines(body):
    """Command lines only: no blanks, no comments, no line continuations."""
    return [
        ln.strip()
        for ln in body.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]


def offending_tool(body):
    """The repo-scoped tool this block runs, or None."""
    for line in effective_lines(body):
        # Split on shell separators so `foo && git status` is still seen.
        for segment in re.split(r"&&|\|\||;|\|", line):
            seg = segment.strip()
            if not seg:
                continue
            if any(rx.match(seg) for rx in EXEMPT):
                continue
            head = seg.split()[0] if seg.split() else ""
            # Strip a leading env assignment such as FOO=bar git status
            while "=" in head and not head.startswith("-"):
                parts = seg.split(None, 1)
                if len(parts) < 2:
                    break
                seg = parts[1]
                head = seg.split()[0] if seg.split() else ""
            if head in REPO_TOOLS:
                return head
    return None


def last_assistant_text(path):
    if not path or not os.path.exists(path):
        return ""
    text = ""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("type") != "assistant":
                continue
            content = (rec.get("message") or {}).get("content")
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = "\n".join(
                    c.get("text", "") for c in content if isinstance(c, dict)
                )
    return text


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    # Never fight a turn we already blocked once.
    if payload.get("stop_hook_active"):
        return 0

    text = last_assistant_text(payload.get("transcript_path"))
    if not text:
        return 0

    for body in blocks(text):
        lines = effective_lines(body)
        if not lines:
            continue
        if STARTS_WITH_CD.match(lines[0]):
            continue
        tool = offending_tool(body)
        if tool:
            sys.stderr.write(
                "Blocked by check-terminal-cwd: you gave the user a "
                "```bash block that runs `%s` without first cd-ing into the "
                "repo. His terminal is not in the project, so this fails with "
                "'fatal: not a git repository'. This has happened five times.\n"
                "\n"
                "Rewrite the block to start with an absolute cd, on its own or "
                "chained:\n"
                '  cd "/absolute/path/to/repo" && %s ...\n'
                "\n"
                "NOTE: the bare no-cd form is required only for YOUR OWN Bash "
                "tool, because dangerous-bash-guard.sh refuses a force branch "
                "delete that carries a cd or a chain. That constraint is about "
                "your shell, not his. Never copy it into a command you hand "
                "the user.\n" % (tool, tool)
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
