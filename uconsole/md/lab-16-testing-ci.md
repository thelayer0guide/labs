# Lab 16 — Testing & CI für alle Tools

> **Phase 6 — Engineering & Integration**
> Voraussetzungen: mindestens 5 abgeschlossene Labs (01–15)
> Geschätzte Zeit: 6–10 Stunden

---

## Lernziele

- `pytest`-Fixtures und Parametrisierung professionell einsetzen
- Netzwerkzugriffe und Dateisystem-Operationen korrekt mocken
- Coverage-Reports interpretieren und sinnvolle Ziele setzen
- GitHub Actions für automatisierte Tests konfigurieren
- Testen als Design-Aktivität verstehen: was machst du testbar?

---

## Hintergrund

Tests sind in diesem Projekt nicht der letzte Schritt — sie sind das, was deine Tools erst produktionsreif macht. Wenn du in Lab 17 und im Capstone deine Tools zusammenführst, sind Tests das Sicherheitsnetz.

Dieses Lab hat keine neue Kernfunktionalität — es ist das Lab, in dem du die Qualität deiner bisherigen Arbeit überprüfst und systematisch verbesserst.

---

## Aufgabe

Für jedes deiner abgeschlossenen Tools (mindestens 5, idealerweise alle):

1. Vollständige Testabdeckung der Kernlogik (`core.py`)
2. Mocking für externe Abhängigkeiten
3. Coverage-Report mit Ziel ≥ 80% auf `core.py`
4. CI-Pipeline mit GitHub Actions

---

## Anforderungen (Pflicht)

### Teststruktur-Anforderungen

Für **jedes Tool** müssen folgende Test-Kategorien abgedeckt sein:

**Kategorie 1: Happy Path**
- [ ] Hauptfunktionen mit normalen Inputs
- [ ] Korrekte Rückgabewerte prüfen

**Kategorie 2: Edge Cases**
- [ ] Leere Eingaben (leere Datei, leeres Verzeichnis, leerer String)
- [ ] Maximale/minimale Werte
- [ ] Ungültige Inputs (falsche Typen, fehlende Felder)
- [ ] Dateien, die nicht gelesen werden können (Permission Denied)

**Kategorie 3: Fehlerbehandlung**
- [ ] Erwartete Exceptions werden korrekt ausgelöst
- [ ] Unerwartete Fehler werden nicht stillschweigend verschluckt
- [ ] Fehlermeldungen sind verständlich

**Kategorie 4: Boundary Conditions**
- [ ] Einzelnes Element in einer Liste
- [ ] Sehr großes Element (wo relevant)
- [ ] Strings mit Sonderzeichen, Unicode, Nullbytes

---

## Pflicht-Tests pro Tool

### Lab 01 (Hash Inspector)
- [ ] `hash_file` auf einer Datei mit bekanntem SHA256-Hash (Vergleich mit `sha256sum`-Ausgabe)
- [ ] `hash_file` auf einer leeren Datei → bekannter SHA256-Hash für leere Datei: `e3b0...`
- [ ] `hash_file` auf nicht existierender Datei → `FileNotFoundError`
- [ ] `hash_file` mit ungültigem Algorithmus → `ValueError`
- [ ] `parse_checksum_file` mit 5 validen Zeilen → korrekte Dict-Länge
- [ ] `parse_checksum_file` mit Kommentarzeilen → werden ignoriert
- [ ] `verify_hashes` — case-insensitive, Groß- und Kleinschreibung gemischt

### Lab 02 (Base Encoding)
- [ ] Parametrisierter Roundtrip-Test: `for fmt in ["base64", "base32", "hex", "url"]: assert decode(encode(data, fmt), fmt) == data`
- [ ] Inputs: leere Bytes, reiner Text, binäre Daten, alle 256 Byte-Werte
- [ ] `decode` mit ungültigem Base64 → `ValueError` mit beschreibender Meldung
- [ ] `detect_encoding` auf eindeutige Inputs

### Lab 03 (Entropy Scanner)
- [ ] `calculate_entropy(b"\x00" * 1000)` → 0.0
- [ ] `calculate_entropy(bytes(range(256)))` → nahe 8.0
- [ ] `scan_file` — Permission-Denied-Simulation mit Mock
- [ ] `scan_directory` mit Extension-Filter — nutze `tmp_path` mit echten Testdateien

### Lab 04 (Log Forensics)
- [ ] `parse_auth_log` auf Fixture → korrekte Anzahl `LogEntry`-Objekte
- [ ] Zeilen mit falschem Format → werden übersprungen
- [ ] `filter_by_time` — Grenzfall: Eintrag genau auf der Grenze

### Lab 07 (Certificate Auditor)
- [ ] `evaluate_certificate` für alle Status-Kombinationen
- [ ] `fetch_certificate` mit gemockter TLS-Verbindung

### Lab 10 (File Integrity Monitor)
- [ ] `scan_path` → Roundtrip: init + sofortiger scan → 0 Änderungen
- [ ] `diff_baselines` für alle drei Änderungstypen (added, removed, changed)
- [ ] `BaselineStore` — save/load/exists

---

## Mocking-Anforderungen

Verwende `unittest.mock.patch` für:

| Tool | Was zu mocken |
|------|---------------|
| Lab 07 | `socket.create_connection` oder `ssl.get_server_certificate` |
| Lab 09 | `psutil.net_connections` |
| Lab 11 | `psutil.process_iter` |
| Lab 14 | `httpx.post` oder `requests.post` |
| Lab 15 | `subprocess.run` (für lsusb, lsblk) |

**Beispiel-Pattern:**
```python
from unittest.mock import patch, MagicMock

def test_fetch_certificate_timeout():
    with patch("socket.create_connection") as mock_conn:
        mock_conn.side_effect = TimeoutError("Verbindung abgelaufen")
        with pytest.raises((TimeoutError, ConnectionError)):
            fetch_certificate("10.255.255.1", timeout=1.0)
```

---

## Coverage-Ziele

Führe `pytest --cov=. --cov-report=term-missing` aus und erreich:

| Modul | Mindest-Coverage |
|-------|-----------------|
| Jedes `core.py` | ≥ 80% |
| `shared/baseline.py` | ≥ 90% |
| `cli.py` (optional) | ≥ 40% |

**Ausgeschlossen von Coverage:** `if __name__ == "__main__":`, reine Stub-Funktionen

Füge in `pyproject.toml` ein:
```toml
[tool.pytest.ini_options]
addopts = "--cov=. --cov-report=term-missing --cov-config=.coveragerc"

[tool.coverage.report]
exclude_lines = [
    "if __name__ == .__main__.",
    "raise NotImplementedError",
]
```

---

## GitHub Actions CI

Erstelle `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: make lint
      - run: make test
```

Anforderungen:
- [ ] Workflow läuft bei jedem Push und Pull Request
- [ ] Testet gegen Python 3.11 und 3.12
- [ ] Führt `ruff check .` aus (Lint)
- [ ] Führt `pytest` aus
- [ ] Schlägt fehl wenn Tests fehlschlagen

---

## conftest.py (Shared Fixtures)

Erstelle `conftest.py` im Root des Repos mit gemeinsamen Fixtures:

```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_dir(tmp_path):
    """Kleines Testverzeichnis mit bekannten Dateien."""
    (tmp_path / "clean.txt").write_text("Hello World")
    (tmp_path / "binary.bin").write_bytes(bytes(range(256)))
    subdir = tmp_path / "sub"
    subdir.mkdir()
    (subdir / "config.txt").write_text("key=value")
    return tmp_path

@pytest.fixture
def known_hash_file(tmp_path):
    """Datei mit bekanntem SHA256-Hash."""
    data = b"security-lab-test-data-2026"
    path = tmp_path / "known.bin"
    path.write_bytes(data)
    return path, data
```

---

## Akzeptanzkriterien

```bash
# Alle Tests laufen durch
make test
# → 0 Failures, 0 Errors

# Coverage-Report
pytest --cov=. --cov-report=term-missing | grep "core.py"
# → Jedes core.py: ≥ 80%

# Lint sauber
make lint
# → 0 Fehler

# CI-Konfiguration valide
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
# → kein Fehler
```

---

## Was zu testen IST und was NICHT

**Testen:**
- Reine Logik in `core.py`
- Korrekte Fehlermeldungen
- Grenzfälle der Eingabe
- Korrektheit von Berechnungen (Entropie, Hashes, Parsing)

**Nicht testen:**
- Echte Netzwerkverbindungen (mocken stattdessen)
- Ausgabe-Formatierung (zu brittle)
- Integration mit echten System-Tools (mocken)
- Was Python/externe Libraries selbst testen

---

## Bonus-Aufgaben

- [ ] **Hypothesis:** Nutze `hypothesis`-Bibliothek für Property-based Testing bei Lab 01 (Hash) und Lab 02 (Encoding): `@given(st.binary())` — automatisch generierte Testdaten
- [ ] **ARM64-CI:** Füge einen CI-Job hinzu, der auf `ubuntu-22.04-arm64` (GitHub-hosted runner) läuft — prüft ob alle Pakete für ARM64 verfügbar sind
- [ ] **Test-Report:** `pytest --html=test-report.html` — lokaler HTML-Report

---

## Hinweise

**`tmp_path`-Fixture:** Von pytest bereitgestellt — jeder Test bekommt ein eigenes temporäres Verzeichnis. Wird nach dem Test automatisch gelöscht.

**Fixture-Scope:** `@pytest.fixture(scope="session")` für teure Fixtures (z. B. eine Baseline die einmal erstellt wird), `scope="function"` (Standard) für Fixtures die pro Test frisch sein sollen.

**parametrize:** 
```python
@pytest.mark.parametrize("algo,expected_len", [
    ("sha256", 64),
    ("md5", 32),
    ("sha1", 40),
])
def test_hash_length(algo, expected_len, known_hash_file):
    path, _ = known_hash_file
    result = hash_file(path, [algo])
    assert len(result[algo]) == expected_len
```

**Mock-Assertion:** Nutze `mock.assert_called_once_with(...)` um zu prüfen dass ein Mock korrekt aufgerufen wurde — wichtig für Tests die sicherstellen wollen, dass keine Netzwerkverbindung aufgebaut wird.
