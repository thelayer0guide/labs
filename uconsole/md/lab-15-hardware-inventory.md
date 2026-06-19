# Lab 15 — USB & Hardware Inventory

> **Phase 5 — Erweiterte Analyse**
> Voraussetzungen: Lab 09 (psutil, Subprocess-Pattern), Lab 10 (BaselineStore)
> Geschätzte Zeit: 3–5 Stunden
> uConsole-spezifisches Lab

---

## Lernziele

- `subprocess.run()` sicher für externe CLI-Tools verwenden
- Strukturierte JSON-Ausgabe von System-Tools direkt parsen
- Nicht-strukturierte CLI-Ausgabe (lsusb) mit Regex parsen
- Das Baseline-Pattern auf Hardware-Inventarisierung anwenden
- Kernel-Module über das `/proc`- und `sys`-Filesystem inspizieren

---

## Hintergrund

Die uConsole hat mehrere exponierte USB-Ports und ein Steckplatz-System. Auf einem mobilen Security-Gerät ist es nützlich zu wissen: Welche USB-Geräte sind angeschlossen? Welche Block-Devices gibt es? Ist `usb-storage` geladen?

Mit dem Baseline-Pattern aus Lab 10 wird das Tool noch nützlicher: Es alarmiert bei neu angeschlossenen USB-Geräten seit dem letzten Scan.

---

## Aufgabe

Implementiere `hwaudit` — ein Hardware-Inventarisierungstool.

### Projektstruktur

```
security-lab/
└── hwaudit/
    ├── __init__.py
    ├── core.py
    ├── cli.py
    └── tests/
        ├── __init__.py
        ├── test_core.py
        └── fixtures/
            ├── lsusb_output.txt
            ├── lsblk_output.json
            └── lsmod_output.txt
```

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `list_usb_devices(lsusb_output: str | None = None) -> list[dict]`
  - Wenn `lsusb_output` None: führt `lsusb` als Subprocess aus
  - Wenn übergeben: parst den String direkt (für Tests)
  - Parst das `lsusb`-Format:
    ```
    Bus 001 Device 003: ID 0951:1666 Kingston Technology DataTraveler 100 G3/G4/SE9 G2
    ```
  - Gibt zurück:
    ```python
    [
        {
            "bus": str,              # "001"
            "device": str,           # "003"
            "vendor_id": str,        # "0951"
            "product_id": str,       # "1666"
            "description": str,      # "Kingston Technology DataTraveler..."
        }
    ]
    ```
  - Bei fehlendem `lsusb`: gibt leere Liste zurück mit Warnung auf stderr

- [ ] Funktion `list_block_devices(lsblk_json: str | None = None) -> list[dict]`
  - Wenn `lsblk_json` None: führt `lsblk --json --output NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,MODEL,VENDOR` aus
  - Parst das JSON-Output von `lsblk` direkt (kein Regex nötig)
  - Gibt flache Liste aller Devices zurück (rekursiv durch `children`):
    ```python
    [
        {
            "name": str,          # "sda"
            "size": str,          # "500G"
            "type": str,          # "disk", "part", "rom"
            "mountpoint": str | None,
            "fstype": str | None, # "ext4", "vfat", etc.
            "model": str | None,
            "vendor": str | None,
        }
    ]
    ```

- [ ] Funktion `list_kernel_modules(lsmod_output: str | None = None) -> list[dict]`
  - Wenn `lsmod_output` None: führt `lsmod` aus
  - Parst `lsmod`-Output:
    ```
    Module                  Size  Used by
    usb_storage            73728  0
    ```
  - Gibt zurück: `[{"name": str, "size": int, "used_by": list[str]}, ...]`

- [ ] Funktion `check_security_relevant_modules(modules: list[dict]) -> list[dict]`
  - Gibt Liste von Security-relevanten Modulen zurück mit Bewertung:
    ```python
    [
        {
            "name": "usb_storage",
            "loaded": bool,
            "risk": "MEDIUM",
            "note": "USB-Massenspeicher aktiv — Datenexfiltration per USB möglich"
        }
    ]
    ```
  - Mindestens diese Module prüfen:
    - `usb_storage`: MEDIUM wenn geladen
    - `nf_conntrack`: INFO wenn geladen (Firewall-Tracking)
    - `bluetooth`: LOW wenn geladen
    - `udf`: LOW wenn geladen (USB-Dateisystem)

- [ ] Funktion `create_hardware_snapshot() -> dict`
  - Kombiniert USB-Geräte, Block-Devices und relevante Module
  - Gibt vollständigen Snapshot-Dict zurück
  - Wird von `BaselineStore` gespeichert

- [ ] Funktion `diff_hardware_snapshots(old: dict, new: dict) -> dict`
  - Nutzt das gleiche Muster wie `diff_baselines` aus Lab 10
  - Vergleicht USB-Geräte nach `vendor_id + product_id`
  - Gibt zurück: neue USB-Geräte, verschwundene USB-Geräte, neue Block-Devices

### cli.py

- [ ] `hwaudit [--format text|json] [--baseline DATEI] [--diff] [--save]`
  - `--diff`: vergleicht mit gespeicherter Baseline
  - `--save`: speichert aktuellen Snapshot als neue Baseline

---

## CLI-Schnittstelle (vollständig)

```
hwaudit                        # einfaches Inventar
hwaudit --save                 # Baseline erstellen/aktualisieren
hwaudit --diff                 # Vergleich mit Baseline
hwaudit --format json
```

Beispiel-Output (Text):
```
HARDWARE INVENTORY
══════════════════════════════════════════

USB-GERÄTE (3)
  Bus 001 Dev 001  ID 1d6b:0002  Linux Foundation 2.0 root hub
  Bus 001 Dev 002  ID 0951:1666  Kingston DataTraveler 100 G3
  Bus 001 Dev 003  ID 04e8:6860  Samsung Electronics Galaxy A50

BLOCK-DEVICES
  NAME        GRÖSSE  TYP    MOUNT       FSTYPE
  mmcblk0     29.1G   disk
  ├─mmcblk0p1  512M   part   /boot/efi   vfat
  └─mmcblk0p2  28.6G  part   /           ext4
  sda          7.5G   disk
  └─sda1       7.5G   part   /media/usb  vfat

KERNEL-MODULE (Security)
  [MED] usb_storage     geladen — USB-Massenspeicher aktiv
  [OK]  nf_conntrack    geladen — Firewall-Tracking (normal)

══════════════════════════════════════════
```

Beispiel `hwaudit --diff`:
```
HARDWARE-DIFF seit 2026-06-19 09:00:00

NEUES USB-GERÄT
  [!] ID 0951:1666  Kingston DataTraveler 100 G3
      Bus 001 · Device 002

KEINE weiteren Änderungen
```

---

## Test-Fixtures

Erstelle `tests/fixtures/lsusb_output.txt`:
```
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 0951:1666 Kingston Technology DataTraveler 100 G3/G4/SE9 G2
```

Erstelle `tests/fixtures/lsblk_output.json`:
```json
{
    "blockdevices": [
        {
            "name": "sda", "size": "7.5G", "type": "disk",
            "mountpoint": null, "fstype": null, "model": "DataTraveler", "vendor": "Kingston",
            "children": [
                {"name": "sda1", "size": "7.5G", "type": "part",
                 "mountpoint": "/media/usb", "fstype": "vfat", "model": null, "vendor": null}
            ]
        }
    ]
}
```

---

## Akzeptanzkriterien

```bash
# USB-Parsing ohne echtes lsusb
python -c "
from hwaudit.core import list_usb_devices
output = 'Bus 001 Device 002: ID 0951:1666 Kingston Technology DataTraveler 100'
devices = list_usb_devices(lsusb_output=output)
assert len(devices) == 1
assert devices[0]['vendor_id'] == '0951'
assert devices[0]['product_id'] == '1666'
print('USB-Parsing OK')
"

# Block-Device-Parsing
python -c "
import json
from hwaudit.core import list_block_devices
sample = json.dumps({'blockdevices': [
    {'name': 'sda', 'size': '7G', 'type': 'disk', 
     'mountpoint': None, 'fstype': None, 'model': None, 'vendor': None,
     'children': [
         {'name': 'sda1', 'size': '7G', 'type': 'part',
          'mountpoint': '/media/usb', 'fstype': 'vfat', 'model': None, 'vendor': None}
     ]}
]})
devices = list_block_devices(lsblk_json=sample)
assert len(devices) == 2  # disk + partition
print('Block-Device-Parsing OK')
"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `list_usb_devices` parst Fixture korrekt (vendor_id, product_id, description)
- [ ] Test: `list_block_devices` parst Fixture korrekt (rekursiv durch children)
- [ ] Test: `list_kernel_modules` parst lsmod-Fixture korrekt
- [ ] Test: `check_security_relevant_modules` flaggt `usb_storage` als MEDIUM
- [ ] Test: `diff_hardware_snapshots` erkennt neues USB-Gerät
- [ ] Test: `diff_hardware_snapshots` erkennt verschwundenes USB-Gerät
- [ ] Test: Subprocess-Fehler (lsusb nicht installiert) → leere Liste, kein Absturz

---

## Bonus-Aufgaben

- [ ] **PCI-Inventar:** `hwaudit --pci` listet PCI-Geräte via `lspci` auf (gleiche Parsing-Logik)
- [ ] **USB-Alarm:** `hwaudit --watch 5` prüft alle 5 Sekunden auf neue USB-Geräte (mit `time.sleep()`, kein Busy-Loop)
- [ ] **Bekannte Geräte-DB:** Lade USB-Vendor/Product-Daten aus `usb.ids`-Datei (öffentlich verfügbar) für leserlichere Namen

---

## Hinweise

**subprocess.run sicher nutzen:**
```python
result = subprocess.run(
    ["lsusb"],
    capture_output=True,
    text=True,
    timeout=10,
)
if result.returncode != 0:
    return []  # Nicht absturzen
```

**lsblk JSON:** `lsblk --json` gibt ein Objekt mit `blockdevices`-Array zurück. Rekursiv `children` traversieren für Partitionen.

**lsusb Regex:** `r"Bus (\d+) Device (\d+): ID ([0-9a-f]{4}):([0-9a-f]{4})\s+(.+)"` — fünf Gruppen.

**uConsole-Realität:** Auf der uConsole gibt es spezifische Hardware (Rockchip RK3566, NIC, 4G-Modem als USB-Device). Teste das Tool explizit dort — das interne 4G-Modem sollte als USB-Device erscheinen.

---

## Schnittstelle für `uctl`

```python
def list_usb_devices(lsusb_output: str | None = None) -> list[dict]:
    """Listet angeschlossene USB-Geräte."""

def create_hardware_snapshot() -> dict:
    """Erstellt vollständigen Hardware-Snapshot."""

def diff_hardware_snapshots(old: dict, new: dict) -> dict:
    """Vergleicht zwei Hardware-Snapshots."""
```
