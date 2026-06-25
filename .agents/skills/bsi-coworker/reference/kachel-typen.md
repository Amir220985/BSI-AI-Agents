# Kachel-Typen — Vollständiger Katalog

Alle verfügbaren Kacheltypen für 360°-Sichten (validiert aus BSI CRM Handbuch Admin Ocean FSR1).
Workflow zum Hinzufügen: → [360-sicht-editor.md](360-sicht-editor.md)

## Übersicht aller Typen

| Kacheltyp | Zweck | Wann verwenden |
|---|---|---|
| **Attribute** | Felder des Datensatzes zeigen (Adresse, Betreuer, Projekleiter) | Stammdaten, Key-Facts auf einen Blick |
| **Bild** | Portrait oder Kunden-Logo | Kundenfoto, Firmenlogo |
| **Chatverlauf** | Chat-Kommunikationshistorie | Contact Center |
| **Diagramm** | Balken, Linien oder Kreisdiagramm | Kommunikationen pro Kanal, Aufträge nach Status |
| **Erfüllungsgrad** | Prozentuale Erfüllung als Tachometer | Bearbeitungsquote, Besuchsanteil, Rechnungsstatus |
| **Formatierter Text** | Strukturierter Fließtext | Freitext-Notizen, Beschreibungen |
| **Graph** | Netzwerkdarstellung | Beziehungsnetzwerke |
| **Graph hierarchische Kundenbeziehung** | Konzern-/Firmen-Hierarchie grafisch | Konzernstrukturen |
| **HTML** | Freie HTML-Gestaltung | Attribute in einer Zeile, Bilder, Hintergrundfarbe, komplexe Layouts |
| **Liste** | Tabelle mit Einträgen | Letzte Kommunikationen, laufende Verträge, offene GeVos |
| **Platzhalter** | Leerer Slot, der Platz belegt | Abstände zwischen Kacheln erzwingen |
| **Rating** | Bewertungsanzeige | Kundenbewertung, NPS |
| **Sales Funnel** | Trichter mit Konversionsraten | Auftragsstatus-Übersicht, Pipeline |
| **Schaltfläche** | Klickbarer Button → Prozess starten | Schnellzugriff auf häufige Prozesse (Kommunikation anlegen, Aufgabe erstellen) |
| **Schaltfläche Bearbeiten** | Datensatz direkt bearbeiten | Schnellbearbeitung ohne Vollmaske |
| **Schaltfläche Dokument erstellen** | Dokumentvorlage aufrufen | Newsletter, Terminbestätigung, Vertragsdokument |
| **Schaltfläche Webseite öffnen** | Externe URL öffnen (neuer Tab) | Sendungsverfolgung, Intranet, externe Daten |
| **Stories** | BSI CX Stories anzeigen | Nur mit BSI CX relevant |
| **Tabelle** | Mehrspaltentabelle mit konfigurierbaren Spalten | Detaillierte Listen (breiter als Liste-Kachel) |
| **Timeline-Kachel** | Zeitstrahl von Ereignissen | Kommunikationshistorie zeitlich |
| **Donut-Kachel** | Kreisdiagramm als Donut | Anteilsverteilungen |
| **Venn-Diagramm** | Schnittmenge dreier Kriterien | Zielgruppen-Analyse, Segmentüberschneidung |
| **Visitenkarte** | Kopfdaten des Kunden | Name, Adresse, Bild auf einen Blick |
| **Webseite** | Externe Webseite eingebettet (iframe) | Social Media, externe CRM-Systeme |
| **Zeiger** | Tachometer-Nadel für eine Kennzahl | Absprungwahrscheinlichkeit, Verkaufsintensität, Besuche |

## Detailkonfiguration wichtiger Typen

### Attribute
- Attributname-Position: Links, Oben oder Keine
- Aktion bei Klick: Webseite öffnen, E-Mail schicken, etc.
- Eigene Bezeichnung überschreibbar

### Diagramm
- Diagrammart: Balken / Linien / Kreisdiagramm
- Legende: rechts / unten / keine
- Entität wählen (z.B. Kommunikationen) + Kriterien einschränken
- X-Achse, Gruppierung (Monat/Quartal/Jahr), Konsolidiert (alle Januar zusammen = ein Balken)
- Datenreihe: Eine (Anzahl) oder Mehrere (aufgeschlüsselt nach Attribut, z.B. Kanal)
- Y-Achse: Anzahl oder Menge (summierbares Attribut)

### Erfüllungsgrad
- Wert für Erfüllungsgrad (Zähler) wählen
- Total/100%-Wert wählen
- Beispiel: Erledigte Aufgaben / Alle Aufgaben

### Liste
- Listenart: Aufzählung (Bullet) / Titel (erste Zeile größer) / Standard (kein Bullet)
- Checkbox: Anzahl der Listeneinträge oben anzeigen
- Entität + Kriterien + Spalten konfigurieren

### Sales Funnel
- Balkengröße gemäß Werten (proportional) oder dekorativ (oben groß → unten klein)
- Konversionsrate anzeigen: Prozent zwischen Balken
- Pro Balken: 1. Wert (z.B. Anzahl Aufträge) + 2. Wert (z.B. Nettopreis)

### Schaltfläche
- Icon wählen
- Prozess verknüpfen (startet Assistent beim Klick)

### Tabelle
- Entität wählen (z.B. Aufträge)
- Kriterien einschränken (z.B. nur eigene)
- Spalten + Sortierung + Sortierreihenfolge

### Venn-Diagramm
- Entität (z.B. betreute Kunden)
- Drei Kriterien-Sets mit Bezeichnung (z.B. A-Kunden / Besuch <6M / Potenzial >10k)

### Zeiger
- Grüner Bereich: links / rechts / Mitte
- Wert für Zeiger (Kennzahl)
- Wertebereich (Min-Max)

### Webseite vs. Schaltfläche Webseite
- **Webseite**: Eingebettet als iframe direkt in der Kachel — bei externer URL mit Variablen
- **Schaltfläche Webseite öffnen**: Öffnet externe URL in neuem Tab (kein iframe)
- Variablen in URL möglich (z.B. Firmenname, Kundennummer)

## Farbschemata
Für alle Kacheln verfügbar:
- **Blau (invertiert)**: Blaue Grafik auf blauem Grund / weiße Schrift
- **Braun (invertiert)**: Braune Grafik auf braunem Grund / weiße Schrift
- **Blau**: Blaue Grafik auf weißem Grund
- **Braun**: Braune Grafik auf weißem Grund
- **Regenbogen**: Farbige Grafik auf weißem Grund

## Kachel-Einstellungen (gelten für alle Typen)
- **Farbschema** (s.o.)
- **Titel**: anzeigen oder ausblenden, mehrsprachig (DE/EN/FR/IT)
- **Sichtbar**: nur für Cockpit — ob Benutzer Kachel schon beim Login sieht oder erst aktivieren muss
- **Positionierung**: Spalte + Zeile im Raster (beliebig viele Spalten/Zeilen möglich)
- **Fixiert**: Kachel kann vom Benutzer nicht verschoben werden
