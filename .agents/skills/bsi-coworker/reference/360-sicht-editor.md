# 360°-Sicht-Editor — Kacheln live konfigurieren

Praxiswissen zum Bearbeiten von 360°-Sichten (Cockpit & Co.) direkt in der Weboberfläche. Validiert am 2026-06-24 auf einer Trial-Instanz (Kachel „offene GeVos" auf das Benutzer-Cockpit).

## Navigationspfad (Beispiel: Benutzer-Cockpit)
1. **Sichtenauswahl** (Icon oben links in der Desktopleiste) → **Administration**.
2. Administration → Kachel/Baumknoten **Entitäten**.
3. Entität öffnen (Doppelklick) — z. B. **Benutzer**. Achtung: Zeilenhöhe beachten, sonst öffnet man die Nachbarzeile. Bei Unsicherheit erst **filtern** (Feld „Filtern nach…" unten).
4. Im Entitäts-Baum: **360°-Sichten** aufklappen → gewünschte Sicht (z. B. **Cockpit**) per Doppelklick öffnen.
5. Es öffnet sich die 360°-Sicht-Vorschau mit Toolbar **„360°-Sicht bearbeiten"**.

> Die Cockpit-Reiter der Live-Sicht (Cockpit, Status, Entwicklung, Analyse, Arbeit, Heutige Besuche) entsprechen je einer 360°-Sicht-Konfiguration der **Benutzer**-Entität (`Reihenfolge` steuert die Reiter-Position).

## Editor-Bedienung
- **„360°-Sicht bearbeiten"** öffnet den Bearbeiten-Modus: Toolbar **Speichern · Schließen · Einstellungen · Bearbeiten · Anzahl Spalten · Komplette Größe verwenden · Undo/Redo**.
- Rechts die **Kachel-Bibliothek** (mit Filter). Kacheltypen: Attribute, Bild, Chatverlauf, Diagramm, Erfüllungsgrad, Formatierter Text, HTML, Liste, Platzhalter, Rating, Sales Funnel, Schaltfläche, Schaltflächen, Stapel, Tabelle, Venn-Diagramm, Visitenkarte, Webseite, Zeiger.
- **Kachel hinzufügen** = Kacheltyp aus der Palette per **Drag & Drop** auf einen freien **Slot** im Raster ziehen. Leere Slots (gestrichelte Kästen) erscheinen **unter** den bestehenden Kacheln — dorthin scrollen, dann ablegen.
- **Kachel konfigurieren**: Kachel selektieren → Toolbar **„Bearbeiten"** (oder Doppelklick). Dialog: links **Attribute/Inhalt**, rechts **Allgemein** (Titel je Sprache DE/EN/FR/IT, „Kein Titel", „Sichtbar", „Fixiert", „Farbschema"). Mit **OK** bestätigen.
- **Ansicht-Umschalter** unten rechts: **Design** (Platzhalter „Lorem ipsum") vs. **Vorschau** (echte Werte). Für echte Werte in der Vorschau zusätzlich unten den **Benutzer** wählen — Kennzahlen werden **pro Benutzer** berechnet.

## Werte/Attribute binden — Datenpicker
Beim Hinzufügen eines Attributs („Neues Attribut") öffnet der **Datenpicker** mit der Kontext-Entität (z. B. Benutzer). Modi oben: **Liste**, **fx (Formel)**, **Relations-Pfad**. Kategorien links: Top-Elemente, **Kennzahlen**, Sonstige, **Zuständigkeit**, Variablen, Fixe Werte.
- **Suchfeld** nutzen (z. B. „Geschäftsvorf") — liefert Treffer gruppiert nach Kategorie inkl. Relations-Pfaden (`Benutzer › Geschäftsvorfälle offen`) und Kennzahlen.
- Element markieren → **„Wählen"** klicken. Wenn ein Pixelklick auf „Wählen" nicht greift: Element-Referenz via `find` holen und per `ref` klicken.

### WICHTIG: Anzahl-Aggregation für Zählungen
Eine **Kennzahl** (z. B. „Geschäftsvorfälle offen") liefert **nicht automatisch eine Ganzzahl**. Bindet man nur die Kennzahl, rendert die Kachel einen Dezimal-/Aggregatwert (Symptom: Anzeige wie „1,1" statt einer sauberen Zahl). Für eine **Anzahl** muss im Datenpicker explizit die **Anzahl**-Aggregation gewählt werden — dann zeigt die Kachel z. B. „Anzahl 42". Bei „Anzahl X" gewünscht also immer prüfen, dass die Aggregation **Anzahl** gesetzt ist, nicht nur die Kennzahl.

### Kontext = Umfang
Im **Benutzer**-Kontext sind Relationen/Kennzahlen wie „Geschäftsvorfälle offen" automatisch **die des angemeldeten Benutzers** (= „nur eigene"). Für „alle im System" braucht es eine andere Quelle (z. B. eine globale Kennzahl/Selektion), nicht die benutzerbezogene Relation.

## Speichern & Sicherheit (Safety-Gate)
- **Speichern** ist der einzige verändernde Schritt — er persistiert die Konfiguration **für alle Nutzer dieser 360°-Sicht**. Davor **Freigabe** einholen (→ [safety-guardrails.md](safety-guardrails.md)).
- **Schließen ohne Speichern verwirft** alle Änderungen (Dry-Run/Preview kostenlos: erst im Editor aufbauen, in der Vorschau prüfen, dann erst speichern).
- Nach dem Speichern **Schließen** → man landet auf der Live-Sicht; Ergebnis dort verifizieren. Live zeigt den echten Per-User-Wert (kann vom Editor-Preview abweichen, der einen aggregierten/anderen Kontext zeigen kann).
