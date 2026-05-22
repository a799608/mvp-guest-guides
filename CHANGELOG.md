# Changelog

Significant changes to the guest guide pages. Newest first.

---

## 2026-05-22 -- AMENITY BADGES pill + Trails A/C wording

### Added

**AMENITY BADGES pill** on ALL 6 property pages (Trails, Wylie, Pound, MacCauley, Milton, Petrarch), positioned directly below GETTING IN in the left column.

- New `cat-alert` color category. Header gradient is amber/orange (`linear-gradient(90deg,#b85c00,#e88a2b)`) so the pill is visually distinct from the green pills around it. Defined inline in each property page CSS block right after the four existing `cat-*` rules.
- Body content (identical across all 6 properties):
  1. Intro paragraph -- community issues one set of badges for the whole year, all guests share that set.
  2. Where-checked paragraph -- pool and beach during operating hours, anyone over age 5 must have one.
  3. Fishing/general use paragraph -- security has been seen asking fishing visitors at the lake, but badges are not required to just be "out and about" the community.
  4. Strict-consequences danger note (red left border) -- $250 replacement per badge, suspension of amenity use after the 3rd lost badge for the year, full security deposit forfeiture on any loss.
  5. Closing apology paragraph -- "I am sorry to have to be so strict about this."
- Pill style: `left:12px;top:159px;width:364px` with NO fixed height. Auto-sizes to its content. (Initial version used `height:320px`; removed because content varies slightly per browser and a fixed value left dead space below the apology line.)
- Left-column pills already below GETTING IN were shifted down to make room. The shift was applied in two passes: +225px when the pill first went in, then an additional +100px when the where-checked paragraph was added. Total displacement is +325px from each property page's pre-edit positions.
- Canvas `min-height` bumped per property to accommodate the longer left column.

### Changed

**Trails A/C pill** wording. The pill height was also bumped from 88px to 135px and the SLEEPING + FIREPIT pills below were shifted down to fit.

Before:
> Large whole-house mini-split unit operated by remote. The remote is kept upstairs near the unit, with a second remote at the mantel.

After:
> Large whole-house mini-split unit operated by remote. The remote is on right of mantel. There is a mode button on the side. A is A/C, H is heat. I am also able to control via a WIFI connection if you would like for me to set the temp for you.

### Why

- The community issues a single set of amenity badges per home for the whole year. Lost badges cost the homeowner $250 each and after 3 losses the community suspends amenity access for the rest of the year. Guests were not aware of this and treated the badges casually; a dedicated, visually distinct pill on the guide sets clear expectations on day 1 of the stay.
- The amber `cat-alert` color was chosen because the existing four `cat-*` headers are all greens or one navy blue, and a fifth green would not stand out. Amber matches the existing gold accents on the page (map pills, summary cards) so it looks intentional rather than alarming.
- The Trails A/C wording was updated because the actual mini-split UI has a mode button on the side of the remote with A (A/C) and H (heat) labels, and Will can remote-set the temperature via WIFI -- guests now know to ask for that if needed.

### Implementation reference

- All 6 property pages share GETTING IN at exactly `left:12px;top:11px;width:364px;height:144px` so bulk insertion below it was clean.
- The left-column shift was driven by regex: any pill with `left < 200 AND top >= 159` was shifted down. Pills in the middle column (`left ~380-590`) and right column (`left ~788-797`) were left alone.
- Mobile breakpoint at max-width:768px collapses all pills to a stacked block layout (overrides `position:absolute` to `static`). Source order matters there -- AMENITY BADGES is inserted in the HTML immediately after GETTING IN so it stacks right after GETTING IN on phones.
- Per-property canvas `min-height` after the change: Trails 820, Wylie 910, Pound 920, MacCauley 1005, Milton 915, Petrarch 1020. (Will need re-tuning if any pill is added or removed.)

### Reverting

To remove AMENITY BADGES from all 6 pages:
1. In each `*/index.html`, delete the `<div class="pill cat-alert" style="left:12px;top:159px;width:364px">...</div></div>` block (one block per file).
2. Unshift left-column pills: any pill with `left < 200 AND top >= 384` should be shifted UP by 325px to return to original positions. (Or just re-run a fresh checkout of the pre-2026-05-22 commit on those files.)
3. Reset canvas `min-height` per property to the pre-edit values: Trails 702, Wylie 700, Pound 800, MacCauley 660, Milton 700, Petrarch 750.
4. Optionally remove the `cat-alert` CSS rule (no harm in leaving it).

### Source commit

`757c48b` on `main`. Diff: 6 files changed, 95 insertions, 34 deletions.