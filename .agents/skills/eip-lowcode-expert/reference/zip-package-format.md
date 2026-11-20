# BSI EIP ZIP Package Format Reference

This document describes the exact structure of BSI EIP configuration export ZIP packages. It is the authoritative reference for generating valid import packages for EIP product version 26.1.8.

---

## ZIP File Overview

Every BSI EIP export is a ZIP archive named using a timestamp:

```
bsi-eip-{YYYY-MM-DD_HH-MM-SS}.zip
```

Example: `bsi-eip-2026-06-23_09-21-32.zip`

### Required File Layout

```
bsi-eip-{timestamp}.zip
├── export-definition.json          (required, always at root)
├── export-log.txt                  (informational only, NOT needed for import)
├── index.json                      (required, always at root)
├── interfaces/
│   └── {InterfaceName}-{uuid}.json (one per interface, full config)
└── projects/
    └── {ProjectName}-{uuid}.json   (one per project)
```

**Filename convention for data files:** Replace spaces with underscores, append a dash and the UUID. Example: `IBAN_validation-af8cb193-e289-48d9-a9b6-36e30941909c.json`

**`export-log.txt`** is never required for import. It can be omitted entirely or provided as an empty/minimal file.

---

## `export-definition.json`

Located at the root of the ZIP. Describes what was exported.

### Structure

```json
{
  "_type" : "bsiscout.ConfigurationExportDefinition",
  "_typeVersion" : "bsiscout-22.0.33",
  "exportFilename" : "bsi-eip-2026-06-23_09-21-32.zip",
  "productId" : "interfaces",
  "rootTransferIds" : [ {
    "_type" : "bsiscout.IdConfigurationTransferId",
    "_typeVersion" : "bsiscout-22.0.0",
    "id" : "interfaces.InterfaceConfigId:{interface-uuid}"
  } ]
}
```

### Field Reference

| Field | Value | Notes |
|---|---|---|
| `_type` | `"bsiscout.ConfigurationExportDefinition"` | Always this value |
| `_typeVersion` | `"bsiscout-22.0.33"` | Always this value |
| `exportFilename` | `"bsi-eip-{timestamp}.zip"` | Must match the actual ZIP filename |
| `productId` | `"interfaces"` | Always `"interfaces"` for EIP configurations |
| `rootTransferIds` | array of ID objects | References the main interface(s) being exported |

### `rootTransferIds` Entry Structure

Each entry references one exported interface:

```json
{
  "_type" : "bsiscout.IdConfigurationTransferId",
  "_typeVersion" : "bsiscout-22.0.0",
  "id" : "interfaces.InterfaceConfigId:{interface-uuid}"
}
```

The `id` value is always in the format `interfaces.InterfaceConfigId:{uuid}` where `{uuid}` is the interface's `id` field (not its `gid`).

---

## `index.json`

Located at the root of the ZIP. The import system reads this to understand what is in the package and how to resolve dependencies.

### Complete Structure

```json
{
  "_type" : "bsiscout.ConfigurationTransferIndex",
  "_typeVersion" : "bsiscout-22.0.0",
  "exportDate" : "2026-06-23 09:22:56.565",
  "exportId" : "47bbf802-72f7-47db-8c6e-7461e28068e1",
  "exportUser" : "andrea.adams",
  "items" : [ ... ],
  "productIdentifier" : "interfaces",
  "productVersion" : "26.1.8",
  "valueMigrationIds" : [
    "454863f5-f931-4527-92ed-fcd1c5bbbc35",
    "9bded4bf-c647-4458-9969-cbdbb318e442",
    "cd76ad5f-c20c-4ce0-870c-dc1a09a15c94",
    "97abafd1-942b-4df0-97b5-ccb042bda038",
    "9ad5ef84-010e-4384-987c-dadf145c7c8a",
    "001d276d-b7b6-4e67-a218-29d0a63ab2ab",
    "ea64e793-b804-411c-85d0-df9a70bf8d91",
    "381fbdee-7c31-48fa-84d6-13dc2f9954dd"
  ]
}
```

### Top-Level Field Reference

| Field | Type | Notes |
|---|---|---|
| `_type` | string | Always `"bsiscout.ConfigurationTransferIndex"` |
| `_typeVersion` | string | Always `"bsiscout-22.0.0"` |
| `exportDate` | timestamp | Format: `"YYYY-MM-DD HH:MM:SS.mmm"` — use current date/time |
| `exportId` | UUID | Freshly generated UUID v4 for each export |
| `exportUser` | string | Username string (informational) |
| `items` | array | See Items section below |
| `productIdentifier` | string | Always `"interfaces"` |
| `productVersion` | string | Always `"26.1.8"` for EIP product version 26.1.8 |
| `valueMigrationIds` | array of UUIDs | **Must be copied verbatim** — see critical note below |

### CRITICAL: `valueMigrationIds`

These 8 UUIDs are tied to EIP product version 26.1.8 and are required for the import to succeed. They must always be present exactly as shown — do not generate new ones, do not reorder them:

```
454863f5-f931-4527-92ed-fcd1c5bbbc35
9bded4bf-c647-4458-9969-cbdbb318e442
cd76ad5f-c20c-4ce0-870c-dc1a09a15c94
97abafd1-942b-4df0-97b5-ccb042bda038
9ad5ef84-010e-4384-987c-dadf145c7c8a
001d276d-b7b6-4e67-a218-29d0a63ab2ab
ea64e793-b804-411c-85d0-df9a70bf8d91
381fbdee-7c31-48fa-84d6-13dc2f9954dd
```

---

## Items in `index.json`

The `items` array enumerates every entity referenced in the export. Items come in two classes:

### Item Classes

| Class | `transferType` | Has `resourcePath` | Has data file | Has `typeVersions` | Has `dataModelNamespaceVersions` |
|---|---|---|---|---|---|
| Full | `"full"` | yes | yes | yes | yes (main interface only) |
| Reference-only | `"reference"` | no | no | no | no |

### Item Group IDs

| `itemGroupId` | Description | Typical `transferType` |
|---|---|---|
| `"interfaces.interface"` | The main interface configuration | `"full"` |
| `"interfaces.project"` | A project grouping interfaces | `"full"` |
| `"interfaces.interface.partial"` | Partial/referenced interface | `"reference"` |
| `"interfaces.interface-type"` | Interface type (e.g. Lambda) | `"reference"` |
| `"interfaces.processor-type"` | Processor type used in the interface | `"reference"` |
| `"start.responsible"` | User responsible for the interface | `"reference"` |

### Full Item Structure

Used for the main interface and for projects. Includes all metadata and a file path.

```json
{
  "_type" : "bsiscout.ConfigurationTransferItem",
  "_typeVersion" : "bsiscout-22.0.0",
  "dataModelNamespaceVersions" : [ "bsiscout-25.1.0" ],
  "descriptions" : { "de" : "Version 1" },
  "globalUniqueId" : "{uuid}",
  "id" : {
    "_type" : "bsiscout.IdConfigurationTransferId",
    "_typeVersion" : "bsiscout-22.0.0",
    "id" : "interfaces.InterfaceConfigId:{uuid}"
  },
  "itemGroupId" : "interfaces.interface",
  "names" : { "de" : "IBAN validation" },
  "referencedItems" : [ ... ],
  "resourcePath" : "interfaces/IBAN_validation-{uuid}.json",
  "root" : true,
  "transferType" : "full",
  "typeVersions" : {
    "interfaces.InterfaceConfig" : "interfaces-24.2.017",
    "interfaces.ProcessorConfig" : "interfaces-22.0.1004",
    "interfaces.OutletConfig" : "interfaces-22.0.1006",
    "interfaces.Point" : "interfaces-22.0.0",
    "interfaces.TypeScriptConfig" : "interfaces-23.2.007",
    "interfaces.CrmLambdaProcessorConfig" : "interfaces-23.2.019",
    "interfaces.IterationProcessorConfig" : "interfaces-26.1.001",
    "interfaces.TypeScriptProcessorConfig" : "interfaces-23.2.018",
    "interfaces.RestConsumerProcessorConfig" : "interfaces-24.2.008",
    "bsiscout.Signature" : "bsiscout-24.1.001",
    "bsiscout.SignatureProperty" : "bsiscout-24.1.001",
    "start.Responsible" : "start-1.3.2"
  }
}
```

#### Full Item Field Notes

| Field | Rule |
|---|---|
| `dataModelNamespaceVersions` | Include only on the main interface item. Value: `["bsiscout-25.1.0"]` |
| `descriptions` | Localised description map, e.g. `{"de": "Version 1"}` |
| `globalUniqueId` | The `gid` UUID of the entity |
| `id.id` | The typed ID string, e.g. `"interfaces.InterfaceConfigId:{id-uuid}"` or `"interfaces.ProjectId:{id-uuid}"` |
| `names` | Localised name map, e.g. `{"de": "IBAN validation"}` |
| `referencedItems` | Array of reference-only items this full item depends on (see below) |
| `resourcePath` | Relative path inside the ZIP to the data file |
| `root` | `true` only on the main interface item; omit or set `false` on all others |
| `transferType` | `"full"` |
| `typeVersions` | Map of type name to version string. Only include types actually used in the interface config. Omit unused processor config types. |

#### `typeVersions` — Which Types to Include

Only include type version entries for types that actually appear in the interface's data file. Remove entries for processor config types that are not used. The following are always present:

```json
"interfaces.InterfaceConfig" : "interfaces-24.2.017",
"interfaces.ProcessorConfig" : "interfaces-22.0.1004",
"interfaces.OutletConfig"    : "interfaces-22.0.1006",
"interfaces.Point"           : "interfaces-22.0.0",
"interfaces.TypeScriptConfig": "interfaces-23.2.007",
"bsiscout.Signature"         : "bsiscout-24.1.001",
"bsiscout.SignatureProperty"  : "bsiscout-24.1.001",
"start.Responsible"          : "start-1.3.2"
```

Add processor-specific config types as needed:

| Processor Config Type | Version |
|---|---|
| `interfaces.CrmLambdaProcessorConfig` | `"interfaces-23.2.019"` |
| `interfaces.IterationProcessorConfig` | `"interfaces-26.1.001"` |
| `interfaces.TypeScriptProcessorConfig` | `"interfaces-23.2.018"` |
| `interfaces.RestConsumerProcessorConfig` | `"interfaces-24.2.008"` |

### Reference-Only Item Structure

Used for interface types, processor types, and the responsible user. Contains no data file.

```json
{
  "_type" : "bsiscout.ConfigurationTransferItem",
  "_typeVersion" : "bsiscout-22.0.0",
  "globalUniqueId" : "{uuid}",
  "id" : {
    "_type" : "bsiscout.IdConfigurationTransferId",
    "_typeVersion" : "bsiscout-22.0.0",
    "id" : "interfaces.ProcessorTypeId:{processor-type-uuid}"
  },
  "itemGroupId" : "interfaces.processor-type",
  "names" : { "de" : "TypeScript" },
  "referencedItems" : [ ],
  "transferType" : "reference"
}
```

Reference-only items do not include: `resourcePath`, `root`, `typeVersions`, `dataModelNamespaceVersions`, or `descriptions`.

### `referencedItems` Within Items

The main interface full item lists all reference-only items it depends on inside its `referencedItems` array. Each entry is an inline reference-only item (same structure as a top-level reference item). Projects typically have an empty `referencedItems` array.

---

## `projects/{ProjectName}-{uuid}.json`

One file per project. Projects group related interfaces.

### Structure

```json
{
  "_type" : "interfaces.Project",
  "_typeVersion" : "interfaces-22.0.0",
  "cooldownTimeInMinutes" : null,
  "id" : "{project-uuid}",
  "name" : "IBAN",
  "notes" : null,
  "recipients" : [ ],
  "responsible" : {
    "_type" : "start.Responsible",
    "_typeVersion" : "start-1.3.2",
    "userId" : "36317f78-6040-4648-936d-e8b66b394c0b"
  }
}
```

### Field Reference

| Field | Type | Notes |
|---|---|---|
| `_type` | string | Always `"interfaces.Project"` |
| `_typeVersion` | string | Always `"interfaces-22.0.0"` |
| `cooldownTimeInMinutes` | number/null | Typically `null` |
| `id` | UUID | The project's UUID (matches the filename and the index item) |
| `name` | string | Display name of the project |
| `notes` | string/null | Optional notes, typically `null` |
| `recipients` | array | Notification recipients, typically `[]` |
| `responsible` | object | See Responsible structure below |

### Responsible Structure (in Project)

```json
{
  "_type" : "start.Responsible",
  "_typeVersion" : "start-1.3.2",
  "userId" : "36317f78-6040-4648-936d-e8b66b394c0b"
}
```

The `userId` `36317f78-6040-4648-936d-e8b66b394c0b` is the system administrator user UUID in the target EIP installation.

---

## `interfaces/{InterfaceName}-{uuid}.json`

The main interface configuration file. See `interface-config.md` for the full reference on this file's structure.

---

## UUID Generation Rules

- All UUIDs (interface `id`, interface `gid`, processor `id`, processor `gid`, project `id`, `exportId`) must be freshly generated random UUIDs v4 for each new configuration.
- The `valueMigrationIds` in `index.json` are the **only** UUIDs that must NOT be generated fresh — they are fixed constants for product version 26.1.8.
- The `responsible.userId` (`36317f78-6040-4648-936d-e8b66b394c0b`) is a fixed system constant, not generated.
- The interface type UUID (`2512c737-a73b-4f78-9ae2-098ac6d291bd` for Lambda) is a fixed system constant.

---

## Timestamp Format

| Context | Format | Example |
|---|---|---|
| ZIP filename | `YYYY-MM-DD_HH-MM-SS` | `2026-06-23_09-21-32` |
| `exportDate` in index.json | `"YYYY-MM-DD HH:MM:SS.mmm"` | `"2026-06-23 09:22:56.565"` |
| `createDate`/`changeDate` in interface | `"YYYY-MM-DD HH:MM:SS.mmm"` | `"2026-06-23 09:19:43.951"` |

---

## Minimal Valid Package Checklist

To produce a valid importable ZIP package:

- [ ] `export-definition.json` present at root with correct `productId` and `rootTransferIds`
- [ ] `index.json` present at root with all 8 `valueMigrationIds` copied verbatim
- [ ] `index.json` contains a full item for the interface (with `resourcePath`, `typeVersions`, `root: true`)
- [ ] `index.json` contains a full item for the project
- [ ] `index.json` contains reference items for: interface type, all processor types used, responsible user
- [ ] Interface data file present at the `resourcePath` referenced in the index
- [ ] Project data file present at the path referenced in the index
- [ ] All freshly generated UUIDs are consistent between index.json and the data files
- [ ] Interface filename matches pattern: `{Name_with_underscores}-{interface-id-uuid}.json`
- [ ] Project filename matches pattern: `{ProjectName}-{project-id-uuid}.json`
