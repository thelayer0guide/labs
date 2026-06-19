# Lab 17 — Plugin-Architektur Prototyp

> **Phase 6 — Engineering & Integration**
> Voraussetzungen: Lab 16 (alle Tests grün)
> Geschätzte Zeit: 4–6 Stunden

---

## Lernziele

- Abstrakte Basisklassen (`ABC`, `abstractmethod`) als Interface-Mechanismus nutzen
- `importlib.metadata.entry_points` für Plugin-Discovery verstehen
- `pyproject.toml` mit `entry_points`/`project.entry-points` konfigurieren
- Dynamisches Laden von Modulen mit `importlib.import_module`
- Das eigene Tool-Ökosystem in ein einheitliches System überführen

---

## Hintergrund

Im Capstone werden alle 15+ Tools zu `uctl` zusammengeführt. Die Plugin-Architektur ist das Bindeglied: Anstatt alle Tools hart in `uctl` zu codieren, entdeckt `uctl` sie dynamisch über den `entry_points`-Mechanismus von Python.

Das bedeutet: Neue Tools können hinzugefügt werden ohne `uctl`'s Code zu ändern — sie registrieren sich einfach als Plugin.

---

## Aufgabe

Definiere das Plugin-Interface, konvertiere 3 bestehende Tools in Plugins, und implementiere den Plugin-Loader.

### Projektstruktur

```
security-lab/
├── shared/
│   ├── __init__.py
│   ├── baseline.py
│   └── plugin.py       ← Plugin-Interface (ABC)
├── hashinspect/
│   ├── ...
│   └── plugin.py       ← Plugin-Implementierung
├── entropyscanner/
│   └── plugin.py
├── certaudit/
│   └── plugin.py
└── pyproject.toml      ← entry_points konfigurieren
```

---

## Das Plugin-Interface

Definiere in `shared/plugin.py`:

```python
from abc import ABC, abstractmethod
import argparse
from typing import Any

class SecurityTool(ABC):
    """Basisklasse für alle uctl-Plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Kurzer Name des Subcommands (z. B. 'hash', 'cert')."""
        ...
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Eine-Zeile-Beschreibung für die CLI-Hilfe."""
        ...
    
    @abstractmethod
    def register_args(self, subparser: argparse.ArgumentParser) -> None:
        """Registriert alle CLI-Argumente für diesen Subcommand."""
        ...
    
    @abstractmethod
    def run(self, args: argparse.Namespace) -> int:
        """Führt das Tool aus. Gibt Exit-Code zurück (0=OK, 1=Fehler/Fund)."""
        ...
    
    def validate_args(self, args: argparse.Namespace) -> list[str]:
        """Optionale Argument-Validierung vor run(). Gibt Fehlermeldungen zurück."""
        return []
```

---

## Anforderungen (Pflicht)

### shared/plugin.py

- [ ] `SecurityTool`-ABC wie oben definiert
- [ ] Funktion `load_plugins(group: str = "uctl.plugins") -> list[SecurityTool]`
  - Nutzt `importlib.metadata.entry_points(group=group)`
  - Lädt jedes Plugin, instanziiert es
  - Ignoriert (mit Warnung) Plugins die `SecurityTool` nicht korrekt implementieren
  - Gibt sortierte Liste nach `plugin.name` zurück

- [ ] Funktion `load_plugin_from_module(module_path: str) -> SecurityTool | None`
  - Lädt ein Plugin direkt per Modul-Pfad: `"hashinspect.plugin:HashInspectPlugin"`
  - Nützlich für Testing und manuelle Registration

### Plugin-Implementierungen

Implementiere `SecurityTool` für **mindestens 3 Tools**:

#### hashinspect/plugin.py

```python
class HashInspectPlugin(SecurityTool):
    
    @property
    def name(self) -> str:
        return "hash"
    
    @property
    def description(self) -> str:
        return "Berechnet kryptografische Hashes für Dateien"
    
    def register_args(self, subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("files", nargs="+", type=Path)
        subparser.add_argument("--algo", default="sha256")
        # ...
    
    def run(self, args: argparse.Namespace) -> int:
        # Nutzt hash_file aus hashinspect.core
        # Gibt 0 oder 1 zurück
        ...
```

Implementiere entsprechend für 2 weitere Tools deiner Wahl.

### pyproject.toml

- [ ] `entry_points` für alle implementierten Plugins konfigurieren:

```toml
[project.entry-points."uctl.plugins"]
hash    = "hashinspect.plugin:HashInspectPlugin"
entropy = "entropyscanner.plugin:EntropyScannerPlugin"
cert    = "certaudit.plugin:CertAuditPlugin"
```

### uctl_proto.py (Mini-Dispatcher)

- [ ] Erstelle eine einfache `uctl_proto.py` im Root als Proof-of-Concept:
  - Lädt alle Plugins via `load_plugins()`
  - Baut einen `argparse`-Parser mit einem Subparser pro Plugin
  - Dispatcht auf das richtige Plugin
  - Zeigt `--help` mit allen registrierten Tools

---

## CLI-Schnittstelle (vollständig)

```
python uctl_proto.py --help
python uctl_proto.py hash datei.iso
python uctl_proto.py entropy ~/Downloads
python uctl_proto.py cert github.com
```

Beispiel-Output `uctl_proto.py --help`:
```
uctl — Unified Security Toolkit (Prototyp)

Subcommands:
  cert      Auditiert TLS-Zertifikate
  entropy   Scannt Verzeichnisse auf Shannon-Entropie
  hash      Berechnet kryptografische Hashes für Dateien

Optionen:
  --help    Zeigt diese Hilfe
```

---

## Akzeptanzkriterien

```bash
# Plugin-Loading funktioniert
pip install -e .   # installiert entry_points
python -c "
from shared.plugin import load_plugins
plugins = load_plugins()
names = [p.name for p in plugins]
print('Geladene Plugins:', names)
assert 'hash' in names
assert len(plugins) >= 3
"

# Dispatcher funktioniert
python uctl_proto.py hash --help
# → zeigt argparse-Hilfe für hash-Plugin

python uctl_proto.py hash /dev/null --algo sha256
# → gibt SHA256 für leere/null-Input aus (je nach OS)

# entry_points korrekt konfiguriert
python -c "
from importlib.metadata import entry_points
eps = entry_points(group='uctl.plugins')
print('entry_points:', list(eps))
assert len(list(eps)) >= 3
"
```

---

## Tests (Anforderungen an test_core.py)

Erstelle `shared/tests/test_plugin.py`:

- [ ] Test: `SecurityTool` kann nicht direkt instanziiert werden (ist ABC)
- [ ] Test: Konkrete Plugin-Implementierung instanziiert sich korrekt
- [ ] Test: `plugin.name` gibt String zurück
- [ ] Test: `plugin.run(args)` gibt int zurück (0 oder 1)
- [ ] Test: `load_plugin_from_module("hashinspect.plugin:HashInspectPlugin")` gibt Instanz zurück
- [ ] Test: `load_plugins()` gibt mindestens 3 Plugins zurück (nach `pip install -e .`)
- [ ] Test: Plugins haben eindeutige Namen (kein Duplikat)

---

## Bonus-Aufgaben

- [ ] **Konfigurations-Weitergabe:** `SecurityTool` erhält beim Aufruf auch eine `config: dict` aus der zentralen `uctl.toml` — Plugins können Defaults daraus lesen
- [ ] **Versionierung:** Jedes Plugin deklariert `min_uctl_version: str` — der Loader warnt bei inkompatiblen Versionen
- [ ] **Lazy Loading:** Plugins werden erst importiert wenn sie aufgerufen werden — reduziert Startup-Zeit

---

## Hinweise

**entry_points Installation:** Plugins werden über `entry_points` registriert, aber die `entry_points`-Konfiguration wird erst nach `pip install -e .` aktiv. Für Tests kannst du `load_plugin_from_module()` direkt nutzen.

**ABC und abstractmethod:**
```python
from abc import ABC, abstractmethod

class MyABC(ABC):
    @abstractmethod
    def my_method(self): ...

# MyABC() → TypeError: Can't instantiate abstract class
```

**importlib.metadata (Python 3.9+):**
```python
from importlib.metadata import entry_points
eps = entry_points(group="uctl.plugins")
for ep in eps:
    cls = ep.load()  # gibt die Klasse zurück
    plugin = cls()
```

**Robustheit:** Wenn ein Plugin-Import fehlschlägt (z. B. fehlende Dependency), soll der Loader das Plugin überspringen und eine Warnung ausgeben — nicht den gesamten Start von `uctl` blockieren.

---

## Schnittstelle für den Capstone

```python
from shared.plugin import SecurityTool, load_plugins

# Im Capstone:
plugins = load_plugins()
# → alle registrierten Tools als fertige SecurityTool-Instanzen
```

Das ist die Brücke: Der Capstone muss für das Hinzufügen eines weiteren Tools nur `entry_points` erweitern — kein Code-Änderung in `uctl` selbst.
