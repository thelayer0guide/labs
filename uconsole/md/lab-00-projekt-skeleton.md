# Lab 00 — Projekt-Skeleton & Dev-Workflow

> **Phase 0 — Fundament**
> Voraussetzungen: keine
> Geschätzte Zeit: 2–4 Stunden

---

## Lernziele

- Einen Python-Monorepo aufsetzen, der alle folgenden Labs trägt
- `poetry` oder `pip + venv` für Dependency-Management nutzen
- `pyproject.toml` als zentralen Konfigurations-Anker verstehen
- Einen reproduzierbaren Build-Workflow (Test / Lint / Format) einrichten
- Git-Workflow und `.gitignore` sauber konfigurieren
- Den Entwicklungsaufwand auf der uConsole (ARM64) einschätzen lernen

---

## Hintergrund

Bevor du das erste Tool schreibst, braucht das Projekt ein stabiles Fundament. Ein Mono-Repo mit einheitlicher Struktur macht es später trivial, Tools miteinander zu kombinieren — und ist die Voraussetzung dafür, dass alle Labs in Phase 6 zu `uctl` zusammenwachsen können.

Professionelle Python-Projekte trennen immer: Kernlogik (testbar, ohne I/O), CLI-Einstiegspunkt, Tests. Diese Struktur lernst du hier einmal sauber aufzusetzen — und hältst sie dann durch alle 17 folgenden Labs durch.

---

## Aufgabe

Richte das Mono-Repo `security-lab/` ein. Es wird das Zuhause für alle Tools aus den Labs 01–17 und schließlich für `uctl`.

### Verzeichnisstruktur

Am Ende dieses Labs muss folgende Struktur stehen:

```
security-lab/
├── pyproject.toml
├── Makefile              (oder justfile)
├── .gitignore
├── shared/
│   ├── __init__.py
│   └── output.py         (zunächst leer — Platzhalter für spätere Utils)
├── hashinspect/          (Platzhalter für Lab 01 — noch leer)
│   ├── __init__.py
│   ├── core.py
│   ├── cli.py
│   └── tests/
│       ├── __init__.py
│       └── test_core.py
└── README.md
```

Du legst **nur** `hashinspect/` als Beispielstruktur an. Die anderen Tool-Verzeichnisse entstehen in den jeweiligen Labs.

---

## Anforderungen (Pflicht)

- [ ] `pyproject.toml` enthält:
  - `[build-system]` mit `setuptools` oder `poetry-core`
  - `[project]` mit `name`, `version`, `requires-python = ">=3.11"`
  - `[project.optional-dependencies]` oder `[tool.poetry.dev-dependencies]` mit `pytest >= 7`, `ruff`, `black`
- [ ] `Makefile` (oder `justfile`) mit mindestens drei Targets:
  - `make test` → führt `pytest` aus
  - `make lint` → führt `ruff check .` aus
  - `make format` → führt `black .` aus
- [ ] `.gitignore` schließt aus: `__pycache__/`, `.venv/`, `*.egg-info/`, `.pytest_cache/`, `dist/`, `.ruff_cache/`
- [ ] `shared/__init__.py` und `shared/output.py` existieren (output.py darf leer sein)
- [ ] `hashinspect/core.py` enthält eine Stub-Funktion:
  ```python
  def hash_file(path, algos):
      raise NotImplementedError
  ```
- [ ] `hashinspect/tests/test_core.py` enthält mindestens einen Test, der aktuell fehlschlägt (`pytest.raises(NotImplementedError)`)
- [ ] `make test` läuft durch (auch wenn Tests fehlschlagen — das Ziel ist, dass pytest überhaupt startet)
- [ ] `make lint` läuft ohne Fehler
- [ ] Das Repo ist git-initialisiert, der erste Commit ist gemacht

---

## Akzeptanzkriterien

Führe nach deiner Einrichtung diese Befehle aus — alle müssen ohne Absturz durchlaufen:

```bash
cd security-lab/
make lint          # kein Fehler
make test          # pytest startet, 1 Test schlägt fehl (NotImplementedError)
python -c "from shared import output; print('OK')"   # importierbar
python -c "from hashinspect.core import hash_file"   # importierbar
git log --oneline  # mind. 1 Commit sichtbar
```

---

## Bonus-Aufgaben

- [ ] `justfile` statt `Makefile` nutzen (modernere Alternative)
- [ ] `make test-cov` als weiteres Target: `pytest --cov=. --cov-report=term-missing`
- [ ] `pyproject.toml` konfiguriert `ruff` mit `line-length = 88` und aktiviert die Regeln `E`, `F`, `I`
- [ ] `pre-commit`-Hook einrichten: lint + format vor jedem Commit automatisch

---

## uConsole-Hinweis

Richte das venv **direkt auf der uConsole** ein, sobald du das Repo dorthin geklont hast. ARM64-Wheels für Pakete wie `cryptography` oder `Pillow` sind nicht immer verfügbar — du wirst `pip install` manchmal durch `--no-binary :all:` ersetzen müssen, was längere Kompilierzeiten bedeutet. Lerne das jetzt, bevor du in Lab 07 oder 12 ein Paket brauchst und stundenlang wartest.

Teste explizit:
```bash
python -m venv .venv && source .venv/bin/activate
pip install pytest ruff black        # alle drei sollten auf ARM64 funktionieren
```

---

## Was du NICHT brauchst

- Keine echte Logik in `core.py` (kommt in Lab 01)
- Kein CI/CD-Setup (kommt in Lab 16)
- Kein vollständiges `shared/output.py` (wächst organisch)
- Keine Abhängigkeiten außer pytest, ruff, black
