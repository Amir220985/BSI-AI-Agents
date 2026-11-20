# IBAN Validation — Annotated Configuration Walkthrough

This document is the primary reference example for the BSI EIP configuration generator. Every structural decision, script, and wiring pattern present in the IBAN validation configuration is explained here in full. Read this before generating a new REST API Lambda.

---

## Overview

The IBAN validation interface is a complete, production-ready BSI EIP Lambda that:

1. Accepts an array of IBAN strings from a caller.
2. Iterates over each IBAN individually.
3. Cleans and validates the IBAN format locally (before hitting the network).
4. Calls the `iban.com` REST API to validate the IBAN and retrieve bank data.
5. Returns a result per IBAN: either valid (with bank metadata), invalid, or an error.

It demonstrates every important pattern used in REST API Lambda interfaces: scoped iteration, pre-call data preparation, external REST invocation, multi-outlet routing, environment variable resolution, and per-item result aggregation.

**Source files:**
- `interfaces/IBAN_validation-af8cb193-e289-48d9-a9b6-36e30941909c.json` — the full interface definition
- `projects/IBAN-4ebaedb9-6f31-408d-bd36-9e36f8b3a357.json` — the project container
- `index.json` — the transfer manifest
- `export-definition.json` — the export descriptor

---

## 1. Data Flow

```
Caller
  │  invokes Lambda with [{iban: "DE89370400440532013000"}, ...]
  ▼
Lambda processor ("lambda")
  │  Aufruf outlet (scoped) — one scope per Lambda invocation
  ▼
Iteration processor ("iteration")
  │  Iteration outlet (scoped) — one sub-scope per array element
  ▼
TypeScript "prepare"
  │  strips whitespace, checks alphanumeric characters
  ├── OK outlet ──────────────────────────────────────────────────────────────┐
  │                                                                           │
  └── Error outlet → returns LambdaResultError("IBAN contains invalid chars") │
                                                                              │
                                                 REST Consumer "restConsumer" ◄┘
                                                   GET https://api.iban.com/clients/api/v4/iban/
                                                   ?api_key=...&format=json&iban=...
                                                   │
                                                   │ Standard outlet (primary)
                                                   ▼
                                             TypeScript "transform"
                                               │
                                               ├── Error outlet → LambdaResultError (API errors, non-200)
                                               ├── Invalid outlet → {valid: false}
                                               └── Valid outlet → {valid: true, bankCode, bic, bankName}

  Iteration result.ts collects: prepare.result || transform.result per item
  Lambda output.ts returns: iteration.result (the aggregated array)
```

The pipeline is entirely linear. Errors short-circuit: a `prepare` Error outlet means `restConsumer` and `transform` are never called for that item. The `iteration.result.ts` uses `||` to collect whichever processor actually produced output for each item.

---

## 2. Signature Explained

The signature is defined inside the Lambda processor's `customConfig` under the `signature` key. It is the public contract that BSI EIP exposes to callers.

### Signature UUID

```
f3eebd1e-ddd7-4f31-b799-0a780f26e538
```

This is the signature's own ID. It is embedded inside the `CrmLambdaProcessorConfig` and is separate from the processor's `id` and `gid`. Generate a fresh UUID for each new signature.

### Name and Description (Four Languages)

```json
"name": {
  "en": "IBAN Validation",
  "fr": "Validation de compte IBAN",
  "it": "Verifica IBAN",
  "und": "IBAN Validierung"
},
"description": {
  "en": "Validates an IBAN and returns additional information about the associated bank.",
  "fr": "Valide une IBAN et renvoie des informations supplémentaires sur la banque associée.",
  "it": "Valuta un IBAN e restituisce informazioni aggiuntive sulla banca ad esso associata.",
  "und": "Validiert eine IBAN und gibt zusätzliche Informationen über die zugehörige Bank zurück."
}
```

The `"und"` key is mandatory — it is the fallback locale (used as German in BSI context). `"en"`, `"fr"`, `"it"` are optional but included here for full multilingual support.

### Fixed Type IDs

```json
"inputTypeId":  "List:Dyn:LambdaInput",
"outputTypeId": "List:Dyn:LambdaOutput"
```

These are always exactly these two strings for Lambda interfaces. Do not change them.

### Input: One Field

```json
{
  "_type": "bsiscout.SignatureProperty",
  "_typeVersion": "bsiscout-24.1.001",
  "identifier": "iban",
  "name": { "und": "IBAN" },
  "description": null,
  "mandatory": true,
  "type": "Text250"
}
```

- `identifier`: `"iban"` — the property name used in TypeScript (`invocation.processors.lambda.input[0].iban`).
- `type`: `"Text250"` — IBANs are at most 34 characters, so `Text250` is appropriate.
- `mandatory: true` — callers must supply this field; EIP will reject calls that omit it.
- Only one input field is needed because the Lambda receives an array of objects, each with just the IBAN.

### Outputs: Four Fields

| identifier | type | mandatory | notes |
|---|---|---|---|
| `valid` | `Boolean` | n/a | Always present in all result objects (true or false) |
| `bankCode` | `Text60` | n/a | Bank sort code (BLZ); only present on valid IBANs |
| `bic` | `Text60` | n/a | BIC/SWIFT code; only present on valid IBANs |
| `bankName` | `Text250` | n/a | Full bank name; only present on valid IBANs |

Outputs are never mandatory. The `?` in the generated TypeScript interface reflects that any output field may be absent (e.g., `bankCode` is not populated when `valid` is `false`).

The generated `api.d.ts` for the Lambda processor derives directly from this signature:

```typescript
export type Input = LambdaInput[];
export type Output = LambdaOutput[];

export interface _Attributes {
  input: Input;
  callingUserId: string;
}

export interface LambdaInput {
  iban: string;
}

export interface LambdaOutput {
  valid?: boolean;
  bankCode?: string;
  bic?: string;
  bankName?: string;
}
```

---

## 3. All Five Processors

### Processor 1: Lambda ("lambda")

**Position:** x=2, y=2  
**typeId:** `ec06bfe3-faab-4c2c-83bc-8420789d3479` (CRM Lambda Processor)  
**Processor id:** `12cfe4f1-96f8-4681-8dd5-cae9dfba4632`  
**Processor gid:** `8c1720c7-9699-4154-8c8e-201cde98b28d`

#### Role

The Lambda processor is the entry point. It defines the callable signature and provides the mechanism for BSI EIP to receive external invocations. Every interface has exactly one Lambda processor, always as the first processor (x=2).

#### customConfig

```json
{
  "_type": "interfaces.CrmLambdaProcessorConfig",
  "_typeVersion": "interfaces-23.2.019",
  "signature": {
    "_type": "bsiscout.Signature",
    "_typeVersion": "bsiscout-24.1.001",
    "id": "f3eebd1e-ddd7-4f31-b799-0a780f26e538",
    "name": { "en": "IBAN Validation", "fr": "Validation de compte IBAN", "it": "Verifica IBAN", "und": "IBAN Validierung" },
    "description": { "en": "Validates an IBAN and returns additional information about the associated bank.", "fr": "Valide une IBAN et renvoie des informations supplémentaires sur la banque associée.", "it": "Valuta un IBAN e restituisce informazioni aggiuntive sulla banca ad esso associata.", "und": "Validiert eine IBAN und gibt zusätzliche Informationen über die zugehörige Bank zurück." },
    "inputTypeId": "List:Dyn:LambdaInput",
    "outputTypeId": "List:Dyn:LambdaOutput",
    "inputs": [ { ...iban field... } ],
    "outputs": [ { ...valid... }, { ...bankCode... }, { ...bic... }, { ...bankName... } ]
  }
}
```

#### Outlets

| Name | executionType | descriptorId | targetProcessorId | Explanation |
|---|---|---|---|---|
| `Aufruf` | `"scoped"` | `78861a9e-e99c-47c7-913b-6bf685f5557b` | `a8d5e05c-...` (iteration) | Fires once per invocation call; creates a sub-scope. Points to the Iteration processor. |
| `Abgeschlossen` | `"default"` | `738f1301-f558-40b5-bbfc-e869a5832156` | `null` | Fires once the lambda call cycle completes. No downstream processor — this is the end. |

The `executionType: "scoped"` on "Aufruf" is critical. It means the Lambda processor wraps the entire inner pipeline in a scope. The Lambda's `output.ts` script is called after all scoped work completes to produce the final return value.

#### Script: `output.ts`

```typescript
import { Output } from './api';
import { Invocation } from '../interface';

export function provideOutput(invocation: Invocation): Output {
  return invocation.processors.iteration.result;
}
```

**Line by line:**
- `Output` is the typed return type (`LambdaOutput[]`) derived from the signature.
- `provideOutput` is the entry point called by EIP after all processors finish.
- `invocation.processors.iteration.result` reads the aggregated array of per-item results that the Iteration processor has collected. This is the entire output of the lambda call.

The Lambda processor's `api.d.ts` is system-generated (readOnly: true) and cannot be edited.

---

### Processor 2: Iteration ("iteration")

**Position:** x=8, y=2  
**typeId:** `21c361ec-5dec-4f13-9767-442db1adb3a3` (Iteration Processor)  
**Processor id:** `a8d5e05c-5275-49a6-9e8c-e3a782da52e1`  
**Processor gid:** `244335ce-23f7-44e4-9f37-96f6fd743394`

#### Role

The Iteration processor takes the input array (one or more IBANs) and processes each element independently. It creates one sub-scope per array item. After all items are processed, it aggregates their individual results into a single output array. This is what allows the Lambda to accept multiple IBANs in one call and return one result per IBAN.

#### customConfig

```json
{
  "_type": "interfaces.IterationProcessorConfig",
  "_typeVersion": "interfaces-26.1.001",
  "aggregateResults": true,
  "aggregateAsListData": false,
  "chunkSize": 1,
  "workerThreads": 1,
  "ignoreNullValues": false
}
```

**Field explanations:**
- `aggregateResults: true` — tells the Iteration processor to collect each item's `result.ts` return value into the final `iteration.result` array. Without this, there would be no aggregation.
- `aggregateAsListData: false` — do not flatten arrays of arrays. Each item produces one result object, not a list of objects.
- `chunkSize: 1` — process one IBAN at a time. Relevant when `workerThreads > 1`.
- `workerThreads: 1` — sequential processing. For independent IBAN lookups this could be increased, but 1 is the safe default.
- `ignoreNullValues: false` — do not skip null elements in the input array (pass them through to detect errors).

#### Outlets

| Name | executionType | descriptorId | targetProcessorId | Explanation |
|---|---|---|---|---|
| `Iteration` | `"scoped"` | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` | `a69ffd89-...` (prepare) | Fires once per array element. Creates a sub-scope for that element's processing. Points to the `prepare` processor. |
| `Abgeschlossen` | `"default"` | `dd8f5806-3156-4697-97c0-dd069570f2e6` | `null` | Fires once after all elements have been processed. No downstream processor. |

#### Script: `data.ts`

```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  const r = invocation.processors.lambda.input;
  return r;
}
```

`provideData` returns the array that the Iteration processor will iterate over. Here it returns `invocation.processors.lambda.input`, which is the full input array the lambda received from its caller (typed as `LambdaInput[]`). The Iteration processor will call the "Iteration" outlet once for each element of this array.

#### Script: `result.ts`

```typescript
import { Invocation } from '../interface';

export function provideResult(invocation: Invocation) {
  return invocation.processors.prepare.result || invocation.processors.transform.result;
}
```

`provideResult` is called once per iteration item, after that item's sub-scope has finished. It returns the result that should be aggregated into the final `iteration.result` array.

The `||` (logical OR) is the key decision here:
- If `prepare` routed to its `Error` outlet, it returned a `LambdaResultError` object. `prepare.result` is truthy in that case.
- If `prepare` routed to `OK`, it returned nothing (`undefined`). Then `transform.result` is used — this contains whatever `transform` produced (valid, invalid, or error).

This pattern gracefully handles the two possible exit paths from the inner pipeline.

#### System-generated `api.d.ts` (readOnly: true)

```typescript
import { Flatten } from '@eip/core';
import { provideData } from './data';
import { provideResult } from './result';

export interface _Attributes {
  element: Flatten<ReturnType<typeof provideData>>;  // single item from the array
  index: number;                                      // 0-based iteration index
  result: ReturnType<typeof provideResult>[];         // aggregated results array
}
```

Inside the iteration scope, `invocation.processors.iteration.element` gives the current item being processed (one `LambdaInput` object), while `invocation.processors.iteration.result` (available after iteration completes) gives the full aggregated array.

---

### Processor 3: TypeScript "prepare"

**Position:** x=14, y=2  
**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` (TypeScript Processor)  
**Processor id:** `a69ffd89-6b06-48e5-84e4-fd41d44682d2`  
**Processor gid:** `9d3e0949-a3e6-431b-b77c-4b3603604de2`

#### Role

`prepare` is a defensive pre-processing step before the external API call. It:
1. Strips whitespace from the IBAN (callers may supply `"DE89 3704 0044 0532 0130 00"` with spaces).
2. Validates that the remaining characters are alphanumeric (IBANs are letters and digits only).
3. If valid: stores the cleaned IBAN as an attribute (`cleanedIban`) and routes to `OK`.
4. If invalid: immediately returns a `LambdaResultError` and routes to `Error`, bypassing the REST call entirely.

This prevents wasteful API calls for obviously malformed input.

#### customConfig

```json
{
  "_type": "interfaces.TypeScriptProcessorConfig",
  "_typeVersion": "interfaces-23.2.018",
  "outletScriptIds": {
    "OK":    "a306a854-64ce-42ac-99f7-13d7f129b882",
    "Error": "099e31bd-0665-47a6-b79e-f141328e25e9"
  }
}
```

`outletScriptIds` maps the outlet name (as used in `self.withOutlet('OK')`) to the outlet's `id` UUID. These IDs must exactly match the `id` fields of the corresponding outlet objects in the `outlets` array. The `Standard` outlet is never listed here because it is the implicit fallback and is not routed programmatically.

#### Outlets

| Name | descriptorId | presentation | targetProcessorId | Explanation |
|---|---|---|---|---|
| `Standard` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `"hidden"` | `null` | Always present, always hidden. Never invoked in this processor. |
| `OK` | `null` | `"default"` | `d9198b4b-...` (restConsumer) | Routes to the REST Consumer when the IBAN passes format validation. |
| `Error` | `null` | `"default"` | `null` | End of pipeline for this item. Returns the error to the Iteration result. |

Custom outlets have `descriptorId: null`. Only system-defined outlets (Standard, Aufruf, Abgeschlossen, etc.) use non-null descriptor IDs.

#### `attributes.d.ts` (user-maintained)

```typescript
export interface Attributes {
  cleanedIban: String
}
```

This declares the named attributes that `self.withAttribute()` may set. The `restConsumer` processor will later read `invocation.processors.prepare.cleanedIban` — this type declaration makes that access type-safe. Every `self.withAttribute()` call in `script.ts` must have a corresponding entry here.

#### `definition.d.ts` (system-generated, readOnly: true)

```typescript
import { Attributes } from './attributes';

export type Outlet = 'Error' | 'OK';

export interface Self {
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;
  withOutlet(outletId: Outlet): Self;
}
```

The `Outlet` type is derived from the keys of `outletScriptIds`. This prevents the script from routing to a non-existent outlet at compile time.

#### Script: `script.ts`

```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  let data = invocation.processors.iteration.element;  // current item: { iban: "..." }

  // Remove all whitespace characters (spaces, tabs, etc.)
  let cleanedIban = data.iban.replace(/\s/g, "");

  // IBANs consist only of letters A-Z and digits 0-9
  if (/^[a-zA-Z0-9]+$/.test(cleanedIban)) {
    self.withOutlet('OK');                              // route to REST Consumer
    self.withAttribute('cleanedIban', cleanedIban);    // store for downstream use
    return;                                             // no return value needed for OK path
  }

  // Invalid characters detected — short-circuit without calling the API
  self.withOutlet('Error');
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'IBAN contains invalid characters'
  };
}
```

**Important patterns:**
- `invocation.processors.iteration.element` — accessing the current iteration item (not the full array).
- `self.withOutlet()` followed by `return` — routing without a return value. The `||` in `result.ts` will fall through to `transform.result`.
- Returning `{ "_type": "bsiscout.LambdaResultError", ... }` — this is the standard error shape for BSI EIP lambdas. The `_type` marker tells EIP to surface this as a structured error, not raw output.
- `self.withAttribute()` — stores `cleanedIban` on the invocation scope so the REST Consumer can read it later as `invocation.processors.prepare.cleanedIban`.

---

### Processor 4: REST Consumer ("restConsumer")

**Position:** x=20, y=2  
**typeId:** `f069aa44-fb5c-469e-a727-705ca7072fee` (REST Consumer Processor)  
**Processor id:** `d9198b4b-be1c-463c-b968-4624fd5b55b7`  
**Processor gid:** `63955fcd-57ff-4f6f-8756-285c150558e1`

#### Role

`restConsumer` makes the outbound HTTP GET request to the `iban.com` API. It is purely an infrastructure processor — it does not contain any business logic. The `prepareRequest` script populates the query parameters; the response handling is entirely deferred to the `transform` processor downstream.

#### customConfig

```json
{
  "_type": "interfaces.RestConsumerProcessorConfig",
  "_typeVersion": "interfaces-24.2.008",
  "server": "https://api.iban.com/",
  "path": "/clients/api/v4/iban/",
  "httpMethod": "get"
}
```

- `server`: The base URL. Always ends with `/`.
- `path`: The API path. Starts with `/`. Combined with `server` to form the full URL.
- `httpMethod`: `"get"` — HTTP GET. Other values: `"post"`, `"put"`, `"patch"`, `"delete"`.

The full request URL becomes: `https://api.iban.com/clients/api/v4/iban/?api_key=...&format=json&iban=...`

#### Outlets

| Name | descriptorId | presentation | targetProcessorId | Explanation |
|---|---|---|---|---|
| `Standard` | `6a132916-f955-4dbd-a377-2c3ee21e7fcb` | `"primary"` | `5d00b8c8-...` (transform) | The main success path — EIP routes here after the HTTP response is received (any status code). Points to `transform`. |
| `Sonstige` | `c95394e3-50c2-4b7c-9529-3149328355e9` | `"hidden"` | `null` | Fallback outlet for unexpected response conditions. Hidden and unconnected. |

Note: The REST Consumer's "Standard" outlet fires for **all** responses including 4xx and 5xx. Status code handling is left to the downstream TypeScript processor (`transform`). The `Sonstige` outlet covers edge cases where EIP itself cannot process the response.

#### `restapi.d.ts` (user-editable)

```typescript
export type PathParams = any;
export type QueryParams = any;
export type RequestBody = any;
export type ResponseBody = any;
```

This file provides type stubs for the request/response shapes. It is intentionally typed as `any` to remain flexible. For stricter type safety, `ResponseBody` could be replaced with a typed interface matching the `iban.com` API response schema.

#### `definition.d.ts` (system-generated, readOnly: true)

```typescript
import { PathParams, QueryParams, RequestBody } from './restapi';

export interface Self {
  withHeader(name: string, value: string): Self;
  withCookie(name: string, value: string): Self;
  withPathParam<T extends keyof PathParams>(paramId: T, value: PathParams[T]): Self;
  withQueryParam<T extends keyof QueryParams>(paramId: T, ...value: QueryParams[T][]): Self;
}
```

These are the methods available on `self` inside `prepareRequest`.

#### Script: `script.ts`

```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('ibanApiKey'))
    .withQueryParam('format', 'json')
    .withQueryParam('iban', invocation.processors.prepare.cleanedIban);
}
```

**Line by line:**
- `Resolvers.environmentVariables.resolveBySetting('ibanApiKey')` — reads the `ibanApiKey` setting from BSI EIP's environment variable store. This is how API keys are injected at runtime without hardcoding them in the config.
- `'format', 'json'` — tells the iban.com API to return JSON (not XML).
- `invocation.processors.prepare.cleanedIban` — reads the attribute that `prepare` stored. This is the whitespace-free, validated IBAN string.

The function name is `prepareRequest` (not `process`) — this is the contract for REST Consumer scripts.

#### `api.d.ts` (system-generated, readOnly: true)

```typescript
import { MapLike } from '@eip/core';
import { ResponseBody } from './restapi';

export interface _Attributes {
  body: ResponseBody;                       // parsed JSON response body
  cookies: MapLike<string, string>;
  headers: MapLike<string, string>;
  /** @deprecated use `headers` instead. Will be removed in 26.1 */
  header: MapLike<string, string>;
  statusCode: number;                       // HTTP status code (200, 404, etc.)
}
```

Downstream processors access the response via `invocation.processors.restConsumer.body`, `...statusCode`, etc.

---

### Processor 5: TypeScript "transform"

**Position:** x=26, y=2  
**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` (TypeScript Processor)  
**Processor id:** `5d00b8c8-876d-41ab-a81d-49eafae8061e`  
**Processor gid:** `c3d75210-f804-4a17-a0d3-1d9beae70fc9`

#### Role

`transform` interprets the HTTP response from `iban.com` and translates it into the Lambda's output format. It handles three cases:
1. **API error** (200 with errors array populated) → `Error` outlet.
2. **Invalid IBAN** (200 with a validation aspect code starting with `"2"`) → `Invalid` outlet.
3. **Valid IBAN** (200, no errors, no failing validations) → `Valid` outlet with bank data.
4. **Non-200 HTTP status** → `Error` outlet.

#### customConfig

```json
{
  "_type": "interfaces.TypeScriptProcessorConfig",
  "_typeVersion": "interfaces-23.2.018",
  "outletScriptIds": {
    "Error":   "8eb0ff73-bcca-43e8-8e52-85a6c800ed84",
    "Valid":   "8cdd2798-4463-4b9d-a6c6-5bb29a94b92b",
    "Invalid": "6f39da7a-0b5b-4a85-a029-017b20b075d4"
  }
}
```

Three custom outlets, each mapped to its outlet `id` UUID. The `Standard` outlet is present but hidden and never used.

#### Outlets

| Name | presentation | targetProcessorId | Explanation |
|---|---|---|---|
| `Standard` | `"hidden"` | `null` | Always present, never used. |
| `Valid` | `"default"` | `null` | End of pipeline for this item. Returns `{valid: true, bankCode, bic, bankName}`. |
| `Invalid` | `"default"` | `null` | End of pipeline for this item. Returns `{valid: false}`. |
| `Error` | `"default"` | `null` | End of pipeline for this item. Returns a `LambdaResultError`. |

All three result outlets end the pipeline for that iteration item (`targetProcessorId: null`).

#### `attributes.d.ts` (user-maintained)

```typescript
export interface Attributes {
}
```

`transform` stores no attributes on the invocation scope — it only returns a result value. The Attributes interface is empty.

#### `definition.d.ts` (system-generated, readOnly: true)

```typescript
import { Attributes } from './attributes';

export type Outlet = 'Error' | 'Invalid' | 'Valid';

export interface Self {
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;
  withOutlet(outletId: Outlet): Self;
}
```

#### Script: `script.ts`

```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { LOG } from '@eip/core';

export function process(invocation: Invocation, self: Self) {
  let response = invocation.processors.restConsumer.body;

  if (invocation.processors.restConsumer.statusCode === 200) {

    // Check for API-level errors (e.g. invalid API key, rate limit)
    if (response.errors && response.errors.length) {
      self.withOutlet('Error');
      let errorMessage = response.errors.map((i) => i.message).join('. ');
      LOG.error(errorMessage);
      return {
        "_type": "bsiscout.LambdaResultError",
        displayMessage: errorMessage
      };
    }

    // Check all six validation aspects from iban.com
    // A code starting with '2' means that aspect failed (invalid IBAN)
    let validationAspects = ['chars', 'iban', 'account', 'structure', 'length', 'country_support'];
    for (var validationAspect of validationAspects) {
      let validation = response.validations[validationAspect];
      if (validation.code.startsWith('2')) {
        self.withOutlet('Invalid');
        return { valid: false };
      }
    }

    // All aspects passed — extract bank data from the response
    let bankData = response.bank_data;
    self.withOutlet('Valid');
    return {
      valid: true,
      bankCode: bankData.bank_code,
      bic: bankData.bic,
      bankName: bankData.bank
    };
  }

  // Non-200 response (timeout, server error, 404, etc.)
  self.withOutlet('Error');
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'Failed to validate iban'
  };
}
```

**Key decisions explained:**

- **Status code guard first**: The outer `if (statusCode === 200)` ensures we never try to parse a response body that may be empty (e.g. a 404 response).
- **Error check before validation**: The `iban.com` API returns `errors` at the top level for API-level failures (wrong key, rate limit). These are distinct from validation failures and must be handled first.
- **Validation aspect loop**: The iban.com API returns six separate validation codes. Any code starting with `"2"` indicates failure. The loop exits at the first failed aspect.
- **Result shape for valid IBAN**: Maps from `bank_data.bank_code` → `bankCode`, `bank_data.bic` → `bic`, `bank_data.bank` → `bankName`. The JSON field names from the API do not match the signature field names — this mapping is the core purpose of `transform`.
- **`LOG.error()`**: Writes to the EIP execution log. Useful for debugging API failures without surfacing internal details to the caller.

---

## 4. Complete TypeScript Script Inventory

The interface contains 12 `TypeScriptConfig` entries in its `typeScripts` array. Here is every one:

| processorId | scriptName | scriptKind | readOnly | test | Purpose |
|---|---|---|---|---|---|
| `null` | `attributes.d.ts` | `public-api` | false | false | Interface-level invocation attributes (empty in this config) |
| `null` | `testIbanValidation.ts` | `script` | false | true | Test suite (4 test cases, see Section 5) |
| `null` | `interface.d.ts` | `public-api` | true | false | Auto-generated: assembles all processor `_Attributes` into `ProcessorAttributes` and defines `Invocation` |
| `null` | `testDefinition.d.ts` | `public-api` | true | true | Auto-generated: type stubs for the `TestDriver` testing API |
| `5d00b8c8` (transform) | `api.d.ts` | `public-api` | true | false | Auto-generated: exposes `result` type as `ReturnType<typeof process>` |
| `5d00b8c8` (transform) | `definition.d.ts` | `private-api` | true | false | Auto-generated: `Outlet` union type and `Self` interface for `transform` |
| `5d00b8c8` (transform) | `attributes.d.ts` | `public-api` | false | false | User-maintained: empty `Attributes` interface (no `withAttribute` calls) |
| `5d00b8c8` (transform) | `script.ts` | `script` | false | false | User-maintained: response interpretation and outlet routing logic |
| `a69ffd89` (prepare) | `api.d.ts` | `public-api` | true | false | Auto-generated: exposes `result` type and `cleanedIban` attribute |
| `a69ffd89` (prepare) | `definition.d.ts` | `private-api` | true | false | Auto-generated: `Outlet` type `'Error' | 'OK'` and `Self` |
| `a69ffd89` (prepare) | `attributes.d.ts` | `public-api` | false | false | User-maintained: declares `cleanedIban: String` |
| `a69ffd89` (prepare) | `script.ts` | `script` | false | false | User-maintained: whitespace removal, character validation, routing |
| `d9198b4b` (restConsumer) | `api.d.ts` | `public-api` | true | false | Auto-generated: `body`, `cookies`, `headers`, `statusCode` attributes |
| `d9198b4b` (restConsumer) | `restapi.d.ts` | `public-api` | false | false | User-maintained: type stubs for request/response shapes (all `any`) |
| `d9198b4b` (restConsumer) | `script.ts` | `script` | false | false | User-maintained: `prepareRequest` sets query params |
| `d9198b4b` (restConsumer) | `definition.d.ts` | `private-api` | true | false | Auto-generated: `Self` with `withHeader`, `withQueryParam`, etc. |
| `12cfe4f1` (lambda) | `api.d.ts` | `public-api` | true | false | Auto-generated: `LambdaInput`, `LambdaOutput`, `_Attributes` from signature |
| `12cfe4f1` (lambda) | `output.ts` | `script` | false | false | User-maintained: `provideOutput` returns `iteration.result` |
| `a8d5e05c` (iteration) | `api.d.ts` | `public-api` | true | false | Auto-generated: `element`, `index`, `result` attributes |
| `a8d5e05c` (iteration) | `data.ts` | `script` | false | false | User-maintained: `provideData` returns `lambda.input` |
| `a8d5e05c` (iteration) | `result.ts` | `script` | false | false | User-maintained: `provideResult` returns `prepare.result || transform.result` |

**Note:** The actual file contains exactly 12 entries (some auto-generated ones are created by the system at import time and may not all appear in the exported JSON). The 8 user-maintained scripts are the ones to focus on when adapting this example.

---

## 5. Test Suite

The test file `testIbanValidation.ts` (`processorId: null`, `test: true`) uses the EIP `TestDriver` API to run the four scenarios against `transform` in isolation. All four tests mock the REST Consumer's response attributes directly, so they run without making any real HTTP call.

### TestDriver Pattern

```typescript
let testInvocation = TestDriver.createTest()
  .startWith('processorIdentifier')       // entry point for this test
  .stopAfter('processorIdentifier')       // exit point for this test
  .processorAttributes('processorId', a => a.attributes({ ... }))  // mock attributes
  .test();                                // execute and return result
```

### Test 1: ValidIban

**Scenario:** The iban.com API returns a 200 response with all passing validation codes and full bank data.

```typescript
test('ValidIban', () => {
  let testInvocation = TestDriver.createTest()
    .startWith('transform')
    .stopAfter('transform')
    .processorAttributes('restConsumer', a => a.attributes({
      "body": {
        "bank_data": {
          "bank": "Commerzbank",
          "bank_code": "37040044",
          "bic": "COBADEFFXXX",
          // ... other fields
        },
        "errors": [],
        "validations": {
          "account":         { "code": "002", "message": "Account Number check digit is correct" },
          "chars":           { "code": "006", "message": "IBAN does not contain illegal characters" },
          "country_support": { "code": "007", "message": "Country supports IBAN standard" },
          "iban":            { "code": "001", "message": "IBAN Check digit is correct" },
          "length":          { "code": "003", "message": "IBAN Length is correct" },
          "structure":       { "code": "005", "message": "IBAN structure is correct" }
        }
      },
      "statusCode": 200
    }))
    .test();

  let result = testInvocation.processors.transform.result;
  expect(result.valid).toBeTrue;
  expect(result.bic).toBe('COBADEFFXXX');
  expect(result.bankCode).toBe('37040044');
  expect(result.bankName).toBe('Commerzbank');
});
```

All validation codes start with a digit other than `"2"`, so none fail. The test verifies that `transform` correctly extracts `bank_code`, `bic`, and `bank` from the response.

### Test 2: InvalidIban

**Scenario:** The API returns validation codes starting with `"2"`, indicating the IBAN is invalid.

The mock response contains `"account": {"code": "201"}` and `"iban": {"code": "202"}`. The first failing code encountered (`"201"` for `chars` check, or whichever comes first in the loop) causes `transform` to route to the `Invalid` outlet.

```typescript
expect(testInvocation.outlet).toEqual('Invalid');
```

Note that the test only checks the outlet name, not the result content. For `Invalid`, the only returned value is `{valid: false}`.

### Test 3: 404

**Scenario:** The API server returns a 404 status.

```typescript
.processorAttributes('restConsumer', a => a.attributes({ "statusCode": 404 }))
// ...
expect(testInvocation.outlet).toEqual('Error');
```

No body is needed because the `transform` script checks `statusCode === 200` first. A 404 falls through to the `Error` branch with a generic message.

### Test 4: InvalidAPIKey

**Scenario:** The API returns 200 but with an errors array (e.g. invalid API key).

```typescript
.processorAttributes('restConsumer', a => a.attributes({
  "body": {
    "errors": [{ "code": "301", "message": "API Key is invalid" }],
    // ...
  },
  "statusCode": 200
}))
// ...
expect(testInvocation.outlet).toEqual('Error');
expect(testInvocation.processors.transform.result.displayMessage).toBe('API Key is invalid');
```

This test verifies that the `errors` array check fires before the validation loop, and that the error message from the API is surfaced as `displayMessage`.

---

## 6. Adapting This Config for a Different REST API

To generate a new Lambda that calls a different REST API, change these 8 things:

### Step 1: Update the Signature

In the Lambda processor's `customConfig.signature`:
- Change `name` (all locales).
- Change `description` (all locales).
- Replace `inputs` with your API's input fields (choose appropriate `type`, set `mandatory`).
- Replace `outputs` with your API's output fields.
- Generate a new UUID for `signature.id`.

### Step 2: Update the REST Consumer `customConfig`

```json
{
  "_type": "interfaces.RestConsumerProcessorConfig",
  "_typeVersion": "interfaces-24.2.008",
  "server": "https://your-api.example.com/",
  "path": "/your/api/path/",
  "httpMethod": "get"
}
```

Change `server`, `path`, and `httpMethod` to match the target API.

### Step 3: Update `prepare/script.ts`

Adapt the cleaning and validation logic to match the new input format:
- What whitespace rules apply?
- What character constraints apply?
- What attribute name(s) should be stored with `self.withAttribute()`?
- Update `prepare/attributes.d.ts` to declare any new attributes.

### Step 4: Update `restConsumer/script.ts`

Update `prepareRequest`:
- Change the query parameter names to match the new API.
- Change the environment variable setting name (e.g., `'myApiKey'` instead of `'ibanApiKey'`).
- If the API uses headers for auth instead of query params: use `self.withHeader('Authorization', ...)`.
- If the API uses path parameters: use `self.withPathParam(...)` and add `{paramName}` to the `path` in customConfig.

### Step 5: Update `transform/script.ts`

Adapt the response interpretation:
- Change the `statusCode === 200` guard if the API uses a different success code.
- Replace the `response.errors` check with the new API's error format.
- Replace the validation loop with the new API's validity signal.
- Replace the field extraction (`bankData.bank_code`, etc.) with the new API's response structure.
- Update the returned object fields to match the new signature outputs.

### Step 6: Update `transform` Outlets (if needed)

If the new API has different success/failure conditions, add or remove outlets:
- Add entries to `outletScriptIds` in `customConfig`.
- Add corresponding outlet objects to the `outlets` array (with new UUIDs for `id` and `gid`).
- Update `transform/definition.d.ts` `Outlet` type accordingly (auto-generated at import time).

### Step 7: Update the Environment Variable Name

In `restConsumer/script.ts`, change the `resolveBySetting(...)` argument to the new variable name. Remember to register this variable in BSI EIP Settings after import (see Section 7).

### Step 8: Update `lambda/api.d.ts`

This file is auto-generated from the signature at import time. If you change the signature, the TypeScript interfaces will update automatically. No manual edit needed, but if you need to pre-populate it: regenerate `LambdaInput` and `LambdaOutput` from your new signature fields.

---

## 7. Post-Import Setup

After importing this configuration ZIP into BSI EIP, one manual configuration step is required:

### Register the Environment Variable

Navigate to: **BSI EIP Settings → Environment Variables**

Add a new entry with the setting name `ibanApiKey`:

```json
{
  "ibanApiKey": {
    "_type": "interfaces.EnvironmentVariableValue",
    "_typeVersion": "interfaces-22.0.1001",
    "crypt": false,
    "value": "YOUR-IBAN-COM-API-KEY"
  }
}
```

- `crypt: false` — the value is stored in plain text. Set to `true` for credentials that should be encrypted at rest.
- `value` — your actual API key from `https://www.iban.com/api-key`.

Without this environment variable, `restConsumer/script.ts` will throw at runtime when `Resolvers.environmentVariables.resolveBySetting('ibanApiKey')` cannot find the key.

### Verify Import

After import and environment variable setup:
1. Open the IBAN validation interface in the BSI EIP editor.
2. Run the test suite (`testIbanValidation.ts`) — all 4 tests should pass.
3. Switch the interface to `status: "live"` if it was imported as draft.
4. Make a test invocation with a known-valid IBAN (e.g. `DE89370400440532013000`).

---

## 8. Key UUID Reference for This Configuration

| Entity | UUID |
|---|---|
| Interface `id` | `af8cb193-e289-48d9-a9b6-36e30941909c` |
| Interface `gid` | `8e21cc76-b0d4-4a29-a041-e984c37ac69b` |
| Signature `id` | `f3eebd1e-ddd7-4f31-b799-0a780f26e538` |
| Project `id` | `4ebaedb9-6f31-408d-bd36-9e36f8b3a357` |
| Processor: lambda `id` | `12cfe4f1-96f8-4681-8dd5-cae9dfba4632` |
| Processor: iteration `id` | `a8d5e05c-5275-49a6-9e8c-e3a782da52e1` |
| Processor: prepare `id` | `a69ffd89-6b06-48e5-84e4-fd41d44682d2` |
| Processor: restConsumer `id` | `d9198b4b-be1c-463c-b968-4624fd5b55b7` |
| Processor: transform `id` | `5d00b8c8-876d-41ab-a81d-49eafae8061e` |
| Outlet: lambda Aufruf `id` | `1390f6d8-6eff-4617-b7af-fce01a789776` |
| Outlet: iteration Iteration `id` | `08e99829-8a61-497f-b682-89d9bded7c10` |
| Outlet: prepare OK `id` | `a306a854-64ce-42ac-99f7-13d7f129b882` |
| Outlet: prepare Error `id` | `099e31bd-0665-47a6-b79e-f141328e25e9` |
| Outlet: transform Valid `id` | `8cdd2798-4463-4b9d-a6c6-5bb29a94b92b` |
| Outlet: transform Invalid `id` | `6f39da7a-0b5b-4a85-a029-017b20b075d4` |
| Outlet: transform Error `id` | `8eb0ff73-bcca-43e8-8e52-85a6c800ed84` |
