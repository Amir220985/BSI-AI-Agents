# Pattern: Lambda → Iteration → TypeScript(prepare) → REST Consumer → TypeScript(transform)

This is the standard BSI EIP pattern for Lambda interfaces that call external REST APIs with batch input.

## Overview

This pattern handles:
- **Batch input** — the Lambda always receives an array; Iteration loops over each element
- **Input validation and cleaning** — the `prepare` TypeScript processor cleans and validates each item before calling the API
- **External API call** — the REST Consumer makes the HTTP request
- **Response transformation and routing** — the `transform` TypeScript processor parses the response and selects an outlet

## Pattern Diagram

```
Lambda (entry)
  └─[Aufruf/scoped]→ Iteration (loops over input array)
                        └─[Iteration/scoped]→ TypeScript "prepare" (clean/validate input)
                                                ├─[OK]→ REST Consumer (call external API)
                                                │         └─[Standard]→ TypeScript "transform" (parse response)
                                                │                         ├─[Valid]→ (end, success)
                                                │                         ├─[Invalid]→ (end, invalid input)
                                                │                         └─[Error]→ (end, technical error)
                                                └─[Error]→ (end, invalid characters)
```

The Iteration processor's `provideResult()` script picks the result from whichever processor ran last (either `prepare` on error, or `transform` after API call). The Lambda returns the full collected array.

## When to Use This Pattern

- Calling an external REST/HTTP API
- Processing an array of inputs (bulk validation, enrichment, lookup)
- Needing to validate or clean inputs before calling the API
- Returning structured results for each input item, including error objects

## Processor Configuration Details

### Position Layout

The processors follow a left-to-right layout on the y=2 row:

| Processor | scriptIdentifier | x | y |
|-----------|-----------------|---|---|
| Lambda | `lambda` | 2 | 2 |
| Iteration | `iteration` | 8 | 2 |
| TypeScript (prepare) | `prepare` | 14 | 2 |
| REST Consumer | `restConsumer` | 20 | 2 |
| TypeScript (transform) | `transform` | 26 | 2 |

### Lambda Processor

- `typeId`: `ec06bfe3-faab-4c2c-83bc-8420789d3479`
- `customConfig._type`: `interfaces.CrmLambdaProcessorConfig`
- Outlet `Aufruf` with `executionType: "scoped"` → Iteration
- Outlet `Abgeschlossen` with `executionType: "default"` → null

### Iteration Processor

- `typeId`: `21c361ec-5dec-4f13-9767-442db1adb3a3`
- `customConfig._type`: `interfaces.IterationProcessorConfig`
- `chunkSize: 1`, `workerThreads: 1` (sequential, one item at a time)
- `aggregateResults: true` — collects all per-item results into an array
- `aggregateAsListData: false`
- `ignoreNullValues: false`
- Outlet `Iteration` with `executionType: "scoped"` → prepare
- Outlet `Abgeschlossen` with `executionType: "default"` → null

### TypeScript "prepare" Processor

- `typeId`: `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`
- `customConfig._type`: `interfaces.TypeScriptProcessorConfig`
- `outletScriptIds` maps outlet names (`OK`, `Error`) to their outlet IDs
- Outlet `Standard` with `presentation: "hidden"` → null (unused)
- Outlet `OK` → REST Consumer
- Outlet `Error` → null (ends iteration for this item with error result)

### REST Consumer Processor

- `typeId`: `f069aa44-fb5c-469e-a727-705ca7072fee`
- `customConfig._type`: `interfaces.RestConsumerProcessorConfig`
- `httpMethod`: `"get"` (or `"post"` for POST requests)
- `server`: the base URL, e.g. `"https://api.iban.com/"`
- `path`: the API path, e.g. `"/clients/api/v4/iban/"`
- Outlet `Standard` with `presentation: "primary"` → transform
- Outlet `Sonstige` with `presentation: "hidden"` → null

### TypeScript "transform" Processor

- `typeId`: `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` (same as prepare — both are TypeScript processors)
- `customConfig._type`: `interfaces.TypeScriptProcessorConfig`
- `outletScriptIds` maps outlet names (`Valid`, `Invalid`, `Error`) to their outlet IDs
- Outlet `Standard` with `presentation: "hidden"` → null (unused)
- Outlet `Valid` → null
- Outlet `Invalid` → null
- Outlet `Error` → null

All terminal outlets point to `targetProcessorId: null` because the Iteration processor collects results — there is no further downstream processor.

## Data Flow Explained

1. **Caller** sends: `[{ iban: "DE89..." }, { iban: "CH93..." }]`
2. **Lambda** receives the array in `invocation.processors.lambda.input`
3. **Iteration** loops through each element; current element available at `invocation.processors.iteration.element`
4. **prepare** reads the element (`data = invocation.processors.iteration.element`), strips whitespace from `data.iban`, validates characters, sets `self.withAttribute('cleanedIban', cleanedIban)` and routes `OK` or `Error`
5. **restConsumer** calls the API — `prepareRequest` attaches query params including the cleaned value from `invocation.processors.prepare.cleanedIban`
6. **transform** reads `invocation.processors.restConsumer.body` and `.statusCode`, returns a result object and selects an outlet (`Valid`, `Invalid`, or `Error`)
7. **Iteration** collects all per-item results via `provideResult()` which returns `invocation.processors.prepare.result || invocation.processors.transform.result`
8. **Lambda** returns `invocation.processors.iteration.result` — the array of all per-item results

### Error Object Convention

When a processor returns an error result, use the standard error object shape so the Lambda framework can surface a user-facing message:

```json
{ "_type": "bsiscout.LambdaResultError", "displayMessage": "Human-readable error" }
```

## TypeScript Scripts (Real IBAN Example)

These are the actual scripts from the IBAN validation interface.

### `lambda/output.ts`

Returns the full collected array from Iteration as the Lambda's output.

```typescript
import { Output } from './api';
import { Invocation } from '../interface';

export function provideOutput(invocation: Invocation): Output {
  return invocation.processors.iteration.result;
}
```

Compiled JavaScript (`javaScript` field):
```javascript
export function provideOutput(invocation) {
    return invocation.processors.iteration.result;
}
```

### `iteration/data.ts`

Returns the array to iterate over — the Lambda input.

```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  const r =
invocation.processors.lambda.input
;
  return r;
}
```

Compiled JavaScript (`javaScript` field):
```javascript
export function provideData(invocation) {
    const r = invocation.processors.lambda.input;
    return r;
}
```

### `iteration/result.ts`

Returns the per-item result. Uses `||` to pick whichever processor produced a result — `prepare` short-circuits on validation error, `transform` handles the API response. Both cannot be non-null in the same invocation.

```typescript
import { Invocation } from '../interface';

export function provideResult(invocation: Invocation) {
  return invocation.processors.prepare.result || invocation.processors.transform.result;
}
```

Compiled JavaScript (`javaScript` field):
```javascript
export function provideResult(invocation) {
    return invocation.processors.prepare.result || invocation.processors.transform.result;
}
```

### `prepare/script.ts`

Cleans the IBAN (strip whitespace), validates characters, routes OK or Error.

The `attributes.d.ts` for this processor declares `cleanedIban: String` — any attribute set via `self.withAttribute()` must be declared there.

```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  let data = invocation.processors.iteration.element;

  // remove whitespaces
  let cleanedIban = data.iban.replace(/\s/g, "");

  // check for not allowed characters
  if (/^[a-zA-Z0-9]+$/.test(cleanedIban)) {
    self.withOutlet('OK');
    self.withAttribute('cleanedIban', cleanedIban)
    return;
  }

  self.withOutlet('Error');
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'IBAN contains invalid characters'
  };
}
```

Compiled JavaScript (`javaScript` field):
```javascript
export function process(invocation, self) {
    let data = invocation.processors.iteration.element;
    // remove whitespaces
    let cleanedIban = data.iban.replace(/\s/g, "");
    // check for not allowed characters
    if (/^[a-zA-Z0-9]+$/.test(cleanedIban)) {
        self.withOutlet('OK');
        self.withAttribute('cleanedIban', cleanedIban);
        return;
    }
    self.withOutlet('Error');
    return {
        "_type": "bsiscout.LambdaResultError",
        displayMessage: 'IBAN contains invalid characters'
    };
}
```

### `restConsumer/script.ts`

Attaches query parameters to the outgoing request. The function is named `prepareRequest` (not `process`).

```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('ibanApiKey'))
    .withQueryParam('format', 'json')
    .withQueryParam('iban', invocation.processors.prepare.cleanedIban)
}
```

Compiled JavaScript (`javaScript` field):
```javascript
import { Resolvers } from '@eip/core';
export function prepareRequest(invocation, self) {
    self
        .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('ibanApiKey'))
        .withQueryParam('format', 'json')
        .withQueryParam('iban', invocation.processors.prepare.cleanedIban);
}
```

Key points:
- `Resolvers.environmentVariables.resolveBySetting('ibanApiKey')` resolves an environment variable named `ibanApiKey` — the setting name must match what is configured in the BSI environment settings
- `invocation.processors.prepare.cleanedIban` accesses the attribute set by `self.withAttribute('cleanedIban', ...)` in the prepare script
- The `Self` interface for REST Consumer only offers `withHeader`, `withCookie`, `withPathParam`, `withQueryParam` — no `withOutlet` or `withBody` for GET requests

### `transform/script.ts`

Parses the API response: checks for errors, validates all IBAN aspects, extracts bank data.

```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { LOG } from '@eip/core';

export function process(invocation: Invocation, self: Self) {
  let response = invocation.processors.restConsumer.body;

  if (invocation.processors.restConsumer.statusCode === 200) {

    // Check for technical issues
    if (response.errors && response.errors.length) {
      self.withOutlet('Error');
      let errorMessage = response.errors.map((i) => i.message).join('. ');
      LOG.error(errorMessage)
      return {
        "_type": "bsiscout.LambdaResultError",
        displayMessage: errorMessage
      };
    }

    // Check Iban
    let validationAspects = ['chars', 'iban', 'account', 'structure', 'length', 'country_support'];
    for (var validationAspect of validationAspects) {
      let validation = response.validations[validationAspect];
      // a code starting with '2' indicates an invalid iban
      if (validation.code.startsWith('2')) {
        self.withOutlet('Invalid');
        return {
          valid: false,
        };
      }
    }

    // Extract additional data for valid iban
    let bankData = response.bank_data

    self.withOutlet('Valid');
    return {
      valid: true,
      bankCode: bankData.bank_code,
      bic: bankData.bic,
      bankName: bankData.bank
    };
  }

  self.withOutlet('Error');
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'Failed to validate iban'
  };
}
```

Compiled JavaScript (`javaScript` field):
```javascript
import { LOG } from '@eip/core';
export function process(invocation, self) {
    let response = invocation.processors.restConsumer.body;
    if (invocation.processors.restConsumer.statusCode === 200) {
        // Check for technical issues
        if (response.errors && response.errors.length) {
            self.withOutlet('Error');
            let errorMessage = response.errors.map((i) => i.message).join('. ');
            LOG.error(errorMessage);
            return {
                "_type": "bsiscout.LambdaResultError",
                displayMessage: errorMessage
            };
        }
        // Check Iban
        let validationAspects = ['chars', 'iban', 'account', 'structure', 'length', 'country_support'];
        for (var validationAspect of validationAspects) {
            let validation = response.validations[validationAspect];
            // a code starting with '2' indicates an invalid iban
            if (validation.code.startsWith('2')) {
                self.withOutlet('Invalid');
                return {
                    valid: false,
                };
            }
        }
        // Extract additional data for valid iban
        let bankData = response.bank_data;
        self.withOutlet('Valid');
        return {
            valid: true,
            bankCode: bankData.bank_code,
            bic: bankData.bic,
            bankName: bankData.bank
        };
    }
    self.withOutlet('Error');
    return {
        "_type": "bsiscout.LambdaResultError",
        displayMessage: 'Failed to validate iban'
    };
}
```

## Auto-Generated Files (readOnly: true)

These files are generated by the system and must not be manually edited. They must be present in the config with `readOnly: true` and `javaScript: null`.

### Interface-level auto-generated files

**`interface.d.ts`** — aggregates all processor attributes into the `Invocation` type. Regenerated whenever processors change.

**`testDefinition.d.ts`** — type definitions for the TestDriver test harness. Never edited.

### Per-processor auto-generated files

Each processor has an **`api.d.ts`** that exports `_Attributes` — the public shape of that processor as seen by other scripts via `invocation.processors.<name>`.

- For TypeScript processors with a `process()` function: `_Attributes` extends the processor's own `Attributes` and adds `result: ReturnType<typeof process>`
- For Iteration: `_Attributes` includes `element`, `index`, and `result`
- For Lambda: `_Attributes` includes `input` and `callingUserId`
- For REST Consumer: `_Attributes` includes `body`, `cookies`, `headers`, `header` (deprecated), `statusCode`

Each TypeScript processor also has a **`definition.d.ts`** that defines the `Self` interface (available outlets, `withAttribute`) and the `Outlet` type union.

## Variations

### Single-item Lambda (no array)

Lambda always receives/returns arrays — do not change this. Use `chunkSize: 1, workerThreads: 1` on Iteration (the default). The array wrapper is transparent to callers in most BSI Scout integrations.

### Parallel processing

Set `workerThreads: 4` and `chunkSize: 1` on the Iteration processor to process up to 4 items concurrently. Only safe when items are independent (no shared mutable state).

### Without prepare step

Connect Iteration directly to REST Consumer. In the REST Consumer `prepareRequest` script, read from `invocation.processors.iteration.element` directly instead of `invocation.processors.prepare.cleanedIban`. Update `iteration/result.ts` to only reference `invocation.processors.transform.result`.

### POST instead of GET

- Set `httpMethod: "post"` in REST Consumer `customConfig`
- In the REST Consumer `script.ts`, add `self.withBody(invocation.processors.prepare.payload)` — the `Self` interface for POST requests includes a `withBody` method
- The `prepareRequest` function signature stays the same

### Error-only routing from transform

All terminal outlets point to `targetProcessorId: null`. This is the standard case — Iteration collects results and there is no downstream processor after transform. The outlet name is still significant: it is recorded in the invocation log and can be inspected in tests via `testInvocation.outlet`.

### Path parameters instead of query parameters

If the API key or input value is part of the URL path (e.g. `/api/v1/validate/{iban}`), declare path params in `restapi.d.ts` and use `self.withPathParam('iban', invocation.processors.prepare.cleanedIban)` in `prepareRequest`. The `path` in `customConfig` should use `{iban}` as the placeholder.

---

## Pattern 3: CRM Batch with Scheduled Trigger

```
Temporal Trigger (daily) → CRM Data Search → Iteration → Invoke Lambda → CRM Mutation
```

**When to use:**
- Nightly or regular bulk updates of CRM records
- When existing Lambda logic should be applied to CRM data
- Batch enrichment: fetch external data for many records and write results back

**Core principle:** Search → Iterate → Enrich (via Lambda) → Write back (via Mutation)

**Processor chain:**

1. **Temporal Trigger** (`typeId: 406211f6-7b91-4790-b492-feb3e7cac22c`)
   - Configure `periodicityType`, `hour`, `minute`, `interval`
   - No script needed

2. **CRM Data Search** (`typeId: 633d02d2-bda7-450d-a399-277644d39082`)
   - Define `selection.relation` (which entity)
   - Set `selection.maximumRowCount` (safety limit, e.g. 20 or 100)
   - Define `selection.constraint` (filter: which records need updating)
   - Define `selection.selections` (which fields are needed)
   - Script `prepareQuery`: usually empty; optionally `self.withMaxRowCount(n)` for dynamic limit

3. **Iteration** (`typeId: 21c361ec-5dec-4f13-9767-442db1adb3a3`)
   - `aggregateResults: false` (batch results don't need to be collected)
   - Script `data.ts`: `return invocation.processors.{searchId}.data;`

4. **Invoke Lambda** (`typeId: 9d107af5-8cdc-4138-bbdf-fc5383ece181`)
   - `qualifiedLambdaId: "interfaces:lambdaProcessor:{lambdaProcessor_gid}:{interface_gid}"`
   - Script `prepare.ts`: `self.withInput({ field: invocation.processors.{iterationId}.element.field })`

5. **CRM Mutation** (`typeId: cf9ee65c-a489-4250-b76a-7b1741868c0f`)
   - Script `data.ts` (function: `prepareMutations`):
     ```typescript
     import { Mutations } from '@eip/crm-mutation';
     self.withMutations(Mutations.create('CrmXxxUpdate', {
       entityKey: invocation.processors.{iterationId}.element.id,
       field: invocation.processors.invokeLambda.data[0].field
     }));
     ```
   - Outlets: Standard (success), Fehler (error)

**Outlet descriptor IDs:**
- Temporal Trigger Standard: `b3f5da65-ba2e-40ab-9983-a4e34544ff28`
- CRM Data Search Standard: `59c636c9-ccce-4650-8460-f7025a556cd2`
- Invoke Lambda Standard: `cce40eff-3c00-45fc-b569-74c5eb3710b7`
- CRM Mutation Standard: `6c0f1af6-2051-4fd5-947b-398c59418229`
- CRM Mutation Fehler: `f3aac37d-ce3b-45d0-8c52-b157854d2e8f`

**Interface type:** Ad-Hoc (`typeId: f72f9f76-fb2d-4579-b397-471b2ed4c4e3`) — no Lambda entry point

**Pre-generation checklist:**
1. Which CRM entity is being processed? (e.g. CrmCustomer)
2. Which fields are searched and what filters applied? → Discovery: `/l/cpd-tools/codetypes`
3. Which Lambda is called? → qualifiedLambdaId from the target interface (gid of the Lambda processor + gid of the interface)
4. Which CRM mutation is executed? → Discovery: `/l/cpd-tools/mutationtypes/{name}`
5. Is a maximumRowCount set? (always required!)

**Full example:** `examples/weather-api/` — `Customer_Weather_Score-eac04f7f-...json`
