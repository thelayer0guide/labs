# Lab 07 — Certificate Auditor

> **Phase 3 — Krypto & Netzwerk**
> Voraussetzungen: Lab 00 (Projektstruktur)
> Kann parallel zu Phase 2 begonnen werden
> Geschätzte Zeit: 4–6 Stunden
> Externe Dependencies: `cryptography`

---

## Lernziele

- TLS-Verbindungen programmatisch aufbauen mit `socket` und `ssl`
- X.509-Zertifikatsstruktur verstehen und parsen
- `datetime`-Vergleiche für Ablauf-Warnungen implementieren
- Netzwerkprogrammierung mit korrektem Timeout-Handling
- Zertifikatsketten inspizieren

---

## Hintergrund

TLS-Zertifikate sind das Fundament verschlüsselter Kommunikation. Sie laufen ab, werden falsch konfiguriert oder nutzen veraltete Algorithmen. Als Security-Analyst oder Sysadmin willst du schnell prüfen können: Läuft dieses Zertifikat bald ab? Welche Domains sind abgedeckt? Ist die Kette vollständig?

Auf der uConsole ist dieses Tool besonders nützlich: Du kannst Heimnetz-Dienste (Router, NAS, selbst gehostete Services) schnell prüfen, auch ohne Browser.

---

## Aufgabe

Implementiere `certaudit` — ein Tool, das TLS-Zertifikate von Hosts abruft, analysiert und bewertet.

### Projektstruktur

```
security-lab/
└── certaudit/
    ├── __init__.py
    ├── core.py
    ├── cli.py
    └── tests/
        ├── __init__.py
        └── test_core.py
```

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `fetch_certificate(host: str, port: int = 443, timeout: float = 10.0) -> dict`
  - Baut TLS-Verbindung auf mit `ssl.create_default_context()` und `socket.create_connection()`
  - Ruft Zertifikat ab **ohne** vollständige Validierung (nutze `ssl.get_server_certificate()` oder `SSLSocket.getpeercert(binary_form=True)`)
  - Parst Zertifikat mit `cryptography.x509.load_der_x509_certificate()` oder `load_pem_x509_certificate()`
  - Gibt folgendes Dict zurück:
    ```python
    {
        "host": str,
        "port": int,
        "subject_cn": str,          # Common Name
        "issuer_cn": str,           # Issuer Common Name
        "issuer_org": str | None,
        "not_before": str,          # ISO 8601
        "not_after": str,           # ISO 8601
        "days_until_expiry": int,   # negativ wenn abgelaufen
        "san_domains": list[str],   # Subject Alternative Names
        "signature_algorithm": str, # z. B. "sha256WithRSAEncryption"
        "serial_number": str,       # Hex
        "chain_length": int,        # Anzahl Zertifikate in der Kette
    }
    ```
  - Wirft `ConnectionError` bei Verbindungsproblemen
  - Wirft `TimeoutError` bei Timeout
  - Wirft `ssl.SSLError` bei TLS-Fehlern (nicht selbst fangen)

- [ ] Funktion `evaluate_certificate(cert: dict, warn_days: int = 30) -> dict`
  - Fügt Bewertungsfelder hinzu:
    ```python
    {
        ...alle cert-Felder...,
        "status": "OK" | "WARNING" | "CRITICAL" | "EXPIRED",
        "warnings": list[str],   # Liste von Warnungen
    }
    ```
  - `EXPIRED` wenn `days_until_expiry <= 0`
  - `CRITICAL` wenn `days_until_expiry <= 7`
  - `WARNING` wenn `days_until_expiry <= warn_days`
  - `OK` sonst
  - Warnungen für: SHA1-Signaturalgorithmus, kein SAN-Eintrag für den angefragten Host

- [ ] Funktion `batch_audit(hosts: list[str], port: int, warn_days: int, timeout: float) -> list[dict]`
  - Prüft alle Hosts nacheinander
  - Fehler pro Host werden als `{"host": str, "error": str}` in die Liste aufgenommen
  - Kein Absturz bei einzelnem fehlerhaften Host

### cli.py

- [ ] `certaudit HOST [HOST ...] [--port 443] [--warn-days 30] [--format text|json] [--file host-liste.txt]`
  - `--file host-liste.txt`: eine Domain pro Zeile, Kommentarzeilen (#) ignorieren

---

## CLI-Schnittstelle (vollständig)

```
certaudit github.com
certaudit github.com gitlab.com codeberg.org
certaudit --file hosts.txt --warn-days 14 --format json
certaudit 192.168.1.1 --port 8443    (Heimnetz-Gerät)
```

Beispiel-Output (Text):
```
CERTIFICATE AUDIT
═══════════════════════════════════════════════════

HOST: github.com:443                         [OK]
─────────────────────────────────────────────────
  Subject    github.com
  Issuer     DigiCert TLS RSA SHA256 2020 CA1
  Gültig     2025-03-14 — 2026-09-17
  Restlaufzeit  91 Tage
  Algorithmus   sha256WithRSAEncryption
  SAN-Einträge  github.com, www.github.com

HOST: expired.example.com:443           [EXPIRED]
─────────────────────────────────────────────────
  Zertifikat ist seit 14 Tagen abgelaufen!
  [!] Zertifikat abgelaufen am 2026-06-05

═══════════════════════════════════════════════════
Zusammenfassung: 2 Hosts · 1 OK · 0 WARNING · 1 EXPIRED
```

---

## Akzeptanzkriterien

```bash
# Grundlegende Funktion (erfordert Internetzugang)
python -m certaudit github.com
# → Muss Zertifikat-Info anzeigen ohne Absturz

# Timeout-Verhalten
python -m certaudit 10.255.255.1 --port 443
# → Muss nach timeout_seconds mit Fehlermeldung enden, kein Hang

# Exit-Code
python -m certaudit github.com; echo "Exit: $?"
# → Exit 0 wenn OK

# Kern-Logik ohne Netzwerk testbar
python -c "
from certaudit.core import evaluate_certificate
cert = {'days_until_expiry': 5, 'signature_algorithm': 'sha256WithRSAEncryption', 
        'san_domains': ['github.com'], 'host': 'github.com',
        'subject_cn': 'github.com', 'issuer_cn': 'DigiCert',
        'issuer_org': 'DigiCert Inc.', 'not_before': '2025-01-01T00:00:00',
        'not_after': '2026-01-01T00:00:00', 'serial_number': 'deadbeef',
        'chain_length': 2}
result = evaluate_certificate(cert, warn_days=30)
assert result['status'] == 'CRITICAL'
print('evaluate_certificate: OK')
"
```

---

## Tests (Anforderungen an test_core.py)

Da echte Netzwerkzugriffe in Tests vermieden werden sollten, mocke die TLS-Verbindung:

- [ ] Test: `evaluate_certificate` mit `days_until_expiry > 30` → `status == "OK"`
- [ ] Test: `evaluate_certificate` mit `days_until_expiry = 20` → `status == "WARNING"`
- [ ] Test: `evaluate_certificate` mit `days_until_expiry = 3` → `status == "CRITICAL"`
- [ ] Test: `evaluate_certificate` mit `days_until_expiry = -1` → `status == "EXPIRED"`
- [ ] Test: `evaluate_certificate` mit SHA1-Algorithmus → enthält Warnung in `warnings`
- [ ] Test: `batch_audit` mit fehlschlagendem Host → kein Absturz, Fehler im Ergebnis

Für Netzwerk-Tests: nutze `unittest.mock.patch` um `socket.create_connection` zu mocken, oder einen lokalen Test-HTTPS-Server (Bonus).

---

## Bonus-Aufgaben

- [ ] **Schwache Algorithmen:** Erkenne und flagge: SHA1, MD5, RSA < 2048 Bit, EC-Kurven unter 256 Bit
- [ ] **OCSP-Check:** Prüfe ob Zertifikat widerrufen wurde (erfordert Netzwerkzugriff)
- [ ] **Export als PEM:** `--save cert.pem` speichert das Zertifikat lokal
- [ ] **Parallele Prüfung:** `batch_audit` nutzt `concurrent.futures.ThreadPoolExecutor` für mehrere Hosts gleichzeitig

---

## Hinweise

**TLS ohne vollständige Validierung:** Für reine Inspektion (kein echter Request) nutze:
```python
import ssl, socket
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
```
Dies erlaubt dir auch selbst-signierte Zertifikate zu inspizieren.

**Zertifikat parsen:** `ssl.get_server_certificate((host, port))` gibt PEM-String zurück. Mit `cryptography.x509.load_pem_x509_certificate(pem.encode())` kommst du an alle X.509-Felder.

**SAN-Einträge:** `cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME).value.get_values_for_type(x509.DNSName)` gibt Liste der DNS-Namen zurück.

**Timeout:** `socket.create_connection((host, port), timeout=10)` — der Timeout gilt nur für den Connect. Setze zusätzlich `sock.settimeout(10)`.

**uConsole-Tipp:** Gegen lokale IPs (Router, NAS) funktioniert das Tool auch ohne Internet. Test: `certaudit 192.168.1.1 --port 443` gegen deinen Heimrouter.

---

## Schnittstelle für `uctl`

```python
def fetch_certificate(host: str, port: int = 443, timeout: float = 10.0) -> dict:
    """Ruft TLS-Zertifikat von einem Host ab und gibt strukturierte Daten zurück."""

def evaluate_certificate(cert: dict, warn_days: int = 30) -> dict:
    """Bewertet ein Zertifikat und gibt Status + Warnungen zurück."""
```
