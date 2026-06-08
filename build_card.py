#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import qrcode

OUT_MARKER = "/Users/mimi/Documents/Claude/Projects/WEB-ARjs/marker/jabra-marker.png"
OUT_PATT   = "/Users/mimi/Documents/Claude/Projects/WEB-ARjs/marker/jabra.patt"
URL = "https://mrsdnf.github.io/WebAr/"

W, H = 1200, 1600
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def font(size):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/Library/Fonts/Arial.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

# --- scannable QR (top) ---
qr = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(URL); qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qsize = 400
qr_img = qr_img.resize((qsize, qsize), Image.NEAREST)
qr_y = 220
img.paste(qr_img, ((W - qsize) // 2, qr_y))

# --- J+ tracking marker (below); border 25% -> inner central 50% ---
mk = 600
mx0 = (W - mk) // 2
my0 = qr_y + qsize + 160
mx1, my1 = mx0 + mk, my0 + mk
frame = int(mk * 0.25)
in0x, in0y = mx0 + frame, my0 + frame
in1x, in1y = mx1 - frame, my1 - frame
inner_w = in1x - in0x; inner_h = in1y - in0y
d.rectangle([mx0, my0, mx1 - 1, my1 - 1], fill="black")
d.rectangle([in0x, in0y, in1x - 1, in1y - 1], fill="white")

label = "J+"
fs = int(inner_h * 0.85)
while fs > 12:
    mf = font(fs); sw = max(2, fs // 16)
    b = d.textbbox((0, 0), label, font=mf, stroke_width=sw)
    if (b[2]-b[0]) <= inner_w*0.80 and (b[3]-b[1]) <= inner_h*0.80:
        break
    fs -= 4
mf = font(fs); sw = max(2, fs // 16)
b = d.textbbox((0, 0), label, font=mf, stroke_width=sw)
tw, th = b[2]-b[0], b[3]-b[1]
d.text((in0x + (inner_w-tw)//2 - b[0], in0y + (inner_h-th)//2 - b[1]),
       label, fill="black", font=mf, stroke_width=sw, stroke_fill="black")

img.save(OUT_MARKER)

# --- .patt from J+ inner central-50% region ---
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
print("OK clean card (QR + J+ only) built; patt regenerated")
