# Modul 02 — Datentypen & Kontrollstrukturen

[← Modul 01](modul-01.md) | [Übersicht](catalog.md) | [Modul 03 →](modul-03.md)

---

**Phase:** Phase A — Grundlagen
**Zeitaufwand:** 4–6 h
**Schwierigkeit:** ★★☆☆☆ Grundkenntnisse
**Voraussetzungen:** Modul 01

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)

---

## Lernziele

- Alle eingebauten Datentypen sicher einsetzen und ihre Unterschiede kennen
- Mutable vs. immutable Objects und Auswirkungen auf Seiteneffekte verstehen
- Slicing und `enumerate()`, `zip()`, `reversed()` idiomatisch nutzen
- List-, Dict- und Set-Comprehensions schreiben
- Kontrollfluss mit `if/elif/else`, `for/else`, `while/else` steuern
- Pattern Matching mit `match/case` (Python 3.10+) anwenden

---

## Hintergrund

Python-Datentypen sind mächtiger als in vielen anderen Sprachen: Integer haben keine Overflow-Grenze, Strings sind Unicode-nativ, Dictionaries sind seit Python 3.7 insertion-ordered. Wer diese Eigenschaften kennt, schreibt kompakteren und korrekte Code.

Comprehensions sind das vielleicht wichtigste idiomatische Merkmal von Python — sie ersetzen ganze for-Schleifen durch einen lesbaren einzeiligen Ausdruck. Falsy-Werte (`None`, `0`, `""`, `[]`, `{}`) erlauben kompakte Bedingungen ohne expliziten Vergleich.

---

## Schlüsselkonzepte

### Dict-Comprehension

```python
log_levels = ["INFO", "WARNING", "ERROR", "INFO", "ERROR"]
counts = {}
for lvl in log_levels:
    counts[lvl] = counts.get(lvl, 0) + 1
# kompakter:
counts = {lvl: log_levels.count(lvl) for lvl in set(log_levels)}
```

### enumerate & zip

```python
hosts = ["web01", "db01", "cache01"]
ips   = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

for i, (host, ip) in enumerate(zip(hosts, ips), start=1):
    print(f"{i:2}. {host:<10} → {ip}")
```

### for-else Muster

```python
def find_user(users: list[str], target: str) -> None:
    for user in users:
        if user == target:
            print(f"Gefunden: {user}")
            break
    else:
        print(f"{target} nicht in der Liste")
```

### match/case

```python
def handle_status(code: int) -> str:
    match code:
        case 200: return "OK"
        case 404: return "Not Found"
        case 500 | 503: return "Server Error"
        case _: return f"Unbekannt: {code}"
```

---

## Aufgabe

Schreibe `log_stats.py` — ein Skript, das eine hartcodierte Liste von Log-Einträgen (als Liste von Dicts) auswertet:

Das Skript soll ausgeben:

```
LOG_ENTRIES = [
    {"level": "INFO",    "service": "nginx",  "msg": "request handled"},
    {"level": "ERROR",   "service": "db",     "msg": "connection timeout"},
    {"level": "WARNING", "service": "nginx",  "msg": "slow response"},
    {"level": "ERROR",   "service": "nginx",  "msg": "upstream failed"},
    {"level": "INFO",    "service": "db",     "msg": "query ok"},
    # ... mindestens 10 Einträge total
]
```

- Anzahl Einträge je Log-Level (via Dict-Comprehension)
- Alle ERROR-Einträge mit Zeilennummer (via `enumerate`)
- Alle beteiligten Services ohne Duplikate (via `set`)
- Service mit den meisten Fehlern

---

## Anforderungen

- [ ] Mindestens 10 hartcodierte Log-Einträge in der Liste
- [ ] Dict-Comprehension für die Level-Zählung — keine manuelle for-Schleife zum Befüllen
- [ ] `enumerate()` für nummerierte ERROR-Ausgabe
- [ ] Service mit meisten Fehlern korrekt bestimmt (auch bei Gleichstand stabil)
- [ ] Keine globalen Variablen außer `LOG_ENTRIES`; alles in Funktionen

---

## Akzeptanzkriterien

```
python log_stats.py

# Erwartete Ausgabe (Beispiel):
# Log-Level-Verteilung:
#   INFO    : 4
#   ERROR   : 3
#   WARNING : 2
#
# ERROR-Einträge:
#   1. [db]    connection timeout
#   2. [nginx] upstream failed
#   ...
#
# Services: {'nginx', 'db'}
# Meiste Fehler: nginx (2)
```

---

[← Modul 01](modul-01.md) | [Übersicht](catalog.md) | [Modul 03 →](modul-03.md)
