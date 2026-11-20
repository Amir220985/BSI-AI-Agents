# EIP Low-Code & Integrations-Beispiele

Dieses Verzeichnis enthält bewährte Vorlagen und Beispiel-Exporte aus realen Projekten für die BSI CustomerSuite.

## Übersicht der Beispiele

* **[bsi-eip-2026-06-23_10-51-52.zip](bsi-eip-2026-06-23_10-51-52.zip)**
  * **Inhalt**: CSV-Import-Interface mit Collections (10 Dateien, ~76 KB)
  * **Enthaltene Artefakte**:
    | Verzeichnis | Dateien |
    |---|---|
    | `interfaces/` | `Import_CSV` |
    | `projects/` | `Import_Data` |
    | `collections/` | `mappings`, `retries`, `processedRecords` (je mit Resource-Datei) |
    | `presets/` | `default` |
    | Root | `index.json`, `export-definition.json`, `export-log.txt` |
  * **Besonderheiten**:
    * Minimales Beispiel-ZIP — ideal als Vorlage für einfache Interface-Exporte mit wenigen Abhängigkeiten.
    * Zeigt die Pflichtstruktur jeder Export-ZIP: `index.json` (Manifest), `export-definition.json` (Metadaten zum Export), `export-log.txt` (Protokoll).
    * Collections liegen immer als Paar vor: `<name>-<uuid>.json` (Konfiguration) + `resource-<uuid>` (Binärdaten des Key-Value-Stores).

* **[bsi-eip-2026-06-23_10-57-43.zip](bsi-eip-2026-06-23_10-57-43.zip)**
  * **Inhalt**: Vollständiger CRM- & Projekt-Export mit allen abhängigen Artefakten (60 Dateien, ~73 MB)
  * **Enthaltene Artefakte**:
    | Verzeichnis | Dateien |
    |---|---|
    | `interfaces/` | `export_crm`, `export_project`, `trigger_import_full`, `import_project`, `import_crm` |
    | `collections/` | `businesses_crm`, `chatConversations_crm`, `cities_crm`, `cases_crm`, `documents_crm`, `customers_project`, `socialMediaPosts_project`, `occurrences_crm`, `occurrences_project`, `codes_crm`, `customers_crm`, `metadata`, `tasks_crm`, `processing_failedMutations`, `processing_importedObjectMappings`, `processing_unresolvedGlobalKeys`, `metadata_currencyVat`, `metadata_customerTypeImportOrder`, `settings`, `mappings_codes`, `communications_crm`, `cases_project` |
    | `scripts/` | `project_export`, `project_import`, `crm_import`, `helper`, `data_types`, `data_types_project`, `data_types_layer`, `timeshift`, `settings`, `metadata`, `layer_export`, `layer_import` |
    | `projects/` | `Volta_Daten` |
    | Root | `index.json`, `export-definition.json`, `export-log.txt` |
  * **Besonderheiten**:
    * Großes Referenz-ZIP — zeigt, wie ein vollständiges Migrationsprojekt mit allen voneinander abhängigen Interfaces, Collections und Shared Scripts verpackt wird.
    * Shared Scripts (`helper`, `data_types`, `timeshift` etc.) werden im Verzeichnis `scripts/` gebündelt und von mehreren Interfaces referenziert.
    * `processing_*`-Collections (`failedMutations`, `importedObjectMappings`, `unresolvedGlobalKeys`) sind Laufzeit-Sammlungen des Import-Prozesses und müssen mit exportiert werden, damit Folgeläufe korrekt weiterarbeiten können.
    * Collections mit großen Resource-Dateien (bis ~20 MB) enthalten die exportierten CRM-Rohdaten und werden beim Import als Zwischenspeicher für das Import-Interface befüllt.

### Struktur einer Export-ZIP

Jede valide BSI-Export-ZIP enthält mindestens:

```
export-definition.json   ← Metadaten: BSI-Version, Export-Zeitstempel, enthaltene Typen
index.json               ← Manifest: Liste aller Artefakte mit UUID und Typ
export-log.txt           ← Protokoll des Export-Vorgangs (informativ)
interfaces/              ← EIP-Interface-JSONs (<name>-<uuid>.json)
collections/             ← Collection-Konfig (<name>-<uuid>.json) + Resource (<name>-<uuid>, binär)
scripts/                 ← Shared TypeScript-Skripte (<name>-<uuid>.json)
projects/                ← Projekt-Definitionen (<name>-<uuid>.json)
presets/                 ← Preset-Definitionen (<name>-<uuid>.json)
```

### Dateinamenskonventionen
- EIP-Konfigurationen: `*.json`
- Collection-Ressourcen (Binär): `resource-<uuid>` (keine Dateiendung)
- Alle Artefakt-Dateien folgen dem Schema: `<lesbarer-name>-<uuid>[.json]`

