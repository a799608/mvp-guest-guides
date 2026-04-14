# MVP Rentals Guest Guides

Live guest-facing property guides for 6 Pocono Mountain vacation rentals.

## Live URLs

- **Landing Page:** https://a799608.github.io/mvp-guest-guides/
- **Petrarch:** https://a799608.github.io/mvp-guest-guides/petrarch/
- **Wylie:** https://a799608.github.io/mvp-guest-guides/wylie/
- **Pound:** https://a799608.github.io/mvp-guest-guides/pound/
- **MacCauley:** https://a799608.github.io/mvp-guest-guides/maccauley/
- **Milton:** https://a799608.github.io/mvp-guest-guides/milton/
- **Trails:** https://a799608.github.io/mvp-guest-guides/trails/

## How It Works

Each property has its own `index.html` page with pill-shaped info cards covering:
- Check-in info (door codes, lock types, parking)
- Sleeping arrangements
- House rules (The Nos)
- Climate controls (Heat, A/C, Fireplace)
- Kitchen (Charcoal Grill, Hood Vent, Garbage Disposal/Firepit/Gameroom)
- Trash collection with map link
- What's Provided / What to Bring
- Pets policy
- Septic system warning
- Checkout checklist

## Pill Layout Editor

Each page has an **Edit Layout** button (top right) for repositioning pills:

1. Click **Edit Layout** (click twice — first loads library, second activates)
2. Drag pills to move them
3. Drag edges/corners to resize
4. Click **Save Layout** to save positions to clipboard
5. The clipboard watcher or save.html helper saves to the file

For the save to write to the file, the local server must be running:
```
cd visual_preview
python server.py
```
This starts a server on http://localhost:8765 with POST support for saving layouts.

## Map Links

Each property page has map pills linking to:
- **House** — property-specific coordinates
- **Trash** — community collection center (41°00'43.0"N 75°35'38.8"W)
- **Beach** — community beach
- **Pool** — community pool
- **Marina** — community marina
- **Courts** — tennis/basketball courts

## Property-Specific Content

These pills have unique wording per property (do NOT standardize across properties):
- Getting In (door codes, lock types, parking)
- Front Door & Pet Gates
- Sleeping Arrangements
- Fireplace
- A/C
- Pets
- Firepit / Garbage Disposal / Gameroom Items

These pills are standardized across all properties:
- Trash Collection (bullets + red warning)
- Septic System (red warning)
- Heat (bullets)
- Charcoal Grill (bullets)
- Hood Vent (bullets)
- The Nos
- What's Provided
- What to Bring

## Checkout Checklist Differences

- **Petrarch:** includes "Front door key to kitchen counter"
- **All others:** no front door key item
- **Trails & Milton:** "Remotes returned to coffee table"
- **Pound & Wylie:** "Remotes returned to entertainment center"
- **Petrarch & MacCauley:** "Remotes returned to coffee table and bedroom dresser"

## File Structure

```
visual_preview/
├── index.html              # Landing page (admin use — links to all properties)
├── assets/
│   ├── style.css           # Shared styles
│   ├── enhance.css         # Enhanced styles
│   └── editor.js           # Pill layout editor (drag/resize/save)
├── petrarch/index.html
├── wylie/index.html
├── pound/index.html
├── maccauley/index.html
├── milton/index.html
├── trails/index.html
├── area/index.html         # Community area guide
├── server.py               # Local dev server with POST save support
└── save.html               # Clipboard save helper
```

## Deployment

Hosted on GitHub Pages from the `main` branch. Push to deploy:
```
git add -A
git commit -m "description of changes"
git push origin main
```
Pages update within 1-2 minutes after push.

## Guest Usage

Send guests the direct link to their property before arrival. Example:
> "Here's your guest guide for your stay: https://a799608.github.io/mvp-guest-guides/trails/"

Guests cannot navigate to other properties — the All Properties link has been removed from individual pages. The landing page is for admin use only.
