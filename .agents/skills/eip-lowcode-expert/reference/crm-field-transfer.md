# CRM Field Creation via Configuration Transfer (BSI EIP 26.1.8)

## ID type for CRM items

CRM data model fields use `crm.DomainKeyConfigurationTransferId` — **not** `bsiscout.IdConfigurationTransferId`.

```json
{
  "_type" : "crm.DomainKeyConfigurationTransferId",
  "_typeVersion" : "crm-22.0.0",
  "domainKey" : "1;209633;190903;j1000200001"
}
```

**domainKey format:** `version;serverId;clientId;jItemId`

- Use `209633` and `190903` as serverId/clientId (from the weather-api example — correct for BSI EIP 26.1.8)
- Item ID: `j1000200001`, `j1000200002`, etc. Increment for each new field
- **Never use `0` for serverId or clientId** — causes `ClassCastException` in `RolePermissionTransferMigrator` during import
- `itemGroupId` must match the clientId segment: `"crm.domain-key.190903"`

## CRM index.json — item structure

```json
{
  "_type" : "bsiscout.ConfigurationTransferItem",
  "_typeVersion" : "bsiscout-22.0.0",
  "dataModelNamespaceVersions" : [ "crm-25.2.2" ],
  "globalUniqueId" : "CrmCustomer/bsiscout.DataModelAttributeId:y-myField",
  "id" : {
    "_type" : "crm.DomainKeyConfigurationTransferId",
    "_typeVersion" : "crm-22.0.0",
    "domainKey" : "1;209633;190903;j1000200001"
  },
  "itemGroupId" : "crm.domain-key.190903",
  "names" : { "de" : "Mein Feld", "en" : "My Field" },
  "resourcePath" : "datamodel/fields/<filename>.json",
  "root" : true,
  "transferType" : "full",
  "typeVersions" : {
    "crm.DataModelFlagConfig" : "crm-22.0.0",
    "crm.DataModelItemConfig" : "crm-22.0.17",
    "crm.DataModelPersistenceFieldDefinition" : "crm-25.1.001",
    "crm.DataModelDataFieldConfig" : "crm-24.2.001",
    "crm.CodeFilterDefinitionContainer" : "crm-22.0.0",
    "crm.CodeFilterDefinition" : "crm-22.0.0"
  }
}
```

**Critical:** Omit `referencedItems` entirely when there are no code type references — do not set it to `[]`. An empty array triggers deserialization errors in BSI. Only set `referencedItems` for fields that reference a code list, using `crm.UidConfigurationTransferId` inside a `bsiscout.ConfigurationTransferReference`.

**globalUniqueId:**
- Simple attribute (Boolean, text, number): `"CrmCustomer/bsiscout.DataModelAttributeId:y-myField"`
- Relation to code type: `"CrmCustomer/bsiscout.DataModelRelationId:y-myField"`

## Field definition file

Placed at `datamodel/fields/<FieldName>-<entityId><qualifiedAttributeId>.json`.

```json
{
  "_type" : "crm.DataModelDataFieldConfig",
  "_typeVersion" : "crm-24.2.001",
  "dataFieldId" : "CrmCustomer/bsiscout.DataModelAttributeId:y-myField",
  "dataFieldKey" : "1;209633;190903;j1000200001",
  "definition" : {
    "_type" : "crm.DataModelPersistenceFieldDefinition",
    "_typeVersion" : "crm-25.1.001",
    "column" : true,
    "currencyReferenceItemId" : null,
    "dateReferenceItemId" : null,
    "dbIndexed" : false,
    "defaultValue" : null,
    "embeddingLambdaBinding" : null,
    "embeddingLambdaConsumerId" : null,
    "filter" : null,
    "list" : false,
    "lookupConstraints" : [ ],
    "onlyLeafSelectable" : false,
    "reverseRelationConfig" : null,
    "searchData" : null,
    "searchIndexed" : false,
    "sql" : "Y_MY_FIELD",
    "timemachineEnabled" : false,
    "timemachineMappingUuid" : null,
    "typeId" : "Boolean"
  },
  "filterVariantIds" : [ ],
  "itemConfig" : {
    "_type" : "crm.DataModelItemConfig",
    "_typeVersion" : "crm-22.0.17",
    "categoryId" : null,
    "descriptions" : { "und" : null },
    "entityId" : "CrmCustomer",
    "flags" : [
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.DeprecatedItem","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.DisabledForConstraintClause","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.DisabledForSelectClause","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.LookupActiveFilterEnabled","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.LookupByTextDisabled","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.LookupHierarchical","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.LookupList","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.LookupSearchRequired","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.LowLevelItem","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.Mandatory","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.ReadOnlyUi","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.RelationTargetDisabled","value":true },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"bsiscout.TopField","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"crm.NotSyncable","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"crm.RemotelyNotAvailable","value":false },
      { "_type":"crm.DataModelFlagConfig","_typeVersion":"crm-22.0.0","flagId":"crm.UniqueValue","value":false }
    ],
    "names" : { "und" : "Mein Feld", "en" : "My Field" },
    "partitionContainer" : {
      "_type" : "crm.CodeFilterDefinitionContainer",
      "_typeVersion" : "crm-22.0.0",
      "filters" : [ { "_type":"crm.CodeFilterDefinition","_typeVersion":"crm-22.0.0","visible":true } ]
    },
    "patch" : false,
    "roleContainer" : {
      "_type" : "crm.CodeFilterDefinitionContainer",
      "_typeVersion" : "crm-22.0.0",
      "filters" : [ { "_type":"crm.CodeFilterDefinition","_typeVersion":"crm-22.0.0","visible":true } ]
    }
  }
}
```

## valueMigrationIds for the CRM index

Copy the 58 CRM-specific UUIDs verbatim from `examples/weather-api/01-crm/index.json`.

## typeId values for common field types

| BSI type | `typeId` | SQL type |
|----------|----------|----------|
| Boolean | `"Boolean"` | `BOOLEAN` or `BIT` |
| Short text | `"Text60"` | `VARCHAR(60)` |
| Long text | `"Text250"` | `VARCHAR(250)` |
| Integer | `"Integer"` | `INTEGER` |
| Decimal | `"Decimal"` | `DECIMAL` |
| Date | `"Date"` | `DATE` |
| Code reference | `"Key:Entity:CrmCode:<codeListUuid>"` | Foreign key |
