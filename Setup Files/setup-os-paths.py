#!/usr/bin/env python3
"""
Make the copied knowledge base match THIS computer's operating system.

Run once during setup, AFTER the files have been copied into place:

    python3 setup-os-paths.py mac   ~/Documents/Claude
    python  setup-os-paths.py win   %USERPROFILE%\\Documents\\Claude

The path can be a folder (processed recursively) or a single file — pass a single
file for ~/.claude/CLAUDE.md, whose folder contains files this must not rewrite.

What it does to every .md and .py file under the target folder:

  1. Deletes the blocks belonging to the OTHER operating system.
     Blocks look like this in the shipped files (HTML comments, so they are
     invisible when the Markdown is rendered):

         <!--os:mac-->
         ...Mac/Linux version of the rule...
         <!--/os:mac-->
         <!--os:win-->
         ...Windows version of the same rule...
         <!--/os:win-->

  2. Deletes the surviving side's marker lines, so the finished file reads
     as if it was always written for this machine.

  3. On Windows only: rewrites `~/Documents/Claude/...` style paths to
     `%USERPROFILE%\\Documents\\Claude\\...` inside backticks.

Idempotent — running it twice changes nothing the second time.
"""
import io, os, re, sys

MARK = re.compile(r'^[ \t]*<!--/?os:(mac|win)-->[ \t]*$')

def strip_blocks(text, drop):
    """Remove <!--os:drop-->…<!--/os:drop--> blocks; unwrap the other side."""
    out, skipping = [], False
    for line in text.split('\n'):
        m = MARK.match(line)
        if m:
            os_name = m.group(1)
            raw = line.strip()
            if os_name == drop:
                skipping = raw.startswith('<!--os:')   # open -> skip, close -> stop
            continue                                   # marker lines never survive
        if not skipping:
            out.append(line)
    return '\n'.join(out)

def win_paths(text):
    def conv(m):
        span = m.group(1).replace('~/', '%USERPROFILE%/')
        return '`' + span.replace('/', '\\') + '`'
    return re.sub(r'`([^`\n]*~/[^`\n]*)`', conv, text)

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('mac', 'win'):
        print("usage: setup-os-paths.py <mac|win> <folder-or-single-file>")
        sys.exit(2)
    target, root = sys.argv[1], os.path.expanduser(sys.argv[2])
    drop = 'win' if target == 'mac' else 'mac'

    # A single file is a valid target — used for ~/.claude/CLAUDE.md, which sits
    # in a folder full of files this script must NOT touch.
    if os.path.isfile(root):
        paths, base = [root], os.path.dirname(root)
    elif os.path.isdir(root):
        paths = [os.path.join(d, n) for d, _x, fs in os.walk(root) for n in fs
                 if n.endswith(('.md', '.py'))]
        base = root
    else:
        print(f"error: no such file or folder: {root}")
        sys.exit(2)

    changed = 0
    for p in paths:
        before = io.open(p, encoding='utf-8').read()
        after = strip_blocks(before, drop)
        if target == 'win':
            after = win_paths(after)
        if after != before:
            io.open(p, 'w', encoding='utf-8').write(after)
            changed += 1
            print("updated", os.path.relpath(p, base))
    print(f"\ndone — {target}; {changed} file(s) updated")

if __name__ == '__main__':
    main()
