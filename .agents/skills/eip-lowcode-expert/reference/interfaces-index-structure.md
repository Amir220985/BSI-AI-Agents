# Interfaces index.json — Structure and Pitfalls (BSI EIP 26.1.8)

## referencedItems

Every entry must be a complete `ConfigurationTransferReference` object — **not a naked UUID string**.

```json
"referencedItems" : [ {
  "_type" : "bsiscout.ConfigurationTransferReference",
  "_typeVersion" : "bsiscout-22.0.19",
  "id" : {
    "_type" : "bsiscout.IdConfigurationTransferId",
    "_typeVersion" : "bsiscout-22.0.0",
    "id" : "interfaces.ProcessorTypeId:<uuid>"
  }
} ]
```

## globalUniqueId for reference items

Items the package only references (but does not own) need a type prefix:

| Item type | globalUniqueId |
|-----------|----------------|
| Processor type | `"ProcessorType/<uuid>"` |
| Interface type | `"InterfaceType/<uuid>"` |
| Admin user | `"User/administrator"` |

Root items (e.g. the interface configuration itself) use a plain UUID as their `globalUniqueId`.

## Admin user item

```json
{
  "_type" : "bsiscout.ConfigurationTransferItem",
  "_typeVersion" : "bsiscout-22.0.0",
  "globalUniqueId" : "User/administrator",
  "id" : {
    "_type" : "start.ResponsibleConfigurationTransferId",
    "_typeVersion" : "start-1.3.2",
    "userId" : "36317f78-6040-4648-936d-e8b66b394c0b"
  },
  "root" : false,
  "transferType" : "reference"
}
```

## Project item ID type

```json
"id" : {
  "_type" : "bsiscout.IdConfigurationTransferId",
  "_typeVersion" : "bsiscout-22.0.0",
  "id" : "interfaces.ProjectId:<uuid>"
}
```

Not `interfaces.ProjectConfigId` — that is wrong.

## Project file structure

`_type: interfaces.Project` (not `interfaces.ProjectConfig`). `name` is a plain string (not `names: {und: ...}`):

```json
{
  "_type" : "interfaces.Project",
  "_typeVersion" : "interfaces-22.0.0",
  "cooldownTimeInMinutes" : null,
  "id" : "<uuid>",
  "name" : "MyProject",
  "notes" : null,
  "recipients" : [ ],
  "responsible" : {
    "_type" : "start.Responsible",
    "_typeVersion" : "start-1.3.2",
    "userId" : "36317f78-6040-4648-936d-e8b66b394c0b"
  }
}
```

## Common wrong vs. correct values

| Field | Wrong | Correct |
|-------|-------|---------|
| Project `_type` | `interfaces.ProjectConfig` | `interfaces.Project` |
| Project `name` field | `"names": {"und": "..."}` | `"name": "..."` |
| Project item ID type | `interfaces.ProjectConfigId` | `interfaces.ProjectId` |
| `referencedItems` entries | plain UUID string | `ConfigurationTransferReference` object |
