# Modul 14 — Praxisprojekte: CLI-Tools

[← Modul 13](modul-13.md) | [Übersicht](catalog.md)

---

**Phase:** Phase C — Praxis & Projekte
**Zeitaufwand:** 6–10 h
**Schwierigkeit:** ★★★★☆ Erfahren
**Voraussetzungen:** Modul 10, Modul 12, Modul 13

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)
- [bash](https://thelayer0guide.github.io/cheat-sheets/sheets/bash-cheatsheet.html)
- [json](https://thelayer0guide.github.io/cheat-sheets/sheets/json-cheatsheet.html)

---

## Lernziele

- Ein vollständiges CLI-Projekt mit mehreren Modulen aufbauen
- Alle bisher gelernten Konzepte (OOP, Logging, Fehlerbehandlung, APIs, Dateien) kombinieren
- Saubere Projektstruktur mit `__main__.py` für `python -m toolkit`
- Exit-Codes konsequent für Skript-Verkettung einsetzen
- Konfiguration über `.env` und CLI-Argumente kombinieren
- Das Tool dokumentieren und ein einfaches `--help` bereitstellen

---

## Hintergrund

Dieses Modul ist das Capstone des Kurses: Hier werden alle 13 vorherigen Module integriert. Ein echtes CLI-Tool für den Admin-Alltag bauen — das ist das Ziel von Anfang an gewesen.

Guter Admin-Code läuft unbeaufsichtigt. Das bedeutet: Exit-Codes für Shell-Verkettung (`&&`, `||`), Logging in Dateien statt `print()`, saubere Fehlerbehandlung ohne Stack-Traces auf der Konsole, Timeout bei Netzwerkoperationen.

---

## Schlüsselkonzepte

### Projektstruktur mit __main__.py

```python
admin-toolkit/
├── .env
├── .gitignore         ← enthält .env
├── requirements.txt
├── toolkit/
│   ├── __init__.py
│   ├── __main__.py    ← python -m toolkit
│   ├── cli.py         ← argparse-Setup
│   ├── inventory.py
│   ├── monitor.py
│   └── report.py
└── tests/
```

### __main__.py Muster

```python
import sys
from toolkit.cli import build_parser
from toolkit import inventory, monitor, report

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd is None:
        parser.print_help()
        return 2
    return args.func(args)  # jeder Subparser setzt args.func

if __name__ == "__main__":
    sys.exit(main())
```

### Subcommand-Dispatch

```python
# In cli.py:
inv_p = sub.add_parser("inventory", help="Systeminventar als JSON")
inv_p.add_argument("--output", "-o", default="inventory.json")
inv_p.set_defaults(func=inventory.run)

mon_p = sub.add_parser("monitor", help="URL auf Verfügbarkeit prüfen")
mon_p.add_argument("url")
mon_p.add_argument("--interval", type=int, default=60)
mon_p.set_defaults(func=monitor.run)
```

---

## Aufgabe

Baue `admin-toolkit` mit drei Subcommands. Jeder muss `int` zurückgeben (0 = OK, 1 = Fehler).

**`toolkit inventory [--output FILE]`**

**`toolkit monitor URL [--interval N] [--log FILE]`**

**`toolkit report CSV [--format text|json]`**

- Erfasst: Hostname, OS, CPU-Kerne, RAM, Disk, Python-Version, laufende Prozesse (Top-5 CPU), Netzwerk-IPs
- Speichert als JSON in `--output` (Default: `inventory.json`)

- Prüft URL alle N Sekunden (Default: 60), misst Antwortzeit
- Loggt Ergebnis (OK/FAIL + Antwortzeit) als CSV in `--log` (Default: `monitor.csv`)
- Ctrl+C beendet sauber mit Zusammenfassung

- Liest `monitor.csv`, berechnet: Uptime-%, mittlere Antwortzeit, Ausfallzeiten
- Ausgabe als Textbericht oder JSON (`--format`)

---

## Anforderungen

- [ ] Alle drei Subcommands implementiert mit korrekten Exit-Codes
- [ ] `python -m toolkit --help` zeigt alle Subcommands
- [ ] `inventory.json` ist valid JSON mit allen geforderten Feldern
- [ ] `monitor`: Ctrl+C gibt Zusammenfassung aus (N checks, X OK, Y FAIL)
- [ ] `report`: Uptime-% korrekt berechnet; bei leerem CSV Exit-Code 1 + Fehlermeldung
- [ ] Logging in Datei `toolkit.log` (DEBUG), Konsole (INFO) — keine unbehandelten Exceptions
- [ ] `.gitignore` enthält `.env`, `*.log`, `__pycache__/`, `.venv/`

---

## Akzeptanzkriterien

```
python -m toolkit inventory
# → inventory.json erzeugt

python -m toolkit monitor https://example.com --interval 5
# → alle 5s: 2026-06-19 14:30:05, OK, 0.234s
# (Ctrl+C) → Zusammenfassung: 4/4 OK, ø 0.218s

python -m toolkit report monitor.csv
# Uptime: 100.0% | Ø 0.218s | 0 Ausfälle

python -m toolkit report monitor.csv --format json
# {"uptime_pct": 100.0, "avg_response_s": 0.218, "failures": 0}
```

---

[← Modul 13](modul-13.md) | [Übersicht](catalog.md)
