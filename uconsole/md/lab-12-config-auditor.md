# Lab 12 — SSH & Firewall Config Auditor

> **Phase 4 — Integrität & Monitoring**
> Voraussetzungen: Lab 04 (Parsing-Muster), Lab 06 (Findings-Modell)
> Geschätzte Zeit: 5–7 Stunden

---

## Lernziele

- Konfigurationsdateien ohne fertige Parser-Bibliothek parsen
- Ein strukturiertes Findings-Modell mit Severity entwerfen
- Best-Practice-Wissen zu SSH und Firewall-Konfiguration codieren
- Einen erweiterbaren Regelwerk-Mechanismus implementieren
- Markdown-Reports mit Severity-Sortierung generieren

---

## Hintergrund

Fehlkonfigurierte SSH- und Firewall-Einstellungen sind eine der häufigsten Ursachen für Sicherheitsvorfälle. `PermitRootLogin yes` in `sshd_config` erlaubt direkten Root-Zugriff. Eine fehlende Default-DROP-Policy in iptables lässt unerwarteten Traffic durch.

Dieses Tool codiert Security-Best-Practices in überprüfbare Regeln — genau wie ein Compliance-Scanner, nur selbst gebaut und verstanden.

---

## Aufgabe

Implementiere `configaudit` — einen Konfigurationsauditor für SSH und Firewall-Regeln.

### Projektstruktur

```
security-lab/
└── configaudit/
    ├── __init__.py
    ├── core.py
    ├── rules.py        ← Regel-Definitionen
    ├── parsers/
    │   ├── __init__.py
    │   ├── sshd.py     ← sshd_config Parser
    │   └── firewall.py ← iptables/nft Parser
    ├── cli.py
    └── tests/
        ├── __init__.py
        ├── test_core.py
        └── fixtures/
            ├── sshd_config_secure
            ├── sshd_config_insecure
            ├── iptables_save_good
            └── iptables_save_bad
```

---

## Das Findings-Modell

Definiere in `core.py`:

```python
from dataclasses import dataclass

@dataclass
class Finding:
    rule_id: str          # z. B. "SSH-001"
    severity: str         # "HIGH", "MEDIUM", "LOW", "INFO"
    title: str            # kurze Beschreibung
    description: str      # ausführliche Erklärung
    recommendation: str   # konkrete Handlungsempfehlung
    file: str             # geprüfte Datei
    line: int | None      # relevante Zeile (wenn anwendbar)
    current_value: str | None  # aktuell gefundener Wert
    expected_value: str | None # empfohlener Wert
```

---

## Anforderungen (Pflicht)

### parsers/sshd.py

- [ ] Funktion `parse_sshd_config(path: Path) -> dict[str, str]`
  - Parst `sshd_config` ohne externe Bibliotheken
  - Format: `Key Value` (durch Leerzeichen getrennt)
  - Ignoriert Kommentarzeilen (`#`) und leere Zeilen
  - Gibt Dict zurück: `{"PermitRootLogin": "yes", "Port": "22", ...}`
  - Keys und Values als Strings — keine Typkonvertierung

### parsers/firewall.py

- [ ] Funktion `parse_iptables_save(content: str) -> dict`
  - Parst Output von `iptables-save` (als String, nicht direkt ausgeführt)
  - Gibt zurück:
    ```python
    {
        "chains": {
            "INPUT":   {"policy": "ACCEPT"|"DROP"|"REJECT"|None, "rules": list[str]},
            "OUTPUT":  {...},
            "FORWARD": {...},
        },
        "has_default_drop_input": bool,
        "wide_open_accepts": list[str],  # Regeln mit -j ACCEPT und -s 0.0.0.0/0
    }
    ```

- [ ] Funktion `parse_nft_ruleset(content: str) -> dict`
  - Parst Output von `nft list ruleset` (vereinfacht: nur Default-Policy und Input-Hooks)
  - Gibt analoges Dict zurück

### rules.py

Definiere mindestens diese Regeln für SSH (als Funktionen oder Daten):

| Rule ID | Prüfung | Severity |
|---------|---------|----------|
| SSH-001 | `PermitRootLogin` != `no` | HIGH |
| SSH-002 | `PasswordAuthentication` != `no` | MEDIUM |
| SSH-003 | `Protocol` != `2` (falls gesetzt) | HIGH |
| SSH-004 | `PermitEmptyPasswords` == `yes` | HIGH |
| SSH-005 | `X11Forwarding` == `yes` | LOW |
| SSH-006 | `MaxAuthTries` > 3 (oder nicht gesetzt) | MEDIUM |
| SSH-007 | `LoginGraceTime` > 30 (oder nicht gesetzt) | LOW |
| SSH-008 | `AllowUsers` oder `AllowGroups` nicht gesetzt | INFO |

Und für Firewall:

| Rule ID | Prüfung | Severity |
|---------|---------|----------|
| FW-001 | INPUT-Policy nicht DROP/REJECT | HIGH |
| FW-002 | Weitreichende ACCEPT-Regeln (0.0.0.0/0) | MEDIUM |
| FW-003 | FORWARD-Policy nicht DROP | MEDIUM |

### core.py

- [ ] Funktion `audit_sshd_config(path: Path) -> list[Finding]`
  - Parst und wendet alle SSH-Regeln an
  - Gibt Finding für jede verletzten Regel zurück

- [ ] Funktion `audit_iptables(path: Path) -> list[Finding]`
  - Liest `iptables-save`-Output aus Datei
  - Wendet Firewall-Regeln an

- [ ] Funktion `generate_report(findings: list[Finding], fmt: str) -> str`
  - Sortiert Findings nach Severity: HIGH → MEDIUM → LOW → INFO
  - `fmt == "text"`: Terminal-freundlich
  - `fmt == "markdown"`: mit Tabellen und Links zu CIS-Benchmarks

### cli.py

- [ ] `configaudit sshd [PFAD] [--format text|markdown|json]`
  - Standard-Pfad: `/etc/ssh/sshd_config`
- [ ] `configaudit firewall [PFAD] [--type iptables|nft]`
  - Liest gespeicherten `iptables-save`-Output aus Datei (kein direktes Ausführen von iptables)

---

## CLI-Schnittstelle (vollständig)

```
configaudit sshd
configaudit sshd /path/to/sshd_config --format markdown
configaudit firewall iptables-rules.txt --type iptables
configaudit sshd --format json | python -m json.tool
```

Beispiel-Output (Text):
```
SSH CONFIG AUDIT: /etc/ssh/sshd_config
════════════════════════════════════════════

[HIGH] SSH-001 — PermitRootLogin
  Aktuell:     yes
  Empfohlen:   no
  Beschreibung: Root-Direktlogin ermöglicht Brute-Force-Angriffe auf den
                privilegiertesten Account.
  Empfehlung:  Setze 'PermitRootLogin no' in sshd_config

[MEDIUM] SSH-002 — PasswordAuthentication
  Aktuell:     yes (Standard)
  Empfohlen:   no
  Empfehlung:  Nutze ausschließlich Public-Key-Authentifizierung

[INFO] SSH-008 — AllowUsers/AllowGroups
  Empfehlung:  Schränke SSH-Zugriff auf bestimmte Nutzer ein

════════════════════════════════════════════
Findings: 3 total (1 HIGH, 1 MEDIUM, 0 LOW, 1 INFO)
```

---

## Test-Fixtures

Erstelle `tests/fixtures/sshd_config_insecure`:
```
PermitRootLogin yes
PasswordAuthentication yes
X11Forwarding yes
PermitEmptyPasswords no
```

Erstelle `tests/fixtures/sshd_config_secure`:
```
PermitRootLogin no
PasswordAuthentication no
X11Forwarding no
MaxAuthTries 3
LoginGraceTime 20
AllowUsers alice bob
```

Erstelle `tests/fixtures/iptables_save_bad`:
```
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
COMMIT
```

---

## Akzeptanzkriterien

```bash
# Insichere Config → findet Findings
python -c "
from configaudit.core import audit_sshd_config
from pathlib import Path
findings = audit_sshd_config(Path('tests/fixtures/sshd_config_insecure'))
high = [f for f in findings if f.severity == 'HIGH']
assert len(high) >= 1, 'Mindestens 1 HIGH-Finding erwartet'
print(f'Findings: {len(findings)} ({len(high)} HIGH)')
"

# Sichere Config → weniger Findings
python -c "
from configaudit.core import audit_sshd_config
from pathlib import Path
findings = audit_sshd_config(Path('tests/fixtures/sshd_config_secure'))
high = [f for f in findings if f.severity == 'HIGH']
assert len(high) == 0, f'Sichere Config sollte keine HIGH-Findings haben, bekam: {high}'
print('Sichere Config: OK')
"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `parse_sshd_config` auf insecure-Fixture → korrektes Dict
- [ ] Test: `parse_sshd_config` ignoriert Kommentare
- [ ] Test: `parse_sshd_config` → `PermitRootLogin` ist `"yes"` in insecure-Fixture
- [ ] Test: `audit_sshd_config` auf insecure-Fixture → enthält SSH-001 Finding
- [ ] Test: `audit_sshd_config` auf secure-Fixture → kein HIGH Finding
- [ ] Test: `parse_iptables_save` auf bad-Fixture → `has_default_drop_input == False`
- [ ] Test: `generate_report` sortiert nach Severity korrekt

---

## Bonus-Aufgaben

- [ ] **Eigenes Regelwerk:** Lade zusätzliche Regeln aus einer TOML-Datei:
  ```toml
  [[rules]]
  id = "CUSTOM-001"
  key = "Banner"
  expected = "/etc/issue.net"
  severity = "LOW"
  title = "Kein Login-Banner"
  ```
- [ ] **CIS-Benchmark-Links:** Ergänze jeden Finding mit dem entsprechenden CIS-Benchmark-Referenzlink
- [ ] **nft-Support:** Vollständiger Parser für `nft list ruleset`-Output

---

## Hinweise

**sshd_config parsen:** Die Datei hat kein Standard-Format (kein `=`). Typisches Format ist `Schlüssel Wert` mit Whitespace-Trennung. Kommentare beginnen mit `#`. Mehrfache Leerzeichen zwischen Key und Value sind möglich.

**Standardwerte:** viele sshd_config-Direktiven haben Standardwerte wenn nicht explizit gesetzt. Implementiere eine `SSHD_DEFAULTS`-Dict mit bekannten Defaults und nutze diese wenn ein Wert nicht in der Config steht.

**iptables-save Format:** Jede Regel beginnt mit `-A CHAIN`. Policy-Zeilen: `:CHAIN POLICY [packets:bytes]`.

---

## Schnittstelle für `uctl`

```python
def audit_sshd_config(path: Path) -> list[Finding]:
    """Auditiert sshd_config und gibt Findings zurück."""

def audit_iptables(path: Path) -> list[Finding]:
    """Auditiert iptables-save-Output und gibt Findings zurück."""
```
