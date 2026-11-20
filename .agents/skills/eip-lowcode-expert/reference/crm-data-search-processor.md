# CRM Data Search Processor (BSI EIP 26.1.8)

Used in Ad-Hoc batch interfaces to search CRM entities.

## Correct type and version

```json
{
  "_type" : "interfaces.CrmDataModelSearchProcessorConfig",
  "_typeVersion" : "interfaces-26.1.001"
}
```

**Wrong (old):** `interfaces.CrmDataSearchProcessorConfig` / `interfaces-24.2.008` — causes deserialization errors in BSI 26.1.8.

## Complete processor config (example: all active customers with email)

```json
{
  "_type" : "interfaces.CrmDataModelSearchProcessorConfig",
  "_typeVersion" : "interfaces-26.1.001",
  "asListData" : false,
  "selection" : {
    "_type" : "bsiscout.DataModelRelationSelection",
    "_typeVersion" : "bsiscout-24.2.001",
    "alias" : "crmCustomers",
    "constraint" : {
      "_type" : "bsiscout.DataModelAndConstraint",
      "_typeVersion" : "bsiscout-8.0.0.034",
      "constraints" : [ {
        "_type" : "bsiscout.DataModelAttributeConstraint",
        "_typeVersion" : "bsiscout-9.0.0.039",
        "attribute" : "active",
        "fieldType" : "Boolean",
        "op" : "true",
        "operands" : [ ]
      } ]
    },
    "containerEntityId" : "Root",
    "distinct" : false,
    "maximumRowCount" : 10000,
    "namespaceVersions" : [ "bsiscout-25.1.0", "crm-25.2.2", "crocus-1.0.0", "cstudio-22.0.0", "interfaces-22.0.0", "oroya-1.0.0", "start-22.0.0" ],
    "relation" : "crmCustomers",
    "resultDoType" : "scout.DoEntity",
    "selections" : [ {
      "_type" : "bsiscout.DataModelAttributeSelection",
      "_typeVersion" : "bsiscout-8.0.0.040",
      "alias" : "id",
      "attribute" : "id",
      "fieldType" : "Key:Entity:CrmCustomer"
    }, {
      "_type" : "bsiscout.DataModelRelationSelection",
      "_typeVersion" : "bsiscout-24.2.001",
      "alias" : "preferredElectronicAddress",
      "relation" : "preferredElectronicAddress",
      "selections" : [ {
        "_type" : "bsiscout.DataModelAttributeSelection",
        "_typeVersion" : "bsiscout-8.0.0.040",
        "alias" : "rawAddress",
        "attribute" : "rawAddress",
        "fieldType" : "Text250"
      } ],
      "targetType" : "Entity:CrmElectronicAddress"
    } ],
    "targetType" : "List:Entity:CrmCustomer"
  }
}
```

## Required fields on DataModelRelationSelection

| Field | Description |
|-------|-------------|
| `_type` | `bsiscout.DataModelRelationSelection` |
| `_typeVersion` | `bsiscout-24.2.001` |
| `alias` | Name for access in TypeScript scripts |
| `containerEntityId` | Always `"Root"` for top-level searches |
| `distinct` | Boolean |
| `namespaceVersions` | List of active namespace versions |
| `resultDoType` | Always `"scout.DoEntity"` |
| `targetType` | `"List:Entity:<EntityName>"` for top-level, `"Entity:<EntityName>"` for nested |

## TypeScript access to search results

```typescript
// Inside an Iteration processor that iterates the search results:
const customerId = invocation.processors.crmSearch.element.id;
const email = invocation.processors.crmSearch.element.preferredElectronicAddress?.rawAddress;
```

## Adding a custom field constraint

To filter on a custom Boolean field (e.g. `y-emailAddressValid`):

```json
{
  "_type" : "bsiscout.DataModelAttributeConstraint",
  "_typeVersion" : "bsiscout-9.0.0.039",
  "attribute" : "y-emailAddressValid",
  "fieldType" : "Boolean",
  "op" : "false",
  "operands" : [ ]
}
```

Combine with `DataModelAndConstraint` to chain multiple conditions.
