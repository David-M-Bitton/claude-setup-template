#!/usr/bin/env python3
"""
Pre-delivery eval/check for HTML reports built from template.html in this folder.
RUN THIS before sharing/publishing ANY HTML report.

Usage:  python3 eval-check.py <file.html> [more.html ...]     (Windows: python eval-check.py ...)

Checks:
  1. no-index — robots AND googlebot meta must be present with noindex.
  2. SEO <title> present and not the unedited placeholder.

Exit code 0 = all pass, 1 = any failure.
"""
import sys, re

def check(path):
    html = open(path, encoding='utf-8').read()
    fails = []
    if not re.search(r'name=["\']robots["\'][^>]*noindex', html, re.I):
        fails.append("missing <meta name=robots noindex>")
    if not re.search(r'name=["\']googlebot["\'][^>]*noindex', html, re.I):
        fails.append("missing <meta name=googlebot noindex>")
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    if not m or not m.group(1).strip():
        fails.append("missing <title>")
    elif 'replace with descriptive title' in m.group(1):
        fails.append("placeholder <title> not replaced")
    return fails

def main():
    if len(sys.argv) < 2:
        print("usage: python3 eval-check.py <file.html> [...]   (Windows: python eval-check.py ...)"); sys.exit(2)
    bad = False
    for path in sys.argv[1:]:
        fails = check(path)
        if fails:
            bad = True
            print(f"FAIL  {path}")
            for f in fails:
                print("   -", f)
        else:
            print(f"PASS  {path}  (noindex present · title set)")
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
