# Lab 03 — Entropy Scanner

> **Phase 1 — Daten & Dateien**
> Voraussetzungen: Lab 01 (Projektstruktur, chunk-weises Lesen)
> Geschätzte Zeit: 4–6 Stunden

---

## Lernziele

- Shannon-Entropie mathematisch verstehen und implementieren
- Verzeichnisrekursion mit `pathlib.Path.rglob()` und Filterlogik
- CSV-Export mit der `csv`-Stdlib strukturieren
- ASCII-Visualisierungen für das Terminal bauen (kein matplotlib)
- Den Unterschied zwischen "Finding" und "Interpretation" in der Forensik verstehen

---

## Hintergrund

Die Shannon-Entropie misst, wie zufällig oder komprimiert Daten sind. Hoch-entropische Dateien (nahe 8 Bit/Byte) können verschlüsselt, komprimiert oder gepackt sein — oder eben auch Mediendateien, Backups, oder Kryptographie-Container.

Ein Entropy Scanner ist ein nützliches Forensik-Werkzeug: Er hilft, "verdächtige" Dateien in einem Verzeichnisbaum zu identifizieren, die dann manuell untersucht werden. Das Tool flaggt — es urteilt nicht. Diese Unterscheidung (Finding vs. Interpretation) ist zentral für jede forensische Arbeit.

---

## Aufgabe

Implementiere `entropy` — einen rekursiven Verzeichnis-Scanner, der die Shannon-Entropie jeder Datei berechnet und Ergebnisse als CSV oder Terminal-Report ausgibt.

### Projektstruktur

```
security-lab/
└── entropyscanner/
    ├── __init__.py
    ├── core.py
    ├── cli.py
    └── tests/
        ├── __init__.py
        └── test_core.py
```

---

## Die Mathematik

**Shannon-Entropie** für eine Datei:

```
H = -Σ p_i · log2(p_i)
```

wobei `p_i` die relative Häufigkeit von Byte-Wert `i` (0–255) in der Datei ist.

- Maximum: **8 Bit/Byte** (jedes der 256 Byte-Werte tritt gleich oft auf — maximale Zufälligkeit)
- Minimum: **0 Bit/Byte** (alle Bytes haben den gleichen Wert — keine Information)

Typische Richtwerte:
- Englischer Text: ~3.5–5 Bit/Byte
- Komprimierte/verschlüsselte Daten: ~7.5–8 Bit/Byte
- Executable-Binaries: ~5.5–7 Bit/Byte

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `calculate_entropy(data: bytes) -> float`
  - Berechnet die Shannon-Entropie für gegebene Bytes
  - Gibt einen Wert zwischen 0.0 und 8.0 zurück
  - `data = b""` → gibt `0.0` zurück (Sonderfall)
  - Nutzt `math.log2()` aus der Stdlib
  - Kein `print()`, kein Dateizugriff

- [ ] Funktion `scan_file(path: Path) -> dict`
  - Liest die Datei chunk-weise (max. 64 KB pro Chunk — nutze Muster aus Lab 01)
  - Gibt zurück: `{"path": str, "size": int, "entropy": float, "extension": str}`
  - Bei Lesefehler (Permissions): gibt `{"path": str, "error": str}` zurück — wirft keine Exception

- [ ] Funktion `scan_directory(root: Path, min_size: int, extensions: list[str] | None) -> list[dict]`
  - Durchsucht `root` rekursiv mit `rglob("*")`
  - Überspringt Verzeichnisse und Symlinks
  - Filtert nach Minimalgröße in Bytes (`min_size`, Standard: 0)
  - Filtert nach Extensions wenn `extensions` angegeben (z. B. `[".py", ".js"]`)
  - Gibt Liste der Scan-Ergebnisse zurück (kein `print()`)

- [ ] Funktion `flag_results(results: list[dict], threshold: float) -> list[dict]`
  - Fügt jedem Ergebnis `"flagged": True/False` hinzu
  - Geflaggt wenn `entropy >= threshold`
  - Gibt neue Liste zurück (mutiert die Eingabe nicht)

- [ ] Funktion `export_csv(results: list[dict], output: Path) -> None`
  - Schreibt CSV mit Spalten: `pfad,größe,entropie,flag,erweiterung`
  - Nutzt `csv.DictWriter` aus der Stdlib

### cli.py

- [ ] `entropy PFAD [--threshold 7.5] [--ext .py,.js] [--min-size 1024] [--format csv|text] [--out DATEI]`
  - Standard: Terminal-Output (Textformat)
  - `--format csv --out report.csv`: schreibt CSV-Datei
  - Zeigt Zusammenfassung am Ende: Anzahl gescannter Dateien, Anzahl geflaggt

---

## CLI-Schnittstelle (vollständig)

```
entropy ~/Downloads
entropy ~/Downloads --threshold 7.5
entropy /etc --ext "" --min-size 0
entropy ~/projects --ext .py,.js,.ts --format csv --out entropy-report.csv
```

Beispiel-Output (Terminal):
```
ENTROPY SCAN: /home/user/Downloads
─────────────────────────────────────────────────────
SUSPECT  7.94  payload.bin          (2.3 MB)
SUSPECT  7.89  archive.tar.gz       (45 MB)
OK       3.21  readme.txt           (4.2 KB)
OK       5.67  app.exe              (1.1 MB)
─────────────────────────────────────────────────────
Gescannt: 4 Dateien · Geflaggt: 2 · Schwellenwert: 7.50
```

---

## Akzeptanzkriterien

```bash
# Mathematische Korrektheit
python -c "
from entropyscanner.core import calculate_entropy
# Alle gleichen Bytes → Entropie 0
assert calculate_entropy(b'\x00' * 1000) == 0.0

# Alle 256 Werte gleichmäßig → maximale Entropie
data = bytes(range(256)) * 4
h = calculate_entropy(data)
assert 7.9 < h <= 8.0, f'Erwartet ~8.0, bekam {h}'

# Leere Eingabe
assert calculate_entropy(b'') == 0.0

print('Entropie-Berechnungen korrekt')
"

# Verzeichnis-Scan
python -m entropyscanner ~/Downloads --threshold 7.5
# → muss ohne Absturz durchlaufen, auch wenn keine Dateien gefunden

# CSV-Export
python -m entropyscanner /tmp --format csv --out /tmp/test.csv
python -c "import csv; rows = list(csv.DictReader(open('/tmp/test.csv'))); print(f'{len(rows)} Zeilen')"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `calculate_entropy(b"\x00" * 1000)` == 0.0
- [ ] Test: `calculate_entropy(bytes(range(256)) * 10)` liegt zwischen 7.99 und 8.0
- [ ] Test: `calculate_entropy(b"")` == 0.0
- [ ] Test: Englischer Text hat Entropie zwischen 3.0 und 6.0
- [ ] Test: `scan_file` auf einer bekannten Datei gibt korrektes Dict zurück
- [ ] Test: `scan_file` auf nicht lesbarer Datei gibt `{"error": ...}` zurück statt Exception
- [ ] Test: `flag_results` markiert korrekt mit `flagged: True/False`
- [ ] Test: `scan_directory` mit Extension-Filter gibt nur passende Dateien zurück
- [ ] Test: `export_csv` erstellt valide CSV-Datei (mit `tmp_path`-Fixture)

---

## Bonus-Aufgaben

- [ ] **ASCII-Histogramm:** `--histogram`-Flag zeigt Byte-Verteilung einer einzelnen Datei als Balkendiagramm im Terminal
  ```
  00-0F: ████░░░░░░ 12%
  10-1F: ██░░░░░░░░  4%
  ...
  ```
  Breite passt sich an `shutil.get_terminal_size()` an.

- [ ] **Extension-Kombination:** Report gruppiert nach Extension, zeigt Durchschnitts-Entropie pro Typ
- [ ] **Größen-normierte Analyse:** Option `--per-chunk` — Entropie pro 4KB-Chunk statt über die gesamte Datei (findet "lokale" Anomalien)

---

## Hinweise

**Byte-Häufigkeiten:** `collections.Counter(data)` zählt Byte-Vorkommen. Für alle 256 möglichen Werte: `Counter(data).get(i, 0)` für jeden Wert 0–255.

**Logarithmus:** `math.log2(0)` ist mathematisch undefiniert — überspringe Bytes mit Häufigkeit 0 in der Summe.

**Performance:** Für große Verzeichnisse ist chunk-weises Lesen wichtig. `calculate_entropy(data)` kann auf den gesammelten Bytes nach dem Lesen aufgerufen werden — du musst nicht den Algorithmus selbst inkrementell machen, da die Byte-Häufigkeiten am Ende berechnet werden.

**uConsole-Tipp:** Scanne niemals `/proc` oder `/sys` — diese Pseudo-Dateisysteme können hängen bleiben. Füge Ausschlusslogik für diese Pfade hinzu.

---

## Forensischer Kontext (wichtig)

Stelle in deinem Report immer klar, dass:
- Hohe Entropie ≠ Malware
- `.tar.gz`, `.jpg`, `.mp4`, `.zip` sind naturgemäß hoch-entropisch
- Das Tool filtert — es urteilt nicht

Implementiere diese Warnung in der Tool-Ausgabe (z. B. als Fußnote im Report).

---

## Schnittstelle für `uctl`

```python
def calculate_entropy(data: bytes) -> float:
    """Berechnet Shannon-Entropie in Bit/Byte (0.0–8.0)."""

def scan_file(path: Path) -> dict:
    """Scannt eine einzelne Datei auf Entropie."""

def scan_directory(root: Path, min_size: int = 0, extensions: list[str] | None = None) -> list[dict]:
    """Scannt ein Verzeichnis rekursiv."""
```
