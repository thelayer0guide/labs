# Lab 13 — Offline PCAP Analyzer

> **Phase 5 — Erweiterte Analyse**
> Voraussetzungen: Lab 04 (Parsing-Muster, Datenmodelle)
> Geschätzte Zeit: 5–8 Stunden
> Externe Dependencies: `dpkt` (empfohlen) oder `scapy`

---

## Lernziele

- Binäre Netzwerkaufzeichnungsformate (PCAP) lesen
- Netzwerkprotokoll-Schichtung (Ethernet → IP → TCP/UDP → Payload) verstehen
- Protokoll-Statistiken und Traffic-Analyse implementieren
- DNS-Queries aus Paketen extrahieren
- ASCII-Zeitachsen-Visualisierung bauen

---

## Hintergrund

PCAP-Dateien (Packet Capture) sind Mitschnitte des Netzwerktraffics. Tools wie `tcpdump`, `Wireshark` oder `tshark` erzeugen sie. Sie sind zentrales Werkzeug der Netzwerkforensik: War dieser Host infiziert? Welche DNS-Anfragen wurden gemacht? Gab es Klartextpasswörter im Traffic?

**Wichtig:** Dieses Lab analysiert *gespeicherte* Dateien — kein Live-Sniffing. Du erzeugst Testdateien selbst in deinem eigenen Netz.

---

## Aufgabe

Implementiere `pcapaudit` — einen Offline-Analyzer für PCAP-Dateien.

### Projektstruktur

```
security-lab/
└── pcapaudit/
    ├── __init__.py
    ├── core.py
    ├── cli.py
    └── tests/
        ├── __init__.py
        ├── test_core.py
        └── fixtures/
            └── sample.pcap   (kleiner Test-Capture)
```

---

## Test-PCAP erstellen

Bevor du anfängst, erstelle eine Test-Datei in deinem eigenen Netz:

```bash
# 30 Sekunden Traffic aufzeichnen (nur eigenes Netzwerk-Interface)
sudo tcpdump -i eth0 -w tests/fixtures/sample.pcap -G 30 -W 1

# Oder kleiner: nur DNS-Traffic
sudo tcpdump -i eth0 port 53 -w tests/fixtures/dns-only.pcap -G 10 -W 1
```

Alternativ: Lade eine der freien Sample-PCAP-Dateien von [Wireshark Wiki](https://wiki.wireshark.org/SampleCaptures) — dort gibt es lizenzfreie Testdateien.

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `load_pcap(path: Path) -> list[dict]`
  - Liest PCAP-Datei mit `dpkt.pcap.Reader` (oder `scapy.rdpcap`)
  - Für jedes Paket:
    ```python
    {
        "timestamp": float,        # UNIX-Timestamp
        "length": int,             # Paketlänge in Bytes
        "protocol": str,           # "TCP", "UDP", "ICMP", "ARP", "OTHER"
        "src_ip": str | None,
        "dst_ip": str | None,
        "src_port": int | None,    # nur TCP/UDP
        "dst_port": int | None,
        "payload_len": int,        # Nutzdaten-Länge
    }
    ```
  - Fehlerhafte/nicht parsbare Pakete werden übersprungen
  - Gibt leere Liste für leere PCAP zurück

- [ ] Funktion `get_protocol_stats(packets: list[dict]) -> dict`
  - Zählt Pakete und Bytes pro Protokoll:
    ```python
    {
        "TCP":  {"packets": int, "bytes": int},
        "UDP":  {"packets": int, "bytes": int},
        "ICMP": {"packets": int, "bytes": int},
        "OTHER":{"packets": int, "bytes": int},
        "total_packets": int,
        "total_bytes": int,
    }
    ```

- [ ] Funktion `get_top_talkers(packets: list[dict], n: int = 10) -> list[dict]`
  - Berechnet Traffic-Volumen pro IP-Paar (src→dst):
    ```python
    [
        {"src": "192.168.1.10", "dst": "1.1.1.1", "bytes": 2345678, "packets": 1234},
        ...
    ]
    ```
  - Sortiert nach Bytes absteigend, gibt Top-n zurück

- [ ] Funktion `extract_dns_queries(path: Path) -> list[dict]`
  - Extrahiert DNS-Abfragen aus UDP-Paketen auf Port 53
  - Nutzt direkt `dpkt` für DNS-Parsing
  - Gibt zurück:
    ```python
    [
        {"timestamp": float, "src_ip": str, "query": str, "qtype": str},
        ...
    ]
    ```
  - `qtype`: `"A"`, `"AAAA"`, `"MX"`, `"CNAME"`, `"OTHER"`

- [ ] Funktion `find_cleartext_auth(path: Path) -> list[dict]`
  - Scannt HTTP-Traffic (Port 80) nach Basic-Auth-Headern
  - Pattern: `Authorization: Basic <base64>`
  - Gibt zurück:
    ```python
    [
        {
            "timestamp": float,
            "src_ip": str,
            "dst_ip": str,
            "masked_credentials": str,  # Base64 dekodiert, dann maskiert
        }
    ]
    ```
  - **Credentials werden maskiert** — gleiche Logik wie Lab 06 `mask_secret()`
  - Dies ist ein Awareness-Feature: zeigt dem Nutzer, dass sein Netz unsicher war

- [ ] Funktion `traffic_timeline(packets: list[dict], buckets: int = 60) -> list[dict]`
  - Teilt Zeitraum in `buckets` gleichmäßige Intervalle
  - Gibt Bytes pro Zeitintervall zurück
  - Wird für ASCII-Sparkline verwendet

### cli.py

- [ ] `pcapaudit PCAP_DATEI [--top N] [--format text|json] [--dns-only]`

---

## CLI-Schnittstelle (vollständig)

```
pcapaudit capture.pcap
pcapaudit capture.pcap --top 5
pcapaudit capture.pcap --dns-only
pcapaudit capture.pcap --format json
```

Beispiel-Output (Text):
```
PCAP ANALYSIS: capture.pcap
Zeitraum: 2026-06-19 09:00:00 — 09:05:00 (5 Minuten)
Pakete gesamt: 12.453 | Traffic: 45.3 MB

PROTOKOLL-VERTEILUNG
  TCP      9.234 Pakete  (38.1 MB, 74.2%)
  UDP      2.876 Pakete  ( 6.8 MB, 14.9%)
  ICMP       343 Pakete  ( 0.4 MB,  0.9%)

TOP-TALKER (nach Bytes)
  192.168.1.10  → 1.1.1.1      2.3 MB
  192.168.1.10  → 8.8.8.8      1.1 MB
  192.168.1.5   → 93.184.216.34  0.8 MB

DNS-ABFRAGEN (Top 10)
  github.com          A      42 mal
  google.com          A      31 mal
  *.amazonaws.com     A      28 mal

ZEITACHSE (Pakete/5s)
  ▂▄▆█▆▄▂▁▁▁▂▃▅▇█▆▄▂▁▁▂▄▆█▇▅▃▁

KLARTEXT-AUTHENTIFIZIERUNG
  [!] HTTP-Basic-Auth gefunden:
      09:02:14  192.168.1.5 → 10.0.0.1
      Credentials: adm***...***123 (maskiert)
```

---

## Akzeptanzkriterien

```bash
# Grundfunktion mit Sample-PCAP
python -m pcapaudit tests/fixtures/sample.pcap
# → Keine Exception, mindestens Protokoll-Statistik angezeigt

# JSON-Export
python -m pcapaudit tests/fixtures/sample.pcap --format json | python -m json.tool
# → Valides JSON

# Kern-Logik unit-testbar
python -c "
from pcapaudit.core import get_protocol_stats
test_packets = [
    {'protocol': 'TCP', 'length': 100, 'payload_len': 80, 'timestamp': 0, 
     'src_ip': '192.168.1.1', 'dst_ip': '1.1.1.1', 'src_port': 12345, 'dst_port': 80},
    {'protocol': 'UDP', 'length': 50, 'payload_len': 30, 'timestamp': 1,
     'src_ip': '192.168.1.1', 'dst_ip': '8.8.8.8', 'src_port': 53000, 'dst_port': 53},
    {'protocol': 'TCP', 'length': 200, 'payload_len': 180, 'timestamp': 2,
     'src_ip': '1.1.1.1', 'dst_ip': '192.168.1.1', 'src_port': 80, 'dst_port': 12345},
]
stats = get_protocol_stats(test_packets)
assert stats['TCP']['packets'] == 2
assert stats['UDP']['packets'] == 1
assert stats['total_packets'] == 3
print('Statistiken korrekt')
"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `get_protocol_stats` auf bekannten Testdaten → korrekte Zählung
- [ ] Test: `get_top_talkers` sortiert korrekt nach Bytes
- [ ] Test: `get_top_talkers` mit `n=2` → maximal 2 Einträge
- [ ] Test: `traffic_timeline` mit 10 Paketen gleichmäßig verteilt → 10 Buckets mit je 1 Paket
- [ ] Test: `load_pcap` auf valider Fixture-Datei → nicht-leere Liste
- [ ] Test: `load_pcap` auf leerer PCAP → leere Liste (kein Fehler)
- [ ] Test: `find_cleartext_auth` maskiert Credentials korrekt

---

## ASCII-Sparkline (Bonus-Pflicht für Terminal-Ausgabe)

Implementiere `render_sparkline(values: list[int], width: int = 60) -> str`:
- Normalisiert Werte auf 8 Stufen: `▁▂▃▄▅▆▇█`
- Passt auf die angegebene Terminal-Breite
- Gibt einen String zurück der die Zeitachse darstellt

---

## Bonus-Aufgaben

- [ ] **TLS-Versionsverteilung:** Aus TLS Client-Hello-Paketen (Port 443) extrahiere die angebotene TLS-Version — erkenne TLS 1.0 und 1.1 als veraltet
- [ ] **Port-Scan-Erkennung:** Erkenne wenn eine IP viele verschiedene Ports auf einer anderen IP in kurzer Zeit kontaktiert (potentieller Port-Scan)
- [ ] **IPv6-Support:** Alle Funktionen unterstützen auch IPv6-Traffic

---

## Hinweise

**dpkt vs scapy:** `dpkt` ist leichtgewichtiger und schneller — empfohlen für dieses Lab. `scapy` ist mächtiger aber deutlich langsamer und ressourcenhungriger (auf der uConsole relevant).

**dpkt PCAP lesen:**
```python
import dpkt
with open(path, "rb") as f:
    pcap = dpkt.pcap.Reader(f)
    for timestamp, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            # weiterverarbeiten...
        except:
            continue
```

**DNS mit dpkt:**
```python
udp = ip.data   # wenn ip.p == 17 (UDP)
dns = dpkt.dns.DNS(udp.data)
for q in dns.qd:
    print(q.name)
```

**uConsole-Hinweis:** Capture-Dateien erzeuge immer nur im eigenen Netz (`-i` auf das eigene Interface). Niemals in fremden Netzen aufzeichnen.

---

## Schnittstelle für `uctl`

```python
def load_pcap(path: Path) -> list[dict]:
    """Liest PCAP-Datei und gibt strukturierte Paketliste zurück."""

def get_protocol_stats(packets: list[dict]) -> dict:
    """Berechnet Protokoll-Statistiken."""

def get_top_talkers(packets: list[dict], n: int = 10) -> list[dict]:
    """Gibt Top-N IP-Paare nach Traffic-Volumen zurück."""
```
