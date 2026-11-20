# BSI CX – Story-Patterns

> Wiederkehrende Story-Muster aus den Beispiel-Exporten. Step-Typen siehe `cx_step_type_catalog.md`.

## CXP1 – Welcome-/Trigger-Mailing
- **Zweck:** Nach einem Auslöser eine (Serien-)E-Mail senden und Reaktion auswerten.
- **Belegt durch:** „Newsletter Welcome Mailing", „Nach Schadenfall".
- **Ablauf:** Teilnehmer-Step (`EntryPointProducer`/`crocus.CrmTriggerProducer`) → `SendEmail` → Verzweigung über Outlets (gelesen/ungelesen/keine Reaktion, ggf. via `temporalConfig`) → Folgeaktion/Indikatoren.
- **Bausteine:** E-Mail-Content + Design; Indikatoren (Versendet/Gelesen/Conversion).

## CXP2 – Double-Opt-in / Newsletter-Anmeldung
- **Zweck:** Anmeldung über Landingpage mit Bestätigung (Opt-in) DSGVO-konform.
- **Belegt durch:** „Newsletter Anmeldung", „Preference Center".
- **Ablauf:** `LandingPage` (Formular) → `ModifyCrmCustomer`/`CrmCustomerOptIn` → Bestätigungs-`SendEmail` → `BranchByCrmCustomerOptIn` → `PreferenceCenter`.
- **Bausteine:** Landingpage-Content mit Formular, Opt-in-Daten-Step.

## CXP3 – Self-Service-Strecke (Online + CRM)
- **Zweck:** Kunde erledigt einen Vorgang online; Daten fließen ins CRM.
- **Belegt durch:** „Self-Service 2024", „SEPA-Mandatsdaten einholen".
- **Ablauf:** Einstieg → `LandingPage`/`WebsiteDispatcher` (mehrseitig) → Validierung (`BranchByConstraint`) → Daten-Steps (`ModifyCrmCustomer`, `CrmCommunication`) → Abschluss-Content.
- **Bausteine:** mehrere verkettete Pages (`WebsiteDispatcher` „Nächste Page"), Formulare, CRM-Rückschreiben.

## CXP4 – E-Signatur / KYC (Integration)
- **Zweck:** Identität feststellen / Dokumente signieren via externem Dienst.
- **Belegt durch:** „inSign Antragsstrecke", „inSign Demostory", „Feststellung wirtschaftl. Berechtigung".
- **Ablauf:** Daten erfassen → `crocus.PushInsign`/`ConfiguredInvokeLambda` (E-Signatur anstoßen) → warten/verzweigen auf Ergebnis → `CreateDocument` → Abschluss.
- **Bausteine:** konfigurierte/Low-Code-Steps; Dokument-Content; Fehlerpfad bei Integration (siehe Designregeln).

## CXP5 – Befragung/NPS mit AI
- **Zweck:** Feedback einholen und (AI-gestützt) auswerten/routen.
- **Belegt durch:** „NPS Umfrage mit AI", „Schoko-Quiz", „Campaign Genius".
- **Ablauf:** Einstieg → `SendEmail`/`LandingPage` (Umfrage) → `CrmFeedback` → `ExecuteBrain` (AI-Klassifikation) → Verzweigung nach Ergebnis → Folgeaktion.
- **Bausteine:** Brain/ML-Step, Feedback-Daten-Step, Indikatoren (NPS).

## CXP6 – Substory (wiederverwendbarer Teil-Flow)
- **Zweck:** Gemeinsamen Teilablauf kapseln und aus mehreren Stories aufrufen.
- **Belegt durch:** „Preference Center Plus" (substory=true).
- **Ablauf:** `SubstoryEntry` … Logik/Push … `SubstoryResponse`; Aufruf aus Hauptstory via Prozedur-Step / `HandOverToOtherStory`.

## CXP7 – Verzweigung & Parallelisierung
- **Zweck:** Teilnehmer nach Kriterien/Filter steuern, Pfade parallel führen und wieder zusammenführen.
- **Belegt durch:** nahezu alle größeren Stories.
- **Ablauf:** `BranchByConstraint`/`BranchByFilter` (Outlets je Zweig) · `ForkFlow` → parallele Pfade → `JoinFlow` · `DelayByInterval`/`DelayUntilFixDate` für Timing.

## CXP8 – KPI-/Indikator-Messung
- **Zweck:** Erfolg messbar machen (Mission Control).
- **Belegt durch:** alle Stories; „KPI Simulieren für Flavor Mailing".
- **Ablauf:** Indikatoren am Outlet setzen (`outlets[].indicatorIds`) bzw. `SetIndicators`-Step; KPIs werden pro **Flavor** definiert.

## Kombinationsmatrix
| Story-Typ | Kern-Patterns |
|---|---|
| Newsletter/Mailing | CXP1 + CXP8 |
| Anmeldung/Opt-in | CXP2 + CXP7 |
| Self-Service | CXP3 + CXP7 + CXP4 (falls Signatur) |
| Befragung | CXP5 + CXP8 |
| Wiederverwendung | CXP6 |
