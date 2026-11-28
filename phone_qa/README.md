# Phone QA — mobile-rendering checker for the guest guides

Automated mobile QA for the six property guide pages (and any responsive page).
Built 2026-06-03 after a Petrarch mobile-layout bug shipped to the live site
undetected. **Run this before pushing any change to the guide pages.**

## Why it exists

Eyeballing one page in a desktop browser does not catch:
- a sibling page whose CSS quietly diverged (Petrarch was missing
  `position:static` in its mobile `.pill` rule, so its pills never collapsed
  into a single column — they stayed in the shrunken desktop canvas with
  overlapping microscopic text),
- sub-pixel horizontal overflow that triggers a hairline horizontal scroll,
- text rendered below the 12px legibility threshold,
- tap targets smaller than 44px,
- stray dev controls left visible to guests (the `editor.js` "Edit Layout"
  button was showing to every guest).

## What it checks

For each property × width (320 / 390 / 430) × engine (Chromium = Android
Chrome's Blink, WebKit = iOS Safari's engine):

1. **Horizontal overflow** — `documentElement.scrollWidth > innerWidth` (FAIL if > 2px)
2. **Offending elements** — individual elements spilling past the right edge
3. **Viewport meta** — must exist and contain `width=device-width` (FAIL otherwise)
4. **Tiny text** — % of visible text under 12px (FAIL at ≥ 60%, Lighthouse threshold)
5. **Tap targets** — links/buttons/inputs under 44×44 CSS px (warning)
6. **Stray dev UI** — any "Edit Layout / Save Layout" control (warning)

Thresholds sourced from Google Lighthouse mobile-usability audits + Apple HIG.

## Usage

```bash
python phone_qa.py                 # all 6 properties, live URLs, both engines
python phone_qa.py trails petrarch # subset
python phone_qa.py --local         # render from local working-copy files
```

Requires Playwright with both Chromium and WebKit installed:

```bash
python -m playwright install chromium webkit
```

## Output

- Console: one PASS/FAIL line per render.
- `C:/temp/phone_qa_out/report.md` — full table + per-render failures/warnings.
- `C:/temp/phone_qa_out/contact_sheet.html` — visual grid of every screenshot.
- `C:/temp/phone_qa_out/screenshots/<prop>_<engine>_<width>.png`

## Known accepted items (as of 2026-06-03)

- The 4-card summary bar overflows by 2–3px at **320px in WebKit only**
  (legacy iPhone SE / small Android). Every current-generation phone (≥ 375px)
  is clean. Cosmetic; not yet fixed.
- ~18–19% of guide text is under 12px (the small pill captions). Below the 60%
  Lighthouse fail threshold, so it passes; left as a design choice.
