# Modul 06 — Werkzeuge der Standardbibliothek

[← Modul 05](modul-05.md) | [Übersicht](catalog.md) | [Modul 07 →](modul-07.md)

---

**Phase:** Phase B — Werkzeuge & Daten
**Zeitaufwand:** 5–7 h
**Schwierigkeit:** ★★★☆☆ Fortgeschritten
**Voraussetzungen:** Modul 05

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)
- [bash](https://thelayer0guide.github.io/cheat-sheets/sheets/bash-cheatsheet.html)

---

## Lernziele

- `pathlib.Path` für alle Dateisystemoperationen verwenden (kein `os.path` mehr)
- Verzeichnisse und Archive mit `shutil` automatisiert verwalten
- Externe Befehle sicher mit `subprocess.run()` aufrufen (kein `shell=True`)
- CLI-Interfaces mit `argparse` bauen: Argumente, Flags, Subcommands
- Zeitstempel formatieren und Zeiträume berechnen mit `datetime`
- IP-Adressen und Netzwerke mit `ipaddress` validieren

---

## Hintergrund

Die Python-Standardbibliothek ist umfangreich genug, dass man für die meisten Admin-Aufgaben kein einziges Drittpaket braucht. Das ist wichtig in Umgebungen, wo `pip install` nicht möglich ist oder nicht erwünscht ist.

`subprocess.run()` ist die sichere Methode für externe Befehle. Der Schlüssel: Befehle immer als Liste übergeben (`["ls", "-la", path]`), nie als String mit `shell=True` — das öffnet Shell-Injection-Schwachstellen.

---

## Schlüsselkonzepte

### pathlib — sicher und lesbar

```python
from pathlib import Path

log_dir = Path("/var/log")
for log_file in log_dir.rglob("*.log"):
    size = log_file.stat().st_size
    print(f"{log_file.name:30} {size / 1024:6.1f} KB")
```

### subprocess ohne shell=True

```python
import subprocess

result = subprocess.run(
    ["df", "-h", "/"],
    capture_output=True, text=True, timeout=10
)
if result.returncode == 0:
    print(result.stdout)
else:
    print("Fehler:", result.stderr)
```

### argparse mit Subcommands

```python
import argparse

parser = argparse.ArgumentParser(description="syscheck")
sub = parser.add_subparsers(dest="cmd")

disk_p = sub.add_parser("disk", help="Speicherplatz prüfen")
disk_p.add_argument("path", nargs="?", default="/")

env_p = sub.add_parser("env", help="Umgebungsvariable abfragen")
env_p.add_argument("key")

args = parser.parse_args()
```

### ipaddress Validierung

```python
import ipaddress

def parse_ip(raw: str) -> ipaddress.IPv4Address | None:
    try:
        return ipaddress.IPv4Address(raw)
    except ipaddress.AddressValueError:
        return None

net = ipaddress.IPv4Network("192.168.1.0/24")
print(ipaddress.IPv4Address("192.168.1.50") in net)  # True
```

---

## Aufgabe

Baue `syscheck` — ein CLI-Tool mit drei Subcommands:

- **`syscheck disk [PATH]`**: Zeigt Speicherbelegung via `shutil.disk_usage()`. Default: `/`. Flag `--warn PROZENT` gibt Warnung aus, wenn über Schwelle.
- **`syscheck env KEY`**: Liest Umgebungsvariable via `os.environ.get()`. Gibt Fehlermeldung + Exit-Code 1, wenn nicht gesetzt.
- **`syscheck run BEFEHL [ARGS...]`**: Führt externen Befehl aus und gibt stdout/stderr getrennt aus. Flag `--timeout N` (Default: 30).

---

## Anforderungen

- [ ] `argparse` mit drei Subcommands, jeder mit eigenem `--help`
- [ ] `disk`: gibt Gesamt, Benutzt, Frei in lesbarer Form aus; Warnung korrekt
- [ ] `env`: Exit-Code 1 + Fehlermeldung auf stderr wenn Variable fehlt
- [ ] `run`: kein `shell=True`; Timeout korrekt übergeben; returncode ausgeben
- [ ] Unbekannter Subcommand zeigt Hilfe und beendet mit Exit-Code 2

---

## Akzeptanzkriterien

```
python syscheck.py disk / --warn 80
# → Disk /: 45.2 GB / 100.0 GB (45%) — OK

python syscheck.py env HOME
# → HOME=/home/user

python syscheck.py env NICHT_GESETZT; echo $?
# → Fehler: NICHT_GESETZT nicht gesetzt
# → 1

python syscheck.py run ls -la /tmp
# → (Ausgabe von ls)
```

---

[← Modul 05](modul-05.md) | [Übersicht](catalog.md) | [Modul 07 →](modul-07.md)
