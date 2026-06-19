# Capstone — `uctl`: Unified Security Toolkit

> **Phase 6 — Engineering & Integration**
> Voraussetzungen: Lab 16 (Tests) + Lab 17 (Plugin-Architektur) + mindestens 8 Tools fertig
> Geschätzte Zeit: 8–15 Stunden

---

## Überblick

`uctl` ist das Endprodukt aller Labs. Es vereint alle deine Tools unter einer einheitlichen CLI, einer zentralen Konfiguration und einem gemeinsamen Output-Format. Am Ende läuft es auf der uConsole — installierbar via `pipx install .`, auch offline.

Das Capstone ist kein neues Lab — es ist das Zusammenführen von allem, was du gebaut hast.

---

## Ziel-Vision

```bash
# Alle deine Tools unter einem Dach
uctl hash       kali-linux-2026.iso
uctl enc        decode "SGVsbG8="
uctl entropy    ~/Downloads --threshold 7.5
uctl logs       /var/log/auth.log --since 7d
uctl meta       foto.jpg
uctl secrets    ~/projects --format md
uctl cert       github.com
uctl pw         --stdin
uctl ports      --proto tcp
uctl fim        scan /etc
uctl procs      --diff
uctl config     /etc/ssh/sshd_config
uctl pcap       capture.pcap
uctl cve        --source pip
uctl hw         --diff
```

---

## Anforderungen (Pflicht)

### CLI-Framework

- [ ] Ersetze alle bestehenden `argparse`-Subcommands durch **Typer**:
  - `pip install typer`
  - Eine `uctl/app.py` als zentraler Einstiegspunkt
  - Jedes Plugin registriert einen Typer-Subcommand via Plugin-Interface

- [ ] Einheitliche Fehlerbehandlung:
  - Alle unerwarteten Exceptions werden abgefangen, Fehlermeldung auf `stderr`, Exit-Code 1
  - Bekannte Fehler (z. B. Datei nicht gefunden) mit verständlicher Meldung

- [ ] `--verbose` / `--quiet` Flags global (für alle Subcommands):
  - `--verbose`: Debug-Logging aktivieren
  - `--quiet`: nur Ergebnis, keine Status-Meldungen

### Zentrale Konfiguration

- [ ] `~/.config/uctl/config.toml` als zentrale Konfigurationsdatei:
  ```toml
  [defaults]
  output_format = "text"   # "text", "json"
  
  [entropy]
  threshold = 7.5
  
  [cert]
  warn_days = 30
  
  [fim]
  baseline_dir = "~/.local/share/uctl/fim"
  
  [secrets]
  exclude_dirs = ["node_modules", ".venv", "__pycache__"]
  ```
  
- [ ] Konfiguration wird beim Start geladen und als `dict` an alle Plugins weitergegeben
- [ ] CLI-Argumente überschreiben Konfigurationsdatei-Werte (CLI hat höhere Priorität)
- [ ] `uctl config --show` zeigt aktuelle Konfiguration

### Zentrales Logging

- [ ] Logging-Setup via `logging`-Modul:
  - Konsole: nur WARNING und höher (Standard)
  - Log-Datei: `~/.local/share/uctl/uctl.log` (alle Level)
  - `--verbose`: setzt Konsolen-Level auf DEBUG
  - `--quiet`: setzt Konsolen-Level auf ERROR
- [ ] Format: `[2026-06-19 10:00:00] [INFO] cert: Verbinde mit github.com:443`

### Einheitliches Output-Format

- [ ] Alle Subcommands unterstützen `--json` (gibt strukturiertes JSON aus)
- [ ] Terminal-Output nutzt `rich` für Tabellen, Farbmarkierungen, Status-Icons
- [ ] Terminal-Breite dynamisch: `shutil.get_terminal_size().columns` — nie mehr als diese Breite
- [ ] Online-Tools sind explizit markiert (`[online]` im `--help`)

### Plugin-Integration

- [ ] Alle fertiggestellten Tools sind als Plugins registriert (aus Lab 17)
- [ ] `uctl --list-plugins` zeigt alle registrierten Tools mit Kurzbeschreibung
- [ ] Plugin-Ladezeit ist akzeptabel: `uctl --help` in < 2 Sekunden

### Packaging

- [ ] `pyproject.toml` vollständig für Distribution:
  ```toml
  [project]
  name = "uctl"
  version = "0.1.0"
  requires-python = ">=3.11"
  dependencies = ["typer", "rich", "psutil", "cryptography", "httpx", "Pillow", "pypdf", "packaging"]
  
  [project.scripts]
  uctl = "uctl.app:main"
  ```

- [ ] `pipx install .` installiert `uctl` als eigenständiges CLI-Tool
- [ ] `uctl --version` gibt Version aus

---

## uConsole End-to-End-Test

Führe nach der Installation auf der uConsole folgende Befehle aus — alle müssen funktionieren:

```bash
# Installation
pipx install .
uctl --version

# Offline-fähige Tools (kein Netz nötig)
uctl hash /etc/hostname
uctl entropy /etc --min-size 1024
uctl logs /var/log/auth.log
uctl meta /boot/config.txt
uctl ports
uctl fim init /etc
uctl fim scan /etc
uctl procs snapshot
uctl procs scan
uctl hw
uctl config /etc/ssh/sshd_config

# Online-Tools (erfordern Netz)
uctl cert github.com
uctl cve --source dpkg

# Skript-Verkettung
uctl ports --format json | python -m json.tool
uctl hash /bin/ls --format json | jq .sha256

# Terminal-Breite
uctl entropy /etc | cat   # muss ohne Umbruchs-Fehler funktionieren
```

---

## Akzeptanzkriterien

### Funktional

- [ ] Alle integrierten Tools geben sinnvolle Ergebnisse aus
- [ ] `--json` funktioniert für alle Tools und gibt valides JSON aus
- [ ] Fehler-Szenarien (Datei nicht gefunden, Netz nicht verfügbar) werden graceful behandelt
- [ ] Exit-Code 0 bei Erfolg, 1 bei Fehler

### Performance (uConsole)

- [ ] `uctl --help` startet in < 3 Sekunden auf der uConsole
- [ ] `uctl hash /etc/hostname` braucht < 1 Sekunde
- [ ] Kein Tool hält einen dauerhaften CPU-Loop (ohne `--watch`)

### Zuverlässigkeit

- [ ] Kein Tool stürzt ab wenn ein Argument fehlt → `--help` anzeigen
- [ ] Kein Tool stürzt ab wenn eine Datei nicht lesbar ist
- [ ] Online-Tools zeigen verständliche Fehlermeldung wenn kein Netz

---

## Plugin-Interface (finales Design)

```python
from shared.plugin import SecurityTool
import typer

class SecurityToolV2(SecurityTool):
    """Erweitertes Interface für Typer-Integration."""
    
    @property
    @abstractmethod
    def typer_app(self) -> typer.Typer:
        """Gibt Typer-App für diesen Subcommand zurück."""
        ...
    
    @property
    def online_only(self) -> bool:
        """True wenn Tool Internetzugriff benötigt."""
        return False
```

---

## Architektur-Übersicht

```
uctl/
├── app.py           ← Typer-App, Plugin-Dispatcher, Config-Loading
├── config.py        ← Config-Handling (TOML laden, mergen)
├── logging_setup.py ← Logging-Konfiguration
└── output.py        ← Einheitliche Output-Utilities (rich-Tabellen, JSON)

shared/
├── plugin.py        ← SecurityTool ABC
├── baseline.py      ← BaselineStore
└── output.py        ← Output-Utils (gemeinsam)

hashinspect/
entropyscanner/
... (alle Tools)
```

---

## Bonus-Anforderungen

- [ ] **Offline-Markierung:** `uctl ports [online]` — Tools die Internet brauchen sind in `--help` markiert
- [ ] **Alias-Support:** `uctl h` als Alias für `uctl hash`
- [ ] **Autocomplete:** `uctl --install-completion` installiert Shell-Completion (Typer bietet das out-of-the-box)
- [ ] **Colored Output unterdrücken:** `NO_COLOR=1 uctl hash file.iso` oder `--no-color` für Terminal-Pipes
- [ ] **ARM64 Wheel-Cache:** Erstelle ein `scripts/build-wheels-arm64.sh` das alle Dependencies als Wheels baut und cached — so kann `pipx install .` auch ohne Internet funktionieren

---

## Hinweise

**Typer-Integration:** Typer und argparse können koexistieren. Du kannst bestehende argparse-basierte Plugins auch ohne Umbau integrieren, indem du einen Typer-Callback erzeugst der `argparse.parse_args()` intern aufruft.

**rich.console:** Erstelle eine einzelne `Console`-Instanz in `uctl/output.py` und importiere sie überall — das verhindert mehrere Konsolen-Initialisierungen.

**TOML mit tomllib:**
```python
import tomllib
from pathlib import Path

config_path = Path.home() / ".config" / "uctl" / "config.toml"
if config_path.exists():
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
else:
    config = {}
```

**pipx auf ARM64:** Teste `pipx install .` früh auf der uConsole. Manche Dependencies (z. B. `Pillow`, `cryptography`) müssen aus dem Source kompiliert werden wenn kein ARM64-Wheel verfügbar ist.

---

## Was das Capstone beweist

Wenn `uctl` läuft, hast du:

1. **15+ eigenständige Security-Tools** gebaut
2. **Plugin-Architektur** designed und implementiert
3. **Testen** professionell betrieben (≥ 80% Coverage)
4. **ARM64-Deployment** auf echter Hardware gemeistert
5. **CLI-Ergonomie** durchgehend gedacht (Exit-Codes, JSON, --help)
6. **Offline-first-Design** als Constraint ernst genommen

Das ist kein Tutorial-Ergebnis — das ist ein echtes Werkzeug.
