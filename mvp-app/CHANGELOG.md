# MVP App Changelog

Significant changes to the iPhone PWA launcher (`mvp-app/`). Newest first.

---

## 2026-05-24 -- v2: Financial Watch tile

### Added

**Financial Watch wide tile** inserted between the 2x2 main grid and the existing Personal Dashboard wide tile.

- Icon: chart (&#128202;).
- Link target: `financial-watch.html` (relative, hosted in this folder).
- Tile style: `wide` (full grid width, single-row, icon + label horizontal).

**`financial-watch.html`** added to the folder -- a verbatim copy of `Dashboard/mvp_financial_watch.html` from the `mvp-rentals` repo. Self-contained: all CSS inline, all data embedded, one base64-embedded MVP logo, zero external src/href references. Serving size 48,949 bytes.

### Changed

Footer version stamp `v1 - 2026-05-15` -> `v2 - 2026-05-24`.

### Why

Will requested the Financial Watch be reachable from his iPhone alongside the other operations dashboards. The Financial Watch dashboard previously lived only as a local HTML file on Will's desktop (`Dashboard/mvp_financial_watch.html` in the `mvp-rentals` repo) and had no way to be opened from a phone. Hosting it under the PWA folder gives the phone a stable URL.

### Implementation reference

- The wide-tile style is the same `class="tile wide"` already used by the Personal Dashboard tile. Spans `grid-column: 1 / -1`, drops the column flex layout, and lays out icon + label side-by-side.
- Source file copied via `cp` from the OneDrive-tracked `Dashboard/` folder. Since the HTML is fully self-contained, no asset paths needed rewriting.

### Refresh

The Financial Watch HTML embeds a snapshot of the data at generation time. To refresh, re-run `python Dashboard/mvp_financial_watch.py` in the `mvp-rentals` repo and re-copy the output here. See `README.md` for the exact sequence.

### Reverting

To remove the Financial Watch tile from the launcher:

1. In `mvp-app/index.html`, delete the four-line `<a class="tile wide" href="financial-watch.html">...</a>` block (sits between the Guest Guides tile and the Personal Dashboard wide tile).
2. Optionally delete `mvp-app/financial-watch.html` (~49 KB).
3. Bump the footer version stamp.
4. Commit and push.

### Source commit

`5c2640d` on `main`. Diff: 2 files changed, 596 insertions, 1 deletion (the 596 insertions are the bulk of the Financial Watch HTML).

---

## 2026-05-15 -- v1: Phase 1 PWA launchpad

### Added

Initial release of the iPhone home-screen launcher.

- **`index.html`** -- 2x2 grid of square tiles (Cleaning Operations / Reservation Lifecycle / Occupancy Calendar / Guest Guides) plus one full-width wide tile (Personal Dashboard, marked desktop-only). MVP green/gold theme, iOS-safe-area-aware padding, tap-feedback animation. All CSS inline.
- **`manifest.json`** -- PWA manifest declaring `display: standalone`, portrait orientation, MVP green theme + background color, and three icon sizes.
- **`icons/icon-180.png`**, **`icons/icon-192.png`**, **`icons/icon-512.png`** -- launcher icons. 180 is the iOS apple-touch-icon; 192 and 512 are the PWA standards.

### Why

Will wanted one-tap access to the MVP operations dashboards from his iPhone without typing URLs each time and without launching Safari + tab juggling. The Add-to-Home-Screen PWA flow on iOS gives a native-app-like feel (full-screen, custom icon, splash) with zero Apple Developer cost and no App Store review.

### Source commit

`11675b7` on `main`.
