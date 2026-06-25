---
name: cx-design
description: Richtet ein BSI CX Master Template Kundenprojekt ein und passt es an das Kundendesign an (Schriften, Farben, Navigation, Footer, Content-Elemente).
---

# CX Design Experte

## Rolle
Deine Aufgabe ist es, **BSI CX Master Template Web**-Projekte für Kundenprojekte einzurichten und vollständig an das Kundendesign anzupassen. Der Einstiegspunkt ist immer `/cx-setup` — dieser Skill orchestriert alle weiteren Schritte.

## Einstiegspunkt

**Lies und befolge immer zuerst `.agents/skills/cx-design/skills/cx-setup.md`** — nie direkt die untergeordneten Skills aufrufen, außer du wirst explizit aus `cx-setup` heraus dazu angewiesen.

`cx-setup` übernimmt:
- GitHub-Release herunterladen und entpacken
- npm install
- Projektname und Build-Konfiguration festlegen
- Kunden-URL ermitteln
- Vollständige Brand-Anpassung (via `cx-brand`)
- Element-Anpassung (via `cx-elements-customize`)

## Skill-Hierarchie

```
skills/cx-setup.md               ← einziger öffentlicher Einstiegspunkt
  ├── skills/cx-brand.md         ← Orchestrator: Schriften → Farben → Navigation/Footer
  │     ├── skills/cx-fonts.md         (Schriften, Logo, Favicon)
  │     ├── skills/cx-colors.md        (Farben, Bootstrap-Overrides)
  │     └── skills/cx-layout.md        (Footer ContentElement, Navigation)
  └── skills/cx-elements-customize.md  ← systematische Element-Anpassung
        └── skills/cx-element-create.md  (wenn neue ContentElements/Includes erstellt werden)
```

Alle Pfade sind relativ zu `.agents/skills/cx-design/`.

Alle Skills außer `cx-setup.md` sind **interne Sub-Skills** — sie werden ausschließlich aus dem jeweiligen übergeordneten Skill heraus geladen, nie direkt.

## Abgrenzung

- **cx-design** (dieser Skill): BSI CX Master Template Web — Frontend-Projekt, SCSS, Twig, design.js.
- **cx-expert**: BSI CX Studio / `studio` — Marketing Automation, Customer Stories.
- **eip-lowcode-expert**: BSI EIP — Schnittstellen und Low-Code-Prozesse.

## Wann diesen Skill nutzen

- "Richte ein BSI CX Projekt für Kunde X ein"
- "Passe das Master Template an das Design von Kunde X an"
- "Erstelle ein neues CX-Template-Projekt"
- Immer wenn eine Kundenwebsite als Vorlage für ein BSI CX Design-Projekt dient

## Richtlinien

1. **Nur `cx-setup.md` von außen aufrufen** — der Skill führt den vollständigen Setup-Prozess interaktiv durch.
2. **Niemals `webpack.config.js` verändern** — Build-Konfiguration ist abgeschlossen.
3. **Niemals `.github/workflows/build-template.yml` verändern** — nur auf explizite Anfrage.
4. Alle generierten Artefakte landen im Kundenprojektordner (nicht im Workshop-Verzeichnis).
