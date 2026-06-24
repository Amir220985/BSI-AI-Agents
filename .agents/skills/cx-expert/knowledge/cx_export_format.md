# BSI CX (studio) – Exportformat

> Abgeleitet aus 17 BSI-CX-Exporten vom 2026-06-24 (`examples/bsi-cx-2026-06-24_*.zip`).
> Produkt: **`studio`** (technischer Name von BSI CX), `productVersion` **26.1.8**, Typfamilie `bsiscout.ConfigurationTransfer*` (wie CRM/EIP).
> Fakten sind belegt; interpretierte Bedeutungen sind als *(Annahme)* markiert.

## 1. ZIP-Grundstruktur (Einzelprodukt-Export)

```
<export>.zip
├── index.json                  # bsiscout.ConfigurationTransferIndex (Manifest)
├── index-watermarked.json      # identisch + Wasserzeichen (optional)
├── export-definition.json      # bsiscout.ConfigurationExportDefinition (productId, rootTransferIds)
├── export-log.txt
├── stories/        <Name>-<uuid>.json                       (studio.StoryConfig)
├── contents/       <Name>-<uuid>-<rev>/content.json + content-resource-<lang>.html
├── designs/        <Name>-<uuid>-<rev>/design.json + Ressourcen
├── flavors/        <Name>-<uuid>.json                       (studio.FlavorConfig)
├── indicators/     <Name>-<uuid>.json                       (KPI/Indikator)
├── media-library-items/  <datei>-<uuid>/media-library-item.json + Binärdatei
├── start-folders/  Ordnerstruktur (start.folder)
├── settings/       suite.setting / suite.setting-descriptor
└── configured-step/ <Name>-<uuid>.json                      (studio.configuredStep, Low-Code)
```

**Content und Design sind Ordner**, nicht einzelne JSON: `content.json`/`design.json` plus zugehörige `*.html`, Bilder, `.docx` etc. Das erklärt die vielen html/jpg/png/docx im Export.

## 2. `export-definition.json`

```json
{
  "_type": "bsiscout.ConfigurationExportDefinition",
  "_typeVersion": "bsiscout-22.0.33",
  "exportFilename": "bsi-cx-...zip",
  "productId": "studio",
  "rootTransferIds": [
    { "_type": "bsiscout.IdConfigurationTransferId", "_typeVersion": "bsiscout-22.0.0",
      "id": "studio.StoryConfigId:<uuid>" }
  ]
}
```
Wurzelobjekt eines Story-Exports ist die Story (`studio.StoryConfigId:<uuid>`).

## 3. `index.json` – Pflichtfelder (Root)

| Feld | Wert |
|---|---|
| `_type` | `bsiscout.ConfigurationTransferIndex` |
| `_typeVersion` | `bsiscout-22.0.0` |
| `exportDate` | `"YYYY-MM-DD HH:mm:ss.SSS"` |
| `exportId` | UUID |
| `exportUser` | Username |
| `productIdentifier` | **`"studio"`** (Pflicht) |
| `productVersion` | **`"26.1.8"`** (Pflicht) |
| `valueMigrationIds` | **Pflicht** — 15 UUIDs; aus einem Beispiel-Export (`index.json`) übernehmen |

> `valueMigrationIds` und `dataModelNamespaceVersions` immer aus einem **passenden Beispiel-Export gleicher Version** übernehmen — nicht erfinden. Studio-Namespace: `["studio-25.1.0","bsiscout-25.1.0","crm-25.2.2","crocus-1.0.0","oroya-1.0.0","start-22.0.0"]`.

## 4. Index-Items: ID-Typen & itemGroupId

| Artefakt | `itemGroupId` | `id._type` | `id`-Beispiel | transferType |
|---|---|---|---|---|
| Story | `studio.story` | `bsiscout.IdConfigurationTransferId` | `studio.StoryConfigId:<uuid>` | full |
| Story (Revision) | `studio.story.partial` | `studio.UuIdWithRevisionConfigurationTransferId` | — | full |
| Flavor | `studio.flavor` | `bsiscout.IdConfigurationTransferId` | `studio.FlavorId:<uuid>` | full |
| Content | `studio.content` / `…partial` | `bsiscout.IdConfigurationTransferId` / Revision | `studio.ContentId:<uuid>` | full |
| Design | `studio.design` / `…partial` | dito | `studio.DesignId:<uuid>` | full |
| Indikator | `studio.indicator` | `bsiscout.IdConfigurationTransferId` | `studio.IndicatorId:<uuid>` | full |
| Media-Library-Item | `studio.media-library-item` | `bsiscout.IdConfigurationTransferId` | `studio.MediaLibraryItemId:<uuid>` | full |
| Konfigurierter Step | `studio.configuredStep` | `bsiscout.IdConfigurationTransferId` | `studio.ConfiguredStepId:<uuid>` | full |
| **Step-Typ** | `studio.step.type` | `bsiscout.IdConfigurationTransferId` | `studio.StepTypeId:<uuid>` | **reference-only** (Standard-Steps existieren im Zielsystem) |
| Outlet-Funktionstyp | `studio.outlet-function-type` | dito | `studio.OutletFunctionTypeId:<uuid>` | reference-only |
| Ordner | `start.folder` | `bsiscout.IdConfigurationTransferId` | — | full |
| Verantwortliche | `start.responsible` | `start.ResponsibleConfigurationTransferId` | — | meist reference-only |
| String-Entity-Key | `start.string-entity-key` | `suite.StringEntityKeyConfigurationTransferId` | — | je nach Fall |
| Einstellung | `suite.setting` / `…-descriptor` | — | — | full |
| Referenzierte CRM-Codes | `crm.configurable-code-type.<N>.main` u. a. | `crm.UidConfigurationTransferId` / `crm.DomainKeyConfigurationTransferId` | wie CRM-Export | reference-only (existieren im CRM) |

**resourcePath-Muster** (nur bei `full`):
- `stories/<Name>-<uuid>.json`
- `flavors/<Name>-<uuid>.json`
- `indicators/<Name>-<uuid>.json`
- `contents/<Name>_(<contentType>)_-_Version_<n>-<uuid>-<rev>/content.json`
- `designs/<Name>_(<type>)_-_Version_<n>-<uuid>-<rev>/design.json`
- `media-library-items/<datei>-<uuid>/media-library-item.json`
- `configured-step/<Name>-<uuid>.json`

**Konsistenzregel** (wie export-expert): Jede in `referencedItems` referenzierte ID braucht einen eigenen Index-Eintrag — entweder `full` (mitgeliefert) oder `reference-only` (im Zielsystem vorhanden, `optionalType: "preserve"`). Standard-Step-Typen, Outlet-Funktionstypen und CRM-Codes sind typischerweise `reference-only`.

## 5. Multi-Produkt-Paket (CX + CRM gemeinsam)

Beispiel `bsi-cx-2026-06-24_16-32-20`:
```
<export>.zip
├── multi-index.json     # bsiscout.ConfigurationTransferMultiIndex
├── 01-crm/              # vollständiger crm-Export (eigene index.json)
└── 02-studio/           # vollständiger studio-Export (eigene index.json)
```
`multi-index.json.stages[]` listet je Stage `productId`, `rootPath` (`01-crm`/`02-studio`), `exportId` und `foreignIdMappings` (ID-Mapping zwischen den Produkten). Reihenfolge der Stages = Importreihenfolge. *(CRM zuerst, dann studio, da studio CRM-Codes referenziert — Annahme, durch Stage-Reihenfolge gestützt.)*

## 6. Story-Objektmodell

`studio.StoryConfig`
| Feld | Bedeutung |
|---|---|
| `name`, `gid`, `id` | Bezeichnung, globale GUID, Versions-ID |
| `flavorId` | Pflicht-Zuordnung zu einem **Flavor** (Story-Typ, z. B. Journey/Mailing) |
| `status` | `draft` / `live` / `sunset` |
| `executionType` | `manual` / `auto` |
| `steps[]` | `studio.StepConfig` (siehe unten) |
| `groups[]` | `studio.GroupConfig` (visuelle Gruppierung mit Farbe) |
| `properties[]` | `studio.PropertyConfig` — **Story-Attribute** |
| `responsible` | `start.Responsible` |
| `storyFolderId` | Ablageordner |
| `substory`, `template` | Substory- bzw. Musterstory-Flag |
| `plannedSunsetDate`, `plannedArchivingDate` | automatische Statuswechsel |

`studio.StepConfig`
| Feld | Bedeutung |
|---|---|
| `stepTypeId` | UUID → `studio.step.type` (Step-Bibliothek, meist reference-only) |
| `customConfig` | step-spezifische Konfiguration; **`_type` = Step-Identität** (Registry-Schlüssel) |
| `outlets[]` | `studio.OutletConfig`: `targetStepGid` (Ziel-Step über **gid**), `descriptorId`, `connectorPoints`, `name`, `presentation`, `outletFunctionConfigs`, `indicatorIds` |
| `properties[]` | Step-Attribute (in Folge-Steps via Picker nutzbar) |
| `executionType` | `auto` / `manual` |
| `temporalConfig` / `timelineConfig` | Ausführungszeitpunkt/-rhythmus |
| `participantStrategy` | Verhalten bei Teilnehmer-Erzeugung |
| `position`, `groupId` | Layout/Gruppe |

**Outlet-Verschaltung:** Verbindungen laufen über `outlets[].targetStepGid` (Ziel-Step-`gid`). Wie bei CRM-Prozessen existiert `descriptorId`; Outlets ohne direktes Ziel können darüber verknüpft sein — bei Analyse/Validierung berücksichtigen.

## 7. Content & Design

- **Content** (`studio.Content`): Felder `contentType`, `name`, `status`, `storyGid` (Verknüpfung zur Story), `contentRevision`, `latestRevision`, `folderId`, `validFromDate`/`validUntilDate`, `tags`. Der eigentliche Inhalt liegt als `content-resource-<lang>.html` (mehrsprachig) im selben Ordner.
- **Content-Typen** (Doku): `email`, `landing-page`, `word-document`, `pdf-document`, `sms`, `news-snippet`, `whatsapp`, `gespraechsleitfaden`, `ical`, `preview`. In den Beispielen vertreten: landing-page (33), email (11), word-document (7), sms (2), preview (1).
- **Design** (`studio.DesignConfig`): Layoutvorlage; nur für `email`, `landing-page`, `gespraechsleitfaden`, `preview` relevant. Content referenziert ein Design.
- **Media-Library-Item**: Binärdatei (jpg/png/docx) + Metadaten-JSON.

## 8. Weitere Artefakte

- **Flavor** (`studio.FlavorConfig`): Story-Typ/Kategorie; definiert u. a. verfügbare KPIs. Pflicht je Story.
- **Indikator** (`studio.indicator`): KPI-Zähler (z. B. „Versendete E-Mails", „Conversion", „Bounces"), an Outlets gesetzt (`outlets[].indicatorIds`).
- **Konfigurierter Step** (`studio.configuredStep`): per Low-Code/JavaScript erstellter Custom-Step; erscheint in der Step-Bibliothek. customConfig-Typ häufig `studio.ConfiguredInvokeLambdaStepletConfig` oder `crocus.*`.

## Offene Fragen / zu verifizieren
- Vollständige Pflichtfeld-Liste je `studio.*`-Index-Item (analog zur CRM-Tabelle im export-expert) — beim ersten Testimport verifizieren.
- Genaue Importreihenfolge im Multi-Paket (Annahme: CRM vor studio).
- `globalUniqueId`-Ableitung für studio-Items: in den Beispielen = die UUID des Objekts (z. B. Story-UUID). Bei Referenzen auf CRM-Codes gelten die CRM-Regeln des export-expert.
