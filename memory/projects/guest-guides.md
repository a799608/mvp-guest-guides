# Guest Guides

**Also called:** the guides, property pages
**Status:** Live, https://a799608.github.io/mvp-guest-guides/<prop>/

## What It Is
One mobile guide per property. Guests get their property's direct link before arrival; they can't navigate to other properties.

## How to change
1. Edit `<prop>/v1.html` (content) or `build_v2.py` (all six).
2. `python build_v2.py`
3. QA with `phone_qa/phone_qa.py`
4. Add a CHANGELOG.md entry (Will's quote, changes, QA counts, revert note)
5. Deploy from `main` (Pages updates in 1-2 min)

## Checkout differences
- Petrarch: front door key on kitchen counter
- Trails & Milton: remotes to coffee table
- Pound & Wylie: remotes to entertainment center
- Petrarch & MacCauley: remotes to coffee table and bedroom dresser

## Firepits
Trails, Milton, Pound, MacCauley, Petrarch. Fires are allowed in TT (since 2026-11-01).

## Codes
Never in HTML. Form 2 shows them only during check-in through check-out. See docs/door_code_access.md.
