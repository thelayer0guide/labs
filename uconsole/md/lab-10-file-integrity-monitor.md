# Lab 10 — File Integrity Monitor

> **Phase 4 — Integrität & Monitoring**
> Voraussetzungen: Lab 01 (Hash-Berechnung), Lab 03 (Verzeichnisrekursion)
> Geschätzte Zeit: 5–7 Stunden

---

## Lernziele

- Das Baseline/Diff-Pattern für Integritätsprüfungen implementieren
- JSON-Persistenz für strukturierte Daten sauber gestalten
- Eine gemeinsame `BaselineStore`-Klasse in `shared/` entwickeln
- Inkrementelle Updates mit manueller Bestätigung umsetzen
- Ausschlusslogik für volatile Pfade (Logs, tmp) implementieren

---

## Hintergrund

File Integrity Monitoring (FIM) ist ein Kernkonzept in der Host-basierten Intrusion Detection: Wenn kritische Systemdateien wie `/etc/ssh/sshd_config` oder `/etc/passwd` unangekündigt geändert werden, ist das ein Warnsignal. Tools wie AIDE oder Tripwire machen das industriell — du baust deine eigene Version.

Das wichtigste Konzept ist das **Baseline/Diff-Muster**: Du fotografierst den Zustand zu einem Zeitpunkt (Baseline), und vergleichst später dagegen. Abweichungen sind Findings.

---

## Aufgabe

Implementiere `fim` — einen File Integrity Monitor mit `init` (Baseline erstellen) und `scan` (Vergleichen) Subcommands.

### Projektstruktur

```
security-lab/
├── shared/
│   ├── __init__.py
│   └── baseline.py      ← BaselineStore-Klasse (für Labs 10 & 11)
└── fim/
    ├── __init__.py
    ├── core.py
    ├── cli.py
    └── tests/
        ├── __init__.py
        └── test_core.py
```

---

## Die BaselineStore-Klasse (in `shared/baseline.py`)

Diese Klasse wird von Lab 10 (Dateien) und Lab 11 (Prozesse) verwendet:

```python
class BaselineStore:
    """Persistiert und verwaltet einen Zustandssnapshot als JSON."""
    
    def __init__(self, path: Path):
        """path: Pfad zur JSON-Datei (wird erstellt wenn nicht vorhanden)"""
    
    def save(self, data: dict, metadata: dict | None = None) -> None:
        """Speichert Snapshot + Metadaten (Timestamp, Tool-Version)."""
    
    def load(self) -> dict:
        """Lädt letzten Snapshot. Wirft FileNotFoundError wenn keine Baseline."""
    
    def exists(self) -> bool:
        """Gibt True zurück wenn eine Baseline-Datei existiert."""
    
    def get_metadata(self) -> dict:
        """Gibt Metadaten des letzten Snapshots zurück (Zeitstempel etc.)."""
```

Das JSON-Format:
```json
{
    "_meta": {
        "created": "2026-06-19T10:00:00",
        "tool": "fim",
        "version": "1.0"
    },
    "data": {
        "/etc/ssh/sshd_config": { ... },
        ...
    }
}
```

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `scan_path(root: Path, exclude_patterns: list[str]) -> dict[str, dict]`
  - Scannt `root` rekursiv mit `pathlib.rglob("*")`
  - Für jede Datei (kein Verzeichnis, kein Symlink):
    ```python
    {
        "hash_sha256": str,     # aus Lab 01 wiederverwenden
        "size": int,
        "mtime": float,         # UNIX-Timestamp
        "permissions": str,     # oktales Format: "644"
        "uid": int,
        "gid": int,
    }
    ```
  - Schließt Pfade aus, die auf einen der `exclude_patterns` matchen (Glob-Matching mit `fnmatch`)
  - Bei Lesefehler: Datei überspringen, Warnung auf stderr
  - Key im Dict: **relativer Pfad** zu `root` als String

- [ ] Funktion `diff_baselines(old: dict, new: dict) -> dict`
  - Vergleicht zwei Snapshots:
    ```python
    {
        "added":   list[str],    # neue Dateien
        "removed": list[str],    # gelöschte Dateien
        "changed": list[dict],   # geänderte Dateien mit Detailinfos
        "unchanged": int,        # Anzahl unveränderte (für Statistik)
    }
    ```
  - `changed`-Einträge:
    ```python
    {
        "path": str,
        "changes": list[str],    # z. B. ["hash_changed", "permissions_changed"]
        "old": dict,
        "new": dict,
    }
    ```

- [ ] Funktion `format_diff_report(diff: dict, fmt: str) -> str`
  - `fmt == "text"`: Lesbare Ausgabe mit Farb-Hinweisen (ANSI-Codes oder plain)
  - `fmt == "json"`: JSON-String
  - `fmt == "markdown"`: Markdown mit Tabellen

### cli.py

- [ ] `fim init PATH [--baseline DATEI] [--exclude PATTERN]`
  - Erstellt Baseline für `PATH`
  - `--baseline ~/.local/share/fim/baseline.json` (Standardpfad)
  - `--exclude "/var/log/*" --exclude "/tmp/*"` (mehrfach verwendbar)

- [ ] `fim scan PATH [--baseline DATEI] [--format text|json|markdown] [--accept]`
  - Vergleicht aktuellen Zustand mit Baseline
  - `--accept`: aktualisiert die Baseline mit dem aktuellen Zustand (nach manueller Prüfung)

---

## CLI-Schnittstelle (vollständig)

```
fim init /etc --baseline /var/lib/fim/etc-baseline.json
fim init /etc --exclude "/etc/mtab" --exclude "/etc/resolv.conf"
fim scan /etc
fim scan /etc --format json > fim-report.json
fim scan /etc --accept    (akzeptiert Änderungen und aktualisiert Baseline)
```

Beispiel-Output `fim scan`:
```
FILE INTEGRITY SCAN: /etc
Baseline vom: 2026-06-15T09:00:00
══════════════════════════════════════════

GEÄNDERT (3)
────────────
  /etc/ssh/sshd_config
    Hash geändert | Permissions: 600 → 644
    
  /etc/hosts
    Hash geändert
    
  /etc/crontab
    Hash geändert | mtime: +2h

NEU (1)
────────
  /etc/nginx/sites-enabled/newsite.conf

GELÖSCHT (0)

══════════════════════════════════════════
Gescannt: 847 Dateien | Unverändert: 843 | Geändert: 3 | Neu: 1 | Gelöscht: 0
```

---

## Standard-Ausschlüsse

Implementiere diese Ausschlüsse als Standard (immer aktiv, überschreibbar):

```python
DEFAULT_EXCLUDES = [
    "*/proc/*",
    "*/sys/*",
    "*/dev/*",
    "*/run/*",
    "/tmp/*",
    "/var/log/*",
    "*/lost+found/*",
]
```

---

## Akzeptanzkriterien

```bash
# Init + Scan auf einem kleinen Verzeichnis
mkdir -p /tmp/fim-test/
echo "original" > /tmp/fim-test/config.txt
python -m fim init /tmp/fim-test --baseline /tmp/test-baseline.json

# Keine Änderungen → leerer Report
python -m fim scan /tmp/fim-test --baseline /tmp/test-baseline.json
# → "Unverändert: 1"

# Änderung machen
echo "modified" > /tmp/fim-test/config.txt
python -m fim scan /tmp/fim-test --baseline /tmp/test-baseline.json
# → zeigt config.txt als "GEÄNDERT"

# Neue Datei
touch /tmp/fim-test/new-file.txt
python -m fim scan /tmp/fim-test --baseline /tmp/test-baseline.json
# → zeigt new-file.txt als "NEU"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `scan_path` auf kleinem Verzeichnis (mit `tmp_path`) → korrektes Dict
- [ ] Test: `scan_path` mit Ausschluss → ausgeschlossene Datei nicht im Dict
- [ ] Test: `diff_baselines` mit identischen Dicts → `added=[], removed=[], changed=[]`
- [ ] Test: `diff_baselines` mit neuer Datei → in `added`
- [ ] Test: `diff_baselines` mit gelöschter Datei → in `removed`
- [ ] Test: `diff_baselines` mit geändertem Hash → in `changed`
- [ ] Test: `BaselineStore.save()` und `.load()` sind invers
- [ ] Test: `BaselineStore.exists()` vor und nach `save()`
- [ ] Test: `BaselineStore.load()` ohne existierende Datei → `FileNotFoundError`

---

## Bonus-Aufgaben

- [ ] **Inkrementelle Baseline-Updates:** `fim accept /etc/hosts` akzeptiert eine einzelne Datei ohne die gesamte Baseline neu zu erstellen
- [ ] **Audit-Log:** Alle `fim scan`-Ergebnisse werden in einer Log-Datei akkumuliert (nicht überschrieben) — historische Veränderungen nachverfolgbar
- [ ] **Vergleich zweier Baselines:** `fim diff baseline-a.json baseline-b.json` — zwei gespeicherte Snapshots direkt vergleichen
- [ ] **Permissions-Alert:** Spezielle Warnung wenn Security-kritische Dateien ihre Permissions änderten (`/etc/passwd`, `/etc/shadow`, `sshd_config`)

---

## Hinweise

**Hash-Wiederverwendung:** Importiere `hash_file` aus `hashinspect.core` — das ist genau der Zweck der sauberen Schnittstellendefinition aus Lab 01.

**relative Pfade:** Verwende `path.relative_to(root)` um relative Pfade zu berechnen. Als Dict-Key: `str(relative_path)`.

**mtime-Vergleich:** `os.stat(path).st_mtime` gibt Float (UNIX-Timestamp). Vergleiche mit `abs(old - new) > 1.0` um Floating-Point-Ungenauigkeiten zu vermeiden.

**Performance:** Für große Verzeichnisse (/etc, /usr) kann Hashing lange dauern. Zeige Fortschritt analog zu Lab 01 (Fortschrittsanzeige mit `\r`).

---

## Schnittstelle für `uctl`

```python
def scan_path(root: Path, exclude_patterns: list[str]) -> dict[str, dict]:
    """Scannt Verzeichnis und gibt Snapshot-Dict zurück."""

def diff_baselines(old: dict, new: dict) -> dict:
    """Vergleicht zwei Snapshots und gibt strukturiertes Diff zurück."""
```
