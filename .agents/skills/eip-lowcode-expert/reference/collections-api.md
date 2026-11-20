# BSI EIP Collections API Reference

Collections are **persistent, typed key-value stores** that survive between interface runs. Unlike `invocation.attributes` (which exist only for the duration of one run), collections retain their data across multiple executions and can be used to:

- Store state between scheduled runs (e.g., processed record hashes)
- Provide configurable mapping tables (e.g., urgency → priority)
- Track failed records with retry counters
- Cache CRM lookups for incremental processing

**Reference example:** `examples/csv-import/` — demonstrates all three collection use patterns.

---

## Collection Declaration in the Interface JSON

Collections are **not** declared inside the interface JSON file. They live in separate JSON files in the `collections/` folder of the ZIP and reference the project.

### Collection JSON format

```json
{
  "_type": "interfaces.CollectionConfig",
  "_typeVersion": "interfaces-24.2.009",
  "id": "{collection-uuid}",
  "identifier": "myCollection",
  "type": "generic",
  "exportData": false,
  "grouping": null,
  "notes": "Optional description of this collection's purpose.",
  "projectId": "{project-uuid}",
  "typeScriptApi": "export type Key = string;\nexport type Value = MyValue;\n"
}
```

### CollectionConfig Field Reference

| Field | Type | Notes |
|---|---|---|
| `_type` | string | Always `"interfaces.CollectionConfig"` |
| `_typeVersion` | string | Always `"interfaces-24.2.009"` |
| `id` | UUID | Unique ID for this collection definition |
| `identifier` | string | Name used in TypeScript: `Collections.get('identifier')` |
| `type` | enum | `"generic"` for all typical use cases |
| `exportData` | boolean | See below |
| `grouping` | string/null | Grouping key for the EIP UI; typically `null` |
| `notes` | string/null | Optional documentation |
| `projectId` | UUID | Must match the project UUID in `projects/` |
| `typeScriptApi` | string | TypeScript type declarations for key and value |

### `exportData` Flag

| `exportData` | Meaning |
|---|---|
| `true` | The collection's current data is included in the ZIP export. Use for pre-populated mapping tables that should be transferred together with the interface config. |
| `false` | Only the collection definition is exported — data is not included. Use for runtime state collections (retries, caches) that should start empty on a fresh install. |

---

## TypeScript API

### Import

```typescript
import { Collections } from '../../collections';
```

The import path is relative to the processor's script directory. From inside a processor's subdirectory (e.g., `validateAndMap/script.ts`), the path is `../../collections`.

### Core Methods

#### `Collections.get(identifier)`

Returns a collection handle for the given identifier string.

```typescript
const col = Collections.get('myCollection');
```

#### `.get(key): Value | undefined`

Retrieves one value by key. Returns `undefined` if not found.

```typescript
const prio = Collections.get('mappings').get(record.urgency);
if (!prio) {
  // key not found
}
```

#### `.putImmediately(key, value): void`

Writes a value immediately (not deferred). Data is persisted to the collection store synchronously.

```typescript
Collections.get('processedRecords').putImmediately(record.id, {
  hash: Hash.md5(record),
  taskKey: resp.mutationResults[0].affectedItemKey
});
```

#### `.removeImmediately(key): void`

Deletes an entry immediately by key.

```typescript
Collections.get('retries').removeImmediately(record.id);
```

#### `.list(options): Entry[]`

Lists entries with optional filtering and a result limit.

```typescript
const entries = Collections.get('retries').list({
  maxResults: 100,
  valueRestrictions: [
    Collections.jsonPath()
      .property('retryCount')
      .condition(b => b.lt(b.filterPath(), 5))
  ]
});
// entries is an array of { key, value } objects
entries.map(e => e.value.record);  // extract only the record field
```

**`list` options:**

| Option | Type | Description |
|---|---|---|
| `maxResults` | number | Maximum number of entries to return |
| `valueRestrictions` | array | Array of `jsonPath()` filter conditions |

**Entry structure:**
```typescript
interface Entry<K, V> {
  key: K;
  value: V;
}
```

---

## JSON Path Filtering

`Collections.jsonPath()` creates a filter condition for `.list()`.

### Basic pattern

```typescript
Collections.jsonPath()
  .property('fieldName')
  .condition(b => b.lt(b.filterPath(), threshold))
```

### `.property(name)`

Navigates into a property of the stored value object.

```typescript
Collections.jsonPath().property('retryCount')
// navigates to value.retryCount
```

### `.condition(builder => expr)`

Defines the filter condition. The builder `b` provides comparison methods.

| Builder method | Meaning |
|---|---|
| `b.lt(a, b)` | `a < b` |
| `b.gt(a, b)` | `a > b` |
| `b.eq(a, b)` | `a === b` |
| `b.ne(a, b)` | `a !== b` |
| `b.le(a, b)` | `a <= b` |
| `b.ge(a, b)` | `a >= b` |
| `b.filterPath()` | Reference to the value navigated to by `.property()` |

**Example:** Filter to `retryCount < 5`:
```typescript
Collections.jsonPath()
  .property('retryCount')
  .condition(b => b.lt(b.filterPath(), 5))
```

---

## Common Usage Patterns

### Pattern 1: Mapping Table (exportData: true)

Used for static or semi-static configuration data that should be bundled with the interface.

```typescript
// TypeScript API declaration in collection JSON:
// export type Key = string;
// export type Value = 'high' | 'normal' | 'low';

// Read:
const priority = Collections.get('mappings').get(record.urgency);
// priority is 'high' | 'normal' | 'low' | undefined
```

Data is initialized in the `resource-{uuid}` binary file bundled in the ZIP. Values can be managed in the EIP UI after import.

### Pattern 2: Runtime State Cache (exportData: false)

Used to remember what was processed across runs.

```typescript
// After successful processing:
Collections.get('processedRecords').putImmediately(record.id, {
  hash: Hash.md5(record),
  taskKey: crmKey
});

// Next run — check if unchanged:
const cached = Collections.get('processedRecords').get(record.id);
if (cached && cached.hash === Hash.md5(record)) {
  // skip — unchanged
}
```

### Pattern 3: Retry Queue (exportData: false)

Used to accumulate failed records and re-process them.

```typescript
// Store on failure (with counter):
const retries = Collections.get('retries');
const last = retries.get(record.id);
const count = (last && last.hash === hash) ? last.retryCount + 1 : 0;
retries.putImmediately(record.id, { record, hash, issues, retryCount: count });

// List for retry (only those under limit):
const toRetry = Collections.get('retries')
  .list({
    maxResults: 100,
    valueRestrictions: [
      Collections.jsonPath().property('retryCount').condition(b => b.lt(b.filterPath(), 5))
    ]
  })
  .map(e => e.value.record);

// Remove on success:
Collections.get('retries').removeImmediately(record.id);
```

---

## ZIP File Structure for Collections

When a collection has `exportData: true`, the ZIP contains two files:
- `collections/{identifier}-{uuid}.json` — the collection definition
- `collections/resource-{uuid}` — the binary data file (initial collection values)

When `exportData: false`, only the `.json` definition file is present.

**In `index.json`:** Collections appear as reference items with `itemGroupId: "interfaces.collection"` and `transferType: "full"` (or `"reference"` for cross-project references).

---

## Type Safety

The `typeScriptApi` field in the collection JSON declares TypeScript types for key and value:

```json
"typeScriptApi": "export type Key = string;\nexport type Value = 'high' | 'normal';\n"
```

These types are used for type-checking in the EIP TypeScript editor. When generating a new collection, define the types as precisely as possible.

Example for the retry collection:
```typescript
export type Key = number;
export interface Value {
  record: Record;
  hash: string;
  issues: string[];
  retryCount: number;
}
interface Record {
  id: number;
  task: string;
  urgency: string;
  userName: string;
}
```
