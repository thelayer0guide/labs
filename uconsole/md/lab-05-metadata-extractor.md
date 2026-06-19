# Lab 05 — Metadata Extractor

> **Phase 2 — Parsing & Forensik**
> Voraussetzungen: Lab 04 (Datenmodell-Muster)
> Geschätzte Zeit: 4–6 Stunden
> Externe Dependencies: `Pillow`, `pypdf`

---

## Lernziele

- Externe Bibliotheken (`Pillow`, `pypdf`) gezielt für Metadaten-Extraktion einsetzen
- Einheitliche Datenstrukturen über verschiedene Dateitypen hinweg bauen
- GPS-Koordinaten aus EXIF-Rohdaten in Dezimalgrad umrechnen
- `os.stat()` und `pathlib.Path.stat()` für Dateisystem-Metadaten nutzen
- Datenschutz-Implikationen von Metadaten praktisch verstehen

---

## Hintergrund

Dateien tragen oft mehr Informationen als der reine Inhalt: Fotos enthalten GPS-Koordinaten, Kameramodell und Aufnahmedatum. PDFs verraten das Autorenkürzel, das Office-Programm und manchmal interne Firmennamen. Selbst generische Dateieigenschaften wie `ctime`/`mtime` können forensisch relevant sein.

Dieses Tool ist dual-use: Als Forensik-Werkzeug analysierst du fremde Dateien. Als Datenschutz-Tool prüfst du deine eigenen Dateien, bevor du sie teilst. Beide Anwendungsfälle sind legitim und lehrreich.

---

## Aufgabe

Implementiere `meta` — ein Tool, das Metadaten aus verschiedenen Dateitypen extrahiert und in einem einheitlichen JSON-Format ausgibt.

### Projektstruktur

```
security-lab/
└── metaextract/
    ├── __init__.py
    ├── core.py
    ├── extractors/
    │   ├── __init__.py
    │   ├── image.py      ← EXIF-Extraktion (Pillow)
    │   ├── pdf.py        ← PDF-Metadaten (pypdf)
    │   └── generic.py    ← os.stat() für alle Dateitypen
    ├── cli.py
    └── tests/
        ├── __init__.py
        ├── test_core.py
        └── fixtures/
            ├── sample.jpg    (kleines Testbild mit EXIF)
            └── sample.pdf    (kleines Test-PDF)
```

---

## Das Datenmodell

Alle Extraktoren geben ein Dict mit folgendem Schema zurück:

```python
{
    "path": str,
    "type": str,          # "jpeg", "png", "pdf", "unknown"
    "size_bytes": int,
    "modified": str,      # ISO 8601
    "created": str,       # ISO 8601 (ctime — nicht immer Erstellzeit!)
    "permissions": str,   # oktales Format: "644"
    "owner": str,         # UID oder Username
    
    # EXIF (nur für Bilder, falls vorhanden):
    "exif": {
        "camera_make": str | None,
        "camera_model": str | None,
        "datetime_original": str | None,   # ISO 8601
        "gps_lat": float | None,           # Dezimalgrad, N positiv
        "gps_lon": float | None,           # Dezimalgrad, E positiv
        "software": str | None,
        "orientation": int | None,
    } | None,
    
    # PDF (nur für PDFs, falls vorhanden):
    "pdf": {
        "author": str | None,
        "creator": str | None,           # z. B. "Microsoft Word"
        "producer": str | None,          # z. B. "Acrobat PDF 15.0"
        "creation_date": str | None,     # ISO 8601
        "modification_date": str | None, # ISO 8601
        "page_count": int,
        "encrypted": bool,
    } | None,
    
    # Anomalien (immer vorhanden, leer wenn keine):
    "anomalies": list[str],
}
```

---

## Anforderungen (Pflicht)

### extractors/generic.py

- [ ] Funktion `extract_generic(path: Path) -> dict`
  - Füllt alle Felder aus dem Schema (ohne EXIF und PDF)
  - `permissions` als oktaler String (z. B. `"644"`)
  - Timestamps als ISO-8601-Strings
  - Bei fehlenden Rechten: gibt `{"path": str, "error": "permission denied"}` zurück

### extractors/image.py

- [ ] Funktion `extract_exif(path: Path) -> dict | None`
  - Nutzt `PIL.Image.open()` und `._getexif()`
  - Gibt das EXIF-Teildict zurück oder `None` wenn keine EXIF-Daten vorhanden
  - Importiert `PIL` in einem Try/Except: wenn nicht installiert → gibt `None` zurück
  - GPS-Koordinaten: EXIF speichert diese als Grad/Minuten/Sekunden-Tupel → umrechnen in Dezimalgrad

- [ ] Funktion `gps_to_decimal(degrees, minutes, seconds, ref: str) -> float`
  - Reine Berechnung, kein I/O
  - `ref` ist `"N"`, `"S"`, `"E"` oder `"W"` — South und West sind negativ

### extractors/pdf.py

- [ ] Funktion `extract_pdf_meta(path: Path) -> dict | None`
  - Nutzt `pypdf.PdfReader`
  - Gibt das PDF-Teildict zurück oder `None` bei Fehler
  - Bei verschlüsseltem PDF: `encrypted: True`, restliche Felder `None`

### core.py

- [ ] Funktion `extract_metadata(path: Path) -> dict`
  - Kombiniert alle Extraktoren zum vollständigen Schema
  - Erkennt Dateityp via `path.suffix.lower()` und Magic Bytes (erste 4 Bytes)
  - Füllt `anomalies`-Liste:
    - PDF: "modification_date before creation_date" wenn Änderungsdatum vor Erstelldatum
    - Bild: "GPS coordinates present" als Hinweis (nicht als Fehler)
    - Allgemein: "ctime in future" wenn `ctime` in der Zukunft liegt

### cli.py

- [ ] `meta DATEI [DATEI ...] [--format json|text]`
- [ ] `meta VERZEICHNIS --recursive [--ext jpg,pdf]`

---

## CLI-Schnittstelle (vollständig)

```
meta foto.jpg
meta dokument.pdf --format json
meta ~/Dokumente --recursive --ext pdf
meta foto1.jpg foto2.jpg foto3.jpg
```

Beispiel-Output (Text):
```
METADATA: foto.jpg
─────────────────────────────
Typ         JPEG
Größe       3.2 MB
Geändert    2026-05-15T14:32:01
Rechte      644

KAMERA
  Hersteller  Apple
  Modell      iPhone 15 Pro
  Aufnahme    2026-05-15T12:00:00

GPS
  Koordinaten  48.1351° N, 11.5820° E
  [!] Tipp: GPS-Koordinaten in Datei vorhanden — vor dem Teilen prüfen!

ANOMALIEN
  (keine)
```

---

## Akzeptanzkriterien

```bash
# Erstelle ein minimales Test-JPEG (ohne EXIF)
python -c "
from PIL import Image
img = Image.new('RGB', (100, 100), color='red')
img.save('/tmp/test_noexif.jpg')
"
python -m metaextract /tmp/test_noexif.jpg --format json
# → valides JSON, exif: null

# GPS-Umrechnung
python -c "
from metaextract.extractors.image import gps_to_decimal
lat = gps_to_decimal(48, 8, 3.6, 'N')
assert abs(lat - 48.134333) < 0.001, f'Erwartet ~48.134, bekam {lat}'
lat_s = gps_to_decimal(48, 8, 3.6, 'S')
assert lat_s < 0, 'Südlich muss negativ sein'
print('GPS-Umrechnung OK')
"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `extract_generic` gibt vollständiges Dict mit allen Pflichtfeldern zurück
- [ ] Test: `gps_to_decimal(48, 8, 3.6, "N")` → ~48.134
- [ ] Test: `gps_to_decimal(48, 8, 3.6, "S")` → negativ
- [ ] Test: `gps_to_decimal(11, 34, 55.2, "E")` → positiv
- [ ] Test: `gps_to_decimal(11, 34, 55.2, "W")` → negativ
- [ ] Test: `extract_pdf_meta` auf Sample-PDF gibt `page_count >= 1` zurück
- [ ] Test: `extract_metadata` erkennt JPEG korrekt (`type == "jpeg"`)
- [ ] Test: `extract_metadata` auf nicht existierender Datei → enthält `"error"`-Feld

Erstelle in `tests/fixtures/` ein minimales Test-PDF mit `pypdf`-Skript (oder Download eines freien 1-seitigen PDFs).

---

## Bonus-Aufgaben

- [ ] **Magic Bytes:** Erkenne Dateityp nicht nur via Extension, sondern via erste Bytes (`\xff\xd8\xff` = JPEG, `%PDF` = PDF, `\x89PNG` = PNG)
- [ ] **Batch-Report:** `--format csv` für mehrere Dateien (eine Zeile pro Datei)
- [ ] **Metadata-Stripping-Hinweis:** Zeige bei Dateien mit GPS-Daten konkret an, wie man Metadaten entfernt (`exiftool -all= datei.jpg`)

---

## Hinweise

**Pillow EXIF:** `Image.open(path)._getexif()` gibt ein Dict mit numerischen Tag-IDs zurück. Nutze `PIL.ExifTags.TAGS` zum Umwandeln in lesbare Namen: `TAGS.get(tag_id, str(tag_id))`.

**GPS-Daten in EXIF:** GPS-Info steckt unter Tag-ID `34853` (GPSInfo). Die Werte für Breitengrad sind unter GPSLatitude (2) und GPSLatitudeRef (1). Die Rohdaten sind `IFDRational`-Objekte — rechne mit `float(val)`.

**ctime auf Linux:** `ctime` ist die Zeit der letzten Inode-Änderung, **nicht** die Erstellzeit. Benenne es entsprechend im Output oder erkläre es in einem Kommentar.

**pypdf:** `PdfReader(path).metadata` gibt ein `DocumentInformation`-Objekt zurück. Zugriff via Attribut: `.author`, `.creation_date`. Datumswerte sind manchmal `datetime`-Objekte, manchmal Strings — normalisiere zu ISO 8601.

---

## Datenschutz-Hinweis (wichtiger Teil der Aufgabe)

Implementiere einen expliziten Warnhinweis in der Ausgabe, wenn GPS-Koordinaten gefunden werden:

```
[!] DATENSCHUTZ: Diese Datei enthält GPS-Koordinaten (48.1351° N, 11.5820° E).
    Wenn du diese Datei teilst, teilst du auch deinen Standort.
    Zum Entfernen: exiftool -GPS:all= datei.jpg
```

Dieser Hinweis soll Nutzer schulen, nicht erschrecken.

---

## Schnittstelle für `uctl`

```python
def extract_metadata(path: Path) -> dict:
    """Extrahiert alle verfügbaren Metadaten einer Datei.
    
    Returns:
        Vollständiges Metadaten-Dict nach definiertem Schema.
        Enthält "error"-Feld bei nicht lesbaren Dateien.
    """
```
