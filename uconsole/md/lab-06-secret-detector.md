# Lab 06 — Secret Detector

> **Phase 2 — Parsing & Forensik**
> Voraussetzungen: Lab 04 (Regex, Dateisystem-Iteration), Lab 03 (Entropie)
> Geschätzte Zeit: 5–8 Stunden

---

## Lernziele

- Regex-Pattern für bekannte Secret-Formate formulieren
- Severity-Modelle entwerfen und anwenden
- Rekursive Dateisuche mit gitignore-ähnlicher Ausschlusslogik implementieren
- Secrets im Report maskieren (Datenschutz bei Auditing-Tools)
- False-Positive-Management als Designproblem verstehen

---

## Hintergrund

Versehentlich commitete API-Keys, Passwörter in Config-Dateien, private Schlüssel im Projektordner — das sind reale Sicherheitsprobleme in jedem Entwickleralltag. Tools wie `detect-secrets` oder `truffleHog` lösen dieses Problem industriell. Du baust deine eigene Version.

**Wichtige Design-Entscheidung:** Dieses Tool ist ein Auditing-Werkzeug. Es zeigt dem Eigentümer des Codes, wo Secrets lauern — es ist kein Exfiltrations-Tool. Deshalb werden gefundene Secrets immer maskiert.

---

## Aufgabe

Implementiere `secretaudit` — einen rekursiven Code-Scanner, der bekannte Secret-Muster erkennt, bewertet und als maskierten Report ausgibt.

### Projektstruktur

```
security-lab/
└── secretdetect/
    ├── __init__.py
    ├── core.py
    ├── patterns.py    ← Regex-Pattern-Definitionen
    ├── cli.py
    └── tests/
        ├── __init__.py
        ├── test_core.py
        └── fixtures/
            ├── clean_file.py
            ├── dirty_file.py     (enthält Fake-Secrets für Tests)
            └── .secretauditignore
```

---

## Pattern-Definitionen

Definiere in `patterns.py` eine Liste von Pattern-Objekten:

```python
from dataclasses import dataclass

@dataclass
class SecretPattern:
    name: str           # z. B. "AWS Access Key ID"
    pattern: str        # Regex-Pattern
    severity: str       # "HIGH", "MEDIUM", "LOW"
    description: str    # Erklärung, was dieses Pattern bedeutet
```

Du musst mindestens diese Patterns implementieren:

| Name | Pattern | Severity |
|------|---------|----------|
| AWS Access Key ID | `AKIA[0-9A-Z]{16}` | HIGH |
| AWS Secret Key | `(?i)aws.{0,20}secret.{0,20}[a-z0-9/+]{40}` | HIGH |
| Private Key Header | `-----BEGIN (RSA\|EC\|OPENSSH\|DSA) PRIVATE KEY-----` | HIGH |
| JWT Token | `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}` | MEDIUM |
| Generic Password | `(?i)(password\|passwd\|pwd)\s*[=:]\s*["']?[^\s"']{8,}` | MEDIUM |
| Generic API Key | `(?i)(api[_-]?key\|apikey\|api[_-]?token)\s*[=:]\s*["']?[a-z0-9]{16,}` | MEDIUM |
| Generic Secret | `(?i)secret\s*[=:]\s*["']?[^\s"']{8,}` | LOW |

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `mask_secret(secret: str) -> str`
  - Zeigt erste 4 und letzte 4 Zeichen, Rest als `***`
  - Bei Strings unter 12 Zeichen: zeigt nur erste und letzte 2 Zeichen
  - `mask_secret("AKIAIOSFODNN7EXAMPLE")` → `"AKIA***...***MPLE"`

- [ ] Funktion `scan_line(line: str, line_number: int, patterns: list[SecretPattern]) -> list[dict]`
  - Prüft eine Zeile gegen alle Patterns
  - Gibt Liste von Findings zurück:
    ```python
    {
        "pattern_name": str,
        "severity": str,
        "line_number": int,
        "match": str,          # der vollständige Match
        "masked_match": str,   # maskierter Match
        "context": str,        # gesamte Zeile, Match ebenfalls maskiert
    }
    ```
  - Ein Finding pro Match (eine Zeile kann mehrere haben)

- [ ] Funktion `scan_file(path: Path, patterns: list[SecretPattern]) -> list[dict]`
  - Liest Datei zeilenweise
  - Ruft `scan_line` für jede Zeile auf
  - Fügt `"file": str(path)` zu jedem Finding hinzu
  - Überspringt Binärdateien (prüfe erste 8 KB auf Null-Bytes)
  - Bei Lesefehler: gibt `[{"file": str(path), "error": str(e)}]` zurück

- [ ] Funktion `should_exclude(path: Path, root: Path, exclude_patterns: list[str]) -> bool`
  - Prüft ob ein Pfad ausgeschlossen werden soll
  - Standard-Ausschlüsse (immer aktiv): `.git/`, `node_modules/`, `.venv/`, `venv/`, `__pycache__/`, `*.egg-info/`
  - Weitere Ausschlüsse aus der übergebenen Liste (Glob-Pattern)

- [ ] Funktion `scan_directory(root: Path, patterns: list[SecretPattern], ignore_file: Path | None) -> list[dict]`
  - Scannt `root` rekursiv
  - Liest `.secretauditignore`-Datei wenn vorhanden (eine Zeile = ein Glob-Pattern)
  - Verwendet `should_exclude` für jeden Pfad
  - Gibt alle Findings zurück

- [ ] Funktion `generate_report(findings: list[dict], fmt: str) -> str`
  - `fmt == "text"`: lesbarer Report mit Severity-Gruppierung
  - `fmt == "markdown"`: Markdown-Report mit Tabellen
  - `fmt == "json"`: JSON-Array

### cli.py

- [ ] `secretaudit [PFAD] [--format text|markdown|json] [--severity HIGH|MEDIUM|LOW] [--out DATEI]`
  - Standard-Pfad: aktuelles Verzeichnis
  - `--severity HIGH`: zeigt nur HIGH-Findings

---

## CLI-Schnittstelle (vollständig)

```
secretaudit ~/projects
secretaudit . --format markdown --out security-report.md
secretaudit /path/to/repo --severity HIGH
secretaudit . --format json | python -m json.tool
```

Beispiel-Output (Text):
```
SECRET DETECTOR: /home/user/projects
═══════════════════════════════════════════════════

[HIGH] AWS Access Key ID
  Datei: backend/.env
  Zeile: 12
  Fund:  AKIA***...***F3X
  Zeile: AWS_ACCESS_KEY_ID=AKIA***...***F3X

[HIGH] Private Key Header
  Datei: scripts/deploy.sh
  Zeile: 5
  Fund:  -----BEGIN RSA PRIVATE KEY-----

[MEDIUM] Generic Password
  Datei: config/database.yml
  Zeile: 8
  Fund:  pass***...***min

═══════════════════════════════════════════════════
Zusammenfassung: 3 Findings (2 HIGH, 1 MEDIUM, 0 LOW)
Gescannte Dateien: 47 | Übersprungen: 12 (Binärdateien/Ausgeschlossen)
```

---

## .secretauditignore Format

```
# Kommentare werden ignoriert
tests/fixtures/dirty_file.py     # bekannte Test-Fixtures
docs/examples/*.md
vendor/
```

---

## Test-Fixtures

Erstelle `tests/fixtures/dirty_file.py` mit bekannten Fake-Secrets:

```python
# Test-Datei mit Fake-Secrets (NUR FÜR TESTS)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
password = "mein_supergeheimes_passwort_123"
api_key = "sk-verylongapikey123456789abcdef"
```

Erstelle `tests/fixtures/clean_file.py` ohne Secrets (echten Code).

---

## Akzeptanzkriterien

```bash
# Maskierung korrekt
python -c "
from secretdetect.core import mask_secret
assert mask_secret('AKIAIOSFODNN7EXAMPLE') == 'AKIA***...***MPLE'
assert len(mask_secret('short')) < len('short') + 10  # nicht gekürzt aber maskiert
print('Maskierung OK')
"

# Scan findet bekannte Patterns
python -c "
from pathlib import Path
from secretdetect.core import scan_file
from secretdetect.patterns import DEFAULT_PATTERNS
findings = scan_file(Path('tests/fixtures/dirty_file.py'), DEFAULT_PATTERNS)
assert len(findings) >= 2, f'Mindestens 2 Findings erwartet, bekam {len(findings)}'
print(f'Gefunden: {len(findings)} Secrets')
"

# Keine gefundenen Secrets in sauberem Code
python -c "
from pathlib import Path
from secretdetect.core import scan_file
from secretdetect.patterns import DEFAULT_PATTERNS
findings = scan_file(Path('tests/fixtures/clean_file.py'), DEFAULT_PATTERNS)
assert findings == [], f'Keine Findings erwartet, bekam {findings}'
print('Saubere Datei korrekt erkannt')
"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `mask_secret` für String über 12 Zeichen → erste/letzte 4 sichtbar
- [ ] Test: `mask_secret` für String unter 12 Zeichen → erste/letzte 2 sichtbar
- [ ] Test: `scan_line` findet AWS-Key in bekannter Zeile
- [ ] Test: `scan_line` findet nichts in sauberer Zeile
- [ ] Test: `scan_file` auf `dirty_file.py` → mindestens 2 Findings
- [ ] Test: `scan_file` auf `clean_file.py` → 0 Findings
- [ ] Test: `should_exclude` schließt `.git/`-Verzeichnisse aus
- [ ] Test: `should_exclude` schließt `node_modules/` aus
- [ ] Test: `.secretauditignore` wird gelesen und angewendet
- [ ] Test: Gefundener Match ist im Report **maskiert** (nicht im Klartext)

---

## Bonus-Aufgaben

- [ ] **Entropie-Filter:** Kombiniere mit Lab 03 — zeige bei `MEDIUM`-Findings die Entropie des Match-Strings. Hohe Entropie (>3.5) erhöht Konfidenz; "password=test123" hat niedrige Entropie → wahrscheinlich Placeholder
- [ ] **Hash-basiertes Ignore:** `.secretauditignore` unterstützt auch SHA256-Hashes von Match-Strings für bekannte False Positives (wie `detect-secrets` Baseline)
- [ ] **Diff-Modus:** `secretaudit --diff HEAD~1`: scanne nur geänderte Zeilen seit letztem Commit (nutzt `git diff`)

---

## Hinweise

**Binärdatei-Erkennung:** Lese die ersten 8 KB und prüfe auf Null-Bytes (`b"\x00" in data`). Das ist eine Heuristik — zuverlässig genug für diesen Zweck.

**Pattern-Matching:** `re.finditer(pattern, line)` gibt alle Matches. `match.group(0)` ist der vollständige Match.

**Kontext-Snippet:** Die gesamte Zeile mit maskiertem Secret. Ersetze den Match in der Originalzeile durch die maskierte Version.

**Performance:** Bei großen Repos mit vielen Dateien kann `re.compile(pattern)` am Anfang (einmal für alle Patterns) erheblich schneller sein als `re.search(pattern, ...)` pro Zeile.

---

## Schnittstelle für `uctl`

```python
def scan_directory(root: Path, patterns: list[SecretPattern], ignore_file: Path | None = None) -> list[dict]:
    """Scannt ein Verzeichnis rekursiv auf Secrets."""

def generate_report(findings: list[dict], fmt: str = "text") -> str:
    """Erstellt einen formatierten Report aus den Findings."""
```
