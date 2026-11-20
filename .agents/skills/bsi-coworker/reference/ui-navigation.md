# UI-Navigation — BSI Customer Suite

Karte des Oberflächen-Vokabulars und der Modulstruktur, damit du den **aktuellen UI-Kontext erkennen** und gezielt **navigieren** kannst. Grundlage: BSI-„Benutzeroberfläche"-Doku (April 2026) und Produktspezifikation 2025 V1.3.

## Module (Sichten/Produkte)
| Modul | Arbeitsobjekt | Bausteine |
|---|---|---|
| **BSI CRM** | Prozesse | Prozessschritte |
| **BSI CX** | Story | Steps (Storyboard) |
| **BSI Insight** | Selektionsdiagramm | Selektionsschritte |
| **BSI AI** | Brain | Cortexe |
| **BSI EIP** | Interface | Prozessoren |
| **Flow Designer** | Flows | — |

Modulwechsel erfolgt über die **Sichtenauswahl** in der Desktopleiste.

## Grundflächen (BSI CRM)
1. **Desktopleiste** (oben) — Sichtenauswahl · Globale Suche · Favoriten · Fokus · Menüs · Menü «Benutzerprofil»
2. **Navigationsbaum** (links) — Ordner · Dossier mit Drill-down
3. **Funktionsleiste** — Schliessen · Öffnen · Menü · Drop-down-Menü · Dreipunkt-Menü · Menü «Teilen»
4. **Arbeitsbereich mit Tabellenansicht** — Spalte · Spaltenkopf · Spalteneinstellungen · Filter · Sortierung
5. **Werkzeugleiste** (für Tabellen) — Suche · Diagramm · Karte · Summe · Filter · Status

**Session-Anker (Login erfolgreich?):** Sind Desktopleiste, Navigationsbaum und ein Cockpit/Dashboard sichtbar und ist das **Benutzerprofil-Menü** befüllt, besteht eine gültige Session.

## Weitere UI-Elemente
- **Masken und Reiter** — Detailansicht eines Objekts mit Reitern.
- **Assistent** — Menü «Assistent» → **Prozessgruppe** → vorkonfigurierte Prozesse. Beim Ausführen: **Schrittleiste** + **Assistentenleiste** (Folgeaktion, „Nächster Schritt", Fehlerhandling).
- **360°-Sichten** — **Cockpit** (360°-Sicht des Benutzers) und **360°-Sicht** (auf Kunden, Aufträge etc.).
- **Prozess** — Prozesskonfiguration · Prozessschritt · Seitenleiste.
- **Telefon** — Menü «Telefon» · Telefonbuch.
- **Diagramme** — Säulen/Balken/Linien/Kreis/Blasen.
- **Rückfrage** & **System-Meldungen** — Dialoge der Suite; relevant für den Safety-Check (Bestätigungs- und Warnhinweise **lesen**, nicht blind wegklicken).

## CRM-Hauptbereiche (Navigationsbaum, oberste Ebene)
Zur Orientierung beim Suchen von Datensätzen/Funktionen:

1. **Kunden** — Adressen, Bankverbindungen, Beziehungen, Datenschutz, Dubletten, Target/Next Best Action, Visitenkarte
2. **Aufträge** — Capture Plan, Lead-/Opportunity-Mgmt, Lieferungen, Produkte, Projektmanagement, Zahlungen
3. **Kommunikationen** — E-Mail, Telefon, SMS, Chat, Social Media, Brief/Fax, Besuch/Event
4. **Marketing** — Aktionen, Kampagnen, Zielgruppen, Potenzialanalysen, Reaktionen, Themen
5. **Arbeit** — Aufgaben, Tickets, Cockpit, Kalender, Geschäftsvorfälle, SLA, Servicelinien, Stellvertretung
6. **Allgemeine Funktionen** — Assistent, Suche, Favoriten, Fokus, Teilen, Dokumenterstellung
7. **Konfigurationen** — 360°-Sichten, Prozesse, Dokumentvorlagen, Wertelisten, Regelwerk
8. **Daten (Customer Data Platform)** — AI/Cortex, Customer Insight, Picker, Reports, Zeitmaschine
9. **Personalmanagement** — Buchungen, Kurse
10. **Betrieb** — Enterprise Integration, Jobs, Parameter, Smoketests
11. **Benutzer** — Interne Organisation, Zugriffsrechte, Berechtigungen

> Die tatsächliche Baumstruktur ist mandanten-/rollenspezifisch. Verlasse dich auf den **sichtbaren** Baum, nicht auf diese Liste — sie dient nur der Orientierung und der Begriffszuordnung.

## Navigationsmuster
- **Direktnavigation**: Liegt eine Deep-Link-URL auf Datensatz/Prozess/Bereich vor, per `navigate` direkt öffnen.
- **Globale Suche**: Objekte über die Suche in der Desktopleiste finden.
- **Tabellenansicht**: Filter/Sortierung nutzen, um Datensätze einzugrenzen — Spalteneinstellungen nicht dauerhaft verändern, außer fachlich gewünscht.
- **Aktion stets validieren**: nach Klick/Eingabe prüfen, ob die erwartete Maske/Reiter/Statusmeldung erscheint (`read_page`/`find`).
