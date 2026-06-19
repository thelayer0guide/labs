# Lab 01 — Hash Inspector

> **Phase 1 — Daten & Dateien**
> Voraussetzungen: Lab 00
> Geschätzte Zeit: 4–6 Stunden

---

## Lernziele

- `hashlib` für kryptografische Hash-Funktionen einsetzen
- Dateien chunk-weise lesen statt vollständig in den RAM zu laden
- `argparse` für eine vollwertige CLI mit Subcommands nutzen
- Exit-Codes sinnvoll für Skript-Verkettung einsetzen
- Eine eigene Fortschrittsanzeige ohne externe Bibliotheken bauen
- Die Trennung von Kernlogik (`core.py`) und I/O (`cli.py`) konsequent umsetzen

---

## Hintergrund

Hash-Werte sind das Fundament der Dateiintegrität: Wenn du eine ISO herunterlädst, ein Backup überprüfst oder Forensik betreibst, vergleichst du Hash-Werte. Tools wie `sha256sum` machen genau das — du baust jetzt eine erweiterte Version, die mehrere Algorithmen gleichzeitig berechnet und gegen Prüfsummenlisten vergleicht.

Der entscheidende Lernaspekt hier ist nicht die Hash-Berechnung selbst (die `hashlib` übernimmt), sondern das korrekte chunk-weise Lesen: Eine 4 GB ISO-Datei darf nicht komplett in den Arbeitsspeicher geladen werden — auf der uConsole mit begrenztem RAM wäre das fatal.

---

## Aufgabe

Implementiere `hashinspect` — ein CLI-Tool, das Dateien hasht, mehrere Algorithmen parallel unterstützt und Prüfsummenlisten abgleicht.

### Projektstruktur

```
security-lab/
└── hashinspect/
    ├── __init__.py
    ├── core.py      ← reine Hash-Logik, kein print(), kein sys.exit()
    ├── cli.py       ← argparse, Ausgabe, Exit-Code
    └── tests/
        ├── __init__.py
        └── test_core.py
```

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `hash_file(path: Path, algos: list[str]) -> dict[str, str]`
  - Liest die Datei in Blöcken von **maximal 64 KB** (kein `f.read()` ohne Größenangabe)
  - Gibt ein Dict zurück, z. B. `{"sha256": "a4f2...", "md5": "c3b1..."}`
  - Unterstützt mindestens: `sha256`, `sha1`, `md5`
  - Wirft `ValueError` bei unbekanntem Algorithmus-Namen
  - Wirft `FileNotFoundError` wenn die Datei nicht existiert (nicht selbst fangen — durchlassen)

- [ ] Funktion `parse_checksum_file(path: Path) -> dict[str, str]`
  - Parst das Format von `sha256sum`-Output: `<hash>  <dateiname>` (zwei Leerzeichen)
  - Gibt ein Dict zurück: `{dateiname: hash}`
  - Ignoriert Kommentarzeilen (beginnen mit `#`)
  - Wirft `ValueError` bei Zeilen mit falschem Format

- [ ] Funktion `verify_hashes(computed: dict[str, str], expected: dict[str, str]) -> dict[str, bool]`
  - Vergleicht berechnete gegen erwartete Hashes (case-insensitive)
  - Gibt zurück, welche Dateien übereinstimmen und welche nicht

### cli.py

- [ ] Subcommand `hash`: berechnet Hash(es) für eine oder mehrere Dateien
  - `hashinspect hash datei1.iso datei2.tar.gz`
  - `--algo sha256` (Standard: sha256; mehrere mit Komma: `sha256,md5`)
  - Ausgabe: `SHA256  a4f2...  datei1.iso`
- [ ] Subcommand `check`: vergleicht gegen eine Prüfsummenliste
  - `hashinspect check hashes.txt`
  - Ausgabe pro Datei: `✓ datei.iso` oder `✗ datei.iso (erwartet: a4f2... gefunden: b3e1...)`
  - Exit-Code **0** wenn alle Hashes stimmen, **1** wenn mindestens einer abweicht
- [ ] Fortschrittsanzeige beim Hashing:
  - Nutzt `\r` und `sys.stdout.write` — **kein `tqdm`**
  - Zeigt: verarbeitete Bytes und Prozentsatz, aktualisiert pro Chunk
  - Wird nach Abschluss durch die Ergebniszeile überschrieben

---

## CLI-Schnittstelle (vollständig)

```
hashinspect hash [--algo ALGO] DATEI [DATEI ...]
hashinspect check [--algo ALGO] CHECKSUMMEN_DATEI
hashinspect hash --help
```

Beispiel-Output `hash`:
```
SHA256  a4f2c8d1e9b3f7a2...  kali-linux-2026.iso   (3.8 GB · 4.2s)
MD5     c3b1a9e8d7f2b4c1...  kali-linux-2026.iso
```

Beispiel-Output `check`:
```
✓  kali-linux-2026.iso     SHA256  match
✗  ubuntu-24.iso           SHA256  mismatch
   erwartet: a4f2c8d1...
   gefunden: deadbeef...

Ergebnis: 1/2 Dateien OK
```

---

## Akzeptanzkriterien

```bash
# Erstellt eine Testdatei und prüft den Hash
python -c "open('test.bin','wb').write(b'hello'*1000)"
python -m hashinspect hash test.bin --algo sha256
# → muss SHA256 + Hex-String ausgeben

# Verzeichnet den Hash und prüft ihn
python -m hashinspect hash test.bin --algo sha256 | \
  awk '{print $2"  test.bin"}' > hashes.txt
python -m hashinspect check hashes.txt
echo $?    # → 0

# Verfälsche den Hash und teste Exit-Code
echo "deadbeef  test.bin" > bad.txt
python -m hashinspect check bad.txt
echo $?    # → 1

# Unbekannter Algorithmus
python -m hashinspect hash test.bin --algo xxhash
# → Fehlermeldung auf stderr, Exit-Code != 0
```

Die Kernfunktion muss in Tests ohne CLI nutzbar sein:
```python
from hashinspect.core import hash_file
result = hash_file(Path("test.bin"), ["sha256", "md5"])
assert "sha256" in result
assert len(result["sha256"]) == 64
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `hash_file` auf einer kleinen bekannten Datei → Ergebnis stimmt mit `sha256sum` überein
- [ ] Test: `hash_file` mit ungültigem Algorithmus → `ValueError`
- [ ] Test: `hash_file` auf nicht existierender Datei → `FileNotFoundError`
- [ ] Test: `parse_checksum_file` parst valides Format korrekt
- [ ] Test: `parse_checksum_file` ignoriert Kommentarzeilen
- [ ] Test: `verify_hashes` — case-insensitive Vergleich funktioniert
- [ ] Test: Chunk-Verhalten — erstelle eine künstliche Datei, die größer als ein Chunk ist, prüfe dass Hash korrekt ist

Nutze `pytest`'s `tmp_path`-Fixture für alle dateibasierten Tests.

---

## Bonus-Aufgaben

- [ ] `--algo sha256,md5,sha1` — alle drei Algorithmen in einem Durchlauf, Datei nur einmal lesen
- [ ] Mehrere Dateien parallel verarbeiten mit `concurrent.futures.ThreadPoolExecutor`
- [ ] `--quiet` Flag: keine Fortschrittsanzeige, nur Ergebnis
- [ ] Formatierter Output: Hashes in Tabelle ausrichten (kürzeste Spaltenbreite berechnen)
- [ ] Verifikation gegen eine URL (HEAD-Request, `Content-MD5` Header) — optional, erfordert `requests`

---

## Hinweise

**Chunk-Lesen:** `hashlib`-Objekte unterstützen inkrementelles Update via `.update(data)`. Erzeuge das Hash-Objekt einmal, rufe dann `.update()` für jeden Chunk auf, und erst am Ende `.hexdigest()`.

**Mehrere Algorithmen gleichzeitig:** Statt die Datei für jeden Algorithmus erneut zu lesen, kannst du ein Dict `{algo: hashlib.new(algo)}` anlegen und in einer Schleife alle Objekte gleichzeitig updaten.

**Fortschrittsanzeige:** `os.path.getsize(path)` gibt dir die Dateigröße vorab. Mit `bytes_read / total_size * 100` berechnest du den Fortschritt. `sys.stdout.write(f"\r{progress:.1f}%")` und `sys.stdout.flush()` — am Ende `sys.stdout.write("\n")`.

**Exit-Codes:** Setze den Exit-Code mit `sys.exit(0)` oder `sys.exit(1)` — nie mit einer Exception.

---

## Schnittstelle für `uctl`

Diese Funktion wird später 1:1 als `uctl hash`-Subcommand verwendet:

```python
def hash_file(path: Path, algos: list[str]) -> dict[str, str]:
    """Berechnet kryptografische Hashes für eine Datei.
    
    Args:
        path: Pfad zur Datei
        algos: Liste der Algorithmen, z. B. ["sha256", "md5"]
    
    Returns:
        Dict {algorithmus: hex_digest}
    
    Raises:
        ValueError: Bei unbekanntem Algorithmus
        FileNotFoundError: Wenn die Datei nicht existiert
    """
```

Halte diese Signatur genau so — Änderungen würden spätere Integration erschweren.
