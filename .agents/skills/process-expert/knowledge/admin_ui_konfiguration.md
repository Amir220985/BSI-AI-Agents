# BSI Admin UI – Konfiguration via Browser-Automatisierung

> Erfahrungswissen aus direkter Arbeit im BSI Customer Suite Admin-Interface (Chrome MCP).
> Ergänzt die programmatische Prozesserstellung aus `process-expert/SKILL.md` um die
> manuelle Admin-UI-Perspektive.

---

## 1. Prozessverwaltung

### Navigation
`Administration → Prozessverwaltung → Prozesse → [Gruppe] → [Prozess]`

### Neuen Prozess anlegen
1. Rechtsklick auf Gruppe (z. B. „Service") → **Neu**
2. Felder im Tab **Allgemein**:
   - Name (de/en/…)
   - Prozessgruppe (Pflicht)
   - **Verantw. Team** → Pflichtfeld! Ohne Eintrag erscheint beim Speichern die Validation-Fehlermeldung: `Allgemein > Verantw. Team`. Beispielwert: `Kundendienst`
3. Tab **Verfügbar** – verfügbare Checkboxen:
   - ✅ Im Assistenten (= F7)
   - Im Schnellzugriff
   - Als Lambda
   - ⚠️ **F8 (Eingangsassistent) ist NICHT als Checkbox vorhanden.** Die Option fehlt im Verfügbar-Tab. F8-Konfiguration muss ggf. separat über das Input Management erfolgen.
4. Tab **Sichtbarkeit**: Gerätearten (Desktop ✓), Servicelinien, Rollen

### Prozess-Designer
- Aufruf: Bearbeitungs-Icon (Stift) am Prozess → Designer öffnet sich
- Toolbar: Speichern | Schließen | Zurücksetzen | Prozess-Einstellungen | Schritt bearbeiten | Schritt löschen | Gruppierung
- **Schritte hinzufügen**: Palette rechts → Suchfeld → Schritt auf Canvas ziehen
  - Kategorie „Kunde": Interesse bearbeiten, Kunde bearbeiten, Kunde erstellen, **Kunde suchen**, Kundendaten exportieren, Kundendupletten bearbeiten, Kundenrollen bearbeiten, Schnellerfassung
  - Kategorie „Korrespondenz": Korrespondenz erstellen (referenziert Dokumentvorlage)
- **Canvas-Block verschieben**:
  - ⚠️ `left_click_drag` via Chrome MCP (`mcp__Claude_in_Chrome`) funktioniert **nicht** für das Verschieben von Blöcken auf dem Canvas
  - Für Repositionierung: computer-use MCP (`mcp__computer-use__left_click_drag`) mit `request_access` für Chrome nutzen
- **Blöcke verbinden**: Ausgangsport eines Blocks (kleiner Kreis bei „Weiter") anklicken und auf Eingangsport des nächsten ziehen
- Minimap (unten rechts im Designer-Panel) zeigt relative Block-Positionen

### Prozess-Schritttypen im Designer (UI-Namen → Registry-Typ)
| UI-Name | Funktion |
|---|---|
| Kunde suchen | Kundentreffer-Suche (typeId: Kunde suchen) |
| Korrespondenz erstellen | Sendet E-Mail/Brief via Dokumentvorlage |
| Freier Schritt | Generische Aufgabe/Zwischenschritt |
| Start / Ende | Automatisch vorhanden; nicht löschbar |

---

## 2. Dokumentvorlagen

### Navigation
`Administration → Dokumentvorlagen → Neu (Plus-Icon)`

### Pflichtfelder beim Anlegen
| Feld | Wert / Hinweis |
|---|---|
| Typ | E-Mail |
| Format | Rich Text |
| Entität | Geschäftsvorfall |
| E-Mail-Betreff | Freitext |
| Vorlage (Body) | Rich-Text-Editor |

> ⚠️ Beim Ausfüllen nie Typ und Entität verwechseln – beide Felder sehen ähnlich aus. Den Entität-Wert immer erst nach dem Typ-Feld setzen.

### BSI Variablen (Merge Fields)
- Die BSI Variablen erscheinen im rechten Panel unter **BSI Variablen**
- Solange **Adressnutzung** nicht gesetzt ist, zeigen alle Kategorien `(0)` — Variablen sind leer
- **Workaround ohne Adressnutzung**: Platzhalter als Klartext schreiben, z. B. `[Anrede]` und `[Nachname]`, und später durch echte BSI-Variablen-Token ersetzen
- Adressnutzung setzen → dann Empfänger-Variablen (Anrede, Nachname, etc.) wählbar

### Beispiel-Vorlage: Bestätigung Anfrage Rückdeckung Haftpflicht
```
Betreff: Ihre Anfrage zur Rückdeckung Ihrer Haftpflichtversicherung

[Anrede] [Nachname],

vielen Dank für Ihre Anfrage zur Rückdeckung Ihrer Haftpflichtversicherung.
Wir haben Ihre Anfrage erhalten und werden uns in Kürze bei Ihnen melden.

Mit freundlichen Grüßen,
Ihr Kundendienst-Team
```

---

## 3. Chrome MCP – Gotchas & Lösungen

| Problem | Ursache | Lösung |
|---|---|---|
| Tab friert ein | BSI-Timeout oder langsames Laden | `select_browser` aufrufen, Screenshot erneut versuchen |
| `left_click_drag` bewegt Canvas-Block nicht | Chrome MCP Drag-Limitation bei SVG/Canvas | computer-use MCP verwenden (`mcp__computer-use__left_click_drag`) mit vorherigem `request_access` |
| Falsches Feld befüllt (Typ statt Entität) | Beide Felder ähneln sich | X-Button klicken → Feld zurücksetzen → korrekt neu befüllen |
| BSI Variablen zeigen (0) | Adressnutzung fehlt | Adressnutzung zuerst setzen oder Platzhalter-Workaround |
| Speichern schlägt fehl mit Pflichtfeld-Fehler | Verantw. Team nicht gesetzt | Im Tab Allgemein Verantw. Team befüllen (z. B. „Kundendienst") |
| F8 (Eingangsassistent) nicht sichtbar | Kein Checkbox im Verfügbar-Tab | Separate Konfiguration über Input Management erforderlich |

---

## 4. Empfohlene Reihenfolge beim Anlegen eines Prozesses

1. **Dokumentvorlage** zuerst anlegen (Typ E-Mail, Adressnutzung setzen, Variablen prüfen)
2. **Prozess anlegen**: Allgemein (Name, Gruppe, Verantw. Team), Verfügbar (F7/Schnellzugriff), Sichtbarkeit
3. **Prozess-Designer** öffnen und Schritte in dieser Reihenfolge einfügen:
   - Start (bereits vorhanden)
   - Kunde suchen (Kategorie „Kunde")
   - Anfrage erfassen (Freier Schritt)
   - Korrespondenz erstellen (referenziert die Dokumentvorlage)
   - Abschließen/Weiterleiten (Freier Schritt oder Aufgabe erstellen)
   - Ende (bereits vorhanden)
4. Schritte miteinander verbinden (Weiter-Ports)
5. Speichern → Version 0.0.1 (Aktiv)
