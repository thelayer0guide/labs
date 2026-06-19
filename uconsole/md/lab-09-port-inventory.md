# Lab 09 — Local Port Inventory

> **Phase 3 — Krypto & Netzwerk**
> Voraussetzungen: Lab 00 (Projektstruktur)
> Geschätzte Zeit: 3–5 Stunden
> Externe Dependencies: `psutil`

---

## Lernziele

- `psutil` für Prozess- und Netzwerk-Informationen einsetzen
- Socket-zu-Prozess-Mapping verstehen
- Strukturierte Filter- und Exportlogik implementieren
- Whitelist-basierte Anomalie-Erkennung als Vorstufe zu Lab 10/11

---

## Hintergrund

Welche Ports lauschen auf meinem System? Welcher Prozess öffnet Port 8080? Seit wann läuft dieser Service? Diese Fragen sind bei der Härtung von Systemen, nach einer Systemkompromittierung oder schlicht beim Verstehen der eigenen Maschine zentral.

`ss -tlnp` oder `netstat -tlnp` zeigen das auf der Kommandozeile — du baust die Python-Version, die die Daten strukturiert und filterbar macht.

---

## Aufgabe

Implementiere `portinv` — ein Tool, das listening TCP/UDP-Ports inventarisiert, zugehörige Prozesse anzeigt und gegen eine Whitelist prüft.

### Projektstruktur

```
security-lab/
└── portinventory/
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

- [ ] Funktion `list_listening_ports() -> list[dict]`
  - Nutzt `psutil.net_connections(kind="inet")` und `psutil.net_connections(kind="inet6")`
  - Filtert auf `status == "LISTEN"` (TCP) und Ports ohne Verbindungsstatus (UDP)
  - Für jeden Port:
    ```python
    {
        "protocol":  str,       # "tcp" oder "udp"
        "local_ip":  str,       # gebundene IP oder "0.0.0.0" / "::"
        "local_port": int,
        "pid":       int | None,
        "process_name": str | None,
        "process_path": str | None,
        "process_user": str | None,
        "process_cmdline": str | None,   # erster Teil der Kommandozeile
        "ipv6": bool,
    }
    ```
  - Bei `pid=None` (kein Prozess zugeordnet): Felder als `None`
  - Bei Berechtigungsfehlern beim Prozess-Lookup: Felder mit `"<permission denied>"` befüllen

- [ ] Funktion `filter_ports(ports: list[dict], protocol: str | None, port_range: tuple[int, int] | None) -> list[dict]`
  - `protocol`: `"tcp"`, `"udp"` oder `None` (alle)
  - `port_range`: `(1, 1024)` für well-known ports, `None` für alle
  - Gibt gefilterte Liste zurück (keine Mutation der Eingabe)

- [ ] Funktion `load_whitelist(path: Path) -> dict`
  - Parst eine TOML-Datei (nutze `tomllib` aus der Stdlib ab Python 3.11):
    ```toml
    [[ports]]
    port = 22
    protocol = "tcp"
    description = "SSH"
    
    [[ports]]
    port = 80
    protocol = "tcp"
    description = "HTTP"
    ```
  - Gibt zurück: `{(port, protocol): description}`
  - Gibt leeres Dict zurück wenn Datei nicht existiert

- [ ] Funktion `check_against_whitelist(ports: list[dict], whitelist: dict) -> list[dict]`
  - Fügt jedem Port `"whitelisted": bool` und `"whitelist_note": str | None` hinzu
  - Nicht-whitelistete Ports sind potenzielle Anomalien

### cli.py

- [ ] `portinv [--proto tcp|udp] [--range 1-1024] [--whitelist ports.toml] [--format text|json] [--only-unknown]`
  - `--only-unknown`: zeigt nur nicht-whitelistete Ports

---

## CLI-Schnittstelle (vollständig)

```
portinv
portinv --proto tcp
portinv --range 1-1024
portinv --whitelist ~/ports.toml --only-unknown
portinv --format json > ports.json
```

Beispiel-Output (Text):
```
LOCAL PORT INVENTORY
═══════════════════════════════════════════════════
PROTO  PORT   IP              PROZESS        USER
───────────────────────────────────────────────────
tcp    22     0.0.0.0         sshd           root
tcp    80     0.0.0.0         nginx          www-data
tcp    3000   127.0.0.1       node           alice    [!] nicht whitelisted
udp    53     0.0.0.0         systemd-r...   systemd-resolve
tcp6   443    ::              nginx          www-data
═══════════════════════════════════════════════════
Gesamt: 5 Ports (1 nicht whitelisted)
```

---

## Akzeptanzkriterien

```bash
# Grundfunktion (erfordert laufendes System)
python -m portinventory
# → mind. Port 22 (SSH) sollte erscheinen wenn SSH läuft

# Filter
python -m portinventory --proto tcp
# → nur TCP-Ports

# JSON-Export
python -m portinventory --format json | python -m json.tool
# → valides JSON ohne Fehler

# Kern-Logik unit-testbar
python -c "
from portinventory.core import filter_ports
test_ports = [
    {'protocol': 'tcp', 'local_port': 22, 'local_ip': '0.0.0.0', 'pid': None,
     'process_name': 'sshd', 'process_path': None, 'process_user': 'root',
     'process_cmdline': None, 'ipv6': False},
    {'protocol': 'udp', 'local_port': 53, 'local_ip': '0.0.0.0', 'pid': None,
     'process_name': 'systemd-resolved', 'process_path': None, 'process_user': 'systemd-resolve',
     'process_cmdline': None, 'ipv6': False},
]
tcp_only = filter_ports(test_ports, 'tcp', None)
assert len(tcp_only) == 1
assert tcp_only[0]['local_port'] == 22
print('Filter OK')
"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `filter_ports` mit `protocol="tcp"` → nur TCP-Einträge
- [ ] Test: `filter_ports` mit `port_range=(1, 1024)` → nur Ports ≤ 1024
- [ ] Test: `filter_ports` mit `protocol=None, port_range=None` → alle Einträge unverändert
- [ ] Test: `load_whitelist` mit valider TOML-Datei → korrektes Dict
- [ ] Test: `load_whitelist` mit nicht existierender Datei → leeres Dict (kein Absturz)
- [ ] Test: `check_against_whitelist` markiert whitelistete Ports korrekt
- [ ] Test: `check_against_whitelist` markiert unbekannte Ports korrekt

Für `list_listening_ports`: Nutze `unittest.mock.patch("psutil.net_connections")` mit vorgefertigten Mock-Daten.

---

## Bonus-Aufgaben

- [ ] **Baseline-Integration:** `portinv --save baseline.json` speichert aktuellen Zustand. `portinv --diff baseline.json` zeigt neue/verschwundene Ports seit dem Snapshot — direkte Brücke zu Lab 10.
- [ ] **Prozess-Uptime:** Zeige wie lange der Prozess läuft (`psutil.Process(pid).create_time()`)
- [ ] **Wiederholtes Scannen:** `portinv --watch 5s` — alle 5 Sekunden neu scannen und Änderungen hervorheben (ohne Busy-Loop: `time.sleep()` zwischen Scans)

---

## Hinweise

**psutil und Berechtigungen:** Auf Linux benötigt `psutil` erhöhte Rechte um Prozessinformationen für alle Prozesse zu sehen. Wenn du als normaler Nutzer läufst, siehst du nur deine eigenen Prozesse — handle `psutil.AccessDenied` entsprechend.

**UDP-Ports:** `psutil.net_connections(kind="udp")` gibt UDP-Verbindungen zurück. UDP hat keinen "LISTEN"-Status — alle UDP-Sockets sind potenziell lauschend. Filtere nach `laddr.port > 0`.

**IPv6:** `::` bedeutet "alle Adressen" (wie `0.0.0.0` für IPv4). `::1` ist Loopback. Zeige IPv6-Einträge deutlich markiert.

**Prozess-Cmdline:** `psutil.Process(pid).cmdline()` gibt eine Liste zurück — join mit Space, aber kürze auf sinnvolle Länge für die Ausgabe.

---

## Schnittstelle für `uctl`

```python
def list_listening_ports() -> list[dict]:
    """Listet alle lauschenden TCP/UDP-Ports mit Prozess-Informationen."""

def filter_ports(ports: list[dict], protocol: str | None, port_range: tuple[int, int] | None) -> list[dict]:
    """Filtert Port-Liste nach Protokoll und Port-Range."""
```
