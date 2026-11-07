# MVP Rentals iPhone PWA Launcher

iPhone home-screen launcher for the MVP Rentals operations suite. Installed via Safari's **Add to Home Screen** feature, it appears as a native-looking app icon, launches full-screen (no Safari chrome), and gives one-tap access to every operations dashboard.

## Live URL

https://a799608.github.io/mvp-guest-guides/mvp-app/

## Install on iPhone

1. Open Safari on iPhone.
2. Navigate to the live URL above.
3. Tap the **Share** icon (square with up-arrow).
4. Scroll down and tap **Add to Home Screen**.
5. Tap **Add** in the upper-right.

An MVP-branded icon appears on the home screen. Tapping it opens the launcher full-screen, with the iOS status bar honoring the MVP green theme color.

## Tiles

Listed in display order. Tiles marked "wide" span both columns of the grid.

| # | Tile | Type | Target |
|---|------|------|--------|
| 1 | Cleaning Operations (primary/gold) | square | Cleaning Dashboard GAS web app |
| 2 | Reservation Lifecycle | square | Reservation Lifecycle GAS web app (`?token=will`) |
| 3 | Occupancy Calendar | square | Occupancy Calendar GAS web app (`?token=will`) |
| 4 | Guest Guides | square | `a799608.github.io/mvp-guest-guides/` |
| 5 | Financial Watch | wide | `financial-watch.html` (hosted here, in this folder) |
| 6 | Personal Dashboard (desktop only) | wide | `file:///...Personal Dashboard/index.html` — opens only on Will's desktop |

The Cleaning Operations tile uses the gold/cream primary style; every other square uses the green theme. Tiles 5 and 6 stack at the bottom as full-width "wide" tiles.

## Architecture

Single-page static PWA. No build step, no JavaScript framework.

- **`index.html`** — the launcher itself. Contains all CSS inline. Tile URLs are hard-coded `<a href>` links. iOS-specific meta tags (`apple-touch-icon`, `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`) drive the native-app-like behavior when launched from the home screen.
- **`manifest.json`** — PWA manifest. Declares `display: standalone`, `orientation: portrait`, theme color, and 192/512 px icons.
- **`icons/`** — three PNG icons: `icon-180.png` (iOS apple-touch-icon), `icon-192.png` (PWA standard), `icon-512.png` (PWA standard + maskable).
- **`financial-watch.html`** — copy of `Dashboard/mvp_financial_watch.html` from the `mvp-rentals` repo. Self-contained HTML (embedded data, no external refs), so it works as a static file. Refresh by re-running `python Dashboard/mvp_financial_watch.py` in the source repo and re-copying the output here.

## Updating

1. Edit `mvp-app/index.html` (add/remove/reorder tiles, change copy).
2. Bump the footer version stamp: `<footer>v<N> - YYYY-MM-DD</footer>`.
3. Add a CHANGELOG entry (`mvp-app/CHANGELOG.md`).
4. `git add mvp-app/ && git commit && git push`.
5. GitHub Pages publishes within ~60 seconds.

If Pages doesn't publish within 60 seconds, the build may be zombied. Manually re-trigger via `gh api -X POST repos/a799608/mvp-guest-guides/pages/builds` and a fresh build will queue immediately.

## Refresh the Financial Watch data

The Financial Watch HTML embeds a snapshot of the data at the time it was generated. To refresh:

```
cd "C:/Users/wmmmo/OneDrive/Desktop/Claude/MVP Rentals/MVP Rentals Claude Project File/Dashboard"
git pull
python mvp_financial_watch.py
cp mvp_financial_watch.html C:/temp/mvp-guest-guides/mvp-app/financial-watch.html
cd C:/temp/mvp-guest-guides
git add mvp-app/financial-watch.html
git commit -m "chore(mvp-app): refresh Financial Watch snapshot"
git push
```

A future enhancement could schedule this via Windows Task Scheduler nightly, similar to the `MVP_Pricing_Daily_Refit` task that already refreshes the rate-table sheet.

## Privacy / security note

The launcher is served from a public GitHub Pages site. The dashboard URLs it links to are themselves protected only by long obscure URLs (`?token=will` style). The Financial Watch HTML is publicly served once committed — anyone with the URL can see portfolio revenue numbers. This matches the existing security model for the other dashboards. If stricter access control is required later, the URLs would need to move behind a Google sign-in gate (e.g., Apps Script's `Session.getActiveUser().getEmail()` allowlist).

## Source

- Repo: https://github.com/a799608/mvp-guest-guides (`main` branch, `mvp-app/` folder)
- Sibling-folder source for Financial Watch: https://github.com/a799608/mvp-rentals (`master` branch, `Dashboard/mvp_financial_watch.py`)
