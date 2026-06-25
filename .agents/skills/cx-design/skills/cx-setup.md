# cx-setup — BSI CX Kundenprojekt einrichten

Richtet ein neues BSI CX Kundenprojekt ein: GitHub-Release herunterladen, entpacken, npm install, Kunden-URL ermitteln, Styleguide anwenden, Elemente anpassen.

Dieser Skill wird von `.agents/skills/cx-design/SKILL.md` geladen — nie direkt aufrufen.

---

## SCHRITT 1 — GitHub-Release auswählen und herunterladen

Rufe die GitHub Releases API ab um verfügbare Versionen zu ermitteln:

```
https://api.github.com/repos/bsi-software/bsi-cx-design-master-template-web/releases
```

Liste dem Benutzer die letzten 5 verfügbaren Versionen auf (tag_name + Veröffentlichungsdatum). Frage dann:

> "Welche Version soll heruntergeladen werden? [Versionsnummer eingeben oder Enter für die neueste: X.X.X]"

Ermittle aus der gewählten Release die Source-ZIP-URL (das Asset mit `Source code (zip)` bzw. die `zipball_url` der Release). Lade die ZIP in den Downloads-Ordner des Benutzers herunter:

```powershell
$downloads = [Environment]::GetFolderPath("UserProfile") + "\Downloads"
$dest = "$downloads\bsi-cx-master-template-[VERSION].zip"
Invoke-WebRequest -Uri "[ZIP_URL]" -OutFile $dest
```

Bestätige dem Benutzer den Download-Pfad.

---

## SCHRITT 2 — Zielordner festlegen

Frage den Benutzer:

> "In welchen Ordner soll das Projekt entpackt werden? Bitte vollständigen Pfad eingeben:"

Schlage als Beispiel vor (generisch, Platzhalter in eckigen Klammern ersetzen):
`C:\Users\[Benutzername]\Documents\cx-[Kundenname]`

Den Benutzernamen dynamisch ermitteln:
```powershell
$env:USERNAME
```

Merke den eingegebenen Pfad als `$ZIELORDNER`. Prüfe ob der Pfad syntaktisch gültig ist. Falls nicht: erneut fragen.

---

## SCHRITT 3 — ZIP entpacken

```powershell
if (-not (Test-Path "$ZIELORDNER")) {
    New-Item -ItemType Directory -Path "$ZIELORDNER" | Out-Null
}
Expand-Archive -Path "$ZIP_PFAD" -DestinationPath "$ZIELORDNER" -Force
```

Prüfe nach dem Entpacken die Verzeichnisstruktur:
- Enthält `$ZIELORDNER` einen einzelnen Unterordner (z.B. `bsi-cx-design-master-template-web-1.3.11/`)? → Das ist der eigentliche Projektordner — aktualisiere `$ZIELORDNER` auf diesen Unterordner.
- Enthält er direkt `package.json`? → `$ZIELORDNER` ist bereits korrekt.

Bestätige dem Benutzer:
> "ZIP erfolgreich entpackt nach: [ZIELORDNER]"

---

## SCHRITT 4 — Node.js prüfen und npm install

### 4.1 Node.js-Version prüfen

```powershell
$nodeRaw = node --version 2>$null
if (-not $nodeRaw) {
    Write-Host "nicht installiert"
} else {
    $major = [int]($nodeRaw -replace 'v(\d+)\..*', '$1')
    Write-Host "$nodeRaw | major=$major"
}
```

Bewerte das Ergebnis:

| Ergebnis | Verhalten |
|---|---|
| Node.js nicht gefunden | Abbrechen. Meldung: "Node.js ist nicht installiert. Bitte Node.js v22 von https://nodejs.org installieren." |
| Major <= 22 | OK. Meldung: "Node.js $nodeRaw — Version geprüft, alles in Ordnung." |
| Major > 22 | Abbrechen. Meldung: "Node.js $nodeRaw ist zu neu. Bitte Node.js v22 verwenden (https://nodejs.org). Neuere Versionen sind mit diesem Projekt nicht getestet." |

### 4.2 npm install ausführen

```powershell
cd "$ZIELORDNER"
npm install
```

- Warte auf Abschluss
- Bei Fehler (Exit-Code != 0): Fehlermeldung ausgeben — frage ob trotzdem fortgefahren werden soll

---

## SCHRITT 5 — Projektname festlegen und webpack.config.js anpassen

### 5.1 Projektname abfragen

Frage den Benutzer:
> "Wie soll das Kundenprojekt heißen? (Dieser Name ersetzt 'master' in allen Build-Konfigurationen, z.B. 'acme' → 'acme-template-cx-24.2-website')"

Validierung:
- Nur Kleinbuchstaben, Ziffern und Bindestriche erlaubt (kein Leerzeichen, keine Umlaute)
- Mindestens 2 Zeichen
- Falls ungültig: erneut fragen

Merke den Namen als `$PROJEKTNAME`.

### 5.2 Verfügbare Build-Konfigurationen auslesen

Lese `webpack.config.js` und extrahiere alle `.withName('...')`-Werte. Liste sie dem Benutzer nummeriert auf:

Beispiel:
```
Verfügbare Build-Konfigurationen:
 1. master-template-cx-1.3-website
 2. master-template-cx-22.0-website
 3. master-template-cx-23.2-website
 4. master-template-cx-24.2-website
 5. master-template-cx-1.3-landingpage-de
 6. master-template-cx-22.0-landingpage-de
 7. master-template-cx-23.2-landingpage-de
 8. master-template-cx-24.2-landingpage-de
 9. master-template-cx-22.0-landingpage-en
```

Frage den Benutzer:
> "Welche Konfigurationen sollen aktiv bleiben? Nummern kommagetrennt eingeben (z.B. 4,7 für cx-24.2-website + cx-23.2-landingpage-de):"

### 5.3 webpack.config.js anpassen

Öffne `webpack.config.js` und führe beide Änderungen durch:

**Änderung A — Projektname einsetzen:**
Ersetze in allen `.withName('...')`-Aufrufen das Wort `master` durch `$PROJEKTNAME`:
```
.withName('master-template-cx-24.2-website')
→ .withName('[projektname]-template-cx-24.2-website')
```

**Änderung B — Nicht ausgewählte Konfigurationen auskommentieren:**
Jede nicht ausgewählte `BuildConfig.create()...build()`-Block wird mit `/* ... */` umschlossen. Die Blöcke werden **nicht gelöscht** — nur deaktiviert, damit sie später wieder aktiviert werden können.

Beispiel für einen auskommentierten Block:
```javascript
/*
BuildConfig.create()
  .withRootPath('./templates/website')
  .withName('[projektname]-template-cx-1.3-website')
  // ...
  .build(),
*/
```

**Wichtig bei Kommas:** JavaScript-Arrays erlauben kein trailing comma vor `]`. Stelle sicher dass das letzte **aktive** `build()` kein abschließendes Komma hat (oder dass auskommentierte Blöcke das Komma innerhalb des `/* */`-Blocks behalten).

Bestätige dem Benutzer:
> "webpack.config.js angepasst: [N] Konfigurationen aktiv, [M] auskommentiert."

---

## SCHRITT 6 — Kunden-URL ermitteln

Frage den Benutzer:
> "An welcher Kundenwebsite soll das Template ausgerichtet werden? Bitte URL eingeben (z.B. https://www.kunde.de):"

Validierung:
- Muss mit `http://` oder `https://` beginnen
- Führe einen kurzen Erreichbarkeitstest durch (WebFetch oder curl HEAD-Request)
- Falls nicht erreichbar: frage ob trotzdem fortgefahren werden soll

Merke die URL als `$KUNDEN_URL`.

---

## SCHRITT 7 — cx-brand ausführen

Lade den Sub-Skill aus dem Projekt:
`.agents/skills/cx-design/skills/cx-brand.md`

Falls nicht verfügbar, Fallback:
`$env:USERPROFILE\.claude\commands\cx-styleguide-start.md`

**Wichtig:** Das Arbeitsverzeichnis muss `$ZIELORDNER` sein. Die Kunden-URL aus Schritt 6 als Ausgangspunkt für die Website-Analyse verwenden.

---

## SCHRITT 8 — Element-Anpassung: Modus wählen

Nach Abschluss von cx-brand frage den Benutzer:

> "Wie sollen die Content-Elemente angepasst werden?"
> 1. **Alle Elemente** — alle Elemente automatisch analysieren und anpassen
> 2. **Einzeln** — du gibst an, welche Elemente angepasst werden sollen

**Bei Option 1:**
Lade den Sub-Skill aus dem Projekt:
`.agents/skills/cx-design/skills/cx-elements-customize.md`

Falls nicht verfügbar, Fallback:
`$env:USERPROFILE\.claude\commands\cx-element-adapt.md`

**Bei Option 2:**
Teile dem Benutzer mit:
> "Setup abgeschlossen. Mit `/cx-elements-customize` kannst du jederzeit einzelne Elemente anpassen."

---

## FEHLERBEHANDLUNG

| Situation | Verhalten |
|---|---|
| GitHub API nicht erreichbar | Manuell nach ZIP-URL oder lokalem Pfad fragen |
| Ungültige Versionsnummer eingegeben | Verfügbare Versionen erneut anzeigen |
| Download schlägt fehl | Fehlermeldung + erneut versuchen oder lokale ZIP nutzen |
| Zielordner-Pfad ungültig | Erneut fragen |
| ZIP enthält kein `package.json` | Warnen, Schritt 3 wiederholen lassen |
| Node.js nicht installiert | Abbrechen, Installationslink zeigen |
| Node.js Major > 22 | Abbrechen, v22 empfehlen |
| `npm install` schlägt fehl | Fehlermeldung zeigen, Benutzer entscheidet ob weiter |
| Kunden-URL nicht erreichbar | Benutzer entscheidet ob weiter |
| cx-brand Skill nicht ladbar | Skill-Datei direkt lesen und Anweisungen befolgen |
