# Administration — Konfigurationsbereich

Navigationspfad: **Sichtenauswahl → Administration → Konfiguration**
Quelle: BSI CRM Handbuch Admin Ocean FSR1, Kapitel 4.

## Übersicht Konfigurationsbereich

| Bereich | Pfad | Zweck |
|---|---|---|
| **360°-Sichten** | Administration → Konfiguration → (Entität auswählen) | Kachel-Layout pro Entität konfigurieren |
| **Masken** | Administration → Konfiguration → Masken | Formularfelder anpassen |
| **Suchmasken** | Administration → Konfiguration → Suchmasken | Suchfelder pro Entität erweitern |
| **Indizes** | Administration → Konfiguration → Indizes | Volltextsuche (Apache Lucene) — technisch |
| **Datenmodell** | Administration → Konfiguration → Datenmodell | Attribut-Sichtbarkeit pro Rolle steuern |
| **Tabellen** | Administration → Konfiguration → Tabellen | Standard-Tabellenansichten definieren |
| **Reports** | Administration → Konfiguration → Reports | Reports mit Suchbedingungen + Spalten |
| **Kennzahlen** | Administration → Konfiguration → Kennzahlen | KPIs definieren (DWH-ähnlich) |
| **Performance Management** | Administration → Konfiguration → Performance Management | Soll-/Ist-Vergleiche |

---

## 360°-Sichten

Vollständige Dokumentation: [360-sicht-editor.md](360-sicht-editor.md) + [kachel-typen.md](kachel-typen.md)

Neue 360°-Sicht anlegen:
1. Entität auswählen → Neue 360°-Sicht über Menüzeile
2. Name (= Reiterbezeichnung beim Benutzer)
3. Sichtbarkeit: Desktop / Tablet / Mobile
4. Aktiv/Inaktiv
5. **Kriterien**: für welche Datensätze sichtbar (z.B. nur A-Kunden)
6. **Benutzerfilter**: nur für bestimmte Rollen/Benutzer
7. **Reihenfolge**: bestimmt Reiter-Position wenn mehrere Sichten passen
→ Alle zutreffenden Sichten werden als Reiter angezeigt

Entitäten mit 360°-Sichten: Kunden, Aktionen, Kampagnen, Aufträge, Geschäftsvorfälle, weitere.

---

## Masken

Administration → Konfiguration → Masken (z.B. Person, Organisation, Kommunikation, Produkt, Kampagne)

Aktionen in der Vorschau (live):
- Neues **Feld** nach ausgewähltem Feld einfügen (nach oder innerhalb Gruppe)
- **Feldgruppe**: Gruppierung mehrerer Felder (Sichtbarkeit als Ganzes steuerbar)
- **Reitergruppe**: Element mit Reitern; jeder Reiter = eine Feldgruppe

### Feldarten
| Art | Besonderheit |
|---|---|
| Checkbox | Keine weiteren Optionen |
| Datum (mit/ohne Zeit) | Versatzregel möglich (z.B. Nachfassdatum = Startdatum + 3 Tage) |
| Text | Regex-Regel, Min-/Max-Länge, Rechtschreibprüfung |
| Werteliste (einfach/Mehrfach) | Werteliste wählen oder andere Entität verknüpfen |
| Zahl (mit/ohne Nachkomma) | Zahlenbereich (von…bis) |

### Feld-Optionen
- **SQL**: DB-Spaltenname überschreiben
- **Index**: für Volltextsuche berücksichtigen
- **Pflichtfeld**: Speichern erzwingt Ausfüllen
- **Wert eindeutig**: Duplikat-Prüfung beim Speichern
- **Mehrfachauswahl für Suche**: Liste statt Smartfield in Suche
- **Feldname im Feld anzeigen**: Placeholder-Text
- **Anzahl Zeilen/Spalten**: Breite 1 = halbe Maske, 2 = volle Maske

---

## Suchmasken

Administration → Konfiguration → Suchmasken

- Wie Masken konfigurierbar: Felder hinzufügen, Suchkriterien erweitern
- Tooltips können mehrsprachig vergeben werden (überschreiben Standard-Tooltips)
- Gilt auch für Kacheln, Spalten, Reports und prozessspezifische Infos im Kundenservice-Schritt

---

## Datenmodell

Administration → Konfiguration → Datenmodell

- Alle Attribute pro Entität sichtbar (mit Verknüpfungen zu anderen Entitäten)
- **Sichtbarkeit pro Rolle**: Attribute ein-/ausblenden für bestimmte Rollen (ohne Rechteverlust)
- Tiefe Abfragen: Attribut-Beziehungen zwischen Entitäten im logischen Modell

---

## Tabellen

Administration → Konfiguration → Tabellen

- Standard-Listensichten für diverse Entitäten definieren
- Alle Entitäten, Felder, Verknüpfungen und Operatoren verfügbar
- Benutzer sehen diese als Standardsicht (kann individuell überschrieben werden)

---

## Reports

Administration → Konfiguration → Reports

- Report anlegen: Entität wählen → Suchbedingungen → Spalten konfigurieren
- Einschränken: für welche Benutzer sichtbar und aktiv (Aktiv/Sichtbar/Editierbar-Logik)
- Benutzer sehen Reports unter ihrer Sicht unter „Eigene Reports"

---

## Kennzahlen

Administration → Konfiguration → Kennzahlen

- Analog Datawarehouse-KPIs direkt in BSI CRM
- Einfach: „erfasste Aufgaben pro Verkäufer"
- Komplex: „Summe der Offerten pro Verkäufer im Segment A" (SQL-Kenntnisse nötig)
- Berechnung via Job (zeitgesteuert) oder manuell nachberechnen
- Verwendung: Dokumente, Performance Management Reports, Datenpicker in 360°-Sichten

---

## Regelwerk

Administration → Regelwerk (Kapitel 7)

Automatische Logik ohne Programmierung. Beispiele: Segmentierung, Status-Trigger, Daten-Bereinigung.

### Konfiguration einer Regel
- **Entität**: z.B. Organisation, Auftrag, Kommunikation
- **Ausführungszeitpunkt**:
  - Manuell
  - Zeitgesteuert (mit Wiederholung: immer oder einmal pro Datensatz)
  - **Trigger**: beim Ändern des Datensatzes (z.B. „wenn Status auf Lieferung gesetzt wird")
- Trigger-Optionen: beim Erstellen / beim Bearbeiten / beides

### Filter
- Filterset nach Prinzip der erweiterten Suche
- Vorschau: zeigt alle Datensätze, auf die Regel zutrifft

### Operationen (pro Datensatz, in Reihenfolge ausgeführt)
- Datensatz ändern
- Datensatz erstellen
- E-Mail versenden
- Geschäftsvorfall erstellen
- SMS versenden
- Zum Marketing-Review hinzufügen

### Log-Bereinigung
- Aufbewahrung pro Status (OK / Warnung / Fehler) separat konfigurierbar
- Optionen: alle löschen / letzte n Läufe behalten / letzte n Tage behalten

### Monitoring → Regelwerk
Administration → Monitoring → Regelwerk → Regeln: zeigt alle aktiven Regeln + Ausführungslog

---

## Datenschutz

Administration → Datenschutz

- **Aufbewahrungspflichten**: Regeln für gesetzlich vorgeschriebene Datenhaltung (Entität + Dauer + Filter)
- **Datenschutzregeln**: Automatisches Sperren oder Löschen nach Regeln
  - Gesperrt = nicht mehr sichtbar (außer mit Spezialrecht); rückgängig machbar
  - Gelöscht = physikalisch weg (anonymisierte Referenzen bleiben); **nicht rückgängig machbar**
  - Simulator: zukünftiges Datum wählen → prüfen, was dann gelöscht/gesperrt würde
- **Datenschutzsperren**: Liste aller aktuell gesperrten Elemente

---

## Texte & Parameter

### Texte
Administration → Texte: Alle UI-Applikationstexte überschreibbar (pro Sprache). Ersetzungsregel-Reihenfolge wichtig; letzte Checkbox verhindert Kettenersetzungen.

### Parameter
Administration → Parameter: Systemweite Einstellungen (meist BSI-vorgegeben).
- Max. Anzahl Zeilen (Web/Mobile, pro Rolle verfeinerbar)
- Standard-E-Mail-Programm, Standard-Eingangskanal, Standard-Kilometersatz
- Rote Markierung = fehlende Pflichteinstellungen

---

## Monitoring

Administration → Monitoring

| Bereich | Inhalt |
|---|---|
| **Verarbeitungen** | Jobs auf Zielgruppenselektionen, Potenzialanalysen |
| **Jobs** | Automatisierte Jobs: aktiv? Nächster/letzter Lauf? (Schnittstellen, Reports, Regelwerk) |
| **Cluster** | Aktive Knoten; Cache-Status; manuell neu laden |
| **Cluster Locks** | Verhindert Mehrfach-Ausführung; bei hängendem Knoten manuell löschen |
| **Profiler** | Performance-Bottlenecks; Ctrl+Alt+P / Ctrl+Alt+Shift+P |
| **Regelwerk** | Aktive Regeln |
| **Gesperrte Objekte** | Masken, die nicht korrekt geschlossen wurden → Sperre löschen |
| **Smoketests** | Systemtests + Ergebnis |
| **Tutorials** | Welcher Benutzer hat wann welches Tutorial abgeschlossen |
