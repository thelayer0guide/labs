# Modul 11 — Datenanalyse mit Pandas

[← Modul 10](modul-10.md) | [Übersicht](catalog.md) | [Modul 12 →](modul-12.md)

---

**Phase:** Phase C — Praxis & Projekte
**Zeitaufwand:** 5–7 h
**Schwierigkeit:** ★★★☆☆ Fortgeschritten
**Voraussetzungen:** Modul 07

## Cheat Sheets

- [python](https://thelayer0guide.github.io/cheat-sheets/sheets/python-cheatsheet.html)

---

## Lernziele

- DataFrames mit `pd.read_csv()`, `read_excel()` und `read_json()` erstellen
- Zeilen und Spalten mit booleschen Filtern selektieren
- Daten mit `groupby()` aggregieren und auswerten
- Fehlende Werte mit `isna()`, `dropna()`, `fillna()` behandeln
- Duplikate mit `duplicated()` und `drop_duplicates()` entfernen
- Ergebnisse mit `to_csv()` und `to_excel()` exportieren

---

## Hintergrund

Pandas ist das wichtigste Datenanalyse-Tool in Python. Auch wenn man kein Data Scientist ist, lohnt es sich: Serverinventare, Monitoring-Exports, CSV-Berichte aus Ticketsystemen — all das lässt sich mit wenigen Zeilen Pandas analysieren, was sonst Excel-Arbeit wäre.

Der Einstieg ist zunächst ungewohnt, weil Pandas seine eigene API hat. Der Schlüssel: den DataFrame wie eine Tabellenkalkulation in Code denken. Eine Zeile ist ein Record, eine Spalte ist eine Series.

---

## Schlüsselkonzepte

### DataFrame laden und inspizieren

```python
import pandas as pd

df = pd.read_csv("server_inventory.csv")
print(df.shape)        # (Zeilen, Spalten)
print(df.dtypes)       # Datentypen je Spalte
print(df.head())       # erste 5 Zeilen
print(df.describe())   # Statistiken für numerische Spalten
```

### Filtern und Sortieren

```python
high_cpu = df[df["cpu_usage"] > 80]
critical = df[(df["cpu_usage"] > 80) & (df["status"] == "production")]

top10 = df.sort_values("ram_gb", ascending=False).head(10)
```

### groupby Aggregation

```python
by_role = df.groupby("role")["cpu_usage"].agg(["mean", "max", "count"])
print(by_role)

# OS-Verteilung:
os_counts = df["os"].value_counts()
print(os_counts)
```

---

## Aufgabe

Erstelle eine CSV-Datei `server_inventory.csv` mit mindestens 20 Zeilen und Spalten: `hostname, ip, os, role, cpu_cores, ram_gb, disk_tb, cpu_usage, status`. Schreibe dann `inventory_report.py`:

1. `load_inventory(path: Path) -> pd.DataFrame`: lädt CSV, prüft auf fehlende Werte, gibt bereinigten DataFrame zurück
2. `high_utilization(df, threshold: float = 80.0) -> pd.DataFrame`: Server mit CPU über Schwelle
3. `summary_by_role(df) -> pd.DataFrame`: gruppiert nach Role, gibt mean/max CPU und Anzahl Server
4. `export_report(df, summary, path: Path) -> None`: schreibt Excel mit zwei Sheets: "Alle Server" und "Nach Rolle"

---

## Anforderungen

- [ ] CSV hat mindestens 20 Einträge mit unterschiedlichen Rollen und OS
- [ ] `load_inventory` loggt Anzahl fehlender Werte und füllt sie mit sinnvollen Defaults
- [ ] `summary_by_role` gibt DataFrame mit Index=role und Spalten mean_cpu, max_cpu, count zurück
- [ ] Excel-Datei hat zwei Sheets mit korrekten Daten
- [ ] `pip install pandas openpyxl` in requirements.txt vermerkt

---

## Akzeptanzkriterien

```
python inventory_report.py
# → report.xlsx erzeugt

# Prüfen:
python -c "
import pandas as pd
df = pd.read_excel('report.xlsx', sheet_name='Nach Rolle')
print(df.columns.tolist())
assert 'mean_cpu' in df.columns
print('OK')
"
```

---

[← Modul 10](modul-10.md) | [Übersicht](catalog.md) | [Modul 12 →](modul-12.md)
