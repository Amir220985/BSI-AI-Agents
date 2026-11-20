# Skill: BSI CX Design — Content Elements & Includes erstellen

## Wann diesen Skill nutzen
Wenn neue **Content Elements** oder **Includes** für das BSI CX Master Template erstellt, erweitert oder in `design.js` registriert werden sollen. Dieser Skill enthält alle nötigen Code-Templates, Builder-APIs und Regeln — kein erneutes Lesen der Doku nötig.

---

## PFLICHT-VORBEREITUNG

Lies diese Dateien IMMER zuerst, bevor etwas erstellt wird:
- `templates/website/design.js` — aktuelle Elementgruppen und Includes der Website
- `templates/landingpage/design.js` — aktuelle Elementgruppen der Landingpage
- Das relevante Element-Verzeichnis wenn etwas erweitert wird

---

## KERNKONZEPTE

### Content Element vs. Include vs. PageInclude

| Typ | Was ist es? | Wo registriert | Builder |
|-----|-------------|----------------|---------|
| **ContentElement** | Drag-&-drop Block im Editor. Redakteur platziert es in Dropzones. | `design.js` → `withContentElementGroups` | `cx.contentElement` |
| **Include** | Fester HTML-Bereich im Layout (z.B. Navigation, Logo-Bereich, Footer-Bereich). Nicht vom Redakteur verschiebbar. | `design.js` → `.withWebsite().withIncludes()` | `cx.include` |
| **PageInclude** | Wie Include, aber mit seitenspezifischen Dropzones (pro Seite verschiedener Inhalt). | `design.js` → `.withWebsite().withIncludes()` | `cx.pageInclude` |

### ID-Format
Alle IDs folgen dem Schema `name-XXXXXX` (6-stelliger alphanumerischer Hash, Groß+Kleinbuchstaben+Ziffern).

**IDs müssen eindeutig sein** im gesamten Projekt — inklusive der Standard Library.
Standard-Library-IDs prüfen: `grep -r "withElementId" node_modules/@bsi-cx/design-standard-library-web/ --include="*.js"`

### Bekannte Standard-Library-Element-IDs
```
col-one-l2ZclN       col-two-ILRIL0       col-three-MEOl1p     col-four-yFAGKM
spacer-jarY9b
```

---

## TEIL 1: CONTENT ELEMENT ERSTELLEN

### 1.1 Verzeichnisstruktur

```
templates/shared/content-elements/mein-element/
├── index.js          ← Pflicht: Registriert das Element beim Build-System
├── template.twig     ← Pflicht: HTML-Struktur des Elements
└── styles.scss       ← Optional: Eigene Styles
```

**Ablageort:**
- `templates/shared/content-elements/` — wenn das Element in Website UND Landingpage verwendet wird
- `templates/website/content-elements/` — wenn es nur für die Website ist
- `templates/landingpage/content-elements/` — wenn es nur für die Landingpage ist

### 1.2 index.js — Custom Element (von Null)

```javascript
const { cx, Icon } = require('@bsi-cx/design-build');
const { layoutElements } = require('@bsi-cx/design-standard-library-web/content-elements/layout/');

module.exports = cx.contentElement
  .withElementId('mein-element-XXXXXX')        // EINDEUTIGE ID generieren!
  .withLabel('Mein Element')
  .withFile(require('./template.twig'))
  .withIcon(Icon.ONE_COLUMN)
  .withStyleConfigs(
    require('../../configs/styles/footer-color'),
  )
  .withDropzones(
    cx.dropzone
      .withDropzone('mein-element-dropzone-YYYYYY')
      .withAllowedElements(...layoutElements)
  );
```

**Minimal-Beispiel ohne Dropzone und StyleConfig:**
```javascript
const { cx, Icon } = require('@bsi-cx/design-build');

module.exports = cx.contentElement
  .withElementId('teaser-card-A7bx3K')
  .withLabel('Teaser Card')
  .withFile(require('./template.twig'))
  .withIcon(Icon.BANNER);
```

### 1.3 index.js — Prototype Pattern (Standard Library erweitern)

```javascript
// Beispiel: Logo mit Dark Mode (aus Standard Library)
require('./styles.scss');

const contentElement = require('@bsi-cx/design-standard-library-web/content-elements/advanced/logo-with-darkmode/prototype');

module.exports = contentElement(
  require('./template.twig'),
  'logo-pm7eOT',
  'Logo',
).withStyleConfigs();
```

### 1.4 template.twig — Einfaches Element (ohne Dropzone)

```twig
{% apply spaceless %}
  <div data-bsi-element="mein-element-XXXXXX"
       class="element-mein-element-XXXXXX bsi-custom-element">
    <div class="container">
      <h2 class="element-title">{{ properties.someProperty }}</h2>
    </div>
  </div>
{% endapply %}
```

**Pflichtattribute:**
- `data-bsi-element="ELEMENT-ID"` — muss identisch zur `withElementId()` in `index.js` sein
- CSS-Klasse `element-ELEMENT-ID` — BSI-Konvention für spezifische SCSS-Selektoren

### 1.5 template.twig — Element mit Dropzone

```twig
{% apply spaceless %}
  {% set myColor = (myColor ?: properties.footerColor) ?: 'bg-dark' %}

  <div data-bsi-element="mein-element-XXXXXX"
       class="element-mein-element-XXXXXX {{ myColor }} py-5">
    <div class="container">
      <div data-bsi-dropzone="mein-element-dropzone-YYYYYY"
           data-bsi-dropzone-allowed-elements="col-one-l2ZclN col-two-ILRIL0"
           data-bsi-dropzone-max-number-of-elements="3">
        {% block mein_element_content %}
        {% endblock %}
      </div>
    </div>
  </div>
{% endapply %}
```

### 1.6 template.twig — Prototype-Template

```twig
{# Methode 1: include — wenn keine eigenen Blöcke überschrieben werden #}
{% apply spaceless %}
  {% include '@bsi-cx/design-standard-library-web/content-elements/advanced/logo-with-darkmode/prototype/template.twig' with {
    elementId: 'logo-pm7eOT',
    imageSrc: bsi_cx_asset('../../static/logo.svg'),
    imageDarkModeSrc: bsi_cx_asset('../../static/logo-dm.svg'),
  } %}
{% endapply %}
```

### 1.7 styles.scss — Element-Styles

```scss
// bsiProperty('tokenName', fallbackValue) — greift auf properties.js-Token zu
.element-mein-element-XXXXXX {
  padding: 2rem 0;

  .element-title {
    color: bsiProperty('primaryColor', #16616d);
  }

  // Responsive (LG = 940px, NICHT 992px!)
  @include media-breakpoint-down(lg) {
    padding: 1rem 0;
  }
}
```

**SCSS-Regeln:**
- `@use` (nicht `@import`) für Prototype-Styles
- LG-Breakpoint = 940px (nicht 992px!)

### 1.8 Content Element in design.js registrieren

```javascript
// In bestehende Gruppe einfügen:
cx.contentElementGroup
  .withGroupId('content-JFLFHv')
  .withLabel('Inhalt')
  .withContentElements(
    // ... bestehende Elemente ...
    require('./../shared/content-elements/mein-element'),  // ← NEU
  ),
```

---

## TEIL 2: INCLUDES ERSTELLEN

### 2.1 Include vs. PageInclude

| | `cx.include` | `cx.pageInclude` |
|--|------------|----------------|
| **Zweck** | Fester Bereich im Layout (gleich auf allen Seiten) | Seiten-spezifischer Bereich |
| **Identifier** | `withIdentifier('id-XXXXXX')` | Kein `withIdentifier` — nur `withName` |
| **Beispiel** | Logo-Bereich, Footer-Bereich, Header-Bild | Content-Bereich (Hauptinhalt) |

### 2.2 index.js — Include

```javascript
const { cx } = require('@bsi-cx/design-build');

module.exports = cx.include
  .withIdentifier('mein-include-XXXXXX')
  .withName('Mein Bereich')
  .withEditable(true)
  .withFile(require('./template.twig'))
  .withDropzones(
    cx.dropzone
      .withDropzone('mein-include-dropzone-YYYYYY')
      .withMaxAllowedElements(1)
      .withAllowedElements(
        require('./../../../shared/content-elements/mein-element')
      )
  );
```

### 2.3 index.js — PageInclude

```javascript
const { cx } = require('@bsi-cx/design-build');
const { layoutElements } = require('@bsi-cx/design-standard-library-web/content-elements/layout/');

module.exports = cx.pageInclude
  // KEIN .withIdentifier() — das ist der Unterschied zu cx.include!
  .withName('Seiteninhalt')
  .withEditable(true)
  .withFile(require('./template.twig'))
  .withDropzones(
    cx.dropzone
      .withDropzone('page-content-dropzone-YYYYYY')
      .withAllowedElements(...layoutElements)
  );
```

### 2.4 Include in design.js registrieren

```javascript
.withWebsite(
  cx.website
    .withMaxNavigationLevel(2)
    .withIncludes(
      require("./includes/navigation"),
      require("./includes/mein-include"),  // ← NEU
    )
);
```

**Wichtig:** Includes gibt es nur für den Website-Typ. Landingpages haben keine `withWebsite()` Konfiguration.

---

## TEIL 3: STYLE CONFIGURATIONS

```javascript
// templates/shared/configs/styles/meine-style-option.js
const { cx } = require('@bsi-cx/design-build');

module.exports = cx.style
  .withIdentifier('meine-style-option-XXXXXX')
  .withLabel('Farboption')
  .withCssClasses(
    cx.cssClass.withLabel('Primärfarbe').withCssClass('bg-primary'),
    cx.cssClass.withLabel('Sekundärfarbe').withCssClass('bg-secondary'),
  );
```

---

## TEIL 4: API-REFERENZ

### cx.contentElement — Builder-Methoden

```javascript
cx.contentElement
  .withElementId('name-XXXXXX')          // Pflicht
  .withLabel('Label im Editor')           // Pflicht
  .withFile(require('./template.twig'))   // Pflicht
  .withIcon(Icon.ONE_COLUMN)             // Optional
  .withStyleConfigs(/* StyleConfig */)   // Optional
  .withDropzones(/* cx.dropzone */)      // Optional
```

### cx.include — Builder-Methoden

```javascript
cx.include
  .withIdentifier('name-XXXXXX')         // Pflicht
  .withName('Interner Name')             // Pflicht
  .withEditable(true)                    // Pflicht
  .withFile(require('./template.twig'))  // Pflicht
  .withDropzones(/* cx.dropzone */)      // Optional
```

### cx.pageInclude — Builder-Methoden

```javascript
cx.pageInclude
  // KEIN .withIdentifier()!
  .withName('Interner Name')
  .withEditable(true)
  .withFile(require('./template.twig'))
  .withDropzones(/* cx.dropzone */)
```

### Icon-Konstanten

```javascript
const { Icon } = require('@bsi-cx/design-build');
Icon.ONE_COLUMN    // Footer, Column-Elemente
Icon.IMAGE         // Bild-Elemente
Icon.BANNER        // Banner/Header-Image
```

Weitere: `grep -r "Icon\." node_modules/@bsi-cx/design-standard-library-web/content-elements/ --include="index.js" -h | sort -u`

---

## TEIL 5: PITFALLS & CHECKLISTE

### Häufige Fehler

**1. IDs stimmen nicht überein**
- `withElementId()` in index.js ≠ `data-bsi-element` im Template
- `withDropzone()` in index.js ≠ `data-bsi-dropzone` im Template

**2. ID-Kollision mit Standard Library**
- Prüfen: `grep -r "withElementId('meine-neue-id'" node_modules/@bsi-cx/design-standard-library-web/`

**3. PageInclude mit withIdentifier()**
- `cx.pageInclude` hat KEIN `withIdentifier()` — nur `cx.include` hat es

**4. SCSS: @use nach @import**
- In den Entry-Files nach `@import '~@bsi-cx/...'` nur `@import` verwenden

**5. LG-Breakpoint ist 940px, nicht 992px**

**6. require('./styles.scss') nicht vergessen**
- Bei Prototype-Pattern: `require('./styles.scss')` am Anfang der index.js!

### Checkliste nach jedem neuen Element

- [ ] Element-ID eindeutig im Projekt
- [ ] Dropzone-IDs eindeutig und in JS + Twig identisch
- [ ] Bei Include: `withWebsite().withIncludes()` in design.js ergänzt
- [ ] Bei Content Element: in `withContentElementGroups()` ergänzt (website UND landingpage falls shared)
- [ ] `npm run build:dev` läuft ohne Fehler
- [ ] Element erscheint im CX-Editor in der richtigen Gruppe

---

## REFERENZEN

- **Standard Library Quellen:** `node_modules/@bsi-cx/design-standard-library-web/content-elements/`
- **Offizielle Doku:** https://bsi-software.github.io/bsi-cx-docs/docs/26.1/design.html
- **CLAUDE.md:** Vollständiges Projekt-Cheatsheet
