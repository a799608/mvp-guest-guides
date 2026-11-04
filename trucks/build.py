# -*- coding: utf-8 -*-
"""2WD truck board. Every row: verified live (not sold), <=25 mi from FORTY FORT ONLY,
and listed within ~1 month unless availability was confirmed another way."""
import html, datetime, os

OUT_LOCAL = r"C:\Users\wmmmo\OneDrive\Desktop\truck_deals.html"
OUT_WEB   = r"C:\temp\mvp-guest-guides\trucks\index.html"

# dt, price, vehicle, miles, town, dist, listed, insp, flag, take, url
D = [
("2WD",3150,"2010 Chevy Silverado 1500 ext cab LTZ 5.3","138,333","Plains","1.5","4 weeks ago","not mentioned","",
 "BEST ON THIS PAGE. The only ad that states 2WD outright, states a clean title, and describes the frame as good. An LTZ ext cab at this mileage normally brings $6-7k; the seller tells you why it is cheap - the bed and tow hitch are rotted. His words: 'runs excellent, smooth engine and tranny, mechanically perfect.' Buy the running gear, plan on a bed. Put it on a lift before you pay - 'frame looks good' from a dealer is a sales opinion, not an inspection.",
 "https://www.facebook.com/marketplace/item/2055507101750694/"),
("2WD",4495,"2014 Ford F-150 XL reg cab 5.0 V8, 8ft bed","236,000","Wilkes-Barre","1.9","Jun 10 - STILL ON THE LOT, verified today","not mentioned","",
 "BEST PAPERWORK. Clean title, ONE owner, ZERO accidents. 2WD confirmed three ways including the NHTSA VIN decode. It is the oldest listing here, so I checked Gene Scatena's own inventory page today - still listed, no sold marker, still $4,495. Cut twice since June ($4,995 -> $4,795 -> $4,495), so open at $3,500. THE RISK IS THE ENGINE: the 2011-14 5.0 has known cam phaser / timing chain wear that shows up as a rattle on a COLD start. Show up unannounced and start it yourself stone cold. Rattle = walk.",
 "https://www.cars.com/vehicledetail/e5118636-bcbd-4f78-b0f5-a095d06621c0/"),
("2WD",3599,"2003 Ford F-250 long bed work truck, gas","220,463","Old Forge","10.1","1 week ago","not mentioned","CAUTION",
 "Dealer truck. Seller: 'runs and drives, not the prettiest but cheap basic transportation' - sold 'as is / where is / no warranty / no financing.' A gas Super Duty at 220k is at the end of its working life and you own every problem the second you sign. Fine as a hauler, wrong as a daily.",
 "https://www.facebook.com/marketplace/item/1394695962204218/"),
("2WD",4800,"1992 Ford F-150 FX2","93,563","Moosic","9.2","2 weeks ago","not mentioned","CAUTION",
 "FX2 trim means 2WD. Genuinely low miles for the year and it will photograph well, but it carries a NEW JERSEY TITLE - PA title transfer and PA inspection before it is legal in your driveway. A 34-year-old truck with a nine-word description at $4,800 is a collector price for an unknown.",
 "https://www.facebook.com/marketplace/item/1093991103056621/"),
("2WD",4500,"2008 Ford F-150 FX2","162,000","Wilkes-Barre","1.9","2 days ago","not mentioned","RISK",
 "FX2 = 2WD, and that is the only good news. Seller: 'New motor spun baring warenty is transferable Motor is under warranty.' That is a replacement engine that FAILED. The ad never once says the truck runs, and it is priced like a normal running F-150. Skip it.",
 "https://www.facebook.com/marketplace/item/3067244630287769/"),
("2WD",2000,"2005 Dodge Dakota crew cab SLT","144,465","Kingston","1.2","6 days ago","EXPIRES 10/26 - ~4 wks","",
 "2WD CONFIRMED BY WILL. A mile from your door and the only truck here with a current PA sticker - but read the date: it EXPIRES October 2026, about four weeks out. PA stickers run 12 months, so it passed roughly a year ago, not recently. Seller: 'Has cracked in windshield but passed inspection. Has exhaust manifold leak. 144000 original miles. Inspected until 10/26.' A crack in the driver's sweep is a PA fail item and cracks spread, so you may be buying glass in October. Ask three things: what month it was inspected, exactly where the crack sits, and does he have the receipt. Then ask 2WD or 4WD - that still decides whether it belongs on this list at all.",
 "https://www.facebook.com/marketplace/item/2290365621797573/"),
("ASK",2500,"1997 Chevy Silverado 1500 ext cab 5.7","250,000","Edwardsville","1.6","4 days ago","not mentioned","",
 "A mile and a half away, clean title, freshly listed. Seller says 'Does turn key and go' with 'some dings and dents.' 250k on a 5.7 is not automatically fatal - they run a long time - but at that mileage you are buying a truck with a finite tail. Ask drivetrain.",
 "https://www.facebook.com/marketplace/item/2953758474969533/"),
("ASK",2200,"2005 Dodge Dakota","240,000","Ashley","4.3","3 weeks ago","not mentioned","",
 "Honest seller running it as his own daily: 'put well over 10k miles on it since December... rust isn't terrible only the inner wheel wells inside the bed are bad.' New rotors, pads, belt and idler pulley; could use tires. 240k is the catch. Ask drivetrain.",
 "https://www.facebook.com/marketplace/item/1431882408820276/"),
("ASK",3000,"2012 GMC Sierra long bed work truck","137,000","Kingston","1.2","4 weeks ago","FAILS inspection","RISK",
 "A mile from you and the mileage is genuinely low, but the seller says it outright: 'Runs well. Won't pass inspection due to rusting underneath.' Rust underneath that fails inspection is frame or body-mount rot. You would be buying a truck you cannot legally register.",
 "https://www.facebook.com/marketplace/item/1809454423377692/"),
("ASK",4300,"2002 Nissan Frontier king cab","206,000","Hazleton","22.3","3 weeks ago","not mentioned","VERIFY",
 "Description is genuinely blank - not truncated, there is nothing written. $4,300 for a 206k-mile Frontier is well over market with nothing to justify it. Low priority.",
 "https://www.facebook.com/marketplace/item/1711545160120744/"),
]

# what was removed this pass, and why
DROPPED = [
("SOLD",      1000,"2003 Ford Ranger Edge","Weatherly","23.0","Listing now carries Facebook's SOLD badge.","https://www.facebook.com/marketplace/item/4376763105872743/"),
("TOO OLD",   1900,"2008 Chevy 1500 ext cab","Pittston","5.9","Listed 22 weeks ago. Also states frame rust AND body rust.","https://www.facebook.com/marketplace/item/914531744678852/"),
("TOO OLD",   3000,"2005 Ford F-150 crew","Kingston","1.2","Listed 14 weeks ago, Spanish one-liner description.","https://www.facebook.com/marketplace/item/912305461829279/"),
("TOO OLD",   1500,"1998 Ford Ranger XLT","Thornhurst","16.8","Listed 18 weeks ago.","https://www.facebook.com/marketplace/item/1683560165968705/"),
("TOO OLD",   3000,"2012 Chevy Colorado ext cab","Nanticoke","7.8","Listed 6 weeks ago. Good ad (new trans 2k mi ago, solid frame) - say the word and I will message the seller to confirm it is still there.","https://www.facebook.com/marketplace/item/1037540058758860/"),
("OUT OF RANGE",3200,"2003 Chevy S-10 4-cyl 5-speed","Orefield","46.6","46.6 mi from Forty Fort, not 24.6. Scanner measured from the Albrightsville rental base.","https://www.facebook.com/marketplace/item/4307207462829832/"),
("OUT OF RANGE",3900,"2003 Chevy S-10 Xtreme","Nazareth","47.2","47.2 mi from Forty Fort.","https://www.facebook.com/marketplace/item/1549952159841271/"),
("OUT OF RANGE",3000,"2000 Chevy S-10 4.3","Laurys Station","42.0","42.0 mi from Forty Fort.","https://www.facebook.com/marketplace/item/2098857467384347/"),
("OUT OF RANGE",995,"2001 Ford Ranger supercrew","East Stroudsburg","40.8","40.8 mi from Forty Fort. Blank description anyway.","https://www.facebook.com/marketplace/item/1362993369117079/"),
("OUT OF RANGE",900,"2003 Dodge Dakota SXT","Slatington","38.7","38.7 mi from Forty Fort.","https://www.facebook.com/marketplace/item/1525914532473231/"),
("OUT OF RANGE",1495,"2002 Chevy Silverado 2500HD","Bartonsville","36.4","36.4 mi from Forty Fort.","https://www.facebook.com/marketplace/item/2223898301675336/"),
("OUT OF RANGE",1500,"2000 Chevy S-10 2.2","Nesquehoning","28.4","28.4 mi from Forty Fort. Seller calls it a project with a misfire and rotted floors.","https://www.facebook.com/marketplace/item/2083014052616867/"),
("NOT A RUNNER",4500,"2000 Nissan Frontier XE crew","not stated","8.2","FB spec block says 4x4; ad claims 'extremely low miles' and gives none; account created 2026, no ratings.","https://www.facebook.com/marketplace/item/958228987269748/"),
("NOT A RUNNER",2000,"2011 Dodge Ram 1500 Laramie","Hazleton","19.3","NHTSA VIN decode: 4WD. Has a misfire, and asks $2,500 in the text while listed at $2,000.","https://www.facebook.com/marketplace/item/28128419766775313/"),
("NOT A RUNNER",1200,"2001 Ford Ranger super cab XLT","Kingston","1.9","Ad headline: '*** SEIZED MOTOR ***'.","https://www.facebook.com/marketplace/item/1048167291175173/"),
("NOT A RUNNER",1000,"Chevy Colorado 08 'take as is'","Wilkes-Barre","4.5","'part truck... starts but doesn't drive!'","https://www.facebook.com/marketplace/item/2161278291456324/"),
("NOT A RUNNER",1000,"1989 Dodge Dakota","Nesquehoning","14.6","'Project car NEEDS new brakes. Must be towed.'","https://www.facebook.com/marketplace/item/1769322514256492/"),
("NOT A RUNNER",500,"2005 Dodge Ram 1500 quad cab SLT","Slatington","16.7","'Needs engine work. Is not inspected. Cannot be driven as is.' Also 4WD.","https://www.facebook.com/marketplace/item/788336824072682/"),
("NOT A RUNNER",1234,"2011 Ford F-150 XLT","Slatington","16.7","Ad title is literally 'PART OUT'.","https://www.facebook.com/marketplace/item/2175850082979868/"),
]

FLAGC = {"RISK": "#f6d0d0", "CAUTION": "#fbe6c9", "VERIFY": "#fdf3c9"}
DTC   = {"2WD": ("#1b7f4b", "2WD CONFIRMED"), "ASK": ("#8a6d1f", "ASK DRIVETRAIN")}
DROPC = {"SOLD": "#f2c6c6", "TOO OLD": "#e8e8e8", "OUT OF RANGE": "#e3e9f2", "NOT A RUNNER": "#f2c6c6"}

rows = []
for dt, price, veh, miles, town, dist, listed, insp, flag, take, url in D:
    bg = FLAGC.get(flag, "#e6f4ec" if dt == "2WD" else "#ffffff")
    fg, label = DTC[dt]
    fl = '<span class="flag">%s</span>' % flag if flag else ""
    rows.append((0 if dt == "2WD" else 1, price, """<tr style="background:{bg}" data-key="{k}">
      <td data-label="" class="rmcell"><span class="rm" onclick="rm(this)" title="Remove from list">&#10005; remove</span></td>
      <td data-label="Drivetrain" data-v="{sv}"><b style="color:{fg}">{label}</b></td>
      <td data-label="Price" data-v="{price}" class="num">${price:,}</td>
      <td data-label="Truck"><a href="{k}" target="_blank">{veh}</a> {fl}</td>
      <td data-label="Miles">{miles}</td>
      <td data-label="Town">{town}</td>
      <td data-label="Mi away" data-v="{dist}" class="num">{dist}</td>
      <td data-label="Listed">{listed}</td>
      <td data-label="PA inspection">{insp}</td>
      <td data-label="My take" class="take">{take}</td></tr>""".format(
        bg=bg, k=html.escape(url), sv=(0 if dt == "2WD" else 1), fg=fg, label=label,
        price=price, veh=html.escape(veh), fl=fl, miles=html.escape(miles), town=html.escape(town),
        dist=html.escape(dist), listed=html.escape(listed), insp=html.escape(insp), take=html.escape(take))))
rows.sort(key=lambda r: (r[0], r[1]))
body = "\n".join(r[2] for r in rows)

drop_rows = "\n".join("""<tr style="background:{bg}"><td><b>{why}</b></td><td class="num">${p:,}</td>
  <td><a href="{u}" target="_blank">{v}</a></td><td>{t}</td><td class="num">{d}</td><td class="take">{w}</td></tr>""".format(
    bg=DROPC.get(why, "#eee"), why=html.escape(why), p=p, u=html.escape(u), v=html.escape(v),
    t=html.escape(t), d=html.escape(d), w=html.escape(w))
    for why, p, v, t, d, w, u in DROPPED)

n2wd = sum(1 for r in D if r[0] == "2WD")
nask = sum(1 for r in D if r[0] == "ASK")
# Date the listings were last reopened and verified NOT sold. Update ONLY when you actually re-run the sold/age check.
# Never use datetime.now() here - a plain rebuild would falsely claim the listings were re-checked today.
ts = "Sep 13, 2026 03:24 PM"

CSS = """
body{font-family:-apple-system,Segoe UI,Arial,sans-serif;margin:24px;background:#fafafa;color:#1a1a1a}
h1{margin:0 0 2px} .sub{color:#666;margin:0 0 16px;font-size:14px}
table{border-collapse:collapse;width:100%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.12);font-size:14px}
th,td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}
th{background:#1f4e5f;color:#fff;cursor:pointer;position:sticky;top:0;white-space:nowrap}
th:hover{background:#2e7d8a} .num{text-align:right;white-space:nowrap}
td a{color:#1155cc;text-decoration:none;font-weight:600} td a:hover{text-decoration:underline}
.take{color:#333;max-width:520px} .flag{font-size:11px;font-weight:700;color:#a33;margin-left:6px}
.rm{display:inline-block;border:1px solid #c66;color:#c33;border-radius:12px;padding:1px 8px;font-size:12px;font-weight:700;cursor:pointer;user-select:none}
.rm:hover{background:#c33;color:#fff}
h2{margin:26px 0 8px;font-size:16px;color:#a33}
.hint{color:#888;font-size:12px;margin:6px 0 0}
.msort{display:none;margin:10px 0 6px;font-size:15px;font-weight:600}
.msort select{font-size:16px;padding:6px 8px;border-radius:6px;border:1px solid #bbb;margin-left:6px}
@media (max-width:760px){
  .msort{display:block}
  body{margin:10px;font-size:15px} h1{font-size:20px}
  table{box-shadow:none;background:transparent;font-size:15px}
  thead{display:none}
  tbody tr{display:block;border:1px solid #ddd;border-radius:10px;margin:0 0 12px;padding:10px 12px;
           box-shadow:0 1px 3px rgba(0,0,0,.12)}
  tbody td{display:flex;justify-content:space-between;gap:14px;border:0;padding:4px 0;text-align:left}
  tbody td:before{content:attr(data-label);font-weight:700;color:#5a5a5a;font-size:12px;
                  text-transform:uppercase;letter-spacing:.3px;flex:0 0 auto}
  tbody td.take{display:block} tbody td.take:before{display:block;margin-bottom:3px}
  tbody td.rmcell{justify-content:flex-end;padding-top:6px} tbody td.rmcell:before{display:none}
  .rm{padding:6px 14px;font-size:14px}
  td a{font-size:16px} .take{max-width:none}
}
"""

JS = """
var RK='truck_deals_removed';
function getRm(){try{return JSON.parse(localStorage.getItem(RK)||'[]')}catch(e){return []}}
function rm(el){var tr=el.closest('tr');var k=tr.dataset.key;var l=getRm();if(l.indexOf(k)<0)l.push(k);
try{localStorage.setItem(RK,JSON.stringify(l))}catch(e){}tr.style.display='none';}
function applyRm(){var l=getRm();document.querySelectorAll('#t tbody tr').forEach(function(tr){
if(l.indexOf(tr.dataset.key)>=0)tr.style.display='none';});}
function resetRm(){try{localStorage.removeItem(RK)}catch(e){}
document.querySelectorAll('#t tbody tr').forEach(function(tr){tr.style.display='';});}
document.addEventListener('DOMContentLoaded',applyRm);
function s(c){var tb=document.querySelector('#t tbody');var rs=[].slice.call(tb.rows);
var asc=tb.getAttribute('sc')!=c+'a';rs.sort(function(a,b){
var x=a.cells[c].dataset.v!==undefined?a.cells[c].dataset.v:a.cells[c].innerText;
var y=b.cells[c].dataset.v!==undefined?b.cells[c].dataset.v:b.cells[c].innerText;
var nx=parseFloat(x),ny=parseFloat(y);if(!isNaN(nx)&&!isNaN(ny)){x=nx;y=ny}
return (x>y?1:x<y?-1:0)*(asc?1:-1);});
tb.setAttribute('sc',c+(asc?'a':'d'));rs.forEach(function(r){tb.appendChild(r)});}
"""

doc = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>2WD Trucks under $5k</title>
<meta property="og:title" content="2WD Trucks under $5k - 25 mi of Forty Fort">
<meta property="og:description" content="Two-wheel-drive pickups under $5,000 within 25 miles of Forty Fort - each one checked live for sold status and listing age.">
<meta property="og:image" content="https://a799608.github.io/mvp-guest-guides/og-cover.jpg">
<meta property="og:url" content="https://a799608.github.io/mvp-guest-guides/trucks/">
<style>%CSS%</style></head><body>
<h1>2WD trucks under $5k &mdash; 25 mi of Forty Fort</h1>
<p class="sub">Re-checked %TS% &middot; every listing below was reopened today and is NOT sold &middot;
distances measured from Forty Fort only &middot; %N2WD% with 2WD CONFIRMED, %NASK% that run but need one phone call to confirm drivetrain &middot;
click any header to re-sort</p>
<div class="msort">Sort: <select onchange="s(+this.value)"><option value="1">Drivetrain</option><option value="2">Price</option><option value="6">Miles away</option></select></div>
<p class="hint">&#10005; removes a truck from your list (remembered on this browser) &middot; <a href="#" onclick="resetRm();return false">show removed / reset</a></p>
<table id="t"><thead><tr>
<th></th><th onclick="s(1)">Drivetrain</th><th onclick="s(2)">Price</th><th onclick="s(3)">Truck (opens listing)</th>
<th onclick="s(4)">Miles</th><th onclick="s(5)">Town</th><th onclick="s(6)">Mi away</th><th onclick="s(7)">Listed</th>
<th onclick="s(8)">PA inspection</th><th onclick="s(9)">My take</th>
</tr></thead><tbody>
%BODY%
</tbody></table>
<p class="hint"><b>How drivetrain was decided:</b> green = proven, either the ad states 2WD / 4x2 / FX2 or the NHTSA VIN decode says 4x2.
Amber = the listing publishes no drivetrain anywhere, so it is unconfirmed and needs one question asked. Nothing here was labelled 2WD on a guess.<br>
<b>Shading:</b> green = confirmed 2WD and clean &middot; yellow = verify (thin information) &middot; orange = caution (a stated problem) &middot; red = risk.<br>
<b>Freshness:</b> nothing older than about a month is shown unless availability was confirmed another way - the 2014 F-150 is listed since June but was verified on the dealer's own inventory page today.</p>
<h2>Removed this pass, and why</h2>
<table><thead><tr><th>Why</th><th>Price</th><th>Truck</th><th>Town</th><th>Mi from Forty Fort</th><th>Detail</th></tr></thead><tbody>
%DROP%
</tbody></table>
<p class="hint">Note on the out-of-range group: the scanner measures distance from the nearer of two bases &mdash; Forty Fort and the Albrightsville rental property &mdash; so Lehigh Valley towns looked close when they are not. Every distance on this page is now from Forty Fort alone.</p>
<script>%JS%</script></body></html>"""

doc = (doc.replace("%CSS%", CSS).replace("%JS%", JS).replace("%TS%", ts)
          .replace("%N2WD%", str(n2wd)).replace("%NASK%", str(nask))
          .replace("%BODY%", body).replace("%DROP%", drop_rows))

os.makedirs(os.path.dirname(OUT_WEB), exist_ok=True)
for p in (OUT_LOCAL, OUT_WEB):
    open(p, "w", encoding="utf-8").write(doc)
    print("SAVED:", p)
print("rows:", len(D), "| 2WD:", n2wd, "| ask:", nask, "| dropped:", len(DROPPED))
