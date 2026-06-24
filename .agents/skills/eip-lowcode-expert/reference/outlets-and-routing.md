# Outlets and Routing Reference

## Overview

Processors in a BSI EIP interface connect to each other through **outlets**. Every processor has an `outlets` array defining where execution continues after the processor finishes. An outlet points to the next processor via `targetProcessorId`. When `targetProcessorId` is `null`, the pipeline ends at that outlet.

---

## OutletConfig Structure

Every element in the `outlets` array has this structure:

```json
{
  "_type" : "interfaces.OutletConfig",
  "_typeVersion" : "interfaces-22.0.1006",
  "id" : "{outlet-uuid}",
  "gid" : "{outlet-gid-uuid}",
  "descriptorId" : "{descriptor-uuid-or-null}",
  "name" : "Standard",
  "presentation" : "primary",
  "executionType" : "default",
  "targetProcessorId" : "{next-processor-uuid-or-null}",
  "connectorPoints" : [ ]
}
```

---

## Field Reference

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique ID — also used as outlet script ID in TypeScript processor's `outletScriptIds` |
| `gid` | UUID | Global UUID stable across imports |
| `descriptorId` | UUID or null | References a system outlet descriptor (for standard/fixed outlets); `null` for custom outlets in TypeScript processors |
| `name` | string | Display name shown in the UI |
| `presentation` | enum | Visual style: `"primary"` (bold), `"default"` (normal), `"hidden"` (not shown) |
| `executionType` | enum | `"default"` = runs inline; `"scoped"` = creates sub-execution scope (used for Lambda "Aufruf" and Iteration "Iteration") |
| `targetProcessorId` | UUID or null | ID of the next processor; `null` means end of pipeline |
| `connectorPoints` | array | Visual routing points in the UI canvas; always empty `[]` in generated configs |

### `presentation` Values

| Value | Effect |
|---|---|
| `"primary"` | Bold connector — used for the main success path (e.g., REST Consumer "Standard") |
| `"default"` | Normal connector — used for named paths (e.g., Lambda "Aufruf", custom TypeScript outlets) |
| `"hidden"` | Connector not shown in the UI — used for fallback/error outlets that are rarely connected (e.g., TypeScript "Standard", REST Consumer "Sonstige") |

### `executionType` Values

| Value | Effect |
|---|---|
| `"default"` | Normal inline execution — control flows directly to the target processor |
| `"scoped"` | Creates a sub-execution scope — used for Lambda "Aufruf" (each lambda invocation) and Iteration "Iteration" (each loop iteration) |

---

## Standard Outlet Patterns by Processor Type

### Lambda Processor

A Lambda processor always has **exactly two outlets**: "Aufruf" (the scoped call outlet) and "Abgeschlossen" (the completion outlet).

```json
[
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{uuid-1}",
    "gid": "{uuid-2}",
    "descriptorId": "78861a9e-e99c-47c7-913b-6bf685f5557b",
    "name": "Aufruf",
    "presentation": "default",
    "executionType": "scoped",
    "targetProcessorId": "{first-processing-step-id}",
    "connectorPoints": []
  },
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{uuid-3}",
    "gid": "{uuid-4}",
    "descriptorId": "738f1301-f558-40b5-bbfc-e869a5832156",
    "name": "Abgeschlossen",
    "presentation": "default",
    "executionType": "default",
    "targetProcessorId": null,
    "connectorPoints": []
  }
]
```

- The "Aufruf" outlet is `executionType: "scoped"` — it runs once per lambda invocation.
- The "Abgeschlossen" outlet fires when the entire lambda call cycle completes; typically `targetProcessorId: null`.

---

### Iteration Processor

An Iteration processor always has **exactly two outlets**: "Iteration" (the scoped loop outlet) and "Abgeschlossen" (fires once after all iterations complete).

```json
[
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{uuid-1}",
    "gid": "{uuid-2}",
    "descriptorId": "da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575",
    "name": "Iteration",
    "presentation": "default",
    "executionType": "scoped",
    "targetProcessorId": "{first-step-inside-loop-id}",
    "connectorPoints": []
  },
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{uuid-3}",
    "gid": "{uuid-4}",
    "descriptorId": "dd8f5806-3156-4697-97c0-dd069570f2e6",
    "name": "Abgeschlossen",
    "presentation": "default",
    "executionType": "default",
    "targetProcessorId": null,
    "connectorPoints": []
  }
]
```

- The "Iteration" outlet fires once per loop item — its `executionType` is `"scoped"`.
- The "Abgeschlossen" outlet fires once after the full loop completes; typically `targetProcessorId: null`.

---

### TypeScript Processor

A TypeScript processor always has a hidden "Standard" system outlet plus any number of **custom named outlets**. The custom outlets are defined with `descriptorId: null` and their IDs are referenced in the processor's `customConfig.outletScriptIds`.

```json
[
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{uuid-1}",
    "gid": "{uuid-2}",
    "descriptorId": "c4b09fff-0dae-4726-bdeb-12fd01ddc2da",
    "name": "Standard",
    "presentation": "hidden",
    "executionType": "default",
    "targetProcessorId": null,
    "connectorPoints": []
  },
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{outlet-id-OK}",
    "gid": "{uuid-4}",
    "descriptorId": null,
    "name": "OK",
    "presentation": "default",
    "executionType": "default",
    "targetProcessorId": "{next-processor-id}",
    "connectorPoints": []
  },
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{outlet-id-Error}",
    "gid": "{uuid-5}",
    "descriptorId": null,
    "name": "Error",
    "presentation": "default",
    "executionType": "default",
    "targetProcessorId": null,
    "connectorPoints": []
  }
]
```

Key rules:
- The "Standard" outlet (`descriptorId: "c4b09fff-0dae-4726-bdeb-12fd01ddc2da"`) is always present and always `presentation: "hidden"`.
- Custom outlets have `descriptorId: null`.
- The `id` values of custom outlets (here `{outlet-id-OK}` and `{outlet-id-Error}`) **must exactly match** the values in `customConfig.outletScriptIds`.

---

### REST Consumer Processor

A REST Consumer processor always has a "Standard" outlet (primary, success path) and a "Sonstige" outlet (hidden, fallback for unexpected HTTP responses).

```json
[
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{uuid-1}",
    "gid": "{uuid-2}",
    "descriptorId": "6a132916-f955-4dbd-a377-2c3ee21e7fcb",
    "name": "Standard",
    "presentation": "primary",
    "executionType": "default",
    "targetProcessorId": "{transform-processor-id}",
    "connectorPoints": []
  },
  {
    "_type": "interfaces.OutletConfig",
    "_typeVersion": "interfaces-22.0.1006",
    "id": "{uuid-3}",
    "gid": "{uuid-4}",
    "descriptorId": "c95394e3-50c2-4b7c-9529-3149328355e9",
    "name": "Sonstige",
    "presentation": "hidden",
    "executionType": "default",
    "targetProcessorId": null,
    "connectorPoints": []
  }
]
```

- "Standard" uses `presentation: "primary"` and points to the next processing step (e.g., a TypeScript transform processor).
- "Sonstige" uses `presentation: "hidden"` and typically has `targetProcessorId: null`.

---

## Key Descriptor IDs (System-Defined Outlets)

These fixed UUIDs identify built-in outlet types. Use them exactly as shown — they are not generated per-config.

| Processor Type | Outlet Name | Descriptor ID |
|---|---|---|
| Lambda | Aufruf | `78861a9e-e99c-47c7-913b-6bf685f5557b` |
| Lambda | Abgeschlossen | `738f1301-f558-40b5-bbfc-e869a5832156` |
| Iteration | Iteration | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` |
| Iteration | Abgeschlossen | `dd8f5806-3156-4697-97c0-dd069570f2e6` |
| TypeScript | Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| REST Consumer | Standard | `6a132916-f955-4dbd-a377-2c3ee21e7fcb` |
| REST Consumer | Sonstige | `c95394e3-50c2-4b7c-9529-3149328355e9` |
| TypeScript custom outlets | (any name) | `null` |

---

## TypeScript Processor: `outletScriptIds` Explained

When a TypeScript processor has custom named outlets (beyond "Standard"), the processor's `customConfig` must include an `outletScriptIds` map. This map tells the TypeScript runtime which outlet ID to activate when the script selects a given outlet name.

```json
{
  "_type": "interfaces.TypeScriptProcessorConfig",
  "outletScriptIds": {
    "OK": "{outlet-id-of-OK-outlet}",
    "Error": "{outlet-id-of-Error-outlet}"
  }
}
```

The values in `outletScriptIds` **must exactly match** the `id` fields of the corresponding outlet objects in the `outlets` array. A mismatch will cause the outlet selection to fail silently at runtime.

In the TypeScript script itself, outlets are selected by name:

```typescript
export function execute(invocation: Invocation, self: Self) {
  if (isValid) {
    self.selectOutlet('OK');
  } else {
    self.selectOutlet('Error');
  }
}
```

The string passed to `selectOutlet()` must match both the outlet's `name` field and its key in `outletScriptIds`.

---

## Routing Chains: How Processors Connect

Outlets form a directed graph. Each outlet's `targetProcessorId` points to exactly one processor. A processor can be the target of multiple outlets (merging paths), but each outlet can point to only one target.

### Typical Linear Chain

```
Lambda (Aufruf) → Prepare → REST Consumer (Standard) → Transform → Lambda (Abgeschlossen: null)
```

Expressed in outlet fields:
- Lambda "Aufruf" outlet: `targetProcessorId = {prepare-processor-id}`
- Prepare "Standard" outlet: `targetProcessorId = {rest-consumer-processor-id}`
- REST Consumer "Standard" outlet: `targetProcessorId = {transform-processor-id}`
- Transform "OK" outlet: `targetProcessorId = null` (end of scoped execution)
- Lambda "Abgeschlossen" outlet: `targetProcessorId = null`

### Branching

TypeScript processors with multiple named outlets create branching paths:

```
Validate
  → OK outlet → Transform → (end)
  → Error outlet → (end)
```

Both branches can eventually point to `null` or reconverge on a shared processor.

---

## Common Mistakes

- **Forgetting to include the "Standard" hidden outlet** on TypeScript processors — it is required even if never used in scripts.
- **Mismatched outlet IDs in `outletScriptIds`** — the map values must equal the outlet `id` fields, not `gid` fields.
- **Using `executionType: "scoped"` on the wrong outlet type** — only Lambda "Aufruf" and Iteration "Iteration" use scoped execution.
- **Setting `connectorPoints` to anything other than `[]`** — always use an empty array in generated configs; the UI manages visual routing independently.
- **Using the wrong `descriptorId`** — copy descriptor IDs from the table above; do not generate them.
