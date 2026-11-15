#!/usr/bin/env python3
"""Find and repair dead relative links in the repo's markdown files after file renames.

Run from the repo root:
    python fix_dead_links.py            # dry run: shows what would change
    python fix_dead_links.py --apply    # rewrite files

A dead link is repaired only when exactly ONE file in the same top-level case-study folder has the
same name once leading numbering ("04-") is ignored (PRD.md -> 04-PRD.md). Anything ambiguous or
unmatched is reported for you to fix by hand. Links that are empty or point to http(s) are reported,
never rewritten.
"""
import os, re, sys

APPLY = "--apply" in sys.argv
LINK = re.compile(r"(!?\[[^\]]*\]\()([^)\s]*)(\))")


def norm(name): return re.sub(r"^\d+-", "", name).lower()


files = [os.path.join(d, f) for d, _, fs in os.walk(".") if ".git" not in d.split(os.sep) for f in fs]
changed = unresolved = 0
for md in [f for f in files if f.endswith(".md")]:
    src = open(md, encoding="utf-8").read()
    out, base = src, os.path.dirname(md)

    def fix(m):
        global changed, unresolved
        target = m.group(2)
        if target == "":
            print(f"EMPTY LINK  {md}"); unresolved += 1; return m.group(0)
        if re.match(r"(https?:|mailto:|#)", target):
            return m.group(0)
        path, frag = (target.split("#", 1) + [""])[:2]
        if os.path.exists(os.path.normpath(os.path.join(base, path))):
            return m.group(0)
        top = os.path.normpath(md).split(os.sep)[:2]  # e.g. case-studies/retail-gen-ai
        cands = [f for f in files if norm(os.path.basename(f)) == norm(os.path.basename(path))
                 and os.path.normpath(f).split(os.sep)[:2] == top]
        if len(cands) != 1:
            print(f"UNRESOLVED  {md}: {target}  ({len(cands)} candidates)"); unresolved += 1; return m.group(0)
        new = os.path.relpath(cands[0], base).replace(os.sep, "/")
        if path.startswith("./"): new = "./" + new
        new += ("#" + frag) if frag else ""
        print(f"FIX         {md}: {target} -> {new}"); changed += 1
        return m.group(1) + new + m.group(3)

    out = LINK.sub(fix, src)
    if APPLY and out != src:
        open(md, "w", encoding="utf-8").write(out)
print(f"\n{changed} fixable, {unresolved} need hand-fixing" + ("  (applied)" if APPLY else "  (dry run; add --apply)"))
