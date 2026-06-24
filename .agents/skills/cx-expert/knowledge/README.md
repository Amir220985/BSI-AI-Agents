# CX Expert – Knowledge Base

Wissensbasis für BSI CX (`studio`), abgeleitet aus 17 Beispiel-Exporten (`../examples/`) und dem BSI-CX-Help-Center.

| Datei | Inhalt |
|---|---|
| [cx_export_format.md](cx_export_format.md) | ZIP-/Index-Struktur, ID-Typen, itemGroupId, Multi-Paket, Story-/Step-Objektmodell |
| [cx_step_type_catalog.md](cx_step_type_catalog.md) | Step-Typen nach den 5 Step-Arten (aus 489 Steps) |
| [cx_story_inventory.md](cx_story_inventory.md) | 20 analysierte Stories mit Komplexität & Mustern |
| [cx_content_and_design.md](cx_content_and_design.md) | Content-Typen, Design, Medien, Verknüpfungslogik |
| [cx_patterns.md](cx_patterns.md) | Wiederverwendbare Story-Patterns (CXP1–CXP8) |
| [cx_glossary.md](cx_glossary.md) | Begriffe, Objekte, Konzepte |
| [cx_design_rules.md](cx_design_rules.md) | Designregeln CXR1–CXR20 |
| [cx_generation_template.md](cx_generation_template.md) | Spezifikations-Template für neue Stories |
| [cx_review_checklist.md](cx_review_checklist.md) | Review-/Import-Checkliste |

Maschinenlesbare Step-Registry: [../registry/cx_step_registry.json](../registry/cx_step_registry.json).

## Nutzung
1. Pattern wählen (`cx_patterns.md`) → 2. Steps aus `../registry/cx_step_registry.json` → 3. Designregeln anwenden (`cx_design_rules.md`) → 4. aus `../examples/` ableiten → 5. ZIP gemäß export-expert → 6. Review-Checkliste.

## Vorbehalte
- Step-Bedeutungen aus Namen/`customConfig` abgeleitet; verbindlich ist die BSI-Step-Bibliothek der Zielinstanz.
- Pflichtfeld-Listen je Index-Item sind beim ersten Testimport zu verifizieren (Round-Trip steht noch aus).
- Abgedeckt sind die in den Beispielen genutzten 59 Step-Typen; weitere bei Bedarf aus neuen Exporten ergänzen.
