# Audit AP5 – Schnittstellen-/Lambda-Fehlerpfade

> Prüfgegenstand: Hat **jeder** Schnittstellen-/Lambda-Step einen behandelten Fehlerpfad? (Design-Rule **R5**, Anti-Pattern **AP5**)
> Quelle: `examples/bsi-crm-2026-06-24_15-09-39`, alle 19 Prozesse.
> Methode: Lambda-Steps identifiziert über `lambdaConsumerId = crm:invokeLambdaProcessStep:<gid>` (aus `lambda-bindings/`) **und** Step-Typ `209754` (synchroner Aufruf) / `216266` (Hintergrund-Versand). Anschließend Graph-Analyse: direkte Ausgänge des Lambda-Steps **und** Vorwärts-BFS (≤4 Schritte) auf einen Erfolgs-/Fehler-Entscheidungs-Step (`209153`/`107779`) bzw. einen Fehler-Behandlungs-Step (`138297`/`168173` mit Namensindikator „Fehler/Abbruch/nicht …/prüfen").
> Strukturfakt: **typeId 201503 = Start-Step, 201504 = End-Step** (je 1× pro Prozess).

## Gesamtergebnis

| Kategorie | Anzahl | Bedeutung |
|---|---:|---|
| ✅ **OK** | **38** | Erfolg/Fehler wird über nachgelagerten Kriterien-Step **oder** über die eigenen Ausgänge des Lambda-Steps differenziert behandelt. |
| 🟦 **Hintergrund/asynchron** | **5** | Dunkelverarbeitung (`216266` bzw. erfolgsgeprüfte Hintergrundänderung) – Fehlerbehandlung teils außerhalb des Flows (Monitoring). Akzeptabel, aber zu verifizieren. |
| ⚠️ **Risiko (echte Lücke)** | **2** | Beide Ausgänge führen direkt zum **End-Step** (201504) – keine In-Flow-Erfolgskontrolle/Fehlerbehandlung. |
| **Summe geprüfter Schnittstellen-Steps** | **45** | |

**Fazit:** Die Fehlerbehandlung ist über das Portfolio **überwiegend stark** ausgeprägt. Das dominante Muster ist `Lambda aufrufen (209754)` → `Lambda erfolgreich? (209153)` → Fehlerzweig („Techn. Fehler Lambda", „Zuweisung konnte nicht durchgeführt werden", „Lambda Fehler", „Neuer Kunde nicht geladen"). AP5 ist als **systemisches** Risiko **entkräftet**; es verbleiben **2 konkrete Einzelbefunde**.

---

## ⚠️ Konkrete Befunde (Risiko)

### F1 – Vertrag – Daten ändern: „Start Push zu CS-API" (typeId 209754)
- **Beobachtung:** Step hat zwei Ausgänge (B, A), **beide** führen direkt zum End-Step (201504). Kein „erfolgreich?"-Kriterium, kein Fehlerzweig im Flow.
- **Risiko:** Schreib-Push in CS-API; bei Fehler keine sichtbare Reaktion/Eskalation im Prozess → potenzielle Inkonsistenz CRM ↔ CS-API.
- **Mögliche Erklärung (Annahme):** „**Start** Push" deutet auf asynchronen Anstoß; Erfolg/Fehler wird evtl. asynchron bzw. über „Bestätigung im Hintergrund versenden" / Monitoring behandelt. **Zu verifizieren.**
- **Empfehlung:** Entweder synchroner `209153`-Erfolgscheck mit Fehlerzweig (Retry/Eskalation an Team), oder dokumentiertes asynchrones Fehler-/Monitoring-Konzept; die zwei identischen Ausgänge zum End-Step bereinigen (siehe Modellierungshinweis unten).
- **Relevanz: hoch** (Backend-Write).

### F2 – Fahrzeug – Daten ändern: „Lambda aufrufen" (typeId 209754, Gruppe „Self Service – Daten ändern")
- **Beobachtung:** Beide Ausgänge (B, A) führen direkt zum End-Step (201504). Kein Erfolgscheck.
- **Kontext:** Der **Inbound-Pfad** desselben Prozesses ist korrekt abgesichert: „Daten im Hintergrund ändern" → „Daten im Hintergrund ändern war erfolgreich" (✅). Nur der **Self-Service-Pfad** endet ungeprüft.
- **Risiko:** Self-Service-Änderung wird ohne Erfolgsrückmeldung abgeschlossen; Kunde erhält ggf. keine Fehlerinfo.
- **Empfehlung:** Self-Service-Pfad analog zum Inbound-Pfad mit Erfolgscheck + Fehlerbehandlung versehen (Pattern P2). *(gegen AP4 – Inbound/Self-Service-Drift)*
- **Relevanz: mittel** (Self-Service-Write).

> **Modellierungshinweis (beide Befunde):** Ein Lambda-Step mit zwei Ausgängen, die auf dasselbe Ziel zeigen, ist eine **leere Verzweigung** – entweder echten Fehlerzweig anschließen oder auf einen Ausgang reduzieren.

---

## 🟦 Hintergrund/asynchron (akzeptabel, zu verifizieren)

| Prozess | Step | typeId |
|---|---|---|
| Vertrag – Daten ändern | Bestätigung im Hintergrund versenden (2×) | 216266 |
| Vertrag – Daten ändern | Korrespondenz/Dokument im Hintergrund erstellen (2×) | 216266 |
| Fahrzeug – Daten ändern | „Daten im Hintergrund ändern war erfolgreich" (Erfolgscheck zur Hintergrundänderung) | 209153 |

→ Dunkelverarbeitung. **Empfehlung:** dokumentieren, wo Fehler dieser asynchronen Versände/Erstellungen auflaufen (Monitoring, Wiedervorlage, Fehlerqueue). Mindestens Logging/Alerting sicherstellen.

---

## ✅ OK – Beispiele für vorbildliche Absicherung

| Prozess | Lambda-Step | Erfolgs-/Fehlerbehandlung |
|---|---|---|
| Dokument – Dokumenttyp zuweisen | Lambda Einzel-/Mehrfach-/Restzuweisung, „anhand Dateityp", „Fachl. Prüfung starten" | je „Lambda erfolgreich?" → „Techn. Fehler Lambda – Standard Zuweisung" / „Fehler bei der fachl. Prüfung" (3 Zweige) |
| Kunde – Daten ändern | Daten zu IBM i pushen; Namensänderung/Kundenform im Hintergrund | „War der Push erfolgreich?" / „… erfolgreich?" mit Fehlerzweig |
| Vertrag – Daten ändern | Bank-/Vertrags-/Kilometer-/Vertragsbeginn-/Bankverbindung im Hintergrund ändern | je „Lambda erfolgreich?"; Bankverbindung → „Bankverbindung des Vertrages prüfen" |
| Kommunikation – Themengebiet/Team zuweisen | Lambda aufrufen (2×) | „Lambda erfolgreich?" + „Zuweisung konnte nicht durchgeführt werden" (mit Retry-Schleife) |
| Kunde – Halterwechsel | Lambda aufrufen | eigene Ausgänge → „Neuer Kunde nicht geladen" + Kriterien-Step |
| Stammdaten Sales Location | Update Branch | eigene Ausgänge → „Lambda Fehler" / „Abschluss-Info" |
| Kundenanfrage beantworten | Kontaktdaten ändern / IBM i laden / Datenanreicherung senden | je eigener Erfolgscheck |

> Zwei dominante, gut wiederverwendbare Fehlerbehandlungs-Stile:
> 1. **Separater Kriterien-Step** `209153` „… erfolgreich?" nach dem Lambda.
> 2. **Direkte Zweige am Lambda-Step** (Ausgang A=Fehler → Fehler-Info, B=Erfolg → weiter). Häufig sogar mit **Retry-Schleife** (Fehlerzweig zurück auf den Lambda-Step, s. Kommunikation-Routing).

---

## Empfehlungen (priorisiert)

1. **F1 verifizieren/härten** (CS-API-Push) – synchroner Check oder dokumentiertes Async-Fehlerkonzept. *(hoch)*
2. **F2 schließen** – Self-Service-Fahrzeugpfad analog Inbound absichern. *(mittel)*
3. **Hintergrund-Versände** (216266) mit dokumentiertem Monitoring/Fehlerqueue hinterlegen. *(mittel)*
4. **Leere Verzweigungen** (zwei Ausgänge auf dasselbe Ziel) als Lint-Regel ausschließen. *(niedrig)*
5. **Konvention:** Erfolgs-Kriterien-Steps einheitlich „… erfolgreich?" benennen (statt generisch „Kriterien"), damit Audits/automatische Prüfungen zuverlässig greifen. *(niedrig, gegen AP1/AP9)*

## Zusätzliche Strukturbefunde (durch `tools/lint_process.py`)

Der Linter ([tools/lint_process.py](../tools/lint_process.py)) bestätigt F1/F2 als die einzigen AP5-Lücken und deckt **3 echt offene Outlets** auf (R1, nicht über `targetProcessStepId` *und* nicht über geteilte `descriptorId` auflösbar):

| Prozess | Step | offener Outlet |
|---|---|---|
| Kunde – Daten ändern (29.0.0) | „Kunde bearbeiten" | B |
| Kunde – Daten ändern (29.0.0) | „Adress- und Kontakdaten ändern" | B |
| Vertrag – Daten ändern | „Kilometerstand eingeben" | B |

→ Diese dangling Outlets erklären zugleich mehrere „vom Start nicht erreichbare" Steps (v. a. die Self-Service-Namensänderungs-Gruppe in „Kunde – Daten ändern"). **Empfehlung:** Outlets verbinden oder entfernen; anschließend Linter erneut laufen lassen.

Gesamtbefund Linter (Beispiel-Export): **5 ERROR** (2× AP5 + 3 offene Outlets), 26 WARN, 379 INFO.

## Methodische Hinweise / Grenzen
- „Hintergrund"-Heuristik basiert auf typeId 216266 + Namensindikatoren; einige IBM-i-Hintergrundänderungen (z. B. „Bankverbindung im Hintergrund ändern", typeId 209754) sind **synchron mit Erfolgscheck** modelliert und daher als OK gewertet.
- Befunde F1/F2 sind belegt (beide Ausgänge → End-Step 201504); die *Erklärung* zur Asynchronität ist eine **Annahme** und sollte mit dem Fachbereich/der Integrationsdoku abgeglichen werden.
- Reproduzierbar über `/tmp/audit_ap5.py` (Ergebnis-Dump: `/tmp/bsi_analysis/ap5.json`).
