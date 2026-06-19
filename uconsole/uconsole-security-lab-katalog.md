# uConsole Security & Forensik Lab — Aufgabenkatalog

> Ziel: Schritt für Schritt eigene CLI-Tools für Analyse, Auditierung und Forensik bauen — am Ende vereint in einer einzigen Suite (`uctl`), die auf der uConsole läuft. Kein offensives Automatisieren, kein "Hacking-Framework" — sondern ein Werkzeugkasten, wie ihn ein Security-Analyst, Sysadmin oder Forensiker täglich braucht.

## Lernphilosophie

- **Stdlib first.** Jedes Lab funktioniert idealerweise erstmal nur mit `hashlib`, `socket`, `ssl`, `re`, `argparse`, `json` — keine Abhängigkeit, die du nicht verstehst.
- **Logik von I/O trennen.** Jede Kernfunktion (z. B. `calculate_entropy(data: bytes) -> float`) bekommt eine reine Funktion ohne `print()` oder Dateizugriff. Das macht spätere Tests und die Integration in `uctl` trivial.
- **Jedes Tool ist eigenständig nutzbar.** Erst wenn 5–10 Tools stabil laufen, kommt die Zusammenführung (Phase 6).
- **uConsole-Realität einplanen:** ARM64 (RK3566), kleines Terminal (~50–80 Spalten je nach Schriftgröße), oft offline, begrenzte Batterie → keine Busy-Loops, schlanke Abhängigkeiten, Ausgabe spaltenbreit testen.

---

## Phasenüberblick

| Phase | Thema | Labs | Kernkonzepte |
|---|---|---|---|
| 0 | Fundament | Lab 00 | Projektstruktur, venv, Git, pytest-Grundgerüst |
| 1 | Daten & Dateien | Lab 01–03 | hashlib, Datei-I/O, Bytes/Strings, Statistik |
| 2 | Parsing & Forensik | Lab 04–06 | Regex, Rekursion, Datenmodelle |
| 3 | Krypto & Netzwerk | Lab 07–09 | sockets, ssl, psutil |
| 4 | Integrität & Monitoring | Lab 10–12 | Baselines, Diffing, Config-Parsing |
| 5 | Erweiterte Analyse | Lab 13–15 | Binärformate, externe APIs, Subprocess |
| 6 | Engineering & Integration | Lab 16–17 + Capstone | pytest, Plugin-Architektur, Typer, Packaging |

Geschätzte Gesamtdauer bei 3–5 h/Woche: 4–6 Monate, abhängig von Vorwissen.

---

## Phase 0 — Fundament

### Lab 00: Projekt-Skeleton & Dev-Workflow

**Lernziele:** venv/Poetry-Setup, Projektstruktur, Git-Workflow, erstes pytest.

**Aufgabe:** Lege ein Mono-Repo `security-lab/` an, in dem jedes spätere Tool ein eigenes Unterverzeichnis mit eigenem `main.py`, `core.py` (reine Logik) und `tests/` bekommt:

```
security-lab/
  hashinspect/
    core.py
    cli.py
    tests/test_core.py
  encodingtool/
  ...
  shared/        # später: gemeinsame Utils (Logging, Output-Formatierung)
```

**Anforderungen:**
- `pyproject.toml` mit `pytest`, `black`, `ruff` als Dev-Dependencies
- Ein Makefile oder `justfile` mit `test`, `lint`, `format`
- `.gitignore` für `__pycache__`, `.venv`, `*.egg-info`

**uConsole-Hinweis:** Richte dir gleich ein zweites venv auf der uConsole selbst ein (ARM64-Wheels sind nicht immer verfügbar — teste `pip install` früh dort, nicht erst am Ende).

---

## Phase 1 — Daten & Dateien

### Lab 01: Hash Inspector

**Voraussetzung:** Lab 00.
**Lernziele:** `hashlib`, chunked File-Reading, `argparse`, Fortschrittsanzeige ohne externe Lib.

**Pflicht:**
- SHA256, SHA1, MD5 für eine oder mehrere Dateien berechnen
- Dateien in Blöcken lesen (nicht komplett in den RAM laden — wichtig bei ISO-Dateien auf der uConsole mit wenig RAM)
- Vergleich gegen eine übergebene Hash-Liste (`--check hashes.txt`, Format wie `sha256sum`)
- Exit-Code 0/1 je nach Übereinstimmung (für Skript-Verkettung)

**Bonus:**
- Eigene Fortschrittsanzeige mit `\r` und `sys.stdout.write` (kein `tqdm` — du willst das Prinzip verstehen)
- `--algo` zur Auswahl einzelner Algorithmen, um Zeit zu sparen

**Schnittstelle für später:** `def hash_file(path: Path, algos: list[str]) -> dict[str, str]` — diese Signatur wird später 1:1 ein `uctl hash`-Subcommand.

---

### Lab 02: Base Encoding Toolkit

**Voraussetzung:** Lab 01.
**Lernziele:** Bytes-vs-String-Unterscheidung, `base64`/`base32`-Module, `urllib.parse`.

**Pflicht:**
- `encode`/`decode` für Base64, Base32, Hex, URL-Encoding
- String-Modus (`enc encode "text"`) und Datei-Modus (`enc encode -f file.bin`)
- Sinnvolle Fehlermeldung bei ungültigem Input (z. B. fehlerhaftes Padding)

**Bonus:**
- Auto-Erkennung des Encodings bei `decode` (heuristisch: Zeichensatz prüfen)
- `--chain` um mehrere Encodings hintereinander anzuwenden (z. B. erst Base64 dann Hex)

**Hier zum ersten Mal Tests schreiben:** Da die Logik reine String/Bytes-Transformation ist, ist das ideal für dein erstes `pytest`-Modul mit Parametrisierung (`@pytest.mark.parametrize`).

---

### Lab 03: Entropy Scanner

**Voraussetzung:** Lab 01.
**Lernziele:** Shannon-Entropie, Verzeichnisrekursion mit `pathlib.Path.rglob`, CSV-Export.

**Pflicht:**
- Shannon-Entropie pro Datei berechnen (Byte-Häufigkeiten → `-Σ p·log2(p)`)
- Rekursiver Verzeichnisscan mit Filter (`--ext`, `--min-size`)
- Schwellenwert-Markierung (z. B. > 7.5 Bit/Byte = "verdächtig", typisch für verschlüsselte/komprimierte/gepackte Dateien)
- CSV-Report (`pfad, größe, entropie, flag`)

**Bonus:**
- Histogramm der Byte-Verteilung als ASCII-Balkendiagramm (kein matplotlib — Terminal-Output für die uConsole)

**Forensischer Kontext:** Hohe Entropie alleine ist kein Malware-Beweis (auch Backups, Crypto-Container, Mediendateien sind hoch-entropisch) — im Report immer mit Dateityp/Extension kombinieren, das schult sauberes "Findings vs. Interpretation"-Denken.

---

## Phase 2 — Parsing & Forensik

### Lab 04: Log Forensics Toolkit

**Voraussetzung:** Lab 03.
**Lernziele:** Regex-Gruppen, `datetime`-Parsing, `collections.Counter`.

**Pflicht:**
- IP-Adressen aus `auth.log`/`nginx`-Logs extrahieren (IPv4 + IPv6)
- Fehlgeschlagene SSH-Logins zählen, nach IP gruppiert, sortiert nach Häufigkeit
- Zeitraum-Filter (`--since`, `--until`)
- Zusammenfassung: Top-10-IPs, Login-Erfolgsquote, zeitliche Verteilung (Stunden-Histogramm)

**Bonus:**
- GeoIP-Lookup optional via lokaler MaxMind-DB (offline, kein API-Call nötig)
- `--format json` für maschinenlesbaren Output (wichtig fürs spätere `uctl`)

**Architektur-Hinweis:** Hier zum ersten Mal das Muster „Parser → Datenmodell (dataclass `LogEntry`) → Aggregation → Report" einführen. Dieses Muster ziehst du durch fast alle folgenden Labs.

---

### Lab 05: Metadata Extractor

**Voraussetzung:** Lab 04.
**Lernziele:** `Pillow` (EXIF), `pypdf` (PDF-Metadaten), einheitliche Datenstrukturen über Dateitypen hinweg.

**Pflicht:**
- EXIF-Daten aus JPEG/PNG (Kamera, GPS falls vorhanden, Aufnahmedatum)
- PDF-Metadaten (Autor, Erstellungstool, Änderungsdatum, Seitenzahl)
- Generische Dateieigenschaften (Größe, ctime/mtime, Owner/Permissions via `os.stat`)
- Einheitlicher JSON-Export, unabhängig vom Dateityp

**Bonus:**
- Warnung bei verdächtigen Diskrepanzen (z. B. PDF "erstellt" nach "geändert")
- GPS-Koordinaten aus EXIF in Klartext-Koordinaten umrechnen

**Datenschutz-Hinweis (gut fürs Auditing-Mindset):** Dieses Tool zeigt dir auch, wie viel Metadaten man selbst unabsichtlich weitergibt — guter Use-Case, um es auf eigene Dateien vor dem Teilen anzuwenden.

---

### Lab 06: Secret Detector

**Voraussetzung:** Lab 04, Lab 05.
**Lernziele:** Regex-Pattern-Bibliotheken, rekursive Dateisuche mit Ausschlusslisten, Severity-Modelle.

**Pflicht:**
- Pattern für: generische API-Keys, AWS Access Key IDs (`AKIA[0-9A-Z]{16}`), private Key-Header (`-----BEGIN ... PRIVATE KEY-----`), JWTs, generische `password=`/`secret=`-Zuweisungen
- Rekursive Suche mit `.gitignore`-ähnlichem Exclude-Mechanismus (keine `node_modules`, `.git`, `venv` scannen)
- Severity-Einstufung (High/Medium/Low je Pattern-Typ)
- Markdown-Report mit Datei, Zeile, Pattern-Typ, Kontext-Snippet (Secret selbst maskieren, z. B. nur erste/letzte 4 Zeichen zeigen!)

**Bonus:**
- Entropie-Check (Lab 03) als zweites Signal kombinieren, um False Positives bei generischen `password=`-Mustern zu reduzieren
- `.secretauditignore`-Datei für bekannte False Positives (Hash-basiert, ähnlich `detect-secrets`)

**Wichtig:** Dieses Tool maskiert gefundene Secrets im Report immer — es ist ein Auditing-Tool, kein Exfiltrations-Tool.

---

## Phase 3 — Krypto & Netzwerk

### Lab 07: Certificate Auditor

**Voraussetzung:** Lab 00.
**Lernziele:** `socket`, `ssl`-Modul, X.509-Zertifikatsstruktur, `datetime`-Vergleiche.

**Pflicht:**
- TLS-Verbindung zu Host:Port aufbauen, Zertifikat ohne vollständige Validierung auslesen (`ssl.get_server_certificate` + `cryptography.x509`)
- Issuer, Subject, Gültigkeitszeitraum, SAN-Einträge anzeigen
- Warnung bei < 30 Tagen Restlaufzeit (konfigurierbarer Schwellenwert)
- Zertifikatskette anzeigen (wie viele Zwischenzertifikate)

**Bonus:**
- Batch-Modus: Liste von Hosts aus Datei einlesen, Sammelreport erzeugen
- Schwache Signaturalgorithmen erkennen (z. B. SHA1-signierte Zertifikate flaggen)

**uConsole-Hinweis:** Gutes Tool, um eigene Heimnetz-Zertifikate (Router, NAS, selbst gehostete Dienste) regelmäßig von der uConsole aus zu prüfen, auch offline-fähig wenn man gegen lokale IPs prüft.

---

### Lab 08: Password Strength Analyzer

**Voraussetzung:** Lab 00.
**Lernziele:** Entropie-Berechnung (diesmal auf Zeichenklassen-Basis statt Byte-Ebene), Regex-Zeichenklassen, Wörterbuch-Abgleich.

**Pflicht:**
- Zeichenklassen erkennen (Klein-/Großbuchstaben, Ziffern, Sonderzeichen)
- Entropie in Bit berechnen basierend auf Zeichenraum × Länge
- Abgleich gegen eine lokale Liste häufiger Passwörter (z. B. `rockyou`-Auszug, offline)
- Verständlicher Bericht: "geschätzte Crack-Zeit" bei definierten Angriffsraten (nur Aufklärung, keine echte Crack-Funktion)

**Bonus:**
- Erkennung von Tastatur-Mustern (`qwertz123`, `asdf`)
- Haveibeenpwned-API-Abfrage optional (k-Anonymity-Modus, Passwort wird nie im Klartext übertragen)

**Wichtig:** Reine lokale Bewertung — kein Versand von Klartextpasswörtern, das ist auch ein gutes Lehrbeispiel für privacy-bewusstes Tool-Design.

---

### Lab 09: Local Port Inventory

**Voraussetzung:** Lab 00.
**Lernziele:** `psutil`, Prozess-Socket-Mapping, Filterlogik.

**Pflicht:**
- Listening TCP/UDP-Ports auflisten
- Zugehörige Prozesse (PID, Name, Pfad, User) anzeigen
- Filter nach Protokoll, Port-Range
- JSON-Export

**Bonus:**
- Vergleich gegen eine "erwartete Ports"-Whitelist (`ports.toml`) → Abweichungen flaggen (Brücke zu Lab 10/11)
- IPv6 berücksichtigen

---

## Phase 4 — Integrität & Monitoring

### Lab 10: File Integrity Monitor

**Voraussetzung:** Lab 01, Lab 03.
**Lernziele:** Baseline-/Diff-Muster, JSON-Persistenz, Verzeichnisrekursion mit Metadaten.

**Pflicht:**
- `fim init /etc` erzeugt Baseline (Pfad, Hash, Größe, mtime, Permissions) als JSON
- `fim scan /etc` vergleicht aktuellen Zustand gegen Baseline → neue/gelöschte/geänderte Dateien
- Übersichtlicher Report (Konsole + optional Markdown/JSON)

**Bonus:**
- Inkrementelle Updates der Baseline nach manueller Prüfung ("akzeptiere diese Änderung")
- Ausschlussregeln für volatile Pfade (`/var/log`, `/tmp`)

**Architektur-Hinweis:** Dieses Muster (Baseline → Vergleich → Report) ist die Grundlage für Lab 11 — beide Tools sollten eine gemeinsame `BaselineStore`-Klasse aus `shared/` nutzen können.

---

### Lab 11: Process & Service Baseline Monitor

**Voraussetzung:** Lab 09, Lab 10.
**Lernziele:** Wiederverwendung des Baseline-Patterns, Erkennung verdächtiger Prozess-Eigenschaften.

**Pflicht:**
- Baseline aller laufenden Prozesse (PID, Name, Pfad, Hash der Binary, Startzeit, User)
- Erkennung neuer/unbekannter Prozesse seit letzter Baseline
- Heuristik-Flags: Prozess läuft aus `/tmp` oder gelöschtem Pfad (`(deleted)` in `/proc/PID/exe`), Prozess ohne zugehörige Binary-Datei

**Bonus:**
- Whitelist für bekannte, häufig wechselnde Prozesse (Browser-Tabs etc.)

---

### Lab 12: SSH & Firewall Config Auditor

**Voraussetzung:** Lab 04, Lab 06.
**Lernziele:** Konfigurationsdatei-Parsing ohne fertige Lib, Findings-Modell mit Severity, Best-Practice-Wissen einbauen.

**Pflicht:**
- `sshd_config` parsen: `PermitRootLogin`, `PasswordAuthentication`, `Protocol`, `Ciphers`/`MACs` gegen eine Liste unsicherer Defaults prüfen
- `iptables-save`- oder `nft list ruleset`-Output (aus Datei, offline) parsen: fehlende Default-DROP-Policy, zu offene `ACCEPT`-Regeln (`0.0.0.0/0`) erkennen
- Findings als strukturierte Liste (`dataclass Finding(rule, severity, recommendation)`)
- Markdown-Report, sortiert nach Severity

**Bonus:**
- Eigene Regelwerk-Datei (YAML/TOML), damit Nutzer eigene Checks ergänzen können — erste Vorstufe der späteren Plugin-Idee

---

## Phase 5 — Erweiterte Analyse

### Lab 13: Offline PCAP Analyzer

**Voraussetzung:** Lab 04.
**Lernziele:** Binärformate, `dpkt` oder `scapy` (nur zum *Lesen* gespeicherter Dateien), Protokoll-Statistik.

**Pflicht:**
- `.pcap`-Datei einlesen (offline, keine Live-Capture nötig — Capture-Dateien z. B. mit `tcpdump` selbst auf eigenem Netz erzeugen)
- Top-Talker (IP-Paare nach Traffic-Volumen), Protokollverteilung (TCP/UDP/ICMP/DNS)
- DNS-Queries extrahieren und auflisten
- Erkennung von Klartext-Zugangsdaten in unverschlüsselten Protokollen (z. B. HTTP-Basic-Auth-Header) als Awareness-Feature

**Bonus:**
- Zeitachsen-Diagramm des Traffics als ASCII-Sparkline

**Hinweis:** Reine Nachanalyse aufgezeichneter Dateien — kein Sniffing-Tool. Capture-Dateien erzeugst du dir selbst im eigenen Netz mit `tcpdump -w file.pcap`.

---

### Lab 14: Installed-Package CVE Auditor

**Voraussetzung:** Lab 00.
**Lernziele:** HTTP-APIs (`requests`/`httpx`), Versionsvergleich (`packaging.version`), Caching von API-Antworten.

**Pflicht:**
- Installierte Python-Pakete (`pip list --format=json`) oder Debian-Pakete (`dpkg -l`) einlesen
- Abfrage gegen die OSV.dev-API (offen, kostenlos, kein Key nötig) nach bekannten Schwachstellen
- Report sortiert nach Severity, mit Link zur Advisory

**Bonus:**
- Lokales Caching der Abfragen (JSON-Datei mit TTL), damit Tool auch mit Mobilfunk/wenig Datenvolumen auf der uConsole nutzbar bleibt
- `--offline`-Modus mit zuvor heruntergeladener CVE-Datenbank

---

### Lab 15: USB & Hardware Inventory (uConsole-spezifisch)

**Voraussetzung:** Lab 09.
**Lernziele:** `subprocess`-Wrapping robust gestalten, Parsing strukturierter CLI-Ausgaben (`lsusb`, `lsblk -J`).

**Pflicht:**
- Angeschlossene USB-Geräte auflisten (Vendor/Product-ID, Beschreibung)
- Block-Devices inventarisieren (`lsblk --json` direkt als JSON parsen, kein Regex nötig)
- Geladene, sicherheitsrelevante Kernel-Module prüfen (z. B. ist `usb-storage` deaktiviert?)

**Bonus:**
- Baseline-Vergleich (Lab 10-Pattern wiederverwenden): alarmiert bei neu angeschlossenem USB-Gerät seit letztem Scan — nützlich gerade am mobilen Gerät uConsole

---

## Phase 6 — Engineering & Integration

### Lab 16: Testing & CI für alle Tools

**Voraussetzung:** mind. 5 abgeschlossene Labs.
**Lernziele:** `pytest`-Fixtures, Mocking von Dateisystem/Netzwerk, Coverage.

**Aufgabe:**
- Für jedes Tool: Kernlogik (nicht CLI) vollständig testen, inkl. Edge Cases (leere Datei, riesige Datei, ungültiges Encoding, abgelaufenes Zertifikat als Testfixture)
- `tmp_path`-Fixture für Dateisystem-Tests, `unittest.mock` für Netzwerkzugriffe (Cert-Auditor, CVE-Auditor)
- Coverage-Ziel realistisch ansetzen (z. B. 80 % auf `core.py`-Modulen)
- Optional: GitHub Actions Workflow, der bei jedem Push alle Tests + `ruff` laufen lässt

---

### Lab 17: Plugin-Architektur Prototyp

**Voraussetzung:** Lab 16.
**Lernziele:** `importlib`, abstrakte Basisklassen, `entry_points` in `pyproject.toml`.

**Aufgabe:**
- Definiere ein gemeinsames Interface, z. B.:

```python
class SecurityTool(ABC):
    name: str
    @abstractmethod
    def run(self, args: argparse.Namespace) -> int: ...
    @abstractmethod
    def register_args(self, subparser) -> None: ...
```

- Wandle 2–3 bestehende Tools in Plugins um, die dieses Interface implementieren
- Dynamische Discovery über `importlib.metadata.entry_points(group="uctl.plugins")`

---

## Capstone: `uctl` — Unified Security Toolkit

**Voraussetzung:** Phase 6 abgeschlossen, mind. 8 Einzeltools fertig.

**Ziel-Architektur:**

```
uctl hash file.iso
uctl cert github.com
uctl logs auth.log --since "2026-06-01"
uctl entropy ~/Downloads --format csv
uctl secrets ~/projects
uctl ports --proto tcp
uctl fim scan /etc
uctl pcap capture.pcap
```

**Anforderungen:**
- Typer als CLI-Framework (löst die bisherigen `argparse`-Subcommands ab)
- Zentrale `~/.config/uctl/config.toml` für Defaults (Schwellenwerte, Ausschlusspfade, Output-Format)
- Zentrales Logging (`logging`-Modul, Konsole + Logdatei, Loglevel über `--verbose`/`--quiet`)
- Einheitliches Output-Format über alle Subcommands (Konsole-Tabelle via `rich`, optional `--json` für Skriptverkettung)
- Packaging über `pyproject.toml` + `pipx install .` — funktioniert offline auf der uConsole nach einmaligem Wheel-Cache
- Jedes bisherige Tool wird zum Plugin (Lab 17-Pattern)

**uConsole-Endcheck:**
- Terminal-Breite dynamisch erkennen (`shutil.get_terminal_size()`) statt feste Spaltenbreiten
- Alle Tools laufen ohne Internetzugriff außer Cert-Auditor (Phase 3) und CVE-Auditor (Phase 5) — diese explizit als "online" markieren
- Akku-bewusst: keine Tools mit Dauerschleifen/Polling ohne expliziten `--watch`-Flag

---

## Empfohlene Reihenfolge (Kurzfassung)

00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → Capstone

Du kannst Phase 3 (Krypto & Netzwerk) auch parallel zu Phase 2 angehen, falls dir Netzwerk-Themen mehr Spaß machen als Forensik-Parsing — die einzige harte Abhängigkeit ist, dass Lab 10/11 das Baseline-Pattern aus Lab 01/03 voraussetzen, und Lab 17/Capstone erst nach Lab 16 sinnvoll sind.
