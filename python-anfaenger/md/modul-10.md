# Modul 10 — Fehlerbehandlung & Logging

[← Modul 09](modul-09.md) | [Übersicht](catalog.md) | [Modul 11 →](modul-11.md)

---

**Phase:** Phase B — Werkzeuge & Daten
**Zeitaufwand:** 3–5 h
**Schwierigkeit:** ★★☆☆☆ Grundkenntnisse
**Voraussetzungen:** Modul 04

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)

---

## Lernziele

- Spezifische Exceptions fangen statt blankem `except:`
- `try/except/else/finally` korrekt strukturieren
- Das `logging`-Modul gegenüber `print()` bevorzugen und warum
- Logger, Handler und Formatter konfigurieren
- Log-Level (DEBUG, INFO, WARNING, ERROR, CRITICAL) sinnvoll einsetzen
- Rotierende Logdateien mit `RotatingFileHandler` einrichten

---

## Hintergrund

In Produktionsskripten ist `print()` für Fehlerausgaben ungeeignet: Es gibt keine Zeitstempel, kein Log-Level, keine Möglichkeit, Ausgaben in Dateien umzuleiten ohne Shell-Tricks. Das `logging`-Modul löst all das — und ist in der Standardbibliothek enthalten.

Spezifische Exceptions zu fangen ist wichtig: `except Exception` fängt alles, auch Programmierfehler wie `NameError` oder `TypeError`, die sofort sichtbar sein sollten.

---

## Schlüsselkonzepte

### try/except/else/finally

```python
def read_config(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Config nicht gefunden: %s", path)
        raise
    except json.JSONDecodeError as e:
        logger.error("Ungültiges JSON in %s: %s", path, e)
        raise ValueError(f"Config-Fehler: {e}") from e
    else:
        logger.info("Config geladen: %s", path)
```

### Logging konfigurieren

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Konsole: INFO+
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))

# Datei: DEBUG+, max 1 MB, 3 Backups
fh = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3)
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))

logger.addHandler(ch)
logger.addHandler(fh)
```

---

## Aufgabe

Refaktoriere `api_poller.py` aus Modul 09 mit vollständiger Fehlerbehandlung und Logging:

1. Richte einen Logger ein: Konsole (INFO+) + rotierende Datei `poller.log` (DEBUG+)
2. Alle API-Aufrufe in `try/except` einwickeln: `requests.Timeout`, `requests.HTTPError`, `requests.ConnectionError` separat behandeln
3. Cache-Operationen mit `try/except (FileNotFoundError, json.JSONDecodeError)` absichern
4. Fehler werden geloggt, nicht als `print()` ausgegeben
5. Bei nicht-behebbaren Fehlern: `logger.critical(...)` + `sys.exit(1)`

---

## Anforderungen

- [ ] `logging.getLogger(__name__)` — kein `logging.basicConfig()` im Modul-Code
- [ ] Jede Exception-Art gibt eine sinnvolle, nicht-generische Fehlermeldung
- [ ] `poller.log` enthält Zeitstempel, Modul-Name, Level und Message
- [ ] Konsolenausgabe zeigt keine DEBUG-Meldungen
- [ ] Testbar: wenn `https://jsonplaceholder.typicode.com` nicht erreichbar, Exit-Code 1

---

## Akzeptanzkriterien

```
python api_poller.py
# Konsole zeigt INFO-Meldungen

cat poller.log | head -5
# 2026-06-19 14:23:01 __main__ INFO API-Aufruf: /posts
# 2026-06-19 14:23:01 __main__ DEBUG HTTP 200 in 0.34s

# Datei beschädigen, dann:
python api_poller.py
# ERROR Cache-Datei korrupt — lade neu
```

---

[← Modul 09](modul-09.md) | [Übersicht](catalog.md) | [Modul 11 →](modul-11.md)
