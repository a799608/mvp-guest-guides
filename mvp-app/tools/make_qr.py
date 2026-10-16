#!/usr/bin/env python3
"""
make_qr.py -- MVP Rentals QR code generator + verifier.

Generates a high-error-correction QR PNG for any URL and verifies it decodes
back to that URL, so a label is never printed from a bad code.

Usage:
  python make_qr.py "<url>" "<output.png>"
      Generate one QR for <url> -> <output.png>, then verify it decodes.

  python make_qr.py --properties "<output_dir>"
      Regenerate the six per-property GUIDE-PAGE codes (QR_<Name>.png) into
      <output_dir>. They point at https://a799608.github.io/mvp-guest-guides/<slug>/.

How-to / per-item codes use the single-URL form with the per-item guide page URL:
  python make_qr.py "https://a799608.github.io/mvp-guest-guides/wylie/fireplace/" \
      qr/howto/QR_wylie_fireplace.png

QR settings (locked): error correction H (survives label wear), box_size 24,
border 4  ->  ~1176x1176 PNG. Verified with zbar (phone-grade) when available,
else OpenCV; if no decoder is installed the PNG is still written but flagged
UNVERIFIED.

Deps: pip install qrcode pillow pyzbar  (opencv-python-headless optional fallback)

Property slug source of truth: PROPERTY_GUIDE_SLUG in
mvp-rentals Data/mvp_guest_send.py. Mirrored here by hand (slugs are stable).
"""
import sys, os

PROPERTY_URLS = {
    "Trails":    "https://a799608.github.io/mvp-guest-guides/trails/",
    "Pound":     "https://a799608.github.io/mvp-guest-guides/pound/",
    "Milton":    "https://a799608.github.io/mvp-guest-guides/milton/",
    "Wylie":     "https://a799608.github.io/mvp-guest-guides/wylie/",
    "MacCauley": "https://a799608.github.io/mvp-guest-guides/maccauley/",
    "Petrarch":  "https://a799608.github.io/mvp-guest-guides/petrarch/",
}


def make_qr(url, out, box=24, border=4):
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    d = os.path.dirname(os.path.abspath(out))
    if d:
        os.makedirs(d, exist_ok=True)
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=box, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img.save(out, dpi=(300, 300))
    return img.size


def verify(out, url):
    """Return (ok, decoder). ok is None when no decoder is installed."""
    try:
        from pyzbar.pyzbar import decode as zdecode
        from PIL import Image
        r = zdecode(Image.open(out))
        return (bool(r) and r[0].data.decode() == url, "zbar")
    except Exception:
        pass
    try:
        import cv2
        det = cv2.QRCodeDetector()
        img = cv2.imread(out)
        val, _, _ = det.detectAndDecode(img)
        if not val:
            big = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
            val, _, _ = det.detectAndDecode(big)
        return (val == url, "cv2")
    except Exception:
        pass
    return (None, "none")


def gen_one(url, out):
    size = make_qr(url, out)
    ok, dec = verify(out, url)
    status = "VERIFIED" if ok else ("UNVERIFIED (no decoder)" if ok is None else "FAILED VERIFY")
    print("%s %s -> %s  [%s / %s]" % (os.path.basename(out), size, url, status, dec))
    return ok is not False  # unverified = non-fatal; failed verify = fatal


def main(argv):
    if len(argv) >= 2 and argv[0] == "--properties":
        outdir = argv[1]
        all_ok = True
        for name, url in PROPERTY_URLS.items():
            all_ok = gen_one(url, os.path.join(outdir, "QR_%s.png" % name)) and all_ok
        return 0 if all_ok else 1
    if len(argv) == 2:
        return 0 if gen_one(argv[0], argv[1]) else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
