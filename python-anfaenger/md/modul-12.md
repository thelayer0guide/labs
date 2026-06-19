# Modul 12 — Python & das Betriebssystem

[← Modul 11](modul-11.md) | [Übersicht](catalog.md) | [Modul 13 →](modul-13.md)

---

**Phase:** Phase C — Praxis & Projekte
**Zeitaufwand:** 4–6 h
**Schwierigkeit:** ★★★☆☆ Fortgeschritten
**Voraussetzungen:** Modul 06

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)
- [bash](https://thelayer0guide.github.io/cheat-sheets/sheets/bash-cheatsheet.html)
- [systemd](https://thelayer0guide.github.io/cheat-sheets/sheets/systemd-cheatsheet.html)

---

## Lernziele

- CPU, RAM und Disk mit `psutil` auslesen
- Laufende Prozesse mit `psutil.process_iter()` inspizieren
- Netzwerkverbindungen und -statistiken abfragen
- Plattform-Details mit `platform`-Modul erfassen
- Umgebungsvariablen mit `os.environ` und `python-dotenv` verwalten
- Externe Befehle sicher ausführen und Output verarbeiten

---

## Hintergrund

`psutil` (process and system utilities) ist das Standard-Tool für Systeminformationen in Python. Es abstrahiert Linux-spezifische Interfaces (`/proc`) und funktioniert auf Windows und macOS identisch — ideal für plattformübergreifende Admin-Skripte.

Vorsicht bei `subprocess`: Mit `shell=True` und User-Input entsteht eine Shell-Injection-Schwachstelle. Immer als Liste übergeben: `["systemctl", "status", service_name]` — dann ist `service_name` ein Argument, kein Shell-Code.

---

## Schlüsselkonzepte

### Systemressourcen

```python
import psutil

cpu = psutil.cpu_percent(interval=1)  # Auslastung über 1 Sekunde
ram = psutil.virtual_memory()
disk = psutil.disk_usage("/")

print(f"CPU: {cpu}%")
print(f"RAM: {ram.used / 1e9:.1f} GB / {ram.total / 1e9:.1f} GB ({ram.percent}%)")
print(f"Disk: {disk.percent}% belegt")
```

### Prozesse filtern

```python
import psutil

def find_process(name: str) -> list[dict]:
    result = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_mb"]):
        if name.lower() in proc.info["name"].lower():
            result.append(proc.info)
    return result
```

### Servicecheck via subprocess

```python
import subprocess

def service_status(name: str) -> str:
    result = subprocess.run(
        ["systemctl", "is-active", name],
        capture_output=True, text=True
    )
    return result.stdout.strip()  # "active", "inactive", "failed"
```

---

## Aufgabe

Schreibe `sysmon.py` — ein Monitoring-Skript, das:

1. CPU, RAM, Disk und Netzwerk-IO sammelt (`psutil`)
2. Die Top-5 Prozesse nach CPU-Auslastung ausgibt
3. Systeminfos (Hostname, OS, Kernel, Python-Version) erfasst (`platform`)
4. Den Status von `ssh`, `cron` und `systemd-resolved` prüft (`subprocess + systemctl`) — graceful degradieren auf nicht-systemd-Systemen
5. Alle Daten als JSON-Snapshot in `snapshots/YYYY-MM-DD_HH-MM-SS.json` speichert
6. CLI: `--interval N` wiederholt die Messung N Sekunden, `--once` für Einmalmessung

---

## Anforderungen

- [ ] `psutil.cpu_percent(interval=1)` — nicht 0 (gibt immer 0.0)
- [ ] Snapshot-Verzeichnis wird automatisch erstellt wenn nicht vorhanden
- [ ] systemctl-Prüfung schlägt nicht fehl auf Systemen ohne systemd (z. B. macOS, WSL)
- [ ] JSON-Snapshot ist valid JSON und enthält alle sechs Kategorien
- [ ] `--interval`: zwischen Messungen `time.sleep(N)`, Ctrl+C sauber abgefangen

---

## Akzeptanzkriterien

```
python sysmon.py --once
# → Ausgabe aller Metriken
# → snapshots/2026-06-19_14-30-00.json erzeugt

python -c "import json; d=json.load(open('snapshots/$(ls snapshots | tail -1)')); print(list(d.keys()))"
# ['system', 'cpu', 'ram', 'disk', 'network', 'services', 'top_procs']
```

---

[← Modul 11](modul-11.md) | [Übersicht](catalog.md) | [Modul 13 →](modul-13.md)
