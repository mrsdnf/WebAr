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

def wrap(text, fnt, max_w):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_block(text, y, fs, max_w):
    fnt = font(fs)
    ab = d.textbbox((0, 0), "Ag", font=fnt); lh = ab[3] - ab[1]; gap = int(fs * 0.3)
    for ln in wrap(text, fnt, max_w):
        w = d.textlength(ln, font=fnt)
        d.text(((W - w) / 2, y), ln, fill="black", font=fnt)
        y += lh + gap
    return y

margin = 80; maxw = W - 2 * margin
y = 70
y = draw_block("Jabra Sound Plus App in 3D", y, 78, maxw)
y += 16
y = draw_block("Scan the code with your phone camera to open it, then aim at the J+ symbol below to see it in 3D.", y, 44, maxw)
y += 26

# --- scannable QR code that opens the AR page ---
qr = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(URL); qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qsize = 330
qr_img = qr_img.resize((qsize, qsize), Image.NEAREST)
img.paste(qr_img, ((W - qsize) // 2, int(y)))
y = y + qsize + 8
y = draw_block("Step 1  -  Scan to open", y, 38, maxw)
y += 30

# --- J+ tracking marker (border 25% -> inner central 50%, matches patternRatio 0.5) ---
mk = 500
mx0 = (W - mk) // 2; my0 = int(y)
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
y = my1 + 8
y = draw_block("Step 2  -  Aim your camera at the J+", y, 38, maxw)

img.save(OUT_MARKER)

# --- .patt trained on the J+ marker's inner central-50% region ---
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
print("OK card with scannable QR + J+ marker built; patt regenerated")
