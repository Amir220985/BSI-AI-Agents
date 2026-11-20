# Pattern: CSV Import with Collections, Change Detection, and Retry

**Use when:** You need to periodically import data from a CSV source (S3, FTP, API) into BSI CRM, with:
- Change detection to skip unchanged records (idempotent imports)
- Validation and mapping of source values to CRM values
- Automatic retry of failed records (up to N attempts)

**Interface type:** Input (`ce4bb086-02d6-4cee-9509-7b0dadaa6654`) — NOT Lambda  
**Reference example:** `examples/csv-import/ANNOTATION.md`

---

## Processor Chain

### Fetch Path (triggered periodically)

```
Temporal Trigger
  → simulateFetch (TypeScript) — provides CSV string
  → csv (CSV Processor) — parses CSV into rows
  → iterateFetch (Iteration) — iterates rows
    → prepareData (TypeScript) — sets invocation.attributes.record
    → validateAndMap (TypeScript, multi-outlet)
        → "Daten mutieren" → mutation (CRM Mutation) → computeHash (TypeScript)
        → "fehlendes Mapping" → storeForRetry (TypeScript)
        → "Kein Änderungen" → (stop)
```

### Retry Path (triggered manually)

```
Manual Trigger
  → listCollection (TypeScript) — lists retry candidates
  → iterateRetry (Iteration) — iterates failed records
    → prepareDataRetry (TypeScript) — sets invocation.attributes.record
    → validateAndMap (TypeScript) — SAME processor as Fetch path!
```

---

## Required Collections

Declare these in the ZIP's `collections/` folder:

| identifier | exportData | Purpose |
|---|---|---|
| `mappings` | `true` | External value → internal value (e.g., urgency → priority) |
| `processedRecords` | `false` | Hash + CRM key per successfully imported record |
| `retries` | `false` | Failed records with retry counter |

---

## Processor Configurations

### Temporal Trigger

```json
{
  "_type": "interfaces.TriggerTemporalProcessorConfig",
  "_typeVersion": "interfaces-22.0.0",
  "temporalConfig": {
    "_type": "bsiscout.TemporalConfig",
    "_typeVersion": "bsiscout-22.0.0",
    "temporalMode": "periodicity",
    "temporalOption": "interval",
    "periodicityConfig": {
      "_type": "bsiscout.PeriodicityConfig",
      "_typeVersion": "bsiscout-22.0.0",
      "periodicityType": "daily",
      "temporalOption": "interval",
      "hour": 2,
      "minute": 0,
      "interval": 1
    }
  }
}
```

Outlet: `Standard` → `simulateFetch` (descriptor: `b3f5da65-ba2e-40ab-9983-a4e34544ff28`)

### CSV Processor

```json
{
  "_type": "interfaces.CsvProcessorCustomConfig",
  "_typeVersion": "interfaces-26.1.001",
  "operation": "read",
  "presetId": "{preset-uuid}"
}
```

Requires a Preset file in `presets/` with CSV format settings (delimiter, encoding, etc.).  
Outlet: `Standard` → `iterateFetch` (descriptor: `ed9dfe53-c48e-4551-b398-b1c2598726a8`)

### Iteration Processor (both iterateFetch and iterateRetry)

```json
{
  "_type": "interfaces.IterationProcessorConfig",
  "_typeVersion": "interfaces-26.1.001",
  "aggregateResults": false,
  "aggregateAsListData": false,
  "chunkSize": 1,
  "workerThreads": 1
}
```

### Manual Trigger

```json
{
  "_type": "interfaces.TriggerManualProcessorConfig",
  "_typeVersion": "interfaces-22.0.0"
}
```

Outlet: `Standard` → `listCollection` (descriptor: `d20e1c72-467d-4af8-9c19-0027cd18c901`)

### TypeScript validateAndMap — Multi-Outlet Config

```json
{
  "_type": "interfaces.TypeScriptProcessorConfig",
  "_typeVersion": "interfaces-23.2.018",
  "outletScriptIds": {
    "unchanged": "{outlet-id-for-unchanged}",
    "modify data": "{outlet-id-for-modify}",
    "missing mapping": "{outlet-id-for-missing}"
  }
}
```

Outlets (use `descriptorId: null` for all custom outlets):
```json
[
  { "name": "Standard", "descriptorId": "c4b09fff-0dae-4726-bdeb-12fd01ddc2da", "presentation": "hidden", "targetProcessorId": null },
  { "name": "Daten mutieren", "descriptorId": null, "presentation": "default", "targetProcessorId": "{mutation-id}" },
  { "name": "fehlendes Mapping", "descriptorId": null, "presentation": "default", "targetProcessorId": "{storeForRetry-id}" },
  { "name": "Kein Änderungen", "descriptorId": null, "presentation": "default", "targetProcessorId": null }
]
```

The outlet `id`s must match the values in `outletScriptIds` exactly.

---

## Key TypeScript Scripts

### `simulateFetch/script.ts` — provide CSV data

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';

export function process(invocation: Invocation, self: Self) {
  // In production: load from S3, FTP, REST API, etc.
  return `id;field1;field2\n1;value1a;value2a\n2;value1b;value2b`;
}
```

### `csv/data.ts` — feed CSV string to parser

```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.simulateFetch.result;
}
```

### `iterateFetch/data.ts` — iterate CSV rows

```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.csv.rows;
}
```

### `prepareDataFetch/script.ts` — map CSV row to record

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';

export function process(invocation: Invocation, self: Self) {
  const element = invocation.processors.iterateFetch.element;
  invocation.attributes.record = {
    id: parseInt(element.id),
    field1: element.field1,
    field2: element.field2
  };
}
```

### `validateAndMap/script.ts` — validate, map, detect changes

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Collections } from '../../collections';
import { Hash } from '@eip/utils';
import { ProcessorTypes, Resolvers } from '@eip/core';

export function process(invocation: Invocation, self: Self) {
  const record = invocation.attributes.record;

  // Change detection
  const cached = Collections.get('processedRecords').get(record.id);
  if (cached && cached.hash === Hash.md5(record)) {
    self.withOutlet('unchanged');
    return;
  }

  const issues: string[] = [];

  // Mapping via collection
  const mappedValue = Collections.get('mappings').get(record.field1);
  if (!mappedValue) {
    issues.push('Unknown value: ' + record.field1);
  }

  if (issues.length > 0) {
    self.withAttribute('issues', issues).withOutlet('missing mapping');
    return;
  }

  self.withOutlet('modify data');
  return ProcessorTypes.dataMutation.createModifyTask({
    id: cached?.taskKey,       // undefined = create, string = update
    highPriority: mappedValue === 'high',
    subject: record.field2,
    responsible: Resolvers.crmEntities.resolveUser({ restrictions: { username: 'admin' } })
  });
}
```

### `mutation/data.ts` — pass mutation to CRM

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';

export function prepareMutations(invocation: Invocation, self: Self) {
  self.withMutations(invocation.processors.validateAndMap.result);
}
```

### `computeHash/script.ts` — store success state

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Codes } from '@eip/crm-core';
import { Hash } from '@eip/utils';
import { Collections } from '../../collections';

export function process(invocation: Invocation, self: Self) {
  const resp = invocation.processors.mutation.response;
  if (resp.mutationResults[0].status !== Codes.DataMutationStatus.Ok) return;

  const record = invocation.attributes.record;
  Collections.get('processedRecords').putImmediately(record.id, {
    hash: Hash.md5(record),
    taskKey: resp.mutationResults[0].affectedItemKey
  });
  Collections.get('retries').removeImmediately(record.id);
}
```

### `storeForRetry/script.ts` — store failure with counter

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Collections } from '../../collections';
import { Hash } from '@eip/utils';

export function process(invocation: Invocation, self: Self) {
  const record = invocation.attributes.record;
  const hash = Hash.md5(record);
  const retries = Collections.get('retries');
  const last = retries.get(record.id);
  const count = (last && last.hash === hash) ? last.retryCount + 1 : 0;
  retries.putImmediately(record.id, {
    record,
    hash,
    issues: invocation.processors.validateAndMap.issues,
    retryCount: count
  });
}
```

### `listCollection/script.ts` — query retry candidates

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
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

### `iterateRetry/data.ts` — iterate retry queue

```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.listCollection.result;
}
```

### `prepareDataRetry/script.ts` — restore record for reprocessing

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';

export function process(invocation: Invocation, self: Self) {
  invocation.attributes.record = invocation.processors.iterateRetry.element;
}
```

---

## Interface-Level `attributes.d.ts`

```typescript
export interface Attributes {
  record: Record;
}

export interface Record {
  id: number;
  field1: string;
  field2: string;
  // add your CSV column mappings here
}
```

---

## Outlet Descriptor IDs (Quick Reference)

| Processor type | Outlet | Descriptor ID |
|---|---|---|
| Temporal Trigger | Standard | `b3f5da65-ba2e-40ab-9983-a4e34544ff28` |
| Manual Trigger | Standard | `d20e1c72-467d-4af8-9c19-0027cd18c901` |
| CSV Processor | Standard | `ed9dfe53-c48e-4551-b398-b1c2598726a8` |
| Iteration | Iteration | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` |
| Iteration | Abgeschlossen | `dd8f5806-3156-4697-97c0-dd069570f2e6` |
| TypeScript | Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| CRM Mutation | Standard | `6c0f1af6-2051-4fd5-947b-398c59418229` |
| CRM Mutation | Fehler | `f3aac37d-ce3b-45d0-8c52-b157854d2e8f` |

---

## Pre-Generation Checklist

- [ ] Interface type is Input (`ce4bb086-02d6-4cee-9509-7b0dadaa6654`), NOT Lambda
- [ ] Three collections defined: `mappings` (exportData: true), `processedRecords` and `retries` (exportData: false)
- [ ] CSV Preset file created with correct delimiter, encoding
- [ ] `invocation.attributes.record` type defined in interface-level `attributes.d.ts`
- [ ] `validateAndMap` has correct `outletScriptIds` — outlet IDs must match exactly
- [ ] `mutation` CRM Mutation processor — verify mutation type and fields
- [ ] `computeHash` handles both Standard and Fehler paths from mutation
- [ ] Retry limit threshold matches business requirements (default: 5)
- [ ] Both Iteration processors (`iterateFetch`, `iterateRetry`) → `validateAndMap` (shared)
