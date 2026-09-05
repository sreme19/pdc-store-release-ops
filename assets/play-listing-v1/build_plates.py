"""Play Store phone screenshots — BUILD-YOURSELF-FIRST, women-first, India listing.

    /Users/performek5/Desktop/Code/pdc-ad-management-agent/.venv/bin/python \
        assets/play-listing-v1/build_plates.py

Re-cuts the same Flow frames behind the shipped Snap carousel
(pdc-ad-management-agent/creatives/buildyourself-carousel-w1830) into 1080x1920
Play screenshots. No new generation: every plate's source is a frame this account
already generated and QA'd once.

Deliberate departures from the Snap carousel, per the 2026-09-05 store-listing
session:
  * Act 1 (ghosted / catfished / "kab tak" / "bas ab nahin") is DROPPED. An ad
    earns attention by naming the pain; a store listing does not — she already
    tapped. Owner's direction: sell the transformation, not the grievance.
  * Type sits on a CREAM band, not the carousel's dark footer gradient. The
    competitive audit's single most reliable "looks professional" signal is one
    consistent colour field across icon and every screenshot, and riteangle's
    field is the light one (creative-style.md: "The palette is light, on
    purpose — every major rival ships a dark UI").
"""
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

AD = Path("/Users/performek5/Desktop/Code/pdc-ad-management-agent")
FR = AD / "creatives/buildyourself-lead-w1830/_source/frames"
OUT = Path(__file__).parent / "plates"
UI = Path(__file__).parent / "ui-captures"
FONT = "/Users/performek5/Desktop/Code/pocket-dating-coach/mobile/assets/fonts/Gabarito.ttf"

# Shared crop so this build and the ad repo's push gate can't drift on how a
# Google/Flow "made with AI" sparkle is removed (compliance.md 6.2: no visible
# AI-tool watermark). Falls back to the documented 150px if the import fails.
sys.path.insert(0, str(AD / "src"))
try:
    from ad_management_agent.watermark import strip_flow_watermark
except Exception:
    def strip_flow_watermark(im):
        return im.crop((0, 0, im.width, im.height - 150))

W, H = 1080, 1920
CREAM = "#FFF3F0"
INK = "#1B1020"
PINK = "#FF3B6B"
MUTED = "#6E5F64"
BAND = 660          # cream band height
MARGIN = 84


def face(size, weight="ExtraBold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def find(prefix):
    hits = sorted(p for p in FR.iterdir()
                  if p.name.startswith(prefix) and "(1)" not in p.name)
    if not hits:
        raise SystemExit(f"no source frame for {prefix!r}")
    return hits[0]


def photo(prefix, mode="cover", bias=0.28):
    """Load a frame, strip the watermark band, fit it to the photo area.

    mode="cover" fills the area and crops. mode="fit" letterboxes on cream and is
    REQUIRED for the two multi-panel group frames: sourcing.md records that
    cropping the 2x2 grid destroys it, and cover-cropping the group shot drops
    two of the four women. Letterboxing on a cream ground reads as intentional
    here in a way it would not on the carousel's dark footer.
    """
    im = strip_flow_watermark(Image.open(find(prefix)).convert("RGB"))
    target_h = H - BAND
    if mode == "grid2x2":
        # The hero is a 2x2 contact grid of the same four women lifting their
        # heads into the lens -- the thesis frame. Cover-cropping it destroys the
        # grid (sourcing.md) and letterboxing it leaves it too small to read as a
        # Play search thumbnail. So recompose: cut the four panels apart and
        # re-lay them to fill the photo area exactly, losing no woman.
        pw, ph = im.width // 2, im.height // 2
        cw, ch = W // 2, target_h // 2
        grid = Image.new("RGB", (W, target_h), CREAM)
        for idx, (cx, cy) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
            panel = im.crop((cx * pw, cy * ph, (cx + 1) * pw, (cy + 1) * ph))
            sc = max(cw / panel.width, ch / panel.height)
            panel = panel.resize((round(panel.width * sc), round(panel.height * sc)), Image.LANCZOS)
            ox, oy = (panel.width - cw) // 2, (panel.height - ch) // 2
            grid.paste(panel.crop((ox, oy, ox + cw, oy + ch)), (cx * cw, cy * ch))
        return grid
    if mode == "fit":
        scale = min(W / im.width, target_h / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        pad = Image.new("RGB", (W, target_h), CREAM)
        pad.paste(im, ((W - im.width) // 2, (target_h - im.height) // 2))
        return pad
    scale = max(W / im.width, target_h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = round((im.height - target_h) * bias)   # bias up: keep faces off the crop line
    return im.crop((left, top, left + W, top + target_h))


def device(shot_name):
    """Put a real screen capture in a device frame.

    The audit is explicit that bezel/notch/status-bar chrome "reads as more
    'authentic app'" than a borderless marketing card, and that a listing with no
    product visible at all (Betterhalf) is a self-imposed transparency gap. These
    three captures come from the app's PRE-AUTH lane, so they contain no member's
    photo, name or messages -- see BLOCKERS.md.
    """
    target_h = H - BAND
    shot = Image.open(UI / shot_name).convert("RGB")
    sh = target_h - 96
    sw = round(shot.width * sh / shot.height)
    shot = shot.resize((sw, sh), Image.LANCZOS)

    pad, radius = 14, 46
    frame = Image.new("RGB", (W, target_h), CREAM)
    d = ImageDraw.Draw(frame)
    bx, by = (W - sw) // 2 - pad, (target_h - sh) // 2 - pad
    d.rounded_rectangle([bx, by, bx + sw + 2 * pad, by + sh + 2 * pad],
                        radius=radius, fill=INK)

    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], radius=radius - pad, fill=255)
    frame.paste(shot, (bx + pad, by + pad), mask)
    return frame


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def plate(name, prefix, headline, keyword=None, strap=None, wordmark=False,
          mode="cover", bias=0.28):
    canvas = Image.new("RGB", (W, H), CREAM)
    canvas.paste(device(prefix) if mode == "device" else photo(prefix, mode, bias), (0, BAND))
    d = ImageDraw.Draw(canvas)

    f_head = face(96)
    f_strap = face(40, "Medium")
    max_w = W - 2 * MARGIN
    lines = wrap(d, headline, f_head, max_w)

    strap_lines = wrap(d, strap, f_strap, max_w) if strap else []
    block_h = len(lines) * 112 + (len(strap_lines) * 52 + 18 if strap_lines else 0)
    y = (BAND - block_h) // 2 + 10

    for ln in lines:
        x = MARGIN
        # brand-pink the one keyword, ink the rest, word by word
        for word in ln.split():
            colour = PINK if keyword and word.strip(".,!?").lower() == keyword.lower() else INK
            d.text((x, y), word, font=f_head, fill=colour)
            x += d.textlength(word + " ", font=f_head)
        y += 112

    y += 8
    for sl in strap_lines:
        d.text((MARGIN, y), sl, font=f_strap, fill=MUTED)
        y += 52

    if wordmark:
        f_mark = face(72)
        d.text((MARGIN, BAND - 132), "riteangle", font=f_mark, fill=PINK)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.png"
    canvas.save(path, "PNG", optimize=True)
    print(f"  {path.name}  {canvas.size[0]}x{canvas.size[1]}")
    return path


PLATES = [
    # name, frame prefix, headline, pink keyword, strap, mode, crop bias
    ("01-hero",     "Four_women_looking_into_camera",   "Khud ko bana sakti ho.", "bana",
     "14 verified suitors, ordered by fit — not by who gamed the photo.", "grid2x2", 0.28),
    ("02-strength", "Woman_completing_heavy_barbell",   "Pehle apni taakat.",  "taakat", None, "cover", 0.20),
    ("03-career",   "Woman_smiling_in_modern_office",   "Pehle apna career.",  "career", None, "cover", 0.55),
    ("04-calm",     "Woman_meditating_on_balcony",      "Pehle apna sukoon.",  "sukoon", None, "cover", 0.25),
    ("05-verified",  "05-gate.png",  "Har koi ID-verified.",   "ID-verified",
     "No one sees the raw files — only the signals you allow.", "device", 0),
    ("06-minutes",   "06-lane.png",  "Minutes mein. Months nahi.", "Minutes",
     "Earn your profile, verify your intent.", "device", 0),
    ("07-fit",       "07-fit.png",   "Fit se match. Swipe se nahi.", "Fit",
     "Best match, good fit, and who you never see — decided before you open the app.", "device", 0),
    ("08-endcard",  "Four_women_standing_in_space",     "Pehle tum. Phir koi aur.", "tum",
     "No swipes. Ever. Just verified matches.", "fit", 0.28),
]

if __name__ == "__main__":
    print(f"Building {len(PLATES)} plates into {OUT}/")
    for name, prefix, head, kw, strap, mode, bias in PLATES:
        plate(name, prefix, head, kw, strap, wordmark=(name == "08-endcard"),
              mode=mode, bias=bias)
    print("\nAll 8 plates built. UI plates come from the pre-auth lane -- no member data.")


# ── Feature graphic ──────────────────────────────────────────────────────────
# Play spec: 1024x500, PNG or JPEG, no transparency. It sits at the top of the
# listing, and Play overlays a centred play button on it whenever a promo video
# exists -- so nothing load-bearing goes in the middle, even though there is no
# promo video today. Text also stays well inside the edges, because this asset
# gets re-cropped across Play surfaces.
FG_W, FG_H = 1024, 500


def feature_graphic():
    im = strip_flow_watermark(Image.open(find("Four_women_standing_in_space")).convert("RGB"))
    scale = max(FG_W / im.width, FG_H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - FG_W) // 2
    top = round((im.height - FG_H) * 0.42)
    canvas = im.crop((left, top, left + FG_W, top + FG_H))

    # Cream panel over the left, feathered into the photo so the four women stay
    # readable on the right. The light field is the point -- it is what makes the
    # feature graphic, the icon and all eight screenshots read as one system.
    panel = Image.new("RGB", (FG_W, FG_H), CREAM)
    mask = Image.new("L", (FG_W, FG_H), 0)
    md = ImageDraw.Draw(mask)
    solid, fade = 470, 660
    md.rectangle([0, 0, solid, FG_H], fill=255)
    for x in range(solid, fade):
        md.line([(x, 0), (x, FG_H)], fill=round(255 * (1 - (x - solid) / (fade - solid))))
    canvas = Image.composite(panel, canvas, mask)

    d = ImageDraw.Draw(canvas)
    d.text((64, 74), "riteangle", font=face(46), fill=PINK)

    f_head = face(64)
    for i, (txt, kw) in enumerate([("Pehle tum.", "tum"), ("Phir koi aur.", None)]):
        x, y = 64, 168 + i * 76
        for word in txt.split():
            colour = PINK if kw and word.strip(".") == kw else INK
            d.text((x, y), word, font=f_head, fill=colour)
            x += d.textlength(word + " ", font=f_head)

    d.text((64, 340), "No swipes. Ever. Just verified matches.",
           font=face(27, "Medium"), fill=MUTED)

    path = Path(__file__).parent / "feature-graphic.png"
    canvas.save(path, "PNG", optimize=True)
    print(f"  feature-graphic.png  {canvas.size[0]}x{canvas.size[1]}")


feature_graphic()
