# MVP Rentals QR Codes

Two QR features, both available on **the phone app** (`mvp-app/`) **and the desktop
Personal Dashboard** (separate `mvp-personal-dashboard` repo). Built 2026-06-24.

All codes are generated at **error-correction H** (survives label wear), ~1176px PNG,
and **verified to decode** before use (a label is never printed from a bad code).

---

## 1. Property QR Codes  (one per house -> guide page)

One code per property. Scanning it opens that property's guest-guide page -- the same
link guests get on check-in day (`https://a799608.github.io/mvp-guest-guides/<slug>/`).

Use: print/post in the house, on the parking pass, etc.

| Where | File |
|-------|------|
| Phone app page | `mvp-app/qr.html` (tile: "Property QR Codes") |
| Phone app images | `mvp-app/qr/QR_<Name>.png` |
| Desktop dashboard | "Property QR Codes" section in `index.html` |
| Desktop images | `static/qr/QR_<Name>.png` (personal-dashboard repo) |

Slugs: trails, pound, milton, wylie, maccauley, petrarch. Source of truth for the
URL mapping is `PROPERTY_GUIDE_SLUG` / `property_guide_url()` in mvp-rentals
`Data/mvp_guest_send.py`.

Regenerate all six:
```
cd mvp-app/tools
python make_qr.py --properties ../qr            # phone app images
python make_qr.py --properties "<dashboard>/static/qr"   # desktop images
```

---

## 2. House How-To Codes  (by house -> per-item guide, e.g. fireplace/AC)

A **separate** section, **grouped by house**, that collects per-room how-to codes as
videos are produced. Each code opens a per-item page on the guide site
(e.g. `https://a799608.github.io/mvp-guest-guides/wylie/fireplace/`).

Both surfaces are **data-driven** -- adding a code is a one-line edit, no layout work:

| Where | File | Data object |
|-------|------|-------------|
| Phone app page | `mvp-app/howto.html` (tile: "House How-To Codes") | `HOWTO` |
| Phone app images | `mvp-app/qr/howto/QR_<house>_<item>.png` | |
| Desktop dashboard | "Property How-To Codes" section in `index.html` | `HOWTO_DASH` |
| Desktop images | `static/qr/howto/QR_<house>_<item>.png` (personal-dashboard repo) | |

Houses with no codes show "No how-to codes yet." until populated.

### Adding a how-to code (workflow)

When Will provides a video, he sends three things: **house**, **label**
(e.g. "Fireplace"), and **the video** (link or file). Then:

1. **Build the per-item page** on the guide site, e.g. `wylie/fireplace/index.html`,
   embedding the video. URL becomes `.../mvp-guest-guides/wylie/fireplace/`.
2. **Generate + verify the QR** into both image folders:
   ```
   cd mvp-app/tools
   python make_qr.py "https://a799608.github.io/mvp-guest-guides/wylie/fireplace/" ../qr/howto/QR_wylie_fireplace.png
   # copy the same PNG into the dashboard repo's static/qr/howto/
   ```
3. **Add one entry** to the right house in BOTH data objects:
   ```js
   { label: "Fireplace", url: "https://a799608.github.io/mvp-guest-guides/wylie/fireplace/", img: "qr/howto/QR_wylie_fireplace.png" }
   ```
   (Dashboard `img` path is `static/qr/howto/QR_wylie_fireplace.png`.)
4. **Commit + push** both repos.

---

## Tool: make_qr.py

`mvp-app/tools/make_qr.py` -- generates a QR PNG for any URL and verifies it decodes
back to that URL (zbar preferred, OpenCV fallback; unverified is flagged, failed
verify exits non-zero). See its docstring for usage. Deps:
`pip install qrcode pillow pyzbar`.

## Getting a code onto a label

- **Desktop dashboard:** each card has **Download PNG** (high-res bare code) or
  right-click the image -> **Copy image** straight into the label maker.
- **Phone app:** **press & hold** a code -> Save Image / Share.
- Print-ready labeled sheet of all six property codes (PNG + PDF) was also produced
  ad hoc at `Desktop/MVP_QR_Codes/` on Will's machine.

## Decoder caveat

OpenCV's `QRCodeDetector` intermittently fails to decode perfectly valid codes
(observed on the Wylie property code). **zbar** (pyzbar) matches real phone scanners
and is the trusted verifier; `make_qr.py` prefers it.
