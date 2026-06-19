# Modul 04 — Module, Pakete & Projektstruktur

[← Modul 03](modul-03.md) | [Übersicht](catalog.md) | [Modul 05 →](modul-05.md)

---

**Phase:** Phase A — Grundlagen
**Zeitaufwand:** 3–4 h
**Schwierigkeit:** ★★☆☆☆ Grundkenntnisse
**Voraussetzungen:** Modul 03

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)
- [bash](https://thelayer0guide.github.io/cheat-sheets/sheets/bash-cheatsheet.html)

---

## Lernziele

- Den Unterschied zwischen Modul, Paket und Skript erklären
- Eigene Module erstellen und mit verschiedenen `import`-Formen verwenden
- Ein Paket mit `__init__.py` aufbauen
- Den Modulauflösungspfad (`sys.path`) verstehen
- Den `if __name__ == '__main__'`-Guard korrekt einsetzen
- Ein Admin-Projekt nach empfohlener Verzeichnisstruktur organisieren

---

## Hintergrund

Ab einer gewissen Komplexität wird ein einzelnes Skript unübersichtlich. Python löst das mit Modulen (einzelne .py-Dateien) und Paketen (Verzeichnisse mit `__init__.py`). Die Aufteilung ermöglicht Wiederverwendung: Eine Funktion, die Logdateien liest, kann in mehreren Skripten genutzt werden, ohne sie zu kopieren.

Der `if __name__ == '__main__'`-Guard ist entscheidend: Er stellt sicher, dass Code nur ausgeführt wird, wenn das Skript direkt gestartet wird — nicht wenn es von einem anderen Modul importiert wird.

---

## Schlüsselkonzepte

### Empfohlene Projektstruktur

```python
admin-toolkit/
├── .venv/
├── requirements.txt
├── main.py              ← Einstiegspunkt
└── lib/
    ├── __init__.py
    ├── file_utils.py    ← Funktionen aus Modul 03
    └── report.py
```

### Import-Varianten

```python
# Ganzes Modul
import lib.file_utils
lib.file_utils.count_files_by_extension(".")

# Selektiver Import
from lib.file_utils import count_files_by_extension, total_size_bytes

# Alias
from lib import file_utils as fu
```

### __init__.py für saubere API

```python
# lib/__init__.py
from .file_utils import count_files_by_extension, total_size_bytes, find_largest_file
from .report import print_report

# Dann von außen:
from lib import print_report
```

---

## Aufgabe

Nimm `file_report.py` aus Modul 03 und refaktoriere es zu einem echten Paket:

1. Erstelle die Struktur `file-toolkit/lib/` mit `__init__.py`
2. Verschiebe Berechnungsfunktionen nach `lib/file_utils.py`
3. Verschiebe Ausgabefunktionen nach `lib/report.py`
4. Erstelle `main.py`, der `sys.argv[1]` als Pfad entgegennimmt und den Bericht ausgibt
5. Stelle sicher, dass `lib/file_utils.py` auch direkt als Skript ausführbar ist und dann das aktuelle Verzeichnis analysiert

---

## Anforderungen

- [ ] `lib/__init__.py` exportiert alle öffentlichen Funktionen
- [ ] `main.py` importiert nur aus `lib`, enthält selbst keine Berechnungslogik
- [ ] `python main.py /etc` gibt denselben Bericht wie Modul 03 aus
- [ ] `python lib/file_utils.py` analysiert das aktuelle Verzeichnis
- [ ] Kein `sys.path`-Hacking nötig — Struktur funktioniert out-of-the-box

---

## Akzeptanzkriterien

```
# Aus dem Projektverzeichnis:
python main.py /var/log
# → gleicher Report wie in Modul 03

python lib/file_utils.py
# → Report über aktuelles Verzeichnis

# Kein ImportError, keine Pfadmanipulation
```

---

[← Modul 03](modul-03.md) | [Übersicht](catalog.md) | [Modul 05 →](modul-05.md)
