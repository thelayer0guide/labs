# Lab 11 — Process & Service Baseline Monitor

> **Phase 4 — Integrität & Monitoring**
> Voraussetzungen: Lab 09 (psutil), Lab 10 (BaselineStore)
> Geschätzte Zeit: 4–6 Stunden
> Externe Dependencies: `psutil`

---

## Lernziele

- `psutil` für umfassende Prozess-Informationen einsetzen
- Das Baseline-Pattern aus Lab 10 auf Prozesse übertragen
- Linux `/proc`-Filesystem für ergänzende Informationen nutzen
- Heuristiken für verdächtige Prozess-Eigenschaften entwickeln
- Whitelist-Logik für bekannte gute Prozesse implementieren

---

## Hintergrund

Unbekannte Prozesse auf einem System sind ein klassisches Warnsignal: Malware, Rootkits oder unautorisierte Dienste starten neue Prozesse. Ein Prozess-Monitor mit Baseline ermöglicht es, neue Prozesse seit dem letzten Check zu erkennen.

Besonders interessant sind Heuristiken: Ein Prozess, der aus `/tmp` läuft oder dessen Binary-Pfad als "gelöscht" markiert ist, ist fast immer verdächtig.

---

## Aufgabe

Implementiere `procmon` — einen Prozess-Baseline-Monitor der verdächtige Prozesse erkennt und neue Prozesse seit dem letzten Snapshot aufzeigt.

### Projektstruktur

```
security-lab/
└── procmon/
    ├── __init__.py
    ├── core.py
    ├── cli.py
    └── tests/
        ├── __init__.py
        └── test_core.py
```

**Nutze** `BaselineStore` aus `shared/baseline.py` (Lab 10).

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `snapshot_processes() -> dict[str, dict]`
  - Scannt alle laufenden Prozesse via `psutil.process_iter()`
  - Key: `str(pid)` (String für JSON-Kompatibilität)
  - Für jeden Prozess:
    ```python
    {
        "pid": int,
        "name": str,
        "exe": str | None,           # Pfad zur Binary
        "cmdline": str,              # erste 200 Zeichen
        "username": str | None,
        "create_time": float,        # UNIX-Timestamp
        "exe_hash": str | None,      # SHA256 der Binary (wenn lesbar)
        "status": str,               # "running", "sleeping", etc.
        "suspicious_flags": list[str],  # (zunächst leer, wird von check_heuristics gefüllt)
    }
    ```
  - Bei `psutil.AccessDenied` oder `psutil.NoSuchProcess`: Prozess überspringen
  - `exe_hash`: nur wenn Binary < 50 MB (Sicherheitslimit, keine ISO-Dateien hashen)

- [ ] Funktion `check_heuristics(proc: dict) -> list[str]`
  - Prüft einen einzelnen Prozess-Eintrag auf verdächtige Merkmale
  - Gibt Liste von Warnungen zurück (leer = unauffällig):
    - `"exe_from_tmp"`: Binary läuft aus `/tmp/`, `/dev/shm/`, `/var/tmp/`
    - `"exe_deleted"`: `exe` enthält `"(deleted)"` oder Pfad existiert nicht mehr
    - `"no_exe"`: Prozess hat keine zugehörige Binary (Kernel-Thread ausgenommen: PID < 3)
    - `"running_as_root_unusual"`: läuft als root, Name ist kein bekannter System-Service
    - `"hidden_pid_gap"`: PID-Nummer stark unregelmäßig (möglicher Hinweis auf Rootkits — Low-confidence)

- [ ] Funktion `diff_process_snapshots(old: dict, new: dict, whitelist: set[str]) -> dict`
  - Nutzt das gleiche Diff-Pattern wie `diff_baselines` aus Lab 10:
    ```python
    {
        "new_processes":     list[dict],   # neue PIDs
        "terminated":        list[dict],   # beendete PIDs
        "suspicious":        list[dict],   # Prozesse mit suspicious_flags
        "whitelisted_new":   int,          # neue Prozesse in Whitelist (nur Statistik)
    }
    ```
  - `whitelist`: Set von Prozessnamen die ignoriert werden sollen

- [ ] Funktion `load_whitelist(path: Path) -> set[str]`
  - Liest eine Textdatei: ein Prozessname pro Zeile, Kommentare mit `#`
  - Gibt `set[str]` zurück
  - Gibt leeres Set zurück wenn Datei nicht existiert

### cli.py

- [ ] `procmon snapshot [--baseline DATEI]`
  - Erstellt Baseline aller aktuellen Prozesse
- [ ] `procmon scan [--baseline DATEI] [--whitelist DATEI] [--format text|json]`
  - Vergleicht mit Baseline, zeigt neue/verdächtige Prozesse

---

## CLI-Schnittstelle (vollständig)

```
procmon snapshot
procmon scan
procmon scan --whitelist whitelist.txt
procmon scan --format json
```

Beispiel-Output `procmon scan`:
```
PROCESS BASELINE SCAN
Baseline vom: 2026-06-19T08:00:00
══════════════════════════════════════════

NEUE PROZESSE (2)
────────────────
  PID 45123  python3   alice   /home/alice/myapp.py
  PID 45200  node      bob     /home/bob/server.js

VERDÄCHTIG (1)
──────────────
  PID 9911   .x        nobody  /tmp/.x
  [!] exe_from_tmp: Binary läuft aus /tmp/
  [!] running_as_root_unusual: Prozess läuft als root

BEENDET (3)
───────────
  PID 1234  python3    (beendet)
  PID 1235  bash       (beendet)
  PID 1236  sleep      (beendet)

══════════════════════════════════════════
Gesamt: 124 Prozesse · 2 neu · 1 verdächtig · 3 beendet
```

---

## Akzeptanzkriterien

```bash
# Snapshot erstellen
python -m procmon snapshot --baseline /tmp/proc-baseline.json
# → Keine Fehler, JSON-Datei erstellt

# Scan direkt danach → kaum Änderungen
python -m procmon scan --baseline /tmp/proc-baseline.json
# → "0 neue Prozesse" (oder minimal, je nach System)

# Heuristik-Test (keine echten Malware-Prozesse — nur prüfen ob Logik korrekt)
python -c "
from procmon.core import check_heuristics

# Verdächtiger Prozess aus /tmp
suspicious = {
    'pid': 99999, 'name': '.x', 'exe': '/tmp/.x', 'cmdline': '',
    'username': 'nobody', 'create_time': 0, 'exe_hash': None,
    'status': 'running', 'suspicious_flags': []
}
flags = check_heuristics(suspicious)
assert 'exe_from_tmp' in flags, f'Erwartet exe_from_tmp, bekam {flags}'

# Normaler sshd
normal = {
    'pid': 1234, 'name': 'sshd', 'exe': '/usr/sbin/sshd', 'cmdline': 'sshd -D',
    'username': 'root', 'create_time': 0, 'exe_hash': None,
    'status': 'sleeping', 'suspicious_flags': []
}
flags = check_heuristics(normal)
assert 'exe_from_tmp' not in flags

print('Heuristiken OK')
"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `check_heuristics` erkennt `exe_from_tmp` für Pfade in `/tmp/`, `/dev/shm/`
- [ ] Test: `check_heuristics` erkennt `exe_deleted` wenn `exe` den String `(deleted)` enthält
- [ ] Test: `check_heuristics` gibt leere Liste für normalen sshd-Prozess zurück
- [ ] Test: `diff_process_snapshots` erkennt neuen Prozess korrekt
- [ ] Test: `diff_process_snapshots` erkennt beendeten Prozess korrekt
- [ ] Test: `diff_process_snapshots` respektiert Whitelist (whitelistete neue Prozesse nicht in `new_processes`)
- [ ] Test: `load_whitelist` ignoriert Kommentarzeilen
- [ ] Test: `load_whitelist` auf nicht existierende Datei → leeres Set

Nutze `unittest.mock.patch("psutil.process_iter")` um `snapshot_processes` ohne echte Prozesse testen zu können.

---

## Bonus-Aufgaben

- [ ] **Network-Verbindungen pro Prozess:** Zeige welche Netzwerkverbindungen ein Prozess hält (nutze `psutil.Process(pid).connections()`)
- [ ] **Eltern-Kind-Baum:** Erkenne ungewöhnliche Parent-Child-Beziehungen (z. B. `nginx` spawnt `bash`)
- [ ] **Binary-Hash-Vergleich:** Wenn ein bekannter Prozessname (z. B. `sshd`) mit einem anderen Binary-Hash läuft als in der Baseline, ist das ein starkes Warnsignal

---

## Hinweise

**`psutil.process_iter()`:** Nutze `attrs`-Parameter um nur benötigte Felder zu laden: `psutil.process_iter(attrs=["pid", "name", "exe", "username", "status", "create_time", "cmdline"])`. Das ist deutlich schneller als alles zu laden.

**`/proc/PID/exe`:** Wenn eine Binary gelöscht wird während ein Prozess läuft, zeigt `/proc/PID/exe` den Pfad mit angehängtem ` (deleted)`. `psutil.Process(pid).exe()` gibt das weiter.

**Kernel-Threads:** Prozesse mit PID < 10 und ohne exe sind Kernel-Threads — kein Alarm nötig.

**exe_hash:** Das Hashen großer Binaries kann Zeit kosten. Setze ein Größenlimit (50 MB) und überspinge Dateien die größer sind.

---

## Schnittstelle für `uctl`

```python
def snapshot_processes() -> dict[str, dict]:
    """Erstellt Snapshot aller laufenden Prozesse."""

def diff_process_snapshots(old: dict, new: dict, whitelist: set[str]) -> dict:
    """Vergleicht zwei Prozess-Snapshots."""
```
