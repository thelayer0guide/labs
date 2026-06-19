# Modul 03 — Funktionen & Wiederverwendbarkeit

[← Modul 02](modul-02.md) | [Übersicht](catalog.md) | [Modul 04 →](modul-04.md)

---

**Phase:** Phase A — Grundlagen
**Zeitaufwand:** 3–4 h
**Schwierigkeit:** ★★☆☆☆ Grundkenntnisse
**Voraussetzungen:** Modul 02

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)

---

## Lernziele

- Funktionen mit `def` definieren und aufrufen
- Pflicht-, Default- und Keyword-Argumente unterscheiden und kombinieren
- Type Hints für Parameter und Rückgabewerte schreiben (`str`, `int`, `list[str]`)
- Mehrere Rückgabewerte via Tuple-Unpacking nutzen
- Docstrings sinnvoll — aber knapp — einsetzen
- Code-Duplikate durch Funktionen eliminieren

---

## Hintergrund

Funktionen sind das wichtigste Strukturierungsmittel in Python. Eine Funktion sollte genau eine Sache tun, die ihr Name beschreibt. Die Grenze: wenn du eine Funktion nicht in einem Satz erklären kannst, ist sie zu groß.

Type Hints (eingeführt in Python 3.5, vollständig seit 3.9) werden zur Laufzeit nicht erzwungen — sie sind Dokumentation für den Leser und das IDE. `mypy` kann sie statisch prüfen. In Admin-Skripten genügt oft `str`, `int`, `Path`, `list[str]`.

---

## Schlüsselkonzepte

### Funktionssignatur mit Type Hints

```python
def scan_directory(path: str, extension: str = ".log") -> list[str]:
    """Gibt alle Dateien mit gegebener Endung zurück."""
    from pathlib import Path
    return [str(f) for f in Path(path).rglob(f"*{extension}")]
```

### Mehrere Rückgabewerte

```python
def file_stats(path: str) -> tuple[int, int, int]:
    """Gibt (Zeilen, Wörter, Bytes) zurück."""
    text = open(path).read()
    return len(text.splitlines()), len(text.split()), len(text.encode())

lines, words, size = file_stats("server.log")
```

### Keyword-Only Args

```python
def backup(source: str, dest: str, *, dry_run: bool = False) -> None:
    if dry_run:
        print(f"[DRY] {source} → {dest}")
        return
    # ... echtes Backup

backup("/data", "/backup", dry_run=True)
```

---

## Aufgabe

Schreibe `file_report.py`: ein Skript, das ein Verzeichnis analysiert und einen Bericht ausgibt.

Das Skript soll folgende Funktionen enthalten:

- `count_files_by_extension(path: str) -> dict[str, int]`
- `total_size_bytes(path: str) -> int`
- `find_largest_file(path: str) -> tuple[str, int]`
- `format_bytes(n: int) -> str` — gibt "1.4 MB", "320 KB" etc. zurück
- `print_report(path: str) -> None` — ruft alle anderen auf und gibt den Bericht aus

---

## Anforderungen

- [ ] Alle fünf Funktionen implementiert mit korrekten Type Hints
- [ ] `pathlib.Path.rglob()` für rekursives Verzeichnis-Scanning
- [ ] `format_bytes` gibt korrekte Einheiten aus: B, KB, MB, GB
- [ ] Jede Funktion ist eigenständig testbar — kein globaler State
- [ ] `print_report` ruft nur die anderen Funktionen auf, führt selbst keine Berechnungen durch

---

## Akzeptanzkriterien

```
python file_report.py /etc

# Beispiel-Ausgabe:
# Verzeichnis: /etc
# Dateien nach Typ:
#   .conf : 42
#   .d    : 18
#   (kein Typ): 31
# Gesamt: 1.2 MB in 91 Dateien
# Größte Datei: /etc/services — 19.4 KB
```

---

[← Modul 02](modul-02.md) | [Übersicht](catalog.md) | [Modul 04 →](modul-04.md)
