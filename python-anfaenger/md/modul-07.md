# Modul 07 — Dateien & Daten verarbeiten

[← Modul 06](modul-06.md) | [Übersicht](catalog.md) | [Modul 08 →](modul-08.md)

---

**Phase:** Phase B — Werkzeuge & Daten
**Zeitaufwand:** 3–5 h
**Schwierigkeit:** ★★☆☆☆ Grundkenntnisse
**Voraussetzungen:** Modul 04

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)
- [json](https://thelayer0guide.github.io/cheat-sheets/sheets/json-cheatsheet.html)

---

## Lernziele

- Dateien mit Context Manager (`with open()`) sicher öffnen und schließen
- Große Dateien zeilenweise lesen ohne alles in den RAM zu laden
- CSV-Dateien mit `csv.DictReader` und `csv.DictWriter` verarbeiten
- JSON mit `json.load()` und `json.dump(indent=2)` lesen und schreiben
- UTF-8-Kodierung explizit setzen
- Mehrere Dateien zusammenführen (merge)

---

## Hintergrund

Dateien sind das universelle Interface in der Systemadministration: Logdateien, Konfigurationen, Exporte. Die wichtigste Regel: immer den Context Manager (`with`) verwenden — er stellt sicher, dass Dateien auch bei Ausnahmen korrekt geschlossen werden.

CSV-Dateien ohne Header sind schwer zu lesen. `csv.DictReader` macht Spaltennamen zum Dict-Schlüssel — das macht den Code lesbar und robust gegenüber Spaltenverschiebungen.

---

## Schlüsselkonzepte

### Zeilenweises Lesen

```python
from pathlib import Path

def count_errors(log_path: Path) -> int:
    count = 0
    with log_path.open(encoding="utf-8") as f:
        for line in f:  # nie f.read() bei großen Dateien!
            if "ERROR" in line:
                count += 1
    return count
```

### CSV DictReader

```python
import csv
from pathlib import Path

def read_server_inventory(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# CSV-Header: hostname,ip,os,role
servers = read_server_inventory(Path("servers.csv"))
```

### JSON schreiben

```python
import json
from pathlib import Path

def save_report(data: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

---

## Aufgabe

Schreibe `log_aggregator.py`:

1. Erstelle drei Test-CSV-Dateien (`logs_jan.csv`, `logs_feb.csv`, `logs_mar.csv`) mit Spalten: `timestamp,level,service,message`
2. Schreibe `merge_csv_logs(paths: list[Path]) -> list[dict]`: liest alle CSVs und gibt eine zusammengeführte Liste zurück
3. Schreibe `filter_by_level(entries: list[dict], level: str) -> list[dict]`
4. Schreibe `summary_report(entries: list[dict]) -> dict`: gibt `{"total": N, "by_level": {...}, "by_service": {...}}` zurück
5. Speichere den Report als `report.json` mit `indent=2`

---

## Anforderungen

- [ ] Alle CSV-Dateien mit `newline=''` und `encoding='utf-8'` geöffnet
- [ ] `merge_csv_logs` akzeptiert beliebig viele Pfade
- [ ] `summary_report` gibt korrekte Zählungen für alle Level und Services zurück
- [ ] report.json enthält gültiges JSON mit `indent=2`
- [ ] Kein `f.read()` ohne Größenangabe — zeilenweises Lesen bei Textdateien

---

## Akzeptanzkriterien

```
python log_aggregator.py

# report.json muss gültiges JSON sein:
python -c "import json; json.load(open('report.json'))"
# → kein Fehler

cat report.json
# {
#   "total": 30,
#   "by_level": {"INFO": 15, "WARNING": 8, "ERROR": 7},
#   "by_service": {"nginx": 12, "db": 10, "auth": 8}
# }
```

---

[← Modul 06](modul-06.md) | [Übersicht](catalog.md) | [Modul 08 →](modul-08.md)
