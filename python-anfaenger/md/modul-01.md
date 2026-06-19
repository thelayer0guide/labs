# Modul 01 — Python & Umgebung einrichten

[Übersicht](catalog.md) | [Modul 02 →](modul-02.md)

---

**Phase:** Phase A — Grundlagen
**Zeitaufwand:** 2–3 h
**Schwierigkeit:** ★☆☆☆☆ Einsteiger
**Voraussetzungen:** Linux-Grundkenntnisse, Terminal bedienen können

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)
- [bash](https://thelayer0guide.github.io/cheat-sheets/sheets/bash-cheatsheet.html)

---

## Lernziele

- Python 3 installieren und die richtige Version prüfen
- Virtuelle Umgebungen mit `venv` erstellen und aktivieren
- Pakete mit `pip` installieren und `requirements.txt` erzeugen
- Ein erstes Skript strukturiert mit `main()` aufbauen
- Den Unterschied zwischen `python skript.py` und `python -m paket` verstehen
- VS Code mit Python-Extension einrichten

---

## Hintergrund

Python ist mittlerweile das wichtigste Werkzeug für Systemadministratoren und DevOps-Ingenieure. Bash-Skripte stoßen schnell an Grenzen, sobald Daten strukturiert verarbeitet, APIs angesprochen oder komplexe Logik abgebildet werden soll. Python löst all das — plattformübergreifend, lesbar, mit einer riesigen Standardbibliothek.

Eine sauber eingerichtete Umgebung ist kein Nice-to-have, sondern Pflicht. Virtuelle Umgebungen verhindern, dass Pakete aus verschiedenen Projekten sich gegenseitig überschreiben und den System-Python unbrauchbar machen.

---

## Schlüsselkonzepte

### Installation prüfen

```python
python3 --version
# → Python 3.12.x

which python3
# → /usr/bin/python3
```

### Virtuelle Umgebung

```python
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

pip install --upgrade pip
pip install ipython black
```

### Skript-Grundstruktur

```python
def main() -> None:
    print("Automatisierung startet...")

if __name__ == "__main__":
    main()
```

### requirements.txt erzeugen

```python
pip freeze > requirements.txt

# Später reinstallieren:
pip install -r requirements.txt
```

---

## Aufgabe

Schreibe ein Skript `sysinfo.py`, das beim Ausführen folgende Informationen strukturiert ausgibt:

Alle Ausgaben sollen gut lesbar formatiert sein — nutze f-Strings, keine `print("text" + var)`-Verkettung.

- Python-Version und Interpreter-Pfad
- Betriebssystem und Hostname
- Aktuelles Arbeitsverzeichnis
- Ob eine virtuelle Umgebung aktiv ist

---

## Anforderungen

- [ ] sysinfo.py existiert und startet ohne Fehler
- [ ] Alle vier Informationsblöcke werden ausgegeben
- [ ] `import sys, os, platform` — kein Drittpaket notwendig
- [ ] Skript hat eine `main()`-Funktion mit `if __name__ == '__main__'`-Guard
- [ ] Virtuelle Umgebung ist aktiv (prüfe `sys.prefix != sys.base_prefix`)
- [ ] requirements.txt mit `pip freeze` erzeugt (auch wenn sie leer ist)

---

## Akzeptanzkriterien

```
python sysinfo.py
# Ausgabe muss enthalten:
# Python 3.12.x — /pfad/zu/python
# OS: Linux / Hostname: mein-rechner
# Arbeitsverzeichnis: /pfad/zum/projekt
# venv aktiv: Ja

# Kein ImportError, kein SyntaxError
```

---

[Übersicht](catalog.md) | [Modul 02 →](modul-02.md)
