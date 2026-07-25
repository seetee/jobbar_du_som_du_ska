#!/usr/bin/env python3
"""Genererar appikonerna ur läsårsbandsmotivet — fyra rör som fyllts olika mycket.

Körs sällan (ikonerna ändras i praktiken aldrig), men finns med så att PNG:erna
är reproducerbara i stället för ogenomskinliga blobbar i git:

    python3 icons/make-icons.py
"""
from PIL import Image, ImageDraw

ACCENT = (47, 93, 79, 255)      # --accent, samma som appens ljusa tema
TRACK = (24, 52, 43, 255)       # mörkare än bakgrunden — annars syns inte fyllnadsnivån
FILL = (234, 238, 234, 255)     # --paper
FRACTIONS = (1.0, 0.72, 0.45, 0.18)


def draw(size, *, inset, radius_frac):
    """inset = andel av kanten som lämnas tom (maskable behöver stor marginal)."""
    scale = 4  # rita stort och nedsampla, ger mjuka kanter utan antialias-krångel
    px = size * scale
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, px - 1, px - 1], radius=int(px * radius_frac), fill=ACCENT)

    pad = px * inset
    box = px - 2 * pad
    gap = box * 0.07
    bar_w = (box - 3 * gap) / 4
    r = bar_w * 0.28
    for i, frac in enumerate(FRACTIONS):
        x0 = pad + i * (bar_w + gap)
        x1 = x0 + bar_w
        d.rounded_rectangle([x0, pad, x1, pad + box], radius=r, fill=TRACK)
        top = pad + box * (1 - frac)
        # ett helt tomt rör ska inte ritas som en tunn strimma
        if box * frac > r:
            d.rounded_rectangle([x0, top, x1, pad + box], radius=r, fill=FILL)

    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    import pathlib
    here = pathlib.Path(__file__).parent
    # "any": plattformen maskar själv, så måttlig marginal och rundade hörn
    draw(192, inset=0.20, radius_frac=0.16).save(here / "icon-192.png")
    draw(512, inset=0.20, radius_frac=0.16).save(here / "icon-512.png")
    # "maskable": innehållet måste ligga inom mittcirkeln (safe zone ~80%)
    draw(512, inset=0.30, radius_frac=0.0).save(here / "icon-maskable-512.png")
    # iOS maskar själv och gillar inte transparens
    draw(180, inset=0.20, radius_frac=0.0).save(here / "apple-touch-icon.png")
    print("skrev icon-192, icon-512, icon-maskable-512, apple-touch-icon")
