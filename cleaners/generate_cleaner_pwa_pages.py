"""generate_cleaner_pwa_pages.py

Generates per-cleaner landing pages at /cleaners/<token>/ that are:
  (1) Installable as a PWA on iOS Safari (Share -> Add to Home Screen) so the
      cleaner gets the MVP green-and-gold icon on their home screen labeled
      with their first name.
  (2) Auto-redirect to the GAS CleanerDash web app after a 2.5s pause so the
      cleaner has time to install if they want.
  (3) Have a manual "Open Dashboard" button as a fallback.

Run from C:/temp/mvp-guest-guides/cleaners/ :
    python generate_cleaner_pwa_pages.py

Idempotent. Re-run when cleaners are added/removed/renamed.

Then commit + push the repo. GitHub Pages serves the new pages within ~60s.
"""
import json
import pathlib

GAS_BASE = (
    "https://script.google.com/macros/s/"
    "AKfycbww4No3u0KRRqWcbMRfqNzgapHwLYvjA8t3RBUCe56dU82q11rw2tGQTr4EZjoTUw_E"
    "/exec?token="
)

# Folder token -> first-name to display on the home-screen icon label.
# Token is the lowercased name with spaces stripped (Will -> will,
# Michelle Pow -> michellepow). First name is what iOS uses for the
# Add-to-Home-Screen label via apple-mobile-web-app-title / short_name.
FIRST_NAMES = {
    "will": "Will",
    "michelle": "Michelle",
    "michellepow": "Michelle",
    "ogmichelle": "Michelle",
    "newmichelle": "Michelle",
    "brittany": "Brittany",
    "lacy": "Lacy",
    "maryanne": "MaryAnne",
    "jen": "Jen",
    "sam": "Sam",
    "brandee": "Brandee",
    "jack": "Jack",
}

CLEANERS_DIR = pathlib.Path(__file__).parent


def make_index_html(first_name, gas_url):
    # Single triple-quoted template; only simple {token} substitution at the end.
    # Curly braces in CSS/JS are doubled so .format() leaves them alone.
    tpl = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>MVP Schedule - {first_name}</title>

<!-- PWA manifest -->
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#0d2e10">

<!-- iOS Safari Add-to-Home-Screen -->
<link rel="apple-touch-icon" sizes="180x180" href="/mvp-guest-guides/mvp-app/icons/icon-180.png">
<link rel="apple-touch-icon" sizes="192x192" href="/mvp-guest-guides/mvp-app/icons/icon-192.png">
<link rel="apple-touch-icon" sizes="512x512" href="/mvp-guest-guides/mvp-app/icons/icon-512.png">
<link rel="icon" type="image/png" sizes="192x192" href="/mvp-guest-guides/mvp-app/icons/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{first_name}">

<style>
  html, body {{ margin: 0; padding: 0; min-height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0d2e10; color: #fff; }}
  .wrap {{ min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 24px; box-sizing: border-box; }}
  .brand {{ font-size: 13px; letter-spacing: 3px; color: #c8990a; text-transform: uppercase; margin-bottom: 8px; }}
  .name {{ font-size: 32px; font-weight: 800; letter-spacing: 1px; margin: 0 0 4px; }}
  .sub {{ font-size: 14px; opacity: 0.7; margin-bottom: 28px; }}
  .btn {{ display: inline-block; background: #c8990a; color: #0d2e10; padding: 14px 32px; border-radius: 8px; font-weight: 800; font-size: 15px; letter-spacing: 0.5px; text-decoration: none; border: 2px solid #c8990a; }}
  .btn:active {{ background: #b8890a; }}
  .hint {{ margin-top: 24px; font-size: 11px; opacity: 0.55; line-height: 1.5; max-width: 320px; }}
  .countdown {{ margin-top: 16px; font-size: 11px; opacity: 0.45; }}
</style>

<script>
  // Auto-open the dashboard after a short pause so the cleaner has time to
  // tap Share -> Add to Home Screen if they want the MVP icon on their phone.
  var DEST = "{gas_url}";
  var DELAY_MS = 2500;
  setTimeout(function() {{ window.location.replace(DEST); }}, DELAY_MS);
</script>
</head><body>
<div class="wrap">
  <div class="brand">MVP Rentals</div>
  <h1 class="name">{first_name}</h1>
  <div class="sub">Cleaning Schedule</div>
  <a class="btn" href="{gas_url}">Open Dashboard</a>
  <div class="hint">On iPhone: tap the Safari <strong>Share</strong> button below, then <strong>Add to Home Screen</strong> to install this as an app.</div>
  <div class="countdown">Opening in a moment&hellip;</div>
</div>
</body></html>
"""
    return tpl.format(first_name=first_name, gas_url=gas_url)


def make_manifest_json(first_name, token):
    return json.dumps({
        "name": "MVP Schedule - " + first_name,
        "short_name": first_name,
        "start_url": "/mvp-guest-guides/cleaners/" + token + "/",
        "scope": "/mvp-guest-guides/cleaners/" + token + "/",
        "display": "standalone",
        "background_color": "#0d2e10",
        "theme_color": "#0d2e10",
        "icons": [
            {"src": "/mvp-guest-guides/mvp-app/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/mvp-guest-guides/mvp-app/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2)


def main():
    rows = []
    for d in sorted(CLEANERS_DIR.iterdir()):
        if not d.is_dir():
            continue
        token = d.name
        if token.startswith(".") or token.startswith("_"):
            continue
        first_name = FIRST_NAMES.get(token, token.capitalize())
        gas_url = GAS_BASE + token

        idx_path = d / "index.html"
        man_path = d / "manifest.webmanifest"

        idx_path.write_text(make_index_html(first_name, gas_url), encoding="utf-8", newline="\n")
        man_path.write_text(make_manifest_json(first_name, token), encoding="utf-8", newline="\n")

        rows.append((token, first_name))
        print("  {0:18s} -> {1}".format(token, first_name))

    print("Total cleaners: {0}".format(len(rows)))


if __name__ == "__main__":
    main()
