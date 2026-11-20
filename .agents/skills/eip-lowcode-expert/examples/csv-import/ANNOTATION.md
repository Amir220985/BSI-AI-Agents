# CSV Import Example — Annotated Walkthrough

This example demonstrates a complete CSV import pipeline in BSI EIP with three key features:
- **CSV reading** via the dedicated CSV Processor
- **Collections-based state management** (change detection + retry tracking)
- **Multi-outlet routing** via `outletScriptIds` in TypeScript processor config

**Source:** `_source.zip` (exported 2026-06-23, EIP version 26.1.8)  
**Interface type:** Input (`ce4bb086-02d6-4cee-9509-7b0dadaa6654`) — NOT Lambda  
**Interface name:** Import CSV  
**Interface id:** `634cc4c0-5468-408e-a0b0-523841f750b8`  
**Interface gid:** `1ed9a729-fd0c-4f64-aa0a-9bffeb7f3ea8`

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FETCH (color3)                                                              │
│                                                                             │
│  [Temporal Trigger] → [simulateFetch TS] → [csv CSV] → [iterateFetch Iter] │
│                                                            │                │
│                                               [prepareDataFetch TS]         │
└──────────────────────────────────────────────────│──────────────────────────┘
                                                   │
┌──────────────────────────────────────────────────▼──────────────────────────┐
│ PROCESS (color2)                                                             │
│                                                                             │
│  [validateAndMap TS] ──── "Daten mutieren" ────→ [mutation CRM Mutation]    │
│       │                                               │                     │
│       │                                          ↙ Standard                 │
│       │                                    [computeHash TS]                 │
│       │                                                                     │
│       └──── "fehlendes Mapping" ──→ [storeForRetry TS]                     │
│       └──── "Kein Änderungen" → (null, stop)                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ RETRY (color1)                                                              │
│                                                                             │
│  [Manual Trigger] → [listCollection TS] → [iterateRetry Iter]              │
│                                                  │                         │
│                                          [prepareDataRetry TS] ────────────┘
│                                                  │                         │
│                                           → [validateAndMap TS] (shared)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Concepts Illustrated

| Concept | Where used |
|---|---|
| **Input Interface** (not Lambda) | Interface `typeId: ce4bb086-...` |
| **Groups** | Three colored groups: Fetch, Process, Retry |
| **CSV Processor** | `csv` processor reads CSV string from `simulateFetch` |
| **Collections** | `mappings`, `retries`, `processedRecords` |
| **Multi-outlet routing** | `validateAndMap` via `outletScriptIds` |
| **invocation.attributes** | `record` shared across all processors |
| **Hash-based deduplication** | `Hash.md5()` + `processedRecords` collection |
| **Retry pattern** | `retries` collection + `Manual Trigger` entry point |
| **ProcessorTypes** | `ProcessorTypes.dataMutation.createModifyTask()` |
| **Resolvers.crmEntities** | `Resolvers.crmEntities.resolveUser()` |

---

## Groups

Groups are visual containers for processors in the EIP editor. They are declared in the `groups` array of the interface JSON.

```json
"groups": [
  { "_type": "interfaces.GroupConfig", "_typeVersion": "interfaces-22.0.0",
    "id": "f9c1cd7e-6556-4be4-8136-883864d8d9a6", "name": "Retry", "color": "color1" },
  { "_type": "interfaces.GroupConfig", "_typeVersion": "interfaces-22.0.0",
    "id": "b78917ab-8a1d-4f05-822e-e2f7a92b309c", "name": "Process", "color": "color2" },
  { "_type": "interfaces.GroupConfig", "_typeVersion": "interfaces-22.0.0",
    "id": "bcec3578-a5f2-4c00-a9cd-9de77e764c28", "name": "Fetch", "color": "color3" }
]
```

Processors reference their group via `groupId`. A processor not assigned to any group has `groupId: null`.

---

## Collections

Collections are persistent key-value stores that survive between interface runs. They are defined separately from processors and accessed via `Collections.get('name')` in TypeScript.

### `mappings` — Urgency-to-Priority Mapping

**File:** `collections/mappings-c105aee0-f7ef-4715-906e-a3200c1d6aa3.json`

```json
{
  "_type": "interfaces.CollectionConfig",
  "_typeVersion": "interfaces-24.2.009",
  "id": "c105aee0-f7ef-4715-906e-a3200c1d6aa3",
  "identifier": "mappings",
  "type": "generic",
  "exportData": true,
  "typeScriptApi": "export type Key = string;\nexport type Value = 'high' | 'normal';\n"
}
```

- `exportData: true` — the collection's initial data is included in the ZIP export
- Contains: `"asap" → "high"`, `"dringend" → "high"`, `"rasch" → "low"`
- Used in `validateAndMap` to map urgency strings to priority levels

### `retries` — Failed Record Store

**File:** `collections/retries-6a679c2b-4acb-4eed-92c0-93f1961b8e22.json`

```json
{
  "id": "6a679c2b-4acb-4eed-92c0-93f1961b8e22",
  "identifier": "retries",
  "type": "generic",
  "exportData": false
}
```

- `exportData: false` — not exported; starts empty on fresh install
- Key: `record.id` (number)
- Value: `{ record, hash, issues, retryCount }`
- Max `retryCount` before exclusion: 5

### `processedRecords` — Successful Import Cache

**File:** `collections/processedRecords-263fc920-6c37-41bf-905a-31ce2e968cb2.json`

```json
{
  "id": "263fc920-6c37-41bf-905a-31ce2e968cb2",
  "identifier": "processedRecords",
  "type": "generic",
  "exportData": false
}
```

- `exportData: false` — runtime state only
- Key: `record.id` (number)
- Value: `{ hash: string, taskKey: string }`
- Used for both deduplication (hash comparison) and update detection (taskKey)

### CSV Preset

**File:** `presets/default-6e8adc7e-0df7-4fb1-861e-5ef82f08ffc6.json`

```json
{
  "_type": "interfaces.Preset",
  "_typeVersion": "interfaces-22.0.0",
  "id": "6e8adc7e-0df7-4fb1-861e-5ef82f08ffc6",
  "name": "default",
  "descriptorId": "01f03794-f5f3-4b44-93f7-ddde66869af8",
  "projectId": "d4fc2d45-4afe-4890-9de5-06c546299560",
  "value": {
    "_type": "interfaces.CsvPresetValue",
    "_typeVersion": "interfaces-22.0.1002",
    "delimiterCharacter": ";",
    "encoding": "UTF-8",
    "escapeCharacter": "\\",
    "allowDuplicateHeaderNames": false,
    "allowMissingHeaderNames": false,
    "ignoreEmptyLines": false,
    "ignoreHeaderRecord": false,
    "ignoreSurroundingSpaces": false,
    "ignoreTrailingDelimiter": false
  }
}
```

---

## Shared State: `invocation.attributes`

A key concept in this interface is the `invocation.attributes.record` object. It is written once per iteration (by either `prepareDataFetch` or `prepareDataRetry`) and read by all downstream processors.

**Type definition** (in `attributes.d.ts` at interface level):
```typescript
export interface Attributes {
  record: Record;
}

export interface Record {
  id: number;
  task: string;
  urgency: string;
  userName: string;
}
```

This is distinct from processor-level attributes (set via `self.withAttribute()`). Interface-level attributes persist across the entire processor chain for one run.

---

## Processors

### 1. `temporalTrigger` — Temporal Trigger (Fetch group)

**typeId:** `406211f6-7b91-4790-b492-feb3e7cac22c`  
**position:** (3, 3)

```json
"customConfig": {
  "_type": "interfaces.TriggerTemporalProcessorConfig",
  "_typeVersion": "interfaces-22.0.0",
  "temporalConfig": {
    "_type": "bsiscout.TemporalConfig",
    "_typeVersion": "bsiscout-22.0.0",
    "temporalMode": "periodicity",
    "temporalOption": "manual"
  }
}
```

Note: `temporalOption: "manual"` means "manually triggered" mode — no schedule configured. In production, replace with `"interval"` and add a `periodicityConfig`.

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `b3f5da65-ba2e-40ab-9983-a4e34544ff28` | `simulateFetch` |

---

### 2. `simulateFetch` — TypeScript (Fetch group)

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`  
**position:** (9, 3)  
**purpose:** Provides CSV data as a string (mocked). In production, this would load from S3, FTP, or an API.

**`script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  return `nr;betreff;dringlichkeit;benutzer
1;Getriebeprobleme;dringend;vicky.valetti
2;Ölflecken;dringend;andrea.adams
3;Upgrade-Möglichkeiten;KW 11;vicky.valetti
4;Upgrade-Möglichkeiten;rasch;vicky.valetti
5;Kunden werben Kunden Programm;asap;administrator`;
}
```

The return value is a semicolon-delimited CSV string with a header row. This becomes `invocation.processors.simulateFetch.result` in downstream processors.

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `csv` |

---

### 3. `csv` — CSV Processor (Fetch group) ★ NEW PROCESSOR TYPE

**typeId:** `1245030d-3b73-42fb-a7a8-3ed91b729303`  
**position:** (15, 3)

```json
"customConfig": {
  "_type": "interfaces.CsvProcessorCustomConfig",
  "_typeVersion": "interfaces-26.1.001",
  "operation": "read",
  "presetId": "6e8adc7e-0df7-4fb1-861e-5ef82f08ffc6"
}
```

The CSV Processor reads a CSV string from the upstream processor and outputs a `ListData<Record<string,string>>`. The column names come from the CSV header row.

**Data script** (`data.ts`) — tells the CSV processor where to find its input:
```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.simulateFetch.result;
}
```

**Auto-generated `api.d.ts`:**
```typescript
import { ListData } from '@eip/core';
export interface _Attributes {
  rows: ListData<Record<string, string>>;
}
```

The `rows` attribute holds one entry per CSV row (excluding header). Each entry is a `Record<string, string>` mapping column name to value.

**Output for example data:**
```
rows[0] = { nr: "1", betreff: "Getriebeprobleme", dringlichkeit: "dringend", benutzer: "vicky.valetti" }
rows[1] = { nr: "2", betreff: "Ölflecken", dringlichkeit: "dringend", benutzer: "andrea.adams" }
...
```

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `ed9dfe53-c48e-4551-b398-b1c2598726a8` | `iterateFetch` |

---

### 4. `iterateFetch` — Iteration (Fetch group)

**typeId:** `21c361ec-5dec-4f13-9767-442db1adb3a3`  
**position:** (21, 3)

```json
"customConfig": {
  "_type": "interfaces.IterationProcessorConfig",
  "_typeVersion": "interfaces-26.1.001",
  "aggregateResults": false,
  "aggregateAsListData": false,
  "chunkSize": 1,
  "workerThreads": 1
}
```

**Data script** (`data.ts`):
```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.csv.rows;
}
```

Iterates over each CSV row. `element` is `Flatten<ListData<Record<string,string>>>` = one row object.

**Outlets:**
| Name | Descriptor ID | ExecutionType | Target |
|---|---|---|---|
| Iteration | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` | scoped | `prepareDataFetch` |
| Abgeschlossen | `dd8f5806-3156-4697-97c0-dd069570f2e6` | default | null |

---

### 5. `prepareDataFetch` — TypeScript (Fetch group)

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`  
**position:** (27, 3)  
**purpose:** Maps the raw CSV row (strings) to the typed `Record` interface and stores it in `invocation.attributes`.

**`script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  const element = invocation.processors.iterateFetch.element;

  invocation.attributes.record = {
    id: parseInt(element.nr),
    task: element.betreff,
    urgency: element.dringlichkeit,
    userName: element.benutzer
  };
}
```

Note: `element.nr` is a string (all CSV values are strings). `parseInt()` converts to number.  
This processor does NOT return a value — its only job is to populate `invocation.attributes.record`.

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `validateAndMap` |

---

### 6. `validateAndMap` — TypeScript (Process group) ★ MULTI-OUTLET PATTERN

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`  
**position:** (38, 7)

This processor demonstrates **multi-outlet routing** via `outletScriptIds` in `customConfig`:

```json
"customConfig": {
  "_type": "interfaces.TypeScriptProcessorConfig",
  "_typeVersion": "interfaces-23.2.018",
  "outletScriptIds": {
    "unchanged": "bc585c90-eb0e-4950-bdee-1cbbd41d1ff4",
    "modify data": "95e72bc1-76b2-48bc-a518-511700deceed",
    "missing mapping": "436b236a-9e49-4cfd-9c4d-c4b5aedfb09d"
  }
}
```

The `outletScriptIds` maps outlet names (used in `self.withOutlet('...')`) to outlet UUIDs (the `id` of the corresponding `OutletConfig`). This allows TypeScript to dynamically route to named outlets.

**Outlets (4 total):**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | null (hidden, never used) |
| Daten mutieren | null | `mutation` |
| fehlendes Mapping | null | `storeForRetry` |
| Kein Änderungen | null | null (stop) |

Custom outlets (the non-Standard ones) have `descriptorId: null`.

**`attributes.d.ts`** (for `validateAndMap`):
```typescript
export interface Attributes {
  issues: string[];
}
```

**Auto-generated `definition.d.ts`:**
```typescript
import { Attributes } from './attributes';

export type Outlet = 'missing mapping' | 'modify data' | 'unchanged';

export interface Self {
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;
  withOutlet(outletId: Outlet): Self;
}
```

The `Outlet` union type is generated from the `outletScriptIds` keys. This gives TypeScript type safety for `self.withOutlet()`.

**`script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Collections } from '../../collections';
import { Hash } from '@eip/utils';
import { ProcessorTypes, Resolvers } from '@eip/core';

export function process(invocation: Invocation, self: Self) {
  const record = invocation.attributes.record;

  // check if data is known and unchanged
  const info = Collections.get('processedRecords').get(record.id);
  if (info && info.hash === Hash.md5(record)) {
    self.withOutlet('unchanged');
    return;
  }

  // collect issues
  const issues: string[] = [];

  // resolve prio
  const prio = Collections.get('mappings').get(record.urgency);
  if (!prio) {
    issues.push('unknown urgency [collection mappings]: \'' + record.urgency + '\'');
  }

  // resolver user
  let userId = Resolvers.crmEntities.resolveUser({ restrictions: { username: record.userName } });
  if (!userId) {
    issues.push('unknown user [customer suite]: \'' + record.userName + '\'');
  }

  if (issues.length > 0) {
    self
      .withAttribute('issues', issues)
      .withOutlet('missing mapping');
    return;
  }

  // otherwise, create mutation
  self.withOutlet('modify data');
  return ProcessorTypes.dataMutation.createModifyTask({
    id: info?.taskKey,
    highPriority: prio === 'high',
    subject: '[imported] ' + record.task,
    responsible: userId
  });
}
```

**Logic:**
1. Check if the record hash matches the stored hash → `'unchanged'` (skip)
2. Collect validation issues (unknown urgency or unknown user)
3. If issues → store in `self.withAttribute('issues', ...)` → `'missing mapping'`
4. Otherwise → return mutation object → `'modify data'`

Key APIs used:
- `Collections.get('processedRecords').get(record.id)` — lookup stored hash
- `Hash.md5(record)` — compute MD5 hash of the record object
- `Collections.get('mappings').get(record.urgency)` — lookup priority from mapping table
- `Resolvers.crmEntities.resolveUser({ restrictions: { username } })` — find user by username
- `ProcessorTypes.dataMutation.createModifyTask({...})` — create mutation object
  - `id`: the stored `taskKey` if updating existing, `undefined` if creating new
  - `highPriority: prio === 'high'` — boolean from mapping
  - `subject`: prefixed with `[imported]`
  - `responsible`: resolved user ID

---

### 7. `mutation` — CRM Mutation (Process group)

**typeId:** `cf9ee65c-a489-4250-b76a-7b1741868c0f`  
**position:** (44, 7)

```json
"customConfig": {
  "_type": "interfaces.CrmMutationProcessorConfig",
  "_typeVersion": "interfaces-24.2.010"
}
```

**`data.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function prepareMutations(invocation: Invocation, self: Self) {
  self.withMutations(invocation.processors.validateAndMap.result);
}
```

The mutation object was created by `validateAndMap` and is passed directly to `self.withMutations()`.

Note: In this example, the mutation uses `ProcessorTypes.dataMutation.createModifyTask()` (not `Mutations.create()`). This is an alternative API for task-specific mutations.

**Outlets:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `6c0f1af6-2051-4fd5-947b-398c59418229` | `computeHash` |
| Fehler | `f3aac37d-ce3b-45d0-8c52-b157854d2e8f` | `computeHash` |

Both Standard and Fehler route to `computeHash` — the hash computation happens regardless of success or failure, because `computeHash` checks the status internally.

---

### 8. `computeHash` — TypeScript (Process group)

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`  
**position:** (50, 7)  
**purpose:** If mutation succeeded, store record hash and CRM key in `processedRecords`. Also remove from retries.

**`script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Codes } from '@eip/crm-core';
import { Hash } from '@eip/utils';
import { Collections } from '../../collections';

export function process(invocation: Invocation, self: Self) {
  const resp = invocation.processors.mutation.response;

  if (resp.mutationResults[0].status !== Codes.DataMutationStatus.Ok) {
    return;
  }

  const todo = invocation.attributes.record;

  // store hash
  Collections.get('processedRecords').putImmediately(todo.id, {
    hash: Hash.md5(todo),
    taskKey: resp.mutationResults[0].affectedItemKey
  });

  // remove potential retry
  Collections.get('retries').removeImmediately(todo.id);
}
```

**Key patterns:**
- `invocation.processors.mutation.response` — access CRM mutation response
- `resp.mutationResults[0].status` — check against `Codes.DataMutationStatus.Ok`
- `resp.mutationResults[0].affectedItemKey` — the CRM key of the created/updated record
- `Collections.get(...).putImmediately(key, value)` — immediately persist to collection
- `Collections.get(...).removeImmediately(key)` — remove from another collection

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | null |

---

### 9. `storeForRetry` — TypeScript (Process group)

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`  
**position:** (44, 12)  
**purpose:** Stores failed records in the `retries` collection with retry counter.

**`script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Collections } from '../../collections';
import { Hash } from '@eip/utils';

export function process(invocation: Invocation, self: Self) {
  const record = invocation.attributes.record;
  const hash = Hash.md5(record);

  const retries = Collections.get('retries');
  const lastRetry = retries.get(invocation.attributes.record.id);

  const retryCount = (lastRetry && lastRetry.hash === hash) ? lastRetry.retryCount + 1 : 0;

  retries.putImmediately(invocation.attributes.record.id, {
      record: invocation.attributes.record,
      hash: hash,
      issues: invocation.processors.validateAndMap.issues,
      retryCount: retryCount
    });
}
```

**Retry counter logic:**
- If the record was already in retries AND the hash is the same (same error, same data) → increment counter
- If the data changed or it's new → reset counter to 0

`invocation.processors.validateAndMap.issues` — accessing the custom attribute set by `self.withAttribute('issues', ...)` in `validateAndMap`.

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | null |

---

### 10. `manualTrigger` — Manual Trigger (Retry group) ★ NEW PROCESSOR TYPE

**typeId:** `b4447959-8495-4a20-83e1-e3e0384c5935`  
**position:** (3, 14)

```json
"customConfig": {
  "_type": "interfaces.TriggerManualProcessorConfig",
  "_typeVersion": "interfaces-22.0.0"
}
```

The Manual Trigger has no configuration — it is a start node that can be triggered manually from the EIP UI. It enables running the Retry path independently of the Fetch path.

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `d20e1c72-467d-4af8-9c19-0027cd18c901` | `listCollection` |

---

### 11. `listCollection` — TypeScript (Retry group)

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`  
**position:** (9, 14)  
**purpose:** Queries the `retries` collection for records that haven't exceeded the retry limit.

**`script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Collections } from '../../collections';

export function process(invocation: Invocation, self: Self) {
  return Collections.get('retries')
    .list({
      maxResults: 100,
      valueRestrictions: [
        Collections.jsonPath()
          .property('retryCount')
          .condition(b => b.lt(b.filterPath(), 5))
      ]
    })
    .map(e => e.value.record);
}
```

**`Collections.get().list({...})` API:**
- `maxResults`: maximum number of entries to return
- `valueRestrictions`: array of `jsonPath()` filter conditions
- `Collections.jsonPath().property('retryCount')` — navigate to the `retryCount` field in the stored value
- `.condition(b => b.lt(b.filterPath(), 5))` — filter: `retryCount < 5`
- `e.value.record` — extract just the `record` object from each entry

The return value is `Record[]` — an array of records ready for re-processing.

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `iterateRetry` |

---

### 12. `iterateRetry` — Iteration (Retry group)

**typeId:** `21c361ec-5dec-4f13-9767-442db1adb3a3`  
**position:** (21, 14)

Same configuration as `iterateFetch`. Data script:
```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.listCollection.result;
}
```

**Outlets:**
| Name | Descriptor ID | ExecutionType | Target |
|---|---|---|---|
| Iteration | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` | scoped | `prepareDataRetry` |
| Abgeschlossen | `dd8f5806-3156-4697-97c0-dd069570f2e6` | default | null |

---

### 13. `prepareDataRetry` — TypeScript (Retry group)

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`  
**position:** (27, 14)  
**purpose:** Restores `invocation.attributes.record` from the retry record — then routes to `validateAndMap` (same processor as in Fetch path).

**`script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  invocation.attributes.record = invocation.processors.iterateRetry.element;
}
```

This is the key to the retry pattern: the `element` here is already a `Record` object (from `listCollection`'s `.map(e => e.value.record)`), so we just assign it directly.

**Outlet:**
| Name | Descriptor ID | Target |
|---|---|---|
| Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `validateAndMap` |

---

## Data Flow Diagram

```
Fetch path:
  simulateFetch → (CSV string) → csv.rows → iterateFetch.element
  → prepareDataFetch sets invocation.attributes.record
  → validateAndMap reads invocation.attributes.record
    ├─ "unchanged": stop (no change detected)
    ├─ "modify data": → mutation → computeHash
    │                               └─ writes to processedRecords
    │                               └─ removes from retries
    └─ "missing mapping": → storeForRetry
                              └─ writes to retries (with counter)

Retry path:
  manualTrigger → listCollection (retries where retryCount < 5)
  → iterateRetry.element → prepareDataRetry sets invocation.attributes.record
  → validateAndMap (same processor!) → ... (same logic as fetch path)
```

---

## Adaptation Guide

To adapt this interface for a real CSV import:

### 1. Replace `simulateFetch` with real data loading
```typescript
// Load from S3:
// return S3.getObject(bucket, key).body;
// or from a REST Consumer in the Fetch chain
```

### 2. Adapt the CSV column mapping in `prepareDataFetch`
```typescript
invocation.attributes.record = {
  id: parseInt(element.externalId),
  // map CSV column names to your record fields
};
```

### 3. Update the `mappings` collection with your actual mappings
- Add entries via the EIP UI after import, or in the collection resource file

### 4. Update the mutation call in `validateAndMap`
```typescript
return ProcessorTypes.dataMutation.createModifyTask({
  // adapt fields to your use case
});
// or use Mutations.create() for other entity types:
return Mutations.create('CrmContactCreate', { firstName, lastName });
```

### 5. Adjust the Temporal Trigger schedule
- Set `temporalMode: "periodicity"` and add `periodicityConfig`
- Set `hour` and `minute` for the desired run time
- Set `interval: 1` for daily runs

### 6. Consider the retry limit
- Currently 5 retries: `b.lt(b.filterPath(), 5)` — adjust as needed
- Consider adding alerting when `retryCount >= 5` (records with exhausted retries)

---

## Post-Import Checklist

After importing this ZIP into BSI EIP:

1. **Configure the Temporal Trigger** — set the desired schedule
2. **Populate the `mappings` collection** — add urgency → priority mappings
3. **Verify `Resolvers.crmEntities.resolveUser`** — usernames must match BSI CRM users
4. **Test manually** — use the Manual Trigger on the Fetch group first
5. **Test the Retry path** — trigger the Manual Trigger in the Retry group
6. **Adapt `simulateFetch`** — replace mock data with real data source

---

## UUID Reference

### Processor IDs

| scriptIdentifier | id | gid |
|---|---|---|
| temporalTrigger | `61bb73de-3432-4926-969e-5f9fa68ae0af` | `b5fc3ff8-c967-4ea0-aed1-26dcb1e6392b` |
| simulateFetch | `94688555-235b-423f-9709-39fd38ceaaba` | `a1cdc940-4491-432a-851c-af2259ee534a` |
| csv | `89cd7e4e-2e0c-416d-b010-f68e011260dd` | `2cf0b060-9d17-4090-a328-b09ff3a8cc12` |
| iterateFetch | `514d2017-f891-4656-96cb-02e230cee48c` | `6df6ea9e-c677-4a47-b079-0a7c8f4d57e6` |
| prepareDataFetch | `0844262d-87e2-4c15-a612-e5707d52e3d8` | `cc493c9a-c805-4796-b8b7-633a560e3a5d` |
| validateAndMap | `9b8571e9-a48f-41e8-bc45-d4b49bb6e023` | `e36d528f-a901-4062-a96d-26d6ae8be7fc` |
| mutation | `01b728d3-f0e8-4a79-a8d0-1adc33fb5cf3` | `bfb9dffe-0ed3-4792-8e5a-dc8d023675d2` |
| computeHash | `cbdb2baa-7779-40ff-ab01-9ed56215101d` | `a9c591fa-2545-4069-bec6-fe5ca2ec2ff0` |
| storeForRetry | `a45e3a4c-25ca-4a8c-8981-632d8e6d7d63` | `e421a558-fd3e-4d1b-a27b-22997da5a847` |
| manualTrigger | `5bb5412b-b824-4a2e-a558-3e76d8cb8b13` | `5e74e8df-8029-42d4-817d-3e56ae692ec1` |
| listCollection | `ee2e70e3-f155-4b3e-8694-d3df5020f9c5` | `3f01ca01-76fd-4fa8-b859-673300b98f75` |
| iterateRetry | `f7d39247-35a4-4435-9f24-122c822ac1ee` | `effe8fd6-4213-4747-9ecc-c89d5fefc750` |
| prepareDataRetry | `e99d05be-436c-4e85-971b-07ee0662536c` | `28700c00-82d8-459e-8abb-fbc0f94431fe` |

### Outlet IDs used in this interface (do not reuse — for reference only)

| Processor | Outlet name | Outlet id | descriptorId |
|---|---|---|---|
| temporalTrigger | Standard | `6b748726-9d9f-4be7-b1ce-cc8c63cba4da` | `b3f5da65-ba2e-40ab-9983-a4e34544ff28` |
| simulateFetch | Standard | `dd515636-f953-4441-943e-d121ab320d3a` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| csv | Standard | `07b071b5-5767-4716-8f91-a146d3a66cc4` | `ed9dfe53-c48e-4551-b398-b1c2598726a8` |
| iterateFetch | Iteration | `403173ea-673d-4764-9b20-4d0f744029d5` | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` |
| iterateFetch | Abgeschlossen | `1f6b98f3-9f9f-4982-8f59-09e2eb3435e8` | `dd8f5806-3156-4697-97c0-dd069570f2e6` |
| prepareDataFetch | Standard | `e8f3bc3e-cabd-48bc-b69f-06c7f15e9fc0` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| validateAndMap | Standard (hidden) | `4130f2dd-ef35-4bd5-816d-130a273066b2` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| validateAndMap | Daten mutieren | `95e72bc1-76b2-48bc-a518-511700deceed` | null |
| validateAndMap | fehlendes Mapping | `436b236a-9e49-4cfd-9c4d-c4b5aedfb09d` | null |
| validateAndMap | Kein Änderungen | `bc585c90-eb0e-4950-bdee-1cbbd41d1ff4` | null |
| mutation | Standard | `1ac416b3-421a-4f1c-99c5-b7395dd122b0` | `6c0f1af6-2051-4fd5-947b-398c59418229` |
| mutation | Fehler | `c22d94f2-2778-49bd-aec7-ba24065a3150` | `f3aac37d-ce3b-45d0-8c52-b157854d2e8f` |
| computeHash | Standard | `5b5af630-e14e-4e42-86c0-54234f4ea1d7` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| storeForRetry | Standard | `651fcbbc-7e13-4ea9-8fb7-4438ce13e852` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| manualTrigger | Standard | `48f85b95-b0e7-48ef-815d-2b102defe679` | `d20e1c72-467d-4af8-9c19-0027cd18c901` |
| listCollection | Standard | `a9a05e80-4889-4276-b23d-fcf541ffc78b` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| iterateRetry | Iteration | `ca6caa56-40a4-43d7-a1b7-3b0ff1b08ff8` | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` |
| iterateRetry | Abgeschlossen | `5b94cbb3-9caf-48f7-a77b-705e431bd50e` | `dd8f5806-3156-4697-97c0-dd069570f2e6` |
| prepareDataRetry | Standard | `401a3fba-a064-4b84-a289-e0eee7bc3e00` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
