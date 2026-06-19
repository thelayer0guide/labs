# Modul 05 — OOP: Klassen & Dataclasses

[← Modul 04](modul-04.md) | [Übersicht](catalog.md) | [Modul 06 →](modul-06.md)

---

**Phase:** Phase B — Werkzeuge & Daten
**Zeitaufwand:** 4–6 h
**Schwierigkeit:** ★★★☆☆ Fortgeschritten
**Voraussetzungen:** Modul 04

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)

---

## Lernziele

- Klassen mit `__init__`, Attributen und Methoden definieren
- `__repr__` und `__str__` für lesbare Objektdarstellung implementieren
- `@dataclass` für kompakte Datenobjekte einsetzen
- Mutable Default-Werte mit `field(default_factory=...)` korrekt handhaben
- `frozen=True` für unveränderliche Konfigurationsobjekte nutzen
- Entscheidungskriterien: Wann Klasse, wann Dict, wann Dataclass?

---

## Hintergrund

OOP ist in Python kein Pflichtparadigma — Funktionen und Dicts lösen viele Probleme eleganter. Klassen werden sinnvoll, wenn Daten und die dazugehörige Logik zusammen verwaltet werden müssen und das Objekt einen Zustand hat, der sich über mehrere Operationen verändert.

`@dataclass` (Python 3.7+) ist der Sweet Spot für reine Datenobjekte: Es generiert automatisch `__init__`, `__repr__` und `__eq__`, ohne Boilerplate. Für Konfigurationsobjekte, API-Antworten und DTOs ist es die erste Wahl.

---

## Schlüsselkonzepte

### Klasse mit Zustand

```python
class Server:
    def __init__(self, hostname: str, ip: str) -> None:
        self.hostname = hostname
        self.ip = ip
        self.online: bool = False

    def start(self) -> None:
        self.online = True

    def __repr__(self) -> str:
        status = "online" if self.online else "offline"
        return f"Server({self.hostname!r}, {status})"
```

### @dataclass

```python
from dataclasses import dataclass, field

@dataclass
class LogEntry:
    level: str
    service: str
    message: str
    tags: list[str] = field(default_factory=list)

    def is_error(self) -> bool:
        return self.level == "ERROR"
```

### frozen Dataclass

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class DBConfig:
    host: str
    port: int = 5432
    database: str = "prod"

# Unveränderlich — wirft FrozenInstanceError bei Zuweisung
cfg = DBConfig(host="db.intern")
print(cfg.host, cfg.port)
```

---

## Aufgabe

Modelliere eine Server-Verwaltung mit zwei Klassen:

**1. `@dataclass class ServerConfig`** (frozen): host, port, os, role (web/db/cache)

**2. `class Server`**: Nimmt eine `ServerConfig` im Konstruktor, verwaltet Zustand (`online`, `error_count`) und hat Methoden:

**3. `class ServerPool`**: Verwaltet eine Liste von Servern, bietet `add()`, `all_online()`, `servers_by_role(role)`, `summary()`.

- `ping(self) -> bool` — simuliert Ping (gibt bei online=True immer True zurück)
- `record_error(self, msg: str) -> None` — erhöht error_count, speichert letzte Fehlermeldung
- `status_report(self) -> dict` — gibt dict mit allen Infos zurück

---

## Anforderungen

- [ ] `ServerConfig` ist frozen — Zuweisung nach Erstellung wirft Exception
- [ ] `Server` speichert letzten Fehler als Instanzattribut
- [ ] `ServerPool.summary()` gibt Gesamtzahl, Anzahl online, Anzahl mit Fehlern zurück
- [ ] `servers_by_role('web')` filtert korrekt
- [ ] Kein globaler State — alle Daten leben in Instanzattributen

---

## Akzeptanzkriterien

```
pool = ServerPool()
pool.add(Server(ServerConfig('web01', 8080, 'Ubuntu 24', 'web')))
pool.add(Server(ServerConfig('db01', 5432, 'Debian 12', 'db')))
pool.servers[0].online = True
pool.servers[1].record_error('connection refused')

print(pool.summary())
# {'total': 2, 'online': 1, 'with_errors': 1}

print(pool.servers_by_role('web'))
# [Server(web01, online)]
```

---

[← Modul 04](modul-04.md) | [Übersicht](catalog.md) | [Modul 06 →](modul-06.md)
