# Pill Layout Builder — Design Spec

**Date:** 2026-04-11
**Project:** MVP Rentals Guest Guides
**Status:** Approved, ready for implementation

## Overview

A standalone builder page that lets Will visually arrange guest guide pills (cards) on a free-form canvas using drag-to-move and drag-to-resize. No auto-layout, no reflow, no snapping. Like PowerPoint shapes on a blank slide.

The output is position/size data that gets hardcoded into the real guest page.

## Problem

Every CSS layout approach (flexbox, grid, CSS columns) causes automatic reflow when one pill is resized or moved, breaking other pills. The user needs direct, manual control over every pill's position and size with zero auto-behavior.

## Solution

### Builder Page (builder.html)

**Purpose:** Internal tool for Will only. Not seen by guests.

**Canvas:**
- White background, fixed width ~1200px (matching desktop viewport)
- Light dot grid background for visual reference (no snapping)
- Vertically scrollable if layout goes tall

**Pills on canvas:**
- All 15 Petrarch pills rendered with full real content (headers, text, lists, warnings, notes)
- Category color-coded headers (climate=teal-green, kitchen=lime-green, beds=blue-green, default=dark-green)
- Every pill uses `position: absolute` — no flexbox, no grid, no auto-anything
- Pills start in a loose column on the left so nothing overlaps initially

**Interactions:**

| Action | How |
|--------|-----|
| Move | Click and drag from anywhere on the pill body |
| Resize | Drag any of 8 handles (4 corners + 4 edge midpoints) |
| Select | Click a pill — shows handles and size readout (e.g. "280 x 145") |
| Deselect | Click empty canvas |
| Z-order | Clicked pill comes to front |

**Critical rules:**
- NOTHING auto-repositions. Ever.
- No snapping to grid
- No grouping
- No reflow
- Only the pill you are dragging moves or changes size

**Resize handles:**
- 8 handles: 4 corners + 4 edge midpoints
- Visually large enough to grab easily (at least 12x12px)
- Distinct visual treatment (solid colored squares)
- Cursor changes to appropriate resize arrow on hover

**Export:**
- "Export Layout" button in toolbar
- Copies JSON to clipboard: `[{name, id, x, y, width, height}, ...]`
- Also displays the JSON on screen for manual copy
- User pastes data to Claude, who hardcodes it into guest page

### Guest Page Changes (index.html)

**Desktop (>768px):**
- All pills use `position: absolute` with hardcoded x, y, width, height from builder export
- Container has `position: relative` with explicit height
- No flexbox, no grid, no auto-layout

**Mobile (<=768px):**
- `@media` query switches pills to `position: static; width: 100%`
- Pills stack in a single column in DOM order
- Simple, fast, no horizontal scrolling

## Technical Approach

- Single self-contained HTML file (`petrarch/builder.html`)
- All CSS and JavaScript inline — no external dependencies
- Vanilla JS mouse events for drag and resize
- No libraries, no CDN loads

### Drag implementation:
- `mousedown` on pill body — record offset from mouse to pill top-left
- `mousemove` on document — update pill position (left/top)
- `mouseup` on document — stop dragging

### Resize implementation:
- `mousedown` on handle — record which handle, starting mouse position, starting pill rect
- `mousemove` on document — update pill width/height/left/top based on which handle
- `mouseup` on document — stop resizing
- Edge handles constrain to one axis (left/right = width only, top/bottom = height only)
- Corner handles allow both axes simultaneously

### Handle positions:
- Top-left, Top-center, Top-right
- Middle-left, Middle-right
- Bottom-left, Bottom-center, Bottom-right

## Pill Data (Petrarch)

15 pills with the following IDs, names, and categories:

1. getting-in (default) — Door code, lock type, parking, wristbands
2. front-door (default) — Front door mechanism + pet gates
3. trash (default) — Bear warning, collection center map link
4. the-nos (default) — No smoking, fireworks, noise rules
5. pets (default) — Pet fee, furniture, leash rules
6. septic (default) — Septic-safe toilet paper only
7. provided (default) — Linens, detergent, soap, trash bags, TP, paper towels
8. bring (default) — Shampoo, charcoal, firewood, beach/winter/sports gear
9. heat (climate) — Wall thermostats, turn off before A/C
10. ac (climate) — Three units, run all three
11. fireplace (climate) — Remote operation instructions + warnings
12. hood-vent (kitchen) — Run on high when cooking
13. disposal (kitchen) — Push-button on sink cabinet
14. grill (kitchen) — Charcoal grill, clean after use
15. beds (beds) — 2 Queen 2 Twin, sleeps 6

## Rollout Plan

1. Build builder.html for Petrarch
2. Will arranges pills, exports layout data
3. Claude applies layout data to petrarch/index.html
4. Verify desktop layout matches builder arrangement
5. Verify mobile layout stacks correctly
6. Repeat for other 5 properties (each has different content but same builder approach)
7. Push all changes to GitHub in one commit

## Success Criteria

- Will can grab any pill and drag it to any position on canvas
- Will can grab any edge or corner of any pill and resize it freely
- No other pill moves when one is being dragged or resized
- Export produces valid JSON with positions and sizes
- Guest page renders pills at exact exported positions on desktop
- Guest page stacks pills in single column on mobile
