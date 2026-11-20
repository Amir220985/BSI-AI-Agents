# Skill: BSI CX — Content Element Anpassung an Kundendesign

## Wann diesen Skill nutzen
Nach Abschluss der globalen Brand-Anpassungen (Schriften, Farben, Navigation, Footer via `cx-brand`).
Ziel: Jedes BSI Content-Element wird auf die Kundenwebsite gemappt, analysiert und ggf. angepasst.

## Verwandte Skills
- **`cx-brand`** — muss vorher abgeschlossen sein (globale Tokens, variables.scss, properties.js)
- **`cx-element-create`** — laden wenn StyleConfigs, neue ContentElements oder Includes erstellt werden müssen
  → `.agents/skills/cx-design/skills/cx-element-create.md`

---

## EINSTIEG — Scope klären

**Bevor mit der Analyse begonnen wird, Scope mit dem Nutzer klären:**

> Sollen **alle Elemente** systematisch durchgegangen werden,  
> oder gezielt **bestimmte Elemente** angepasst werden (z.B. nur Buttons, nur Accordion)?

**Option A — Gezielt (ein oder mehrere benannte Elemente):**
→ Direkt zu Phase 2 springen. Element-Mapping entfällt.
→ Für jedes genannte Element: Analyse + Variante bestimmen + implementieren.

**Option B — Alle Elemente systematisch:**
→ Phase 1 vollständig durchführen (Mapping + Tabelle), dann alle Elemente nacheinander durch Phase 2.

---

## PHASE 1 — Element-Mapping: BSI-Elemente auf Kundenelemente abbilden

### 1.1 Alle registrierten BSI-Elemente ermitteln

```bash
grep -r "withElementId\|withLabel" templates/website/design.js templates/landingpage/design.js
```

Vollständige Liste aller Standard-Bibliotheks-Elemente: `CLAUDE.md § 5`.

### 1.2 Kundenwebsite auf Gegenstücke durchsuchen

Für jedes BSI-Element: Gibt es auf der Kundenwebsite ein funktionales Äquivalent?

```bash
curl -s "https://www.kunde.de/beispielseite/" > page.html

grep -oiE '<h[1-6][^>]*>.*?</h[1-6]>' page.html
grep -iE 'accordion|details|collapse|expandable' page.html
grep -iE '<button|class="btn|cta' page.html
grep -iE 'card|tile|teaser' page.html
grep -iE 'linkedin|xing|twitter|facebook|youtube|instagram' page.html
grep -iE '<form|input|select|textarea' page.html
```

### 1.3 Mapping-Tabelle anlegen

| BSI-Element | Kundenäquivalent | URL-Beispiel | Vorhanden? |
|---|---|---|---|
| `h1`–`h6` | Seitenüberschriften | /startseite/ | ✓ |
| `text` | Fließtext | /ueber-uns/ | ✓ |
| `button` | CTA-Buttons | /kontakt/ | ✓ |
| `accordion` | FAQ-Akkordeon | /faq/ | ✓ |
| `card` | Teaser-Karten | /leistungen/ | ✓ |
| `social-media-follow` | Social-Icons Footer | /footer | ✓ |
| `video` | Eingebettete Videos | — | ✗ |

Elemente die beim Kunden **nicht vorkommen** werden trotzdem analysiert und angepasst — Redakteure könnten sie später verwenden.

---

## PHASE 2 — Analyse und Entscheidung je Element

Für jedes vorhandene Element aus der Mapping-Tabelle:

**Analyseschritt:**
1. Kundensite im Browser öffnen, Element per DevTools inspizieren
2. Welche CSS-Eigenschaften weichen vom BSI-Default ab? (Farbe, Schrift, Abstände, Border, Icon, Radius, Shadow)
3. Wurde die Abweichung durch globale Tokens bereits behoben?
4. Entscheidungsbaum → eine der vier Varianten wählen (Kombinationen erlaubt)

---

## VARIANTE 1 — Globale Anpassung reicht aus

**Wann:** Element entspricht dem Kundendesign durch die bereits gesetzten globalen Tokens.

### Prüfung: Konfigurationsoptionen bereinigen

```bash
grep -A 20 "withLabel" node_modules/@bsi-cx/design-standard-library-web/content-elements/base/ELEMENT/index.js
```

**Nicht verwendete Optionen entfernen:**

```javascript
// templates/shared/configs/styles/button-layout.js
module.exports = StyleConfig.create()
  .withLabel('Layout')
  .withCssClasses(
    { cssClass: 'bsi-btn-filled', label: 'Gefüllt' },
    // { cssClass: 'bsi-btn-outline', label: 'Outline' },  // Kunde nutzt das nicht
  );
```

---

## VARIANTE 2 — Bestehende Konfigurationen anpassen / SCSS ergänzen

**Wann:** Globale Tokens reichen nicht; Abweichung ist durch Konfiguration oder SCSS behebbar.

### Schritt 1: Prüfen ob vorhandene StyleConfig-Optionen ausreichen

```bash
grep -r "cssClass" node_modules/@bsi-cx/design-standard-library-web/content-elements/base/ELEMENT/
```

### Schritt 2: StyleConfig um neue Option erweitern

> **SKILL LADEN:** `cx-element-create` aus dem Projekt lesen:
> `.agents/skills/cx-design/skills/cx-element-create.md`

```javascript
// templates/shared/configs/styles/accordion-header-bg.js
const {StyleConfig} = require('@bsi-cx/design-build');

module.exports = StyleConfig.create()
  .withLabel('Header Hintergrund')
  .withCssClasses(
    { cssClass: 'bsi-accordion-header-bg-primary',   label: 'Primär' },
    { cssClass: 'bsi-accordion-header-bg-secondary', label: 'Sekundär' },
  );
```

### Schritt 3: Custom SCSS für feste Kundenwerte

```scss
// templates/shared/content-elements/accordion/styles.scss
@use '../../styles/variables' as *;

.bsi-element-accordion-OowSb3 {
  .accordion-button {
    font-family: $font-primary;
    font-weight: $font-weight-medium;

    &:not(.collapsed) {
      background-color: $color-primary;
      color: $color-white;
    }
  }
}
```

> **Spezifitäts-Falle bei Text-Elementen:** BSI setzt `.bsi-element-text-kkq2fq.bsi-text-dark p { color: $darkColor }` mit Spezifität (0,2,1). Overrides für `p`-Inhalte immer mit `p` im Selektor schreiben:
> ```scss
> .mein-container .bsi-text-dark,
> .mein-container .bsi-text-dark p { color: $color-footer-text; }
> ```

---

## VARIANTE 3 — Neue StyleConfig-Dimension oder vollständiger Style-Override

**Wann:** Element braucht eine komplett neue Konfigurationsdimension.

> **SKILL LADEN:** `cx-element-create` aus dem Projekt lesen:
> `.agents/skills/cx-design/skills/cx-element-create.md`

```scss
// templates/shared/content-elements/card/styles.scss
@use '../../styles/variables' as *;

.bsi-element-card-crRST4 {
  border: none;
  border-radius: $border-radius-lg;
  box-shadow: 0 4px 12px rgba($color-primary, 0.12);

  .card-body { padding: $spacing-xl; }

  .card-title {
    font-family: $font-primary;
    color: $color-primary;
  }
}
```

---

## VARIANTE 4 — Custom Element erstellen (Standard-Element ersetzen)

**Wann:** Keine der vorherigen Varianten reicht. Das Kunden-Element hat eine grundlegend andere Struktur.

> **SKILL LADEN:** `cx-element-create` aus dem Projekt lesen:
> `.agents/skills/cx-design/skills/cx-element-create.md`

### Schritt 1: Element in shared/ anlegen

```
templates/shared/content-elements/accordion/
├── index.js        ← eigene Element-ID, eigene StyleConfigs
├── template.twig   ← ggf. embed des Standard-Prototype
└── styles.scss
```

### Schritt 2: Alle Dropzone-Referenzen auf die alte Element-ID aktualisieren

```bash
grep -rn "accordion-OowSb3" templates/
grep -rn "require.*base/accordion" templates/
```

### Schritt 3: In website/design.js und landingpage/design.js registrieren

```javascript
// NEU (in beiden design.js):
require('./../shared/content-elements/accordion')
```

---

## SHARED-ELEMENT-WRAPPER-MUSTER

Wenn ein Standard-Element mit eigenen StyleConfigs oder SCSS erweitert/ersetzt wird, gehört es nach `shared/`. Gilt ab Variante 2 wenn eigene Styles für ein Element angelegt werden.

**Warum `@use` und nicht `@import`?**
Die Einschränkung gilt nur für die **Entry-Dateien** (`website/styles/styles.scss`, `landingpage/styles/styles.scss`). Innerhalb von `shared/styles/` sind alle Dateien **Module** und kommunizieren per `@use`.

```scss
// templates/shared/styles/elements-custom.scss  (neu anlegen)
@use '../content-elements/accordion/styles';
@use '../content-elements/card/styles';
```

```scss
// templates/shared/styles/styles.scss — Eintrag ergänzen:
@use 'bootstrap-overrides';
@use 'fonts';
@use 'navigation';
@use 'elements';
@use 'elements-custom';   // ← neu
@use 'footer';
```

---

## ABSCHLUSS-CHECKLISTE JE ELEMENT

- [ ] BSI-Element auf Kundensite-Äquivalent gemappt
- [ ] Abweichungen in CSS-Eigenschaften identifiziert (DevTools)
- [ ] Variante bestimmt (V1 / V2 / V3 / V4 — Kombinationen erlaubt)
- [ ] Implementierung abgeschlossen
- [ ] Bei Custom-Element: alle Dropzone-Referenzen aktualisiert
- [ ] Bei Custom-Element: in `website/design.js` und `landingpage/design.js` registriert
- [ ] `npm run build:dev` läuft ohne Fehler
- [ ] Preview geprüft: Element entspricht Kundendesign

---

## HÄUFIGE FEHLER

### Element-ID-Konflikt nach Ersetzen
→ Nie Standard-Element-ID wiederverwenden. Alle Referenzen mit `grep -rn "alte-id" templates/` suchen.

### StyleConfig-Option ohne CSS-Wirkung
→ Jede neue `cssClass` in einer StyleConfig braucht eine entsprechende CSS-Regel in `styles.scss`.

### `p`-Text bleibt dunkel auf dunklem Hintergrund
→ BSI setzt `.bsi-element-text-kkq2fq.bsi-text-dark p` mit Spezifität (0,2,1). Override ohne `p` verliert — immer beide Selektoren schreiben: `.bsi-text-dark, .bsi-text-dark p`.

### Dropzone lässt neues Custom-Element nicht rein
→ `data-bsi-dropzone-allowed-elements` enthält noch die alte Standard-Element-ID.

### Nur website/design.js aktualisiert, landingpage vergessen
→ Bei allen Elementen in `shared/` immer **beide** `design.js`-Dateien aktualisieren.
