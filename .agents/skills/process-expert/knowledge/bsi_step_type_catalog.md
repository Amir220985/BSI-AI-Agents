# BSI Step-Typ-Katalog (abgeleitet)

> Abgeleitet aus 19 Prozessen des Exports `bsi-crm-2026-06-24_15-09-39`.
> Methode: `processSteps[].typeId` ↔ deutscher Step-Name aus `processStepDefinitions[].languageItems` (matched über `gid`). Häufigkeiten = Vorkommen über alle 19 Prozesse.
> **Fakt** = Step wurde im Export mit diesem `typeId` und diesen Namen gefunden. **Annahme** = fachliche Bedeutung wurde aus den Namen/Verschaltung interpretiert.

`typeId` ist der numerische Suffix von `stepDefinitionKey` (`1;112215;45832;j<typeId>`).

| typeId | Häufigkeit | Beobachtete Step-Namen (Beispiele) | Abgeleitete Funktion (Annahme) | Kategorie |
|---|---:|---|---|---|
| **209153** | 145 | „Lambda erfolgreich?", „Ist ein Themengebiet zugewiesen?", „Wurde ein Team zugewiesen?", „Hauptbetreuer?", „Entscheidung" | **Kriterien-/Entscheidungs-Step** (Verzweigung mit booleschen/DataModel-Constraints, Outlets je Zweig) | Logik |
| **138297** | 79 | „Kachelschritt", „Techn. Fehler Lambda", „Automatische Zuweisung restlicher Dokumente" | **Kachel-/Routing-Step** (Menü/Tile, technischer Verteiler, Default-Pfade) | UI/Logik |
| **168901** | 77 | „E-Mail senden", „Abschlussschreiben verfassen", „Empfangsbestätigung verfassen" | **Korrespondenz/E-Mail erstellen & senden** (mit Vorlagen) | Korrespondenz |
| **209754** | 40 | „Lambda … aufrufen", „Lambda für Einzelzuweisung aufrufen" | **Lambda/Schnittstelle aufrufen** (Integration, synchron) | Integration |
| **168173** | 39 | „Abbruch-Info", „Änderungen prüfen", „Dokumenttyp zuweisen", „Hinweis: …" | **Info-/Hinweis-/manueller Prüf-/Bearbeitungs-Step** (Maske ohne Entitäts-Edit) | UI/Manuell |
| **150292** | 29 | „Gestartete Geschäftsvorfälle abwarten", „KYC Prozess abwarten" | **Warte-/Join-Step** (auf Subprozess/Geschäftsvorfall warten) | Orchestrierung |
| **117298** | 29 | „Themengebiet-Zuweisung starten", „KYC Prozess starten", „Dokumentklassifizierung starten" | **Subprozess/Geschäftsvorfall starten** (Fork) | Orchestrierung |
| **133850** | 22 | „Prozess-Attribute setzen", „Vorher-Stand speichern", „Zwischenspeichern" | **Attribute/Daten setzen** (automatisch, Zustandsspeicher) | Automatik |
| **217005** | 13 | „Dokument suchen", „Einen Vertrag auswählen", „Beschwerdeführer Daten betrachten" | **Such-/Auswahl-Step** (Entität wählen/anzeigen) | UI/Manuell |
| **10005** | 10 | „Kunde bearbeiten", „Ansprechpartner bearbeiten", „Beziehungen bearbeiten" | **Entität bearbeiten** (Edit-Maske, mit Bindings) | UI/Manuell |
| **10049** | 9 | „Geschäftsvorfall abschließen", „Kundenservice", „Wiedervorlage" | **Abschluss-/Wiedervorlage-Step** (Endzustand / Follow-up) | Abschluss |
| **120386** | 9 | „Geschäftsvorfall manuell zuweisen" | **Manuelle Zuweisung** (an Team/Bearbeiter) | Zuweisung |
| **177421** | 9 | „360°-Sicht anzeigen", „Änderungen prüfen", „Geänderte Daten überprüfen" | **Anzeige-/Review-Step** (read-only Prüfung) | UI/Manuell |
| **112440** | 6 | „Kunde suchen" | **Kundensuche** (spezialisierter Such-Step) | UI/Manuell |
| **213681** | 5 | „Vertrag suchen", „Vertragsauswahl" | **Vertragssuche/-auswahl** | UI/Manuell |
| **216266** | 4 | „Bestätigung im Hintergrund versenden", „Korrespondenz im Hintergrund erstellen" | **Hintergrund-Korrespondenz** (automatischer Versand) | Korrespondenz/Automatik |
| **108606** | 3 | „Geschäftsvorfall automatisch/an Erfasser zuweisen" | **Automatische Zuweisung** | Zuweisung |
| **10006** | 2 | „Kunde erstellen", „Ansprechpartner anlegen" | **Entität anlegen** | UI/Manuell |
| **10004** | 2 | „Kunde suchen", „Beschwerdeführer Daten" | **Such-/Datenerfassungs-Step** | UI/Manuell |
| **216489** | 2 | „… Daten mit Nachweis bearbeiten", „Daten anreichern" | **Bearbeiten mit Nachweis/Anreicherung** | UI/Manuell |
| **216463** | 2 | „Daten erstellen", „Bankverbindung anlegen" | **Datensatz/Subentität erstellen** | UI/Manuell |
| **134213** | 1 | „Schriftliche Abklärung – Vorlage wählen" | **Vorlagenauswahl** | Korrespondenz |
| **134229** | 1 | „Korrespondenz/Dokument bearbeiten" | **Dokument bearbeiten** | Korrespondenz |
| **104108** | 1 | „Telefonisch abklären" | **Telefonkontakt/Aktivität** | Manuell |
| **146286** | 1 | „Beziehung zu Kunde hinzufügen" | **Beziehung anlegen** | UI/Manuell |
| **10064** | 1 | „Kunde deaktivieren" | **Entität deaktivieren** | UI/Manuell |
| **10048** | 1 | „Bitte Beschwerdeführer auswählen" | **Auswahl-Step** | UI/Manuell |
| **128738** | 1 | „Kommunikation suchen" | **Kommunikationssuche** | UI/Manuell |
| **176353** | 1 | „Adress- und Kontaktdaten ändern" | **Spezial-Edit-Step** | UI/Manuell |
| **213680** | 1 | „Vertragsauswahl" | **Vertragsauswahl (Variante)** | UI/Manuell |
| **107779** | 1 | „Ist der Portalzugang weiterhin gesperrt?" | **Kriterien-Step (Variante)** | Logik |
| **201503 / 201504** | je 1+ | (ohne Name – Start/technisch) | **Start-/technischer Marker-Step** *(Annahme)* | Struktur |

## Faustregeln zur Step-Auswahl (abgeleitet)

- **Verzweigung** → `209153` (Kriterien-Step). Outlets tragen Labels (A/B/C…), die im Graph als Verbindungen zu `targetProcessStepId` führen.
- **Schnittstelle synchron** → `209754` (Lambda aufrufen) + nachgelagerter `209153` „Lambda erfolgreich?" für Fehlerpfad.
- **Schnittstelle/Subprozess asynchron** → `117298` (starten) … später `150292` (abwarten/joinen).
- **Automatischer Hintergrundversand** → `216266`; **interaktiver Versand** → `168901`.
- **Zustand zwischenspeichern (z. B. Vorher-Stand für 4-Augen/Rollback)** → `133850`.
- **Abschluss/Wiedervorlage** → `10049`.
- **Manuelle vs. automatische Zuweisung** → `120386` vs. `108606`.

> Hinweis: Die fachliche Bedeutung der typeIds ist aus Namen + Verschaltung **abgeleitet**, nicht aus einem offiziellen BSI-Step-Katalog. Bei Diskrepanz gilt der offizielle BSI-Process-Step-Registry-Eintrag (vgl. `bsi-ai-development/.agents/skills/process-expert/process_step_registry.json`).
