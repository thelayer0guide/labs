# Labs — uConsole Security Lab Curriculum

18 aufeinander aufbauende Python-Labs. Jedes Tool ist eigenständig nutzbar. Am Ende vereint als `uctl` — eine einheitliche CLI-Suite, die auf der uConsole läuft.

---

## Verzeichnisstruktur

```
labs/
├── uconsole/
│   ├── md/          ← Markdown-Quelldateien (19 Labs)
│   └── html/        ← HTML-Seiten im thelayer0guide-Branding
│       └── index.html
├── uconsole-lab-katalog.html
├── uconsole-security-lab-katalog.md
├── python-jahreskurs.html
└── README.md
```

---

## Phasenübersicht

| Phase | Thema | Labs |
|-------|-------|------|
| 0 | Fundament | [Lab 00](uconsole/md/lab-00-projekt-skeleton.md) |
| 1 | Daten & Dateien | [Lab 01](uconsole/md/lab-01-hash-inspector.md) · [Lab 02](uconsole/md/lab-02-base-encoding.md) · [Lab 03](uconsole/md/lab-03-entropy-scanner.md) |
| 2 | Parsing & Forensik | [Lab 04](uconsole/md/lab-04-log-forensics.md) · [Lab 05](uconsole/md/lab-05-metadata-extractor.md) · [Lab 06](uconsole/md/lab-06-secret-detector.md) |
| 3 | Krypto & Netzwerk | [Lab 07](uconsole/md/lab-07-certificate-auditor.md) · [Lab 08](uconsole/md/lab-08-password-strength.md) · [Lab 09](uconsole/md/lab-09-port-inventory.md) |
| 4 | Integrität & Monitoring | [Lab 10](uconsole/md/lab-10-file-integrity-monitor.md) · [Lab 11](uconsole/md/lab-11-process-baseline.md) · [Lab 12](uconsole/md/lab-12-config-auditor.md) |
| 5 | Erweiterte Analyse | [Lab 13](uconsole/md/lab-13-pcap-analyzer.md) · [Lab 14](uconsole/md/lab-14-cve-auditor.md) · [Lab 15](uconsole/md/lab-15-hardware-inventory.md) |
| 6 | Engineering & Integration | [Lab 16](uconsole/md/lab-16-testing-ci.md) · [Lab 17](uconsole/md/lab-17-plugin-architektur.md) |
| ★ | Capstone | [uctl](uconsole/md/capstone-uctl.md) |

---

## HTML-Ansicht

→ **[uconsole/html/index.html](uconsole/html/index.html)** — Alle Labs im thelayer0guide-Branding

---

## Empfohlene Reihenfolge

```
00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → ★
```

Phase 3 (Labs 07–09) kann parallel zu Phase 2 begonnen werden.

---

## Lab-Dateien enthalten

- **Lernziele** — was du nach dem Lab können sollst
- **Hintergrund** — warum dieses Tool in der Praxis relevant ist
- **Anforderungen (Pflicht)** — konkrete, verifizierbare Anforderungen
- **CLI-Schnittstelle** — exakte Befehle und erwartetes Output-Format
- **Akzeptanzkriterien** — Befehle zum Selbst-Testen
- **Test-Anforderungen** — was du testen musst (keine Musterlösungen)
- **Bonus-Aufgaben** — optionale Erweiterungen
- **Hinweise** — technische Tipps ohne Lösungen
- **Schnittstelle für `uctl`** — die Funktionssignatur, die im Capstone genutzt wird
