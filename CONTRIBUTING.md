# Beiträge

Danke für dein Interesse an unseren Open-Source-Projekten. Issues und Pull Requests sind in allen
öffentlichen Repositories der [BlueBranch GmbH](https://github.com/BlueBranch-GmbH) willkommen.

## Fehler melden

Lege ein Issue im betroffenen Repository an und beschreibe möglichst konkret:

- was du erwartet hast und was stattdessen passiert ist
- wie sich der Fehler reproduzieren lässt
- die verwendeten Versionen (bei Contao-Erweiterungen: PHP-, Contao- und Paketversion)
- Fehlermeldungen aus Log oder Konsole, falls vorhanden

Ein Fehler mit einer nachvollziehbaren Reproduktion ist meist am selben Tag eingeordnet.

## Änderungen vorschlagen

1. Repository forken und einen Branch von `main` abzweigen
2. Änderung umsetzen und dabei den Stil des umgebenden Codes beibehalten
3. Commit-Nachrichten kurz und im Imperativ halten, zum Beispiel `Alt-Text-Cache invalidieren`
4. Pull Request gegen `main` öffnen und darin erklären, welches Problem die Änderung löst

Bei größeren Umbauten lohnt sich vorab ein Issue – so klären wir die Richtung, bevor Arbeit
hineinfließt.

## Code

- Für PHP-Pakete gilt der Contao-Coding-Standard, also im Wesentlichen PSR-12.
- Für TypeScript- und Dart-Projekte gilt die jeweils im Repository hinterlegte Linter- und
  Formatter-Konfiguration.
- Öffentliche Schnittstellen bekommen einen kurzen Docblock, interne Logik nur dort einen
  Kommentar, wo der Code allein sie nicht erklärt.

## Lizenz

Mit dem Einreichen eines Pull Requests stimmst du zu, dass dein Beitrag unter der Lizenz des
jeweiligen Repositories veröffentlicht wird – bei unseren Paketen die MIT-Lizenz.

## Fragen

Für alles, was nicht in ein Issue gehört: [hello@bluebranch.de](mailto:hello@bluebranch.de)
