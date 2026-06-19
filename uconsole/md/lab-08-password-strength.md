# Lab 08 — Password Strength Analyzer

> **Phase 3 — Krypto & Netzwerk**
> Voraussetzungen: Lab 00 (Projektstruktur)
> Kann parallel zu Phase 2 begonnen werden
> Geschätzte Zeit: 4–6 Stunden

---

## Lernziele

- Entropie auf Zeichenklassen-Basis (nicht Byte-Ebene) berechnen
- Wörterbuch-Abgleich mit lokalen Passwortlisten implementieren
- k-Anonymity als Datenschutz-Prinzip praktisch anwenden
- Tastatur-Muster und bekannte Transformationen erkennen
- Privacy-bewusstes API-Design (Klartext verlässt das Gerät nie)

---

## Hintergrund

Passwort-Stärke ist kein binäres Konzept — es ist eine Schätzung der Angreifbarkeit unter bekannten Angriffsmethoden. Die wichtigsten Faktoren: Länge (dominiert), Zeichenraum, Wörterbuch-Verwundbarkeit, erkennbare Muster.

Die k-Anonymity-Integration mit HaveIBeenPwned ist ein elegantes Datenschutz-Design: Du sendest nur den SHA1-Präfix (5 von 40 Zeichen), erhältst eine Liste von Hashes, die mit diesem Präfix beginnen, und prüfst lokal ob dein vollständiger Hash dabei ist — das Klartext-Passwort verlässt das Gerät nie.

---

## Aufgabe

Implementiere `pwcheck` — ein lokales Passwort-Analyse-Tool ohne Cloud-Abhängigkeit.

### Projektstruktur

```
security-lab/
└── pwcheck/
    ├── __init__.py
    ├── core.py
    ├── wordlists/
    │   └── top-10k.txt    (10.000 häufige Passwörter aus rockyou, anonymisiert)
    ├── cli.py
    └── tests/
        ├── __init__.py
        └── test_core.py
```

---

## Anforderungen (Pflicht)

### core.py

- [ ] Funktion `detect_character_classes(password: str) -> dict`
  - Erkennt welche Klassen vorhanden sind:
    ```python
    {
        "lowercase": bool,      # a-z
        "uppercase": bool,      # A-Z
        "digits": bool,         # 0-9
        "special": bool,        # alles andere
        "charset_size": int,    # Größe des genutzten Zeichenraums
    }
    ```
  - `charset_size`: Summe der genutzten Klassen (26 + 26 + 10 + 32 = 94 für alle vier)
  - Zeichenraumgröße der Sonderzeichen: nutze 32 als Schätzung (druckbare ASCII-Sonderzeichen)

- [ ] Funktion `calculate_password_entropy(password: str) -> float`
  - Formel: `log2(charset_size) × len(password)`
  - Gibt Bits zurück
  - `password = ""` → 0.0

- [ ] Funktion `estimate_crack_time(entropy_bits: float) -> dict`
  - Berechnet geschätzte Zeit in Sekunden für verschiedene Angriffsraten:
    ```python
    {
        "online_throttled":     float,  # 100 Versuche/Stunde (echtes Login)
        "online_unthrottled":   float,  # 10^4/Sekunde (kein Rate-Limit)
        "offline_fast":         float,  # 10^9/Sekunde (GPU, bcrypt)
        "offline_very_fast":    float,  # 10^12/Sekunde (GPU, MD5)
    }
    ```
  - Formel: `2^entropy_bits / rate` = Sekunden für 50% Wahrscheinlichkeit
  - Gibt `float("inf")` wenn Zeit > 10^15 Sekunden (praktisch unknackbar)

- [ ] Funktion `format_crack_time(seconds: float) -> str`
  - Lesbare Darstellung: "< 1 Sekunde", "3 Minuten", "47 Stunden", "12 Jahre", "Jahrhunderte"
  - `float("inf")` → "praktisch unknackbar"

- [ ] Funktion `check_wordlist(password: str, wordlist_path: Path) -> bool`
  - Gibt `True` zurück wenn Passwort in der Wortliste vorkommt
  - **Case-insensitive** Vergleich
  - Wortliste wird bei erstem Aufruf geladen und intern gecacht (einmal lesen genügt)
  - Kein Absturz wenn Wortlistendatei nicht existiert (gibt `False` zurück, loggt Warnung)

- [ ] Funktion `detect_keyboard_patterns(password: str) -> list[str]`
  - Erkennt bekannte Tastatur-Läufe: `qwerty`, `qwertz`, `asdf`, `1234`, `abcd` (und Varianten)
  - Prüft sowohl vorwärts als auch rückwärts
  - Gibt Liste erkannter Muster zurück (leer wenn keines)
  - Mindestlänge eines erkannten Musters: 4 Zeichen

- [ ] Funktion `analyze_password(password: str, wordlist_path: Path | None) -> dict`
  - Kombiniert alle obigen Analysen:
    ```python
    {
        "length": int,
        "entropy_bits": float,
        "character_classes": dict,
        "in_wordlist": bool,
        "keyboard_patterns": list[str],
        "crack_times": dict,
        "score": int,          # 0–4 (analog zxcvbn)
        "score_label": str,    # "sehr schwach", "schwach", "mittel", "stark", "sehr stark"
        "feedback": list[str], # Konkrete Verbesserungsvorschläge
    }
    ```

- [ ] **Score-Logik:**
  - Score 0: In Wortliste ODER Länge < 6
  - Score 1: Nur eine Zeichenklasse ODER Länge < 8
  - Score 2: Zwei Zeichenklassen ODER Keyboard-Muster erkannt
  - Score 3: Drei Zeichenklassen UND Länge ≥ 12
  - Score 4: Vier Zeichenklassen UND Länge ≥ 16 UND nicht in Wortliste

- [ ] **Feedback-Generierung:** Generiere konkrete Hinweise, z. B.:
  - "Passwort ist zu kurz (< 12 Zeichen)"
  - "Passwort in bekannter Wortliste gefunden"
  - "Tastatur-Muster erkannt: 'qwerty'"
  - "Füge Sonderzeichen hinzu"

### cli.py

- [ ] `pwcheck PASSWORD [--wordlist DATEI] [--hibp]`
  - `PASSWORD`: entweder als Argument oder `--stdin` (sicherer)
  - `--wordlist`: alternative Wortliste
  - `--hibp`: optionaler HaveIBeenPwned-Check (Bonus)

**Wichtig für die CLI:** Das Passwort als Argument erscheint in der Shell-History. Implementiere auch `--stdin`:
```bash
echo "mypassword" | pwcheck --stdin
```

---

## CLI-Schnittstelle (vollständig)

```
pwcheck "Tr0ub4dor&3"
pwcheck --stdin
echo "password123" | pwcheck --stdin --wordlist /custom/list.txt
```

Beispiel-Output:
```
PASSWORD STRENGTH ANALYZER
══════════════════════════════════════════

Länge          14 Zeichen
Zeichenraum    94 (Groß + Klein + Ziffern + Sonderzeichen)
Entropie       91.8 Bit

CRACK-ZEITEN (geschätzt)
  Online (throttled)    Jahrhunderte
  Online (kein Limit)   ~23 Tage
  Offline GPU           ~11 Sekunden  ← bcrypt macht das langsamer

BEWERTUNG: ★★★☆☆ MITTEL (Score 3/4)

Feedback:
  ✓ Alle Zeichenklassen vorhanden
  ✗ Passwort enthält erkanntes Muster: "Tr0ub4d" (Leet-Speak)
  → Tipp: Vier zufällige Wörter sind oft sicherer als komplexe kurze Passwörter

══════════════════════════════════════════
HINWEIS: Das Passwort wurde lokal analysiert und nirgends übertragen.
```

---

## Wortliste erstellen

Erstelle `wordlists/top-10k.txt`:
- 10.000 Zeilen, ein Passwort pro Zeile
- Aus öffentlichen rockyou-Datensätzen (die obersten 10.000 sind weit verbreitet und frei verfügbar)
- Keine echten Nutzerpasswörter — nur die bekannten "schlechtesten" Passwörter wie `password`, `123456`, `qwerty` etc.

Alternativ: Download eines bestehenden Top-10k-Listen-Auszugs und Referenz in `README.md`.

---

## Akzeptanzkriterien

```bash
python -c "
from pwcheck.core import analyze_password
from pathlib import Path

# Schwaches Passwort
weak = analyze_password('password', Path('wordlists/top-10k.txt'))
assert weak['score'] == 0, f'Erwartet Score 0, bekam {weak[\"score\"]}'
assert weak['in_wordlist'] == True

# Starkes Passwort
strong = analyze_password('X\$k9!mP@2#qW8&vR', None)
assert strong['score'] >= 3
assert strong['entropy_bits'] > 80

# Keyboard-Pattern
kp = analyze_password('qwerty12345', None)
assert len(kp['keyboard_patterns']) > 0

print('Alle Tests bestanden')
"
```

---

## Tests (Anforderungen an test_core.py)

- [ ] Test: `detect_character_classes("abc")` → nur lowercase, charset_size = 26
- [ ] Test: `detect_character_classes("Abc1!")` → alle Klassen, charset_size = 94
- [ ] Test: `calculate_password_entropy("a" * 8)` → `log2(26) * 8 ≈ 37.6`
- [ ] Test: `calculate_password_entropy("")` → 0.0
- [ ] Test: `estimate_crack_time(0.0)` → alle Zeiten nahe 0
- [ ] Test: `format_crack_time(30)` → "30 Sekunden" oder ähnlich
- [ ] Test: `format_crack_time(float("inf"))` → "praktisch unknackbar"
- [ ] Test: `detect_keyboard_patterns("qwertz123")` → nicht leer
- [ ] Test: `detect_keyboard_patterns("X\$k9!mP@")` → leer
- [ ] Test: `check_wordlist("password", ...)` → True
- [ ] Test: `check_wordlist("X\$k9!mP@2#qW8", ...)` → False

---

## Bonus-Aufgaben

- [ ] **HaveIBeenPwned k-Anonymity:**
  ```
  pwcheck "mypassword" --hibp
  ```
  - SHA1-Hash des Passworts berechnen
  - Nur die ersten 5 Zeichen des Hashes senden: `GET https://api.pwnedpasswords.com/range/{prefix}`
  - Antwort lokal prüfen ob vollständiger Hash enthalten
  - Passwort verlässt das Gerät nie im Klartext

- [ ] **Leet-Speak-Erkennung:** Erkenne typische Substitutionen (`a→@`, `e→3`, `i→1`, `o→0`, `s→$`) und warne wenn das Original ein Wörterbuch-Wort wäre

- [ ] **Passphrase-Modus:** Erkenne Wort-Kombinationen und bewerte sie entsprechend (4 zufällige Wörter sind oft sicherer als "Tr0ub4dor&3")

---

## Hinweise

**Entropie-Formel:** `math.log2(charset_size) * len(password)` — das ist eine obere Schranke (worst-case für Angreifer). Bekannte Muster oder Wörterbuch-Wörter reduzieren die echte Entropie erheblich.

**Wortlisten-Caching:** Nutze ein Modul-Level-Dict `_wordlist_cache: dict[Path, set[str]] = {}`. Bei erstem Aufruf laden, danach aus Cache lesen. Verwende ein `set` für O(1)-Lookup.

**Tastatur-Layout:** QWERTY und QWERTZ unterscheiden sich — implementiere beide. Definiere Reihen als Strings: `"qwertyuiop"`, `"asdfghjkl"`, `"zxcvbnm"`, `"qwertzuiop"` etc.

**Privacy-Hinweis in der CLI:** Zeige immer explizit an, dass das Passwort nicht übertragen wird.

---

## Schnittstelle für `uctl`

```python
def analyze_password(password: str, wordlist_path: Path | None = None) -> dict:
    """Analysiert Passwort-Stärke lokal ohne Netzwerkzugriff."""
```
