#!/usr/bin/env python3
"""Generates modul-01.html through modul-14.html for python-anfaenger."""

from pathlib import Path

OUT = Path(__file__).parent / "html"
OUT.mkdir(exist_ok=True)

CHEATSHEET_BASE = "https://thelayer0guide.github.io/cheat-sheets/sheets/"

MODULES = [
    # (num, slug, phase, phase_label, accent, time, diff_n, diff_label, prev, next, sheets, tagline, sections)
    {
        "num": "01", "slug": "modul-01", "phase": "A", "phase_label": "Phase A — Grundlagen",
        "accent": "#58a6ff", "time": "2–3 h", "diff_n": 1, "diff_label": "Einsteiger",
        "prev": None, "next": "modul-02",
        "title": "Python & Umgebung einrichten",
        "sheets": [("python", "python-cheatsheet"), ("bash", "bash-cheatsheet")],
        "prereq": "Linux-Grundkenntnisse, Terminal bedienen können",
        "tagline": "Python 3.12+ installieren, virtuelle Umgebung einrichten, erstes eigenes Skript schreiben und starten.",
        "lernziele": [
            "Python 3 installieren und die richtige Version prüfen",
            "Virtuelle Umgebungen mit <code>venv</code> erstellen und aktivieren",
            "Pakete mit <code>pip</code> installieren und <code>requirements.txt</code> erzeugen",
            "Ein erstes Skript strukturiert mit <code>main()</code> aufbauen",
            "Den Unterschied zwischen <code>python skript.py</code> und <code>python -m paket</code> verstehen",
            "VS Code mit Python-Extension einrichten",
        ],
        "hintergrund": """<p>Python ist mittlerweile das wichtigste Werkzeug für Systemadministratoren und DevOps-Ingenieure. Bash-Skripte stoßen schnell an Grenzen, sobald Daten strukturiert verarbeitet, APIs angesprochen oder komplexe Logik abgebildet werden soll. Python löst all das — plattformübergreifend, lesbar, mit einer riesigen Standardbibliothek.</p>
        <p>Eine sauber eingerichtete Umgebung ist kein Nice-to-have, sondern Pflicht. Virtuelle Umgebungen verhindern, dass Pakete aus verschiedenen Projekten sich gegenseitig überschreiben und den System-Python unbrauchbar machen.</p>""",
        "konzepte": [
            ("Installation prüfen", 'python3 --version\n# → Python 3.12.x\n\nwhich python3\n# → /usr/bin/python3'),
            ("Virtuelle Umgebung", 'python3 -m venv .venv\nsource .venv/bin/activate   # Linux/macOS\n.venv\\Scripts\\activate      # Windows\n\npip install --upgrade pip\npip install ipython black'),
            ("Skript-Grundstruktur", 'def main() -> None:\n    print("Automatisierung startet...")\n\nif __name__ == "__main__":\n    main()'),
            ("requirements.txt erzeugen", 'pip freeze > requirements.txt\n\n# Später reinstallieren:\npip install -r requirements.txt'),
        ],
        "aufgabe": """<p>Schreibe ein Skript <code>sysinfo.py</code>, das beim Ausführen folgende Informationen strukturiert ausgibt:</p>
        <ul>
          <li>Python-Version und Interpreter-Pfad</li>
          <li>Betriebssystem und Hostname</li>
          <li>Aktuelles Arbeitsverzeichnis</li>
          <li>Ob eine virtuelle Umgebung aktiv ist</li>
        </ul>
        <p>Alle Ausgaben sollen gut lesbar formatiert sein — nutze f-Strings, keine <code>print("text" + var)</code>-Verkettung.</p>""",
        "anforderungen": [
            ("sysinfo.py existiert und startet ohne Fehler", []),
            ("Alle vier Informationsblöcke werden ausgegeben", []),
            ("<code>import sys, os, platform</code> — kein Drittpaket notwendig", []),
            ("Skript hat eine <code>main()</code>-Funktion mit <code>if __name__ == '__main__'</code>-Guard", []),
            ("Virtuelle Umgebung ist aktiv (prüfe <code>sys.prefix != sys.base_prefix</code>)", []),
            ("requirements.txt mit <code>pip freeze</code> erzeugt (auch wenn sie leer ist)", []),
        ],
        "akzeptanz": 'python sysinfo.py\n# Ausgabe muss enthalten:\n# Python 3.12.x — /pfad/zu/python\n# OS: Linux / Hostname: mein-rechner\n# Arbeitsverzeichnis: /pfad/zum/projekt\n# venv aktiv: Ja\n\n# Kein ImportError, kein SyntaxError',
    },
    {
        "num": "02", "slug": "modul-02", "phase": "A", "phase_label": "Phase A — Grundlagen",
        "accent": "#58a6ff", "time": "4–6 h", "diff_n": 2, "diff_label": "Grundkenntnisse",
        "prev": "modul-01", "next": "modul-03",
        "title": "Datentypen & Kontrollstrukturen",
        "sheets": [("python", "python-cheatsheet")],
        "prereq": "Modul 01",
        "tagline": "Strings, Listen, Dicts, Tupel, Sets. if/for/while, Comprehensions, Pattern Matching (3.10+).",
        "lernziele": [
            "Alle eingebauten Datentypen sicher einsetzen und ihre Unterschiede kennen",
            "Mutable vs. immutable Objects und Auswirkungen auf Seiteneffekte verstehen",
            "Slicing und <code>enumerate()</code>, <code>zip()</code>, <code>reversed()</code> idiomatisch nutzen",
            "List-, Dict- und Set-Comprehensions schreiben",
            "Kontrollfluss mit <code>if/elif/else</code>, <code>for/else</code>, <code>while/else</code> steuern",
            "Pattern Matching mit <code>match/case</code> (Python 3.10+) anwenden",
        ],
        "hintergrund": """<p>Python-Datentypen sind mächtiger als in vielen anderen Sprachen: Integer haben keine Overflow-Grenze, Strings sind Unicode-nativ, Dictionaries sind seit Python 3.7 insertion-ordered. Wer diese Eigenschaften kennt, schreibt kompakteren und korrekte Code.</p>
        <p>Comprehensions sind das vielleicht wichtigste idiomatische Merkmal von Python — sie ersetzen ganze for-Schleifen durch einen lesbaren einzeiligen Ausdruck. Falsy-Werte (<code>None</code>, <code>0</code>, <code>""</code>, <code>[]</code>, <code>{}</code>) erlauben kompakte Bedingungen ohne expliziten Vergleich.</p>""",
        "konzepte": [
            ("Dict-Comprehension", 'log_levels = ["INFO", "WARNING", "ERROR", "INFO", "ERROR"]\ncounts = {}\nfor lvl in log_levels:\n    counts[lvl] = counts.get(lvl, 0) + 1\n# kompakter:\ncounts = {lvl: log_levels.count(lvl) for lvl in set(log_levels)}'),
            ("enumerate & zip", 'hosts = ["web01", "db01", "cache01"]\nips   = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]\n\nfor i, (host, ip) in enumerate(zip(hosts, ips), start=1):\n    print(f"{i:2}. {host:<10} → {ip}")'),
            ("for-else Muster", 'def find_user(users: list[str], target: str) -> None:\n    for user in users:\n        if user == target:\n            print(f"Gefunden: {user}")\n            break\n    else:\n        print(f"{target} nicht in der Liste")'),
            ("match/case", 'def handle_status(code: int) -> str:\n    match code:\n        case 200: return "OK"\n        case 404: return "Not Found"\n        case 500 | 503: return "Server Error"\n        case _: return f"Unbekannt: {code}"'),
        ],
        "aufgabe": """<p>Schreibe <code>log_stats.py</code> — ein Skript, das eine hartcodierte Liste von Log-Einträgen (als Liste von Dicts) auswertet:</p>
        <pre><code>LOG_ENTRIES = [
    {"level": "INFO",    "service": "nginx",  "msg": "request handled"},
    {"level": "ERROR",   "service": "db",     "msg": "connection timeout"},
    {"level": "WARNING", "service": "nginx",  "msg": "slow response"},
    {"level": "ERROR",   "service": "nginx",  "msg": "upstream failed"},
    {"level": "INFO",    "service": "db",     "msg": "query ok"},
    # ... mindestens 10 Einträge total
]</code></pre>
        <p>Das Skript soll ausgeben:</p>
        <ul>
          <li>Anzahl Einträge je Log-Level (via Dict-Comprehension)</li>
          <li>Alle ERROR-Einträge mit Zeilennummer (via <code>enumerate</code>)</li>
          <li>Alle beteiligten Services ohne Duplikate (via <code>set</code>)</li>
          <li>Service mit den meisten Fehlern</li>
        </ul>""",
        "anforderungen": [
            ("Mindestens 10 hartcodierte Log-Einträge in der Liste", []),
            ("Dict-Comprehension für die Level-Zählung — keine manuelle for-Schleife zum Befüllen", []),
            ("<code>enumerate()</code> für nummerierte ERROR-Ausgabe", []),
            ("Service mit meisten Fehlern korrekt bestimmt (auch bei Gleichstand stabil)", []),
            ("Keine globalen Variablen außer <code>LOG_ENTRIES</code>; alles in Funktionen", []),
        ],
        "akzeptanz": 'python log_stats.py\n\n# Erwartete Ausgabe (Beispiel):\n# Log-Level-Verteilung:\n#   INFO    : 4\n#   ERROR   : 3\n#   WARNING : 2\n#\n# ERROR-Einträge:\n#   1. [db]    connection timeout\n#   2. [nginx] upstream failed\n#   ...\n#\n# Services: {\'nginx\', \'db\'}\n# Meiste Fehler: nginx (2)',
    },
    {
        "num": "03", "slug": "modul-03", "phase": "A", "phase_label": "Phase A — Grundlagen",
        "accent": "#58a6ff", "time": "3–4 h", "diff_n": 2, "diff_label": "Grundkenntnisse",
        "prev": "modul-02", "next": "modul-04",
        "title": "Funktionen & Wiederverwendbarkeit",
        "sheets": [("python", "python-cheatsheet")],
        "prereq": "Modul 02",
        "tagline": "def, Parameter, Rückgabewerte, Default-Argumente, Keyword-Args. Code in wiederverwendbare Bausteine kapseln.",
        "lernziele": [
            "Funktionen mit <code>def</code> definieren und aufrufen",
            "Pflicht-, Default- und Keyword-Argumente unterscheiden und kombinieren",
            "Type Hints für Parameter und Rückgabewerte schreiben (<code>str</code>, <code>int</code>, <code>list[str]</code>)",
            "Mehrere Rückgabewerte via Tuple-Unpacking nutzen",
            "Docstrings sinnvoll — aber knapp — einsetzen",
            "Code-Duplikate durch Funktionen eliminieren",
        ],
        "hintergrund": """<p>Funktionen sind das wichtigste Strukturierungsmittel in Python. Eine Funktion sollte genau eine Sache tun, die ihr Name beschreibt. Die Grenze: wenn du eine Funktion nicht in einem Satz erklären kannst, ist sie zu groß.</p>
        <p>Type Hints (eingeführt in Python 3.5, vollständig seit 3.9) werden zur Laufzeit nicht erzwungen — sie sind Dokumentation für den Leser und das IDE. <code>mypy</code> kann sie statisch prüfen. In Admin-Skripten genügt oft <code>str</code>, <code>int</code>, <code>Path</code>, <code>list[str]</code>.</p>""",
        "konzepte": [
            ("Funktionssignatur mit Type Hints", 'def scan_directory(path: str, extension: str = ".log") -> list[str]:\n    """Gibt alle Dateien mit gegebener Endung zurück."""\n    from pathlib import Path\n    return [str(f) for f in Path(path).rglob(f"*{extension}")]'),
            ("Mehrere Rückgabewerte", 'def file_stats(path: str) -> tuple[int, int, int]:\n    """Gibt (Zeilen, Wörter, Bytes) zurück."""\n    text = open(path).read()\n    return len(text.splitlines()), len(text.split()), len(text.encode())\n\nlines, words, size = file_stats("server.log")'),
            ("Keyword-Only Args", 'def backup(source: str, dest: str, *, dry_run: bool = False) -> None:\n    if dry_run:\n        print(f"[DRY] {source} → {dest}")\n        return\n    # ... echtes Backup\n\nbackup("/data", "/backup", dry_run=True)'),
        ],
        "aufgabe": """<p>Schreibe <code>file_report.py</code>: ein Skript, das ein Verzeichnis analysiert und einen Bericht ausgibt.</p>
        <p>Das Skript soll folgende Funktionen enthalten:</p>
        <ul>
          <li><code>count_files_by_extension(path: str) -&gt; dict[str, int]</code></li>
          <li><code>total_size_bytes(path: str) -&gt; int</code></li>
          <li><code>find_largest_file(path: str) -&gt; tuple[str, int]</code></li>
          <li><code>format_bytes(n: int) -&gt; str</code> — gibt "1.4 MB", "320 KB" etc. zurück</li>
          <li><code>print_report(path: str) -&gt; None</code> — ruft alle anderen auf und gibt den Bericht aus</li>
        </ul>""",
        "anforderungen": [
            ("Alle fünf Funktionen implementiert mit korrekten Type Hints", []),
            ("<code>pathlib.Path.rglob()</code> für rekursives Verzeichnis-Scanning", []),
            ("<code>format_bytes</code> gibt korrekte Einheiten aus: B, KB, MB, GB", []),
            ("Jede Funktion ist eigenständig testbar — kein globaler State", []),
            ("<code>print_report</code> ruft nur die anderen Funktionen auf, führt selbst keine Berechnungen durch", []),
        ],
        "akzeptanz": 'python file_report.py /etc\n\n# Beispiel-Ausgabe:\n# Verzeichnis: /etc\n# Dateien nach Typ:\n#   .conf : 42\n#   .d    : 18\n#   (kein Typ): 31\n# Gesamt: 1.2 MB in 91 Dateien\n# Größte Datei: /etc/services — 19.4 KB',
    },
    {
        "num": "04", "slug": "modul-04", "phase": "A", "phase_label": "Phase A — Grundlagen",
        "accent": "#58a6ff", "time": "3–4 h", "diff_n": 2, "diff_label": "Grundkenntnisse",
        "prev": "modul-03", "next": "modul-05",
        "title": "Module, Pakete & Projektstruktur",
        "sheets": [("python", "python-cheatsheet"), ("bash", "bash-cheatsheet")],
        "prereq": "Modul 03",
        "tagline": "Eigene Module erstellen, importieren und als Paket strukturieren. sys.path verstehen. Skripte sauber organisieren.",
        "lernziele": [
            "Den Unterschied zwischen Modul, Paket und Skript erklären",
            "Eigene Module erstellen und mit verschiedenen <code>import</code>-Formen verwenden",
            "Ein Paket mit <code>__init__.py</code> aufbauen",
            "Den Modulauflösungspfad (<code>sys.path</code>) verstehen",
            "Den <code>if __name__ == '__main__'</code>-Guard korrekt einsetzen",
            "Ein Admin-Projekt nach empfohlener Verzeichnisstruktur organisieren",
        ],
        "hintergrund": """<p>Ab einer gewissen Komplexität wird ein einzelnes Skript unübersichtlich. Python löst das mit Modulen (einzelne .py-Dateien) und Paketen (Verzeichnisse mit <code>__init__.py</code>). Die Aufteilung ermöglicht Wiederverwendung: Eine Funktion, die Logdateien liest, kann in mehreren Skripten genutzt werden, ohne sie zu kopieren.</p>
        <p>Der <code>if __name__ == '__main__'</code>-Guard ist entscheidend: Er stellt sicher, dass Code nur ausgeführt wird, wenn das Skript direkt gestartet wird — nicht wenn es von einem anderen Modul importiert wird.</p>""",
        "konzepte": [
            ("Empfohlene Projektstruktur", 'admin-toolkit/\n├── .venv/\n├── requirements.txt\n├── main.py              ← Einstiegspunkt\n└── lib/\n    ├── __init__.py\n    ├── file_utils.py    ← Funktionen aus Modul 03\n    └── report.py'),
            ("Import-Varianten", '# Ganzes Modul\nimport lib.file_utils\nlib.file_utils.count_files_by_extension(".")\n\n# Selektiver Import\nfrom lib.file_utils import count_files_by_extension, total_size_bytes\n\n# Alias\nfrom lib import file_utils as fu'),
            ("__init__.py für saubere API", '# lib/__init__.py\nfrom .file_utils import count_files_by_extension, total_size_bytes, find_largest_file\nfrom .report import print_report\n\n# Dann von außen:\nfrom lib import print_report'),
        ],
        "aufgabe": """<p>Nimm <code>file_report.py</code> aus Modul 03 und refaktoriere es zu einem echten Paket:</p>
        <ol>
          <li>Erstelle die Struktur <code>file-toolkit/lib/</code> mit <code>__init__.py</code></li>
          <li>Verschiebe Berechnungsfunktionen nach <code>lib/file_utils.py</code></li>
          <li>Verschiebe Ausgabefunktionen nach <code>lib/report.py</code></li>
          <li>Erstelle <code>main.py</code>, der <code>sys.argv[1]</code> als Pfad entgegennimmt und den Bericht ausgibt</li>
          <li>Stelle sicher, dass <code>lib/file_utils.py</code> auch direkt als Skript ausführbar ist und dann das aktuelle Verzeichnis analysiert</li>
        </ol>""",
        "anforderungen": [
            ("<code>lib/__init__.py</code> exportiert alle öffentlichen Funktionen", []),
            ("<code>main.py</code> importiert nur aus <code>lib</code>, enthält selbst keine Berechnungslogik", []),
            ("<code>python main.py /etc</code> gibt denselben Bericht wie Modul 03 aus", []),
            ("<code>python lib/file_utils.py</code> analysiert das aktuelle Verzeichnis", []),
            ("Kein <code>sys.path</code>-Hacking nötig — Struktur funktioniert out-of-the-box", []),
        ],
        "akzeptanz": '# Aus dem Projektverzeichnis:\npython main.py /var/log\n# → gleicher Report wie in Modul 03\n\npython lib/file_utils.py\n# → Report über aktuelles Verzeichnis\n\n# Kein ImportError, keine Pfadmanipulation',
    },
    {
        "num": "05", "slug": "modul-05", "phase": "B", "phase_label": "Phase B — Werkzeuge & Daten",
        "accent": "#3fb950", "time": "4–6 h", "diff_n": 3, "diff_label": "Fortgeschritten",
        "prev": "modul-04", "next": "modul-06",
        "title": "OOP: Klassen & Dataclasses",
        "sheets": [("python", "python-cheatsheet")],
        "prereq": "Modul 04",
        "tagline": "Eigene Klassen modellieren. @dataclass für Datenobjekte. Entscheiden, wann OOP besser ist als Funktionen.",
        "lernziele": [
            "Klassen mit <code>__init__</code>, Attributen und Methoden definieren",
            "<code>__repr__</code> und <code>__str__</code> für lesbare Objektdarstellung implementieren",
            "<code>@dataclass</code> für kompakte Datenobjekte einsetzen",
            "Mutable Default-Werte mit <code>field(default_factory=...)</code> korrekt handhaben",
            "<code>frozen=True</code> für unveränderliche Konfigurationsobjekte nutzen",
            "Entscheidungskriterien: Wann Klasse, wann Dict, wann Dataclass?",
        ],
        "hintergrund": """<p>OOP ist in Python kein Pflichtparadigma — Funktionen und Dicts lösen viele Probleme eleganter. Klassen werden sinnvoll, wenn Daten und die dazugehörige Logik zusammen verwaltet werden müssen und das Objekt einen Zustand hat, der sich über mehrere Operationen verändert.</p>
        <p><code>@dataclass</code> (Python 3.7+) ist der Sweet Spot für reine Datenobjekte: Es generiert automatisch <code>__init__</code>, <code>__repr__</code> und <code>__eq__</code>, ohne Boilerplate. Für Konfigurationsobjekte, API-Antworten und DTOs ist es die erste Wahl.</p>""",
        "konzepte": [
            ("Klasse mit Zustand", 'class Server:\n    def __init__(self, hostname: str, ip: str) -> None:\n        self.hostname = hostname\n        self.ip = ip\n        self.online: bool = False\n\n    def start(self) -> None:\n        self.online = True\n\n    def __repr__(self) -> str:\n        status = "online" if self.online else "offline"\n        return f"Server({self.hostname!r}, {status})"'),
            ("@dataclass", 'from dataclasses import dataclass, field\n\n@dataclass\nclass LogEntry:\n    level: str\n    service: str\n    message: str\n    tags: list[str] = field(default_factory=list)\n\n    def is_error(self) -> bool:\n        return self.level == "ERROR"'),
            ("frozen Dataclass", 'from dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass DBConfig:\n    host: str\n    port: int = 5432\n    database: str = "prod"\n\n# Unveränderlich — wirft FrozenInstanceError bei Zuweisung\ncfg = DBConfig(host="db.intern")\nprint(cfg.host, cfg.port)'),
        ],
        "aufgabe": """<p>Modelliere eine Server-Verwaltung mit zwei Klassen:</p>
        <p><strong>1. <code>@dataclass class ServerConfig</code></strong> (frozen): host, port, os, role (web/db/cache)</p>
        <p><strong>2. <code>class Server</code></strong>: Nimmt eine <code>ServerConfig</code> im Konstruktor, verwaltet Zustand (<code>online</code>, <code>error_count</code>) und hat Methoden:</p>
        <ul>
          <li><code>ping(self) -&gt; bool</code> — simuliert Ping (gibt bei online=True immer True zurück)</li>
          <li><code>record_error(self, msg: str) -&gt; None</code> — erhöht error_count, speichert letzte Fehlermeldung</li>
          <li><code>status_report(self) -&gt; dict</code> — gibt dict mit allen Infos zurück</li>
        </ul>
        <p><strong>3. <code>class ServerPool</code></strong>: Verwaltet eine Liste von Servern, bietet <code>add()</code>, <code>all_online()</code>, <code>servers_by_role(role)</code>, <code>summary()</code>.</p>""",
        "anforderungen": [
            ("<code>ServerConfig</code> ist frozen — Zuweisung nach Erstellung wirft Exception", []),
            ("<code>Server</code> speichert letzten Fehler als Instanzattribut", []),
            ("<code>ServerPool.summary()</code> gibt Gesamtzahl, Anzahl online, Anzahl mit Fehlern zurück", []),
            ("<code>servers_by_role('web')</code> filtert korrekt", []),
            ("Kein globaler State — alle Daten leben in Instanzattributen", []),
        ],
        "akzeptanz": "pool = ServerPool()\npool.add(Server(ServerConfig('web01', 8080, 'Ubuntu 24', 'web')))\npool.add(Server(ServerConfig('db01', 5432, 'Debian 12', 'db')))\npool.servers[0].online = True\npool.servers[1].record_error('connection refused')\n\nprint(pool.summary())\n# {'total': 2, 'online': 1, 'with_errors': 1}\n\nprint(pool.servers_by_role('web'))\n# [Server(web01, online)]",
    },
    {
        "num": "06", "slug": "modul-06", "phase": "B", "phase_label": "Phase B — Werkzeuge & Daten",
        "accent": "#3fb950", "time": "5–7 h", "diff_n": 3, "diff_label": "Fortgeschritten",
        "prev": "modul-05", "next": "modul-07",
        "title": "Werkzeuge der Standardbibliothek",
        "sheets": [("python", "python-cheatsheet"), ("bash", "bash-cheatsheet")],
        "prereq": "Modul 05",
        "tagline": "pathlib, shutil, os, subprocess, argparse, datetime, platform, ipaddress — alles ohne Drittpaket.",
        "lernziele": [
            "<code>pathlib.Path</code> für alle Dateisystemoperationen verwenden (kein <code>os.path</code> mehr)",
            "Verzeichnisse und Archive mit <code>shutil</code> automatisiert verwalten",
            "Externe Befehle sicher mit <code>subprocess.run()</code> aufrufen (kein <code>shell=True</code>)",
            "CLI-Interfaces mit <code>argparse</code> bauen: Argumente, Flags, Subcommands",
            "Zeitstempel formatieren und Zeiträume berechnen mit <code>datetime</code>",
            "IP-Adressen und Netzwerke mit <code>ipaddress</code> validieren",
        ],
        "hintergrund": """<p>Die Python-Standardbibliothek ist umfangreich genug, dass man für die meisten Admin-Aufgaben kein einziges Drittpaket braucht. Das ist wichtig in Umgebungen, wo <code>pip install</code> nicht möglich ist oder nicht erwünscht ist.</p>
        <p><code>subprocess.run()</code> ist die sichere Methode für externe Befehle. Der Schlüssel: Befehle immer als Liste übergeben (<code>["ls", "-la", path]</code>), nie als String mit <code>shell=True</code> — das öffnet Shell-Injection-Schwachstellen.</p>""",
        "konzepte": [
            ("pathlib — sicher und lesbar", 'from pathlib import Path\n\nlog_dir = Path("/var/log")\nfor log_file in log_dir.rglob("*.log"):\n    size = log_file.stat().st_size\n    print(f"{log_file.name:30} {size / 1024:6.1f} KB")'),
            ("subprocess ohne shell=True", 'import subprocess\n\nresult = subprocess.run(\n    ["df", "-h", "/"],\n    capture_output=True, text=True, timeout=10\n)\nif result.returncode == 0:\n    print(result.stdout)\nelse:\n    print("Fehler:", result.stderr)'),
            ("argparse mit Subcommands", 'import argparse\n\nparser = argparse.ArgumentParser(description="syscheck")\nsub = parser.add_subparsers(dest="cmd")\n\ndisk_p = sub.add_parser("disk", help="Speicherplatz prüfen")\ndisk_p.add_argument("path", nargs="?", default="/")\n\nenv_p = sub.add_parser("env", help="Umgebungsvariable abfragen")\nenv_p.add_argument("key")\n\nargs = parser.parse_args()'),
            ("ipaddress Validierung", 'import ipaddress\n\ndef parse_ip(raw: str) -> ipaddress.IPv4Address | None:\n    try:\n        return ipaddress.IPv4Address(raw)\n    except ipaddress.AddressValueError:\n        return None\n\nnet = ipaddress.IPv4Network("192.168.1.0/24")\nprint(ipaddress.IPv4Address("192.168.1.50") in net)  # True'),
        ],
        "aufgabe": """<p>Baue <code>syscheck</code> — ein CLI-Tool mit drei Subcommands:</p>
        <ul>
          <li><strong><code>syscheck disk [PATH]</code></strong>: Zeigt Speicherbelegung via <code>shutil.disk_usage()</code>. Default: <code>/</code>. Flag <code>--warn PROZENT</code> gibt Warnung aus, wenn über Schwelle.</li>
          <li><strong><code>syscheck env KEY</code></strong>: Liest Umgebungsvariable via <code>os.environ.get()</code>. Gibt Fehlermeldung + Exit-Code 1, wenn nicht gesetzt.</li>
          <li><strong><code>syscheck run BEFEHL [ARGS...]</code></strong>: Führt externen Befehl aus und gibt stdout/stderr getrennt aus. Flag <code>--timeout N</code> (Default: 30).</li>
        </ul>""",
        "anforderungen": [
            ("<code>argparse</code> mit drei Subcommands, jeder mit eigenem <code>--help</code>", []),
            ("<code>disk</code>: gibt Gesamt, Benutzt, Frei in lesbarer Form aus; Warnung korrekt", []),
            ("<code>env</code>: Exit-Code 1 + Fehlermeldung auf stderr wenn Variable fehlt", []),
            ("<code>run</code>: kein <code>shell=True</code>; Timeout korrekt übergeben; returncode ausgeben", []),
            ("Unbekannter Subcommand zeigt Hilfe und beendet mit Exit-Code 2", []),
        ],
        "akzeptanz": 'python syscheck.py disk / --warn 80\n# → Disk /: 45.2 GB / 100.0 GB (45%) — OK\n\npython syscheck.py env HOME\n# → HOME=/home/user\n\npython syscheck.py env NICHT_GESETZT; echo $?\n# → Fehler: NICHT_GESETZT nicht gesetzt\n# → 1\n\npython syscheck.py run ls -la /tmp\n# → (Ausgabe von ls)',
    },
    {
        "num": "07", "slug": "modul-07", "phase": "B", "phase_label": "Phase B — Werkzeuge & Daten",
        "accent": "#3fb950", "time": "3–5 h", "diff_n": 2, "diff_label": "Grundkenntnisse",
        "prev": "modul-06", "next": "modul-08",
        "title": "Dateien & Daten verarbeiten",
        "sheets": [("python", "python-cheatsheet"), ("json", "json-cheatsheet")],
        "prereq": "Modul 04",
        "tagline": "Textdateien sicher öffnen. CSV mit DictReader/DictWriter. JSON laden und speichern. Große Dateien speichereffizient lesen.",
        "lernziele": [
            "Dateien mit Context Manager (<code>with open()</code>) sicher öffnen und schließen",
            "Große Dateien zeilenweise lesen ohne alles in den RAM zu laden",
            "CSV-Dateien mit <code>csv.DictReader</code> und <code>csv.DictWriter</code> verarbeiten",
            "JSON mit <code>json.load()</code> und <code>json.dump(indent=2)</code> lesen und schreiben",
            "UTF-8-Kodierung explizit setzen",
            "Mehrere Dateien zusammenführen (merge)",
        ],
        "hintergrund": """<p>Dateien sind das universelle Interface in der Systemadministration: Logdateien, Konfigurationen, Exporte. Die wichtigste Regel: immer den Context Manager (<code>with</code>) verwenden — er stellt sicher, dass Dateien auch bei Ausnahmen korrekt geschlossen werden.</p>
        <p>CSV-Dateien ohne Header sind schwer zu lesen. <code>csv.DictReader</code> macht Spaltennamen zum Dict-Schlüssel — das macht den Code lesbar und robust gegenüber Spaltenverschiebungen.</p>""",
        "konzepte": [
            ("Zeilenweises Lesen", 'from pathlib import Path\n\ndef count_errors(log_path: Path) -> int:\n    count = 0\n    with log_path.open(encoding="utf-8") as f:\n        for line in f:  # nie f.read() bei großen Dateien!\n            if "ERROR" in line:\n                count += 1\n    return count'),
            ("CSV DictReader", 'import csv\nfrom pathlib import Path\n\ndef read_server_inventory(path: Path) -> list[dict]:\n    with path.open(newline="", encoding="utf-8") as f:\n        return list(csv.DictReader(f))\n\n# CSV-Header: hostname,ip,os,role\nservers = read_server_inventory(Path("servers.csv"))'),
            ("JSON schreiben", 'import json\nfrom pathlib import Path\n\ndef save_report(data: dict, path: Path) -> None:\n    with path.open("w", encoding="utf-8") as f:\n        json.dump(data, f, indent=2, ensure_ascii=False)'),
        ],
        "aufgabe": """<p>Schreibe <code>log_aggregator.py</code>:</p>
        <ol>
          <li>Erstelle drei Test-CSV-Dateien (<code>logs_jan.csv</code>, <code>logs_feb.csv</code>, <code>logs_mar.csv</code>) mit Spalten: <code>timestamp,level,service,message</code></li>
          <li>Schreibe <code>merge_csv_logs(paths: list[Path]) -&gt; list[dict]</code>: liest alle CSVs und gibt eine zusammengeführte Liste zurück</li>
          <li>Schreibe <code>filter_by_level(entries: list[dict], level: str) -&gt; list[dict]</code></li>
          <li>Schreibe <code>summary_report(entries: list[dict]) -&gt; dict</code>: gibt <code>{"total": N, "by_level": {...}, "by_service": {...}}</code> zurück</li>
          <li>Speichere den Report als <code>report.json</code> mit <code>indent=2</code></li>
        </ol>""",
        "anforderungen": [
            ("Alle CSV-Dateien mit <code>newline=''</code> und <code>encoding='utf-8'</code> geöffnet", []),
            ("<code>merge_csv_logs</code> akzeptiert beliebig viele Pfade", []),
            ("<code>summary_report</code> gibt korrekte Zählungen für alle Level und Services zurück", []),
            ("report.json enthält gültiges JSON mit <code>indent=2</code>", []),
            ("Kein <code>f.read()</code> ohne Größenangabe — zeilenweises Lesen bei Textdateien", []),
        ],
        "akzeptanz": 'python log_aggregator.py\n\n# report.json muss gültiges JSON sein:\npython -c "import json; json.load(open(\'report.json\'))"\n# → kein Fehler\n\ncat report.json\n# {\n#   "total": 30,\n#   "by_level": {"INFO": 15, "WARNING": 8, "ERROR": 7},\n#   "by_service": {"nginx": 12, "db": 10, "auth": 8}\n# }',
    },
    {
        "num": "08", "slug": "modul-08", "phase": "B", "phase_label": "Phase B — Werkzeuge & Daten",
        "accent": "#3fb950", "time": "3–4 h", "diff_n": 2, "diff_label": "Grundkenntnisse",
        "prev": "modul-07", "next": "modul-09",
        "title": "Konfigurationsdateien automatisieren",
        "sheets": [("python", "python-cheatsheet")],
        "prereq": "Modul 07",
        "tagline": "INI-Dateien mit configparser lesen und schreiben. YAML für Docker/Ansible/K8s. TOML für moderne Python-Projekte.",
        "lernziele": [
            "INI-Dateien mit <code>configparser</code> lesen, schreiben und modifizieren",
            "Typkonvertierung (<code>getint()</code>, <code>getboolean()</code>) korrekt einsetzen",
            "YAML-Dateien mit <code>yaml.safe_load()</code> einlesen (kein <code>yaml.load()</code>!)",
            "YAML-Strukturen für Docker Compose und Ansible dynamisch erzeugen",
            "TOML mit <code>tomllib</code> (Python 3.11+) oder <code>tomli</code> lesen",
            "Konverter zwischen Konfigurationsformaten schreiben",
        ],
        "hintergrund": """<p>Konfigurationsformate haben unterschiedliche Stärken: INI ist simpel und weit verbreitet (cron, samba, many Linux tools). YAML ist lesbar und dominant in DevOps (Docker, Kubernetes, Ansible, GitHub Actions). TOML ist präzise und für Python-Projekte Standard (<code>pyproject.toml</code>).</p>
        <p>Wichtig: <code>yaml.load()</code> ist gefährlich — es kann beliebigen Python-Code ausführen. Immer <code>yaml.safe_load()</code> verwenden, das nur sichere YAML-Typen deserialisiert.</p>""",
        "konzepte": [
            ("configparser — INI lesen", 'import configparser\n\ncfg = configparser.ConfigParser()\ncfg.read("backup.conf", encoding="utf-8")\n\nhost = cfg["database"]["host"]             # str\nport = cfg["database"].getint("port")      # int\ndebug = cfg["app"].getboolean("debug")     # bool'),
            ("PyYAML — Docker Compose erzeugen", 'import yaml\n\ndef make_compose(services: list[dict]) -> str:\n    compose = {"version": "3.8", "services": {}}\n    for svc in services:\n        compose["services"][svc["name"]] = {\n            "image": svc["image"],\n            "ports": [f"{svc[\'port\']}:{svc[\'port\']}"],\n        }\n    return yaml.dump(compose, default_flow_style=False)'),
            ("tomllib — TOML lesen (Python 3.11+)", 'import tomllib\n\nwith open("pyproject.toml", "rb") as f:  # rb — Binärmodus!\n    config = tomllib.load(f)\n\nversion = config["project"]["version"]\ndeps = config["project"].get("dependencies", [])'),
        ],
        "aufgabe": """<p>Schreibe <code>config_converter.py</code> — ein Tool, das Konfigurationen zwischen Formaten konvertiert:</p>
        <ol>
          <li>Erstelle eine Test-INI-Datei (<code>app.conf</code>) mit Abschnitten <code>[database]</code>, <code>[server]</code>, <code>[logging]</code></li>
          <li>Implementiere <code>ini_to_dict(path: Path) -&gt; dict</code>: liest INI, gibt verschachteltes Dict zurück</li>
          <li>Implementiere <code>dict_to_yaml(data: dict, path: Path) -&gt; None</code>: schreibt als YAML</li>
          <li>Implementiere <code>dict_to_json(data: dict, path: Path) -&gt; None</code>: schreibt als JSON</li>
          <li>CLI: <code>python config_converter.py app.conf --to yaml</code> oder <code>--to json</code></li>
        </ol>""",
        "anforderungen": [
            ("<code>yaml.safe_load()</code> — nie <code>yaml.load()</code>", []),
            ("Alle INI-Werte korrekt als Strings übernommen (keine Typkonvertierung im Konverter)", []),
            ("Ausgabedatei hat denselben Basisnamen wie Eingabe: <code>app.yaml</code>, <code>app.json</code>", []),
            ("Unbekannte <code>--to</code>-Option gibt Fehlermeldung + Exit-Code 1", []),
            ("<code>tomllib</code>-Abhängigkeit nur wenn Python &lt; 3.11: <code>try: import tomllib except ImportError: import tomli as tomllib</code>", []),
        ],
        "akzeptanz": '# INI erstellen und konvertieren:\npython config_converter.py app.conf --to yaml\nls app.yaml  # → existiert\npython -c "import yaml; print(yaml.safe_load(open(\'app.yaml\')))"  # kein Fehler\n\npython config_converter.py app.conf --to json\npython -c "import json; json.load(open(\'app.json\'))"  # kein Fehler',
    },
    {
        "num": "09", "slug": "modul-09", "phase": "B", "phase_label": "Phase B — Werkzeuge & Daten",
        "accent": "#3fb950", "time": "4–6 h", "diff_n": 3, "diff_label": "Fortgeschritten",
        "prev": "modul-08", "next": "modul-10",
        "title": "HTTP, APIs & Webservices",
        "sheets": [("python", "python-cheatsheet"), ("curl", "curl-cheatsheet"), ("json", "json-cheatsheet")],
        "prereq": "Modul 07",
        "tagline": "REST-APIs mit requests abfragen. JSON verarbeiten. API-Keys sicher mit .env speichern. Paginierung, Timeout, Auth.",
        "lernziele": [
            "GET- und POST-Requests mit <code>requests</code> korrekt senden",
            "JSON-Antworten verarbeiten und in eigene Datenstrukturen überführen",
            "API-Keys und Tokens aus <code>.env</code>-Dateien laden (<code>python-dotenv</code>)",
            "Timeouts, Retry-Logik und <code>raise_for_status()</code> für robuste Requests",
            "Paginated APIs vollständig abrufen",
            "Dateien speichereffizient mit <code>stream=True</code> herunterladen",
        ],
        "hintergrund": """<p>Fast jede moderne Infrastruktur hat eine API: Monitoring-Tools, Cloud-Provider, Ticketsysteme, Git-Plattformen. Wer REST-APIs aus Python heraus bedienen kann, automatisiert, was sonst manuell bleiben würde.</p>
        <p>API-Keys niemals hardcoden — sie landen sonst in der Versionsverwaltung. <code>python-dotenv</code> lädt Schlüssel aus einer <code>.env</code>-Datei, die in <code>.gitignore</code> aufgenommen wird.</p>""",
        "konzepte": [
            ("GET mit Fehlerbehandlung", 'import requests\n\ndef fetch_users(base_url: str, token: str) -> list[dict]:\n    headers = {"Authorization": f"Bearer {token}"}\n    resp = requests.get(f"{base_url}/users", headers=headers, timeout=10)\n    resp.raise_for_status()  # wirft HTTPError bei 4xx/5xx\n    return resp.json()'),
            (".env laden", '# .env Datei:\n# API_TOKEN=abc123\n# API_BASE=https://api.example.com\n\nfrom dotenv import load_dotenv\nimport os\n\nload_dotenv()  # liest .env aus aktuellem Verzeichnis\ntoken = os.environ["API_TOKEN"]\nbase  = os.environ["API_BASE"]'),
            ("Paginierung", 'def fetch_all_pages(url: str) -> list[dict]:\n    results = []\n    page = 1\n    while True:\n        resp = requests.get(url, params={"page": page, "per_page": 100}, timeout=10)\n        resp.raise_for_status()\n        data = resp.json()\n        if not data:\n            break\n        results.extend(data)\n        page += 1\n    return results'),
        ],
        "aufgabe": """<p>Schreibe <code>api_poller.py</code>, das die öffentliche JSONPlaceholder-API (<code>https://jsonplaceholder.typicode.com</code>) abfragt:</p>
        <ol>
          <li><code>fetch_posts(user_id: int | None) -&gt; list[dict]</code>: alle Posts oder Posts eines Users</li>
          <li><code>fetch_user(user_id: int) -&gt; dict</code>: User-Daten inkl. Adresse</li>
          <li><code>posts_per_user(posts: list[dict]) -&gt; dict[int, int]</code>: Anzahl Posts je User-ID</li>
          <li>Alle Daten lokal als <code>posts_cache.json</code> speichern, bei erneutem Aufruf aus Cache laden wenn nicht älter als 5 Minuten</li>
          <li>CLI: <code>--user-id N</code> filtert nach User, <code>--refresh</code> ignoriert Cache</li>
        </ol>""",
        "anforderungen": [
            ("<code>timeout=10</code> bei allen Requests", []),
            ("<code>raise_for_status()</code> bei allen Antworten", []),
            ("Cache-Prüfung via <code>Path.stat().st_mtime</code> und <code>time.time()</code>", []),
            ("<code>--refresh</code>-Flag löscht Cache und lädt neu", []),
            ("Kein API-Key nötig für JSONPlaceholder — aber Struktur für Bearer-Token vorbereiten", []),
        ],
        "akzeptanz": 'python api_poller.py\n# → lädt Posts, speichert posts_cache.json\n\npython api_poller.py\n# → "Cache verwendet (2m 14s alt)"\n\npython api_poller.py --user-id 3\n# → zeigt nur Posts von User 3\n\npython api_poller.py --refresh\n# → Cache ignoriert, neu geladen',
    },
    {
        "num": "10", "slug": "modul-10", "phase": "B", "phase_label": "Phase B — Werkzeuge & Daten",
        "accent": "#3fb950", "time": "3–5 h", "diff_n": 2, "diff_label": "Grundkenntnisse",
        "prev": "modul-09", "next": "modul-11",
        "title": "Fehlerbehandlung & Logging",
        "sheets": [("python", "python-cheatsheet")],
        "prereq": "Modul 04",
        "tagline": "try/except/else/finally für robuste Skripte. logging-Modul mit Handlern, Formattern und Log-Leveln. Rotierende Logdateien.",
        "lernziele": [
            "Spezifische Exceptions fangen statt blankem <code>except:</code>",
            "<code>try/except/else/finally</code> korrekt strukturieren",
            "Das <code>logging</code>-Modul gegenüber <code>print()</code> bevorzugen und warum",
            "Logger, Handler und Formatter konfigurieren",
            "Log-Level (DEBUG, INFO, WARNING, ERROR, CRITICAL) sinnvoll einsetzen",
            "Rotierende Logdateien mit <code>RotatingFileHandler</code> einrichten",
        ],
        "hintergrund": """<p>In Produktionsskripten ist <code>print()</code> für Fehlerausgaben ungeeignet: Es gibt keine Zeitstempel, kein Log-Level, keine Möglichkeit, Ausgaben in Dateien umzuleiten ohne Shell-Tricks. Das <code>logging</code>-Modul löst all das — und ist in der Standardbibliothek enthalten.</p>
        <p>Spezifische Exceptions zu fangen ist wichtig: <code>except Exception</code> fängt alles, auch Programmierfehler wie <code>NameError</code> oder <code>TypeError</code>, die sofort sichtbar sein sollten.</p>""",
        "konzepte": [
            ("try/except/else/finally", 'def read_config(path: str) -> dict:\n    try:\n        with open(path, encoding="utf-8") as f:\n            return json.load(f)\n    except FileNotFoundError:\n        logger.error("Config nicht gefunden: %s", path)\n        raise\n    except json.JSONDecodeError as e:\n        logger.error("Ungültiges JSON in %s: %s", path, e)\n        raise ValueError(f"Config-Fehler: {e}") from e\n    else:\n        logger.info("Config geladen: %s", path)'),
            ("Logging konfigurieren", 'import logging\nfrom logging.handlers import RotatingFileHandler\n\nlogger = logging.getLogger(__name__)\nlogger.setLevel(logging.DEBUG)\n\n# Konsole: INFO+\nch = logging.StreamHandler()\nch.setLevel(logging.INFO)\nch.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))\n\n# Datei: DEBUG+, max 1 MB, 3 Backups\nfh = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3)\nfh.setLevel(logging.DEBUG)\nfh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))\n\nlogger.addHandler(ch)\nlogger.addHandler(fh)'),
        ],
        "aufgabe": """<p>Refaktoriere <code>api_poller.py</code> aus Modul 09 mit vollständiger Fehlerbehandlung und Logging:</p>
        <ol>
          <li>Richte einen Logger ein: Konsole (INFO+) + rotierende Datei <code>poller.log</code> (DEBUG+)</li>
          <li>Alle API-Aufrufe in <code>try/except</code> einwickeln: <code>requests.Timeout</code>, <code>requests.HTTPError</code>, <code>requests.ConnectionError</code> separat behandeln</li>
          <li>Cache-Operationen mit <code>try/except (FileNotFoundError, json.JSONDecodeError)</code> absichern</li>
          <li>Fehler werden geloggt, nicht als <code>print()</code> ausgegeben</li>
          <li>Bei nicht-behebbaren Fehlern: <code>logger.critical(...)</code> + <code>sys.exit(1)</code></li>
        </ol>""",
        "anforderungen": [
            ("<code>logging.getLogger(__name__)</code> — kein <code>logging.basicConfig()</code> im Modul-Code", []),
            ("Jede Exception-Art gibt eine sinnvolle, nicht-generische Fehlermeldung", []),
            ("<code>poller.log</code> enthält Zeitstempel, Modul-Name, Level und Message", []),
            ("Konsolenausgabe zeigt keine DEBUG-Meldungen", []),
            ("Testbar: wenn <code>https://jsonplaceholder.typicode.com</code> nicht erreichbar, Exit-Code 1", []),
        ],
        "akzeptanz": 'python api_poller.py\n# Konsole zeigt INFO-Meldungen\n\ncat poller.log | head -5\n# 2026-06-19 14:23:01 __main__ INFO API-Aufruf: /posts\n# 2026-06-19 14:23:01 __main__ DEBUG HTTP 200 in 0.34s\n\n# Datei beschädigen, dann:\npython api_poller.py\n# ERROR Cache-Datei korrupt — lade neu',
    },
    {
        "num": "11", "slug": "modul-11", "phase": "C", "phase_label": "Phase C — Praxis & Projekte",
        "accent": "#d2a8ff", "time": "5–7 h", "diff_n": 3, "diff_label": "Fortgeschritten",
        "prev": "modul-10", "next": "modul-12",
        "title": "Datenanalyse mit Pandas",
        "sheets": [("python", "python-cheatsheet")],
        "prereq": "Modul 07",
        "tagline": "DataFrames aus CSV, Excel und JSON laden. Filtern, Sortieren, Gruppieren. Fehlende Werte bereinigen. Berichte exportieren.",
        "lernziele": [
            "DataFrames mit <code>pd.read_csv()</code>, <code>read_excel()</code> und <code>read_json()</code> erstellen",
            "Zeilen und Spalten mit booleschen Filtern selektieren",
            "Daten mit <code>groupby()</code> aggregieren und auswerten",
            "Fehlende Werte mit <code>isna()</code>, <code>dropna()</code>, <code>fillna()</code> behandeln",
            "Duplikate mit <code>duplicated()</code> und <code>drop_duplicates()</code> entfernen",
            "Ergebnisse mit <code>to_csv()</code> und <code>to_excel()</code> exportieren",
        ],
        "hintergrund": """<p>Pandas ist das wichtigste Datenanalyse-Tool in Python. Auch wenn man kein Data Scientist ist, lohnt es sich: Serverinventare, Monitoring-Exports, CSV-Berichte aus Ticketsystemen — all das lässt sich mit wenigen Zeilen Pandas analysieren, was sonst Excel-Arbeit wäre.</p>
        <p>Der Einstieg ist zunächst ungewohnt, weil Pandas seine eigene API hat. Der Schlüssel: den DataFrame wie eine Tabellenkalkulation in Code denken. Eine Zeile ist ein Record, eine Spalte ist eine Series.</p>""",
        "konzepte": [
            ("DataFrame laden und inspizieren", 'import pandas as pd\n\ndf = pd.read_csv("server_inventory.csv")\nprint(df.shape)        # (Zeilen, Spalten)\nprint(df.dtypes)       # Datentypen je Spalte\nprint(df.head())       # erste 5 Zeilen\nprint(df.describe())   # Statistiken für numerische Spalten'),
            ("Filtern und Sortieren", 'high_cpu = df[df["cpu_usage"] > 80]\ncritical = df[(df["cpu_usage"] > 80) & (df["status"] == "production")]\n\ntop10 = df.sort_values("ram_gb", ascending=False).head(10)'),
            ("groupby Aggregation", 'by_role = df.groupby("role")["cpu_usage"].agg(["mean", "max", "count"])\nprint(by_role)\n\n# OS-Verteilung:\nos_counts = df["os"].value_counts()\nprint(os_counts)'),
        ],
        "aufgabe": """<p>Erstelle eine CSV-Datei <code>server_inventory.csv</code> mit mindestens 20 Zeilen und Spalten: <code>hostname, ip, os, role, cpu_cores, ram_gb, disk_tb, cpu_usage, status</code>. Schreibe dann <code>inventory_report.py</code>:</p>
        <ol>
          <li><code>load_inventory(path: Path) -&gt; pd.DataFrame</code>: lädt CSV, prüft auf fehlende Werte, gibt bereinigten DataFrame zurück</li>
          <li><code>high_utilization(df, threshold: float = 80.0) -&gt; pd.DataFrame</code>: Server mit CPU über Schwelle</li>
          <li><code>summary_by_role(df) -&gt; pd.DataFrame</code>: gruppiert nach Role, gibt mean/max CPU und Anzahl Server</li>
          <li><code>export_report(df, summary, path: Path) -&gt; None</code>: schreibt Excel mit zwei Sheets: "Alle Server" und "Nach Rolle"</li>
        </ol>""",
        "anforderungen": [
            ("CSV hat mindestens 20 Einträge mit unterschiedlichen Rollen und OS", []),
            ("<code>load_inventory</code> loggt Anzahl fehlender Werte und füllt sie mit sinnvollen Defaults", []),
            ("<code>summary_by_role</code> gibt DataFrame mit Index=role und Spalten mean_cpu, max_cpu, count zurück", []),
            ("Excel-Datei hat zwei Sheets mit korrekten Daten", []),
            ("<code>pip install pandas openpyxl</code> in requirements.txt vermerkt", []),
        ],
        "akzeptanz": 'python inventory_report.py\n# → report.xlsx erzeugt\n\n# Prüfen:\npython -c "\nimport pandas as pd\ndf = pd.read_excel(\'report.xlsx\', sheet_name=\'Nach Rolle\')\nprint(df.columns.tolist())\nassert \'mean_cpu\' in df.columns\nprint(\'OK\')\n"',
    },
    {
        "num": "12", "slug": "modul-12", "phase": "C", "phase_label": "Phase C — Praxis & Projekte",
        "accent": "#d2a8ff", "time": "4–6 h", "diff_n": 3, "diff_label": "Fortgeschritten",
        "prev": "modul-11", "next": "modul-13",
        "title": "Python & das Betriebssystem",
        "sheets": [("python", "python-cheatsheet"), ("bash", "bash-cheatsheet"), ("systemd", "systemd-cheatsheet")],
        "prereq": "Modul 06",
        "tagline": "Prozessmonitoring mit psutil. Systeminfos erfassen. Externe Befehle steuern. Umgebungsvariablen und Dateisystem verwalten.",
        "lernziele": [
            "CPU, RAM und Disk mit <code>psutil</code> auslesen",
            "Laufende Prozesse mit <code>psutil.process_iter()</code> inspizieren",
            "Netzwerkverbindungen und -statistiken abfragen",
            "Plattform-Details mit <code>platform</code>-Modul erfassen",
            "Umgebungsvariablen mit <code>os.environ</code> und <code>python-dotenv</code> verwalten",
            "Externe Befehle sicher ausführen und Output verarbeiten",
        ],
        "hintergrund": """<p><code>psutil</code> (process and system utilities) ist das Standard-Tool für Systeminformationen in Python. Es abstrahiert Linux-spezifische Interfaces (<code>/proc</code>) und funktioniert auf Windows und macOS identisch — ideal für plattformübergreifende Admin-Skripte.</p>
        <p>Vorsicht bei <code>subprocess</code>: Mit <code>shell=True</code> und User-Input entsteht eine Shell-Injection-Schwachstelle. Immer als Liste übergeben: <code>["systemctl", "status", service_name]</code> — dann ist <code>service_name</code> ein Argument, kein Shell-Code.</p>""",
        "konzepte": [
            ("Systemressourcen", 'import psutil\n\ncpu = psutil.cpu_percent(interval=1)  # Auslastung über 1 Sekunde\nram = psutil.virtual_memory()\ndisk = psutil.disk_usage("/")\n\nprint(f"CPU: {cpu}%")\nprint(f"RAM: {ram.used / 1e9:.1f} GB / {ram.total / 1e9:.1f} GB ({ram.percent}%)")\nprint(f"Disk: {disk.percent}% belegt")'),
            ("Prozesse filtern", 'import psutil\n\ndef find_process(name: str) -> list[dict]:\n    result = []\n    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_mb"]):\n        if name.lower() in proc.info["name"].lower():\n            result.append(proc.info)\n    return result'),
            ("Servicecheck via subprocess", 'import subprocess\n\ndef service_status(name: str) -> str:\n    result = subprocess.run(\n        ["systemctl", "is-active", name],\n        capture_output=True, text=True\n    )\n    return result.stdout.strip()  # "active", "inactive", "failed"'),
        ],
        "aufgabe": """<p>Schreibe <code>sysmon.py</code> — ein Monitoring-Skript, das:</p>
        <ol>
          <li>CPU, RAM, Disk und Netzwerk-IO sammelt (<code>psutil</code>)</li>
          <li>Die Top-5 Prozesse nach CPU-Auslastung ausgibt</li>
          <li>Systeminfos (Hostname, OS, Kernel, Python-Version) erfasst (<code>platform</code>)</li>
          <li>Den Status von <code>ssh</code>, <code>cron</code> und <code>systemd-resolved</code> prüft (<code>subprocess + systemctl</code>) — graceful degradieren auf nicht-systemd-Systemen</li>
          <li>Alle Daten als JSON-Snapshot in <code>snapshots/YYYY-MM-DD_HH-MM-SS.json</code> speichert</li>
          <li>CLI: <code>--interval N</code> wiederholt die Messung N Sekunden, <code>--once</code> für Einmalmessung</li>
        </ol>""",
        "anforderungen": [
            ("<code>psutil.cpu_percent(interval=1)</code> — nicht 0 (gibt immer 0.0)", []),
            ("Snapshot-Verzeichnis wird automatisch erstellt wenn nicht vorhanden", []),
            ("systemctl-Prüfung schlägt nicht fehl auf Systemen ohne systemd (z. B. macOS, WSL)", []),
            ("JSON-Snapshot ist valid JSON und enthält alle sechs Kategorien", []),
            ("<code>--interval</code>: zwischen Messungen <code>time.sleep(N)</code>, Ctrl+C sauber abgefangen", []),
        ],
        "akzeptanz": 'python sysmon.py --once\n# → Ausgabe aller Metriken\n# → snapshots/2026-06-19_14-30-00.json erzeugt\n\npython -c "import json; d=json.load(open(\'snapshots/$(ls snapshots | tail -1)\')); print(list(d.keys()))"\n# [\'system\', \'cpu\', \'ram\', \'disk\', \'network\', \'services\', \'top_procs\']',
    },
    {
        "num": "13", "slug": "modul-13", "phase": "C", "phase_label": "Phase C — Praxis & Projekte",
        "accent": "#d2a8ff", "time": "5–7 h", "diff_n": 3, "diff_label": "Fortgeschritten",
        "prev": "modul-12", "next": "modul-14",
        "title": "Logdateien & Monitoringdaten analysieren",
        "sheets": [("python", "python-cheatsheet"), ("regex", "regex-cheatsheet"), ("bash", "bash-cheatsheet")],
        "prereq": "Modul 07, Modul 10",
        "tagline": "Apache/Nginx-Logs mit Regex parsen. Stundenbezogene Statistiken. Schwellenwerte überwachen. Berichte und Alarme.",
        "lernziele": [
            "Reguläre Ausdrücke mit <code>re.compile()</code> und <code>re.match()</code>/<code>re.search()</code> einsetzen",
            "Apache/Nginx-Logformat mit Regex-Gruppen parsen",
            "Häufigkeiten mit <code>collections.Counter</code> effizient zählen",
            "Zeitstempel aus Logs parsen und in <code>datetime</code>-Objekte umwandeln",
            "Stundenbezogene Statistiken berechnen",
            "Alarme bei Schwellenwertüberschreitung auslösen",
        ],
        "hintergrund": """<p>Logs sind strukturierte Daten im Plaintext-Format. Apache und Nginx nutzen das Combined Log Format — ein bekanntes Muster, das sich gut mit einem einzigen regulären Ausdruck parsen lässt. Der Schlüssel: <code>re.compile()</code> einmal außerhalb der Schleife aufrufen, nicht bei jedem Aufruf.</p>
        <p><code>collections.Counter</code> ist für Häufigkeitszählungen optimiert und bietet <code>.most_common(N)</code> direkt an — kein manuelles Dict-Befüllen und Sortieren nötig.</p>""",
        "konzepte": [
            ("Apache Combined Log Format Regex", 'import re\n\nLOG_PATTERN = re.compile(\n    r\'(?P<ip>\\S+) \\S+ \\S+ \\[(?P<time>[^\\]]+)\\] \'\n    r\'"(?P<method>\\S+) (?P<path>\\S+) \\S+" \'\n    r\'(?P<status>\\d{3}) (?P<size>\\d+|-)\'\n)\n\ndef parse_line(line: str) -> dict | None:\n    m = LOG_PATTERN.match(line)\n    return m.groupdict() if m else None'),
            ("Counter für Häufigkeiten", 'from collections import Counter\n\ndef top_ips(log_path: str, n: int = 10) -> list[tuple[str, int]]:\n    counter: Counter[str] = Counter()\n    with open(log_path) as f:\n        for line in f:\n            entry = parse_line(line)\n            if entry:\n                counter[entry["ip"]] += 1\n    return counter.most_common(n)'),
            ("Schwellenwert-Alarm", 'def check_error_rate(entries: list[dict], threshold: float = 0.05) -> bool:\n    total = len(entries)\n    errors = sum(1 for e in entries if e["status"].startswith("5"))\n    rate = errors / total if total else 0\n    if rate > threshold:\n        logger.warning("Error-Rate %.1f%% überschreitet Schwelle %.1f%%", rate*100, threshold*100)\n        return True\n    return False'),
        ],
        "aufgabe": """<p>Erstelle eine realistische Beispiel-Logdatei <code>access.log</code> mit mindestens 500 Zeilen im Apache Combined Log Format. Schreibe dann <code>log_analyzer.py</code>:</p>
        <ol>
          <li><code>parse_log(path: Path) -&gt; list[dict]</code>: parst alle Zeilen, überspringt fehlerhafte</li>
          <li><code>requests_per_hour(entries: list[dict]) -&gt; dict[int, int]</code>: Anfragen je Stunde (0–23)</li>
          <li><code>top_paths(entries, n=10) -&gt; list[tuple[str, int]]</code>: meistangeforderte URLs</li>
          <li><code>error_summary(entries) -&gt; dict[str, int]</code>: Anzahl je HTTP-Status (200, 404, 500, ...)</li>
          <li><code>generate_report(path: Path, out: Path) -&gt; None</code>: schreibt Textbericht</li>
          <li>CLI: <code>--top N</code> (Default 10), <code>--warn-errors PROZENT</code> (Default 5.0)</li>
        </ol>""",
        "anforderungen": [
            ("Beispiel-Logdatei vorhanden, mindestens 500 Zeilen, diverse IPs/Status-Codes/Pfade", []),
            ("<code>re.compile()</code> außerhalb der Parse-Schleife", []),
            ("Zeitstempel korrekt als <code>datetime</code> geparst: <code>strptime(..., '%d/%b/%Y:%H:%M:%S %z')</code>", []),
            ("Fehlerhafte Zeilen zählen und am Ende als INFO loggen", []),
            ("Bericht enthält: Gesamtanfragen, Zeitraum, Top-IPs, Top-Paths, Status-Verteilung, Error-Rate", []),
        ],
        "akzeptanz": 'python log_analyzer.py access.log --top 5\n\n# Ausgabe enthält:\n# Gesamt: 523 Anfragen (2026-01-01 bis 2026-01-31)\n# Top-5 Pfade:\n#   1. /api/status   (142)\n#   ...\n# Status-Verteilung:\n#   200: 412  404: 67  500: 44\n# Error-Rate: 8.4% — WARNING: über Schwelle (5.0%)',
    },
    {
        "num": "14", "slug": "modul-14", "phase": "C", "phase_label": "Phase C — Praxis & Projekte",
        "accent": "#d2a8ff", "time": "6–10 h", "diff_n": 4, "diff_label": "Erfahren",
        "prev": "modul-13", "next": None,
        "title": "Praxisprojekte: CLI-Tools",
        "sheets": [("python", "python-cheatsheet"), ("bash", "bash-cheatsheet"), ("json", "json-cheatsheet")],
        "prereq": "Modul 10, Modul 12, Modul 13",
        "tagline": "Vollständiges admin-toolkit CLI mit drei Subcommands. Alle Konzepte aus den Modulen 01–13 integriert.",
        "lernziele": [
            "Ein vollständiges CLI-Projekt mit mehreren Modulen aufbauen",
            "Alle bisher gelernten Konzepte (OOP, Logging, Fehlerbehandlung, APIs, Dateien) kombinieren",
            "Saubere Projektstruktur mit <code>__main__.py</code> für <code>python -m toolkit</code>",
            "Exit-Codes konsequent für Skript-Verkettung einsetzen",
            "Konfiguration über <code>.env</code> und CLI-Argumente kombinieren",
            "Das Tool dokumentieren und ein einfaches <code>--help</code> bereitstellen",
        ],
        "hintergrund": """<p>Dieses Modul ist das Capstone des Kurses: Hier werden alle 13 vorherigen Module integriert. Ein echtes CLI-Tool für den Admin-Alltag bauen — das ist das Ziel von Anfang an gewesen.</p>
        <p>Guter Admin-Code läuft unbeaufsichtigt. Das bedeutet: Exit-Codes für Shell-Verkettung (<code>&amp;&amp;</code>, <code>||</code>), Logging in Dateien statt <code>print()</code>, saubere Fehlerbehandlung ohne Stack-Traces auf der Konsole, Timeout bei Netzwerkoperationen.</p>""",
        "konzepte": [
            ("Projektstruktur mit __main__.py", 'admin-toolkit/\n├── .env\n├── .gitignore         ← enthält .env\n├── requirements.txt\n├── toolkit/\n│   ├── __init__.py\n│   ├── __main__.py    ← python -m toolkit\n│   ├── cli.py         ← argparse-Setup\n│   ├── inventory.py\n│   ├── monitor.py\n│   └── report.py\n└── tests/'),
            ("__main__.py Muster", 'import sys\nfrom toolkit.cli import build_parser\nfrom toolkit import inventory, monitor, report\n\ndef main() -> int:\n    parser = build_parser()\n    args = parser.parse_args()\n    if args.cmd is None:\n        parser.print_help()\n        return 2\n    return args.func(args)  # jeder Subparser setzt args.func\n\nif __name__ == "__main__":\n    sys.exit(main())'),
            ("Subcommand-Dispatch", '# In cli.py:\ninv_p = sub.add_parser("inventory", help="Systeminventar als JSON")\ninv_p.add_argument("--output", "-o", default="inventory.json")\ninv_p.set_defaults(func=inventory.run)\n\nmon_p = sub.add_parser("monitor", help="URL auf Verfügbarkeit prüfen")\nmon_p.add_argument("url")\nmon_p.add_argument("--interval", type=int, default=60)\nmon_p.set_defaults(func=monitor.run)'),
        ],
        "aufgabe": """<p>Baue <code>admin-toolkit</code> mit drei Subcommands. Jeder muss <code>int</code> zurückgeben (0 = OK, 1 = Fehler).</p>
        <p><strong><code>toolkit inventory [--output FILE]</code></strong></p>
        <ul><li>Erfasst: Hostname, OS, CPU-Kerne, RAM, Disk, Python-Version, laufende Prozesse (Top-5 CPU), Netzwerk-IPs</li><li>Speichert als JSON in <code>--output</code> (Default: <code>inventory.json</code>)</li></ul>
        <p><strong><code>toolkit monitor URL [--interval N] [--log FILE]</code></strong></p>
        <ul><li>Prüft URL alle N Sekunden (Default: 60), misst Antwortzeit</li><li>Loggt Ergebnis (OK/FAIL + Antwortzeit) als CSV in <code>--log</code> (Default: <code>monitor.csv</code>)</li><li>Ctrl+C beendet sauber mit Zusammenfassung</li></ul>
        <p><strong><code>toolkit report CSV [--format text|json]</code></strong></p>
        <ul><li>Liest <code>monitor.csv</code>, berechnet: Uptime-%, mittlere Antwortzeit, Ausfallzeiten</li><li>Ausgabe als Textbericht oder JSON (<code>--format</code>)</li></ul>""",
        "anforderungen": [
            ("Alle drei Subcommands implementiert mit korrekten Exit-Codes", []),
            ("<code>python -m toolkit --help</code> zeigt alle Subcommands", []),
            ("<code>inventory.json</code> ist valid JSON mit allen geforderten Feldern", []),
            ("<code>monitor</code>: Ctrl+C gibt Zusammenfassung aus (N checks, X OK, Y FAIL)", []),
            ("<code>report</code>: Uptime-% korrekt berechnet; bei leerem CSV Exit-Code 1 + Fehlermeldung", []),
            ("Logging in Datei <code>toolkit.log</code> (DEBUG), Konsole (INFO) — keine unbehandelten Exceptions", []),
            ("<code>.gitignore</code> enthält <code>.env</code>, <code>*.log</code>, <code>__pycache__/</code>, <code>.venv/</code>", []),
        ],
        "akzeptanz": 'python -m toolkit inventory\n# → inventory.json erzeugt\n\npython -m toolkit monitor https://example.com --interval 5\n# → alle 5s: 2026-06-19 14:30:05, OK, 0.234s\n# (Ctrl+C) → Zusammenfassung: 4/4 OK, ø 0.218s\n\npython -m toolkit report monitor.csv\n# Uptime: 100.0% | Ø 0.218s | 0 Ausfälle\n\npython -m toolkit report monitor.csv --format json\n# {"uptime_pct": 100.0, "avg_response_s": 0.218, "failures": 0}',
    },
]


CSS_COMMON = """  :root {
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #7d8590; --code-bg: #10161d;
    --accent: {accent};
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: 'Syne', sans-serif; min-height: 100vh; }

  .topnav {
    padding: 0 48px; height: 46px; border-bottom: 1px solid var(--border);
    background: var(--bg); position: sticky; top: 0; z-index: 100;
    display: flex; align-items: center; gap: 8px;
  }
  .nav-back { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); text-decoration: none; transition: color 0.15s; }
  .nav-back:hover { color: var(--text); }
  .nav-sep { color: var(--border); font-size: 18px; }
  .nav-crumb { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--accent); }

  header {
    border-bottom: 2px solid var(--accent); padding: 40px 48px 32px;
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #0d1117 0%, #0d1420 60%, #0d1117 100%);
  }
  header::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 700px 250px at 65% 50%, color-mix(in srgb, var(--accent) 8%, transparent), transparent);
  }
  .header-grid { display: grid; grid-template-columns: 1fr auto; align-items: start; gap: 32px; position: relative; max-width: 1240px; }
  .badge-row { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }
  .badge { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 3px 10px; border-radius: 3px; }
  .badge-mod { color: var(--accent); background: color-mix(in srgb, var(--accent) 10%, transparent); border: 1px solid color-mix(in srgb, var(--accent) 30%, transparent); }
  .badge-phase { color: var(--muted); background: rgba(255,255,255,0.04); border: 1px solid var(--border); }
  .badge-time { color: var(--muted); background: rgba(255,255,255,0.04); border: 1px solid var(--border); }
  h1 { font-size: clamp(24px, 3.5vw, 44px); font-weight: 800; letter-spacing: -1px; line-height: 1.1; color: var(--text); margin-bottom: 12px; }
  .header-meta { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--muted); line-height: 2; }
  .header-meta span { color: var(--text); }

  .sheets-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 18px; min-width: 180px; }
  .sheets-label { font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-bottom: 12px; }
  .sheet-lnk { display: flex; align-items: center; gap: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: var(--muted); text-decoration: none; padding: 5px 0; border-bottom: 1px solid var(--border); transition: color 0.15s; }
  .sheet-lnk:last-child { border-bottom: none; }
  .sheet-lnk::before { content: '→'; color: var(--accent); opacity: 0.5; transition: opacity 0.15s; }
  .sheet-lnk:hover { color: var(--accent); }
  .sheet-lnk:hover::before { opacity: 1; }

  .page-body { display: grid; grid-template-columns: 1fr 220px; gap: 40px; max-width: 1240px; margin: 0 auto; padding: 48px; align-items: start; }
  .content { min-width: 0; }

  .lab-section { margin-bottom: 44px; }
  .sec-heading { font-size: 14px; font-weight: 700; letter-spacing: 0.5px; color: var(--accent); padding-bottom: 8px; margin-bottom: 18px; border-bottom: 1px solid color-mix(in srgb, var(--accent) 20%, transparent); }
  h3 { font-size: 13px; font-weight: 700; color: var(--text); margin: 18px 0 10px; }
  p { font-size: 13.5px; line-height: 1.75; color: #c9d1d9; margin-bottom: 10px; }
  ul, ol { list-style: none; padding: 0; margin-bottom: 14px; }
  li { font-size: 13.5px; line-height: 1.7; color: #c9d1d9; padding: 3px 0 3px 20px; position: relative; }
  li::before { content: '·'; position: absolute; left: 6px; color: var(--accent); opacity: 0.7; }
  ol { counter-reset: item; }
  ol li { counter-increment: item; }
  ol li::before { content: counter(item) '.'; font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; left: 0; color: var(--accent); }
  li.task { padding-left: 26px; }
  li.task::before { display: none; }
  .chk { display: inline-block; width: 14px; height: 14px; border: 1.5px solid color-mix(in srgb, var(--accent) 40%, transparent); border-radius: 3px; background: color-mix(in srgb, var(--accent) 6%, transparent); position: absolute; left: 0; top: 6px; }
  code { font-family: 'JetBrains Mono', monospace; font-size: 12px; background: var(--code-bg); border: 1px solid var(--border); padding: 1px 5px; border-radius: 3px; color: #e6edf3; }
  pre { background: var(--code-bg); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: 6px; padding: 18px 20px; overflow-x: auto; margin: 14px 0; }
  pre code { background: none; border: none; padding: 0; font-size: 12.5px; line-height: 1.65; }
  blockquote { border-left: 3px solid var(--accent); padding: 12px 16px; background: color-mix(in srgb, var(--accent) 6%, transparent); border-radius: 0 6px 6px 0; margin: 14px 0; }
  blockquote p { margin: 0; font-size: 13px; color: var(--muted); }

  .sidebar { position: sticky; top: 60px; }
  .sidebar-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 14px; }
  .sidebar-lbl { font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); margin-bottom: 12px; }
  .toc-lnk { display: block; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); text-decoration: none; padding: 5px 0; border-bottom: 1px solid var(--border); transition: color 0.15s; }
  .toc-lnk:last-child { border-bottom: none; }
  .toc-lnk:hover { color: var(--accent); }
  .nav-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; }
  .nav-mod-link { display: block; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-decoration: none; padding: 5px 0; color: var(--muted); border-bottom: 1px solid var(--border); transition: color 0.15s; }
  .nav-mod-link:last-child { border-bottom: none; }
  .nav-mod-link:hover { color: var(--accent); }
  .nav-mod-link.prev::before { content: '← '; }
  .nav-mod-link.next::after { content: ' →'; }

  @media (max-width: 900px) {
    .page-body { grid-template-columns: 1fr; padding: 32px 24px; }
    .header-grid { grid-template-columns: 1fr; }
    .sidebar, .sheets-panel { display: none; }
    .topnav, header { padding-left: 24px; padding-right: 24px; }
  }"""


def stars(n: int) -> str:
    on = '<span style="color:#e3b341">★</span>'
    off = '<span style="color:#30363d">★</span>'
    return "".join([on] * n + [off] * (5 - n))


def diff_badge(n: int, label: str, accent: str) -> str:
    return (
        f'<span class="badge" style="color:{accent};background:rgba(0,0,0,0);'
        f'border:1px solid {accent}88;font-size:11px;letter-spacing:0.5px">'
        f'{stars(n)} {label}</span>'
    )


def konzept_blocks(konzepte: list) -> str:
    blocks = []
    for title, code in konzepte:
        blocks.append(
            f'        <h3>{title}</h3>\n'
            f'        <pre><code>{code}</code></pre>'
        )
    return "\n".join(blocks)


def lernziele_html(items: list) -> str:
    return "\n".join(f"          <li>{item}</li>" for item in items)


def anforderungen_html(items: list) -> str:
    parts = []
    for text, sub in items:
        parts.append(f'          <li class="task"><span class="chk"></span>{text}')
        if sub:
            parts.append("            <ul>")
            for s in sub:
                parts.append(f"              <li>{s}</li>")
            parts.append("            </ul>")
        parts.append("          </li>")
    return "\n".join(parts)


def sheets_html(sheets: list) -> str:
    return "\n".join(
        f'        <a href="{CHEATSHEET_BASE}{slug}.html" class="sheet-lnk">{label}</a>'
        for label, slug in sheets
    )


def nav_links(mod: dict) -> str:
    lines = []
    if mod["prev"]:
        lines.append(f'<a href="{mod["prev"]}.html" class="nav-mod-link prev">{mod["prev"].replace("modul-", "Modul ")}</a>')
    if mod["next"]:
        lines.append(f'<a href="{mod["next"]}.html" class="nav-mod-link next">{mod["next"].replace("modul-", "Modul ")}</a>')
    return "\n        ".join(lines)


def render(mod: dict) -> str:
    css = CSS_COMMON.replace("{accent}", mod["accent"])
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Modul {mod['num']} — {mod['title']} - TheLayer0Guide</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;800&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
  <nav class="topnav">
    <a href="../../index.html" class="nav-back">← Labs</a>
    <span class="nav-sep">/</span>
    <a href="../catalog.html" class="nav-back">Python für Anfänger</a>
    <span class="nav-sep">/</span>
    <span class="nav-crumb">Modul {mod['num']} — {mod['title']}</span>
  </nav>
  <header>
    <div class="header-grid">
      <div>
        <div class="badge-row">
          <span class="badge badge-mod">Modul {mod['num']}</span>
          <span class="badge badge-phase">{mod['phase_label']}</span>
          <span class="badge badge-time">{mod['time']}</span>
          {diff_badge(mod['diff_n'], mod['diff_label'], mod['accent'])}
        </div>
        <h1>{mod['title']}</h1>
        <div class="header-meta">
          Voraussetzungen: <span>{mod['prereq']}</span>
        </div>
      </div>
      <div class="sheets-panel">
        <div class="sheets-label">Cheat Sheets</div>
        {sheets_html(mod['sheets'])}
      </div>
    </div>
  </header>
  <div class="page-body">
    <div class="content">

      <div class="lab-section" id="lernziele">
        <div class="sec-heading">Lernziele</div>
        <ul>
{lernziele_html(mod['lernziele'])}
        </ul>
      </div>

      <div class="lab-section" id="hintergrund">
        <div class="sec-heading">Hintergrund</div>
        {mod['hintergrund']}
      </div>

      <div class="lab-section" id="konzepte">
        <div class="sec-heading">Schlüsselkonzepte</div>
{konzept_blocks(mod['konzepte'])}
      </div>

      <div class="lab-section" id="aufgabe">
        <div class="sec-heading">Aufgabe</div>
        {mod['aufgabe']}
      </div>

      <div class="lab-section" id="anforderungen">
        <div class="sec-heading">Anforderungen (Pflicht)</div>
        <ul>
{anforderungen_html(mod['anforderungen'])}
        </ul>
      </div>

      <div class="lab-section" id="akzeptanz">
        <div class="sec-heading">Akzeptanzkriterien</div>
        <pre><code>{mod['akzeptanz']}</code></pre>
      </div>

    </div>
    <div class="sidebar">
      <div class="sidebar-card">
        <div class="sidebar-lbl">Inhalt</div>
        <a href="#lernziele" class="toc-lnk">Lernziele</a>
        <a href="#hintergrund" class="toc-lnk">Hintergrund</a>
        <a href="#konzepte" class="toc-lnk">Konzepte</a>
        <a href="#aufgabe" class="toc-lnk">Aufgabe</a>
        <a href="#anforderungen" class="toc-lnk">Anforderungen</a>
        <a href="#akzeptanz" class="toc-lnk">Akzeptanz</a>
      </div>
      <div class="nav-card">
        <div class="sidebar-lbl">Navigation</div>
        {nav_links(mod)}
      </div>
      <div class="sidebar-card">
        <div class="sidebar-lbl">Kurs</div>
        <a href="../catalog.html" class="toc-lnk">← Übersicht</a>
        <a href="../../index.html" class="toc-lnk">← Alle Labs</a>
      </div>
    </div>
  </div>
</body>
</html>"""


if __name__ == "__main__":
    for mod in MODULES:
        path = OUT / f"{mod['slug']}.html"
        path.write_text(render(mod), encoding="utf-8")
        print(f"  ✓ {path.name}")
    print(f"Done — {len(MODULES)} module pages generated in {OUT}")
