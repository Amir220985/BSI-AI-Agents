# Prozessverwaltung & Geschäftsvorfälle

Navigationspfad: **Administration → Prozessverwaltung**
Quelle: BSI CRM Handbuch Admin Ocean FSR1, Kapitel 5 + Prozessschritte-PDF.

## Kernbegriffe

| Begriff | Bedeutung |
|---|---|
| **Prozess** | Vorlage/Definition des Ablaufs (Konfiguration) |
| **Geschäftsvorfall (GeVo)** | Instanz eines Prozesses — der laufende Fall, der bearbeitet wird |
| **Schritt** | Ein Baustein im Prozess (ca. 80 vorgefertigte Typen) |
| **Prozessgruppe** | Thematische Bündelung von Prozessen (z.B. Service, Verkauf, Marketing) |
| **Assistent (F7)** | Der UI-Einstieg für Benutzer, um Prozesse zu starten |
| **Eingangsassistent (F8)** | Alternativer Einstieg (z.B. bei eingehendem Anruf/E-Mail) |

## Prozess anlegen/bearbeiten
Administration → Prozessverwaltung → Prozesse

- **Prozessgruppe**: welche Gruppe
- **Verfügbarkeit**: Assistent (F7) / Eingangsassistent (F8) / beide
- **Ohne GeVo**: Assistent-only-Prozesse können ohne Geschäftsvorfall-Dokumentation laufen (z.B. vereinfachte Kommunikationserfassung)
- **Verantwortliches Team**: Virtuelles Team, das beim Job-Start eines GeVo den Verantwortlichen bestimmt
- **Texte**: Mehrsprachig (DE/EN/FR/IT)
- **Name + Synonyme**: erscheint in Prozessauswahl; Synonyme helfen bei der Suche

### Versionierung
- Immer nur **eine aktive Version** pro Prozess
- Bereits gestartete GeVos laufen auf alter Version weiter
- Neue GeVos folgen der neuen Version
- Versionen mit offenen GeVos: nur marginale Änderungen (z.B. Rechtschreibung)
- **Prozess duplizieren**: schnellste Art für ähnliche Prozesse
- **Prozess prüfen**: Validierung auf Fehler

## Prozess-Inputs
- Inputs aus dem aktuellen Kontext (z.B. Telefonnummer aus laufendem Telefonat)
- **Ausgewählt**: wird automatisch verknüpft beim Start
- **Pflicht**: Ohne diesen Input kann der Prozess nicht starten; fehlt er, wird automatisch ein Suchschritt eingefügt

## SLA-Konfiguration
- **Bearbeitungszeit 1**: → Status **Überfällig** (inkl. Servicezeiten der Servicelinie)
- **Bearbeitungszeit 2**: → Status **Eskaliert**; ggf. automatische Zuweisung entzogen
- **Warnung**: x% vor Ablauf (z.B. bei 80%)
- **Benachrichtigung**: Erfasser / aktueller Bearbeiter / spezielles Team
- **Automatische Zuweisung**: nach Eskalation per Regel neuen Verantwortlichen setzen
- Benutzer können individuell einstellen: E-Mail bei überfälligen/eskalierten GeVos

## Prozessattribute (Datenfelder)
- Alle BSI-CRM-Datentypen verwendbar
- Pro Schritt: Sichtbarkeit und Pflichtfeld-Status einzeln konfigurierbar
- Vorschlagswerte pro Prozess hinterlegbar
- Tipp: Bei abteilungsübergreifenden Prozessen Sichtbarkeit pro Schritt nutzen (Datenschutz)

## Schritt-Typen (Baukasten ~80 Schritte)

### Entitäten-Schritte
- **Entität suchen**: Suchmaske im Assistenten für gewählte Entität
- **Entität bearbeiten**: Maske im Bearbeitungsmodus öffnen
- **Neue Entität**: Erfassungsmaske für neuen Datensatz
- **Prozessinput suchen**: Suche + Prozessinput setzen
- **Person/Organisation deaktivieren**
- **Betreuung bearbeiten**: Erstellen/Bearbeiten von Betreuungen
- **Beziehung zu Organisation hinzufügen**
- **Firmen-Personen-Rollen bearbeiten**
- **Flag „Werbesperre" setzen**
- **Interesse bearbeiten**
- **Auftragsrollen bearbeiten**

### Ablaufsteuerung
- **Kachelschritt**: Kacheln zum Absprung auf Schritte oder zum Starten neuer GeVos
- **Gehe zu...**: Automatischer Sprung zu definiertem Schritt (Schleifen möglich)
- **Geschäftsvorfall manuell zuweisen**
- **Geschäftsvorfall starten**: Neuen GeVo erstellen (mit Prozess-Inputs übergeben)
- **Gestartete Geschäftsvorfälle abwarten**: Warten bis Sub-GeVos abgeschlossen
- **Prozessverzweigung**: Nur ein Ast wird ausgeführt (abhängig von Entscheidung); andere Äste unsichtbar

### Korrespondenz/Kommunikation
- **Ausgangskommunikation**: Kanalauswahl → Ausgangskommunikation; kann automatisiert werden
- **Benachrichtigung im Hintergrund**: E-Mail im Hintergrund an konfigurierten Empfänger
- **Telefonische Korrespondenz**: Telefonkommunikation führen; Wechsel zu schriftlich möglich

### Spezialschritte
- **Browser-Schritt**: Externe Webseite direkt im Schritt anzeigen (Parameter-Übergabe für direkten Sprung)
- **HTML-Informations-Schritt**: Gesprächsleitfaden, Links auf andere Schritte/Systeme
- **Kalender**: Kalender als Schritt im Assistenten
- **Kundenservice**: Daten erfassen + manuelle Eingriffe (zurückstellen mit Datum, weiterleiten an Team/Benutzer, abschließen mit Grund)
- **Löschen auf Verlangen**: Personen/Organisationen löschen (DSGVO-Anfrage); zeigt auch betroffene Entitäten und Aufbewahrungspflichten

## Sub-Geschäftsvorfälle
- Parallel-GeVos aus einem Haupt-GeVo starten
- **Schrittabschluss-Optionen**: Warten auf letzten gestarteten GeVo, auf alle GeVos, oder sofort
- **Wiedervorlage entfernen**: bei Abschluss jedes Sub-GeVo oder erst wenn alle fertig
- **Prozess-Inputs weitergeben**: Kontext (z.B. bereits gewählter Auftrag) wird mitgegeben

## Know-how
Administration → Prozessverwaltung → Know-how

- Wissensartikel mit Gültigkeit + Gültigkeitsende (→ löschen oder überarbeiten)
- **Thema**: erscheint in Know-how-Liste im Geschäftsvorfall
- **Beschreibung**: Word-Editor; Upload möglich; interne Verlinkungen auf andere Artikel via Link-Kennung
- **Verknüpfung mit Prozessen**: Hauptartikel (erster Platz, nur einer) oder Nebenartikel
- **Verantwortlicher**: Erhält Aufgabe wenn Gültigkeit endet

## Monitoring: GeVo-Status-Übersicht
Administration → Monitoring → Jobs: automatisierte Jobs überwachen (Schnittstellen, Reports, Regelwerk).

## Praxistipps

| Aufgabe | Vorgehen |
|---|---|
| Neuen Prozess anlegen | Erst alle Schritte anlegen, dann Verknüpfungen setzen |
| Ähnlichen Prozess | Bestehenden duplizieren, anpassen |
| Prozess testen | Neuen GeVo starten (Trial), Schritt für Schritt durchgehen |
| Schritt-Reihenfolge tauschen | Per Verschieben in Schritt-Liste |
| GeVo-Zuständigkeit einschränken | Checkbox „Zuständigkeit erzwingen" pro Schritt |
| Know-how zu Prozess zuordnen | Über Know-how-Maske → Reiter „Prozesse" verknüpfen |
