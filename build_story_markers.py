#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import qrcode

BASE = "/Users/mimi/Documents/Claude/Projects/WEB-ARjs/marker"
URL = "https://mrsdnf.github.io/WebAr/"

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

def make_marker(glyph, out_png, out_patt):
    S = 1000
    img = Image.new("RGB", (S, S), "white")
    d = ImageDraw.Draw(img)
    margin = int(S * 0.10)
    mx0, my0 = margin, margin
    mx1, my1 = S - margin, S - margin
    mksize = mx1 - mx0
    frame = int(mksize * 0.25)            # 25% border -> inner central 50% (patternRatio 0.5)
    in0x, in0y = mx0 + frame, my0 + frame
    in1x, in1y = mx1 - frame, my1 - frame
    inner_w, inner_h = in1x - in0x, in1y - in0y
    d.rectangle([mx0, my0, mx1 - 1, my1 - 1], fill="black")
    d.rectangle([in0x, in0y, in1x - 1, in1y - 1], fill="white")
    fs = int(inner_h * 0.9)
    while fs > 12:
        f = font(fs); sw = max(2, fs // 16)
        b = d.textbbox((0, 0), glyph, font=f, stroke_width=sw)
        if (b[2]-b[0]) <= inner_w*0.78 and (b[3]-b[1]) <= inner_h*0.78:
            break
        fs -= 4
    f = font(fs); sw = max(2, fs // 16)
    b = d.textbbox((0, 0), glyph, font=f, stroke_width=sw)
    tw, th = b[2]-b[0], b[3]-b[1]
    d.text((in0x + (inner_w-tw)//2 - b[0], in0y + (inner_h-th)//2 - b[1]),
           glyph, fill="black", font=f, stroke_width=sw, stroke_fill="black")
    img.save(out_png)
    inner = img.crop((in0x, in0y, in1x, in1y)).convert("L").resize((16, 16), Image.BILINEAR)
    def block(im):
        px = im.load(); out = []
        for _ch in range(3):
            for ry in range(16):
                out.append(" ".join("%3d" % px[rx, ry] for rx in range(16)))
        return "\n".join(out)
    patt = "\n\n".join(block(inner.rotate(90*k, expand=False)) for k in range(4)) + "\n"
    with open(out_patt, "w") as fh:
        fh.write(patt)

make_marker("J", BASE + "/marker-J.png", BASE + "/J.patt")
make_marker("S", BASE + "/marker-S.png", BASE + "/S.patt")
make_marker("P", BASE + "/marker-P.png", BASE + "/P.patt")

# standalone launch QR
qr = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(URL); qr.make(fit=True)
qimg = qr.make_image(fill_color="black", back_color="white").convert("RGB").resize((600, 600), Image.NEAREST)
card = Image.new("RGB", (800, 800), "white")
card.paste(qimg, ((800-600)//2, (800-600)//2))
card.save(BASE + "/qr-launch.png")
print("OK generated marker-J/S/P.png, J/S/P.patt, qr-launch.png")
