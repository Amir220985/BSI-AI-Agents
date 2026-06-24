# Weather API — Annotated Configuration Walkthrough

This document is the second reference example for the BSI EIP configuration generator. It builds on the IBAN validation example and introduces four new capabilities: the **Local Routine** processor, the **REST Provider** processor, the **CRM Data Search** processor, the **CRM Mutation** processor, and the **Invoke Lambda** processor. It also shows how to define a custom CRM code list and a custom CRM field, and how to connect those definitions to interface signatures and TypeScript imports.

Read the IBAN validation ANNOTATION.md first — this document focuses on what is new, not on repeating patterns already explained there.

---

## 0. Overview

This example exports two BSI EIP interfaces plus CRM data model extensions:

**WetterAbfrage** (Lambda + REST Provider) — A Lambda interface that:
1. Accepts a city name as input.
2. Validates and sanitizes the city name.
3. Calls the public `wttr.in` API for current weather data.
4. Scores the weather (Fantastisch / Gut / Erträglich / Schlecht) using a point algorithm.
5. Returns temperature, wind speed, humidity, weather condition text, and the score code.

In addition, the same interface exposes the weather lookup as a **REST endpoint** (`GET /weather/{city}`) via a REST Provider + Local Routine.

**Customer Weather Score** (Ad-Hoc) — A nightly batch interface that:
1. Triggers daily at 01:00.
2. Searches CRM customers who are active and do not yet have a weather score.
3. Reads each customer's city from their preferred physical address.
4. Calls the WetterAbfrage Lambda for each city.
5. Writes the score back to the custom `y-weatherScore` field on the customer record.

**What is new compared to IBAN validation:**

| Pattern | IBAN example | This example |
|---|---|---|
| Lambda + Iteration + REST Consumer | Yes | Yes |
| Custom outlet routing (prepare/transform) | Yes | Yes |
| Environment variables | Yes | No (wttr.in is public) |
| CRM data model customization | No | Yes (code list + field) |
| Local Routine processor | No | Yes |
| REST Provider processor | No | Yes |
| Invocation attributes as shared state | No | Yes (`attributes.input`) |
| `@eip/crm-core` Codes import | No | Yes |
| CRM Data Search processor | No | Yes |
| Iteration without result aggregation | No | Yes |
| Invoke Lambda processor | No | Yes |
| CRM Mutation processor | No | Yes |
| `@eip/crm-mutation` Mutations import | No | Yes |
| Two-stage multi-package ZIP | No | Yes |

---

## 1. ZIP Structure

The export is a **multi-package ZIP** with two sub-ZIPs (stages), indexed by `multi-index.json`. This two-stage structure is required whenever CRM data model changes must be deployed before interface configurations.

```
weather-api/
├── multi-index.json              ← Multi-package index (productId crm → productId interfaces)
├── 01-crm/                       ← Stage 1: CRM data model customizations
│   ├── index.json                ← Transfer manifest for stage 1
│   ├── export-definition.json    ← Export descriptor
│   ├── export-log.txt            ← Export log
│   ├── codes/
│   │   ├── Eigene_Wertelisten-103294/
│   │   │   ├── Wetter_Score-9ac81c27-...json     ← Code list header
│   │   │   ├── Fantastisch-368ff57b-...json       ← Code value
│   │   │   ├── Gut-403071c4-...json               ← Code value
│   │   │   ├── Ertr+ñglich-832bfd2a-...json       ← Code value (URL-encoded ä)
│   │   │   └── Schlecht-563e80b6-...json          ← Code value
│   │   └── Sprachen-71099/
│   │       ├── Deutsch-246.json                   ← Language code (dependency)
│   │       ├── Englisch-1303.json
│   │       ├── Franz+Âsisch-7770.json
│   │       └── Italienisch-7771.json
│   └── datamodel/
│       └── fields/
│           └── Wetter_Score-CrmCustomer...y-weatherScore.json  ← Custom field
└── 02-interfaces/                ← Stage 2: Interface configurations
    ├── index.json
    ├── export-definition.json
    ├── export-log.txt
    ├── interfaces/
    │   ├── WetterAbfrage-c9781b3c-...json          ← Lambda + REST Provider interface
    │   └── Customer_Weather_Score-eac04f7f-...json ← Ad-Hoc batch interface
    ├── webapis/
    │   ├── headers/
    │   │   └── Weather-7a28d2aa-...json            ← Web API header (base path)
    │   └── endpoints/
    │       └── weather{city}_-_GET-f1f35f8c-...json ← Endpoint definition
    └── projects/
        └── WetterAbfrage-4ca1cf10-...json          ← Project container
```

The `multi-index.json` defines the import order:

```json
{
  "stages": [
    { "productId": "crm",        "rootPath": "01-crm",        "exportId": "8786a1ac-..." },
    { "productId": "interfaces", "rootPath": "02-interfaces",  "exportId": "34ef4ab5-..." }
  ]
}
```

Stage 1 (CRM) must complete before Stage 2 (interfaces) because the interface signature references the `CrmCode` type from Stage 1. BSI EIP's import process applies stages sequentially.

---

## 2. CRM Data Model Customization

### 2.1 Code List: Wetter_Score

**File:** `01-crm/codes/Eigene_Wertelisten-103294/Wetter_Score-9ac81c27-0a86-459c-ba62-482fee56739c.json`

This defines the code list header (the category that contains the four score values). Key fields:

```json
{
  "_type": "crm.CrmCode",
  "scriptIdentifier": "AttributeUserDefinedCodes.WeatherScore",
  "codeUid": "1;112192;106064;j1000120161;j103294",
  "names": {
    "1;112192;106064;j246;j71099":  "Wetter Score",
    "1;112192;106064;j1303;j71099": "Weather Score"
  }
}
```

The `id` in the file name (`9ac81c27-0a86-459c-ba62-482fee56739c`) is the **UUID** of this code list. This UUID appears in three places:
- The field definition's `typeId`: `"Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c"`
- The CRM Search constraint's `targetType`
- The Lambda signature's output `type` for the `score` field

### 2.2 Code Values

The four child codes are defined in the same folder. Each is a child of the Wetter_Score code list (`parentUid` points to the list's `codeUid`):

| File name | German name | English name | scriptIdentifier | sortcode |
|---|---|---|---|---|
| `Fantastisch-368ff57b-...json` | Fantastisch | Fantastic | `AttributeUserDefinedCodes.WeatherScoreFantastic` | 10 |
| `Gut-403071c4-...json` | Gut | Good | `AttributeUserDefinedCodes.WeatherScoreGood` | 20 |
| `Ertr+ñglich-832bfd2a-...json` | Erträglich | Tolerable | `AttributeUserDefinedCodes.WeatherScoreTolerable` | 30 |
| `Schlecht-563e80b6-...json` | Schlecht | Bad | `AttributeUserDefinedCodes.WeatherScoreBad` | 40 |

The `scriptIdentifier` (e.g. `AttributeUserDefinedCodes.WeatherScoreFantastic`) is how these codes are referenced in TypeScript via `import { Codes } from '@eip/crm-core'`. The `Codes` object exposes a constant for each code value whose runtime value is the UUID of that code.

The `Sprachen-71099/` subfolder contains language codes (Deutsch, Englisch, Französisch, Italienisch) that are dependencies of the name localization structure. They are exported alongside the Wetter_Score codes but are standard system codes that already exist in any BSI CRM installation.

### 2.3 Custom Field: y-weatherScore on CrmCustomer

**File:** `01-crm/datamodel/fields/Wetter_Score-CrmCustomerbsiscout.DataModelRelationIdy-weatherScore.json`

This defines a new relation field on the `CrmCustomer` entity:

```json
{
  "_type": "crm.DataModelDataFieldConfig",
  "dataFieldId": "CrmCustomer/bsiscout.DataModelRelationId:y-weatherScore",
  "definition": {
    "typeId": "Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c",
    "sql": "Y_WEATHER_SCORE_UID",
    "column": true,
    "list": false,
    "searchIndexed": false
  },
  "itemConfig": {
    "entityId": "CrmCustomer",
    "names": { "und": "Wetter Score", "en": "Weather Score" }
  }
}
```

Key points:
- **`dataFieldId`**: The field's technical identifier. The prefix `y-` is a BSI convention for custom (customer-specific) fields.
- **`typeId`**: `Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c` — this is a relation to the Wetter_Score code list. The field stores the UUID of one code value.
- **`sql`**: `Y_WEATHER_SCORE_UID` — the actual DB column name in the CRM database.
- **`column: true`**: The value is persisted as a separate column (not in a serialized blob).
- **`list: false`**: A single code value per customer (not a multi-select).

When the CRM Mutation writes `y_weatherScore: score`, it stores the UUID returned by `Codes.AttributeUserDefinedCodes.WeatherScoreXxx` into the `Y_WEATHER_SCORE_UID` column.

---

## 3. Interface 1: WetterAbfrage (Lambda + REST Provider)

### 3.1 Data Flow

Two separate entry paths converge at the shared `weatherApi_prepare` processor:

```
Lambda path:
  weatherApi_lambda [x=2,y=2]
    └─ Aufruf (scoped) ──► weatherApi_iteration [x=8,y=2]
                             └─ Iteration (scoped) ──► lambdaInput_weatherApi_typescript [x=14,y=2]
                                                          └─ Standard ──► weatherApi_prepare [x=21,y=3]
                                                                            ├─ OK ──► weatherApi_restConsumer [x=27,y=3]
                                                                            │           └─ Standard ──► weatherApi_transform [x=33,y=3]
                                                                            │                           ├─ Valid ──► (end)
                                                                            │                           ├─ Invalid ──► (end)
                                                                            │                           └─ Error ──► (end)
                                                                            └─ Error ──► (end)

REST Provider path:
  restProvider [x=2,y=15]
    └─ Aufruf (scoped) ──► callWeatherApi_customer_typescript [x=8,y=15]
                             └─ Standard ──► (end)
                             (calls LocalRoutines.weatherApi_localRoutine internally)

Local Routine (called from REST Provider path):
  weatherApi_localRoutine [x=8,y=8]
    └─ Aufruf (scoped) ──► localRoutineInput_weatherApi_typescript [x=14,y=8]
                             └─ Standard ──► weatherApi_prepare [x=21,y=3] (shared!)
```

The key architectural insight: `weatherApi_prepare`, `weatherApi_restConsumer`, and `weatherApi_transform` are **shared** by both paths. The two input processors (`lambdaInput_weatherApi_typescript` and `localRoutineInput_weatherApi_typescript`) write to the same `invocation.attributes.input` object so that `weatherApi_prepare` can read from it regardless of which path triggered it.

### 3.2 Signature

**Signature id:** `1a70a628-af57-4d50-b9d9-215cf3dbba69`

**Names:**
```json
{
  "en": "Weather Query",
  "und": "Wetter Abfrage"
}
```

**Description:**
```json
{
  "en":  "Returns current weather data for a city name.",
  "und": "Gibt aktuelle Wetterdaten für einen Stadtnamen zurück."
}
```

**Input:**

| identifier | type | mandatory | description |
|---|---|---|---|
| `city` | `Text60` | true | City name / Stadtname |

**Outputs:**

| identifier | type | description |
|---|---|---|
| `temperature` | `Integer` | Temperature in °C |
| `wind` | `Integer` | Wind speed in km/h |
| `condition` | `Text250` | Weather condition text |
| `humidity` | `Integer` | Humidity in % |
| `score` | `Key:Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c` | Weather score (CrmCode reference) |

The `score` output type `Key:Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c` references the Wetter_Score code list from Stage 1. The value stored is the UUID of the selected code (e.g. the UUID for "Fantastisch"). This is how EIP knows to present it as a code lookup in the UI and how calling interfaces know to interpret the value.

The generated `api.d.ts` for the Lambda processor:

```typescript
export type Input = LambdaInput[];
export type Output = LambdaOutput[];

export interface _Attributes {
  input: Input;
  callingUserId: string;
}

export interface LambdaInput {
  city: string;
}

export interface LambdaOutput {
  temperature?: number;
  wind?: number;
  condition?: string;
  humidity?: number;
  score?: string;   // runtime value: UUID of the selected CrmCode
}
```

Note that `score` is typed as `string` in TypeScript — EIP represents entity key references as UUID strings at runtime.

### 3.3 Interface Metadata

```json
{
  "id":              "c9781b3c-4ac1-472b-b0ee-b69c90fb200d",
  "gid":             "ffc77303-8574-4206-b7e5-ec9be108af21",
  "typeId":          "2512c737-a73b-4f78-9ae2-098ac6d291bd",
  "name":            "WetterAbfrage",
  "logLevel":        "warn",
  "recordingLevel":  "analytics",
  "runtime":         "b",
  "status":          "draft",
  "projectId":       "4ca1cf10-6a17-4389-b979-a41cbfe97167"
}
```

`typeId: 2512c737-a73b-4f78-9ae2-098ac6d291bd` identifies this as a **Lambda** interface. The `gid` (`ffc77303-...`) is the stable cross-environment identifier referenced in the `qualifiedLambdaId` of the Invoke Lambda processor in the second interface.

The interface-level `attributes.d.ts` (processorId=null, readOnly=false) defines invocation-level shared state:

```typescript
export interface Attributes {
  input: {
    city: string;
  };
}
```

This declares the `invocation.attributes.input` object that both input processors write to and that `weatherApi_prepare` reads from.

### 3.4 Processor: weatherApi_lambda

**typeId:** `ec06bfe3-faab-4c2c-83bc-8420789d3479` (CRM Lambda Processor)  
**id:** `6e2cf0d0-a4f3-41ec-9f8b-0a0d3ff0647e`  
**gid:** `dc045211-0a34-4ca4-ba94-dbbc27b50d21`  
**scriptIdentifier:** `weatherApi_lambda`  
**position:** x=2, y=2

The entry point for Lambda invocations. Holds the signature definition. Identical in structure to the IBAN example's `lambda` processor.

**Outlets:**

| Name | descriptorId | executionType | target | Notes |
|---|---|---|---|---|
| `Aufruf` | `78861a9e-e99c-47c7-913b-6bf685f5557b` | `scoped` | `weatherApi_iteration` | Creates a sub-scope for the iteration pipeline |
| `Abgeschlossen` | `738f1301-f558-40b5-bbfc-e869a5832156` | `default` | null | End of call cycle |

**Script `output.ts`:**

```typescript
export function provideOutput(invocation: Invocation): Output {
  return invocation.processors.weatherApi_iteration.result;
}
```

Returns the aggregated array from the iteration. Because `aggregateResults=true` on the iteration and `result.ts` returns `result.data` (a single object), the final Lambda output is an array of one weather result object per input city.

### 3.5 Processor: weatherApi_iteration

**typeId:** `21c361ec-5dec-4f13-9767-442db1adb3a3` (Iteration Processor)  
**id:** `36325f71-2072-4f46-accb-e7ee76ea8cb7`  
**gid:** `b47d01cb-2f75-4fd9-9cda-73d5cb343cf4`  
**scriptIdentifier:** `weatherApi_iteration`  
**position:** x=8, y=2

```json
"customConfig": {
  "_type": "interfaces.IterationProcessorConfig",
  "aggregateResults": true,
  "aggregateAsListData": false,
  "chunkSize": 1,
  "workerThreads": 1,
  "ignoreNullValues": false
}
```

`aggregateResults: true` means `result.ts` is called once per item and its return value is collected into `iteration.result[]`. The Lambda's `output.ts` then returns this array as the final output.

**Outlets:**

| Name | descriptorId | executionType | target |
|---|---|---|---|
| `Iteration` | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` | `scoped` | `lambdaInput_weatherApi_typescript` |
| `Abgeschlossen` | `dd8f5806-3156-4697-97c0-dd069570f2e6` | `default` | null |

**Script `data.ts`:**

```typescript
export function provideData(invocation: Invocation) {
  const r = invocation.processors.weatherApi_lambda.input;
  return r;
}
```

Returns the full Lambda input array (`LambdaInput[]`). The iteration will fire its `Iteration` outlet once for each element.

**Script `result.ts`:**

```typescript
import { ProcessorTypes } from '@eip/core';
export function provideResult(invocation: Invocation) {
  const result = invocation.processors.weatherApi_transform.result;
  return result?.data != null
    ? result.data
    : ProcessorTypes.lambda.createLambdaResultErrorDo('Weather API failed!');
}
```

`result.data` is the object `{ temperature, wind, condition, humidity, score }` returned by `weatherApi_transform` on the `Valid` outlet. If `transform` routed to `Invalid` or `Error` instead, `result.data` is null/undefined and a `LambdaResultError` is created using the `ProcessorTypes.lambda` helper.

Note: Unlike the IBAN example which used the raw `{ "_type": "bsiscout.LambdaResultError", ... }` literal, this example uses `ProcessorTypes.lambda.createLambdaResultErrorDo()` — both approaches are valid; the helper is the preferred modern form.

**Auto-generated `api.d.ts`:**

```typescript
import { Flatten } from '@eip/core';
import { provideData } from './data';
import { provideResult } from './result';

export interface _Attributes {
  element: Flatten<ReturnType<typeof provideData>>;  // one LambdaInput: { city: string }
  index: number;
  result: ReturnType<typeof provideResult>[];         // aggregated results
}
```

### 3.6 Processor: lambdaInput_weatherApi_typescript

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` (TypeScript Processor)  
**id:** `89c96799-1bb1-4e41-a1ed-30ef5c291de7`  
**scriptIdentifier:** `lambdaInput_weatherApi_typescript`  
**position:** x=14, y=2

This is a **bridge processor** whose sole purpose is to copy the current iteration element's `city` into the shared `invocation.attributes.input` object so that the downstream `weatherApi_prepare` processor can read it using a path that does not depend on which entry path was used.

**Outlets:**

| Name | descriptorId | presentation | target |
|---|---|---|---|
| `Standard` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `primary` | `weatherApi_prepare` |

**Script `script.ts`:**

```typescript
export function process(invocation: Invocation, self: Self) {
  const city = invocation.processors.weatherApi_iteration.element.city;
  invocation.attributes.input = {
    city: city
  };
}
```

Reads from `weatherApi_iteration.element.city` (the current array item) and writes to `invocation.attributes.input`. Because `invocation.attributes` is part of the invocation scope, it is accessible to all downstream processors in the same scope.

The `attributes.d.ts` for this processor is empty (`export interface Attributes {}`): it uses `withAttribute` to set nothing — it writes directly to the shared invocation attribute defined at the interface level.

### 3.7 Processor: weatherApi_prepare (shared)

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` (TypeScript Processor)  
**id:** `ccc16f3b-67af-40e3-8298-be8ab3bda42c`  
**gid:** `0bca22dc-001f-4fa3-84de-e320b2ac9fc6`  
**scriptIdentifier:** `weatherApi_prepare`  
**position:** x=21, y=3  
**groupId:** `cc5f3941-cc50-4602-b8cc-5801f107066c` (group "Weather API")

```json
"customConfig": {
  "outletScriptIds": {
    "OK":    "1cd2b9d5-5864-4534-bbd3-6ab040460fcb",
    "Error": "7ab866da-2663-41f0-9cb1-78bd02f75cff"
  }
}
```

**Outlets:**

| Name | descriptorId | presentation | target |
|---|---|---|---|
| `Standard` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `hidden` | null |
| `OK` | null (id: `1cd2b9d5-...`) | `default` | `weatherApi_restConsumer` |
| `Error` | null (id: `7ab866da-...`) | `default` | null |

**`attributes.d.ts`:**

```typescript
export interface Attributes {
  cleanedCity: String
}
```

**`definition.d.ts`** (auto-generated):

```typescript
export type Outlet = 'Error' | 'OK';

export interface Self {
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;
  withOutlet(outletId: Outlet): Self;
}
```

**Script `script.ts`:**

```typescript
import { LOG } from '@eip/core';

export function process(invocation: Invocation, self: Self) {
  const cityRaw = invocation.attributes.input.city;

  if (!cityRaw || typeof cityRaw !== 'string') {
    self.withOutlet('Error');
    LOG.error('City is missing');
    return { error: 'City is missing' };
  }

  const city = cityRaw.trim();
  if (city.length === 0) {
    self.withOutlet('Error');
    LOG.error('City must no be empty');
    return { error: 'City must no be empty' };
  }

  self.withAttribute('cleanedCity', city);
  self.withOutlet('OK');
}
```

This is the **convergence point** for both paths. It reads from `invocation.attributes.input.city` (not from any specific processor), which is why both `lambdaInput_weatherApi_typescript` and `localRoutineInput_weatherApi_typescript` write to the same attribute key.

The `cleanedCity` attribute is stored on the processor's own scope via `self.withAttribute('cleanedCity', city)`. Downstream processors read it as `invocation.processors.weatherApi_prepare.cleanedCity`.

### 3.8 Processor: weatherApi_restConsumer

**typeId:** `f069aa44-fb5c-469e-a727-705ca7072fee` (REST Consumer Processor)  
**id:** `82d6dd66-6066-435c-a21e-3250e8df95c0`  
**scriptIdentifier:** `weatherApi_restConsumer`  
**position:** x=27, y=3

```json
"customConfig": {
  "httpMethod": "get",
  "server": "https://wttr.in",
  "path": "/{city}"
}
```

The path `/{city}` contains a path parameter. The `{city}` placeholder is filled by `self.withPathParam()` in the `prepareRequest` script.

**Outlets:**

| Name | descriptorId | presentation | target |
|---|---|---|---|
| `Standard` | `6a132916-f955-4dbd-a377-2c3ee21e7fcb` | `primary` | `weatherApi_transform` |
| `Sonstige` | `c95394e3-50c2-4b7c-9529-3149328355e9` | `hidden` | null |

**Script `script.ts`:**

```typescript
export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withPathParam('city', invocation.processors.weatherApi_prepare.cleanedCity)
    .withQueryParam('format', 'j1');
}
```

- `withPathParam('city', ...)` fills the `{city}` placeholder in the path.
- `withQueryParam('format', 'j1')` tells wttr.in to return structured JSON. Without this parameter wttr.in returns an ASCII weather display.

No authentication is needed — wttr.in is a public API.

**Auto-generated `api.d.ts`:**

```typescript
import { MapLike } from '@eip/core';
import { ResponseBody } from './restapi';

export interface _Attributes {
  body: ResponseBody;
  cookies: MapLike<string, string>;
  headers: MapLike<string, string>;
  /** @deprecated use `headers` instead. Will be removed in 26.1 */
  header: MapLike<string, string>;
  statusCode: number;
}
```

### 3.9 Processor: weatherApi_transform

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` (TypeScript Processor)  
**id:** `b068b2d5-d1de-48c9-8f33-9e6c146b60fd`  
**scriptIdentifier:** `weatherApi_transform`  
**position:** x=33, y=3

```json
"customConfig": {
  "outletScriptIds": {
    "Error":   "960d8f62-0488-40e5-b010-b4484a051ba9",
    "Valid":   "a6a8f08c-08ba-480e-ac65-a12e311ad7e8",
    "Invalid": "f55dc620-dc0d-4a12-8062-4811bdaacfcc"
  }
}
```

**Outlets:**

| Name | id | presentation | target |
|---|---|---|---|
| `Standard` | `1520c055-...` | `hidden` | null |
| `Valid` | `a6a8f08c-...` | `default` | null |
| `Invalid` | `f55dc620-...` | `default` | null |
| `Error` | `960d8f62-...` | `default` | null |

All three result outlets end the pipeline for this iteration item.

**Script `script.ts` (complete):**

```typescript
import { Codes } from '@eip/crm-core';
import { LOG } from '@eip/core';

const SCORE_TIERS = [
  [8, Codes.AttributeUserDefinedCodes.WeatherScoreFantastic],
  [5, Codes.AttributeUserDefinedCodes.WeatherScoreGood],
  [3, Codes.AttributeUserDefinedCodes.WeatherScoreTolerable],
  [0, Codes.AttributeUserDefinedCodes.WeatherScoreBad],
] as const;

export function process(invocation: Invocation, self: Self) {
  const statusCode = invocation.processors.weatherApi_restConsumer.statusCode;
  const bodyRaw = invocation.processors.weatherApi_restConsumer.body;
  const body = typeof bodyRaw === 'string' ? JSON.parse(bodyRaw) : bodyRaw;

  if (statusCode !== 200 || !body || !body.current_condition || !body.current_condition[0]) {
    self.withOutlet('Error');
    LOG.error('Wetter-API is not available (HTTP ' + statusCode + ')');
    return { error: 'Wetter-API is not available (HTTP ' + statusCode + ')' };
  }

  const cc = body.current_condition[0];
  const temp = parseInt(cc.temp_C, 10);
  const wind = parseInt(cc.windspeedKmph, 10);
  const humidity = parseInt(cc.humidity, 10);
  const condition = cc.weatherDesc && cc.weatherDesc[0] ? cc.weatherDesc[0].value : 'Unknown';
  const code = parseInt(cc.weatherCode, 10);

  let tScore = 0;
  if (temp >= 20 && temp <= 25) tScore = 4;
  else if ((temp >= 15 && temp < 20) || (temp > 25 && temp <= 28)) tScore = 3;
  else if ((temp >= 10 && temp < 15) || (temp > 28 && temp <= 33)) tScore = 2;
  else if ((temp >= 5 && temp < 10) || (temp > 33 && temp <= 38)) tScore = 1;

  let wScore = wind < 15 ? 3 : wind < 30 ? 2 : wind < 50 ? 1 : 0;

  let cScore = 0;
  if (code === 113) cScore = 3;
  else if (code === 116 || code === 119) cScore = 2;
  else if (code === 122 || code === 143 || code === 248 || code === 260) cScore = 1;

  const total = tScore + wScore + cScore;
  const score = SCORE_TIERS.find(([min]) => total >= min)[1];

  self.withOutlet('Valid');
  return {
    data: {
      temperature: temp,
      wind: wind,
      condition: condition,
      humidity: humidity,
      score: score
    }
  };
}
```

**Scoring algorithm:**

| Dimension | Condition | Points |
|---|---|---|
| Temperature | 20–25°C | 4 |
| Temperature | 15–19°C or 26–28°C | 3 |
| Temperature | 10–14°C or 29–33°C | 2 |
| Temperature | 5–9°C or 34–38°C | 1 |
| Temperature | otherwise | 0 |
| Wind | < 15 km/h | 3 |
| Wind | 15–29 km/h | 2 |
| Wind | 30–49 km/h | 1 |
| Wind | >= 50 km/h | 0 |
| Condition (wttr code) | 113 (Clear/Sunny) | 3 |
| Condition | 116 (Partly cloudy) or 119 (Cloudy) | 2 |
| Condition | 122, 143, 248, 260 (Overcast/Mist/Fog) | 1 |
| Condition | otherwise | 0 |

**Score tiers:**

| Total points | Score |
|---|---|
| >= 8 | `Codes.AttributeUserDefinedCodes.WeatherScoreFantastic` |
| >= 5 | `Codes.AttributeUserDefinedCodes.WeatherScoreGood` |
| >= 3 | `Codes.AttributeUserDefinedCodes.WeatherScoreTolerable` |
| >= 0 | `Codes.AttributeUserDefinedCodes.WeatherScoreBad` |

`Codes.AttributeUserDefinedCodes.WeatherScoreFantastic` is a compile-time constant generated by BSI EIP from the CRM data model. Its runtime value is the UUID of the "Fantastisch" code. The mutation in the second interface stores this UUID in `Y_WEATHER_SCORE_UID`.

The `body` defensively handles both string and parsed-object forms: `wttr.in` returns JSON, but EIP may deliver the body as a pre-parsed object in some runtime configurations.

The result is wrapped in `{ data: { ... } }`. This is the shape that `result.ts` checks: `result?.data != null`. The `Error` outlet returns `{ error: '...' }` instead (no `data` key), causing `result.ts` to fall through to `createLambdaResultErrorDo`.

### 3.10 Processor: weatherApi_localRoutine

**typeId:** `9332ef6a-024d-42d7-91ab-01c3d4121750` (Local Routine Processor) — NEW TYPE  
**id:** `19060db6-65b6-43ce-a3c8-4b1da326dc88`  
**gid:** `b5bfc9fd-d988-4053-bce5-db831ef4dad9`  
**scriptIdentifier:** `weatherApi_localRoutine`  
**position:** x=8, y=8

A **Local Routine** is a named sub-pipeline that can be called synchronously from TypeScript within the same interface. It is not callable from outside the interface (unlike a Lambda). Its primary use is to share a pipeline segment between multiple entry paths within one interface.

```json
"customConfig": {
  "_type": "interfaces.LocalRoutineProcessorConfig",
  "_typeVersion": "interfaces-23.2.001"
}
```

The customConfig is intentionally empty — all behavior is defined via scripts.

**Outlets:**

| Name | descriptorId | executionType | target |
|---|---|---|---|
| `Aufruf` | `885d0c0b-3b59-4c13-85af-a061fd11eb66` | `scoped` | `localRoutineInput_weatherApi_typescript` |

The `Aufruf` outlet fires when the local routine is invoked via `LocalRoutines.weatherApi_localRoutine(input)`.

**Script `types.d.ts`** (user-maintained, not readOnly):

```typescript
export type Input = {
  city: string;
};
export type Output = {
  error?: string;
  data?: {
    temperature: number;
    wind: number;
    condition: string;
    humidity: number;
    score: string;
  }
};
```

This is the typed contract of the Local Routine. `Input` defines what callers must pass; `Output` defines what callers receive back.

**Script `output.ts`:**

```typescript
export function provideOutput(invocation: Invocation): Output {
  return invocation.processors.weatherApi_transform.result;
}
```

Returns whatever `weatherApi_transform` produced as the routine's return value. The caller receives this object synchronously.

**Auto-generated `api.d.ts`** (readOnly):

```typescript
import { Input, Output } from './types';

export interface _Attributes {
  input: Input;
}

export function _localRoutine(input: Input): Output;
```

The `_localRoutine` export is what EIP uses internally. The `interface.d.ts` at the interface level wraps it as `LocalRoutines.weatherApi_localRoutine`.

**Interface-level `interface.d.ts`** (auto-generated, readOnly) exposes:

```typescript
export const LocalRoutines: ILocalRoutines;

interface ILocalRoutines {
  weatherApi_localRoutine: typeof _weatherApi_localRoutineLocalRoutine;
}
```

Scripts import it as:

```typescript
import { LocalRoutines } from '../interface';
// then: LocalRoutines.weatherApi_localRoutine({ city: '...' })
```

### 3.11 Processor: localRoutineInput_weatherApi_typescript

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` (TypeScript Processor)  
**id:** `69a49375-9c91-4f91-8bef-a4361c4e74f0`  
**scriptIdentifier:** `localRoutineInput_weatherApi_typescript`  
**position:** x=14, y=8

Mirrors `lambdaInput_weatherApi_typescript` exactly, but reads the city from the local routine's input instead of the iteration element.

**Outlets:**

| Name | descriptorId | presentation | target |
|---|---|---|---|
| `Standard` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `primary` | `weatherApi_prepare` |

**Script `script.ts`:**

```typescript
export function process(invocation: Invocation, self: Self) {
  const city = invocation.processors.weatherApi_localRoutine.input.city;
  invocation.attributes.input = {
    city: city
  };
}
```

Reads from `weatherApi_localRoutine.input.city` (the `Input` object passed by the caller) and writes to `invocation.attributes.input`. After this, the pipeline merges with the Lambda path at `weatherApi_prepare`.

### 3.12 Processor: restProvider

**typeId:** `01eb3948-507e-4ff4-bb31-525bab2b3e08` (REST Provider Processor) — NEW TYPE  
**id:** `cfa29ee0-722b-454c-8be1-f43b12131fd3`  
**gid:** `260d1e19-c254-4bf6-ad16-ad8380f86283`  
**scriptIdentifier:** `restProvider`  
**position:** x=2, y=15  
**groupId:** `9967043f-1c22-4744-af42-5553ba444843` (group "API")

A **REST Provider** is the inbound HTTP server counterpart to the REST Consumer. It listens for incoming HTTP requests on a registered Web API endpoint and triggers an internal pipeline when a request arrives.

```json
"customConfig": {
  "_type": "interfaces.RestProviderProcessorConfig",
  "_typeVersion": "interfaces-24.2.008",
  "webapiId":   "7a28d2aa-2446-432f-8bce-6d64f0fb01f5",
  "endpointId": "f1f35f8c-6998-4bac-a3b0-6ca3373aae0a",
  "operationId": "f03ac424-d5d1-4ad8-8f2c-a66f64301e85"
}
```

These three IDs reference the Web API definition (see Section 5):
- `webapiId` — the `Weather` Web API header (`GET /weather/...`)
- `endpointId` — the specific endpoint (`weather/{city}`)
- `operationId` — the specific HTTP operation (`GET`)

**Outlets:**

| Name | descriptorId | executionType | target |
|---|---|---|---|
| `Aufruf` | `6891417a-17b6-42a1-850a-da8effff4d13` | `scoped` | `callWeatherApi_customer_typescript` |
| `Abgeschlossen` | `1cbc92dc-5491-43f2-8e80-8e25556052dd` | `async` | null |

The `Aufruf` outlet is `scoped` — it creates a sub-scope per HTTP request. The `Abgeschlossen` outlet is `async` — it fires asynchronously after the response has been sent.

**Auto-generated `api.d.ts`:**

```typescript
export interface _Attributes {
  body: RequestBody;
  queryParams: QueryParams & MapLike<string, string>;
  pathParams: {'city': string} & MapLike<string, string>;
  headers: Headers & MapLike<string, string>;
  cookies: Cookies & MapLike<string, string>;
  policies: MapLike<string, object>;
}
```

The `pathParams: {'city': string}` is derived from the endpoint's path parameter definition.

**Script `response.ts`:**

```typescript
export function provideResponse(invocation: Invocation, self: Self) {
  self
    .withStatus(200)
    .withBody(invocation.processors.callWeatherApi_customer_typescript.result);
}
```

Called after the `Aufruf` scope completes. Sets HTTP status 200 and returns whatever `callWeatherApi_customer_typescript` produced as the response body.

Note: The script file is named `response.ts` (not `script.ts`) — the REST Provider uses `provideResponse` as its function name, analogous to how the Lambda Processor uses `provideOutput`.

### 3.13 Processor: callWeatherApi_customer_typescript

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` (TypeScript Processor)  
**id:** `a6567bd8-3494-44cf-b96d-5041e4f47478`  
**scriptIdentifier:** `callWeatherApi_customer_typescript`  
**position:** x=8, y=15

**Outlets:**

| Name | descriptorId | presentation | target |
|---|---|---|---|
| `Standard` | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | `primary` | null |

**Script `script.ts`:**

```typescript
import { LocalRoutines } from '../interface';

export function process(invocation: Invocation, self: Self) {
  const city = invocation.processors.restProvider.pathParams['city'];
  return LocalRoutines.weatherApi_localRoutine({ city: city });
}
```

Reads the city from the HTTP path parameter and calls the local routine synchronously. The return value of `LocalRoutines.weatherApi_localRoutine()` is the routine's output — either `{ data: { temperature, wind, condition, humidity, score } }` or `{ error: '...' }`.

The `restProvider.response.ts` then reads `callWeatherApi_customer_typescript.result` to send back as the HTTP response body.

---

## 4. Interface 2: Customer Weather Score (Ad-Hoc)

### 4.1 Data Flow

```
customer_temporalTrigger (daily at 01:00) [x=2,y=2]
  └─ Standard ──► customer_searchData [x=8,y=2]
                    (finds up to 20 active customers without weatherScore)
                    └─ Standard ──► customer_iteration [x=14,y=2]
                                     └─ Iteration (scoped, no aggregation) ──► invokeLambda [x=20,y=2]
                                                                                  (calls WetterAbfrage)
                                                                                  └─ Standard ──► customer_mutation [x=26,y=2]
                                                                                                   (writes y_weatherScore)
```

### 4.2 Interface Metadata

```json
{
  "id":             "eac04f7f-e126-4261-819c-da6abc9ca7b3",
  "gid":            "1d99da2a-7aad-4b43-9f72-cc7fedfd6e69",
  "typeId":         "f72f9f76-fb2d-4579-b397-471b2ed4c4e3",
  "name":           "Customer Weather Score",
  "logLevel":       "warn",
  "recordingLevel": "analytics",
  "runtime":        "b",
  "status":         "draft",
  "notes":          "Erstellt von Andrea Adams am 23.06.2026, 15:44"
}
```

`typeId: f72f9f76-fb2d-4579-b397-471b2ed4c4e3` identifies this as an **Ad-Hoc** interface — triggered by an internal event (here: a temporal trigger) rather than an external caller. Ad-Hoc interfaces do not have a Lambda signature.

### 4.3 Processor: customer_temporalTrigger

**typeId:** `406211f6-7b91-4790-b492-feb3e7cac22c` (Trigger Temporal Processor) — NEW TYPE  
**id:** `b0d08f4b-7c39-41f4-b4bb-b580716025e4`  
**scriptIdentifier:** `customer_temporalTrigger`  
**position:** x=2, y=2

```json
"customConfig": {
  "_type": "interfaces.TriggerTemporalProcessorConfig",
  "_typeVersion": "interfaces-22.0.0",
  "temporalConfig": {
    "_type": "bsiscout.TemporalConfig",
    "temporalMode": "periodicity",
    "temporalOption": "interval",
    "periodicityConfig": {
      "_type": "bsiscout.PeriodicityConfig",
      "periodicityType": "daily",
      "temporalOption": "interval",
      "interval": 1,
      "hour": 1,
      "minute": 0
    }
  }
}
```

This fires **once per day at 01:00**. Key fields:

| Field | Value | Meaning |
|---|---|---|
| `periodicityType` | `"daily"` | Frequency class |
| `interval` | `1` | Every 1 day |
| `hour` | `1` | At 01:xx |
| `minute` | `0` | At xx:00 |
| `startDate` | null | Runs immediately upon deployment |
| `endDate` | null | No expiry |

Other `periodicityType` values include `"weekly"`, `"monthly"`, `"yearly"`, and `"minutely"`. For hourly: use `"minutely"` with `interval=60`. For weekly on Monday: `"weekly"` with `weekday: 1`.

**Outlets:**

| Name | descriptorId | executionType | target |
|---|---|---|---|
| `Standard` | `b3f5da65-ba2e-40ab-9983-a4e34544ff28` | `default` | `customer_searchData` |

### 4.4 Processor: customer_searchData

**typeId:** `633d02d2-bda7-450d-a399-277644d39082` (CRM Data Search Processor) — NEW TYPE  
**id:** `9e4263bc-9f5f-4fd9-940a-5badd7402cbf`  
**scriptIdentifier:** `customer_searchData`  
**position:** x=8, y=2

The CRM Data Search processor queries the BSI CRM data model. Its configuration is a `DataModelRelationSelection` structure that specifies what entity to query, what constraints to apply, and what fields to select. This structure is the same format used in BSI CRM search configurations.

**Full selection:**

```json
"selection": {
  "relation":        "crmCustomers",
  "alias":           "crmCustomers",
  "targetType":      "List:Entity:CrmCustomer",
  "maximumRowCount": 20,
  "constraint": {
    "_type": "bsiscout.DataModelAndConstraint",
    "constraints": [
      {
        "_type": "bsiscout.DataModelAttributeConstraint",
        "attribute": "active",
        "fieldType": "Boolean",
        "op": "true"
      },
      {
        "_type": "bsiscout.DataModelRelationConstraint",
        "relation":    "y-weatherScore",
        "targetType":  "Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c",
        "negated":     true
      }
    ]
  },
  "selections": [
    {
      "alias": "id",
      "attribute": "id",
      "fieldType": "Key:Entity:CrmCustomer"
    },
    {
      "alias": "cityName",
      "relation": "preferredPhysicalAddress",
      "selections": [ { "attribute": "cityName", "fieldType": "Text60" } ],
      "targetType": "Entity:CrmPhysicalAddress"
    }
  ]
}
```

The AND constraint means: `active = true AND NOT (y-weatherScore IS NOT NULL)`. The second constraint uses `negated: true` on a relation constraint — this means "does not have a value" for the `y-weatherScore` field.

`maximumRowCount: 20` caps the batch size. In production, if more than 20 customers need updating, subsequent nightly runs will process the next batch.

**Auto-generated `api.d.ts`:**

```typescript
export interface CrmCustomers {
  id: string;       // Key:Entity:CrmCustomer — UUID of the customer
  cityName: string; // resolved from preferredPhysicalAddress.cityName
}

export interface _Attributes {
  data: CrmCustomers[];
}
```

The `data` attribute holds the array of matching customer objects.

**Script `script.ts`:**

```typescript
export function prepareQuery(invocation: Invocation, self: Self) {
}
```

The `prepareQuery` function is empty — all query logic is baked into the `customConfig.selection`. The `Self` interface provides `withLocale()`, `withMaxRowCount()`, and `withRunAsUsername()` for runtime overrides if needed.

**Outlets:**

| Name | descriptorId | presentation | target |
|---|---|---|---|
| `Standard` | `59c636c9-ccce-4650-8460-f7025a556cd2` | `primary` | `customer_iteration` |

### 4.5 Processor: customer_iteration

**typeId:** `21c361ec-5dec-4f13-9767-442db1adb3a3` (Iteration Processor)  
**id:** `e99ee094-d41f-49be-99d6-358254b2fb5e`  
**scriptIdentifier:** `customer_iteration`  
**position:** x=14, y=2

```json
"customConfig": {
  "aggregateResults":   false,
  "aggregateAsListData": false,
  "chunkSize": 1,
  "workerThreads": 1,
  "ignoreNullValues": false
}
```

`aggregateResults: false` — results are NOT collected. This is correct here because the purpose of each iteration is to execute a side effect (CRM mutation), not to produce a return value. There is no `result.ts` script on this iteration.

**Auto-generated `api.d.ts`** (note: no `result` attribute when `aggregateResults=false`):

```typescript
export interface _Attributes {
  element: Flatten<ReturnType<typeof provideData>>;  // one CrmCustomers: { id, cityName }
  index: number;
  // no result: attribute
}
```

**Script `data.ts`:**

```typescript
export function provideData(invocation: Invocation) {
  const r = invocation.processors.customer_searchData.data;
  return r;
}
```

Returns the `CrmCustomers[]` array from the search result.

**Outlets:**

| Name | descriptorId | executionType | target |
|---|---|---|---|
| `Iteration` | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` | `scoped` | `invokeLambda` |
| `Abgeschlossen` | `dd8f5806-3156-4697-97c0-dd069570f2e6` | `default` | null |

### 4.6 Processor: invokeLambda

**typeId:** `9d107af5-8cdc-4138-bbdf-fc5383ece181` (Invoke Lambda Processor) — NEW TYPE  
**id:** `d34177ed-776e-44c2-bc21-6cbc29f85689`  
**scriptIdentifier:** `invokeLambda`  
**position:** x=20, y=2

The **Invoke Lambda** processor calls another Lambda interface by its qualified ID. It is the inter-interface communication mechanism.

```json
"customConfig": {
  "_type": "interfaces.InvokeLambdaProcessorConfig",
  "_typeVersion": "interfaces-24.2.015",
  "qualifiedLambdaId": "interfaces:lambdaProcessor:dc045211-0a34-4ca4-ba94-dbbc27b50d21:ffc77303-8574-4206-b7e5-ec9be108af21"
}
```

**qualifiedLambdaId format:**

```
interfaces:lambdaProcessor:{lambdaProcessor_gid}:{interface_gid}
```

- `interfaces` — fixed prefix
- `lambdaProcessor` — fixed segment
- `dc045211-0a34-4ca4-ba94-dbbc27b50d21` — the `gid` of the `weatherApi_lambda` processor in the WetterAbfrage interface
- `ffc77303-8574-4206-b7e5-ec9be108af21` — the `gid` of the WetterAbfrage interface itself

This means the `qualifiedLambdaId` is stable across environments (gid never changes on import) and survives re-imports.

**Outlets:**

| Name | descriptorId | presentation | target |
|---|---|---|---|
| `Standard` | `cce40eff-3c00-45fc-b569-74c5eb3710b7` | `primary` | `customer_mutation` |

**Script `prepare.ts`:**

```typescript
export function prepare(invocation: Invocation, self: Self) {
  const city = invocation.processors.customer_iteration.element.cityName;
  self.withInput({ city: city });
}
```

`prepare` (not `process`) is the function name for Invoke Lambda scripts. `self.withInput({ city: city })` provides the Lambda's `LambdaInput` object. The Invoke Lambda processor wraps the input into `LambdaInput[]` internally (the Lambda always receives an array).

**Auto-generated `api.d.ts`:**

```typescript
export interface _Attributes {
  error: LambdaError[];
  data: LambdaOutput[];
}

export interface LambdaError {
  displayMessage: string;
  correlationId: string;
}

export interface LambdaOutput {
  temperature: number;
  wind: number;
  condition: string;
  humidity: number;
  score: string;
}
```

`data[0]` is the first (and only) result because `self.withInput(...)` sends exactly one item. The mutation reads `invokeLambda.data[0].score`.

**Auto-generated `definition.d.ts`:**

```typescript
export interface Self {
  withRunAsUsername(username: string): Self;
  withInput(input: LambdaInput): Self;
  withInputs(input: LambdaInput[]): Self;
}

export interface LambdaInput {
  city: string;
}
```

`withInput` is for sending a single item; `withInputs` is for sending an array.

### 4.7 Processor: customer_mutation

**typeId:** `cf9ee65c-a489-4250-b76a-7b1741868c0f` (CRM Mutation Processor) — NEW TYPE  
**id:** `45011627-7aed-48a8-af20-de117be676f5`  
**scriptIdentifier:** `customer_mutation`  
**position:** x=26, y=2

```json
"customConfig": {
  "_type": "interfaces.CrmMutationProcessorConfig",
  "_typeVersion": "interfaces-24.2.010"
}
```

The `customConfig` is empty — all mutation logic is in the `data.ts` script.

**Outlets:**

| Name | descriptorId | presentation | target |
|---|---|---|---|
| `Standard` | `6c0f1af6-2051-4fd5-947b-398c59418229` | `default` | null |
| `Fehler` | `f3aac37d-ce3b-45d0-8c52-b157854d2e8f` | `default` | null |

`Fehler` is the mutation error outlet. In this example it is unconnected — mutation errors are logged but not explicitly handled. In production interfaces, you may want to connect `Fehler` to a TypeScript processor that logs or reports the failure.

**Script `data.ts`** (function name is `prepareMutations`, not `process`):

```typescript
import { Mutations } from '@eip/crm-mutation';

export function prepareMutations(invocation: Invocation, self: Self) {
  const customerKey = invocation.processors.customer_iteration.element.id;
  const score = invocation.processors.invokeLambda.data[0].score;
  self.withMutations(Mutations.create('CrmCustomerUpdate', {
    customerKey: customerKey,
    y_weatherScore: score
  }));
}
```

- `Mutations.create('CrmCustomerUpdate', fields)` — creates a mutation object. `CrmCustomerUpdate` is the mutation type identifier; it determines which fields are accepted.
- `customerKey` — the UUID of the CRM customer record. Required by `CrmCustomerUpdate` to identify which record to update.
- `y_weatherScore` — the custom field identifier (matches the `dataFieldId` in the field definition, using underscore instead of hyphen for mutation field names).
- `self.withMutations(...)` — queues the mutation for execution. Multiple mutations can be queued in one call.

**`definition.d.ts`** (auto-generated):

```typescript
export interface Self {
  withMutations(mutations: any): Self;
  withModifiedByUsername(username: string): Self;
  withRunAsUsername(username: string): Self;
}
```

**Auto-generated `api.d.ts`:**

```typescript
export interface MutationResponse {
  requestRef: string;
  keyMappings: MapLike<string, string>;
  status: 'ok' | 'error' | 'cancelled';
  transactionRef: string;
  errorCode: string;
  errorMessage: string;
}

export interface _Attributes {
  response: MutationResponse;
}
```

The `response.status` can be checked downstream (if `Fehler` is connected) to distinguish transient errors from validation failures.

---

## 5. Web API Definition

The Web API definition consists of two JSON files that must exist in BSI EIP before the interface can be imported (or must be imported as part of the same package).

### 5.1 Header: Weather

**File:** `02-interfaces/webapis/headers/Weather-7a28d2aa-2446-432f-8bce-6d64f0fb01f5.json`

```json
{
  "_type": "interfaces.WebapiHeader",
  "id":              "7a28d2aa-2446-432f-8bce-6d64f0fb01f5",
  "name":            "Weather",
  "basePath":        "weather",
  "scriptIdentifier": "weather",
  "projectId":       "4ca1cf10-6a17-4389-b979-a41cbfe97167"
}
```

The `basePath: "weather"` sets the URL base. All endpoints under this API are served at `{eipBaseUrl}/weather/...`.

### 5.2 Endpoint: weather/{city} GET

**File:** `02-interfaces/webapis/endpoints/weather{city}_-_GET-f1f35f8c-6998-4bac-a3b0-6ca3373aae0a.json`

```json
{
  "_type": "interfaces.WebapiEndpoint",
  "id": "f1f35f8c-6998-4bac-a3b0-6ca3373aae0a",
  "webapiId": "7a28d2aa-2446-432f-8bce-6d64f0fb01f5",
  "path": {
    "basePath": "weather",
    "endpointPath": "{city}"
  },
  "pathParameters": [
    { "parameter": "city", "type": "string" }
  ],
  "operations": [
    {
      "id": "f03ac424-d5d1-4ad8-8f2c-a66f64301e85",
      "httpMethod": "get",
      "parameterDescriptions": "export type Cookies = Record<string, string>;\nexport type Headers = Record<string, string>;\nexport type QueryParams = Record<string, string>;\nexport type RequestBody = any;\nexport type ResponseBody = any;"
    }
  ]
}
```

The `parameterDescriptions` is a TypeScript type definition string that becomes the basis for the REST Provider's `api.d.ts`. It defines `pathParams.city` as `string` (via the path parameter declaration) and leaves other types as loose.

Full request URL for a request to this endpoint:

```
GET {eipBaseUrl}/web/weather/Zurich
```

The REST Provider's `api.d.ts` exposes `invocation.processors.restProvider.pathParams['city']` as `string`.

---

## 6. TypeScript Imports: `@eip/crm-core` and `@eip/crm-mutation`

These two packages are new compared to the IBAN validation example.

### 6.1 `import { Codes } from '@eip/crm-core'`

Used in `weatherApi_transform/script.ts`:

```typescript
import { Codes } from '@eip/crm-core';

Codes.AttributeUserDefinedCodes.WeatherScoreFantastic
Codes.AttributeUserDefinedCodes.WeatherScoreGood
Codes.AttributeUserDefinedCodes.WeatherScoreTolerable
Codes.AttributeUserDefinedCodes.WeatherScoreBad
```

Each `Codes.AttributeUserDefinedCodes.*` constant is a string UUID. The value is the UUID of the corresponding CRM code value. These constants are generated by BSI EIP from the CRM data model — specifically from the `scriptIdentifier` fields of the CrmCode objects in `01-crm/codes/`.

The scriptIdentifier `AttributeUserDefinedCodes.WeatherScoreFantastic` becomes `Codes.AttributeUserDefinedCodes.WeatherScoreFantastic` in the TypeScript API. The namespace `AttributeUserDefinedCodes` is the fixed namespace for user-defined (custom) codes in BSI CRM.

Using `Codes.*` constants instead of hardcoded UUIDs is essential: code UUIDs differ between environments, so hardcoding would break on import. The constants resolve to the correct UUID at runtime in each environment.

### 6.2 `import { Mutations } from '@eip/crm-mutation'`

Used in `customer_mutation/data.ts`:

```typescript
import { Mutations } from '@eip/crm-mutation';

Mutations.create('CrmCustomerUpdate', {
  customerKey: customerKey,
  y_weatherScore: score
})
```

`Mutations.create(mutationType, fields)` creates a mutation descriptor object that `self.withMutations()` submits for execution.

The mutation type `CrmCustomerUpdate` defines which fields may be set. To discover available fields for a mutation type, query:

```
GET {eipBaseUrl}/l/cpd-tools/mutationtypes/CrmCustomerUpdate
```

This returns the full field schema. Custom fields use the `y_` prefix with underscore (not hyphen). The BSI CRM convention maps the field identifier `y-weatherScore` (hyphen, as used in the data model) to `y_weatherScore` (underscore) in mutation field names.

---

## 7. Complete TypeScript Script Inventory

### WetterAbfrage interface

| processorId | scriptName | readOnly | user-maintained | Purpose |
|---|---|---|---|---|
| null | `attributes.d.ts` | false | yes | Declares `input.city` shared attribute |
| null | `interface.d.ts` | true | no | Auto-generated: assembles all processor attributes, declares `LocalRoutines` |
| null | `testDefinition.d.ts` | true | no | Auto-generated: TestDriver API for test scripts |
| `6e2cf0d0` (weatherApi_lambda) | `api.d.ts` | true | no | LambdaInput, LambdaOutput, callingUserId |
| `6e2cf0d0` (weatherApi_lambda) | `output.ts` | false | yes | Returns `iteration.result` |
| `36325f71` (weatherApi_iteration) | `api.d.ts` | true | no | element, index, result attributes |
| `36325f71` (weatherApi_iteration) | `data.ts` | false | yes | Returns `lambda.input` |
| `36325f71` (weatherApi_iteration) | `result.ts` | false | yes | Returns `transform.result.data` or `LambdaResultError` |
| `89c96799` (lambdaInput_ts) | `api.d.ts` | true | no | result attribute |
| `89c96799` (lambdaInput_ts) | `attributes.d.ts` | false | yes | Empty |
| `89c96799` (lambdaInput_ts) | `definition.d.ts` | true | no | Self interface |
| `89c96799` (lambdaInput_ts) | `script.ts` | false | yes | Sets `attributes.input.city` from iteration element |
| `ccc16f3b` (weatherApi_prepare) | `api.d.ts` | true | no | result and cleanedCity attributes |
| `ccc16f3b` (weatherApi_prepare) | `attributes.d.ts` | false | yes | Declares `cleanedCity: String` |
| `ccc16f3b` (weatherApi_prepare) | `definition.d.ts` | true | no | `Outlet = 'Error' \| 'OK'`, Self |
| `ccc16f3b` (weatherApi_prepare) | `script.ts` | false | yes | City validation, routing to OK or Error |
| `82d6dd66` (weatherApi_restConsumer) | `api.d.ts` | true | no | body, statusCode, headers |
| `82d6dd66` (weatherApi_restConsumer) | `definition.d.ts` | true | no | Self with withPathParam, withQueryParam |
| `82d6dd66` (weatherApi_restConsumer) | `restapi.d.ts` | false | yes | PathParams, QueryParams type stubs (all `any`) |
| `82d6dd66` (weatherApi_restConsumer) | `script.ts` | false | yes | `prepareRequest`: path param + format=j1 |
| `b068b2d5` (weatherApi_transform) | `api.d.ts` | true | no | result attribute |
| `b068b2d5` (weatherApi_transform) | `attributes.d.ts` | false | yes | Empty |
| `b068b2d5` (weatherApi_transform) | `definition.d.ts` | true | no | `Outlet = 'Error' \| 'Invalid' \| 'Valid'`, Self |
| `b068b2d5` (weatherApi_transform) | `script.ts` | false | yes | Scoring algorithm, CrmCode reference via `Codes.*` |
| `19060db6` (weatherApi_localRoutine) | `api.d.ts` | true | no | input attribute, `_localRoutine` function export |
| `19060db6` (weatherApi_localRoutine) | `types.d.ts` | false | yes | Input and Output type contracts |
| `19060db6` (weatherApi_localRoutine) | `output.ts` | false | yes | Returns `transform.result` |
| `69a49375` (localRoutineInput_ts) | `api.d.ts` | true | no | result attribute |
| `69a49375` (localRoutineInput_ts) | `attributes.d.ts` | false | yes | Empty |
| `69a49375` (localRoutineInput_ts) | `definition.d.ts` | true | no | Self interface |
| `69a49375` (localRoutineInput_ts) | `script.ts` | false | yes | Sets `attributes.input.city` from localRoutine input |
| `cfa29ee0` (restProvider) | `api.d.ts` | true | no | pathParams.city, headers, etc. |
| `cfa29ee0` (restProvider) | `definition.d.ts` | true | no | Self with withStatus, withBody |
| `cfa29ee0` (restProvider) | `response.ts` | false | yes | Sets HTTP 200 + body from callWeatherApi result |
| `a6567bd8` (callWeatherApi_ts) | `api.d.ts` | true | no | result attribute |
| `a6567bd8` (callWeatherApi_ts) | `attributes.d.ts` | false | yes | Empty |
| `a6567bd8` (callWeatherApi_ts) | `definition.d.ts` | true | no | Self interface |
| `a6567bd8` (callWeatherApi_ts) | `script.ts` | false | yes | Reads pathParams.city, calls LocalRoutines |

### Customer Weather Score interface

| processorId | scriptName | readOnly | Purpose |
|---|---|---|---|
| null | `attributes.d.ts` | false | Empty interface-level attributes |
| null | `interface.d.ts` | true | Auto-generated processor attribute assembly |
| null | `testDefinition.d.ts` | true | Auto-generated TestDriver API |
| `9e4263bc` (customer_searchData) | `api.d.ts` | true | CrmCustomers interface: id, cityName |
| `9e4263bc` (customer_searchData) | `definition.d.ts` | true | Self with withLocale, withMaxRowCount, withRunAsUsername |
| `9e4263bc` (customer_searchData) | `script.ts` | false | `prepareQuery` — empty body |
| `e99ee094` (customer_iteration) | `api.d.ts` | true | element (CrmCustomers), index — no result |
| `e99ee094` (customer_iteration) | `data.ts` | false | Returns `customer_searchData.data` |
| `d34177ed` (invokeLambda) | `api.d.ts` | true | error[], data[] (LambdaOutput with score) |
| `d34177ed` (invokeLambda) | `definition.d.ts` | true | Self with withInput, withInputs, withRunAsUsername |
| `d34177ed` (invokeLambda) | `prepare.ts` | false | `prepare`: sets withInput({city}) from iteration element |
| `45011627` (customer_mutation) | `api.d.ts` | true | MutationResponse attribute |
| `45011627` (customer_mutation) | `definition.d.ts` | true | Self with withMutations, withModifiedByUsername, withRunAsUsername |
| `45011627` (customer_mutation) | `data.ts` | false | `prepareMutations`: creates CrmCustomerUpdate with score |

---

## 8. Adaptation Guide

### Pattern: Nightly CRM batch enrichment via external API

Follow these steps to build a new interface pair that enriches a CRM entity nightly using an external REST API.

**Step 1: CRM data model (Stage 1 ZIP)**

1. Define a custom code list (if the new field is an enum). Set `scriptIdentifier` to `AttributeUserDefinedCodes.YourCodeXxx` for each value.
2. Create a custom field on the target entity using `dataFieldId: "CrmEntity/bsiscout.DataModelRelationId:y-yourField"`. Set `typeId` to reference your code list or a primitive type.
3. Export as a `crm` product stage in the multi-index.

**Step 2: Lambda for data fetching (similar to WetterAbfrage)**

Copy the WetterAbfrage interface structure:
1. Lambda processor → define signature (inputs: whatever identifiers the external API needs; outputs: the enrichment data + score code if applicable).
2. Iteration → same settings (`aggregateResults=true`, `chunkSize=1`, `workerThreads=1`).
3. `lambdaInput_ts` → write `invocation.attributes.input` from the iteration element.
4. `prepare` → validate and clean the input, store cleaned values as attributes, route OK/Error.
5. REST Consumer → configure `server`, `path`, `httpMethod`; use `withPathParam` or `withQueryParam` as needed.
6. `transform` → parse the response, score if needed, return `{ data: { ...fields } }` on Valid.
7. Local Routine → same `types.d.ts` shape as Lambda outputs, `output.ts` returns `transform.result`.
8. `localRoutineInput_ts` → same pattern as `lambdaInput_ts` but reads from `localRoutine.input`.
9. REST Provider → link to your Web API definition via `webapiId`, `endpointId`, `operationId`.
10. `callWeatherApi_ts` → reads path/query params, calls `LocalRoutines.yourRoutine(...)`.

**Step 3: Ad-Hoc for batch update (similar to Customer Weather Score)**

1. **Temporal Trigger**: Set `periodicityType`, `hour`, `minute`, `interval`.
2. **CRM Data Search**: Change `relation` to your entity, `targetType`, `selections` (id + lookup fields), `constraint` (active + NOT hasField). Set `maximumRowCount` to a safe batch limit (20–100 depending on API rate limits).
3. **Iteration**: Set `aggregateResults: false` (no result collection needed for side-effect pipelines).
4. **Invoke Lambda**: Update `qualifiedLambdaId` to `interfaces:lambdaProcessor:{lambdaProcessor_gid}:{interface_gid}`. Get the gids from the Lambda interface JSON.
5. **CRM Mutation**: Use `Mutations.create('CrmYourEntityUpdate', { entityKey, y_yourField: value })`.

**Step 4: Discovering mutation field names**

```
GET {eipBaseUrl}/l/cpd-tools/mutationtypes/CrmCustomerUpdate
```

Returns all accepted fields for that mutation type. Custom field identifiers use underscore (`y_fieldName`), even if the data model uses hyphen (`y-fieldName`).

**Step 5: qualifiedLambdaId format**

The format is:
```
interfaces:lambdaProcessor:{lambdaProcessor.gid}:{interface.gid}
```

Both `gid` values are in the Lambda interface JSON: `interface.gid` is the top-level `gid` field; `lambdaProcessor.gid` is the `gid` of the processor whose `typeId` is `ec06bfe3-faab-4c2c-83bc-8420789d3479`.

---

## 9. Post-Import Setup

This ZIP requires no environment variables — `wttr.in` is a public API. After import:

1. **Verify CRM data model**: Check that `Wetter Score` appears in the CRM code list browser and that `y-weatherScore` (Weather Score) appears on the CrmCustomer data model.
2. **Verify Web API**: Open BSI EIP → Web APIs and confirm the `Weather` API with endpoint `GET /weather/{city}` is registered.
3. **Test WetterAbfrage**: Run a manual Lambda invocation with `[{ city: "Zurich" }]`. Expect a result with temperature, wind, condition, humidity, and a score UUID.
4. **Test the REST endpoint**: `GET {eipBaseUrl}/web/weather/Zurich`. Expect JSON with the same fields.
5. **Test Customer Weather Score**: Trigger the Ad-Hoc interface manually for the first run. Check that customer records receive a value in their `Wetter Score` field.
6. **Set live**: Switch both interfaces from `draft` to `live` when ready for production.
7. **Monitor first nightly run**: At 01:00, check the execution log for the `Customer Weather Score` interface. Expect up to 20 customers updated per run.

---

## 10. Key UUID Reference

### WetterAbfrage interface

| Entity | UUID |
|---|---|
| Interface `id` | `c9781b3c-4ac1-472b-b0ee-b69c90fb200d` |
| Interface `gid` | `ffc77303-8574-4206-b7e5-ec9be108af21` |
| Signature `id` | `1a70a628-af57-4d50-b9d9-215cf3dbba69` |
| Project `id` | `4ca1cf10-6a17-4389-b979-a41cbfe97167` |
| Processor: weatherApi_lambda `id` | `6e2cf0d0-a4f3-41ec-9f8b-0a0d3ff0647e` |
| Processor: weatherApi_lambda `gid` | `dc045211-0a34-4ca4-ba94-dbbc27b50d21` |
| Processor: weatherApi_iteration `id` | `36325f71-2072-4f46-accb-e7ee76ea8cb7` |
| Processor: lambdaInput_weatherApi_typescript `id` | `89c96799-1bb1-4e41-a1ed-30ef5c291de7` |
| Processor: weatherApi_prepare `id` | `ccc16f3b-67af-40e3-8298-be8ab3bda42c` |
| Processor: weatherApi_restConsumer `id` | `82d6dd66-6066-435c-a21e-3250e8df95c0` |
| Processor: weatherApi_transform `id` | `b068b2d5-d1de-48c9-8f33-9e6c146b60fd` |
| Processor: weatherApi_localRoutine `id` | `19060db6-65b6-43ce-a3c8-4b1da326dc88` |
| Processor: localRoutineInput_weatherApi_typescript `id` | `69a49375-9c91-4f91-8bef-a4361c4e74f0` |
| Processor: restProvider `id` | `cfa29ee0-722b-454c-8be1-f43b12131fd3` |
| Processor: callWeatherApi_customer_typescript `id` | `a6567bd8-3494-44cf-b96d-5041e4f47478` |
| Outlet: weatherApi_prepare OK `id` | `1cd2b9d5-5864-4534-bbd3-6ab040460fcb` |
| Outlet: weatherApi_prepare Error `id` | `7ab866da-2663-41f0-9cb1-78bd02f75cff` |
| Outlet: weatherApi_transform Valid `id` | `a6a8f08c-08ba-480e-ac65-a12e311ad7e8` |
| Outlet: weatherApi_transform Invalid `id` | `f55dc620-dc0d-4a12-8062-4811bdaacfcc` |
| Outlet: weatherApi_transform Error `id` | `960d8f62-0488-40e5-b010-b4484a051ba9` |
| Web API header `id` | `7a28d2aa-2446-432f-8bce-6d64f0fb01f5` |
| Web API endpoint `id` | `f1f35f8c-6998-4bac-a3b0-6ca3373aae0a` |
| Web API operation `id` | `f03ac424-d5d1-4ad8-8f2c-a66f64301e85` |

### Customer Weather Score interface

| Entity | UUID |
|---|---|
| Interface `id` | `eac04f7f-e126-4261-819c-da6abc9ca7b3` |
| Interface `gid` | `1d99da2a-7aad-4b43-9f72-cc7fedfd6e69` |
| Processor: customer_temporalTrigger `id` | `b0d08f4b-7c39-41f4-b4bb-b580716025e4` |
| Processor: customer_searchData `id` | `9e4263bc-9f5f-4fd9-940a-5badd7402cbf` |
| Processor: customer_iteration `id` | `e99ee094-d41f-49be-99d6-358254b2fb5e` |
| Processor: invokeLambda `id` | `d34177ed-776e-44c2-bc21-6cbc29f85689` |
| Processor: customer_mutation `id` | `45011627-7aed-48a8-af20-de117be676f5` |

### CRM data model

| Entity | UUID / identifier |
|---|---|
| Wetter_Score code list `id` (file name UUID) | `9ac81c27-0a86-459c-ba62-482fee56739c` |
| Code: Fantastisch `scriptIdentifier` | `AttributeUserDefinedCodes.WeatherScoreFantastic` |
| Code: Gut `scriptIdentifier` | `AttributeUserDefinedCodes.WeatherScoreGood` |
| Code: Erträglich `scriptIdentifier` | `AttributeUserDefinedCodes.WeatherScoreTolerable` |
| Code: Schlecht `scriptIdentifier` | `AttributeUserDefinedCodes.WeatherScoreBad` |
| Custom field `dataFieldId` | `CrmCustomer/bsiscout.DataModelRelationId:y-weatherScore` |
| Custom field DB column | `Y_WEATHER_SCORE_UID` |
