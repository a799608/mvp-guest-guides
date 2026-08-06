# -*- coding: utf-8 -*-
"""Transform each property's v1 guest guide into the v2 dark-editorial brand.
Reads <prop>/index.html, writes <prop>/v2.html. Live index.html untouched.
Reuses the approved Petrarch v2 <style> shell so all six are identical."""
import io, re, sys, os
from bs4 import BeautifulSoup

# repo root = this script's directory (script lives in the repo root)
ROOT = os.path.dirname(os.path.abspath(__file__))
PROPS = ["trails", "wylie", "pound", "maccauley", "milton", "petrarch"]

# --- reuse the approved shell CSS from petrarch v2 ---
pet = io.open(f"{ROOT}/petrarch/v2.html", encoding="utf-8").read()
STYLE = re.search(r"<style>.*?</style>", pet, re.S).group(0)
# no sticky action bar anymore -> reclaim the reserved bottom space
STYLE = re.sub(r"padding-bottom:\d+px; /\* room for sticky action bar \*/",
               "padding-bottom:24px;", STYLE)

# nice section-title names + ordering
NICE = {
    "GETTING IN":"Getting In","FRONT DOOR & PET GATES":"Front Door & Pet Gates",
    "FRONT DOOR":"Front Door","AMENITY BADGES":"Amenity Badges","THE NOS":"The Nos",
    "SEPTIC SYSTEM":"Septic System","HEAT":"Heat","A/C":"Air Conditioning","FIREPLACE":"Fireplace",
    "GARBAGE DISPOSAL":"Garbage Disposal","HOOD VENT":"Hood Vent","CHARCOAL GRILL":"Charcoal Grill",
    "FIREPIT":"Firepit","SLEEPING ARRANGMENTS":"Sleeping Arrangements","TRASH COLLECTION":"Trash Collection",
    "PETS":"Pets","WHAT'S PROVIDED":"Provided","WHAT TO BRING":"Bring","GAMEROOM ITEMS":"Gameroom",
    "KITCHEN APPLIANCES":"Kitchen Appliances","LAUNDRY":"Laundry",
}
def section_of(title):
    t = title.upper()
    if "GETTING IN" in t or "FRONT DOOR" in t: return "access"
    if "AMENITY BADGES" in t: return "badges"
    if "THE NOS" in t or "SEPTIC" in t: return "rules"
    if t in ("HEAT","A/C") or "FIREPLACE" in t: return "climate"
    if any(k in t for k in ("GARBAGE DISPOSAL","HOOD VENT","GRILL","FIREPIT","KITCHEN APPLIANCES","LAUNDRY")): return "kitchen"
    if "SLEEPING" in t: return "sleeping"
    if "TRASH" in t or "PETS" in t: return "trashpets"
    if "PROVIDED" in t: return "provided"
    if "BRING" in t: return "bring"
    return "more"

SECTION_LABELS = [
    ("access","Arrival & Access"), ("badges","Amenity Badges"), ("rules","House Rules"),
    ("climate","Climate & Comfort"), ("kitchen","Kitchen & Outdoor"), ("sleeping","Sleeping"),
    ("trashpets","Trash & Pets"), ("more","Good to Know"),
]

def translate_body(body):
    """Rename v1 helper classes to v2 equivalents, return inner HTML string."""
    for el in body.select(".info-row"): el["class"] = ["row"]
    for el in body.select(".info-label"): el["class"] = ["r-l"]
    for el in body.select(".info-value"): el["class"] = ["r-v"]
    # .note / .note.danger pass through unchanged (same class names in v2)
    return "".join(str(c) for c in body.children).strip()

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def build(prop):
    html = io.open(f"{ROOT}/{prop}/v1.html", encoding="utf-8").read()
    s = BeautifulSoup(html, "html.parser")
    name = s.select_one(".hero-title").get_text(strip=True)
    addr = s.select_one(".hero-addr").get_text(strip=True)

    # summary: door code + wifi
    door = s.select_one(".summary-deep .summary-value").get_text(strip=True)
    neut = s.select_one(".summary-neutral")
    wlab = neut.select_one(".summary-label").get_text(strip=True)   # "WiFi — Net"
    wval = neut.select_one(".summary-value").get_text(strip=True)   # "Password — pass"
    wifi_net = wlab.split("—")[-1].strip()
    wifi_pass = wval.split("—")[-1].strip()

    # map pills
    chips = []
    for a in s.select(".map-pill"):
        txt = a.find(string=True).strip()  # "📍 House"
        parts = txt.split(None, 1)
        ico = parts[0]; lab = parts[1] if len(parts) > 1 else ""
        chips.append((ico, lab, a["href"]))

    # pills -> cards grouped
    groups = {k: [] for k, _ in SECTION_LABELS}
    provided_html = bring_html = ""
    lock_type = ""
    sleeps_chip = ""
    for pill in s.select(".pill"):
        head = pill.select_one(".pill-header").get_text(strip=True)
        body = pill.select_one(".pill-body")
        toks = head.split(None, 1)
        icon = toks[0]; raw_title = toks[1] if len(toks) > 1 else head
        title = NICE.get(raw_title.upper(), raw_title.title())
        sec = section_of(raw_title)
        if "GETTING IN" in raw_title.upper():
            lr = pill.select_one(".info-label")
            for r in pill.select(".info-row"):
                if "lock type" in r.get_text().lower():
                    lock_type = r.select_one(".info-value").get_text(strip=True)
        if "SLEEPING" in raw_title.upper():
            b = body.find("b")
            if b and "sleeps" in b.get_text().lower(): sleeps_chip = b.get_text(strip=True)
        inner = translate_body(body)
        alert = "alert" if sec == "badges" else ""
        card = (f'<div class="card {alert}">\n<h3><span class="ico">{icon}</span>{esc(title)}</h3>\n{inner}\n</div>')
        if sec == "provided": provided_html = inner
        elif sec == "bring": bring_html = inner
        else: groups[sec].append(card)

    # checkout checklist
    items = []
    for li in s.select(".checklist li"):
        t = li.get_text(" ", strip=True)
        t = re.sub(r"\s*at (610-621-0769|814-936-3068)", "", t)
        items.append(t)
    notes_el = s.select_one(".notes")
    notes = notes_el.get_text(" ", strip=True) if notes_el else ""

    # ---- assemble ----
    SMS = ("sms:+18149363068?&body=Hi%20Will%2C%20I'm%20at%20the%20"
           + name.replace(" ", "%20") + "%20house%20and%20had%20a%20question%3A%20")
    CO_SMS = ("sms:+18149363068?&body=Hi%20Will%2C%20we've%20checked%20out%20of%20the%20"
           + name.replace(" ", "%20") + "%20house.%20Thank%20you!")
    MSG_SVG = '<svg viewBox="0 0 24 24"><path d="M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2z"/></svg>'
    CALL_SVG = '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg>'
    base = "https://a799608.github.io/mvp-guest-guides/" + prop + "/"

    chips_html = "\n".join(
        f'<a class="chip" target="_blank" rel="noopener" href="{esc(h)}"><span class="c-ico">{ico}</span>{esc(lab)}<span class="c-sub">map</span></a>'
        for ico, lab, h in chips)

    sections_html = ""
    for key, label in SECTION_LABELS:
        if not groups[key]: continue
        sections_html += f'\n<div class="section-label">{label}</div>\n' + "\n".join(groups[key])
    # provisions two-col
    if provided_html or bring_html:
        sections_html += ('\n<div class="section-label">Provisions</div>\n<div class="cols">'
            f'\n<div class="card"><h3><span class="ico">✅</span>Provided</h3>{provided_html}</div>'
            f'\n<div class="card"><h3><span class="ico">🎒</span>Bring</h3>{bring_html}</div>\n</div>')
    # checkout (the "Text Will" item also opens a prefilled checkout text on tap)
    def _li(i):
        if "text will" in i.lower():
            return f'<li data-sms="{CO_SMS}"><span class="box"></span><span>{esc(i)} <em style="color:var(--gold-soft);font-style:normal">— tap to text</em></span></li>'
        return f'<li><span class="box"></span><span>{esc(i)}</span></li>'
    checks = "\n".join(_li(i) for i in items)
    sections_html += ('\n<div class="section-label">Before You Go</div>\n<div class="card">'
        '\n<h3><span class="ico">📋</span>Check-Out Checklist</h3>\n<ul class="check">\n'
        + checks + '\n</ul>' + (f'\n<div class="note">{esc(notes)}</div>' if notes else "") + '\n</div>')
    # explore
    sections_html += ('\n<div class="section-label">Explore</div>\n<div class="card">'
        '\n<h3><span class="ico">🗺️</span>Pocono Area Guide</h3>'
        '\n<p>Community amenities (pool, beach, courts) plus local favorites — Jim Thorpe, '
        'Hickory Run State Park, waterfalls, breweries, and more.</p>'
        '\n<a class="btn btn-ghost" style="margin-top:10px;display:inline-flex;flex:0 0 auto;padding:11px 20px" href="../area/index.html">View Area Guide →</a>\n</div>')

    meta_chips = '<span>Check-in 4 PM</span><span>Check-out 12 PM</span>' + (f'<span>{esc(sleeps_chip)}</span>' if sleeps_chip else "")
    door_sub = esc(lock_type) if lock_type else "Keyless entry"

    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>{esc(name)} — MVP Rentals Guest Guide</title>
<meta property="og:type" content="website">
<meta property="og:site_name" content="MVP Rentals">
<meta property="og:url" content="{base}">
<meta property="og:title" content="{esc(name)} — MVP Rentals Guest Guide">
<meta property="og:description" content="Your guest guide for the {esc(name)} home — door code, WiFi, amenities, and Pocono area tips.">
<meta property="og:image" content="{base}hero.jpg">
<meta property="og:image:alt" content="{esc(name)} — MVP Rentals">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{base}hero.jpg">
{STYLE}
</head>
<body>

<header class="hero" style="background-image:url('hero.jpg')">
  <div class="hero-brand"><span class="dot"></span>MVP Rentals</div>
  <div class="hero-inner">
    <h1>{esc(name)}</h1>
    <div class="addr">{esc(addr)} · Albrightsville, PA</div>
    <div class="hero-meta">{meta_chips}</div>
  </div>
</header>

<div class="wrap">
  <div class="keycard">
    <div class="key-grid">
      <div class="key-tile" data-copy="{esc(door)}"><span class="k-copy">tap to copy</span>
        <div class="k-label">Door Code</div><div class="k-val">{esc(door)}</div>
        <div class="k-sub">{door_sub}</div></div>
      <div class="key-tile" data-copy="{esc(wifi_pass)}"><span class="k-copy">tap to copy</span>
        <div class="k-label">WiFi Password</div><div class="k-val">{esc(wifi_pass)}</div>
        <div class="k-sub">Network: {esc(wifi_net)}</div></div>
    </div>
    <div class="key-actions">
      <a class="btn btn-gold" href="{SMS}">{MSG_SVG}Message Will</a>
    </div>
  </div>

  <div class="maps">
{chips_html}
  </div>

  <p class="intro">Welcome to the Poconos! We've put together everything you need for an easy, comfortable stay. Anything at all, just tap <b>Message Will</b> below.</p>
{sections_html}

  <footer>MVP Rentals · {esc(name)} · {esc(addr)}, Albrightsville PA</footer>
</div>

<div class="toast" id="toast">Copied ✓</div>
<script>
var toast=document.getElementById("toast"),tT;
document.querySelectorAll(".key-tile").forEach(function(t){{t.addEventListener("click",function(){{
  var v=t.getAttribute("data-copy");
  if(navigator.clipboard){{navigator.clipboard.writeText(v).catch(function(){{}});}}
  toast.textContent="Copied "+v+" ✓";toast.classList.add("show");
  clearTimeout(tT);tT=setTimeout(function(){{toast.classList.remove("show");}},1400);}});}});
document.querySelectorAll(".check li").forEach(function(li){{li.addEventListener("click",function(){{li.classList.toggle("done");var u=li.getAttribute("data-sms");if(u){{window.location.href=u;}}}});}});
</script>
</body>
</html>"""
    # carry-over v1 content typos
    for a, bb in {"Dody wash": "Body wash", "2 Twins beds": "2 Twin beds"}.items():
        out = out.replace(a, bb)
    io.open(f"{ROOT}/{prop}/index.html", "w", encoding="utf-8").write(out)  # LIVE
    io.open(f"{ROOT}/{prop}/v2.html", "w", encoding="utf-8").write(out)     # mirror
    # report
    more = [c for c in groups["more"]]
    moretitles = re.findall(r'<h3><span class="ico">[^<]*</span>([^<]*)</h3>', "\n".join(more))
    print(f"{prop:10s} door={door} wifi={wifi_net}/{wifi_pass} sleeps='{sleeps_chip}' chips={len(chips)} "
          f"checkout_items={len(items)} GoodToKnow={moretitles}")

for p in PROPS:
    build(p)
print("\nall v2 files generated")
