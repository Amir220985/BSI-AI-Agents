# CX Expert – Beispiel-Exporte

17 reale BSI-CX-Exporte vom **2026-06-24** (`bsi-cx-2026-06-24_*.zip`), Produkt **`studio`**, Version **26.1.8**.
Grundlage der Wissensbasis unter [`../knowledge/`](../knowledge/) und der Step-Registry [`../registry/cx_step_registry.json`](../registry/cx_step_registry.json).

## Übersicht (Zeitstempel → Story / Inhalt)

| Export `bsi-cx-2026-06-24_…` | Typ | Story(s) | Inhalt |
|---|---|---|---|
| `16-32-20` | **Multi** (CRM+studio) | OVB Companion | großer Companion-Flow (179 Steps) |
| `16-33-23` | studio | ENRA Antragsstrecke | 9 Content, 3 Design, 7 Indikatoren, 3 Medien |
| `16-33-32` | studio | inSign – Feststellung wirtschaftl. Berechtigung | 9 Content, 4 Design |
| `16-33-40` | studio | inSign Antragsstrecke (live) | 4 Content, 2 Design, 1 Medium |
| `16-33-47` | studio | inSign Demostory | 5 Content, 2 Design |
| `16-33-54` | studio | Nach Schadenfall (live) | 6 Content, 3 Design, 6 Medien |
| `16-34-03` | **Multi** | NPS Umfrage mit AI | AI/Brain + Feedback |
| `16-34-10` | **Multi** | Newsletter Welcome Mailing · Preference Center | Mailing + Präferenzen |
| `16-34-17` | **Multi** | Newsletter Anmeldung · Welcome Mailing · Preference Center | Double-Opt-in-Strecke |
| `16-34-25` | studio | KPI Simulieren für Flavor Mailing | Minimalbeispiel: 1 Flavor, 7 Indikatoren |
| `16-34-40` | **Multi** | Preference Center Plus | **Substory** |
| `16-34-47` | **Multi** | Preference Center | Präferenzverwaltung |
| `16-34-54` | studio | Schoko-Quiz | Gamification, 8 Content, 3 Medien |
| `16-35-13` | studio | SEPA-Mandatsdaten einholen | kompakte Self-Service-Strecke |
| `16-35-21` | **Multi** | Self-Service 2024 | Online + CRM (41 Steps) |
| `16-38-40` | studio | Beispiel Pass | mit **3 konfigurierten Steps** (Low-Code) |
| `16-38-48` | studio | Campaign Genius: Silicon Sampling (live) | 10 Content, 13 Medien (56 Steps) |

## Struktur (Kurz)
- **Einzelprodukt-Export:** `index.json` + `export-definition.json` + Ordner `stories/ contents/ designs/ flavors/ indicators/ media-library-items/ start-folders/ settings/ configured-step/`.
- **Multi-Paket:** `multi-index.json` + `01-crm/` + `02-studio/` (je eigener Export). Importreihenfolge CRM → studio.
- **Content/Design** sind **Ordner** (`content.json`/`design.json` + `*.html`/Medien).

Format-Details: [../knowledge/cx_export_format.md](../knowledge/cx_export_format.md).

## Hinweise
- **Nicht verändern** — Referenzmaterial.
- Mit Python (`zipfile`, cp437→UTF-8) entpacken, da `unzip` im iCloud-Verzeichnis bei Umlaut-Dateinamen scheitert.
- Enthält Marketing-Konfiguration und Medien; keine produktiven personenbezogenen Daten in die Wissensbasis übernehmen.
