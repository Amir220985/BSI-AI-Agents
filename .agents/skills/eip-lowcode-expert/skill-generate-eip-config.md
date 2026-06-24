# Skill: Generate BSI EIP Configuration ZIP

**Purpose:** Generate a complete, importable BSI EIP configuration ZIP package based on customer requirements.

**Output:** A ZIP archive (or the JSON file contents ready to be zipped) that can be imported directly into a BSI EIP 26.1.8 installation.

**Primary example:** `examples/iban-validation/` — read `ANNOTATION.md` before generating anything.

---

## Reference Documentation

Before generating, read the relevant reference files in `generator/reference/`:

| File | What it covers |
|---|---|
| `zip-package-format.md` | ZIP structure, `export-definition.json`, `index.json`, all file naming rules, `valueMigrationIds` |
| `interface-config.md` | `InterfaceConfig` structure, `ProcessorConfig`, `TypeScriptConfig`, all field definitions |
| `outlets-and-routing.md` | `OutletConfig` structure, descriptor IDs, `outletScriptIds` wiring rules, routing patterns |
| `processor-types-catalog.md` | All processor type UUIDs, `customConfig` structures, script contracts, outlet patterns |
| `signature-reference.md` | Signature and `SignatureProperty` structure, data types, multilingual names |
| `data-types-reference.md` | All 55+ data types: IDs, Java types, TypeScript equivalents |
| `environment-variables.md` | API keys and secrets via `Resolvers.environmentVariables` |
| `typescript-scripting-api.md` | Full `invocation`, `self`, `LOG`, `Resolvers`, `Collections` API reference |
| `collections-api.md` | Persistent key-value store for retry queues, hash maps, config |
| `bsi-api-discovery.md` | Discovery APIs for codetypes and mutation types (requires base URL) |

**Additional reference files for multi-package / CRM scenarios:**

| File | What it covers |
|---|---|
| `multi-package-zip.md` | `multi-index.json` structure, CRM + interfaces stages, stage types |
| `crm-field-transfer.md` | CRM field creation via config transfer: `DomainKeyConfigurationTransferId`, field definition JSON |
| `interfaces-index-structure.md` | `referencedItems` as objects, `globalUniqueId` prefixes, `interfaces.Project` type |
| `crm-data-search-processor.md` | `CrmDataModelSearchProcessorConfig` v26.1.001, full selection structure |
| `powershell-zip-encoding.md` | UTF-8-safe ZIP creation on Windows (stdin encoding pitfalls, BOM removal) |

**Primary example:** `examples/iban-validation/ANNOTATION.md` — full annotated walkthrough of a complete production interface. Read this to understand how all pieces connect.

**Multi-package example:** `examples/weather-api/ANNOTATION.md` — Lambda + Ad-Hoc batch + CRM field in a single importable ZIP.

---

## Step 0: Base URL and Discovery

Before generating any configuration, determine:

**1. Ask for the customer base URL (ALWAYS)**

The BSI EIP Web API base URL is customer-specific. Always ask:

> "What is the BSI EIP base URL of your installation?  
> Example: `https://bsi-2005.trials.bsi-software.com/bsiinterfaces/web-api`"

Never assume or hardcode this URL. It is required for discovery API calls and must be documented in the post-import instructions.

**2. Use discovery APIs (as needed)**

If the configuration needs CRM code references or mutations, query the discovery APIs before generating:

| If the configuration... | Then query... |
|---|---|
| ...has CRM code fields (`Key:Entity:CrmCode:{uuid}`) | `GET {baseUrl}/l/cpd-tools/codetypes/{name}` — to know code values and UUID |
| ...has negative CRM constraints | `GET {baseUrl}/l/cpd-tools/codetypes` — to find the code list UUID |
| ...executes CRM mutations | `GET {baseUrl}/l/cpd-tools/mutationtypes/{name}` — to know fields and mandatory status |
| ...reads CRM data | No discovery needed — field names are known or provided by the customer |

Full discovery API documentation: `reference/bsi-api-discovery.md`

---

## Step 1: Understand the Requirements

Gather all required information before generating anything. Ask the customer or derive from context:

### Lambda Contract
- What is the Lambda name? (used in filenames and UI)
- What project name should it belong to?
- What is the Lambda description? (shown in BSI EIP, ideally in German + English)
- What language locales are needed? (`und` only, or `en`/`fr`/`it` as well)

### Inputs
For each input field:
- `identifier` (camelCase, e.g. `iban`, `customerId`, `emailAddress`)
- Display name (localized)
- Data type: `Text250`, `Text60`, `Text`, `Boolean`, `Decimal`, `Long`, `Date`, `DateTime`
- Is it mandatory?

### Outputs
For each output field:
- `identifier` (camelCase)
- Display name (localized)
- Data type

### External API
- Base server URL (e.g. `https://api.example.com/`)
- API path (e.g. `/v1/validate/`)
- HTTP method: `get`, `post`, `put`, `patch`, `delete`
- Authentication: API key (query param or header?), Bearer token, Basic auth, or none?
- Environment variable name for the API key (e.g. `myApiKey`)
- Request parameters: query params? path params? JSON body?

### Outcomes
- What are the possible success cases? (e.g. Valid, Invalid — or just one success path?)
- What error cases need distinct outlets?
- What fields does a successful response return?
- What does the error response look like?

### Validation / Preparation
- Does the input need preprocessing? (whitespace removal, format checks)
- Are there input characters that are invalid and should short-circuit?

### CRM Integration (if applicable)

If the interface reads or writes CRM data, additionally gather:

**CRM code fields:**
- Which code lists are involved? (e.g., CommunicationStatus, a custom Wetter_Score list)
- Query `GET {baseUrl}/l/cpd-tools/codetypes/{name}` to see all valid values
- Note the code list UUID (from the BSI CRM data model or `01-crm/codes/` folder)
- Use `Key:Entity:CrmCode:{uuid}` as the signature type

**CRM mutations:**
- Which CRM entity is being updated? (e.g., CrmCustomer, CrmTask)
- Which mutation type? (e.g., CrmCustomerUpdate, CrmTaskCreate)
- Query `GET {baseUrl}/l/cpd-tools/mutationtypes/{name}` to see all available fields
- Note which fields are mandatory

**CRM data search:**
- Which CRM entity is searched? (relation name, e.g., `crmCustomers`)
- Which fields are needed from the search result?
- Which filter constraints are needed?
- What is the maximum result count (safety limit)?

---

## Step 2: Plan the Processor Pipeline

For a standard REST API Lambda, use this pipeline:

```
Lambda → Iteration → TypeScript(prepare) → REST Consumer → TypeScript(transform)
```

This is the canonical pattern from the IBAN validation example. Every processor in this chain has a specific role:

| Processor | scriptIdentifier | Role |
|---|---|---|
| Lambda | `lambda` | Entry point, defines signature, provides output |
| Iteration | `iteration` | Loops over input array, aggregates results |
| TypeScript | `prepare` | Input cleaning, validation, short-circuit on bad input |
| REST Consumer | `restConsumer` | Makes the HTTP call |
| TypeScript | `transform` | Interprets response, routes to appropriate outlet |

If no preprocessing is needed, `prepare` can simply pass through. If there are multiple REST calls, add additional REST Consumer + transform pairs.

**Position layout** (x-coordinates, all at y=2):
- lambda: x=2
- iteration: x=8
- prepare: x=14
- restConsumer: x=20
- transform: x=26

### Alternative: CRM Batch Processing (Ad-Hoc Interface)

For scheduled batch processing (e.g., update CRM records nightly):

```
Temporal Trigger → CRM Data Search → Iteration → Invoke Lambda → CRM Mutation
```

This pattern is used when:
- An operation should run on a schedule (not on-demand)
- Many CRM records need to be processed in bulk
- Existing Lambda logic should be applied to CRM data

**Interface type:** Ad-Hoc (`typeId: f72f9f76-fb2d-4579-b397-471b2ed4c4e3`) — NOT Lambda

### Alternative: CSV-Import (Input Interface)

For periodic CSV imports with change detection and retry:

```
Temporal Trigger → TypeScript(fetch) → CSV → Iteration → TypeScript(prepare)
  → TypeScript(validateAndMap, multi-outlet)
    → CRM Mutation → TypeScript(computeHash)
    → TypeScript(storeForRetry)

Manual Trigger → TypeScript(listCollection) → Iteration → TypeScript(prepareRetry)
  → TypeScript(validateAndMap)  [same processor]
```

**Interface type:** Input (`typeId: ce4bb086-02d6-4cee-9509-7b0dadaa6654`) — NOT Lambda, NOT Ad-Hoc

This pattern is used when:
- Data is provided as CSV (from S3, FTP, or mocked)
- Idempotent imports are needed (change detection via hash)
- Failed records should be queued for retry (up to N attempts)

Requires: 3 Collections (`mappings`, `processedRecords`, `retries`) + CSV Preset file.  
Full pattern: `patterns/csv-import-with-retry.md`

| Processor | scriptIdentifier | Role |
|---|---|---|
| Temporal Trigger | `{name}_temporalTrigger` | Scheduled execution |
| CRM Data Search | `{name}_searchData` | Search CRM records |
| Iteration | `{name}_iteration` | Iterate over results |
| Invoke Lambda | `invokeLambda` | Call an existing Lambda |
| CRM Mutation | `{name}_mutation` | Update CRM records |

**Position layout** (x-coordinates, all at y=2):
- temporalTrigger: x=2
- searchData: x=8
- iteration: x=14
- invokeLambda: x=20
- mutation: x=26

---

## Step 3: Generate UUIDs

Every configuration requires freshly generated UUIDs. Never copy UUIDs from the IBAN example — reusing them will cause import conflicts.

Generate fresh UUIDs for:

| Entity | Count | Notes |
|---|---|---|
| Project `id` | 1 | Used in project filename and `projectId` field |
| Interface `id` | 1 | Used in interface filename and index `resourcePath` |
| Interface `gid` | 1 | Stable across versions; also referenced in index |
| Signature `id` | 1 | Inside the Lambda's `customConfig.signature.id` |
| Each processor `id` | 1 per processor | Used to link scripts and outlets |
| Each processor `gid` | 1 per processor | Must be distinct from `id` |
| Each outlet `id` | 1 per outlet | Used in `outletScriptIds` values; must match exactly |
| Each outlet `gid` | 1 per outlet | Must be distinct from outlet `id` |
| `exportId` in index.json | 1 | Fresh per export |

**For a 5-processor REST Lambda:** you need approximately 30–35 fresh UUIDs (2 per processor + 2 per outlet, plus project, interface id/gid, signature, exportId).

**Fixed UUIDs that must NOT be regenerated:**

| Value | Where used |
|---|---|
| `36317f78-6040-4648-936d-e8b66b394c0b` | `responsible.userId` everywhere |
| `2512c737-a73b-4f78-9ae2-098ac6d291bd` | Interface `typeId` (Lambda interface type) |
| `ec06bfe3-faab-4c2c-83bc-8420789d3479` | Lambda processor `typeId` |
| `21c361ec-5dec-4f13-9767-442db1adb3a3` | Iteration processor `typeId` |
| `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` | TypeScript processor `typeId` |
| `f069aa44-fb5c-469e-a727-705ca7072fee` | REST Consumer processor `typeId` |
| `78861a9e-e99c-47c7-913b-6bf685f5557b` | Lambda "Aufruf" outlet `descriptorId` |
| `738f1301-f558-40b5-bbfc-e869a5832156` | Lambda "Abgeschlossen" outlet `descriptorId` |
| `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` | Iteration "Iteration" outlet `descriptorId` |
| `dd8f5806-3156-4697-97c0-dd069570f2e6` | Iteration "Abgeschlossen" outlet `descriptorId` |
| `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` | TypeScript "Standard" outlet `descriptorId` |
| `6a132916-f955-4dbd-a377-2c3ee21e7fcb` | REST Consumer "Standard" outlet `descriptorId` |
| `c95394e3-50c2-4b7c-9529-3149328355e9` | REST Consumer "Sonstige" outlet `descriptorId` |
| `f72f9f76-fb2d-4579-b397-471b2ed4c4e3` | Interface typeId (Ad-Hoc interface type) |
| `ce4bb086-02d6-4cee-9509-7b0dadaa6654` | Interface typeId (Input interface type) |
| `406211f6-7b91-4790-b492-feb3e7cac22c` | Temporal Trigger processor typeId |
| `b4447959-8495-4a20-83e1-e3e0384c5935` | Manual Trigger processor typeId |
| `1245030d-3b73-42fb-a7a8-3ed91b729303` | CSV Processor typeId |
| `633d02d2-bda7-450d-a399-277644d39082` | CRM Data Search processor typeId |
| `cf9ee65c-a489-4250-b76a-7b1741868c0f` | CRM Mutation processor typeId |
| `9d107af5-8cdc-4138-bbdf-fc5383ece181` | Invoke Lambda processor typeId |
| `01eb3948-507e-4ff4-bb31-525bab2b3e08` | REST Provider processor typeId |
| `9332ef6a-024d-42d7-91ab-01c3d4121750` | Local Routine processor typeId |
| `b3f5da65-ba2e-40ab-9983-a4e34544ff28` | Temporal Trigger "Standard" outlet descriptorId |
| `d20e1c72-467d-4af8-9c19-0027cd18c901` | Manual Trigger "Standard" outlet descriptorId |
| `ed9dfe53-c48e-4551-b398-b1c2598726a8` | CSV Processor "Standard" outlet descriptorId |
| `59c636c9-ccce-4650-8460-f7025a556cd2` | CRM Data Search "Standard" outlet descriptorId |
| `cce40eff-3c00-45fc-b569-74c5eb3710b7` | Invoke Lambda "Standard" outlet descriptorId |
| `6c0f1af6-2051-4fd5-947b-398c59418229` | CRM Mutation "Standard" outlet descriptorId |
| `f3aac37d-ce3b-45d0-8c52-b157854d2e8f` | CRM Mutation "Fehler" outlet descriptorId |
| `885d0c0b-3b59-4c13-85af-a061fd11eb66` | Local Routine "Aufruf" outlet descriptorId |
| `6891417a-17b6-42a1-850a-da8effff4d13` | REST Provider "Aufruf" outlet descriptorId |
| `1cbc92dc-5491-43f2-8e80-8e25556052dd` | REST Provider "Abgeschlossen" outlet descriptorId |
| The 8 `valueMigrationIds` | `index.json` (see critical note below) |

---

## Step 4: Generate the Five Files

### File 1: `export-definition.json`

```json
{
  "_type" : "bsiscout.ConfigurationExportDefinition",
  "_typeVersion" : "bsiscout-22.0.33",
  "exportFilename" : "bsi-eip-{YYYY-MM-DD_HH-MM-SS}.zip",
  "productId" : "interfaces",
  "rootTransferIds" : [ {
    "_type" : "bsiscout.IdConfigurationTransferId",
    "_typeVersion" : "bsiscout-22.0.0",
    "id" : "interfaces.InterfaceConfigId:{interface-id-uuid}"
  } ]
}
```

The `exportFilename` must match the actual ZIP filename you will create.

---

### File 2: `index.json`

This is the most complex file. It contains 9 items for a standard 5-processor REST Lambda (1 interface full + 1 project full + 7 reference-only items).

**Top-level structure:**

```json
{
  "_type" : "bsiscout.ConfigurationTransferIndex",
  "_typeVersion" : "bsiscout-22.0.0",
  "exportDate" : "{YYYY-MM-DD HH:MM:SS.mmm}",
  "exportId" : "{fresh-uuid}",
  "exportUser" : "generator",
  "items" : [ ... ],
  "productIdentifier" : "interfaces",
  "productVersion" : "26.1.8",
  "valueMigrationIds" : [
    "454863f5-f931-4527-92ed-fcd1c5bbbc35",
    "9bded4bf-c647-4458-9969-cbdbb318e442",
    "cd76ad5f-c20c-4ce0-870c-dc1a09a15c94",
    "97abafd1-942b-4df0-97b5-ccb042bda038",
    "9ad5ef84-010e-4384-987c-dadf145c7c8a",
    "001d276d-b7b6-4e67-a218-29d0a63ab2ab",
    "ea64e793-b804-411c-85d0-df9a70bf8d91",
    "381fbdee-7c31-48fa-84d6-13dc2f9954dd"
  ]
}
```

**CRITICAL:** The `valueMigrationIds` array must contain exactly these 8 UUIDs in exactly this order. They are tied to EIP product version 26.1.8. Do not generate new ones, do not reorder them, do not omit any.

**Items array — full item for the interface:**

```json
{
  "_type" : "bsiscout.ConfigurationTransferItem",
  "_typeVersion" : "bsiscout-22.0.0",
  "dataModelNamespaceVersions" : [ "bsiscout-25.1.0" ],
  "descriptions" : { "de" : "Version 1" },
  "globalUniqueId" : "{interface-gid-uuid}",
  "id" : {
    "_type" : "bsiscout.IdConfigurationTransferId",
    "_typeVersion" : "bsiscout-22.0.0",
    "id" : "interfaces.InterfaceConfigId:{interface-id-uuid}"
  },
  "itemGroupId" : "interfaces.interface",
  "names" : { "de" : "{InterfaceName}" },
  "referencedItems" : [ ... all reference items ... ],
  "resourcePath" : "interfaces/{Interface_Name}-{interface-id-uuid}.json",
  "root" : true,
  "transferType" : "full",
  "typeVersions" : {
    "interfaces.InterfaceConfig" : "interfaces-24.2.017",
    "interfaces.ProcessorConfig" : "interfaces-22.0.1004",
    "interfaces.OutletConfig" : "interfaces-22.0.1006",
    "interfaces.Point" : "interfaces-22.0.0",
    "interfaces.TypeScriptConfig" : "interfaces-23.2.007",
    "interfaces.CrmLambdaProcessorConfig" : "interfaces-23.2.019",
    "interfaces.IterationProcessorConfig" : "interfaces-26.1.001",
    "interfaces.TypeScriptProcessorConfig" : "interfaces-23.2.018",
    "interfaces.RestConsumerProcessorConfig" : "interfaces-24.2.008",
    "bsiscout.Signature" : "bsiscout-24.1.001",
    "bsiscout.SignatureProperty" : "bsiscout-24.1.001",
    "start.Responsible" : "start-1.3.2"
  }
}
```

The `referencedItems` array inside the interface item contains inline reference entries for:
- The interface type (Lambda)
- The interface `gid` (partial item)
- Each processor type used
- The project
- The responsible user

See `examples/iban-validation/index.json` for the exact structure of each reference item.

---

### File 3: `projects/{ProjectName}-{project-id-uuid}.json`

```json
{
  "_type" : "interfaces.Project",
  "_typeVersion" : "interfaces-22.0.0",
  "cooldownTimeInMinutes" : null,
  "id" : "{project-id-uuid}",
  "name" : "{ProjectName}",
  "notes" : null,
  "recipients" : [ ],
  "responsible" : {
    "_type" : "start.Responsible",
    "_typeVersion" : "start-1.3.2",
    "userId" : "36317f78-6040-4648-936d-e8b66b394c0b"
  }
}
```

Filename: `{ProjectName}-{project-id-uuid}.json` (no spaces; use the project name as-is if it has no spaces, or replace spaces with underscores).

---

### File 4: `interfaces/{InterfaceName}-{interface-id-uuid}.json`

This is the main configuration file. Build it in this order:

**Top-level fields:**

```json
{
  "_type" : "interfaces.InterfaceConfig",
  "_typeVersion" : "interfaces-24.2.017",
  "changeDate" : "{timestamp}",
  "createDate" : "{timestamp}",
  "gid" : "{interface-gid-uuid}",
  "groups" : [ ],
  "id" : "{interface-id-uuid}",
  "logLevel" : "warn",
  "name" : "{InterfaceName}",
  "notes" : null,
  "processors" : [ ... ],
  "projectId" : "{project-id-uuid}",
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

**Fixed values:** `runtime` is always `"b"`. `status` is `"live"` for ready-to-use configs. `typeId` for Lambda interfaces is always `2512c737-a73b-4f78-9ae2-098ac6d291bd`.

**Filename convention:** Replace spaces in the interface name with underscores, then append `-{interface-id-uuid}.json`.

Example: Interface name `"IBAN validation"` → filename `IBAN_validation-af8cb193-e289-48d9-a9b6-36e30941909c.json`

---

### File 5: `export-log.txt` (optional)

A plain text file at the ZIP root. Not required for import. If included, it can contain any informational text. Omitting it entirely is fine.

---

## Step 5: Fill TypeScript Scripts

For each processor, generate the TypeScript and JavaScript content for the `typeScripts` array entries.

### Lambda processor scripts

**`output.ts`** — always the same pattern:
```typescript
// TypeScript source:
import { Output } from './api';
import { Invocation } from '../interface';

export function provideOutput(invocation: Invocation): Output {
  return invocation.processors.iteration.result;
}
```
```javascript
// Compiled JavaScript:
export function provideOutput(invocation) {
    return invocation.processors.iteration.result;
}
```

### Iteration processor scripts

**`data.ts`** — returns the lambda input array:
```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  const r = invocation.processors.lambda.input;
  return r;
}
```
```javascript
export function provideData(invocation) {
    const r = invocation.processors.lambda.input;
    return r;
}
```

**`result.ts`** — returns whichever processor produced output for this iteration item. Adjust the processor names to match your `scriptIdentifier` values:
```typescript
import { Invocation } from '../interface';

export function provideResult(invocation: Invocation) {
  return invocation.processors.prepare.result || invocation.processors.transform.result;
}
```

If `prepare` can return an error result, it comes first. If `prepare` only short-circuits on actual errors (not on valid-but-empty results), you may need `invocation.processors.prepare.result || invocation.processors.transform.result`.

### TypeScript `prepare` scripts

**`attributes.d.ts`** — declare every attribute set with `self.withAttribute()`:
```typescript
export interface Attributes {
  cleanedInput: String  // replace with your actual attribute name and type
}
```

**`script.ts`** — adapt to your input:
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  let data = invocation.processors.iteration.element;
  // ... your cleaning and validation logic ...
  if (/* valid */) {
    self.withOutlet('OK');
    self.withAttribute('cleanedInput', /* cleaned value */);
    return;
  }
  self.withOutlet('Error');
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'Input contains invalid characters'
  };
}
```

### REST Consumer `restConsumer` scripts

**`restapi.d.ts`** — type stubs (keep as `any` unless you need stricter types):
```typescript
export type PathParams = any;
export type QueryParams = any;
export type RequestBody = any;
export type ResponseBody = any;
```

**`script.ts`** — adapt to your API's auth and parameter scheme:
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('{envVarSettingName}'))
    .withQueryParam('format', 'json')
    .withQueryParam('{inputParamName}', invocation.processors.prepare.cleanedInput);
}
```

For header-based auth:
```typescript
self.withHeader('Authorization', `Bearer ${Resolvers.environmentVariables.resolveBySetting('myToken')}`);
```

For path parameters, add `{paramName}` to the `path` in `customConfig`, then:
```typescript
self.withPathParam('paramName', invocation.processors.iteration.element.fieldName);
```

### TypeScript `transform` scripts

**`attributes.d.ts`** — usually empty (transform only returns results):
```typescript
export interface Attributes {
}
```

**`script.ts`** — adapt to your API's response format and outlet names:
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  let response = invocation.processors.restConsumer.body;

  if (invocation.processors.restConsumer.statusCode === 200) {
    // Check for API-level errors
    if (response.errors && response.errors.length) {
      self.withOutlet('Error');
      return {
        "_type": "bsiscout.LambdaResultError",
        displayMessage: response.errors.map((i: any) => i.message).join('. ')
      };
    }
    // Check for invalid result
    if (/* response indicates invalid */) {
      self.withOutlet('Invalid');
      return { valid: false };
    }
    // Extract success data
    self.withOutlet('Valid');
    return {
      valid: true,
      // ... map API response fields to signature output fields
    };
  }

  self.withOutlet('Error');
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'Request failed'
  };
}
```

---

## Step 6: Build the ZIP

Claude cannot create binary ZIP files directly, but can generate all file contents as text. Once the files are saved, use Bash to create the ZIP:

### Workflow

1. Generate all JSON file contents as text blocks in the conversation.
2. Save each file to disk using the Write tool in the correct directory structure.
3. Use Bash to create the ZIP:

```bash
cd /path/to/output-dir && \
zip -r bsi-eip-{YYYY-MM-DD_HH-MM-SS}.zip \
  export-definition.json \
  index.json \
  interfaces/ \
  projects/
```

Or if an `export-log.txt` is included:
```bash
zip -r bsi-eip-{timestamp}.zip export-definition.json export-log.txt index.json interfaces/ projects/
```

### Directory Structure to Create

```
{output-dir}/
├── export-definition.json
├── export-log.txt             (optional)
├── index.json
├── interfaces/
│   └── {Interface_Name}-{interface-id-uuid}.json
└── projects/
    └── {ProjectName}-{project-id-uuid}.json
```

**Multi-package ZIPs**: BSI EIP can export multiple packages in one ZIP, with subfolders like `01-crm/` and `02-interfaces/`. When generating configs that include CRM data model changes (custom codes, custom fields), the ZIP must contain both packages. The `multi-index.json` at the root coordinates the import order. For pure interface-only configs (no CRM model changes), use the standard single-package structure.

---

## Critical Rules

These rules must never be violated. A config that breaks any of them will fail to import or will produce incorrect runtime behavior.

### UUID Rules

1. **Never reuse UUIDs from the IBAN example** (or any other example). Every new config must have fresh UUIDs for all variable entities.
2. **`valueMigrationIds` must be copied verbatim** — all 8, in order, no changes.
3. **`responsible.userId`** is always `36317f78-6040-4648-936d-e8b66b394c0b` — do not change.
4. **Interface type UUID** is always `2512c737-a73b-4f78-9ae2-098ac6d291bd` for Lambda interfaces.
5. **Processor type UUIDs** (e.g. `ffd19a7a` for TypeScript) are fixed system constants — do not change.
6. **Outlet descriptor IDs** are fixed system constants — copy from the table in `outlets-and-routing.md`.

### `outletScriptIds` Rules

7. Keys in `outletScriptIds` must **exactly match** the outlet `name` fields in the `outlets` array.
8. Values in `outletScriptIds` must **exactly match** the outlet `id` fields (not `gid`) in the `outlets` array.
9. The `Standard` outlet is **never listed** in `outletScriptIds`.

### Script Rules

10. Every `TypeScriptConfig` with `scriptKind: "script"` must have both `typeScript` and `javaScript` populated (never `null` for either).
11. `processorId` in each `TypeScriptConfig` must match the processor's `id` (not `gid`).
12. `scriptIdentifier` values must be unique within the interface.

### Structural Rules

13. `runtime` is always `"b"`.
14. `status` is `"live"` for production configs.
15. `version` and `revision` are both `1` for new configs.
16. All processor positions must be unique — no two processors at the same (x, y).
17. `connectorPoints` in outlet configs is always `[]`.

---

## Pre-Generation Checklist

Before outputting the final ZIP content, verify:

- [ ] All UUIDs are freshly generated (not copied from any example)
- [ ] `valueMigrationIds` contains exactly the 8 fixed UUIDs
- [ ] `responsible.userId` is the admin UUID everywhere
- [ ] Interface `typeId` is the Lambda UUID
- [ ] Lambda processor `typeId` is `ec06bfe3-...`
- [ ] Iteration processor `typeId` is `21c361ec-...`
- [ ] TypeScript processor `typeId` is `ffd19a7a-...`
- [ ] REST Consumer processor `typeId` is `f069aa44-...`
- [ ] All outlet descriptor IDs match the reference table
- [ ] `outletScriptIds` keys match outlet names, values match outlet IDs
- [ ] No two processors share the same (x, y) coordinates
- [ ] `resourcePath` in index.json matches the actual interface filename
- [ ] Interface filename format: `{Name_underscored}-{interface-id}.json`
- [ ] `typeVersions` only lists processor config types actually used
- [ ] All TypeScript scripts have both `typeScript` and `javaScript` non-null
- [ ] `prepare/attributes.d.ts` declares every `self.withAttribute()` call
- [ ] Environment variable name in `resolveBySetting()` is documented for post-import setup
- [ ] Signature `inputTypeId` = `"List:Dyn:LambdaInput"`, `outputTypeId` = `"List:Dyn:LambdaOutput"`
- [ ] `status` = `"live"`, `runtime` = `"b"`, `published` = `true`

**For CRM batch interfaces additionally verify:**
- [ ] Base URL asked and noted for discovery API calls
- [ ] `qualifiedLambdaId` derived correctly: `interfaces:lambdaProcessor:{lambdaProcessor_gid}:{interface_gid}` (use gid, not id!)
- [ ] `maximumRowCount` set in CRM Data Search
- [ ] `aggregateResults: false` in Iteration (for batch — results not needed)
- [ ] Mutation type verified via discovery API (`/l/cpd-tools/mutationtypes/{name}`)
- [ ] Mandatory mutation fields present in `prepareMutations`
- [ ] Interface typeId is Ad-Hoc (`f72f9f76-...`) not Lambda (`2512c737-...`)

---

## Customization Beyond the Standard Pattern

### No preprocessing needed

If the input requires no cleaning or validation before the API call, `prepare/script.ts` can be simplified to just route straight to `OK`:

```typescript
export function process(invocation: Invocation, self: Self) {
  self.withOutlet('OK');
}
```

Or remove `prepare` entirely and connect Iteration directly to `restConsumer`. In that case, update `iteration/result.ts` to reference `transform.result` directly (no `prepare.result ||`).

### POST request with JSON body

Change `httpMethod` to `"post"` in `customConfig` and use `self.withBody()` in `prepareRequest`:

```typescript
export function prepareRequest(invocation: Invocation, self: Self) {
  self.withBody({
    fieldName: invocation.processors.iteration.element.fieldName
  });
}
```

Also update `restapi.d.ts` to type `RequestBody` appropriately.

### Single success path (no Valid/Invalid distinction)

If the API simply succeeds or fails (no "invalid input" case), use only `OK` and `Error` outlets on `transform`. Remove `Invalid` from `outletScriptIds` and from the `outlets` array.

### Multiple REST calls in sequence

Add a second REST Consumer processor (e.g. `restConsumer2` at x=32) and a second transform processor (`transform2` at x=38). Connect `transform/OK` outlet to `restConsumer2`. Update `iteration/result.ts`:

```typescript
return invocation.processors.prepare.result
  || invocation.processors.transform.result
  || invocation.processors.transform2.result;
```
