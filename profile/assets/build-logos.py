#!/usr/bin/env python3
"""Erzeugt logo-light.png und logo-dark.png aus der einfarbigen Marken-SVG.

qlmanage ist der einzige Rasterizer, den macOS ohne Zusatzsoftware mitbringt. Er
rendert immer auf weissem Grund, und wo er den Inhalt auf der quadratischen
Leinwand ablegt, haengt davon ab, ob die SVG feste width/height-Attribute hat.
Beides wird hier umgangen:

* Der Ausschnitt wird aus dem Rendering abgeleitet, nicht angenommen. In der
  Fassung mit schwarzer Unterlegung ist der SVG-Viewport genau der nicht-weisse
  Bereich.
* Der Alphakanal wird zurueckgerechnet, aus demselben Motiv ueber Weiss und
  ueber Schwarz:

      C_weiss   = a * F + (1 - a) * 255
      C_schwarz = a * F
      =>  a = 1 - (C_weiss - C_schwarz) / 255

Da das Motiv einfarbig ist, wird nur der Alphakanal skaliert und die Farbe
danach flaechig gesetzt. Das vermeidet die Farbsaeume, die beim Skalieren
nicht vormultiplizierter RGBA-Bilder entstehen.

Aufruf:  python3 build-logos.py      (benoetigt Pillow)
"""
import re, subprocess, pathlib
from PIL import Image, ImageChops

HERE = pathlib.Path(__file__).parent
SRC = HERE / "bluebranch-logo-mono.svg"
RENDER_AT = 2400          # grosszuegig rastern, danach sauber herunterrechnen
OUT_WIDTH = 1200

# Markenblau erreicht auf hellem Grund 7,07:1, auf GitHubs #0d1117 aber nur
# 2,68:1 und liegt damit unter der 3:1-Schwelle aus WCAG 1.4.11. Im dunklen
# Farbschema steht deshalb das offizielle Weiss (18,92:1).
VARIANTS = {"light": "#0036ff", "dark": "#ffffff"}


def render(svg_text, tag):
    p = HERE / f"_tmp-{tag}.svg"
    p.write_text(svg_text)
    subprocess.run(["qlmanage", "-t", "-s", str(RENDER_AT), "-o", str(HERE), str(p)],
                   check=True, capture_output=True)
    png = HERE / f"_tmp-{tag}.svg.png"
    img = Image.open(png).convert("RGB").copy()
    p.unlink(); png.unlink()
    return img


def nonwhite_bbox(img):
    white = Image.new("RGB", img.size, (255, 255, 255))
    mask = ImageChops.difference(img, white).convert("L").point(lambda v: 255 if v > 8 else 0)
    return mask.getbbox()


def main():
    base = SRC.read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', base).group(1).split()]

    for name, colour in VARIANTS.items():
        tinted = base.replace('fill="white"', f'fill="{colour}"')
        assert tinted != base, 'kein fill="white" in der Quell-SVG gefunden'

        # Schwarzflaeche deutlich groesser als die viewBox, sonst erzeugt ihre
        # eigene geglaettete Kante einen Rand mit Rest-Alpha.
        i = re.search(r"<svg[^>]*>", tinted).end()
        pad = max(vb[2], vb[3]) * 2
        rect = (f'<rect x="{-pad}" y="{-pad}" width="{vb[2] + 2 * pad}" '
                f'height="{vb[3] + 2 * pad}" fill="#000000"/>')

        img_w = render(tinted, f"{name}-w")
        img_b = render(tinted[:i] + rect + tinted[i:], f"{name}-b")

        # In der schwarz unterlegten Fassung ist der Viewport der nicht-weisse Teil
        box = nonwhite_bbox(img_b)
        img_w, img_b = img_w.crop(box), img_b.crop(box)
        w, h = img_w.size
        pw, pb = img_w.load(), img_b.load()

        alpha = Image.new("L", (w, h)); pa = alpha.load()
        for y in range(h):
            for x in range(w):
                rw, gw, bw = pw[x, y]; rb, gb, bb = pb[x, y]
                a = 1.0 - ((rw - rb) + (gw - gb) + (bw - bb)) / 765.0
                pa[x, y] = round(min(1.0, max(0.0, a)) * 255)

        out_h = round(OUT_WIDTH * h / w)
        alpha = alpha.resize((OUT_WIDTH, out_h), Image.LANCZOS)
        rgb = tuple(int(colour.lstrip("#")[k:k + 2], 16) for k in (0, 2, 4))
        out = Image.new("RGBA", alpha.size, rgb + (0,))
        out.putalpha(alpha)
        out.save(HERE / f"logo-{name}.png")

        px = out.load()
        opaque = sum(1 for y in range(out_h) for x in range(OUT_WIDTH) if px[x, y][3] > 250)
        print(f"logo-{name}.png  {OUT_WIDTH}x{out_h}  {colour}  "
              f"deckend {opaque * 100 / (OUT_WIDTH * out_h):.1f}%  Ecke={px[0, 0]}")


if __name__ == "__main__":
    main()
