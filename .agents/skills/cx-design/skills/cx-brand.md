# Skill: BSI CX Master Template — Kundenprojekt Styleguide-Anpassung

## Wann diesen Skill nutzen
Wenn eine Kundenwebsite analysiert und das BSI CX Master Template mit den Kundenstyles (Schriften, Farben, Navigation, Footer) angepasst werden soll.

## Verwandte Skills

> **Nach Abschluss der globalen Brand-Anpassungen (Schriften, Farben, Nav, Footer):**
> Lade den Sub-Skill `cx-elements-customize` aus dem Projekt:
> `.agents/skills/cx-design/skills/cx-elements-customize.md`

> **Wenn im Rahmen dieser Anpassung ein neues Content Element oder Include erstellt werden soll:**
> Lade den Sub-Skill `cx-element-create` aus dem Projekt:
> `.agents/skills/cx-design/skills/cx-element-create.md`

---

## ORCHESTRATOR — Ablauf

Dieser Skill orchestriert drei Sub-Skills, die **nacheinander** ausgeführt werden müssen:

```
Schritt 1 + 1.5  →  Schritt 2  →  Schritt 3
cx-fonts          cx-colors         cx-layout
```

### Ausführungsreihenfolge

**1. Schriften, Logo, Favicon** → Lade Sub-Skill:
`.agents/skills/cx-design/skills/cx-fonts.md`

Enthält:
- Schriften auf der Kundenwebsite ermitteln und herunterladen
- `variables.scss`, `fonts.scss`, `elements.scss`, `navigation.scss` (Stub) erstellen
- `bootstrap-overrides.scss` (mit Platzhalter-RGB) und `shared/styles/styles.scss` erstellen
- Entry-SCSS-Dateien (`website/` + `landingpage/`) aktualisieren
- `properties.js` Schrift-Tokens setzen
- Logo, Dark-Mode-Logo und Favicon herunterladen
- `html-header.twig` Favicon anpassen
- Logo-Größen konfigurieren

**→ Erst nach vollständigem Abschluss von cx-fonts weitermachen.**

---

**2. Farben, Bootstrap-Overrides** → Lade Sub-Skill:
`.agents/skills/cx-design/skills/cx-colors.md`

Enthält:
- Kundenfarben analysieren
- `variables.scss` Farb-Abschnitt befüllen
- `properties.js` Farb-Tokens anpassen
- Farb-gesteuerte Properties wählen (Footer, Buttons, Social Media, Forms)
- `bootstrap-overrides.scss` RGB-Werte eintragen

**→ Erst nach vollständigem Abschluss von cx-colors weitermachen.**

---

**3. Navigation & Footer ContentElement** → Lade Sub-Skill:
`.agents/skills/cx-design/skills/cx-layout.md`

Enthält:
- Kundenwebsite Struktur analysieren
- Shared Footer ContentElement erstellen (`index.js`, `template.twig`, `styles.scss`)
- `footer.scss` in `shared/styles/` anlegen + in `styles.scss` einkommentieren
- Footer in `website/design.js` und `landingpage/design.js` registrieren
- Social Media im Footer konfigurieren
- `navigation.scss` vollständig implementieren (Stub aus Schritt 1 ersetzen)
- PFLICHT-BUILD: `npm run build:dev` + Preview-Prüfung

---

## ABSCHLUSS-CHECKLISTE

Nach allen drei Sub-Skills:

- [ ] `npm run build:dev` läuft ohne Fehler
- [ ] Preview im Browser: alle Elemente rendern mit Kundenschrift
- [ ] Heading-Größen auf Desktop und Mobile korrekt
- [ ] Farben stimmen mit Kundenwebsite überein
- [ ] Logo korrekt in Navbar (Desktop und Mobile)
- [ ] Logo Dark Mode wechselt zu `logo-dm.svg`
- [ ] Footer erscheint in Website-Preview
- [ ] Footer erscheint in Landingpage-Preview
- [ ] Footer-Text lesbar (bei dunklem Hintergrund: weiß)
- [ ] Navigation: Hover-Effekte und Aktiv-Indikator funktionieren
- [ ] `variables.scss` enthält KEINE hardcodierten Werte außer Definitionen
- [ ] Alle SCSS-Dateien nutzen `@use 'variables' as *` (kein direktes Hardcoden)
- [ ] `properties.js` ist konsistent mit `variables.scss` (Farben, Schriften, Größen)
- [ ] Keine Umlaute in neuen Dateinamen
- [ ] Neue Element-IDs sind eindeutig (kein Duplikat mit Standard-Library IDs)
- [ ] `webpack.config.js` wurde nicht verändert

---

## HÄUFIGE FEHLER UND LÖSUNGEN

### Build-Fehler: @use nach @import
```
Error: @use rules must be written before any other rules.
  8 │ @use '../../shared/styles/styles' as shared;
```
→ In den Entry-Files (`website/styles/styles.scss`, `landingpage/styles/styles.scss`) `@import` statt `@use` verwenden:
```scss
@import '~@bsi-cx/design-standard-library-web/styles/styles.scss';
@import '../../shared/styles/styles';   // @import, NICHT @use!
```

### Build-Fehler: Schriftdatei nicht gefunden
```
HookWebpackError: Cannot find module '../static/fonts/fontname.woff2'
```
→ `url()`-Zeilen in `fonts.scss` auskommentieren bis Dateien vorliegen:
```scss
src:
  local('KundenFont');
  // url('../../shared/static/fonts/fontname.woff2') format('woff2');
```

### Footer-Text bleibt dunkel auf dunklem Hintergrund (Spezifitätsproblem)

BSI Standard-Bibliothek setzt:
```css
.bsi-element-text-kkq2fq.bsi-text-dark p { color: #darkColor; }  /* Spezifität: (0,2,1) */
```
Override ohne `p`-Selektor hat Spezifität (0,2,0) und verliert.

→ Immer `p` explizit mitangeben:
```scss
.footer-wrapper.bg-dark {
  .bsi-text-dark p,
  .text-content p { color: $color-footer-text; }
}
```

### BSI Validierungsfehler: "Dropzone enthält Beispiel-Content-Element..."
```
Die Dropzone enthält ein Beispiel-Content-Element, das nicht der Struktur
des definierten Content-Elements entspricht.
```
→ `textPartId` in `{% include '.../text/prototype/template.twig' %}` hat falschen Wert.
→ **Alle** `textPartId`-Werte auf `'text-part-Fjse59'` setzen. Jede Dropzone wirft einen eigenen Fehler.

### Unbekannte Element-ID im Dropzone
→ Element-ID in `design.js` und Template müssen identisch sein.
→ Prüfen: `grep -r "withElementId" templates/`

### bsiProperty() gibt falschen Wert
→ `properties.js` verwendet CommonJS (`module.exports = {}`), kein `export default`.
→ Wert muss String oder Zahl sein, kein `undefined`.

### Footer-Dropzone leer nach Rebuild
→ `data-bsi-dropzone-allowed-elements` prüfen — Element-ID muss exakt dem `withElementId()` entsprechen.

---

## REFERENZEN

- BSI CX Design-Dokumentation: https://bsi-software.github.io/bsi-cx-docs/docs/26.1/design.html
- CLAUDE.md im Projektverzeichnis: vollständiges Projekt-Cheatsheet
- Standard-Library Quellen: `node_modules/@bsi-cx/design-standard-library-web/`
- Design-Build API: `node_modules/@bsi-cx/design-build/`
