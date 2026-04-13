# Guest Guides Visual Preview (v2)

**Status:** Ready for deployment to GitHub Pages
**Created:** 2026-04-10
**Local preview:** http://localhost:8878/Guest%20Guides/visual_preview/index.html (requires personal-dashboard server)

---

## What This Is

A polished, visually-enhanced HTML version of the MVP Rentals guest guides. These pages replace the plain Google Docs with a branded, mobile-friendly web experience featuring:

- Hero banners with property name, address, and eyebrow tagline
- Summary tiles (Check-in, Check-out, Door Code, WiFi)
- Card-based layout for all sections (Essentials, Climate, Rules, Trash, etc.)
- Interactive check-out checklist (click to check off items)
- Back navigation on every page
- MVP brand colors (#0d2e10 deep green, #1F6224 accent, #C8990A gold, #F8F5EF cream)
- Playfair Display headings, Inter body text (Google Fonts)

## Pages

| Page | File | Description |
|------|------|-------------|
| Landing | index.html | Property chooser with 6 cards + area guide link |
| Trails | trails/index.html | 845 Towamensing Trails Rd |
| Pound | pound/index.html | 28 Pound Lane |
| Milton | milton/index.html | 121 Milton Way |
| Wylie | wylie/index.html | 119 Wylie Circle |
| MacCauley | maccauley/index.html | 82 MacCauley Rd |
| Petrarch | petrarch/index.html | 209 Petrarch Trail |
| Area Guide | area/index.html | Community amenities + local attractions |

## Navigation

- **Landing page:** No back button (top-level entry point)
- **Property pages:** "All Properties" back button links to landing (../index.html)
- **Area guide:** "Back" button uses history.back() to return to whichever property page the guest came from
- **External links:** Open in Maps, Collection Center Map, Weather, etc. all open in new tabs (target="_blank")

## Bug Fixes Applied (2026-04-10)

1. **Trash Collection Center Map link** - Original link used text address "44 Towamensing Trail, ALBRIGHTSVLLE, PA 18210" which Google Maps misresolved to Wilkes-Barre (30 miles north). Fixed on all 7 pages to use coordinate-pinned URL: https://www.google.com/maps/search/44+Towamensing+Trail,+Albrightsville,+PA+18210/@41.0115186,-75.593957,17z. Verified via OpenStreetMap geocoding that 44 Towamensing Trail = the Teepee/community clubhouse at 41.0115, -75.5939.

2. **Call Will CTA removed from intro cards** - The prominent gold "Call Will" button was removed from the welcome section of all 6 property pages. Contact info remains at the bottom of each page for when guests actually need it.

3. **Back navigation added** - All property pages and area guide now have back buttons in the header.

## File Structure



## How It Was Built

1. Restored the original HTML pages from git history (commit a54b778, pre-deletion)
2. Added enhance.css as a visual overlay (does not modify style.css)
3. Added hero sections to each property page with eyebrow tags
4. Converted landing page to full-width hero with property cards
5. Fixed trash collection link across all pages
6. Removed prominent Call Will CTA from intro cards
7. Added back navigation to all sub-pages

## Deployment Plan (Not Yet Executed)

**Target:** GitHub Pages at https://a799608.github.io/mvp-guest-guides/

**Prerequisites:**
- Install GitHub CLI: winget install GitHub.cli
- Authenticate: gh auth login (browser-based auth)
- GitHub username: a799608

**Steps:**
1. Install and authenticate GitHub CLI
2. Create public repo: gh repo create a799608/mvp-guest-guides --public
3. Initialize git in visual_preview/, commit all files
4. Push to GitHub
5. Enable GitHub Pages (main branch, root folder)
6. Verify live URL works
7. Update Guest Guides/README.md with live URL
8. Update Personal Dashboard with link to live guides

**Estimated time:** 15-20 minutes once prerequisites are met

## Content Source

The content in these HTML files was pulled from the Google Docs (source of truth as of 2026-04-07). If content has been updated in the Google Docs since then, those changes are NOT reflected here. After deployment, the HTML pages become the new guest-facing content and should be kept in sync with any property changes.

## Link Audit (2026-04-10)

All links tested and verified:

- 22 external links (Google Maps, weather.gov, poconomountains.com) - all return HTTP 200
- 7 internal page-to-page links - all working
- 7 back navigation buttons - all tested via live click-through in Chrome
- Trash collection center link verified via geocoding to correct location (41.0115, -75.5939)
- Milton and Wylie "Open in Maps" links use coordinate-based URLs (correct location but show coords instead of address name in Maps)
