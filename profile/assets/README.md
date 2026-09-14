# Logo-Dateien

## Quellen

Beide SVGs stammen unveraendert von bluebranch.de:

| Datei | Herkunft | Inhalt |
|---|---|---|
| `bluebranch-logo-mono.svg` | `.../assets/images/logo.svg` | einfarbig, `fill="white"` — **Basis der PNGs** |
| `bluebranch-logo-full-color.svg` | `.../assets/images/bluebranch-logo-full-color.svg` | zweifarbig: Bildmarke `#0036ff`, Wortmarke ohne Fuellangabe |

Gebaut wird aus der einfarbigen Fassung. Die zweifarbige liegt nur als Referenz bei: Ihre
Wortmarke hat keine Fuellangabe und faellt damit auf Schwarz zurueck, was im Dark-Mode
unsichtbar waere.

## Farben

| Datei | Farbe | Kontrast |
|---|---|---|
| `logo-light.png` | Markenblau `#0036ff` | 7,07:1 auf Weiss |
| `logo-dark.png` | Weiss `#ffffff` | 18,92:1 auf `#0d1117`, 15,02:1 auf `#22272e` |

Markenblau steht bewusst nur im hellen Farbschema. Auf GitHubs dunklem Grund erreicht es
2,68:1, gedimmt sogar nur 2,13:1 — beides unter der 3:1-Schwelle, die WCAG 1.4.11 fuer
grafische Objekte vorsieht.

Eingebunden werden die PNGs in `profile/README.md` ueber ein `<picture>`-Element, das anhand
von `prefers-color-scheme` umschaltet.

## Neu erzeugen

    python3 build-logos.py

Benoetigt Pillow. Das Skript umgeht zwei Eigenheiten von `qlmanage`, dem einzigen Rasterizer,
den macOS ohne Zusatzsoftware mitbringt:

**Es rendert immer auf weissem Grund.** Ein deckend weisser Kasten hinter dem Logo, im
Dark-Mode deutlich sichtbar. Der Alphakanal wird deshalb zurueckgerechnet, aus demselben
Motiv einmal ueber Weiss und einmal ueber Schwarz:

    C_weiss   = a * F + (1 - a) * 255
    C_schwarz = a * F
    =>  a = 1 - (C_weiss - C_schwarz) / 255

Die schwarze Unterlegung muss groesser als die `viewBox` sein, sonst erzeugt ihre eigene
geglaettete Kante einen Rand mit Rest-Alpha.

**Wo er den Inhalt ablegt, ist nicht vorhersagbar.** Eine SVG mit festen `width`/`height`
landet oben links, eine ohne wird zentriert. Das Skript leitet den Ausschnitt deshalb aus dem
Rendering ab: In der schwarz unterlegten Fassung ist der SVG-Viewport genau der nicht-weisse
Bereich.

Weil das Motiv einfarbig ist, wird am Ende nur der Alphakanal skaliert und die Farbe flaechig
gesetzt. Das vermeidet die Farbsaeume, die beim Skalieren nicht vormultiplizierter
RGBA-Bilder entstehen.
