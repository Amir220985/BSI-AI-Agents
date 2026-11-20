# BSI Process Anti-Patterns

> Beobachtete Schwächen in den Exporten. Relevanz: niedrig / mittel / hoch.
> Belege beziehen sich auf `bsi-crm-2026-06-24_15-09-39`.

---

## AP1 – Inkonsistente / fehlerhafte Benennung (Tippfehler in Status-, Step- und Gruppennamen)

- **Beschreibung:** Mehrere Tippfehler und uneinheitliche Schreibweisen in produktiv exportierten Namen: „Ungültiger sStart", „Starkommunikation"/„Startkommunikation" (beide Varianten), „Vetragsanzeige", „Beschwerdeführe", „Email senden (Telefonat))" (doppelte Klammer), „Adress- und Kontakdaten ändern".
- **Risiko:** Verwirrung im Fachbetrieb, erschwerte Suche/Wartung, schlechter Eindruck in Demos/Audits, fehleranfällige Referenzierung.
- **Betroffen:** Dokument – Dokumenttyp zuweisen; Kundenanfrage beantworten; Vertrag – Einzelvertrag ändern; Kommunikation beantworten; Kunde – Daten ändern.
- **Verbesserung:** Namens-Lint vor Export; Namenskonvention (siehe Design-Rules R7).
- **Relevanz:** mittel

## AP2 – Komplexitäts-Hotspots / Monolith-Prozesse

- **Beschreibung:** „Dokument – Dokumenttyp zuweisen" (91 Steps, 14 Gruppen, 17 Lambdas) und „Kundenanfrage beantworten" (85 Steps, 7 Gruppen) bündeln sehr viel Logik in einem Prozess. „Kunde – Daten ändern" (57) und „Kommunikation beantworten" (52) ebenfalls groß.
- **Risiko:** Schwer testbar, schwer wartbar, hohe Regressionsgefahr bei Änderungen; lange Einarbeitung.
- **Verbesserung:** Wiederkehrende Gruppen (Einzel-/Mehrfach-/Restzuweisung, Kanal-Bearbeitung) als **Subprozesse** auslagern (Pattern P5); gemeinsame Routing-/Suchblöcke konsolidieren.
- **Relevanz:** hoch

## AP3 – Hohe Anzahl Kanal-/Sonderpfade in Kommunikationsprozessen

- **Beschreibung:** Kommunikationsprozesse haben viele nahezu parallele Pfade (E-Mail Servicecenter / Schaden / Telefonat) mit eigenen Vorlagengruppen (55–58 Templates).
- **Risiko:** Duplizierte Logik, Drift zwischen Pfaden, Pflegeaufwand bei Vorlagenänderung.
- **Betroffen:** Kundenanfrage beantworten; Kommunikation beantworten; Neue Kommunikation; Kommunikation weiterleiten.
- **Verbesserung:** Kanal als Parameter/Attribut statt als kopierten Pfad; Vorlagen über Sparte/Themengebiet selektieren statt über getrennte Step-Ketten.
- **Relevanz:** mittel

## AP4 – Doppelpflege Inbound vs. Self-Service

- **Beschreibung:** Stammdatenprozesse pflegen Inbound- und Self-Service-Varianten als getrennte Gruppen/Step-Ketten mit ähnlicher Fachlogik.
- **Risiko:** Logik-Drift (eine Variante wird geändert, die andere nicht).
- **Betroffen:** Kunde – Daten ändern; Vertrag – Daten ändern; Fahrzeug – Daten ändern.
- **Verbesserung:** gemeinsamen fachlichen Kern als Subprozess; Variante nur in Steuerung/Berechtigung unterscheiden.
- **Relevanz:** mittel

## AP5 – Schnittstellenaufruf ohne erkennbaren Fehlerpfad

- **Beschreibung:** Lambda-Steps benötigen einen behandelten Fehlerpfad – entweder über einen nachgelagerten „… erfolgreich?"-Kriterien-Step (`209153`) mit echtem „nein"-Zweig oder über differenzierte eigene Ausgänge (Fehler-Info). Wo beides fehlt, droht stiller Datenverlust.
- **Audit-Ergebnis (vollständig durchgeführt, s. [audit_ap5_schnittstellen_fehlerpfade.md](audit_ap5_schnittstellen_fehlerpfade.md)):** 45 Schnittstellen-Steps geprüft → **38 OK, 5 Hintergrund/asynchron, 2 echte Risiken**. AP5 ist als **systemisches** Risiko **entkräftet**; das dominante Muster (`209754` → `209153` „erfolgreich?" → Fehlerzweig) ist durchgängig vorbildlich.
- **Verbleibende Einzelbefunde:**
  - **F1 (hoch):** „Vertrag – Daten ändern / Start Push zu CS-API" – beide Ausgänge → End-Step (201504), kein In-Flow-Check. Async-Konzept verifizieren oder härten.
  - **F2 (mittel):** „Fahrzeug – Daten ändern / Lambda aufrufen (Self-Service)" – beide Ausgänge → End-Step; Inbound-Pfad desselben Prozesses ist dagegen korrekt abgesichert (Drift, vgl. AP4).
- **Risiko:** Inkonsistenz CRM ↔ IBM i/CS-API; Kunde glaubt Änderung erfolgt, Backend nicht aktualisiert.
- **Verbesserung:** verbindliches Muster P2; Retry/Eskalation; Monitoring auf Lambda-Fehler; leere Verzweigungen (2 Ausgänge auf dasselbe Ziel) per Lint ausschließen.
- **Relevanz:** hoch (Einzelbefunde), systemisch entkräftet.

## AP6 – Verantwortlichkeit nur über Teams, kaum differenzierte Rollen

- **Beschreibung:** `responsibleTypeUid` ist durchgängig ein einziger Typ; fachliche Trennung läuft nur über virtuelle Teams. Im `Rollen`-Code existieren nur technische Rollen (Admin/Entwicklung).
- **Risiko:** Bei Vieraugen-/Freigabeprozessen ist die Bearbeiter-/Freigeber-Trennung schwer nachweisbar/erzwingbar, wenn Personen in beiden Teams sind.
- **Betroffen:** Stammdaten Sales Location (4-Augen) und alle freigabepflichtigen Prozesse.
- **Verbesserung:** explizite Freigeber-Rolle/Team; `enforceResponsibility` für Freigabe-Steps prüfen; Funktionstrennung dokumentieren.
- **Relevanz:** mittel

## AP7 – Strukturlose / gruppenlose Prozesse

- **Beschreibung:** Einige Prozesse haben keine `processStepGroups` (Abklärung zu Beschwerde, Portalzugang freischalten) — bei kleinen Prozessen vertretbar, bei wachsenden ein Risiko.
- **Risiko:** Schlechte Lesbarkeit, sobald der Prozess wächst.
- **Verbesserung:** Gruppen früh einführen; Konvention „>8 Steps ⇒ Gruppen".
- **Relevanz:** niedrig

## AP8 – Mögliche Dubletten in Stammdaten

- **Beschreibung:** Zwei Prozessgruppen „Vertrieb" mit unterschiedlichen IDs.
- **Risiko:** Falsche Zuordnung von Prozessen, inkonsistente Auswertung.
- **Verbesserung:** Dublettenprüfung/Bereinigung; eindeutige Gruppen.
- **Relevanz:** niedrig

## AP9 – Fehlende fachliche Dokumentation der Logik

- **Beschreibung:** `notes`/`knowledges` der Prozess- und Step-Definitionen sind weitgehend leer (`notes: null`, `knowledges: []`). Verzweigungslogik (Outlets A/B/C) ist nur über Diagramm/Bindings erschließbar.
- **Risiko:** Technische Logik ohne fachliche Begründung; Wissensverlust, schwere Übergaben.
- **Verbesserung:** Pflicht-`notes` je Entscheidungs-Step und Lambda-Step; Outlet-Labels sprechend benennen (statt nur A/B/C).
- **Relevanz:** mittel

---

## Audit-Empfehlung (Priorität)

1. **AP5** (Lambda-Fehlerpfade) — pro Schnittstellen-Step verifizieren. *hoch*
2. **AP2** (Monolithen entflechten) — Dokument-/Kundenanfrage-Prozess. *hoch*
3. **AP3/AP4** (Duplizierung Kanal/Inbound). *mittel*
4. **AP1/AP9** (Benennung & Doku) — als Lint/Review-Gate. *mittel*
