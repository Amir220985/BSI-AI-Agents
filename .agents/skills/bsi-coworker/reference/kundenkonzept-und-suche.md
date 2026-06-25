# Kundenkonzept, Dossier & Suche

Quelle: BSI CRM Handbuch Basics Ocean FSR1, Kapitel 2–7.

## Kundenkonzept

### Kundenformen
- **Organisation** (Firma, Verein, Konzern)
- **Person** (Privatperson, Ansprechpartner)
- **Familie** / weitere Formen je nach Konfiguration

Die 360°-Sicht und das Dossier zeigen immer alle zugehörigen Kunden auf einmal (z.B. Familie + alle Familienmitglieder).

### Beziehungstypen

| Typ | Beschreibung | Beispiele |
|---|---|---|
| **Gruppe/Mitglied** | Gerichtete hierarchische Beziehung | Konzern ↔ Tochtergesellschaft, Firma ↔ Mitarbeiter, Familie ↔ Mitglieder |
| **Netzwerk** | Nicht-gerichtet, gleichwertig | Duplikat-Markierung (wenn Zusammenlegung nicht möglich) |

Beziehungen können Zusatzinformationen tragen (z.B. Stellenbezeichnung, Beteiligungsanteil).

---

## Dossier

- Jeder Datensatz existiert **genau einmal** in BSI CRM
- Doppelklick auf Datensatz → öffnet Dossier im Navigationsbaum + 360°-Sicht im Arbeitsbereich
- Gilt für: Person, Organisation, Auftrag, Geschäftsvorfall, Kommunikation, Beziehung, …
- Egal wie man zum Datensatz gelangt (Suche, Navigationsbaum, Verknüpfung) → immer dasselbe Dossier

### Verknüpfte Datensätze im Navigationsbaum (Beispiel Organisation)
- **Beziehungen**: Alle verknüpften Personen (Ansprechpartner)
- **Aufträge**: Alle Aufträge, Potenziale, Angebote, Anträge
- **Geschäftsvorfälle**: Alle GeVos + Status (In Arbeit / Abgeschlossen / Überfällig / Eskaliert)
- **Kommunikationen**: Gesamte Kommunikationshistorie (Besuche, Telefon, E-Mail, Brief, Fax)
- **Aufgaben**: Alle Aufgaben zu diesem Kunden (z.B. Nachfasstermine)

---

## Suche

### Globale Suche (Lupen-Icon oben links)
- Sucht über **alle Daten gleichzeitig**: Organisationen, Personen, Aufträge, ...
- Treffer im Navigationsbaum; Drill-down → sofortiger Zugriff auf Dossier, 360°-Sicht, Bearbeitung, GeVos
- Schnellste Möglichkeit für bekannte Namen/Begriffe

### Einfache & Detaillierte Suche (pro Ordner)
- Lupen-Symbol **unterhalb** der Tabellenansicht
- Reiter: Suche / Target / Marketing / Zuständigkeit / Erweitert / Kategorien
- Felder: Name, Zusatzname, PLZ/Ort, Elektronische Adresse, Form, Volltext
- Rechts: Aktiv, Betreuung, Letzte Kommunikation, **„Hat offene"** (Kommunikationen/Aufgaben/Aufträge/Tickets)
- Mehrere Felder = **UND-Verknüpfung**
- Grauer Balken an Reitern = dort sind Kriterien aktiv
- Ergebnis-Freitext-Filter: filtert **alle** Attribute der Treffer (z.B. „car" findet „Carmen" und „Carekix")
- Sicht Arbeit = nur eigene Daten; Sicht Daten = alle berechtigten Daten
- **Warnung**: „Umfangreiche Datenmenge. Bitte Suche einschränken" → Kriterien verfeinern

### Erweiterte Suche (Reiter „Erweitert")
Für komplexe Queries mit Verknüpfungen über Entitätsgrenzen:
- **UND / ODER / Entweder-Oder** kombinierbar
- **Negieren** von Kriterien möglich
- **Relationale Suche**: z.B. Personen mit einem bestimmten Auftragstyp oder mit einer Beschwerde
- **Wertebereich**: von … bis (z.B. Datum, Preis)
- **Relative Datumsangaben**: in den nächsten n Tagen
- **Aggregationen**: Summe, Maximum, Anzahl als Suchkriterium

### Kategorien
- Datensätze aus verschiedenen Entitäten mit Tags versehen (quer durch Organisation/Person/Auftrag)
- Als Suchkriterium verwendbar
- **Kategorien verwalten**: Ordner + Kategorien anlegen, Farbe + Name, Freigabe für Teams/OE/Benutzer
- Anzahl der Verknüpfungen sichtbar; Verknüpfungen hier auch löschbar

---

## Daten anzeigen

### Tabellenansicht
- **Sortieren**: auf-/absteigend per Spaltenklick; Mehrfachsortierung möglich
- **Gruppieren**: nach Spalte gruppieren → Summen bei Zahlenspalten (z.B. Nettopreis pro Verkäufer)
- **Filtern**: Spaltenfilter für bestimmte Werte (z.B. nur Aufträge von Verkäufer X)
- **Aggregierung**: Summe / Durchschnitt / Minimum / Maximum pro Gruppe
- **Einfärbung**: Farbverlauf oder Balken

### Grafiken (unterhalb der Tabelle)
- Kuchendiagramm-Symbol → Diagrammansicht
- Diagrammtyp, Achsen wählen
- Grafiken sind **interaktiv**: Klick auf Element filtert die Tabelle; Ctrl = Mehrfachauswahl
- **Kartenansicht**: bei geografischen Daten (angepasst: Vertriebsregionen, Kantone, Generalagenturen)
- Filter aus Diagramm entfernen über Statuszeile

### Spalten organisieren
- Reihenfolge per Drag-and-drop oder Spaltenmenü (Zahnrad)
- Einstellungen werden gespeichert (auch nach Neustart)
- Werkeinstellungen jederzeit ladenar
- **Eigene Spalten hinzufügen** (+): alle Attribute der Entität + verknüpfte Daten (z.B. Anzahl Kommunikationen)

### Teilen/Exportieren
- **Excel-Export**: aktuelle Spalten + Spalteneinstellungen
- **Zwischenablage**: aktuelle Zeilen kopieren
- **vCard-Export**: aktuelle Auswahl
- **Favorit speichern**: aktuelle Ansicht als Favorit
- **Startsicht festlegen**: diese Tabellenansicht beim CRM-Start immer laden

---

## Navigationskonzept (Merksatz)

> In BSI CRM funktioniert **Gleiches immer gleich**. Icons und Menüs sind konsistent.

- **Einfachklick** auf Ordner im Navigationsbaum: zeigt Daten im Arbeitsbereich (Tabellenansicht)
- **Doppelklick** auf Ordner: öffnet Dossier
- **Doppelklick** auf Datensatz in Tabelle: öffnet Dossier des Datensatzes
- **Menüzeile** oben: Verfügbare Befehle für den aktuellen Datensatz/Kontext (kontextsensitiv)
- Weitere Masken öffnen sich als **Reiter** (nicht als Popup) — Reiter wechseln möglich

---

## Cockpit vs. Daten-Sicht

| Sicht | Frühere Bezeichnung | Daten |
|---|---|---|
| Cockpit / Arbeit | „Arbeit" | Nur Datensätze, die mit dem Benutzer verknüpft sind (eigene Kunden, eigene GeVos, eigene Aufgaben) |
| Customer Data / Daten | „Daten" | Alle berechtigten Datensätze im System |

**Neuigkeiten** (in Cockpit): Liste von Datensätzen, die sich geändert haben und mit mir verknüpft sind. „Als gelesen markieren" entfernt sie.

**Betreuung** (in Cockpit): Eigene Kunden, Ansprechpartner, Aufträge.

**Kalender**: BSI CRM Aufgaben + Outlook-Termine integriert.
