# Wissensbasis & Hilfe-Library

Schnell-Nachschlagewerk für die Live-Bedienung, aufgebaut aus der In-App-Hilfe (bsi.help), den Tutorials und Live-Erkundung (Trial, 2026-06-24). Ziel: schneller zum Ergebnis, weniger Blind-Klicken.

## Zuerst: In-App-Hilfe nutzen (bsi.help)
Bei Unsicherheit zu einem UI-Element **immer zuerst die eingebaute Hilfe** konsultieren, statt zu raten.
- **Hilfe-Menü** oben rechts in der Desktopleiste → öffnet das Panel **bsi.help**.
- **Suche** „Hilfe durchsuchen" — Stichwort-basiert (exakte Begriffe nötig; generische Begriffe liefern ggf. 0 Treffer).
- **Grüne „?"-Anker**: Sobald bsi.help offen ist, erscheinen an UI-Elementen grüne Fragezeichen — Klick führt direkt zur passenden Hilfe des Elements (der primäre, zuverlässigste Weg).
- **Tastatur**: **Shift + F1** öffnet die Hilfe schneller.
- **↗ (Portal)**: öffnet das vollständige Hilfeportal.
- **Tutorials** sind aus dem Hilfe-Panel verlinkt.

## Tutorials = sichere Lern-Sandbox
Hilfe → Tutorials. **Wichtig:** „Daten, die du im Tutorial erfasst oder änderst, sind nur im Tutorial sichtbar — du kannst keinen Schaden anrichten." Geführte Mehrschritt-Touren mit Glühbirne-Hinweis. Fortschritt wird **nicht** gespeichert; jederzeit „Tutorial abbrechen". 7 Tutorials:

| Tutorial | Dauer | Inhalt |
|---|---|---|
| Navigation | ~10 min | Grundbereiche, Sichten, Zurechtfinden |
| Suchen | ~15 min | Daten effizient/zielgenau finden |
| Erfassen | ~15 min | Daten erfassen & bestehende ändern |
| Anpassen | ~20 min | Tabellen/Einstellungen anpassen |
| Assistent | ~15 min | Geführte Prozesse anstossen |
| Assistent mit Prozessen | ~15 min | Geschäftsvorfälle schrittweise bearbeiten |
| Arbeitsvorrat | ~15 min | Anliegen im Arbeitsvorrat bearbeiten |

## Sichten-Katalog (Sichtenauswahl oben links)
Die **Sichtenauswahl** ist das Icon ganz oben links (Drop-down). Das Icon **wechselt je nach aktiver Sicht**. Verfügbare Sichten:

| Sicht | Zweck |
|---|---|
| **Cockpit** | 360°-Sicht des Benutzers — **nur Datensätze, die dich betreffen** (eigene verantwortete Geschäftsvorfälle, betreute Kunden, eigene Aufgaben) |
| **Customer Data** | **Alle** freigegebenen Daten — durchsuchbar über den Nav-Baum (Kunden, Organisationen, Personen, Aufträge, Geschäftsvorfälle, Kommunikationen, Aufgaben, E-Signatur-Vorgänge, Dokumente, Reports, Agent-Ausführungen) |
| **Sales** | Vertrieb (Leads/Opportunities/Aufträge) |
| **Marketing** | Aktionen, Kampagnen, Zielgruppen |
| **Service** | Tickets, Servicelinien, Geschäftsvorfälle |
| **Customer Insight** | Selektionen/Analysen (BSI Insight) |
| **Artificial Intelligence** | Brains/Cortexe, Customer Agents (BSI AI) |
| **Customer Experience** | Stories/Storyboards (BSI CX) |
| **Enterprise Integration** | Interfaces/Prozessoren (BSI EIP) |
| **Project Management** | Projektmanagement |
| **Administration** | Konfiguration (Entitäten, 360°-Sichten, Wertelisten, Benutzerverwaltung, Prozessverwaltung, Datenmodell, Jobs, …) — siehe [360-sicht-editor.md](360-sicht-editor.md) |

**Merksatz Umfang:** Cockpit = *meine* Daten, Customer Data = *alle* Daten. Für „nur eigene" → Cockpit-/Benutzer-Kontext; für „alle im System" → Customer Data/globale Quelle.

## Navigationsmodell
- **Desktopleiste** (oben): Sichtenauswahl · Globale Suche (Lupe) · Favoriten (Stern) · Fokus (Zielscheibe) · rechts Companion · Assistent · Telefon · Chat · Hilfe · Benutzerprofil.
- **Navigationsbaum** (links): je Sicht eigene Ordnerstruktur (z. B. Cockpit: ARBEIT, BETREUUNG, STORIES, KALENDER). Zähler-Badges zeigen Mengen.
- **Arbeitsbereich**: Tabellenansicht (Spalten, Sortierpfeile, Spalteneinstellungen) bzw. Kachel-/360°-Ansicht.
- **Werkzeugleiste** (unten): Suche · Diagramm · Karte · **Σ Summe** · Filter · Status; „X Zeilen geladen / Daten neu laden / Alle auswählen".

## Suchmasken (Beispiel Kunden)
Eine Entität öffnen → unten die **Suchmaske** mit Reitern: **Suche · Target · Marketing · Zuständigkeit · Erweitert · Kategorien**. Felder u. a. Name, Zusatzname, PLZ/Ort, Elektronische Adresse, Form, Volltext; rechts Aktiv, Betreuung, Letzte Kommunikation, **„Hat offene"** (Kommunikationen/Aufgaben/Aufträge/Tickets). Bei „Umfangreiche Datenmenge. Bitte Suche einschränken" → Kriterien verfeinern statt alles laden.

## Tiefen-Referenz: Produktspezifikation
Die offizielle, vollständige Doku ist die **Produktspezifikation BSI Customer Suite** (vertraulich). Grobe Themen-Landkarte zum schnellen Nachschlagen:

| Kapitel | Themen |
|---|---|
| 1 Kunden | Adressen, Bankverbindungen, Beziehungen, Datenschutz, Dubletten, Target/Next Best Action, Visitenkarte |
| 2 Aufträge | Capture Plan, Lead-/Opportunity-Mgmt, Lieferungen, Produkte, Projektmgmt, Zahlungen |
| 3 Kommunikationen | E-Mail (Bounce, Regeln), Telefon, SMS, Chat, Social Media, Brief/Fax, Besuch/Event |
| 4 Marketing | Aktionen (Challenger-/Kontrollgruppe), Kampagnen, Potenzial-/Reaktionsanalysen, Zielgruppen |
| 5 Arbeit | Aufgaben, Tickets, Cockpit, Kalender, Geschäftsvorfälle, SLA/Eskalation, Servicelinien, Stellvertretung |
| 6 Allgemeine Funktionen | Assistent, Companion, Dokumenterstellung (Word/Outlook-Add-in), Favoriten, Fokus, Suche (Globale Suche), Teilen, Tutorials |
| 7 Konfigurationen | 360°-Sichten (+Editor), Dokumentvorlagen, Individualisierung, Kacheltypen, Kennzahlen, Prozesse, Regelwerk, Wertelisten |
| 8 Daten (CDP) | AI/Cortex/Customer Agents, Customer Insight, Zeitmaschine, Picker (Formel/Tabelle/Kriterien), Reports |
| 10 Betrieb | Enterprise Integration, Jobs (System-Jobs), Parameter, Smoketests |
| 11 Benutzer | Interne Organisation, Organisationseinheit, Virtuelle Teams, Zugriffsrechte/Berechtigungen |
| 13 Benutzeroberfläche | Feld-/Spaltentypen, Kachelansichten, Menüs, Tastatur-Navigation, Rückfrage, System-Meldungen, Tabellen, Werkzeugleiste, Assistentenleiste, Dossiers |

> Bei einer konkreten Aufgabe: erst hier die Themen-Landkarte + [ui-navigation.md](ui-navigation.md) prüfen, dann gezielt in der UI navigieren und bei Element-Unsicherheit das grüne „?" der In-App-Hilfe nutzen.
