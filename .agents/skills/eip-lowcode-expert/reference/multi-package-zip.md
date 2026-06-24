# Multi-Package ZIP Format (BSI EIP 26.1.8)

Use a multi-package ZIP when the import must create a **new CRM data model field** at the same time as the interfaces. The ZIP contains a CRM stage and an interfaces stage processed in order.

## Directory Structure

```
multi-index.json                          ← root orchestration file
01-crm/
  export-definition.json
  index.json
  datamodel/fields/<FieldName>-<entityId+attributeId>.json
02-interfaces/
  export-definition.json
  index.json
  interfaces/<Name>-<uuid>.json
  projects/<Name>-<uuid>.json
```

## multi-index.json

```json
{
  "_type" : "bsiscout.ConfigurationTransferMultiIndex",
  "_typeVersion" : "bsiscout-22.0.1001",
  "stages" : [ {
    "_type" : "bsiscout.ConfigurationTransferMultiIndexStage",
    "_typeVersion" : "bsiscout-22.0.1001",
    "customMetadata" : {
      "_type" : "crm.DataModelSyncStageCustomMetadata",
      "_typeVersion" : "crm-22.0.1001",
      "productIds" : [ "interfaces" ]
    },
    "exportId" : "<uuid-matching-crm-index>",
    "productId" : "crm",
    "rootPath" : "01-crm"
  }, {
    "_type" : "bsiscout.ConfigurationTransferMultiIndexStage",
    "_typeVersion" : "bsiscout-22.0.1001",
    "exportId" : "<uuid-matching-interfaces-index>",
    "productId" : "interfaces",
    "rootPath" : "02-interfaces"
  } ]
}
```

**Common mistakes:**

| Wrong | Correct |
|-------|---------|
| `bsiscout.MultiConfigurationTransferIndex` | `bsiscout.ConfigurationTransferMultiIndex` |
| `_typeVersion: "bsiscout-22.0.0"` | `_typeVersion: "bsiscout-22.0.1001"` |
| Stage without `_type` / `_typeVersion` | Every stage needs both fields |
| CRM stage without `customMetadata` | CRM stage **must** have `crm.DataModelSyncStageCustomMetadata` |
| Interfaces stage with `customMetadata` | Interfaces stage has **no** `customMetadata` |

Rules:
- `customMetadata.productIds` = `["interfaces"]` — the product that depends on the CRM data model
- Each stage's `exportId` must exactly match the `exportId` in its `index.json`
- Stage order matters: CRM first, then interfaces

## CRM stage — export-definition.json

```json
{
  "_type" : "bsiscout.ConfigurationExportDefinition",
  "_typeVersion" : "bsiscout-22.0.33",
  "productId" : "crm",
  "rootTransferIds" : [ {
    "_type" : "crm.DomainKeyConfigurationTransferId",
    "_typeVersion" : "crm-22.0.0",
    "domainKey" : "1;209633;190903;j1000200001"
  } ]
}
```

## Interfaces stage — export-definition.json

Add `importOptions` to auto-activate interfaces after import:

```json
{
  "_type" : "bsiscout.ConfigurationExportDefinition",
  "_typeVersion" : "bsiscout-22.0.33",
  "importOptions" : [ {
    "_type" : "bsiscout.ConfigurationImportOptions",
    "_typeVersion" : "bsiscout-23.2.001",
    "importOptionIds" : [ "interfaces.activate" ],
    "transferId" : { "id" : "interfaces.InterfaceConfigId:<interface-uuid>" }
  } ],
  "productId" : "interfaces",
  "rootTransferIds" : [ ... ]
}
```

## ZIP creation on Windows

Use the PowerShell builder — standard `zip` silently corrupts UTF-8 file names.  
See [`powershell-zip-encoding.md`](powershell-zip-encoding.md) for the complete script.

## Working example

`examples/weather-api/` is a complete multi-package ZIP with a CRM field + Lambda + Ad-Hoc batch.  
`examples/email-validation/` (in `output/`) is a Boolean CRM field + Lambda + Ad-Hoc batch.
