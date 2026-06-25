# Sub-Skill: cx-styleguide-colors
## Farben, Bootstrap-Overrides (Schritt 2)

> Dieser Sub-Skill wird von `cx-styleguide-start` aufgerufen — nach `cx-styleguide-fonts`.
> `variables.scss`, `bootstrap-overrides.scss` und `properties.js` müssen bereits existieren (aus Schritt 1).

---

## SCHRITT 2 — Farben (Color Scheme)

### 2.1 Kundenfarben analysieren

Analysiere die Kundenwebsite auf:
- **Primärfarbe**: Hauptaktionsfarbe (Buttons, Links, CTAs)
- **Sekundärfarbe**: Akzentfarbe
- **Hintergrundfarben**: Body, Sections, Cards
- **Textfarben**: primärer Text, sekundärer/Grau-Text
- **Statusfarben**: Fehler (Rot), Erfolg (Grün) — oft Bootstrap-Standard behalten
- **Footer-Farbe**: Hintergrund + Textfarbe
- **Navbar-Farbe**: Hintergrund + Link-Farbe

Werkzeuge:
- Browser DevTools → computed styles
- `getComputedStyle()` in der Konsole
- ColorZilla Browser-Extension
- Figma/Zeplin falls vorhanden

### 2.2 variables.scss — Farb-Abschnitt befüllen

Ersetze die Platzhalterfarben im Farb-Abschnitt von `templates/shared/styles/variables.scss`:

```scss
// --- FARBEN ---
$color-primary:     #XXXXXX;       // Kundenfarbe 1 — Buttons, Links, CTAs
$color-secondary:   #XXXXXX;       // Kundenfarbe 2 — Akzent
$color-dark:        #XXXXXX;       // Dunkelton — Footer, Dark-Mode-Bereiche
$color-light:       #ffffff;        // Hellton (fast immer weiß)
$color-text:        #XXXXXX;        // Fließtextfarbe
$color-text-muted:  #XXXXXX;       // Sekundärtext/Grau
$color-bg-body:     #ffffff;        // Seitenhintergrund (meist #fff)
$color-footer-bg:   #XXXXXX;       // Footer-Hintergrund
$color-footer-text: #ffffff;        // Footer-Textfarbe (bei dunklem Hintergrund)

// Navigation
$color-nav-bg:         #XXXXXX;    // Navbar-Hintergrund
$color-nav-link:       #XXXXXX;    // Nav-Link Farbe (default)
$color-nav-link-hover: #XXXXXX;    // Nav-Link Farbe (hover/aktiv)
```

### 2.3 properties.js — Farb-Tokens anpassen

Mappe Kundenfarben auf die BSI Design-Tokens:

```javascript
// Kernfarben — IMMER anpassen
primaryColor:   '#XXXXXX',    // Kundenfarbe primär
secondaryColor: '#XXXXXX',    // Kundenfarbe sekundär
darkColor:      '#XXXXXX',    // Dunkelton für Footer, Text
lightColor:     '#ffffff',     // i.d.R. immer weiß

// Sekundäre Farben — prüfen & ggf. anpassen
infoColor:    '#6c757d',       // Grau — oft Bootstrap-Standard ok
invalidColor: '#dc3545',       // Rot  — oft Bootstrap-Standard ok
validColor:   '#198754',       // Grün — oft Bootstrap-Standard ok

// Dark Mode Text (nur relevant wenn darkModeActiveProperty: true)
darkModeTextColor: '#ffffff',
```

### 2.4 Farb-gesteuerte Properties wählen

Für jede Komponente die Standardfarbe in `properties.js` festlegen:

```javascript
// Footer
footerColor:    'bg-dark',        // 'bg-primary' | 'bg-secondary' | 'bg-dark' | 'bg-light'
footerGradient: 'default',        // 'default' | 'bg-gradient'

// Buttons
buttonColor: 'primary',           // 'primary' | 'secondary' | 'dark' | 'light'

// Social Media
socialMediaIconColor:  'light',   // 'primary' | 'secondary' | 'dark' | 'light'
socialMediaHoverColor: 'secondary',

// Formulare
formColor: 'primary',             // 'primary' | 'secondary'
```

> Layout- und Form-Eigenschaften (`buttonLayout`, `buttonBorderRadius`, `formLayout`, `formButtonLayout`) werden in `cx-styleguide-layout` gesetzt.

### 2.5 bootstrap-overrides.scss — RGB-Werte eintragen

Die Datei existiert bereits aus `cx-styleguide-fonts` Schritt 1.7. Öffne `templates/shared/styles/bootstrap-overrides.scss` und ersetze die drei `R, G, B` Platzhalter durch die echten RGB-Tripel der Kundenfarben:

```scss
--bs-primary-rgb:     R, G, B;   // Hex-Wert von $color-primary als RGB, z.B. #1a2b3c → 26, 43, 60
--bs-secondary-rgb:   R, G, B;
--bs-dark-rgb:        R, G, B;
```

### 2.6 Farb-Variablen in alle Styles einbinden

Prüfe: Alle SCSS-Dateien in `shared/styles/` laden `@use 'variables' as *;` — keine hardcodierten Farbwerte in den SCSS-Dateien.

---

## HÄUFIGE FEHLER (Farben)

### Bootstrap-Klassen .bg-primary / .text-primary zeigen noch Bootstrap-Standard
→ `bootstrap-overrides.scss` prüfen: enthält die Datei `:root {}` mit `--bs-primary`?
→ Ist `bootstrap-overrides.scss` als erstes in `shared/styles/styles.scss` via `@use` eingebunden?
→ `npm run build:dev` ausführen und Cache im Browser leeren.

### bsiProperty() gibt falschen Wert
→ `properties.js` verwendet CommonJS (`module.exports = {}`), kein `export default`.
→ Wert muss String oder Zahl sein, kein `undefined`.

---

## REFERENZEN

- BSI CX Docs: https://bsi-software.github.io/bsi-cx-docs/docs/26.1/design.html
- CLAUDE.md im Projektverzeichnis
- Standard-Library: `node_modules/@bsi-cx/design-standard-library-web/`
