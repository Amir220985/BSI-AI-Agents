# Sub-Skill: cx-styleguide-fonts
## Schriften, Logo, Favicon (Schritte 1 + 1.5)

> Dieser Sub-Skill wird von `cx-styleguide-start` aufgerufen. Führe Schritte 1 und 1.5 vollständig durch.

## Verwandte Skills

> **Wenn ein neues Content Element erstellt werden soll:**
> Lade `cx-extend` aus dem Projekt:
> `.agents/skills/cx-styleguide-expert/skills/cx-extend.md`

---

## UNVERÄNDERLICHE DATEIEN — NIEMALS ANFASSEN

| Datei | Grund |
|-------|-------|
| `webpack.config.js` | Build-Konfiguration abgeschlossen. Neue Assets/Fonts über `static/`-Ordner lösen. |
| `.github/workflows/build-template.yml` | CI/CD — nur auf explizite Anfrage |

---

## PFLICHT-VORBEREITUNG

**Lies vor jeder Änderung diese Kerndateien:**
- `properties.js`
- `templates/website/design.js` + `templates/landingpage/design.js`
- `templates/website/styles/styles.scss` + `templates/landingpage/styles/styles.scss`
- `templates/website/_layout.twig` + `templates/landingpage/_layout.twig`
- `templates/website/includes/footer/` + `templates/landingpage/content-elements/footer/`
- `CLAUDE.md`

---

## SCHRITT 1 — Schriften (Fonts)

### 1.1 Schriften auf der Kundenwebsite ermitteln

Analysiere die Seite auf Schriftdateien:

```bash
# Preload-Links aus HTML extrahieren
curl -s "https://www.kunde.de/" | grep -oE 'href="[^"]*\.(woff2|woff|ttf)[^"]*"'

# CSS-Datei auf @font-face prüfen
curl -s "https://www.kunde.de/assets/styles.css" | grep -oE "url\(['\"]?[^)'\"]+\.(woff2|woff)[^)'\"]*['\"]?\)"
```

Identifiziere:
- **Schriftfamilien**: primäre Schrift (Headings), sekundäre Schrift (Body), Fallbacks
- **Schriftschnitte**: nur tatsächlich genutzte (regular, medium, light, bold, italic)
- **Herkunft**: Eigene Dateien auf dem Server, Google Fonts URL, oder System-Font

| Herkunft | Vorgehen |
|----------|---------|
| Eigene Dateien auf dem Server | Herunterladen → `templates/shared/static/fonts/` |
| Google Fonts | `<link rel="preconnect">` + `<link href="...fonts.googleapis.com...">` in `html-header.twig`, KEINE lokalen Dateien |
| System-Font | Nur als Fallback in `font-family` — keine Dateien nötig |

### 1.2 Schriftdateien herunterladen (nur bei eigenen Dateien)

```bash
mkdir -p "templates/shared/static/fonts"

curl -L -o "templates/shared/static/fonts/fontname-regular.woff2" \
  "https://www.kunde.de/pfad/zu/fontname-regular.woff2"

# Dateigröße prüfen: < 1KB = Fehler (404), > 5KB = OK
ls -lh templates/shared/static/fonts/
```

**Regeln:**
- Nur Dateien ablegen die wirklich heruntergeladen wurden (Größe > 5 KB)
- Dateinamen ohne Umlaute und Sonderzeichen (z.B. `fontname-regular.woff2`)
- Nicht verfügbare Schnitte → nicht anlegen

Zielstruktur:
```
templates/shared/static/fonts/
  ├── fontname-regular.woff2
  ├── fontname-medium.woff2
  └── fontname-light.woff2
```

### 1.3 variables.scss erstellen

Erstelle `templates/shared/styles/variables.scss`. Farb- und Nav-Abschnitte werden hier als Platzhalter angelegt — die Werte befüllen `cx-styleguide-colors` (Farben) und `cx-styleguide-layout` (Navigation):

```scss
// --- SCHRIFTEN ---
$font-primary:   'KundenFont-medium',  Helvetica, Arial, sans-serif;  // Headings
$font-secondary: 'KundenFont-regular', Helvetica, Arial, sans-serif;  // Body/Text
$font-light:     'KundenFont-light',   Helvetica, Arial, sans-serif;  // optional

// Heading-Größen Desktop (>= 940px) — aus Kundensite: CSS laden, h1-h6 prüfen
$font-size-h1: ???rem;   $font-size-h2: ???rem;   $font-size-h3: ???rem;
$font-size-h4: ???rem;   $font-size-h5: ???rem;   $font-size-h6: ???rem;

// Heading-Größen Mobile (< 940px)
$font-size-h1-mobile: ???rem;   $font-size-h2-mobile: ???rem;   $font-size-h3-mobile: ???rem;
$font-size-h4-mobile: ???rem;   $font-size-h5-mobile: ???rem;   $font-size-h6-mobile: ???rem;

// Line-Heights (aus Kundensite: DevTools oder CSS-Datei)
$line-height-h1: ???;   $line-height-h2: ???;   $line-height-h3: ???;
$line-height-h4: ???;   $line-height-h5: ???;   $line-height-h6: ???;

// Body
$font-size-base:   1rem;       // 16px
$font-size-small:  0.875rem;   // 14px
$line-height-base: 1.5;

// Schriftgewichte
$font-weight-light:    300;
$font-weight-regular:  400;
$font-weight-medium:   500;
$font-weight-semibold: 600;
$font-weight-bold:     700;

// --- FARBEN (→ Werte in cx-styleguide-colors setzen) ---
$color-primary:     #XXXXXX;
$color-secondary:   #XXXXXX;
$color-dark:        #XXXXXX;
$color-light:       #ffffff;
$color-text:        #XXXXXX;
$color-text-muted:  #XXXXXX;
$color-bg-body:     #ffffff;
$color-footer-bg:   #XXXXXX;
$color-footer-text: #ffffff;

// --- NAVIGATION (→ Werte in cx-styleguide-layout präzisieren) ---
$color-nav-bg:         #ffffff;
$color-nav-link:       $color-text;
$color-nav-link-hover: $color-primary;
$color-grey-light:     #e0e0e0;

// --- ABSTÄNDE ---
$spacing-xs: 0.25rem;   $spacing-sm:  0.5rem;   $spacing-md: 1rem;
$spacing-lg: 1.5rem;    $spacing-xl:  2rem;     $spacing-xxl: 3rem;

// --- BREAKPOINTS (BSI CX spezifisch: LG = 940px, NICHT 992px!) ---
$breakpoint-sm:  576px;   $breakpoint-md: 768px;   $breakpoint-lg: 940px;
$breakpoint-xl: 1200px;   $breakpoint-xxl: 1400px;

// --- BORDER RADIUS ---
$border-radius-sm:   0.25rem;   $border-radius-md:   0.5rem;
$border-radius-lg:   1rem;      $border-radius-pill: 50rem;

// --- LOGO (Werte in Schritt 1.5.6 aus DevTools messen) ---
$logo-width:  ???px;
$logo-height: ???px;
```

**Regel:** Kein `:root {}` in dieser Datei — das gehört in `bootstrap-overrides.scss` (siehe 1.7).

### 1.4 fonts.scss erstellen

Erstelle `templates/shared/styles/fonts.scss`.

**Syntaxregel 1 — Komma statt Semikolon**: `local()` und `url()` mit **Komma** trennen. Semikolon steht nur am Ende der gesamten `src:`-Deklaration. (Häufiger Fehler: Semikolon nach `local()` → `url()` wird nie geladen.)

**Syntaxregel 2 — Webpack-Pfad**: Webpack löst `url()` relativ zur **Entry-Datei** auf (`templates/website/styles/styles.scss`), nicht relativ zur `fonts.scss`. Korrekter Pfad:
```
../../shared/static/fonts/fontname.woff2
```
(Nicht `../static/fonts/` — das würde zu `templates/website/static/fonts/` führen.)

```scss
// Nur vorhandene Schnitte deklarieren.
// Falls Dateien noch nicht vorliegen: url()-Zeilen auskommentieren (sonst Build-Fehler).

@font-face {
  font-display: swap;
  font-family: 'KundenFont-regular';
  font-style: normal;
  font-weight: 400;
  src:
    local('KundenFont-regular'),
    url('../../shared/static/fonts/fontname-regular.woff2') format('woff2');
}

// Für jeden weiteren heruntergeladenen Schnitt wiederholen:
// @font-face { font-family: 'KundenFont-medium'; ... url('...fontname-medium.woff2') ... }
// @font-face { font-family: 'KundenFont-light';  ... url('...fontname-light.woff2')  ... }
```

**Hinweis Google Fonts**: Falls die Schrift über Google Fonts eingebunden wird, entfällt diese Datei. Stattdessen `<link>` in `templates/shared/html-header.twig`.

### 1.4b Konsistenz sicherstellen und properties.js aktualisieren

Der String in `$font-primary` muss **exakt** dem `font-family`-Wert im `@font-face`-Block entsprechen — Groß-/Kleinschreibung und Bindestriche identisch.

Passe in **`properties.js`** die Schrift-Tokens an — Werte müssen identisch mit `variables.scss` sein:

```javascript
primaryFontFamily: 'KundenFont-regular, Helvetica Neue, Helvetica, Arial, sans-serif',
// Falls Headings andere Schrift nutzen:
// titleFontFamily: 'KundenFont-medium, Helvetica, Arial, sans-serif',

// Heading-Größen Desktop (identisch mit $font-size-hX in variables.scss)
titleStyle1Size: '???rem',   titleStyle1SizeMobile: '???rem',  // H1
titleStyle2Size: '???rem',   titleStyle2SizeMobile: '???rem',  // H2
titleStyle3Size: '???rem',   titleStyle3SizeMobile: '???rem',  // H3
titleStyle4Size: '???rem',   titleStyle4SizeMobile: '???rem',  // H4
titleStyle5Size: '???rem',   titleStyle5SizeMobile: '???rem',  // H5
titleStyle6Size: '???rem',   titleStyle6SizeMobile: '???rem',  // H6
```

#### Checkliste nach Font-Integration

- [ ] Alle `@font-face`-Blöcke haben nur heruntergeladene Dateien in `url()`
- [ ] `$font-primary` / `$font-secondary` / `$font-light` in `variables.scss` stimmen mit `font-family` in `@font-face` überein
- [ ] `primaryFontFamily` und `titleStyle*Size`-Werte in `properties.js` identisch mit `variables.scss`
- [ ] `npm run build:dev` läuft ohne Fehler
- [ ] Schrift im Browser-Preview sichtbar (DevTools → Network → Fonts)

### 1.5 elements.scss erstellen

Erstelle `templates/shared/styles/elements.scss`:

```scss
@use 'variables' as *;

// --- HEADINGS (H1-H6) ---
// BSI-Klassen (.bsi-header-style-X) haben niedrigere Spezifität → font-family ohne !important.
// Größen + Line-Heights: !important nötig, da .bsi-header-style-X die Größe aus properties.js setzt.
// Mobile-first: Standard = mobile Größe, ab $breakpoint-lg = Desktop-Größe.

h1, .h1, h2, .h2, h3, .h3,
h4, .h4, h5, .h5, h6, .h6 { font-family: $font-primary; }

h1, .h1 { font-size: $font-size-h1-mobile !important; line-height: $line-height-h1; }
h2, .h2 { font-size: $font-size-h2-mobile !important; line-height: $line-height-h2; }
h3, .h3 { font-size: $font-size-h3-mobile !important; line-height: $line-height-h3; }
h4, .h4 { font-size: $font-size-h4-mobile !important; line-height: $line-height-h4; }
h5, .h5 { font-size: $font-size-h5-mobile !important; line-height: $line-height-h5; }
h6, .h6 { font-size: $font-size-h6-mobile !important; line-height: $line-height-h6; }

@media (min-width: $breakpoint-lg) {
  h1, .h1 { font-size: $font-size-h1 !important; }
  h2, .h2 { font-size: $font-size-h2 !important; }
  h3, .h3 { font-size: $font-size-h3 !important; }
  h4, .h4 { font-size: $font-size-h4 !important; }
  h5, .h5 { font-size: $font-size-h5 !important; }
  h6, .h6 { font-size: $font-size-h6 !important; }
}

// --- BODY ---
body {
  font-family: $font-secondary;
  font-size:   $font-size-base;
  line-height: $line-height-base;
}

// Weitere Overrides nach Analyse der Standard-Bibliothek ergänzen:
// .navbar, .bsi-btn, .bsi-card, .bsi-accordion, .bsi-form etc.
```

> **elements.scss überschreibt properties.js:** BSI `properties.js` unterstützt kein `clamp()` und kein responsives Sizing per Breakpoint. `elements.scss` gewinnt durch `!important` + Media Query. Line-Heights existieren ausschließlich in `elements.scss`.

### 1.6 navigation.scss Stub erstellen

Erstelle `templates/shared/styles/navigation.scss` als Stub — wird in `cx-styleguide-layout` vollständig implementiert:

```scss
@use 'variables' as *;

// Navigation Styles — vollständige Implementierung folgt in cx-styleguide-layout (Schritt 3.6)
.navbar {
  background-color: $color-nav-bg;
  font-family: $font-secondary;
}
```

### 1.7 bootstrap-overrides.scss und shared/styles/styles.scss erstellen

#### `templates/shared/styles/bootstrap-overrides.scss`

**WICHTIG**: `:root {}` NICHT in `variables.scss` — sonst wird der Block mehrfach ausgegeben (einmal pro `@use 'variables'`).

RGB-Werte sind Platzhalter — werden in `cx-styleguide-colors` durch echte Hex-zu-RGB-Werte ersetzt:

```scss
@use 'variables' as *;

:root {
  --bs-primary:         #{$color-primary};
  --bs-secondary:       #{$color-secondary};
  --bs-dark:            #{$color-dark};
  --bs-light:           #{$color-light};

  --bs-primary-rgb:     R, G, B;      // → cx-styleguide-colors befüllt diese Werte
  --bs-secondary-rgb:   R, G, B;
  --bs-dark-rgb:        R, G, B;
}
```

#### `templates/shared/styles/styles.scss`

Diese Datei wird von den Entry-Files per `@import` geladen. Reihenfolge ist wichtig:

```scss
// Reihenfolge: Bootstrap-Overrides → Fonts → Navigation → Elemente → Footer
@use 'bootstrap-overrides';
@use 'fonts';
@use 'navigation';
@use 'elements';
@use 'footer';
```

> `footer.scss` wird in `cx-styleguide-layout` erstellt. Bis dahin Zeile auskommentieren oder leere `footer.scss` anlegen.

### 1.8 Website und Landingpage styles.scss aktualisieren

In **`templates/website/styles/styles.scss`** UND **`templates/landingpage/styles/styles.scss`** nach dem BSI-`@import` ergänzen:

```scss
@import '~@bsi-cx/design-standard-library-web/styles/styles.scss';

// Shared Customer Styles — @import verwenden, KEIN @use!
// (In SASS Dart ist @use nach @import verboten)
@import '../../shared/styles/styles';

$logoWidth: bsiProperty('logoWidth', 60px);
$lg: bsiProperty('gridBreakpointLG', 940px);
```

**Kritische Regel**: In den Entry-Files **immer** `@import` für die shared styles. `@use` nach `@import` bricht den Build:
```
Error: @use rules must be written before any other rules.
```

---

## SCHRITT 1.5 — Logo und Favicon

### 1.5.1 Logo auf der Kundenwebsite finden

**Methode 1 — `<img>` Tag im Header/Navbar**

Browser DevTools → Navbar inspizieren → Logo-`<img>` → `src`-URL notieren → herunterladen (SVG bevorzugt).

**Methode 2 — Inline SVG Sprite** (häufig bei modernen Sites):

```html
<svg><use href="/assets/sprites/icons.svg#logo-id"></use></svg>
```

1. Sprite-URL aus `href` lesen → Sprite herunterladen
2. Symbol-IDs auflisten: `grep -o 'id="[^"]*"' sprite.svg`
3. Passendes `<symbol id="logo-id" viewBox="x y w h">` extrahieren und umwandeln:
   - `<symbol id="logo-id" viewBox="x y w h">` → `<svg xmlns="http://www.w3.org/2000/svg" viewBox="x y w h">`
   - `</symbol>` → `</svg>`
   - Speichern als `logo.svg`

**Methode 3 — CSS background-image:**

URL aus DevTools → Computed Styles → `background-image` → herunterladen.

Dateigröße prüfen: SVG > 1 KB erwartet; < 500 Byte = Fehler-Response (404/Redirect).

### 1.5.2 Dark-Mode-Logo erstellen

BSI Logo-Element erwartet genau diese Dateinamen — hardcodiert, nicht konfigurierbar:
- `logo.svg` — Light Mode (farbiges/dunkles Logo auf hellem Hintergrund)
- `logo-dm.svg` — Dark Mode (helles/weißes Logo auf dunklem Hintergrund)

**Fall A**: Kundenwebsite hat helle Logo-Variante (z.B. im Footer) → als `logo-dm.svg` ablegen.

**Fall B**: Nur eine Logo-Variante vorhanden → für beide Modes verwenden. Keine eigenen Farb-Änderungen am Kundenlogo.

### 1.5.3 Favicon herunterladen

Favicon-Referenz im `<head>` der Kundenwebsite suchen:
```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico">
```

SVG bevorzugen. Falls kein eigenes Favicon → `logo.svg` als Fallback (Standard-Verhalten in `html-header.twig`).

### 1.5.4 Dateien ablegen

| Datei | Pfad | Pflicht |
|-------|------|---------|
| Kunden-Logo light | `templates/shared/static/logo.svg` | Ja |
| Kunden-Logo dark | `templates/shared/static/logo-dm.svg` | Ja |
| Favicon | `templates/shared/static/favicon.svg` (oder `.ico`) | Empfohlen |

### 1.5.5 html-header.twig: Favicon anpassen

Datei: `templates/shared/html-header.twig`

```twig
{# Mit eigenem Favicon (SVG bevorzugt): #}
<link rel="icon" type="image/svg+xml" href="{{ bsi_cx_asset('./static/favicon.svg') }}" sizes="any">

{# Optional: ICO-Fallback für ältere Browser #}
<link rel="icon" href="{{ bsi_cx_asset('./static/favicon.ico') }}" sizes="32x32">
```

Standard (kein eigenes Favicon): Bestehende Logo-Referenz beibehalten.

### 1.5.6 Logo-Größen konfigurieren

**Kundenwerte messen:** Logo-Container auf der Kundensite in DevTools inspizieren (`.navbar-brand` → Computed → `width`, `max-width`, `height`).

Orientierungswerte:
| Kontext | Breite | Höhe |
|---------|--------|------|
| Desktop | 120–200 px | 40–56 px |
| Mobile  | 90–140 px  | 32–44 px |

**`templates/shared/styles/variables.scss`:**
```scss
$logo-width:  ???px;   // Desktop: aus DevTools messen
$logo-height: ???px;
```

**`properties.js`:**
```javascript
logoWidth:     '???px',   // identisch mit $logo-width
logoAlignment: 'left',    // 'left' oder 'right' — aus Kundensite
```

> **Footer-Logo — KRITISCH:** Das BSI `logo-with-darkmode` Prototype rendert `<figure>`, **nicht** `.footer-logo`. Die Klasse `.footer-logo` existiert nicht im Output. `img-fluid` macht Bilder 100 % der Containerbreite — ohne `figure`-Begrenzung wird das Logo auf die volle Spaltenbreite aufgezogen.
>
> → **Immer `figure` direkt targetieren** in `footer/styles.scss`:
> ```scss
> .footer-brand figure {
>   max-width: $logo-width;   // oft 60–80 % der Navbar-Logo-Breite
>   img { max-width: 100%; height: auto; }
> }
> ```

### 1.5.7 Checkliste nach Logo-Integration

- [ ] `logo.svg` in `templates/shared/static/` abgelegt
- [ ] `logo-dm.svg` in `templates/shared/static/` abgelegt
- [ ] Favicon in `templates/shared/static/` abgelegt (falls vorhanden)
- [ ] `html-header.twig` Favicon-Referenz angepasst (oder Standard beibehalten)
- [ ] `variables.scss`: `$logo-width` und `$logo-height` gesetzt
- [ ] `properties.js`: `logoWidth` identisch mit `$logo-width`, `logoAlignment` korrekt
- [ ] `npm run build:dev` läuft ohne Fehler
- [ ] Preview: Logo korrekt in Navbar
- [ ] Dark Mode: Logo wechselt zu `logo-dm.svg`

---

## HÄUFIGE FEHLER

### Build-Fehler: @use nach @import
```
Error: @use rules must be written before any other rules.
```
→ In Entry-Files `@import` statt `@use` verwenden (siehe Schritt 1.8).

### Build-Fehler: Schriftdatei nicht gefunden
```
HookWebpackError: Cannot find module '../static/fonts/fontname.woff2'
```
→ `url()`-Zeilen auskommentieren bis Dateien in `templates/shared/static/fonts/` vorliegen (siehe Schritt 1.4, Syntaxregel 2 für korrekten Pfad).

---

## REFERENZEN

- BSI CX Docs: https://bsi-software.github.io/bsi-cx-docs/docs/26.1/design.html
- CLAUDE.md im Projektverzeichnis
- Standard-Library: `node_modules/@bsi-cx/design-standard-library-web/`
