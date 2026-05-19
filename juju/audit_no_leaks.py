#!/usr/bin/env python
"""Juju Study Guide — answer-leak audit.

Scans juju/v3.html and reports any question where the input placeholder
contains the literal answer (with whitespace stripped, since ce() strips
whitespace before comparing).

Run from anywhere. Expects v3.html in the same directory as this script.
"""
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
HTML = HERE / "v3.html"
if not HTML.exists():
    sys.exit(f"v3.html not found at {HTML}")
src = HTML.read_text(encoding="utf-8")

q_pat = re.compile(
    r"<div class=q id=q(\d+)><p>(.*?)</p>"
    r"<input id=a\1 placeholder=(?:\"([^\"]*)\"|(\S+?))>"
    r"<button class=b onclick=\"(c[kesn])\(\1,([^)]*)\)",
    re.DOTALL,
)
sec_pat = re.compile(r"<h2>[^<]*?Section\s+(\d+)[^<]*</h2>", re.DOTALL)
secs = [(int(m.group(1)), m.start()) for m in sec_pat.finditer(src)]

def section_for(pos):
    s = None
    for ss, p in secs:
        if p < pos:
            s = ss
        else:
            break
    return s

WHITELIST = {
    "yes or no", "letter or word", "comma separated", "mean/median/mode",
    "vowel or consonant", "first or second", "number", "answer", "your answer",
    "simplified fraction", "fraction or whole number", "word", "y = mx + b",
    "dot type + direction", "fraction",
    "inequality with x", "inequality with a", "inequality with b",
    "inequality with c", "inequality with f", "inequality with h",
    "inequality with k", "inequality with r", "inequality with s",
    "inequality with v", "inequality with w",
}

def normspace(s):
    return re.sub(r"\s+", "", s).lower()

found = 0
leaks = []
by_sec = {}
for m in q_pat.finditer(src):
    n = int(m.group(1))
    ph = m.group(3) if m.group(3) is not None else m.group(4)
    fn = m.group(5)
    rest = m.group(6).strip()
    sec = section_for(m.start())
    found += 1
    by_sec.setdefault(sec, []).append((n, ph))

    if ph.lower() in WHITELIST:
        continue
    leak = False
    if fn in ("ce", "ck"):
        am = re.match(r"['\"]([^'\"]*)['\"]", rest)
        if am:
            ans = am.group(1)
            ph_n = normspace(ph)
            for a in ans.split("|"):
                an = normspace(a)
                if len(an) >= 2 and an in ph_n:
                    leak = True
                    leaks.append((sec, n, fn, ph, ans))
                    break
    elif fn == "cn":
        am = re.match(r"(-?[\d.]+)", rest)
        if am:
            try:
                tgt = float(am.group(1))
                t = str(int(tgt) if tgt == int(tgt) else tgt)
                if re.search(r"(?<!\d)" + re.escape(t) + r"(?!\d)", ph):
                    leaks.append((sec, n, fn, ph, t))
            except ValueError:
                pass

print(f"QUESTIONS SCANNED: {found}")
print(f"PLACEHOLDER LEAKS: {len(leaks)}")
print()
for sec in sorted(by_sec):
    qs = by_sec[sec]
    distinct_ph = sorted(set(p for _, p in qs))
    print(f"Sec {sec:>2} | q{qs[0][0]}-q{qs[-1][0]} | {len(qs):>3}q | {distinct_ph}")
print()
if leaks:
    print("=== LEAKS ===")
    for sec, n, fn, ph, ans in leaks:
        print(f"  Sec{sec} q{n} ({fn}): placeholder={ph!r}  answer={ans!r}")
    sys.exit(1)
else:
    print("=== NO PLACEHOLDER LEAKS ===")
    sys.exit(0)
