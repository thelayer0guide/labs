# Modul 08 — Konfigurationsdateien automatisieren

[← Modul 07](modul-07.md) | [Übersicht](catalog.md) | [Modul 09 →](modul-09.md)

---

**Phase:** Phase B — Werkzeuge & Daten
**Zeitaufwand:** 3–4 h
**Schwierigkeit:** ★★☆☆☆ Grundkenntnisse
**Voraussetzungen:** Modul 07

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)

---

## Lernziele

- INI-Dateien mit `configparser` lesen, schreiben und modifizieren
- Typkonvertierung (`getint()`, `getboolean()`) korrekt einsetzen
- YAML-Dateien mit `yaml.safe_load()` einlesen (kein `yaml.load()`!)
- YAML-Strukturen für Docker Compose und Ansible dynamisch erzeugen
- TOML mit `tomllib` (Python 3.11+) oder `tomli` lesen
- Konverter zwischen Konfigurationsformaten schreiben

---

## Hintergrund

Konfigurationsformate haben unterschiedliche Stärken: INI ist simpel und weit verbreitet (cron, samba, many Linux tools). YAML ist lesbar und dominant in DevOps (Docker, Kubernetes, Ansible, GitHub Actions). TOML ist präzise und für Python-Projekte Standard (`pyproject.toml`).

Wichtig: `yaml.load()` ist gefährlich — es kann beliebigen Python-Code ausführen. Immer `yaml.safe_load()` verwenden, das nur sichere YAML-Typen deserialisiert.

---

## Schlüsselkonzepte

### configparser — INI lesen

```python
import configparser

cfg = configparser.ConfigParser()
cfg.read("backup.conf", encoding="utf-8")

host = cfg["database"]["host"]             # str
port = cfg["database"].getint("port")      # int
debug = cfg["app"].getboolean("debug")     # bool
```

### PyYAML — Docker Compose erzeugen

```python
import yaml

def make_compose(services: list[dict]) -> str:
    compose = {"version": "3.8", "services": {}}
    for svc in services:
        compose["services"][svc["name"]] = {
            "image": svc["image"],
            "ports": [f"{svc['port']}:{svc['port']}"],
        }
    return yaml.dump(compose, default_flow_style=False)
```

### tomllib — TOML lesen (Python 3.11+)

```python
import tomllib

with open("pyproject.toml", "rb") as f:  # rb — Binärmodus!
    config = tomllib.load(f)

version = config["project"]["version"]
deps = config["project"].get("dependencies", [])
```

---

## Aufgabe

Schreibe `config_converter.py` — ein Tool, das Konfigurationen zwischen Formaten konvertiert:

1. Erstelle eine Test-INI-Datei (`app.conf`) mit Abschnitten `[database]`, `[server]`, `[logging]`
2. Implementiere `ini_to_dict(path: Path) -> dict`: liest INI, gibt verschachteltes Dict zurück
3. Implementiere `dict_to_yaml(data: dict, path: Path) -> None`: schreibt als YAML
4. Implementiere `dict_to_json(data: dict, path: Path) -> None`: schreibt als JSON
5. CLI: `python config_converter.py app.conf --to yaml` oder `--to json`

---

## Anforderungen

- [ ] `yaml.safe_load()` — nie `yaml.load()`
- [ ] Alle INI-Werte korrekt als Strings übernommen (keine Typkonvertierung im Konverter)
- [ ] Ausgabedatei hat denselben Basisnamen wie Eingabe: `app.yaml`, `app.json`
- [ ] Unbekannte `--to`-Option gibt Fehlermeldung + Exit-Code 1
- [ ] `tomllib`-Abhängigkeit nur wenn Python < 3.11: `try: import tomllib except ImportError: import tomli as tomllib`

---

## Akzeptanzkriterien

```
# INI erstellen und konvertieren:
python config_converter.py app.conf --to yaml
ls app.yaml  # → existiert
python -c "import yaml; print(yaml.safe_load(open('app.yaml')))"  # kein Fehler

python config_converter.py app.conf --to json
python -c "import json; json.load(open('app.json'))"  # kein Fehler
```

---

[← Modul 07](modul-07.md) | [Übersicht](catalog.md) | [Modul 09 →](modul-09.md)
