#!/usr/bin/env python3
"""
phone_qa.py - Automated mobile-rendering QA for the MVP guest guide pages.

Renders each guide at real phone widths in BOTH browser engines guests actually use
(Chromium = Android Chrome's Blink; WebKit = iOS Safari's engine) and runs programmatic
checks for the specific failure modes that make a page "look bad on a phone":

  1. HORIZONTAL OVERFLOW  - documentElement.scrollWidth > innerWidth  (THE classic phone bug)
  2. OFFENDING ELEMENTS   - individual elements whose right edge spills past the viewport
  3. VIEWPORT META TAG    - must be present and width=device-width
  4. TINY TEXT            - % of visible text rendered below 12px (Google legible-font threshold)
  5. TAP TARGETS          - links/buttons/inputs smaller than 44x44 CSS px (Apple HIG / Lighthouse 48)
  6. STRAY DEV UI         - any element whose text matches the editor "Edit Layout" affordance

Thresholds sourced from Google Lighthouse mobile-usability + Apple HIG.
Outputs: a markdown report + full-page screenshots + an HTML contact sheet.

Usage:
  python phone_qa.py                 # all 6 properties, live URLs
  python phone_qa.py trails wylie    # subset
  python phone_qa.py --local         # render from local working-copy files instead of live
"""
import sys, os, json, datetime
from playwright.sync_api import sync_playwright

PROPERTIES = ["trails", "wylie", "pound", "maccauley", "milton", "petrarch"]
WIDTHS = [320, 390, 430]          # iPhone SE/old Android | modern iPhone | Pro Max / large Android
ENGINES = ["chromium", "webkit"]  # Blink (Android Chrome) | WebKit (iOS Safari)
LIVE_BASE = "https://a799608.github.io/mvp-guest-guides/{p}/index.html"
LOCAL_BASE = "file:///C:/temp/mvp-guest-guides/{p}/index.html"

OUTDIR = "C:/temp/phone_qa_out"
SHOTDIR = os.path.join(OUTDIR, "screenshots")

# JS that runs in-page and returns the full check payload for the current viewport.
CHECK_JS = r"""
() => {
  const vw = window.innerWidth;
  const docW = document.documentElement.scrollWidth;
  const overflow = docW - vw;

  // offending elements that spill past the right edge
  const offenders = [];
  const all = document.querySelectorAll('body *');
  for (const el of all) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    // element extends past viewport AND isn't itself viewport-wide-or-more (a scroller)
    if (r.right > vw + 2 && r.width <= vw + 2) {
      offenders.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className && el.className.toString) ? el.className.toString().slice(0,40) : '',
        right: Math.round(r.right),
        over: Math.round(r.right - vw)
      });
    }
  }
  offenders.sort((a,b)=>b.over-a.over);

  // viewport meta tag
  const vp = document.querySelector('meta[name="viewport"]');
  const vpContent = vp ? vp.getAttribute('content') : null;

  // tiny text: walk text nodes, measure computed font-size of parent
  let tinyChars = 0, totalChars = 0;
  const tinyTags = {};
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.nodeValue.trim();
    if (!t) continue;
    const p = n.parentElement;
    if (!p) continue;
    const cs = getComputedStyle(p);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const r = p.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const fs = parseFloat(cs.fontSize);
    totalChars += t.length;
    if (fs < 12) {
      tinyChars += t.length;
      const key = p.tagName.toLowerCase() + ' @' + fs.toFixed(1) + 'px';
      tinyTags[key] = (tinyTags[key]||0) + t.length;
    }
  }

  // tap targets
  const tappable = document.querySelectorAll('a,button,[role=button],input,select,textarea');
  const smallTargets = [];
  for (const el of tappable) {
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.width < 44 || r.height < 44) {
      smallTargets.push({
        tag: el.tagName.toLowerCase(),
        txt: (el.textContent||'').trim().slice(0,24),
        w: Math.round(r.width), h: Math.round(r.height)
      });
    }
  }

  // stray dev UI (editor affordance)
  const dev = [];
  for (const el of document.querySelectorAll('button,a')) {
    const tx = (el.textContent||'').trim();
    if (/edit layout|save layout|exit edit/i.test(tx)) dev.push(tx);
  }

  return {
    vw, docW, overflow,
    offenders: offenders.slice(0,12),
    vpContent,
    tinyPct: totalChars ? +(100*tinyChars/totalChars).toFixed(1) : 0,
    tinyTags,
    smallTargets: smallTargets.slice(0,20),
    smallTargetCount: smallTargets.length,
    dev
  };
}
"""

def grade(r):
    """Return (status, reasons[]) for one render's payload."""
    reasons = []
    if r["overflow"] > 2:
        reasons.append(f"horizontal overflow +{r['overflow']}px (page {r['docW']} > viewport {r['vw']})")
    if not r["vpContent"] or "width=device-width" not in (r["vpContent"] or ""):
        reasons.append(f"viewport meta missing/invalid: {r['vpContent']!r}")
    if r["tinyPct"] >= 60:
        reasons.append(f"{r['tinyPct']}% of text below 12px (Lighthouse-fail)")
    status = "FAIL" if reasons else "PASS"
    return status, reasons

def warnings(r):
    """Non-blocking quality warnings."""
    w = []
    if 0 < r["tinyPct"] < 60:
        w.append(f"{r['tinyPct']}% of text below 12px")
    if r["smallTargetCount"]:
        w.append(f"{r['smallTargetCount']} tap target(s) < 44px")
    if r["dev"]:
        w.append(f"stray dev control(s) visible: {', '.join(sorted(set(r['dev'])))}")
    if r["offenders"]:
        w.append(f"{len(r['offenders'])} element(s) near/over right edge")
    return w

def run():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_local = "--local" in sys.argv
    props = [p for p in args if p in PROPERTIES] or PROPERTIES
    base = LOCAL_BASE if use_local else LIVE_BASE

    os.makedirs(SHOTDIR, exist_ok=True)
    results = []

    with sync_playwright() as p:
        for engine in ENGINES:
            launcher = getattr(p, engine)
            browser = launcher.launch()
            for prop in props:
                url = base.format(p=prop)
                for w in WIDTHS:
                    ctx = browser.new_context(
                        viewport={"width": w, "height": 850},
                        device_scale_factor=3,
                        is_mobile=True,
                    )
                    page = ctx.new_page()
                    try:
                        page.goto(url, wait_until="networkidle", timeout=30000)
                    except Exception:
                        page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(900)
                    payload = page.evaluate(CHECK_JS)
                    shot = f"{prop}_{engine}_{w}.png"
                    page.screenshot(path=os.path.join(SHOTDIR, shot), full_page=True)
                    status, reasons = grade(payload)
                    results.append({
                        "prop": prop, "engine": engine, "width": w,
                        "status": status, "reasons": reasons,
                        "warnings": warnings(payload), "shot": shot,
                        "payload": payload,
                    })
                    print(f"[{status}] {prop:9s} {engine:8s} {w}px  "
                          f"overflow={payload['overflow']:+d}  tiny={payload['tinyPct']}%  "
                          f"smalltargets={payload['smallTargetCount']}  dev={len(payload['dev'])}")
                    ctx.close()
            browser.close()

    write_reports(results)
    fails = [r for r in results if r["status"] == "FAIL"]
    print(f"\n==== {len(results)} renders, {len(fails)} FAIL ====")
    return results

def write_reports(results):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # markdown
    md = [f"# Phone QA report — {ts}\n",
          f"{len(results)} renders ({len(ENGINES)} engines x {len(WIDTHS)} widths x props)\n"]
    md.append("| Property | Engine | Width | Status | Overflow | Tiny% | SmallTargets | DevUI |")
    md.append("|---|---|---|---|---|---|---|---|")
    for r in results:
        pl = r["payload"]
        md.append(f"| {r['prop']} | {r['engine']} | {r['width']} | "
                  f"**{r['status']}** | {pl['overflow']:+d}px | {pl['tinyPct']}% | "
                  f"{pl['smallTargetCount']} | {len(pl['dev'])} |")
    md.append("\n## Failures & warnings\n")
    for r in results:
        if r["reasons"] or r["warnings"]:
            md.append(f"**{r['prop']} / {r['engine']} / {r['width']}px** — {r['status']}")
            for x in r["reasons"]:
                md.append(f"  - FAIL: {x}")
            for x in r["warnings"]:
                md.append(f"  - warn: {x}")
            if r["payload"]["offenders"]:
                off = ", ".join(f"{o['tag']}.{o['cls']}(+{o['over']})" for o in r["payload"]["offenders"][:5])
                md.append(f"  - edge offenders: {off}")
            md.append("")
    mdpath = os.path.join(OUTDIR, "report.md")
    open(mdpath, "w", encoding="utf-8").write("\n".join(md))

    # HTML contact sheet
    html = ["<!doctype html><meta charset=utf-8><title>Phone QA contact sheet</title>",
            "<style>body{font-family:system-ui;background:#e4ede4;margin:0;padding:20px}",
            "h1{margin:0 0 4px}.grid{display:flex;flex-wrap:wrap;gap:14px}",
            ".cell{background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,.15);padding:8px;width:240px}",
            ".cell img{width:100%;border:1px solid #ccc;border-radius:6px;display:block}",
            ".pass{color:#1a7a2e;font-weight:700}.fail{color:#c0392b;font-weight:700}",
            ".meta{font-size:.8rem;margin:6px 2px 0}.warn{font-size:.72rem;color:#b85c00}</style>",
            f"<h1>Phone QA contact sheet</h1><p>{ts}</p><div class=grid>"]
    for r in sorted(results, key=lambda x:(x["prop"], x["engine"], x["width"])):
        cls = "pass" if r["status"]=="PASS" else "fail"
        warn = "<br>".join(r["warnings"])
        html.append(f"<div class=cell><img src='screenshots/{r['shot']}'>"
                    f"<div class=meta><b>{r['prop']}</b> · {r['engine']} · {r['width']}px "
                    f"· <span class={cls}>{r['status']}</span></div>"
                    f"<div class=warn>{warn}</div></div>")
    html.append("</div>")
    htmlpath = os.path.join(OUTDIR, "contact_sheet.html")
    open(htmlpath, "w", encoding="utf-8").write("\n".join(html))
    print(f"\nReport:  {mdpath}\nVisual:  {htmlpath}")

if __name__ == "__main__":
    run()
