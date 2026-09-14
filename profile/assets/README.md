# Logo-Dateien

Quelle: `bluebranch-logo-full-color.svg`, unveraendert von
<https://www.bluebranch.de/wp-content/themes/theme/assets/images/bluebranch-logo-full-color.svg>.

In der Original-SVG traegt nur die Bildmarke eine Farbe (`.cls-1`, `#0036ff`); die Wortmarke hat
keine Fuellangabe und faellt damit auf Schwarz zurueck. Im Dark-Mode von GitHub waere sie
unsichtbar. Deshalb gibt es zwei eingefaerbte Fassungen:

| Datei | Wortmarke | Bildmarke | Einsatz |
|---|---|---|---|
| `logo-light.svg` / `logo-light.png` | `#101828` | `#0036ff` | helles Farbschema |
| `logo-dark.svg` / `logo-dark.png` | `#F0F3F9` | `#6E8BFF` | dunkles Farbschema |

Eingebunden werden die PNGs in `profile/README.md` ueber ein `<picture>`-Element, das anhand von
`prefers-color-scheme` umschaltet.

## PNGs neu erzeugen

Die PNGs entstehen aus den SVGs. `qlmanage`, der einzige auf macOS ohne Zusatzsoftware
verfuegbare Rasterizer, rendert allerdings **auf weissem Grund** – ein deckend weisser Kasten
hinter dem Logo, im Dark-Mode deutlich sichtbar.

Der Alphakanal laest sich exakt zurueckrechnen, indem dieselbe SVG zweimal gerastert wird, einmal
ueber Weiss und einmal ueber Schwarz:

    C_weiss   = a * F + (1 - a) * 255
    C_schwarz = a * F
    =>  a = 1 - (C_weiss - C_schwarz) / 255 ,  F = C_schwarz / a

Das schwarze Rechteck muss dabei groesser als die `viewBox` sein, sonst erzeugt seine eigene
geglaettete Kante einen Rand mit Rest-Alpha.
