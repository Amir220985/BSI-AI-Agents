# BSI EIP InterfaceConfig JSON Reference

This document describes the complete structure of the `interfaces/{Name}-{uuid}.json` file — the main interface definition inside a BSI EIP ZIP export package. This is the file that defines every processor, every script, and the full configuration of one interface version.

---

## Top-Level Structure

```json
{
  "_type" : "interfaces.InterfaceConfig",
  "_typeVersion" : "interfaces-24.2.017",
  "changeDate" : "2026-06-23 09:19:43.951",
  "createDate" : "2026-06-23 09:19:43.951",
  "gid" : "8e21cc76-b0d4-4a29-a041-e984c37ac69b",
  "groups" : [ ],
  "id" : "af8cb193-e289-48d9-a9b6-36e30941909c",
  "logLevel" : "warn",
  "name" : "IBAN validation",
  "notes" : null,
  "processors" : [ ... ],
  "projectId" : "4ebaedb9-6f31-408d-bd36-9e36f8b3a357",
  "published" : true,
  "recordingLevel" : "analytics",
  "responsible" : {
    "_type" : "start.Responsible",
    "_typeVersion" : "start-1.3.2",
    "userId" : "36317f78-6040-4648-936d-e8b66b394c0b"
  },
  "revision" : 1,
  "runtime" : "b",
  "status" : "live",
  "template" : false,
  "typeId" : "2512c737-a73b-4f78-9ae2-098ac6d291bd",
  "typeScripts" : [ ... ],
  "version" : 1
}
```

---

## Top-Level Field Reference

| Field | Type | Required | Default / Fixed | Notes |
|---|---|---|---|---|
| `_type` | string | yes | `"interfaces.InterfaceConfig"` | Always this value |
| `_typeVersion` | string | yes | `"interfaces-24.2.017"` | Current schema version |
| `id` | UUID | yes | generated | Unique per interface version (the InterfaceConfigId). Changes with each new version. |
| `gid` | UUID | yes | generated | Global ID, stable across versions (InterfaceConfigGid). Same across all versions of the same interface. |
| `name` | string | yes | — | Display name shown in the UI |
| `projectId` | UUID | yes | — | UUID of the project this interface belongs to (references `interfaces.Project`) |
| `typeId` | UUID | yes | see Interface Types | Identifies the interface type (e.g. Lambda) |
| `runtime` | enum | yes | `"b"` | `"a"` = legacy runtime, `"b"` = current runtime. Always use `"b"`. |
| `status` | enum | yes | `"live"` | Lifecycle status; see Status Values |
| `published` | boolean | yes | `true` | Whether this interface is visible in production |
| `revision` | number | yes | `1` | Release revision number (integer, starts at 1) |
| `version` | number | yes | `1` | Optimistic locking version counter (integer, starts at 1) |
| `logLevel` | enum | yes | `"warn"` | Logging verbosity; see Log Level Values |
| `recordingLevel` | enum | yes | `"analytics"` | Execution recording detail; see Recording Level Values |
| `template` | boolean | yes | `false` | Whether this is a reusable template. Normally `false`. |
| `notes` | string/null | no | `null` | Optional free-text description |
| `createDate` | timestamp | yes | — | Format: `"YYYY-MM-DD HH:MM:SS.mmm"` |
| `changeDate` | timestamp | yes | — | Format: `"YYYY-MM-DD HH:MM:SS.mmm"`. Equal to `createDate` for new configs. |
| `responsible` | object | yes | — | The responsible user; see Responsible Structure |
| `groups` | array | yes | `[]` | UI processor groups. Use empty array for ungrouped layouts. See Groups section. |
| `collections` | — | — | — | Collections are NOT in the interface JSON — they are separate files in `collections/`. See Collections section. |
| `processors` | array | yes | — | Array of ProcessorConfig objects; see Processors section |
| `typeScripts` | array | yes | — | Array of TypeScriptConfig objects; see TypeScripts section |

---

## Enum Values

### `status`

| Value | Meaning |
|---|---|
| `"draft"` | Work in progress, not yet published |
| `"published"` | Submitted for review / staging |
| `"live"` | Active in production |
| `"archived"` | Retired, no longer active |

Use `"live"` for newly generated configurations intended for immediate use.

### `logLevel`

| Value | Meaning |
|---|---|
| `"trace"` | Most verbose |
| `"debug"` | Debug messages |
| `"info"` | Informational |
| `"warn"` | Warnings only (recommended default) |
| `"error"` | Errors only |
| `"fatal"` | Fatal errors only |

### `recordingLevel`

| Value | Meaning |
|---|---|
| `"none"` | No recording |
| `"basic"` | Basic execution metadata |
| `"analytics"` | Full analytics (recommended default) |
| `"extended"` | Extended detail including payloads |

---

## Interface Types (`typeId`)

| Interface Type | `typeId` UUID | Description |
|---|---|---|
| Lambda | `"2512c737-a73b-4f78-9ae2-098ac6d291bd"` | Callable lambda with signature (input/output) |
| Ad-Hoc | `"f72f9f76-fb2d-4579-b397-471b2ed4c4e3"` | Scheduled batch interface, no signature |
| Input | `"ce4bb086-02d6-4cee-9509-7b0dadaa6654"` | Trigger-based import interface, no signature |

**Lambda:** Standard interface type for on-demand calls. Has a signature with defined inputs/outputs. Entry point is a CRM Lambda processor.

**Ad-Hoc:** Scheduled interface for batch operations. Has no signature or direct call mechanism. Entry point is a Temporal Trigger. Used for nightly batch updates (e.g., CRM record enrichment).

**Input:** Import-oriented interface. Has no signature. Entry points are Temporal Trigger and/or Manual Trigger. Used for CSV imports, data ingestion pipelines. Has no `signature` in the Lambda processor — instead uses the trigger chain directly.

---

## Responsible Structure

```json
{
  "_type" : "start.Responsible",
  "_typeVersion" : "start-1.3.2",
  "userId" : "36317f78-6040-4648-936d-e8b66b394c0b"
}
```

The `userId` `36317f78-6040-4648-936d-e8b66b394c0b` is the fixed UUID for the system administrator in the target EIP installation. Use this value for all generated configurations.

---

## Processors

The `processors` array contains one `ProcessorConfig` object per processing step in the interface.

### ProcessorConfig Structure

```json
{
  "_type" : "interfaces.ProcessorConfig",
  "_typeVersion" : "interfaces-22.0.1004",
  "id" : "{processor-uuid}",
  "gid" : "{processor-gid-uuid}",
  "typeId" : "{processor-type-uuid}",
  "scriptIdentifier" : "myProcessor",
  "notes" : null,
  "groupId" : null,
  "customConfig" : { ... },
  "position" : {
    "_type" : "interfaces.Point",
    "_typeVersion" : "interfaces-22.0.0",
    "x" : 2,
    "y" : 2
  },
  "outlets" : [ ... ]
}
```

### ProcessorConfig Field Reference

| Field | Type | Notes |
|---|---|---|
| `_type` | string | Always `"interfaces.ProcessorConfig"` |
| `_typeVersion` | string | Always `"interfaces-22.0.1004"` |
| `id` | UUID | Unique instance UUID for this processor within the interface. Generated fresh per configuration. |
| `gid` | UUID | Global UUID, stable across imports. Generated fresh per configuration. |
| `typeId` | UUID | Identifies the processor type. See the processor-types-catalog.md for all known type UUIDs. |
| `scriptIdentifier` | string | Unique name within the interface. Used in TypeScript scripts to reference this processor's input/output (e.g. `invocation.processors.myProcessor.body`). Use camelCase. |
| `notes` | string/null | Optional documentation for this processor step. Typically `null`. |
| `groupId` | UUID/null | References a UI group. Typically `null` when `groups` is empty. |
| `customConfig` | object | Processor-specific configuration. Structure depends on `typeId`. See Custom Config section. |
| `position` | object | UI canvas position. See Position section. |
| `outlets` | array | Array of OutletConfig objects. See Outlets section. |

### Position (`interfaces.Point`)

```json
{
  "_type" : "interfaces.Point",
  "_typeVersion" : "interfaces-22.0.0",
  "x" : 2,
  "y" : 2
}
```

The canvas uses a grid coordinate system. Typical layout conventions:

- First processor starts at `x: 2, y: 2`
- Each subsequent processor in the same row increments `x` by 6 (e.g. x = 2, 8, 14, 20...)
- Branching paths use different `y` values

### Outlets (`interfaces.OutletConfig`)

Outlets define the output connections from a processor. Each outlet corresponds to a possible output path (e.g. success, error, specific branches).

```json
{
  "_type" : "interfaces.OutletConfig",
  "_typeVersion" : "interfaces-22.0.1006",
  "id" : "{outlet-uuid}",
  "gid" : "{outlet-gid-uuid}",
  "processorId" : "{target-processor-uuid}",
  "outletId" : "default"
}
```

| Field | Notes |
|---|---|
| `id` | Generated UUID for this outlet connection |
| `gid` | Generated global UUID for this outlet |
| `processorId` | UUID of the processor this outlet connects to (the downstream processor's `id`) |
| `outletId` | Which outlet of the current processor. `"default"` for single-output processors. May be `"true"` / `"false"` for condition branches, or a named branch for routers. |

---

## Custom Configs by Processor Type

The `customConfig` object structure depends on which processor type is used. Common processor types and their configs:

### TypeScript Processor

`typeId`: see processor-types-catalog.md for the TypeScript processor UUID.

```json
{
  "_type" : "interfaces.TypeScriptProcessorConfig",
  "_typeVersion" : "interfaces-23.2.018"
}
```

TypeScript processors have minimal config — the actual logic lives in the `typeScripts` array (linked via `processorId`).

### CRM Lambda Processor

`typeId`: see processor-types-catalog.md for the CRM Lambda processor UUID.

```json
{
  "_type" : "interfaces.CrmLambdaProcessorConfig",
  "_typeVersion" : "interfaces-23.2.019",
  "lambdaId" : "{lambda-interface-gid}",
  "interfaceId" : "{lambda-interface-id}"
}
```

Calls another EIP interface (lambda) from within this interface.

### Iteration Processor

`typeId`: see processor-types-catalog.md for the Iteration processor UUID.

```json
{
  "_type" : "interfaces.IterationProcessorConfig",
  "_typeVersion" : "interfaces-26.1.001",
  "iterationType" : "parallel"
}
```

`iterationType` values: `"parallel"`, `"sequential"`.

### REST Consumer Processor

`typeId`: see processor-types-catalog.md for the REST Consumer processor UUID.

```json
{
  "_type" : "interfaces.RestConsumerProcessorConfig",
  "_typeVersion" : "interfaces-24.2.008",
  "url" : "https://example.com/api/endpoint",
  "method" : "POST",
  "headers" : { },
  "timeout" : 30000
}
```

---

## TypeScripts

The `typeScripts` array contains all TypeScript source files for the interface. Scripts are linked to processors via `processorId`.

### TypeScriptConfig Structure

```json
{
  "_type" : "interfaces.TypeScriptConfig",
  "_typeVersion" : "interfaces-23.2.007",
  "processorId" : "{processor-uuid-or-null}",
  "scriptName" : "script.ts",
  "scriptKind" : "script",
  "readOnly" : false,
  "test" : false,
  "typeScript" : "// TypeScript source code here",
  "javaScript" : "// Compiled JavaScript here"
}
```

### TypeScriptConfig Field Reference

| Field | Type | Notes |
|---|---|---|
| `_type` | string | Always `"interfaces.TypeScriptConfig"` |
| `_typeVersion` | string | Always `"interfaces-23.2.007"` |
| `processorId` | UUID/null | UUID of the processor this script belongs to. `null` for interface-level scripts. |
| `scriptName` | string | Filename of the script. See Script Names below. |
| `scriptKind` | enum | Kind of script. See Script Kinds below. |
| `readOnly` | boolean | Whether the script can be edited in the UI. Always `false` for generated scripts. |
| `test` | boolean | Whether this is a test script. `true` only for test files. |
| `typeScript` | string | The TypeScript source code (uncompiled). |
| `javaScript` | string | The compiled JavaScript output. Both must be provided. |

### Script Kinds (`scriptKind`)

| Value | Purpose | Typical `scriptName` | Typical `processorId` |
|---|---|---|---|
| `"public-api"` | Type definitions visible to other processors | `"definition.d.ts"` | the processor's UUID |
| `"private-api"` | Internal type definitions (Self type) | `"definition.d.ts"` | the processor's UUID |
| `"script"` | Executable processor logic | `"script.ts"` | the processor's UUID |

Interface-level scripts (not tied to a specific processor) have `processorId: null`.

### Script Names Convention

| `scriptName` | Used for |
|---|---|
| `"script.ts"` | Main executable logic (`scriptKind: "script"`) |
| `"definition.d.ts"` | Type declarations (`scriptKind: "public-api"` or `"private-api"`) |

### How Processors and TypeScripts Are Linked

Each processor that contains TypeScript logic will have one or more entries in the `typeScripts` array with matching `processorId`. A typical TypeScript processor has two script entries:

1. `scriptKind: "public-api"`, `scriptName: "definition.d.ts"` — declares the output type of this processor so downstream processors can type-check their inputs.
2. `scriptKind: "script"`, `scriptName: "script.ts"` — the executable logic that runs when the processor is called.

**Example pairing:**

Processor with `id: "proc-uuid-abc"` and `scriptIdentifier: "ibanCheck"` gets:

```json
{
  "processorId" : "proc-uuid-abc",
  "scriptName" : "definition.d.ts",
  "scriptKind" : "public-api",
  "typeScript" : "export type Output = { isValid: boolean; message: string; };",
  "javaScript" : "..."
}
```

```json
{
  "processorId" : "proc-uuid-abc",
  "scriptName" : "script.ts",
  "scriptKind" : "script",
  "typeScript" : "const result = invocation.processors.ibanCheck.body;\nexport const output: Output = { isValid: result.valid, message: result.msg };",
  "javaScript" : "..."
}
```

### Accessing Processor Results in Scripts

Within a TypeScript script, upstream processor outputs are referenced via:

```typescript
invocation.processors.{scriptIdentifier}.body
```

Where `{scriptIdentifier}` matches the `scriptIdentifier` field of the upstream processor.

The interface's input (the lambda call payload) is typically accessed via:

```typescript
invocation.body
```

---

## Interface-Level TypeScript Scripts

Some scripts are attached to the interface itself rather than a processor. These have `processorId: null`.

Common uses:
- Declaring the global input/output signature of the interface
- Defining shared utility types used by multiple processors

---

## Complete Minimal Example

Below is the skeleton of a valid `interfaces/{Name}-{uuid}.json` with one TypeScript processor:

```json
{
  "_type" : "interfaces.InterfaceConfig",
  "_typeVersion" : "interfaces-24.2.017",
  "changeDate" : "2026-06-23 10:00:00.000",
  "createDate" : "2026-06-23 10:00:00.000",
  "gid" : "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  "groups" : [ ],
  "id" : "ffffffff-0000-1111-2222-333333333333",
  "logLevel" : "warn",
  "name" : "My Interface",
  "notes" : null,
  "processors" : [
    {
      "_type" : "interfaces.ProcessorConfig",
      "_typeVersion" : "interfaces-22.0.1004",
      "id" : "11111111-1111-1111-1111-111111111111",
      "gid" : "22222222-2222-2222-2222-222222222222",
      "typeId" : "{typescript-processor-type-uuid}",
      "scriptIdentifier" : "mainLogic",
      "notes" : null,
      "groupId" : null,
      "customConfig" : {
        "_type" : "interfaces.TypeScriptProcessorConfig",
        "_typeVersion" : "interfaces-23.2.018"
      },
      "position" : {
        "_type" : "interfaces.Point",
        "_typeVersion" : "interfaces-22.0.0",
        "x" : 2,
        "y" : 2
      },
      "outlets" : [ ]
    }
  ],
  "projectId" : "99999999-9999-9999-9999-999999999999",
  "published" : true,
  "recordingLevel" : "analytics",
  "responsible" : {
    "_type" : "start.Responsible",
    "_typeVersion" : "start-1.3.2",
    "userId" : "36317f78-6040-4648-936d-e8b66b394c0b"
  },
  "revision" : 1,
  "runtime" : "b",
  "status" : "live",
  "template" : false,
  "typeId" : "2512c737-a73b-4f78-9ae2-098ac6d291bd",
  "typeScripts" : [
    {
      "_type" : "interfaces.TypeScriptConfig",
      "_typeVersion" : "interfaces-23.2.007",
      "processorId" : "11111111-1111-1111-1111-111111111111",
      "scriptName" : "definition.d.ts",
      "scriptKind" : "public-api",
      "readOnly" : false,
      "test" : false,
      "typeScript" : "export type Output = { result: string; };",
      "javaScript" : "export {};"
    },
    {
      "_type" : "interfaces.TypeScriptConfig",
      "_typeVersion" : "interfaces-23.2.007",
      "processorId" : "11111111-1111-1111-1111-111111111111",
      "scriptName" : "script.ts",
      "scriptKind" : "script",
      "readOnly" : false,
      "test" : false,
      "typeScript" : "export const output: Output = { result: 'hello' };",
      "javaScript" : "exports.output = { result: 'hello' };"
    }
  ],
  "version" : 1
}
```

---

## Groups

Groups provide visual organization of processors in the EIP editor. They are declared in the `groups` array of the interface JSON.

```json
"groups": [
  {
    "_type": "interfaces.GroupConfig",
    "_typeVersion": "interfaces-22.0.0",
    "id": "{group-uuid}",
    "name": "Fetch",
    "color": "color3"
  },
  {
    "_type": "interfaces.GroupConfig",
    "_typeVersion": "interfaces-22.0.0",
    "id": "{group-uuid}",
    "name": "Process",
    "color": "color2"
  },
  {
    "_type": "interfaces.GroupConfig",
    "_typeVersion": "interfaces-22.0.0",
    "id": "{group-uuid}",
    "name": "Retry",
    "color": "color1"
  }
]
```

### GroupConfig Fields

| Field | Type | Notes |
|---|---|---|
| `_type` | string | Always `"interfaces.GroupConfig"` |
| `_typeVersion` | string | Always `"interfaces-22.0.0"` |
| `id` | UUID | Unique UUID for this group |
| `name` | string | Display name shown in the UI |
| `color` | enum | `"color1"`, `"color2"`, `"color3"` — EIP UI colors |

Processors join a group by setting `groupId` to the group's `id`. A processor with `groupId: null` belongs to no group.

For interfaces without logical grouping, set `"groups": []` and all processors have `groupId: null`.

---

## Collections

Collections are **not** declared inside the interface JSON. They are separate JSON files in the ZIP's `collections/` folder.

See `reference/collections-api.md` for the full Collections reference.

Collections appear in `index.json` as separate transfer items with `itemGroupId: "interfaces.collection"`.

The `groups` array in the interface JSON has nothing to do with collections — collections are a ZIP-level artifact.

---

## Key Constraints and Rules

1. **UUIDs**: Every `id` and `gid` must be a freshly generated UUID v4. Never reuse UUIDs between processors within the same interface.
2. **`scriptIdentifier` uniqueness**: Each processor's `scriptIdentifier` must be unique within the interface. It is used as the JavaScript property name in `invocation.processors.*`.
3. **TypeScript/JavaScript pairing**: Every `TypeScriptConfig` must have both `typeScript` and `javaScript` populated. The `javaScript` field contains the compiled output of the `typeScript` source.
4. **`processorId` consistency**: Each `TypeScriptConfig.processorId` must exactly match the `id` (not `gid`) of the corresponding processor.
5. **`typeVersions` in index.json**: Only include `typeVersions` entries for processor config types (`interfaces.*ProcessorConfig`) that actually appear in this interface's data file.
6. **Position layout**: Ensure no two processors share the same `(x, y)` coordinates. The grid x-step of 6 between processors prevents visual overlap in the UI.
7. **`version` field**: Always `1` for newly generated interfaces. This is an optimistic locking counter managed by the server after first import.
