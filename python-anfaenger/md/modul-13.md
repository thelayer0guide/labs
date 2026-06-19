# Modul 13 — Logdateien & Monitoringdaten analysieren

[← Modul 12](modul-12.md) | [Übersicht](catalog.md) | [Modul 14 →](modul-14.md)

---

**Phase:** Phase C — Praxis & Projekte
**Zeitaufwand:** 5–7 h
**Schwierigkeit:** ★★★☆☆ Fortgeschritten
**Voraussetzungen:** Modul 07, Modul 10

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)
- [regex](https://thelayer0guide.github.io/cheat-sheets/sheets/regex-cheatsheet.html)
- [bash](https://thelayer0guide.github.io/cheat-sheets/sheets/bash-cheatsheet.html)

---

## Lernziele

- Reguläre Ausdrücke mit `re.compile()` und `re.match()`/`re.search()` einsetzen
- Apache/Nginx-Logformat mit Regex-Gruppen parsen
- Häufigkeiten mit `collections.Counter` effizient zählen
- Zeitstempel aus Logs parsen und in `datetime`-Objekte umwandeln
- Stundenbezogene Statistiken berechnen
- Alarme bei Schwellenwertüberschreitung auslösen

---

## Hintergrund

Logs sind strukturierte Daten im Plaintext-Format. Apache und Nginx nutzen das Combined Log Format — ein bekanntes Muster, das sich gut mit einem einzigen regulären Ausdruck parsen lässt. Der Schlüssel: `re.compile()` einmal außerhalb der Schleife aufrufen, nicht bei jedem Aufruf.

`collections.Counter` ist für Häufigkeitszählungen optimiert und bietet `.most_common(N)` direkt an — kein manuelles Dict-Befüllen und Sortieren nötig.

---

## Schlüsselkonzepte

### Apache Combined Log Format Regex

```python
import re

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<size>\d+|-)'
)

def parse_line(line: str) -> dict | None:
    m = LOG_PATTERN.match(line)
    return m.groupdict() if m else None
```

### Counter für Häufigkeiten

```python
from collections import Counter

def top_ips(log_path: str, n: int = 10) -> list[tuple[str, int]]:
    counter: Counter[str] = Counter()
    with open(log_path) as f:
        for line in f:
            entry = parse_line(line)
            if entry:
                counter[entry["ip"]] += 1
    return counter.most_common(n)
```

### Schwellenwert-Alarm

```python
def check_error_rate(entries: list[dict], threshold: float = 0.05) -> bool:
    total = len(entries)
    errors = sum(1 for e in entries if e["status"].startswith("5"))
    rate = errors / total if total else 0
    if rate > threshold:
        logger.warning("Error-Rate %.1f%% überschreitet Schwelle %.1f%%", rate*100, threshold*100)
        return True
    return False
```

---

## Aufgabe

Erstelle eine realistische Beispiel-Logdatei `access.log` mit mindestens 500 Zeilen im Apache Combined Log Format. Schreibe dann `log_analyzer.py`:

1. `parse_log(path: Path) -> list[dict]`: parst alle Zeilen, überspringt fehlerhafte
2. `requests_per_hour(entries: list[dict]) -> dict[int, int]`: Anfragen je Stunde (0–23)
3. `top_paths(entries, n=10) -> list[tuple[str, int]]`: meistangeforderte URLs
4. `error_summary(entries) -> dict[str, int]`: Anzahl je HTTP-Status (200, 404, 500, ...)
5. `generate_report(path: Path, out: Path) -> None`: schreibt Textbericht
6. CLI: `--top N` (Default 10), `--warn-errors PROZENT` (Default 5.0)

---

## Anforderungen

- [ ] Beispiel-Logdatei vorhanden, mindestens 500 Zeilen, diverse IPs/Status-Codes/Pfade
- [ ] `re.compile()` außerhalb der Parse-Schleife
- [ ] Zeitstempel korrekt als `datetime` geparst: `strptime(..., '%d/%b/%Y:%H:%M:%S %z')`
- [ ] Fehlerhafte Zeilen zählen und am Ende als INFO loggen
- [ ] Bericht enthält: Gesamtanfragen, Zeitraum, Top-IPs, Top-Paths, Status-Verteilung, Error-Rate

---

## Akzeptanzkriterien

```
python log_analyzer.py access.log --top 5

# Ausgabe enthält:
# Gesamt: 523 Anfragen (2026-01-01 bis 2026-01-31)
# Top-5 Pfade:
#   1. /api/status   (142)
#   ...
# Status-Verteilung:
#   200: 412  404: 67  500: 44
# Error-Rate: 8.4% — WARNING: über Schwelle (5.0%)
```

---

[← Modul 12](modul-12.md) | [Übersicht](catalog.md) | [Modul 14 →](modul-14.md)
