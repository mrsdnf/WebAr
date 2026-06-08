#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

OUT_MARKER = "/Users/mimi/Documents/Claude/Projects/WEB-ARjs/marker/jabra-marker.png"
OUT_PATT   = "/Users/mimi/Documents/Claude/Projects/WEB-ARjs/marker/jabra.patt"

W, H = 1200, 1600
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def load_font(size):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/Library/Fonts/Arial.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

# ---------- caption (human-readable; does not affect tracking) ----------
caption = "Point your camera here to discover the extra dimensions you get with the Jabra Sound Plus App"
cap_margin = 80
cap_w = W - 2 * cap_margin
cap_area_h = 460

def wrap(text, font):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= cap_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

cap_fs = 96
while cap_fs > 18:
    f = load_font(cap_fs)
    lines = wrap(caption, f)
    ab = d.textbbox((0, 0), "Ag", font=f); line_h = ab[3] - ab[1]
    gap = int(cap_fs * 0.32)
    if len(lines) * line_h + (len(lines) - 1) * gap <= cap_area_h:
        break
    cap_fs -= 4
f = load_font(cap_fs)
gap = int(cap_fs * 0.32)
ab = d.textbbox((0, 0), "Ag", font=f); line_h = ab[3] - ab[1]
lines = wrap(caption, f)
y = cap_margin
for ln in lines:
    w = d.textlength(ln, font=f)
    d.text(((W - w) / 2, y), ln, fill="black", font=f)
    y += line_h + gap

# ---------- marker square: border = 25% (inner = central 50%, matches patternRatio 0.5) ----------
mk = 820
mx0 = (W - mk) // 2
my0 = 640
mx1, my1 = mx0 + mk, my0 + mk
frame = int(mk * 0.25)                 # 25% border on each side
in0x, in0y = mx0 + frame, my0 + frame
in1x, in1y = mx1 - frame, my1 - frame
inner_w = in1x - in0x; inner_h = in1y - in0y

d.rectangle([mx0, my0, mx1 - 1, my1 - 1], fill="black")
d.rectangle([in0x, in0y, in1x - 1, in1y - 1], fill="white")

# big bold "J+" centered, with stroke to make it blockier/bolder
label = "J+"
fs = int(inner_h * 0.85)
while fs > 12:
    mf = load_font(fs)
    sw = max(2, fs // 16)
    b = d.textbbox((0, 0), label, font=mf, stroke_width=sw)
    if (b[2] - b[0]) <= inner_w * 0.80 and (b[3] - b[1]) <= inner_h * 0.80:
        break
    fs -= 4
mf = load_font(fs)
sw = max(2, fs // 16)
b = d.textbbox((0, 0), label, font=mf, stroke_width=sw)
tw, th = b[2] - b[0], b[3] - b[1]
tx = in0x + (inner_w - tw) // 2 - b[0]
ty = in0y + (inner_h - th) // 2 - b[1]
d.text((tx, ty), label, fill="black", font=mf, stroke_width=sw, stroke_fill="black")

img.save(OUT_MARKER)

# ---------- .patt trained on inner central-50% region ----------
inner = img.crop((in0x, in0y, in1x, in1y)).convert("L").resize((16, 16), Image.BILINEAR)
def block(im):
    px = im.load(); out = []
    for _ch in range(3):
        for ry in range(16):
            out.append(" ".join("%3d" % px[rx, ry] for rx in range(16)))
    return "\n".join(out)
patt = "\n\n".join(block(inner.rotate(90 * k, expand=False)) for k in range(4)) + "\n"
with open(OUT_PATT, "w") as fh:
    fh.write(patt)
print("OK rebuilt marker as bold 'J+' with 25% border; patt regenerated")
