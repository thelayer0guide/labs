# Lab 04 — Log Forensics Toolkit

> **Phase 2 — Parsing & Forensik**
> Voraussetzungen: Lab 03 (Projektstruktur, Verzeichnisiteration)
> Geschätzte Zeit: 5–8 Stunden

---

## Lernziele

- Regex-Gruppen für strukturiertes Parsing einsetzen
- `datetime`-Parsing und Zeitraum-Filterung implementieren
- `collections.Counter` für Häufigkeitsanalysen nutzen
- Ein Datenmodell mit `dataclass` entwerfen (Parser → Modell → Aggregation → Report)
- Maschinenlesbare Ausgabe (JSON) neben menschenlesbarer Ausgabe implementieren

---

## Hintergrund

Log-Dateien sind die Hauptquelle forensischer Analyse auf Linux-Systemen. `auth.log` (oder `secure` auf Fedora/RHEL) enthält SSH-Logins, sudo-Nutzung und Authentifizierungsversuche. Webserver-Logs zeigen Zugriffsmuster. Wer schnell erkennt, welche IP-Adressen besonders aggressiv scannen, kann reagieren.

Das wichtigste Architekturmuster dieses Labs ist die klare Trennung:
**Parser → Datenmodell → Aggregation → Report**

Dieses Muster zieht sich durch fast alle folgenden Labs. Lerne es hier sauber.

---

## Aufgabe

Implementiere `logaudit` — ein Tool zur forensischen Analyse von `auth.log`-Dateien und (als Bonus) nginx-Access-Logs.

### Projektstruktur

```
security-lab/
└── logaudit/
    ├── __init__.py
    ├── core.py
    ├── models.py     ← Datenmodell (dataclasses)
    ├── cli.py
    └── tests/
        ├── __init__.py
        ├── test_core.py
        └── fixtures/
            ├── sample_auth.log
            └── sample_nginx.log
```

---

## Das Datenmodell

Definiere in `models.py`:

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    timestamp: datetime
    host: str
    service: str
    pid: int | None
    message: str
    ip: str | None          # extrahierte IP-Adresse, falls vorhanden
    event_type: str         # "ssh_fail", "ssh_success", "sudo", "other"
    username: str | None    # betroffener Nutzer, falls erkennbar
```

Du kannst das Modell erweitern, aber diese Felder müssen vorhanden sein.

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `parse_auth_log(path: Path) -> list[LogEntry]`
  - Parst eine `auth.log`-Datei zeilenweise
  - Erkennt das Standard-Syslog-Format: `Mmm DD HH:MM:SS hostname service[pid]: message`
  - Extrahiert IP-Adressen per Regex aus der `message` (IPv4 + IPv6)
  - Klassifiziert `event_type`:
    - `ssh_fail`: Zeilen mit "Failed password" oder "Invalid user"
    - `ssh_success`: Zeilen mit "Accepted password" oder "Accepted publickey"
    - `sudo`: Zeilen mit "sudo:"
    - `other`: alles andere
  - Zeilen, die nicht dem Format entsprechen, werden übersprungen (nicht geworfen)
  - Bei Parse-Fehler eines Timestamps: Zeile überspringen, Warnung auf stderr

- [ ] Funktion `filter_by_time(entries: list[LogEntry], since: datetime | None, until: datetime | None) -> list[LogEntry]`
  - Filtert Einträge nach Zeitraum
  - `since` und `until` können unabhängig `None` sein (kein Filter in die Richtung)

- [ ] Funktion `aggregate_ssh_failures(entries: list[LogEntry]) -> dict`
  - Gibt zurück: `{ip: count}` für alle SSH-Fehlversuche, sortiert nach Count (absteigend)
  - Nur Einträge mit `event_type == "ssh_fail"` und vorhandener IP

- [ ] Funktion `hourly_distribution(entries: list[LogEntry]) -> dict[int, int]`
  - Gibt zurück: `{stunde: anzahl}` für alle Einträge (0–23)
  - Nützlich zur Erkennung von Angriffszeiten

- [ ] Funktion `login_success_rate(entries: list[LogEntry]) -> float`
  - Berechnet: erfolgreiche Logins / (erfolgreiche + fehlgeschlagene) × 100
  - Gibt `0.0` zurück wenn kein Login-Versuch vorhanden

### cli.py

- [ ] `logaudit FILE [--since DATUM] [--until DATUM] [--top N] [--format text|json]`
  - `--since "2026-06-01"` oder `--since "2026-06-01T12:00:00"`
  - `--top 10`: zeigt Top-10-IPs (Standard: 10)
  - `--format json`: maschinenlesbarer Output

---

## CLI-Schnittstelle (vollständig)

```
logaudit /var/log/auth.log
logaudit /var/log/auth.log --since "2026-06-01"
logaudit /var/log/auth.log --top 5 --format json
logaudit /var/log/auth.log --since "2026-06-01" --until "2026-06-30"
```

Beispiel-Output (Text):
```
LOG FORENSICS: /var/log/auth.log
Zeitraum: 2026-06-01 — 2026-06-19
Analysiert: 15.234 Einträge

TOP-10 SSH-ANGREIFER
────────────────────────────────
185.220.101.47    1.842 Versuche
193.32.162.9        923 Versuche
198.51.100.1        441 Versuche

STUNDEN-HISTOGRAMM
00: ██░░░░░░░░░░░░░░░░░░ 12%
01: █░░░░░░░░░░░░░░░░░░░  6%
...
23: ████████████░░░░░░░░ 61%

Login-Erfolgsquote: 3.2%
```

---

## Test-Fixtures

Erstelle `tests/fixtures/sample_auth.log` mit mindestens 20 Zeilen — echtes Format, anonymisierte IPs:

```
Jun  1 03:14:15 hostname sshd[12345]: Failed password for invalid user admin from 192.168.1.1 port 45678 ssh2
Jun  1 03:14:16 hostname sshd[12345]: Failed password for root from 192.168.1.1 port 45679 ssh2
Jun  1 03:14:17 hostname sshd[12345]: Accepted publickey for alice from 10.0.0.5 port 52341 ssh2
Jun  1 04:00:01 hostname sudo:  alice : TTY=pts/0 ; PWD=/home/alice ; USER=root ; COMMAND=/bin/ls
```

---

## Akzeptanzkriterien

```bash
# Parst ohne Fehler
python -m logaudit tests/fixtures/sample_auth.log

# JSON-Output ist valides JSON
python -m logaudit tests/fixtures/sample_auth.log --format json | python -m json.tool

# Zeitraum-Filter funktioniert
python -m logaudit tests/fixtures/sample_auth.log --since "2026-06-01" --until "2026-06-01"
# → Nur Einträge vom 1. Juni
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `parse_auth_log` auf dem Sample-Fixture → korrekte Anzahl Einträge
- [ ] Test: Event-Typ-Klassifizierung korrekt für bekannte Log-Zeilen
- [ ] Test: IP-Extraktion aus einer "Failed password"-Zeile
- [ ] Test: `filter_by_time` mit `since`-Filter
- [ ] Test: `filter_by_time` mit `until`-Filter
- [ ] Test: `filter_by_time` mit `since=None, until=None` → alle Einträge
- [ ] Test: `aggregate_ssh_failures` sortiert korrekt nach Häufigkeit
- [ ] Test: `hourly_distribution` gibt Dict mit Keys 0–23 zurück
- [ ] Test: `login_success_rate` bei 0 Logins → 0.0
- [ ] Test: Zeilen mit falschem Format werden übersprungen (keine Exception)

---

## Bonus-Aufgaben

- [ ] **nginx-Support:** `--format nginx` parst Access-Logs (`$remote_addr - - [$time_local] "$request" $status $body_bytes_sent`)
- [ ] **GeoIP-Lookup:** Mit lokaler MaxMind-GeoLite2-DB (`geoip2`-Paket) — kein API-Call, komplett offline
- [ ] **Mehrere Dateien:** `logaudit auth.log.1 auth.log.2 auth.log` kombiniert alle zu einer Analyse
- [ ] **Komprimierte Logs:** `auth.log.gz` on-the-fly mit `gzip.open()` lesen

---

## Hinweise

**Syslog-Timestamp:** Das Format ist `Mmm DD HH:MM:SS` ohne Jahr — nutze das aktuelle Jahr als Fallback. Regex: `r"^(\w+)\s+(\d+)\s+(\d{2}:\d{2}:\d{2})"`. `datetime.strptime()` mit `"%b %d %H:%M:%S"`.

**IPv4-Regex:** `r"\b(\d{1,3}\.){3}\d{1,3}\b"` — ist vereinfacht und matched auch `999.999.999.999`. Eine strikte Version prüft jeden Oktett: `r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"`. Entscheide welche du nimmst und warum.

**Sortierung:** `sorted(d.items(), key=lambda x: x[1], reverse=True)` sortiert ein Dict nach Wert absteigend.

**JSON-Output:** `json.dumps(data, indent=2, default=str)` — `default=str` serialisiert `datetime`-Objekte als Strings.

---

## Schnittstelle für `uctl`

```python
def parse_auth_log(path: Path) -> list[LogEntry]:
    """Parst auth.log und gibt strukturierte Einträge zurück."""

def aggregate_ssh_failures(entries: list[LogEntry]) -> dict[str, int]:
    """Zählt SSH-Fehlversuche pro IP, sortiert nach Häufigkeit."""
```
