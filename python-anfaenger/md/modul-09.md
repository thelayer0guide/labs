# Modul 09 — HTTP, APIs & Webservices

[← Modul 08](modul-08.md) | [Übersicht](catalog.md) | [Modul 10 →](modul-10.md)

---

**Phase:** Phase B — Werkzeuge & Daten
**Zeitaufwand:** 4–6 h
**Schwierigkeit:** ★★★☆☆ Fortgeschritten
**Voraussetzungen:** Modul 07

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)
- [curl](https://thelayer0guide.github.io/cheat-sheets/sheets/curl-cheatsheet.html)
- [json](https://thelayer0guide.github.io/cheat-sheets/sheets/json-cheatsheet.html)

---

## Lernziele

- GET- und POST-Requests mit `requests` korrekt senden
- JSON-Antworten verarbeiten und in eigene Datenstrukturen überführen
- API-Keys und Tokens aus `.env`-Dateien laden (`python-dotenv`)
- Timeouts, Retry-Logik und `raise_for_status()` für robuste Requests
- Paginated APIs vollständig abrufen
- Dateien speichereffizient mit `stream=True` herunterladen

---

## Hintergrund

Fast jede moderne Infrastruktur hat eine API: Monitoring-Tools, Cloud-Provider, Ticketsysteme, Git-Plattformen. Wer REST-APIs aus Python heraus bedienen kann, automatisiert, was sonst manuell bleiben würde.

API-Keys niemals hardcoden — sie landen sonst in der Versionsverwaltung. `python-dotenv` lädt Schlüssel aus einer `.env`-Datei, die in `.gitignore` aufgenommen wird.

---

## Schlüsselkonzepte

### GET mit Fehlerbehandlung

```python
import requests

def fetch_users(base_url: str, token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{base_url}/users", headers=headers, timeout=10)
    resp.raise_for_status()  # wirft HTTPError bei 4xx/5xx
    return resp.json()
```

### .env laden

```python
# .env Datei:
# API_TOKEN=abc123
# API_BASE=https://api.example.com

from dotenv import load_dotenv
import os

load_dotenv()  # liest .env aus aktuellem Verzeichnis
token = os.environ["API_TOKEN"]
base  = os.environ["API_BASE"]
```

### Paginierung

```python
def fetch_all_pages(url: str) -> list[dict]:
    results = []
    page = 1
    while True:
        resp = requests.get(url, params={"page": page, "per_page": 100}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        results.extend(data)
        page += 1
    return results
```

---

## Aufgabe

Schreibe `api_poller.py`, das die öffentliche JSONPlaceholder-API (`https://jsonplaceholder.typicode.com`) abfragt:

1. `fetch_posts(user_id: int | None) -> list[dict]`: alle Posts oder Posts eines Users
2. `fetch_user(user_id: int) -> dict`: User-Daten inkl. Adresse
3. `posts_per_user(posts: list[dict]) -> dict[int, int]`: Anzahl Posts je User-ID
4. Alle Daten lokal als `posts_cache.json` speichern, bei erneutem Aufruf aus Cache laden wenn nicht älter als 5 Minuten
5. CLI: `--user-id N` filtert nach User, `--refresh` ignoriert Cache

---

## Anforderungen

- [ ] `timeout=10` bei allen Requests
- [ ] `raise_for_status()` bei allen Antworten
- [ ] Cache-Prüfung via `Path.stat().st_mtime` und `time.time()`
- [ ] `--refresh`-Flag löscht Cache und lädt neu
- [ ] Kein API-Key nötig für JSONPlaceholder — aber Struktur für Bearer-Token vorbereiten

---

## Akzeptanzkriterien

```
python api_poller.py
# → lädt Posts, speichert posts_cache.json

python api_poller.py
# → "Cache verwendet (2m 14s alt)"

python api_poller.py --user-id 3
# → zeigt nur Posts von User 3

python api_poller.py --refresh
# → Cache ignoriert, neu geladen
```

---

[← Modul 08](modul-08.md) | [Übersicht](catalog.md) | [Modul 10 →](modul-10.md)
