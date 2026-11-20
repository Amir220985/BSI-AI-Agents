# Sub-Skill: cx-styleguide-layout
## Navigation & Footer ContentElement (Schritt 3)

> Dieser Sub-Skill wird von `cx-styleguide-start` aufgerufen — nach `cx-styleguide-colors`.
> `variables.scss` mit echten Farb- und Schriftwerten muss vorliegen (aus Schritten 1 + 2).

## Verwandte Skills

> **Bevor du das Footer ContentElement erstellst:**
> Lade `cx-extend` aus dem Projekt:
> `.agents/skills/cx-styleguide-expert/skills/cx-extend.md`

---

## SCHRITT 3 — Seitenaufbau (Navigation & Footer)

### 3.1 Kundenwebsite Struktur analysieren

Analysiere:
- **Navigation**: Logo-Position (links/rechts), Hamburger-Breakpoint, Hintergrundfarbe, Hover-Effekte, Aktiv-Indikator (border-bottom, background oder keiner)
- **Footer**: Spaltenlayout (1–4 Spalten?), Inhalte (Logo, Links, Social Media, Text, Copyright), Hintergrundfarbe
- **Buttons**: Stil (filled/outline), Form (rounded/sharp)
- **Formulare**: Layout (card/plain), Button-Stil (filled/outline)

### 3.1b Komponenten-Defaults in properties.js setzen

Basierend auf der Analyse den Stil von Buttons und Formularen festlegen:

```javascript
// Buttons — Form und Layout
buttonLayout:       'filled',    // 'filled' | 'outline'
buttonBorderRadius: 'rounded',   // 'sharp' | 'rounded'

// Formulare — Layout
formLayout:       'card',        // 'card' | 'plain'
formButtonLayout: 'outline',     // 'filled' | 'outline'
```

---

### 3.2 Footer ContentElement: Analyse und Aufbau

Der Footer wird als **ContentElement** sowohl für Website als auch für Landingpage erstellt. Layout, Anzahl der Dropzones und erlaubte Elemente werden aus der Analyse der Kundensite abgeleitet — es gibt kein vorgegebenes Layout.

#### 3.2.1 Kundenfooter vollständig analysieren

Lade den Footer-Bereich der Kundensite und kartiere jeden sichtbaren Inhalt:

```bash
curl -s "https://www.kunde.de/" | grep -i -A 200 '<footer\|id="footer\|class="footer'
```

Erstelle eine strukturierte Übersicht — Zeile für Zeile, Spalte für Spalte:

```
Beispiel-Mapping (immer an Kundensite anpassen!):
Zeile 1: [ Spalte A: Logo ]  [ Spalte B: Adresse + Telefon ]  [ Spalte C: 8 Links ]  [ Spalte D: 3 Bilder ]
Zeile 2: [ Social Media Icons (volle Breite) ]
Zeile 3: [ Formular "Newsletter" (volle Breite) ]
Zeile 4: [ Copyright-Text | Impressum | Datenschutz (volle Breite) ]
```

Notiere für jede Zelle:
- Welches Element (Logo, Text, Bild, Links, Icon, Formular, …)
- Wie viele Instanzen (z.B. „8 Links" = ein Text-Block mit Liste, nicht 8 Button-Elemente)
- Ob der Redakteur das im CX Editor ändern soll (→ Dropzone) oder ob es fix ist (→ hardcoded im Template)

#### 3.2.2 BSI-Element-Mapping

Ordne jeden identifizierten Kundeninhalt einem BSI-Element zu:

| Kundeninhalt | BSI-Element | Import-Pfad | Hinweis |
|---|---|---|---|
| Firmenlogo | shared `logo` | `../logo` | Light + Dark Mode automatisch |
| Bild / Grafik | `figure` | `base/figure` | Alt-Text Pflicht |
| Fließtext, Adresse | `text` | `base/text` | HTML-Formatierung möglich |
| Links-Liste | `text` | `base/text` | Als `<ul><li><a>` im Text-Block |
| CTA-Button | `button` | `base/button` | Farbe + Layout via StyleConfig |
| Social Media Icons | `social-media-follow` | `base/social-media-follow` | Plattformen via properties.js |
| Newsletter-Formular | `form-container` | `base/form-container` | Komplexe Logik → cx-extend laden |
| Accordion / FAQ | `accordion` | `base/accordion` | |
| Video | `video` | `base/video` | |
| Abstand | `spacer` | `layout/spacer` | |
| Spalten-Layout | `col-two` / `col-three` / `col-four` | `layout/col-*` | Innerhalb einer Dropzone platzierbar |

Element-IDs für `data-bsi-dropzone-allowed-elements` ermitteln:
```bash
grep -r "withElementId" node_modules/@bsi-cx/design-standard-library-web/
```

Bekannte IDs:
- `logo-pm7eOT` — Shared Logo
- `text-kkq2fq` — Text
- `button-v3cFFn` — Button
- `social-media-follow-2MlXWB` — Social Media Follow

#### 3.2.3 Technische Grenzen in BSI CX

| Nicht möglich | Workaround |
|---|---|
| Interaktive Karte (Google Maps etc.) | `html`-Element mit Embed-Code |
| Live-Daten / dynamische Inhalte | Nicht möglich — statischer Inhalt |
| Komplexe JS-Widgets (Slider, Carousel) | Nur mit `html`-Element + externem Script |
| Footer in mehreren Sprachen mit Umschaltung | Separate Landingpage-Varianten |

#### 3.2.4 Dropzone-Struktur planen

- **Eine Dropzone pro Spalte oder Inhaltsbereich** — nicht pro Element
- `max-number-of-elements="1"` nur setzen wenn wirklich nur ein Element erlaubt sein soll (z.B. Logo)

Benennung nach Position und Funktion:
```
footer-col-a-dropzone-XXXXXX   (Spalte A)
footer-social-dropzone-XXXXXX  (Social Media, volle Breite)
footer-legal-dropzone-XXXXXX   (Copyright/Links, volle Breite)
```

#### 3.2.5 index.js erstellen

```
templates/shared/content-elements/footer/
├── index.js
├── template.twig
└── styles.scss
```

```javascript
const {cx, Icon} = require('@bsi-cx/design-build');

module.exports = cx.contentElement
  .withElementId('footer-content-XXXXXX')   // eindeutiger 6-stelliger Hash
  .withLabel('Footer')
  .withFile(require('./template.twig'))
  .withIcon(Icon.ONE_COLUMN)
  .withStyleConfigs(
    require('../../configs/styles/footer-color'),
    require('../../configs/styles/footer-gradient'))
  .withDropzones(
    cx.dropzone
      .withDropzone('footer-[bereich]-dropzone-XXXXXX')
      .withAllowedElements(
        require('../logo'),
        require('@bsi-cx/design-standard-library-web/content-elements/base/text'),
        // … weitere nach Mapping aus 3.2.2
      ),
    // … weitere Dropzones
  );
```

#### 3.2.6 template.twig erstellen

> **PFLICHT:** Das HTML-Gerüst muss exakt die Zeilen- und Spaltenstruktur widerspiegeln, die in der Kundensite-Analyse (3.2.1) kartiert wurde.

```twig
{% apply spaceless %}
  {% set footerColor    = (footerColor    ?: properties.footerColor)    ?: 'bg-dark' %}
  {% set footerGradient = (footerGradient ?: properties.footerGradient) ?: 'default' %}

  <div data-bsi-element="footer-content-XXXXXX"
       class="element-footer-content-XXXXXX footer-wrapper {{ footerColor }} {{ footerGradient }}">
    <div class="container">
      {# Struktur aus Kundensite-Analyse — Zeilen und Spalten nach Bedarf #}
      <div class="footer-row footer-main">
        <div class="footer-col-a">
          <div data-bsi-dropzone="footer-col-a-dropzone-XXXXXX"
               data-bsi-dropzone-allowed-elements="logo-pm7eOT text-kkq2fq">
            {% block footer_col_a %}
              {# Default-Inhalt mit textPartId: 'text-part-Fjse59' #}
            {% endblock %}
          </div>
        </div>
      </div>
    </div>
  </div>
{% endapply %}
```

> **KRITISCH — textPartId:** Jedes `{% include '.../text/prototype/template.twig' %}` benötigt zwingend `textPartId: 'text-part-Fjse59'`. Jeder andere Wert → BSI CX Validierungsfehler pro betroffener Dropzone.

**Social Media Icons — iconColor nach Hintergrundfarbe:**

| Footer-Hintergrund | `iconColor` |
|---|---|
| Dunkel (bg-dark, bg-primary) | `bsi-icon-color-light` |
| Hell (bg-light, weiß) | `bsi-icon-color-primary` oder `bsi-icon-color-dark` |

#### 3.2.7 styles.scss erstellen

> **KEINE erfundenen Dekorationen:** Kein `border-top`, `border-bottom`, `box-shadow` einfügen, die auf der Kundensite NICHT sichtbar sind.

> **FLEX-LAYOUT REGEL — PFLICHT bei allen Flex-Containern im Footer:**
> BSI CX Content Elements setzen intern eigene `width`/`min-width`-Werte. Ohne `min-width: 0` können Flex-Kinder überlaufen.
>
> ```scss
> .footer-left  { flex: 1 1 0;    min-width: 0; }
> .footer-right { flex: 0 1 auto; min-width: 0; }
> ```

```scss
@use '../../styles/variables' as *;

.footer-wrapper {
  font-family: $font-secondary;

  &.bg-dark,
  &.bg-primary,
  &.bg-secondary {
    color: $color-footer-text;

    a {
      color: rgba($color-footer-text, 0.8);
      &:hover { color: $color-footer-text; text-decoration: none; }
    }

    p, span { color: rgba($color-footer-text, 0.9); }

    // BSI Standard-Bibliothek setzt: .bsi-element-text-kkq2fq.bsi-text-dark p { color: $darkColor }
    // Spezifität: (0,2,1) — ohne expliziten p-Selektor verliert unser Override!
    .bsi-text-dark,
    .text-content,
    .bsi-text-dark p,
    .text-content p { color: $color-footer-text; }
  }

  &.bg-light {
    color: $color-dark;
    a { color: $color-primary; }
  }

  // Logo: figure targetieren — .footer-logo existiert nicht im BSI-Output!
  figure {
    max-width: $logo-width;
    margin-bottom: $spacing-md;
    img { max-width: 100%; height: auto; }
  }
}
```

#### `templates/shared/styles/footer.scss` anlegen

```scss
@use 'variables' as *;
@use '../content-elements/footer/styles' as *;
```

Anschließend in `templates/shared/styles/styles.scss` die Zeile `@use 'footer';` einkommentieren.

---

### 3.3 Shared Footer in website/design.js registrieren

```javascript
cx.contentElementGroup
  .withGroupId('footer-group-XXXXXX')
  .withLabel('Footer')
  .withContentElements(
    require('./../shared/content-elements/footer')
  ),
```

### 3.3b Website Footer Include aktualisieren (PFLICHT)

> **KRITISCH — ohne diesen Schritt kann der Redakteur die shared Footer-CE NICHT in die Website-Footer-Dropzone einfügen.**

**`templates/website/includes/footer/index.js`** — `withAllowedElements` auf shared Footer-CE umstellen:

```javascript
const {cx, Include} = require('@bsi-cx/design-build');

module.exports = cx.include
  .withIdentifier('footer-nJDYZP')
  .withName('Footer')
  .withEditable(true)
  .withFile(require('./template.twig'))
  .withDropzones(
    cx.dropzone
      .withDropzone('footer-dropzone-rR98ys')
      .withMaxAllowedElements(1)
      .withAllowedElements(
        require('./../../../shared/content-elements/footer')  // shared CE — NICHT layoutElements!
      )
  );
```

**`templates/website/includes/footer/template.twig`** — `data-bsi-dropzone-allowed-elements` auf shared Footer-CE-ID setzen:

```twig
{% apply spaceless %}
    {% set dropzoneId = dropzoneId ?: 'footer-dropzone-rR98ys' %}
    <div data-bsi-dropzone="{{ dropzoneId }}"
         data-bsi-dropzone-max-number-of-elements="1"
         data-bsi-dropzone-allowed-elements="footer-content-XXXXXX">
        {% block footer_element %}
            {% include './../../../shared/content-elements/footer/template.twig' %}
        {% endblock %}
    </div>
{% endapply %}
```

### 3.4 Shared Footer in landingpage/design.js registrieren

```javascript
cx.contentElementGroup
  .withGroupId('footer-lJ2X2V')
  .withLabel('Footer')
  .withContentElements(
    require('./../shared/content-elements/footer')
  )
```

In `templates/landingpage/_layout.twig`:
```twig
<div id="footer"
     data-bsi-dropzone="footer-dropzone-z8x25E"
     data-bsi-dropzone-max-number-of-elements="1"
     data-bsi-dropzone-allowed-elements="footer-content-XXXXXX">
```

---

### 3.6 Navigation anpassen

Alle Styles kommen ausschließlich in `templates/shared/styles/navigation.scss` (den Stub aus Schritt 1.6 ersetzen).

**Was NICHT angepasst wird** (BSI CX Architektur-Grenzen):
- Language-Switch-Logik (Alpine.js)
- Navigationsstruktur und -items
- Dropdown-JavaScript-Verhalten
- Mehrstöckige Navbar, Fixed/Sticky-Positionierung

### 3.6.1 Kundennavigation analysieren

| Eigenschaft | CSS-Eigenschaft |
|---|---|
| Navbar-Hintergrund | `background-color` auf `.navbar`, `header` |
| Nav-Link Farbe (default) | `color` auf `.nav-link`, `nav a` |
| Nav-Link Farbe (hover/aktiv) | `color` auf `.nav-link:hover`, `.active` |
| Aktiv-Indikator | `border-bottom`, `background`, `border-left` |
| `margin-bottom` | `-Xpx` bei border-bottom (verhindert Layout-Shift) |
| Font-Größe + Padding Links | `font-size`, `padding` auf `.nav-link` |

### 3.6.2 Navigation implementieren

`templates/shared/styles/navigation.scss` — Stub vollständig ersetzen:

```scss
@use 'variables' as *;

.navbar {
  background-color: $color-nav-bg;
  font-family: $font-secondary;
  border-bottom: 1px solid $color-grey-light;

  .navbar-brand {
    max-width: $logo-width;
    height: $logo-height;
    figure, img { margin: 0; max-width: 100%; height: auto; }
  }

  @media (max-width: #{$breakpoint-lg - 1px}) {
    .navbar-brand { max-width: calc(#{$logo-width} * 0.75); height: auto; }
  }

  .nav-link {
    color: $color-nav-link;
    font-family: $font-secondary;
    font-weight: $font-weight-regular;
    font-size: $font-size-small;
    border-bottom: 4px solid transparent;
    margin-bottom: -4px;

    &:hover, &:focus {
      color: $color-nav-link-hover;
      border-bottom-color: $color-primary;
      text-decoration: none;
    }
  }

  .navbar-nav .nav-link.active,
  .navbar-nav .nav-link.show {
    color: $color-nav-link-hover !important;
    border-bottom-color: $color-primary !important;
  }

  @media (max-width: #{$breakpoint-lg - 1px}) {
    .nav-link {
      font-size: 1rem;
      padding: 0.5rem 0.9375rem;
      border-bottom: none;
      margin-bottom: 0;
      &:hover, &:focus { color: $color-primary; border-bottom: none; background-color: transparent; }
    }
    .navbar-nav .nav-link.active,
    .navbar-nav .nav-link.show { color: $color-primary !important; border-bottom: none !important; }
  }

  .dropdown-menu {
    border-color: rgba($color-primary, 0.15);
    border-radius: $border-radius-sm;

    .dropdown-item {
      font-family: $font-secondary;
      font-size: $font-size-small;
      color: $color-text;
      &:hover, &:focus { background-color: rgba($color-primary, 0.06); color: $color-primary; }
    }
  }

  .navbar-nav .nav-item.dropdown:hover .dropdown-menu { display: block; margin: 0; }

  @media (max-width: #{$breakpoint-lg - 1px}) {
    .navbar-nav .nav-item.dropdown .dropdown-menu { display: block; border: none; padding: 0; }
  }

  .language-switch {
    .current-active { display: none; }
    .dropdown-language-switch { min-width: 54px; }
  }
}
```

---

## PFLICHT-BUILD

```bash
npm run build:dev
```

- [ ] `npm run build:dev` läuft ohne Fehler
- [ ] Footer erscheint in Website-Preview
- [ ] Footer erscheint in Landingpage-Preview
- [ ] Footer-Text ist lesbar (bei dunklem Hintergrund: weiß)
- [ ] Logo im Footer korrekt skaliert
- [ ] Navigation: Hover-Effekte funktionieren
- [ ] Navigation: Logo korrekt Desktop und Mobile

---

## HÄUFIGE FEHLER (Layout)

### Footer-Text bleibt dunkel (Spezifitätsproblem)
→ Immer `p` explizit mitangeben:
```scss
.footer-wrapper.bg-dark {
  .bsi-text-dark,
  .text-content,
  .bsi-text-dark p,
  .text-content p { color: $color-footer-text; }
}
```

### BSI Validierungsfehler: "Dropzone enthält Beispiel-Content-Element..."
→ Alle `textPartId`-Werte im Template auf `'text-part-Fjse59'` setzen.

### Footer-CE kann in Website NICHT in die Footer-Dropzone gezogen werden
→ `templates/website/includes/footer/index.js` prüfen: Hat `withAllowedElements()` noch `...layoutElements` statt `require('./../../../shared/content-elements/footer')`?
→ Schritt 3.3b durchführen.

---

## REFERENZEN

- BSI CX Docs: https://bsi-software.github.io/bsi-cx-docs/docs/26.1/design.html
- CLAUDE.md im Projektverzeichnis
- Element-IDs: `grep -r "withElementId" node_modules/@bsi-cx/design-standard-library-web/`
