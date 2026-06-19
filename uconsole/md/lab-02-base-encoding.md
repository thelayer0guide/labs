# Lab 02 — Base Encoding Toolkit

> **Phase 1 — Daten & Dateien**
> Voraussetzungen: Lab 01 (Projektstruktur)
> Geschätzte Zeit: 3–5 Stunden

---

## Lernziele

- Den Unterschied zwischen `str` (Unicode) und `bytes` (Rohdaten) wirklich verstehen
- `base64`, `base32`, `binascii` und `urllib.parse` aus der Stdlib anwenden
- Robuste Fehlermeldungen bei ungültigem Input produzieren
- `@pytest.mark.parametrize` für tabellengestützte Tests einsetzen
- Das Konzept von Encoding-Ketten (Pipelines) verstehen

---

## Hintergrund

Base64, Hex und URL-Encoding begegnen dir täglich: in HTTP-Headern, JWT-Tokens, Dateiübertragungen, CTF-Challenges und forensischen Analysen. Der entscheidende Unterschied zu einfachem Text: Du arbeitest mit Bytes, nicht mit Strings — und dieser Unterschied hat in Python 3 konkrete Konsequenzen.

Dieses Lab ist auch dein erster echter Einstieg in systematisches Testen: Die Kernlogik ist reine Transformation (Input → Output), ideal für parametrisierte Tests mit Dutzenden von Testfällen.

---

## Aufgabe

Implementiere `enc` — ein CLI-Tool für Encoding und Decoding verschiedener Formate, sowohl für Strings als auch für Binärdateien.

### Projektstruktur

```
security-lab/
└── encodingtool/
    ├── __init__.py
    ├── core.py
    ├── cli.py
    └── tests/
        ├── __init__.py
        └── test_core.py
```

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `encode(data: bytes, fmt: str) -> bytes`
  - Unterstützte Formate: `base64`, `base32`, `hex`, `url`
  - `base64`: Standard Base64 (`+/=`), Output als ASCII-Bytes
  - `base32`: Standard Base32 mit Padding
  - `hex`: Lowercase Hex-Darstellung (`deadbeef`, nicht `DEADBEEF`)
  - `url`: URL-Encoding (Leerzeichen → `%20`, nicht `+`)
  - Wirft `ValueError` bei unbekanntem Format

- [ ] Funktion `decode(data: bytes, fmt: str) -> bytes`
  - Inverse Operationen zu `encode`
  - Bei `base64`: toleriert fehlendes Padding (füge es intern hinzu)
  - Bei `hex`: akzeptiert sowohl Groß- als auch Kleinbuchstaben
  - Wirft `ValueError` bei ungültigem Input (fehlerhaftes Padding, ungültige Zeichen)
  - Fehlermeldung muss konkret sein: nicht nur "invalid" sondern z. B. "ungültiges Base64: Länge 5 ist nicht durch 4 teilbar"

- [ ] Funktion `detect_encoding(data: bytes) -> str | None`
  - Heuristik: Versuche zu erkennen, welches Format vorliegt
  - Prüft: Zeichensatz, Länge/Padding, Präfixe
  - Gibt das wahrscheinlichste Format zurück oder `None` wenn unklar
  - Muss keine 100%-Trefferquote haben — aber für eindeutige Fälle (reines Hex, klares Base64) korrekt sein

### cli.py

- [ ] `enc encode [--format FORMAT] TEXT_ODER_STDIN`
- [ ] `enc decode [--format FORMAT] [--auto] TEXT_ODER_STDIN`
  - `--auto`: versucht Format automatisch zu erkennen (nutzt `detect_encoding`)
- [ ] `enc encode --file DATEI --format base64`: liest Binärdatei, gibt Base64 aus
- [ ] `enc decode --file DATEI --format hex --out ausgabe.bin`: dekodiert in Datei
- [ ] Wenn kein Argument übergeben: liest von `stdin` (Pipeline-freundlich)

---

## CLI-Schnittstelle (vollständig)

```
enc encode --format base64 "Hello, World!"
enc decode --format base64 "SGVsbG8sIFdvcmxkIQ=="
enc encode --format hex --file bild.png
enc decode --format hex "48656c6c6f"
enc decode --auto "SGVsbG8="
enc encode --format url "hello world & more"
enc encode --format base64,hex "hello"   (Bonus: Ketten)
```

Beispiel-Output:
```
$ enc encode --format base64 "Hello"
SGVsbG8=

$ enc decode --format base64 "SGVsbG8="
Hello

$ enc decode --auto "48656c6c6f"
[hex erkannt]
Hello
```

---

## Akzeptanzkriterien

```bash
# Roundtrip: encode dann decode muss original ergeben
python -c "
from encodingtool.core import encode, decode
original = b'Test \x00\x01\x02 binary data'
for fmt in ['base64', 'base32', 'hex']:
    assert decode(encode(original, fmt), fmt) == original, f'Roundtrip failed: {fmt}'
print('Alle Roundtrips OK')
"

# Fehlerbehandlung
python -c "
from encodingtool.core import decode
try:
    decode(b'!!!not-valid-base64!!!', 'base64')
    assert False, 'Hätte ValueError werfen müssen'
except ValueError as e:
    print(f'OK: {e}')
"

# CLI-Pipeline
echo "Hello World" | python -m encodingtool encode --format base64 | \
  python -m encodingtool decode --format base64
# → Hello World
```

---

## Tests (Anforderungen an test_core.py)

Nutze `@pytest.mark.parametrize` für alle Roundtrip-Tests:

- [ ] Parametrisierter Roundtrip-Test: mindestens 5 verschiedene Inputs × alle Formate
  - Leerer String `b""`
  - Reiner ASCII-Text `b"Hello, World!"`
  - Binärdaten mit Nullbytes `b"\x00\x01\x02\x03"`
  - Alle 256 Byte-Werte `bytes(range(256))`
  - Langer Text (>1000 Zeichen)
- [ ] Test: `decode` mit ungültigem Base64 → `ValueError`
- [ ] Test: `decode` mit ungültigem Hex (ungerade Länge) → `ValueError`
- [ ] Test: `decode` akzeptiert Base64 ohne Padding-`=`
- [ ] Test: `encode` mit unbekanntem Format → `ValueError`
- [ ] Test: `detect_encoding` erkennt klares Base64 korrekt
- [ ] Test: `detect_encoding` erkennt reines Hex korrekt

---

## Bonus-Aufgaben

- [ ] `--chain base64,hex`: mehrfaches Encoding in einer Pipeline — Output von Schritt 1 ist Input von Schritt 2
- [ ] `base58`-Format hinzufügen (ohne externe Lib: eigene Implementierung)
- [ ] Beim Dekodieren von URL-Encoding: sowohl `%XX` als auch `+` für Leerzeichen akzeptieren
- [ ] `--stats`-Flag: zeigt Länge vor/nach Encoding, Overhead in Prozent

---

## Hinweise

**Bytes vs. Strings:** `base64.b64encode()` nimmt `bytes` und gibt `bytes` zurück. Strings müssen erst encoded werden: `text.encode("utf-8")`. Beim Ausgeben: `decoded.decode("utf-8", errors="replace")` — `errors="replace"` verhindert Abstürze bei Binärdaten.

**URL-Encoding:** `urllib.parse.quote()` arbeitet mit Strings, `urllib.parse.quote_from_bytes()` mit Bytes. Für vollständige Encoding (auch `/` und `?`): `safe=""` als Parameter.

**Padding bei Base64:** Valides Base64 hat immer eine Länge, die durch 4 teilbar ist. Fehlendes Padding kannst du intern hinzufügen: `data + b"=" * (-len(data) % 4)`.

**detect_encoding Heuristik:** Prüfe in dieser Reihenfolge:
1. Enthält nur `0-9a-fA-F` und gerade Länge → wahrscheinlich Hex
2. Enthält nur Base64-Zeichen (`A-Za-z0-9+/=`) und Länge % 4 == 0 → wahrscheinlich Base64
3. Enthält `%XX`-Muster → wahrscheinlich URL-encoded

---

## Schnittstelle für `uctl`

```python
def encode(data: bytes, fmt: str) -> bytes:
    """Kodiert Bytes in das angegebene Format."""

def decode(data: bytes, fmt: str) -> bytes:
    """Dekodiert Bytes aus dem angegebenen Format."""
```

Diese Funktionen werden als `uctl enc encode` / `uctl enc decode` verwendet.
