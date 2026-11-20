# BSI Process Patterns (wiederverwendbar)

> Abgeleitet aus 19 Prozessen des Exports `bsi-crm-2026-06-24_15-09-39`. Jedes Pattern nennt die belegenden Prozesse.
> Step-Typen siehe `bsi_step_type_catalog.md`. Bewertung der Quell-Prozesse siehe `process_inventory.md`.

---

## P1 – Stammdatenänderung mit Backend-Push (Inbound + Self-Service)

- **Zweck:** Eine Stammdatengruppe (Kunde, Vertrag, Fahrzeug, Bankdaten) erfassen/ändern und ins führende Bestandssystem (IBM i/CS-API) zurückschreiben.
- **Belegt durch:** Kunde – Daten ändern (29.0.0); Vertrag – Daten ändern (4.0.0); Fahrzeug – Daten ändern (1.0.0).
- **Typischer Ablauf:** Einstieg/Steuerung (Kachel `138297`) → Verzweigung Inbound vs. Self-Service (`209153`) → ggf. Kundensuche (`112440`) + „Kunden checken und nachladen" (Lambda `209754` „aus IBM i laden") → fachliche Erfassung (`10005`/`176353`) → „Vorher-Stand speichern" (`133850`) → Review (`177421`) → „im Hintergrund ändern"/„Daten zu IBM i pushen" (`216266`/`209754`) → „Lambda erfolgreich?" (`209153`) → Abschluss (`10049`).
- **Typische Gruppen:** „Inbound – Steuerung", „Self Service – …", „… ändern", „Änderungen zu IBM i pushen".
- **Rollen:** fachliches Team (z. B. Team_Änderung) via `responsibleTeamUid`; Self-Service ohne Bearbeiter.
- **Validierungen:** Formatprüfungen (Fehlermeldungen „E-Mail/Telefon – Falsches Format"); Pflichtfelder über `visibleAttributes`/Bindings.
- **Technische Bausteine:** Lambda laden/pushen, Kriterien-Step für Lambda-Erfolg, Attribut-Snapshot.
- **Varianten:** mit/ohne Self-Service-Pfad; mit/ohne Themengebiets-Subprozess.
- **Risiken:** Doppelpflege Inbound/Self-Service-Logik; Fehlerpfad bei Push muss vorhanden sein.
- **Wiederverwendung:** Goldstandard-Vorlage für jede „Entität X ändern + Backend-Sync".

## P2 – Dunkelverarbeitung mit manueller Nachbearbeitung

- **Zweck:** Änderung automatisch (dunkel) ins Backend schreiben, bei Fehler manuell behandeln.
- **Belegt durch:** Kunde/Vertrag/Fahrzeug – Daten ändern (Gruppen „… zu IBM i pushen"); Stammdaten Sales Location („Update Branch" → „Lambda Fehler").
- **Ablauf:** Hintergrund-Lambda (`216266`/`209754`) → `209153` „Lambda erfolgreich?" → **ja:** Abschluss-Info; **nein:** „Techn. Fehler Lambda"/„Lambda Fehler" (`138297`/`168173`) → manuelle Korrektur/Zuweisung.
- **Validierungen:** Erfolgskriterium auf Lambda-Output.
- **Risiken:** Fehlender „nein"-Pfad = stille Datenverluste. Idempotenz des Backend-Calls.
- **Wiederverwendung:** Pflicht-Baustein für **jeden** Schnittstellenaufruf.

## P3 – Vieraugenprinzip / Freigabe mit Vorher-Stand

- **Zweck:** Kritische Änderung erfassen, durch zweite Instanz freigeben, dann persistieren; Ablehnung mit Begründung möglich.
- **Belegt durch:** **Stammdaten Sales Location bearbeiten (6.0.0)** — Gruppen „Änderungen freigeben (4-Augen)", „Bearbeitung verweigert", „Entscheidung abgelehnt", „Daten persistieren".
- **Ablauf:** Bearbeiten (`10005`/`168173`) → „Änderungen prüfen" (`168173`) → automatische/manuelle Zuweisung an Freigeber (`108606`/`120386`) → „Änderung freigeben" → Entscheidung (`209153`) → **freigegeben:** „Update Branch" (`209754`) + „Abschluss-Info"; **abgelehnt:** „Hinweis: Änderungen abgelehnt" → zurück zur Bearbeitung.
- **Rollen:** Bearbeiter ≠ Freigeber (über `responsibleTeamUid` + `enforceResponsibility`).
- **Bausteine:** Snapshot „Stammdaten vorbelegen"/„Vorher-Stand speichern" (`133850`) für Vergleich.
- **Risiken:** Rollen-Trennung muss technisch erzwungen werden, nicht nur dokumentiert.
- **Wiederverwendung:** Vorlage für alle genehmigungspflichtigen Änderungen (Bank, Stammdaten, Verträge).

## P4 – Kundensuche, -prüfung und Nachladen

- **Zweck:** Kunde finden/auswählen, mit Backend abgleichen und Daten nachladen, bevor fachlich gearbeitet wird.
- **Belegt durch:** Kunde – Daten ändern; Kundenanfrage beantworten; Vertrag – Einzelvertrag ändern/beenden (Gruppen „Kundensuche", „Kunden checken und nachladen").
- **Ablauf:** Kunde suchen (`112440`/`10004`) → Auswahl → „Kunde aus IBM i laden" (`209754`) → „erfolgreich?" (`209153`) → 360°-Sicht (`177421`).
- **Wiederverwendung:** Standard-Eingangsbaustein für kundenbezogene Prozesse.

## P5 – Subprozess starten und joinen (Orchestrierung)

- **Zweck:** Fachlogik in Teilprozesse auslagern (Themengebiet-/Team-Zuweisung, KYC, Dokumentklassifizierung) und auf deren Ergebnis warten.
- **Belegt durch:** Kundenanfrage beantworten; Beschwerde (telefonisch) (KYC); Dokument – Dokumenttyp zuweisen; Kommunikation – Themengebiet und Team zuweisen.
- **Ablauf:** „… starten" (`117298`) → parallele Verarbeitung → „… abwarten" (`150292`) → Ergebnis prüfen (`209153`).
- **Bausteine:** als eigenständige, wiederverwendbare Prozesse modelliert (Globale Referenz).
- **Risiken:** Deadlock/Timeout, wenn Subprozess nie endet → SLA/Eskalation nötig.

## P6 – Themengebiet- und Team-Routing

- **Zweck:** Eingehende Kommunikation automatisch dem richtigen Team/Themengebiet zuordnen.
- **Belegt durch:** Kommunikation – Themengebiet und Team zuweisen (6.0.0); eingebettet in Kommunikation/Kundenanfrage-Prozesse.
- **Ablauf:** Lambda-Routing (`209754`) → „Ist ein Themengebiet zugewiesen?" / „Wurde ein Team zugewiesen?" (`209153`) → ja: zuweisen (`108606`); nein: manuelle Zuweisung (`120386`).
- **Wiederverwendung:** zentraler Routing-Baustein für Inbound.

## P7 – Inbound-Kommunikation bearbeiten & beantworten

- **Zweck:** E-Mail/Telefon-Kommunikation bearbeiten, Kunde zuordnen, mit Vorlage antworten.
- **Belegt durch:** Kundenanfrage beantworten (85 Steps); Kommunikation beantworten (ohne Kundenauswahl) (52); Neue Kommunikation; Kommunikation weiterleiten.
- **Ablauf:** Kommunikation/Kunde suchen → Kanal-Verzweigung E-Mail/Telefon (`138297`/`209153`) → Bearbeitung → E-Mail senden mit Vorlage (`168901`) → Abschluss (`10049`)/Wiedervorlage.
- **Bausteine:** sehr viele Templates (55–58), E-Mail-Accounts pro Sparte (Service/Schaden/IDD).
- **Risiken:** Hohe Komplexität, viele Kanal-Sonderpfade → siehe Anti-Patterns.

## P8 – Beschwerde-/Abklärungsprozess mit Empfangsbestätigung

- **Zweck:** Beschwerde aufnehmen, Empfang bestätigen, intern/extern abklären, abschließen.
- **Belegt durch:** Beschwerde (telefonisch) (7.0.0); Abklärung zu Beschwerde (3.0.0, als Subprozess).
- **Ablauf:** BF-Daten betrachten/anreichern (`217005`/`216489`) → KYC (Subprozess) → Empfangsbestätigung (`168901`) → schriftliche/telefonische Abklärung → „Auf Abklärung warten" (`150292`) → Abschluss.
- **Bausteine:** Vorlagenauswahl (`134213`), Beschwerdeführer-Entität, KYC-Einbindung.

## P9 – Dokumentklassifizierung & -typzuweisung (Einzel/Mehrfach/Rest)

- **Zweck:** Eingehende Dokumente automatisch klassifizieren, Dokumenttyp zuweisen, Rest manuell prüfen.
- **Belegt durch:** Dokument – Dokumenttyp zuweisen (16.0.0) — 91 Steps, 17 Lambdas, 14 Gruppen.
- **Ablauf:** Klassifizierung starten → mehrere Lambda-Zuweisungen (Einzel/Mehrfach/anhand Dateityp) → „Lambda erfolgreich?" je Pfad → fachliche Prüfung → automatische Restzuweisung → Gesamtübersicht.
- **Risiken:** Hohe Verzweigungstiefe; viele technische Fehlerpfade — Wartungs-Hotspot.

## P10 – Wiedervorlage & Bestätigung

- **Zweck:** Vorgang mit Frist auf Wiedervorlage legen und Kunden bestätigen.
- **Belegt durch:** Vertrag – Einzelvertrag ändern/beenden (Gruppe „Wiedervorlage & Bestätigung"); Kunde – Halterwechsel (Gruppe „Weitere Unterlagen").
- **Ablauf:** „Bestätigung im Hintergrund versenden" (`216266`) → Wiedervorlage (`10049`) mit `defaultFollowUpTimeInSeconds`.

## P11 – Entität anlegen mit initialer Beziehung

- **Zweck:** Neues Objekt (Ansprechpartner) erzeugen und sofort verknüpfen.
- **Belegt durch:** Ansprechpartner anlegen (12.0.0).
- **Ablauf:** Prozess-Input prüfen (`209153`) → anlegen (`10006`) → Beziehung anlegen (`146286`) → Daten prüfen & anpassen (`177421`).

## P12 – Lambda-Button-Tile (Ad-hoc-Aktion)

- **Zweck:** Externe Aktion direkt per Button auslösen (Suche/Portalsprung/Aufgabe).
- **Belegt durch:** lambda-bindings „Search KVK", „Registerportal", „Aufgabe erstellen" (`crmlambdaButtonTile`).
- **Wiederverwendung:** für Recherche-/Sprung-Funktionen außerhalb des linearen Flusses.

---

## Pattern-Kombinationsmatrix (Beobachtung)

| Prozesstyp | Kernpatterns |
|---|---|
| Stammdaten ändern | P1 + P2 + P4 (+ P3 bei Freigabepflicht) |
| Kommunikation/Service | P7 + P6 + P4 + P10 |
| Beschwerde | P8 + P5 (KYC) |
| Dokument | P9 + P2 + P5 |
| Vertrag | P1/P4 + P10 + P2 |
