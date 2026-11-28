# Door & WiFi Code Access — how the guide pages gate codes

**Short version:** the door code and WiFi password are **never in these pages' HTML**. They are stored
server-side and revealed only to a guest who (a) enters a valid Reservation ID and (b) is *currently
within their stay* (check-in day through check-out day). Texting/emailing the guide link earlier does
**not** reveal codes earlier.

## What's in the page vs. what's on the server

- Each property page (`<property>/index.html`) renders the Door Code and WiFi tiles **masked**
  (`• • • •`, "🔒 unlock below"). There are no real codes anywhere in the page source.
- The actual codes live in `PROPERTY_CODES` inside the Form 2 Apps Script web app
  (`Form2_GAS_live/Code.js` in the `mvp-rentals` repo). They are returned only by its JSONP
  validation endpoint.

## The unlock flow

1. Guest enters their Reservation ID and taps **Unlock**.
2. The page calls `?action=validate&resId=…&property=…` (`handlePropertyAccess_`) via JSONP.
3. The server returns the codes **only when ALL hold**:
   - reservation not cancelled,
   - registration complete (TTPOA Filled / col AD is set), **and**
   - `today` is **on/after check-in AND on/before check-out**.
   ```js
   if (today < ci) { reason = 'before_checkin'; break; }   // locked
   if (today > co) { reason = 'after_checkout'; break; }   // locked
   // else -> authorized: return door + wifi
   ```
4. On success the page caches the unlock in `localStorage` so the guest doesn't re-enter the ID, and
   shows tap-to-copy codes. Otherwise it shows "Codes appear automatically on check-in day."

## Why this matters

- **Link send-time is decoupled from code visibility.** The house-guide link may be texted/emailed
  ~14 days before check-in (driven by the registration pipeline), but codes still only unlock during
  the actual stay window.
- **Anyone CC'd** via the Form 2 "Additional Guest Email" receives the same **link**, not early codes.
- A page scrape, a forwarded screenshot of the page, or an early visit cannot reveal codes — there is
  nothing to reveal until the validation endpoint authorizes.

## Where the codes are edited

Edit `PROPERTY_CODES` in `Form2_GAS_live/Code.js` (mvp-rentals repo), then redeploy the Form 2 web
app. Do **not** put codes in these guide pages.

Full end-to-end flow (registration → house docs → door codes):
`Documentation/Process Guides/registration_house_docs_and_door_codes.md` in the `mvp-rentals` repo.

*Last verified 2026-06-15.*
