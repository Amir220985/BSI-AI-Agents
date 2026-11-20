# BSI EIP Processor Types Catalog

Complete reference for all BSI EIP processor types: Java class names, `_type` values, `typeId` UUIDs, and configuration details.

---

## Complete Processor Type UUID Table

| Processor Name (Display) | Java Class | `_type` value | typeId UUID | Category |
|---|---|---|---|---|
| Lambda | CrmLambdaProcessor | `interfaces.CrmLambdaProcessorConfig` | `ec06bfe3-faab-4c2c-83bc-8420789d3479` | CRM |
| Iteration | IterationProcessor | `interfaces.IterationProcessorConfig` | `21c361ec-5dec-4f13-9767-442db1adb3a3` | Base |
| TypeScript | TypeScriptProcessor | `interfaces.TypeScriptProcessorConfig` | `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` | Base |
| JavaScript | JavaScriptProcessor | `interfaces.JavaScriptProcessorConfig` | `6b281cf3-c0e1-4d77-b6bf-3cf70a0eb537` | Base |
| REST Consumer | RestConsumerProcessor | `interfaces.RestConsumerProcessorConfig` | `f069aa44-fb5c-469e-a727-705ca7072fee` | REST |
| REST Provider | RestProviderProcessor | `interfaces.RestProviderProcessorConfig` | `01eb3948-507e-4ff4-bb31-525bab2b3e08` | REST |
| SCIM Provider | ScimProviderProcessor | `interfaces.ScimProviderProcessorConfig` | `9cf346bd-627b-4c7c-97c3-6498b3611492` | REST |
| SMTP | SmtpProcessor | `interfaces.SmtpProcessorConfig` | `a9f20929-adae-4f0d-85d0-6591e486ddf8` | Mail |
| IMAP | ImapProcessor | `interfaces.ImapProcessorConfig` | `c95c50cb-7b55-475b-8e1a-53188147a080` | Mail |
| Graph Mail | GraphMailProcessor | `interfaces.GraphMailProcessorConfig` | `d58c487f-30d2-493b-91fe-7cb96ed287e0` | Mail |
| Kafka Consumer | KafkaConsumerProcessor | `interfaces.KafkaConsumerProcessorConfig` | `8b7b0d2c-6dba-4ba0-8752-b6a86de5c397` | Messaging |
| Kafka Producer | KafkaProducerProcessor | `interfaces.KafkaProducerProcessorConfig` | `04129aae-b6e3-4685-b49a-50dfd90cdd26` | Messaging |
| Solace Consumer | SolaceConsumerProcessor | `interfaces.SolaceConsumerProcessorConfig` | `5f450ada-9b5b-41c1-a736-36f1ff179076` | Messaging |
| Solace Producer | SolaceProducerProcessor | `interfaces.SolaceProducerProcessorConfig` | `7ad37f19-31ed-4830-a797-67a5ded3dced` | Messaging |
| MOM Publisher | MomPublisherProcessor | `interfaces.MomPublisherProcessorConfig` | `7bd2b45b-2532-4c9b-a656-8624630df3e0` | Messaging |
| MOM Subscribe | MomSubscribeProcessor | `interfaces.MomSubscribeCustomConfig` | `5cd9bb88-a629-4007-bc19-a7225aa334f8` | Messaging |
| Pulsar Consumer | PulsarConsumerProcessor | `interfaces.PulsarConsumerCustomConfig` | `a8e45adf-2c5d-44af-92a1-bb09a37ea789` | Messaging |
| SQL | SqlProcessor | `interfaces.SqlProcessorConfig` | `0d8a1379-95b8-4bc6-83bb-1d2b2a7a5425` | Data |
| CSV | CsvProcessor | `interfaces.CsvProcessorCustomConfig` | `1245030d-3b73-42fb-a7a8-3ed91b729303` | Data |
| S3 | S3Processor | `interfaces.S3CustomConfig` | `4e3315f8-0597-42a6-957c-33e97eea8016` | Data |
| File Repository | FilerepositoryProcessor | `interfaces.FilerepositoryProcessorCustomConfig` | `5dd937a9-701c-496a-a380-f17fad15693a` | Data |
| LDAP | LdapProcessor | `interfaces.LdapProcessorConfig` | `6a538478-940f-4b89-a6b9-eb5c2ec46e30` | Base |
| Retry | RetryProcessor | `interfaces.RetryProcessorConfig` | `d34c6758-170f-4274-b133-ceada394e678` | Base |
| Try/Catch | TryCatchProcessor | `interfaces.TryCatchProcessorConfig` | `a00c8c2c-42f9-46e0-96e6-5cc02c670da9` | Base |
| Parallelize | ParallelizeProcessor | `interfaces.ParallelizeProcessorConfig` | `39f8a783-0d6f-4937-ab2a-438abc5fac81` | Base |
| Routine | RoutineProcessor | `interfaces.RoutineProcessorConfig` | `8f97036a-6c89-458f-a28a-b0f10b0addd4` | Base |
| Local Routine | LocalRoutineProcessor | `interfaces.LocalRoutineProcessorConfig` | `9332ef6a-024d-42d7-91ab-01c3d4121750` | Base |
| Invoke Lambda | InvokeLambdaProcessor | `interfaces.InvokeLambdaProcessorConfig` | `9d107af5-8cdc-4138-bbdf-fc5383ece181` | CRM |
| CRM Mutation | CrmMutationProcessor | `interfaces.CrmMutationProcessorConfig` | `cf9ee65c-a489-4250-b76a-7b1741868c0f` | CRM |
| CRM Search | CrmDataModelSearchProcessor | `interfaces.CrmDataModelSearchProcessorConfig` | `633d02d2-bda7-450d-a399-277644d39082` | CRM |
| Insign | InsignProcessor | `interfaces.InsignProcessorConfig` | `659c27ec-7084-44e9-aae4-818f7174afe5` | CRM |
| Microsoft Teams | MicrosoftTeamsProcessor | `interfaces.MicrosoftTeamsCustomConfig` | `b9b6cbd6-126b-489d-b982-6e7a78c723ea` | CRM |
| Snapview | SnapviewProcessor | `interfaces.SnapviewCustomConfigDo` | `b07f7518-410e-4ec1-b2fc-46aab4f80087` | CRM |
| Audience | AudienceProcessor | `interfaces.AudienceProcessorConfig` | `fa32cd48-4de8-4391-b989-4ac2ad28e4c7` | Analytics |
| Trigger (Manual) | TriggerManualProcessor | `interfaces.TriggerManualProcessorConfig` | `b4447959-8495-4a20-83e1-e3e0384c5935` | Trigger |
| Trigger (Temporal) | TriggerTemporalProcessor | `interfaces.TriggerTemporalProcessorConfig` | `406211f6-7b91-4790-b492-feb3e7cac22c` | Trigger |
| Placeholder (Data) | PlaceholderDataProcessor | `interfaces.PlaceholderProcessorConfig` | `e884ac9e-2c80-437b-9f41-0a566591524e` | Prototyping |
| Placeholder (Invocation) | PlaceholderInvocationProcessor | `interfaces.PlaceholderInvocationProcessorConfig` | `6d2cbf33-c136-42d9-902d-1d598c7384d7` | Prototyping |
| Placeholder (Logic) | PlaceholderLogicProcessor | `interfaces.PlaceholderProcessorConfig` | `da14aadd-7024-4046-aebc-926091c9a196` | Prototyping |
| Placeholder (Target) | PlaceholderTargetProcessor | `interfaces.PlaceholderProcessorConfig` | `81cfe197-532d-4159-a37f-70c1cb7a233a` | Prototyping |

---

## Detailed Configuration for Key Processors

These are the processors used in most BSI EIP interfaces. Each section documents the full `customConfig` structure, required scripts, and outlet wiring.

---

### 1. Lambda Processor (CRM Lambda — Entry Point)

**typeId:** `ec06bfe3-faab-4c2c-83bc-8420789d3479`
**`_type`:** `interfaces.CrmLambdaProcessorConfig`

Every BSI EIP interface starts with exactly one Lambda processor. It defines the public contract (inputs/outputs) of the interface and acts as the entry point for all invocations.

#### customConfig

```json
{
  "_type": "interfaces.CrmLambdaProcessorConfig",
  "_typeVersion": "interfaces-23.2.019",
  "signature": {
    "_type": "bsiscout.Signature",
    "_typeVersion": "bsiscout-24.1.001",
    "id": "{signature-uuid}",
    "name": {
      "en": "My Lambda",
      "und": "Mein Lambda"
    },
    "description": {
      "en": "Description of what this interface does.",
      "und": "Beschreibung, was diese Schnittstelle macht."
    },
    "inputTypeId": "List:Dyn:LambdaInput",
    "outputTypeId": "List:Dyn:LambdaOutput",
    "inputs": [
      {
        "_type": "bsiscout.SignatureField",
        "id": "{field-uuid}",
        "name": "iban",
        "label": { "en": "IBAN", "und": "IBAN" },
        "typeId": "Text",
        "mandatory": true
      }
    ],
    "outputs": [
      {
        "_type": "bsiscout.SignatureField",
        "id": "{field-uuid}",
        "name": "isValid",
        "label": { "en": "Is Valid", "und": "Ist gueltig" },
        "typeId": "Boolean",
        "mandatory": false
      }
    ]
  }
}
```

#### Outlets

| Outlet Name | Role | Wiring |
|---|---|---|
| `Aufruf` | scoped — fires for each call | connect to first processing step (usually Iteration) |
| `Abgeschlossen` | default — fires when all done | connect to end of interface or leave unconnected |

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `output.ts` | `provideOutput(invocation)` | Returns the final output array to the caller |

**Typical `output.ts`:**
```typescript
import { Invocation } from '../interface';

export function provideOutput(invocation: Invocation) {
  return invocation.processors.iteration.result;
}
```

#### Auto-generated type files (`api.d.ts`)

The Lambda processor's `api.d.ts` is generated from the signature fields:
```typescript
export type Input = LambdaInput[];
export type Output = LambdaOutput[];

export interface _Attributes {
  input: Input;
  callingUserId: string;
}

export interface LambdaInput {
  iban: string;
  // ... one field per signature.inputs entry
}

export interface LambdaOutput {
  isValid: boolean;
  // ... one field per signature.outputs entry
}
```

---

### 2. Iteration Processor

**typeId:** `21c361ec-5dec-4f13-9767-442db1adb3a3`
**`_type`:** `interfaces.IterationProcessorConfig`

Iterates over an array of items (usually the lambda input list), processing each one individually. Collects per-item results into an output array.

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

**Field meanings:**

| Field | Type | Default | Description |
|---|---|---|---|
| `aggregateResults` | boolean | `true` | Collect per-item results into a final array |
| `aggregateAsListData` | boolean | `false` | Flatten nested arrays in the result |
| `chunkSize` | integer | `1` | Number of items per processing chunk |
| `workerThreads` | integer | `1` | Parallel worker threads (set >1 for parallel processing) |
| `ignoreNullValues` | boolean | `false` | Skip null items in the input array |

#### Outlets

| Outlet Name | Role | Wiring |
|---|---|---|
| `Iteration` | scoped — fires once per item | connect to first processing step |
| `Abgeschlossen` | default — fires when all items processed | connect to Lambda's `Abgeschlossen` or end |

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `data.ts` | `provideData(invocation)` | Returns the array to iterate over |
| `result.ts` | `provideResult(invocation)` | Returns the result for the current item |

**Typical `data.ts`:**
```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.lambda.input;
}
```

**Typical `result.ts`:**
```typescript
import { Invocation } from '../interface';

export function provideResult(invocation: Invocation) {
  // Return the result from the last meaningful processor in the chain
  return invocation.processors.transform.result;
}
```

#### Auto-generated type file (`api.d.ts`)

```typescript
import { Flatten } from '@eip/core';
import { provideData } from './data';
import { provideResult } from './result';

export interface _Attributes {
  element: Flatten<ReturnType<typeof provideData>>;
  index: number;
  result: ReturnType<typeof provideResult>[];
}
```

---

### 3. TypeScript Processor

**typeId:** `ffd19a7a-7613-40c0-876a-5d9a6eca66b6`
**`_type`:** `interfaces.TypeScriptProcessorConfig`

The workhorse of BSI EIP. Executes arbitrary TypeScript logic. Can route to custom outlets, set named attributes for downstream processors, or return structured data.

#### customConfig

```json
{
  "_type": "interfaces.TypeScriptProcessorConfig",
  "_typeVersion": "interfaces-23.2.018",
  "outletScriptIds": {
    "OK": "{outlet-config-id}",
    "Error": "{outlet-config-id}"
  }
}
```

**Important:** `outletScriptIds` maps outlet **names** (as displayed in the UI) to the **outlet config object UUID** (the `id` field of the outlet config entry in the `outlets` array). The `Standard` outlet is always present and hidden — it does not need an entry here. Only non-Standard outlets need entries.

#### Outlets

| Outlet Name | Role | Notes |
|---|---|---|
| `Standard` | hidden, always present | Used when no explicit `withOutlet()` call is made |
| Custom (e.g. `OK`, `Error`, `Valid`, `Invalid`) | user-defined | Must be listed in `outletScriptIds` |

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `script.ts` | `process(invocation, self)` | Main processing logic |

**Typical `script.ts`:**
```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { LOG } from '@eip/core';

export function process(invocation: Invocation, self: Self) {
  const element = invocation.processors.iteration.element;
  const iban = element.iban?.trim().replace(/\s+/g, '');

  if (!iban || iban.length < 15) {
    return self.withOutlet('Error').withAttribute('cleanedIban', null);
  }

  LOG.debug(`Processing IBAN: ${iban}`);

  return self
    .withOutlet('OK')
    .withAttribute('cleanedIban', iban);
}
```

**Returning structured data (without outlet routing):**
```typescript
export function process(invocation: Invocation, self: Self) {
  const element = invocation.processors.iteration.element;
  return {
    isValid: true,
    bankCode: element.iban.substring(4, 12),
    bic: 'COBADEFFXXX'
  };
}
```

**Returning a LambdaResultError:**
```typescript
export function process(invocation: Invocation, self: Self) {
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'IBAN format is invalid'
  };
}
```

#### Auto-generated type files

**`api.d.ts`** (readOnly: true):
```typescript
import { Attributes } from './attributes';
import { process } from './script';

export interface _Attributes extends Omit<Attributes, 'result'> {
  result: ReturnType<typeof process>;
}
```

**`definition.d.ts`** (readOnly: true, scriptKind: `"private-api"`):
```typescript
import { Attributes } from './attributes';

export type Outlet = 'OK' | 'Error';  // all non-Standard outlet names

export interface Self {
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;
  withOutlet(outletId: Outlet): Self;
}
```

**`attributes.d.ts`** (readOnly: false — user-maintained):
```typescript
// Add one entry per self.withAttribute() call in script.ts
export interface Attributes {
  cleanedIban: string | null;
}
```

---

### 4. REST Consumer Processor

**typeId:** `f069aa44-fb5c-469e-a727-705ca7072fee`
**`_type`:** `interfaces.RestConsumerProcessorConfig`

Calls an external HTTP REST API. The `prepareRequest` script configures query params, headers, path params, and body. The response body, status code, headers, and cookies are available to downstream processors.

#### customConfig

```json
{
  "_type": "interfaces.RestConsumerProcessorConfig",
  "_typeVersion": "interfaces-24.2.008",
  "server": "https://api.example.com/",
  "path": "/api/v1/endpoint/",
  "httpMethod": "get"
}
```

**httpMethod values:** `"get"`, `"post"`, `"put"`, `"patch"`, `"delete"`

**Path parameters** are embedded in the `path` field using `{paramName}` placeholders:
```json
"path": "/api/v1/users/{userId}/addresses/"
```

#### Outlets

| Outlet Name | Role | Notes |
|---|---|---|
| `Standard` | primary success path | connects to next processor |
| `Sonstige` | hidden, non-2xx responses | for error handling |

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `script.ts` | `prepareRequest(invocation, self)` | Configures the HTTP request |

**Typical `script.ts`:**
```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('myApiKey'))
    .withQueryParam('format', 'json')
    .withQueryParam('iban', invocation.processors.prepare.cleanedIban);
}
```

**With path parameters:**
```typescript
export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withPathParam('userId', invocation.processors.iteration.element.userId)
    .withHeader('Authorization', `Bearer ${Resolvers.environmentVariables.resolveBySetting('token')}`);
}
```

#### Response access in downstream processors

```typescript
// In a TypeScript processor that runs after the REST Consumer:
const body = invocation.processors.myRestConsumer.body;      // parsed JSON
const status = invocation.processors.myRestConsumer.statusCode; // e.g. 200
const headers = invocation.processors.myRestConsumer.headers;   // MapLike<string,string>
const cookies = invocation.processors.myRestConsumer.cookies;   // MapLike<string,string>
```

#### Auto-generated type files

**`api.d.ts`** (readOnly: true):
```typescript
import { MapLike } from '@eip/core';
import { ResponseBody } from './restapi';

export interface _Attributes {
  body: ResponseBody;
  cookies: MapLike<string, string>;
  headers: MapLike<string, string>;
  statusCode: number;
}
```

**`definition.d.ts`** (readOnly: true, scriptKind: `"private-api"`):
```typescript
import { PathParams, QueryParams, RequestBody } from './restapi';

export interface Self {
  withHeader(name: string, value: string): Self;
  withCookie(name: string, value: string): Self;
  withPathParam<T extends keyof PathParams>(paramId: T, value: PathParams[T]): Self;
  withQueryParam<T extends keyof QueryParams>(paramId: T, ...value: QueryParams[T][]): Self;
}
```

**`restapi.d.ts`** (readOnly: false — user-editable for type safety):
```typescript
export type PathParams = any;
export type QueryParams = any;
export type RequestBody = any;
export type ResponseBody = any;
```

---

### 5. Invoke Lambda Processor

**Java class:** InvokeLambdaProcessor
**typeId:** `9d107af5-8cdc-4138-bbdf-fc5383ece181`
**`_type`:** `interfaces.InvokeLambdaProcessorConfig`
**Category:** CRM

Calls another BSI EIP Lambda interface from within the current interface. Used to compose interfaces and reuse shared logic. Typical use: batch interfaces that reuse existing Lambda logic without duplicating it.

#### customConfig

```json
{
  "_type": "interfaces.InvokeLambdaProcessorConfig",
  "_typeVersion": "interfaces-24.2.015",
  "qualifiedLambdaId": "interfaces:lambdaProcessor:{lambdaProcessor_gid}:{interface_gid}"
}
```

**`qualifiedLambdaId` format:**
```
interfaces:lambdaProcessor:{lambdaProcessor_gid}:{interface_gid}
```
Where:
- `lambdaProcessor_gid` = the `gid` of the Lambda Processor within the target interface (NOT the processor `id`, but the `gid`)
- `interface_gid` = the `gid` of the target interface (NOT the interface `id`, but the `gid`)

**Example from weather-api:**
```
interfaces:lambdaProcessor:dc045211-0a34-4ca4-ba94-dbbc27b50d21:ffc77303-8574-4206-b7e5-ec9be108af21
```
- `dc045211-...` = gid of the `weatherApi_lambda` processor
- `ffc77303-...` = gid of the `WetterAbfrage` interface

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `prepare.ts` | `prepare(invocation, self)` | Sets input for the called lambda via `self.withInput()` |
| `definition.d.ts` | *(auto-generated)* | Self with `withInput(input)`, `withInputs(input[])`, `withRunAsUsername()` |
| `api.d.ts` | *(auto-generated)* | Typed with `error: LambdaError[]` and `data: LambdaOutput[]` |

**Typical `prepare.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function prepare(invocation: Invocation, self: Self) {
  const city = invocation.processors.customer_iteration.element.cityName;
  self.withInput({ city: city });
}
```

**Accessing results in downstream processors:**
```typescript
invocation.processors.invokeLambda.data          // LambdaOutput[]
invocation.processors.invokeLambda.data[0].score // first result's score field
invocation.processors.invokeLambda.error         // LambdaError[] if errors occurred
```

#### Outlets

| Outlet Name | Descriptor ID | Notes |
|---|---|---|
| `Standard` | `cce40eff-3c00-45fc-b569-74c5eb3710b7` | → next processor |

**Usage:** The target Lambda must be Live in production; during testing it can be a draft. The `qualifiedLambdaId` references the Lambda Processor's `gid` (not its `id`) and the interface's `gid` (not its `id`).

---

### 6. CRM Mutation Processor

**Java class:** CrmMutationProcessor
**typeId:** `cf9ee65c-a489-4250-b76a-7b1741868c0f`
**`_type`:** `interfaces.CrmMutationProcessorConfig`
**Category:** CRM

Creates or updates records in the BSI CRM. The mutation logic is entirely in the `data.ts` script using `Mutations.create()`.

#### customConfig

```json
{
  "_type": "interfaces.CrmMutationProcessorConfig",
  "_typeVersion": "interfaces-24.2.010"
}
```

The customConfig body is empty — the mutation logic is entirely in the script.

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `data.ts` | `prepareMutations(invocation, self)` | Builds and queues the mutation(s) |
| `definition.d.ts` | *(auto-generated)* | Self with `withMutations()`, `withModifiedByUsername()`, `withRunAsUsername()` |
| `api.d.ts` | *(auto-generated)* | Typed MutationResponse |

**Typical `data.ts`:**
```typescript
import { Mutations } from '@eip/crm-mutation';
import { Self } from './definition';
import { Invocation } from '../interface';

export function prepareMutations(invocation: Invocation, self: Self) {
  const customerKey = invocation.processors.customer_iteration.element.id;
  const score = invocation.processors.invokeLambda.data[0].score;

  self.withMutations(Mutations.create('CrmCustomerUpdate', {
    customerKey: customerKey,
    y_weatherScore: score
  }));
}
```

**`Mutations.create(type, fields)` — key details:**
- Import from `@eip/crm-mutation`
- `type`: mutation type name (e.g., `'CrmCustomerUpdate'`, `'CrmTaskCreate'`)
- `fields`: object with field names from the mutation type definition (query `/l/cpd-tools/mutationtypes/{name}`)

**Optional Self methods:**
- `self.withMutations(mutation)` — queue the mutation (required)
- `self.withModifiedByUsername(username)` — log who made the change
- `self.withRunAsUsername(username)` — execute with permissions of another user

**MutationResponse shape (from api.d.ts):**
```typescript
interface MutationResponse {
  requestRef: string;
  keyMappings: MapLike<string, string>;
  status: 'ok' | 'error' | 'cancelled';
  transactionRef: string;
  errorCode: string;
  errorMessage: string;
  errorMessageOrigin: string;
}
```

#### Outlets

| Outlet Name | Descriptor ID | Notes |
|---|---|---|
| `Standard` | `6c0f1af6-2051-4fd5-947b-398c59418229` | → success path |
| `Fehler` | `f3aac37d-ce3b-45d0-8c52-b157854d2e8f` | → error path |

**Discovery:** Before generating a CRM Mutation, query `{baseUrl}/l/cpd-tools/mutationtypes/{type}` to know which fields are available and which are mandatory. See `bsi-api-discovery.md`.

---

### 7. Temporal Trigger (Zeitlicher Trigger)

**Java class:** TriggerTemporalProcessor
**`_type`:** `interfaces.TriggerTemporalProcessorConfig`
**typeId:** `406211f6-7b91-4790-b492-feb3e7cac22c`
**Category:** Trigger

#### customConfig

```json
{
  "_type": "interfaces.TriggerTemporalProcessorConfig",
  "_typeVersion": "interfaces-22.0.0",
  "temporalConfig": {
    "_type": "bsiscout.TemporalConfig",
    "_typeVersion": "bsiscout-22.0.0",
    "periodicityConfig": {
      "_type": "bsiscout.PeriodicityConfig",
      "_typeVersion": "bsiscout-22.0.0",
      "periodicityType": "daily",
      "temporalOption": "interval",
      "hour": 1,
      "minute": 0,
      "interval": 1,
      "second": null,
      "weekday": null,
      "dayOfMonth": null,
      "month": null,
      "startDate": null,
      "endDate": null
    },
    "temporalMode": "periodicity",
    "temporalOption": "interval"
  }
}
```

**Key fields:**

| Field | Values | Description |
|---|---|---|
| `periodicityType` | `"daily"` \| `"weekly"` \| `"monthly"` \| `"yearly"` | Recurrence unit |
| `hour` | 0–23 | Hour of day for the trigger |
| `minute` | 0–59 | Minute of hour |
| `interval` | integer ≥ 1 | Repeat every N days/weeks/months |
| `temporalMode` | `"periodicity"` | Always `"periodicity"` for scheduled triggers |
| `temporalOption` | `"interval"` | Always `"interval"` |

#### Scripts

No script required. The Temporal Trigger has no scripting — it simply fires at the configured time.

#### Outlets

| Outlet Name | Descriptor ID | Presentation | Notes |
|---|---|---|---|
| `Standard` | `b3f5da65-ba2e-40ab-9983-a4e34544ff28` | primary | → next processor |

**Usage:** Entry point for scheduled (batch) interfaces. Always the first processor in an Ad-Hoc interface that runs on a schedule.

---

### 8. CRM Data Search (Daten suchen)

**Java class:** CrmDataModelSearchProcessor
**`_type`:** `interfaces.CrmDataModelSearchProcessorConfig`
**typeId:** `633d02d2-bda7-450d-a399-277644d39082`
**Category:** CRM

#### customConfig

```json
{
  "_type": "interfaces.CrmDataModelSearchProcessorConfig",
  "_typeVersion": "interfaces-26.1.001",
  "asListData": false,
  "selection": {
    "_type": "bsiscout.DataModelRelationSelection",
    "_typeVersion": "bsiscout-24.2.001",
    "alias": "crmCustomers",
    "relation": "crmCustomers",
    "containerEntityId": "Root",
    "targetType": "List:Entity:CrmCustomer",
    "resultDoType": "scout.DoEntity",
    "distinct": false,
    "maximumRowCount": 20,
    "constraint": {
      "_type": "bsiscout.DataModelAndConstraint",
      "_typeVersion": "bsiscout-8.0.0.034",
      "constraints": [
        {
          "_type": "bsiscout.DataModelAttributeConstraint",
          "_typeVersion": "bsiscout-9.0.0.039",
          "attribute": "active",
          "fieldType": "Boolean",
          "op": "true",
          "operands": []
        },
        {
          "_type": "bsiscout.DataModelRelationConstraint",
          "_typeVersion": "bsiscout-24.2.001",
          "negated": true,
          "relation": "y-weatherScore",
          "targetType": "Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c"
        }
      ]
    },
    "selections": [
      {
        "_type": "bsiscout.DataModelAttributeSelection",
        "_typeVersion": "bsiscout-8.0.0.040",
        "alias": "id",
        "attribute": "id",
        "fieldType": "Key:Entity:CrmCustomer"
      },
      {
        "_type": "bsiscout.DataModelRelationSelection",
        "_typeVersion": "bsiscout-24.2.001",
        "alias": "cityName",
        "relation": "preferredPhysicalAddress",
        "targetType": "Entity:CrmPhysicalAddress",
        "selections": [
          {
            "_type": "bsiscout.DataModelAttributeSelection",
            "_typeVersion": "bsiscout-8.0.0.040",
            "attribute": "cityName",
            "fieldType": "Text60"
          }
        ]
      }
    ],
    "namespaceVersions": ["bsiscout-25.1.0", "crm-25.2.2", "crocus-1.0.0", "cstudio-22.0.0", "interfaces-22.0.0", "oroya-1.0.0", "start-22.0.0"]
  }
}
```

**Key fields:**

| Field | Description |
|---|---|
| `selection.relation` | CRM entity relation name (e.g., `crmCustomers`, `crmContracts`) |
| `selection.maximumRowCount` | Safety limit on result count — **always set this** |
| `selection.constraint` | Filter conditions (AND/OR/NOT combinations) |
| `selection.selections` | Which fields to return (flat attributes and nested relations) |
| `asListData` | Set to `false` |

**Constraint types:**

| Type | Description |
|---|---|
| `bsiscout.DataModelAttributeConstraint` | Filter on a scalar field (`op: "true"/"false"/"notNull"/"isNull"/"eq"/"ne"` etc.) |
| `bsiscout.DataModelRelationConstraint` | Filter on a relation (with optional `negated: true` for NOT) |
| `bsiscout.DataModelAndConstraint` | AND of multiple constraints |
| `bsiscout.DataModelOrConstraint` | OR of multiple constraints |

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `script.ts` | `prepareQuery(invocation, self)` | Optional query overrides: `self.withMaxRowCount(n)`, `self.withLocale('de')`, `self.withRunAsUsername('admin')` |
| `api.d.ts` | *(auto-generated)* | Typed result interface reflecting the selections |

**TypeScript result access:**
```typescript
invocation.processors.customer_searchData.data           // CrmCustomers[]
invocation.processors.customer_searchData.data[0].id     // customer key
invocation.processors.customer_searchData.data[0].cityName // city name
```

#### Outlets

| Outlet Name | Descriptor ID | Presentation | Notes |
|---|---|---|---|
| `Standard` | `59c636c9-ccce-4650-8460-f7025a556cd2` | primary | → next processor |

**Usage:** Query CRM data for batch processing. Always set `maximumRowCount` as a safety limit. Follow with an Iteration processor using the search result as input.

---

### 9. REST Provider

**Java class:** RestProviderProcessor
**`_type`:** `interfaces.RestProviderProcessorConfig`
**typeId:** `01eb3948-507e-4ff4-bb31-525bab2b3e08`
**Category:** REST

Exposes an HTTP endpoint. Receives incoming requests and routes them to the processing chain. The `provideResponse` script assembles the HTTP response.

#### customConfig

```json
{
  "_type": "interfaces.RestProviderProcessorConfig",
  "_typeVersion": "interfaces-24.2.008",
  "endpointId": "f1f35f8c-6998-4bac-a3b0-6ca3373aae0a",
  "operationId": "f03ac424-d5d1-4ad8-8f2c-a66f64301e85",
  "webapiId": "7a28d2aa-2446-432f-8bce-6d64f0fb01f5"
}
```

**Key fields:**

| Field | Description |
|---|---|
| `webapiId` | UUID of the Web API header (from `02-interfaces/webapis/headers/`) |
| `endpointId` | UUID of the Web API endpoint (from `02-interfaces/webapis/endpoints/`) |
| `operationId` | UUID of the specific HTTP operation on the endpoint |

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `response.ts` | `provideResponse(invocation, self)` | Assembles the HTTP response |
| `definition.d.ts` | *(auto-generated)* | Self with `withStatus(code)`, `withBody(value)`, `withHeader(name, value)`, `withPart(...)` |
| `api.d.ts` | *(auto-generated)* | Typed request attributes (body, queryParams, pathParams, headers, cookies, policies) |

**Typical `response.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function provideResponse(invocation: Invocation, self: Self) {
  self
    .withStatus(200)
    .withBody(invocation.processors.callWeatherApi_customer_typescript.result);
}
```

**Request data access (from `api.d.ts`):**
```typescript
invocation.processors.restProvider.pathParams['city']   // URL path parameter
invocation.processors.restProvider.queryParams['q']     // query string parameter
invocation.processors.restProvider.body                 // request body
invocation.processors.restProvider.headers['auth']      // request header
invocation.processors.restProvider.cookies['session']   // cookie
```

#### Outlets

| Outlet Name | Descriptor ID | Execution Type | Notes |
|---|---|---|---|
| `Aufruf` | `6891417a-17b6-42a1-850a-da8effff4d13` | scoped | → processing chain |
| `Abgeschlossen` | `1cbc92dc-5491-43f2-8e80-8e25556052dd` | async | terminal (wire to `null`) |

**Important:** The REST Provider is the entry point for HTTP requests, but it is NOT the first processor in the flow. It is placed separately in the canvas (y=15 in the example) and routes incoming requests via its `Aufruf` outlet to the processing chain. The `Abgeschlossen` outlet is async and fires after the response is sent.

**Prerequisites:** A Web API definition (header + endpoint files) must be created in BSI EIP and imported before this processor can reference it. The Web API files are in `02-interfaces/webapis/`.

---

### 10. Local Routine

**Java class:** LocalRoutineProcessor
**`_type`:** `interfaces.LocalRoutineProcessorConfig`
**typeId:** `9332ef6a-024d-42d7-91ab-01c3d4121750`
**Category:** Base

Defines a reusable, typed sub-routine within an interface. Can be called from any TypeScript processor in the same interface via `LocalRoutines.{scriptIdentifier}({input})`.

#### customConfig

```json
{
  "_type": "interfaces.LocalRoutineProcessorConfig",
  "_typeVersion": "interfaces-23.2.001"
}
```

The customConfig body is empty — the Local Routine is defined entirely by its scripts and outlet chain.

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `types.d.ts` | *(user-maintained)* | Defines `Input` and `Output` TypeScript types |
| `output.ts` | `provideOutput(invocation): Output` | Returns the result of the routine's internal processing chain |
| `api.d.ts` | *(auto-generated)* | Exposes `_localRoutine(input: Input): Output` |

**Typical `types.d.ts`:**
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

**Typical `output.ts`:**
```typescript
import { Output } from './types';
import { Invocation } from '../interface';

export function provideOutput(invocation: Invocation): Output {
  return invocation.processors.weatherApi_transform.result;
}
```

**Calling the Local Routine from a TypeScript processor:**
```typescript
import { LocalRoutines } from '../interface';

export function process(invocation: Invocation, self: Self) {
  const city = invocation.processors.restProvider.pathParams['city'];
  return LocalRoutines.weatherApi_localRoutine({ city: city });
}
```

#### Outlets

| Outlet Name | Descriptor ID | Execution Type | Notes |
|---|---|---|---|
| `Aufruf` | `885d0c0b-3b59-4c13-85af-a061fd11eb66` | scoped | → internal processing chain |

**Usage:** The `Aufruf` outlet is the entry point of the routine's internal pipeline. The routine ends when its outlet chain terminates. The return value of `LocalRoutines.xxx()` is what `provideOutput` returns.

Useful when the same logic is needed from multiple entry points (e.g., both Lambda and REST Provider).

---

### 11. CSV Processor

**Java class:** CsvProcessor
**`_type`:** `interfaces.CsvProcessorCustomConfig`
**typeId:** `1245030d-3b73-42fb-a7a8-3ed91b729303`
**Category:** Data

Reads a CSV string provided by an upstream TypeScript processor and outputs a `ListData<Record<string,string>>` with one entry per CSV row (excluding header). Column names come from the first row (header row).

#### customConfig

```json
{
  "_type": "interfaces.CsvProcessorCustomConfig",
  "_typeVersion": "interfaces-26.1.001",
  "operation": "read",
  "presetId": "{preset-uuid}"
}
```

`presetId` references a Preset file in the ZIP's `presets/` folder.

#### Preset File (`presets/{name}-{uuid}.json`)

```json
{
  "_type": "interfaces.Preset",
  "_typeVersion": "interfaces-22.0.0",
  "id": "{preset-uuid}",
  "name": "default",
  "descriptorId": "01f03794-f5f3-4b44-93f7-ddde66869af8",
  "projectId": "{project-uuid}",
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

**Preset field reference:**

| Field | Default | Description |
|---|---|---|
| `delimiterCharacter` | `";"` | Column separator character |
| `encoding` | `"UTF-8"` | File encoding |
| `escapeCharacter` | `"\\"` | Escape character for special chars |
| `ignoreEmptyLines` | `false` | Skip empty lines |
| `ignoreHeaderRecord` | `false` | Set `true` to skip header row |
| `ignoreSurroundingSpaces` | `false` | Trim whitespace around values |
| `ignoreTrailingDelimiter` | `false` | Ignore trailing delimiter at end of line |

#### Scripts

| Script file | Function | Description |
|---|---|---|
| `data.ts` | `provideData(invocation)` | Returns the CSV string from an upstream processor |
| `api.d.ts` | *(auto-generated)* | `rows: ListData<Record<string, string>>` |

**Typical `data.ts`:**
```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.simulateFetch.result;
  // or: invocation.processors.restConsumer.body  (if CSV comes from an API)
}
```

**Auto-generated `api.d.ts`:**
```typescript
import { ListData } from '@eip/core';
export interface _Attributes {
  rows: ListData<Record<string, string>>;
}
```

**Accessing the parsed data downstream:**
```typescript
invocation.processors.csv.rows                       // ListData<Record<string,string>>
// After Iteration: invocation.processors.iterateFetch.element.columnName
```

#### Outlets

| Outlet Name | Descriptor ID | Notes |
|---|---|---|
| `Standard` | `ed9dfe53-c48e-4551-b398-b1c2598726a8` | → Iteration processor |

**Typical pipeline:** TypeScript (provides CSV string) → **CSV** → Iteration → TypeScript (maps row fields)

---

### 12. Manual Trigger (Manueller Trigger)

**Java class:** TriggerManualProcessor
**`_type`:** `interfaces.TriggerManualProcessorConfig`
**typeId:** `b4447959-8495-4a20-83e1-e3e0384c5935`
**Category:** Trigger

A trigger that is manually invoked from the BSI EIP UI. Used to create alternative entry points within an interface — most commonly for manually triggering a retry path or a one-time administrative operation.

#### customConfig

```json
{
  "_type": "interfaces.TriggerManualProcessorConfig",
  "_typeVersion": "interfaces-22.0.0"
}
```

The customConfig body is empty — no configuration needed.

#### Scripts

No scripts required. The Manual Trigger is purely a start node.

#### Outlets

| Outlet Name | Descriptor ID | Notes |
|---|---|---|
| `Standard` | `d20e1c72-467d-4af8-9c19-0027cd18c901` | → next processor |

**Usage:** Place at `y=14` (or any y-offset below the main flow) to separate it visually from the main flow. Assign it to its own group (e.g., "Retry").

**Comparison with Temporal Trigger:**

| | Temporal Trigger | Manual Trigger |
|---|---|---|
| Activation | Scheduled (time-based) | Manual (UI click) |
| Config | Periodicity, hour, minute | None |
| Typical use | Nightly batch jobs | Retry paths, admin operations |

---

## Standard Outlet Names by Processor Type

| Processor | Standard Outlets | Notes |
|---|---|---|
| Lambda | `Aufruf` (scoped), `Abgeschlossen` (default) | `Aufruf` fires per-call; wire to Iteration |
| Iteration | `Iteration` (scoped), `Abgeschlossen` (default) | `Iteration` fires per-item; wire to first proc |
| TypeScript | `Standard` (hidden), + custom outlets | Custom outlets defined in `outletScriptIds` |
| REST Consumer | `Standard` (primary), `Sonstige` (hidden) | `Sonstige` catches non-2xx responses |
| REST Provider | `Aufruf` (scoped), `Abgeschlossen` (async) | `Aufruf` routes to processing chain; `Abgeschlossen` fires after response sent |
| CSV Processor | `Standard` (primary) | → Iteration |
| Manual Trigger | `Standard` (primary) | → next processor |
| Temporal Trigger | `Standard` (primary) | → next processor |
| Local Routine | `Aufruf` (scoped) | Entry point of the routine's internal pipeline |
| Temporal Trigger | `Standard` (primary) | Fires at the configured schedule |
| CRM Data Search | `Standard` (primary) | → Iteration processor |
| Invoke Lambda | `Standard` | → next processor |
| CRM Mutation | `Standard`, `Fehler` | `Fehler` on mutation failure |
| SMTP | `Standard`, `Fehler` | `Fehler` on send failure |
| Try/Catch | `Standard`, `Catch` | `Catch` fires on exception |
| Retry | `Standard`, `Fehler` | `Fehler` after all retries exhausted |

---

## Position Grid Notes

Processor positions in the visual editor use an (x, y) grid coordinate system.

- **Horizontal spacing:** processors in a sequential row are spaced 6 units apart
  - Column positions: x = 2, 8, 14, 20, 26, 32, ...
- **Vertical position:** `y = 2` for a single-row interface
- **Parallel branches:** use different `y` values (e.g. y=2 and y=8 for two parallel paths)
- **Groups:** processors within a group share the group's coordinate space

**Typical single-row layout:**
```
Lambda (x=2, y=2) → Iteration (x=8, y=2) → TypeScript (x=14, y=2) → ...
```

---

## Outlet Descriptor ID Reference

Outlet `descriptorId` values are fixed per processor type. Use these when constructing outlet connection objects in interface JSON.

| Processor | Outlet Name | Descriptor ID | Execution Type |
|---|---|---|---|
| Lambda | `Aufruf` | *(from working examples)* | scoped |
| Lambda | `Abgeschlossen` | *(from working examples)* | default |
| Iteration | `Iteration` | *(from working examples)* | scoped |
| Iteration | `Abgeschlossen` | *(from working examples)* | default |
| Local Routine | `Aufruf` | `885d0c0b-3b59-4c13-85af-a061fd11eb66` | scoped |
| REST Provider | `Aufruf` | `6891417a-17b6-42a1-850a-da8effff4d13` | scoped |
| REST Provider | `Abgeschlossen` | `1cbc92dc-5491-43f2-8e80-8e25556052dd` | async |
| Temporal Trigger | `Standard` | `b3f5da65-ba2e-40ab-9983-a4e34544ff28` | primary |
| CRM Data Search | `Standard` | `59c636c9-ccce-4650-8460-f7025a556cd2` | primary |
| Invoke Lambda | `Standard` | `cce40eff-3c00-45fc-b569-74c5eb3710b7` | — |
| CRM Mutation | `Standard` | `6c0f1af6-2051-4fd5-947b-398c59418229` | — |
| CRM Mutation | `Fehler` | `f3aac37d-ce3b-45d0-8c52-b157854d2e8f` | — |

---

## Notes on `_typeVersion`

Each `customConfig` object carries a `_typeVersion` field alongside `_type`. This version string tracks the schema version of the config DO. It is set by the platform and should not be altered manually — copy the version from working example configs. Common versions seen in the wild:

| Config type | Example `_typeVersion` |
|---|---|
| `interfaces.CrmLambdaProcessorConfig` | `interfaces-23.2.019` |
| `interfaces.IterationProcessorConfig` | `interfaces-26.1.001` |
| `interfaces.TypeScriptProcessorConfig` | `interfaces-23.2.018` |
| `interfaces.RestConsumerProcessorConfig` | `interfaces-24.2.008` |
| `interfaces.RestProviderProcessorConfig` | `interfaces-24.2.008` |
| `interfaces.LocalRoutineProcessorConfig` | `interfaces-23.2.001` |
| `interfaces.TriggerTemporalProcessorConfig` | `interfaces-22.0.0` |
| `interfaces.CrmDataModelSearchProcessorConfig` | `interfaces-26.1.001` |
| `interfaces.InvokeLambdaProcessorConfig` | `interfaces-24.2.015` |
| `interfaces.CrmMutationProcessorConfig` | `interfaces-24.2.010` |
| `bsiscout.Signature` | `bsiscout-24.1.001` |
| `bsiscout.SignatureField` | *(no version field)* |
| `bsiscout.TemporalConfig` | `bsiscout-22.0.0` |
| `bsiscout.PeriodicityConfig` | `bsiscout-22.0.0` |
| `bsiscout.DataModelRelationSelection` | `bsiscout-24.2.001` |
| `bsiscout.DataModelAttributeSelection` | `bsiscout-8.0.0.040` |
| `bsiscout.DataModelAndConstraint` | `bsiscout-8.0.0.034` |
| `bsiscout.DataModelAttributeConstraint` | `bsiscout-9.0.0.039` |
| `bsiscout.DataModelRelationConstraint` | `bsiscout-24.2.001` |
