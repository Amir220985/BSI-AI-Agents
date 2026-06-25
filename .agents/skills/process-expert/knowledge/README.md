# BSI Process Knowledge Base

Wissensbasis aus der Analyse von 10 BSI-CustomerSuite-Exporten (2026-06-24).
9 Exporte = Prozessgruppen, 1 Export = 19 Prozesse + Stammdaten/Datenmodell/Integrationen.

## Dateien
| Datei | Inhalt |
|---|---|
| [process_inventory.md](process_inventory.md) | Übersicht aller Prozesse, Export-Struktur, Rollen, Schnittstellen, Auffälligkeiten |
| [bsi_step_type_catalog.md](bsi_step_type_catalog.md) | Abgeleiteter Step-Typ-Katalog (typeId → Funktion) |
| [process_patterns.md](process_patterns.md) | 12 wiederverwendbare Patterns (P1–P12) |
| [process_anti_patterns.md](process_anti_patterns.md) | 9 Anti-Patterns mit Risiko & Verbesserung (AP1–AP9) |
| [bsi_process_glossary.md](bsi_process_glossary.md) | Begriffe, Objekte, Rollen, technische Elemente |
| [bsi_process_design_rules.md](bsi_process_design_rules.md) | 20 Designregeln (R1–R20) |
| [process_generation_template.md](process_generation_template.md) | Template für neue Prozesse |
| [process_review_checklist.md](process_review_checklist.md) | Review-Checkliste |
| [audit_ap5_schnittstellen_fehlerpfade.md](audit_ap5_schnittstellen_fehlerpfade.md) | AP5-Audit: Fehlerpfad-Prüfung aller 45 Schnittstellen-/Lambda-Steps |
| [admin_ui_konfiguration.md](admin_ui_konfiguration.md) | Admin-UI-Wissen: Prozess- & Dokumentvorlagen-Konfiguration via Browser, Chrome-MCP-Gotchas |

## Registry
- [../registry/process_step_registry.json](../registry/process_step_registry.json) — maschinenlesbare Step-Typ-Registry v1.0.0 (19 typeIds, Templates, Bindings, Outlet-Deskriptoren)

## Werkzeuge
- [../tools/lint_process.py](../tools/lint_process.py) — statischer Prozess-Linter, der einen Export gegen die Design-Rules prüft (ERROR/WARN/INFO, `--json`, CI-tauglicher Exit-Code). Siehe [../tools/README.md](../tools/README.md).

## Nutzung bei Folgeaufgaben
1. Passende Patterns (P…) identifizieren → `process_patterns.md`
2. Designregeln (R…) anwenden → `bsi_process_design_rules.md`
3. Anti-Patterns (AP…) prüfen → `process_anti_patterns.md`
4. Review-Checkliste nutzen → `process_review_checklist.md`
5. Step-Typen nachschlagen → `bsi_step_type_catalog.md`

## Wichtige Vorbehalte
- Step-Typ-Bedeutungen sind aus Namen + Verschaltung **abgeleitet**, nicht aus offiziellem BSI-Katalog.
- Für **importierbare** Exporte gilt die technische Registry unter `bsi-ai-development/.agents/skills/process-expert/`.
- Quelldateien liegen unter `examples/` (bzw. lokal `/tmp/bsi_analysis/examples`) und wurden **nicht verändert**.
