# BSI EIP TypeScript Scripting API Reference

Complete reference for TypeScript scripts within BSI EIP processor configurations. Covers all available modules, objects, function signatures, and patterns.

---

## Module Imports

Every TypeScript script in BSI EIP uses module imports. The exact import paths depend on whether the script is at the interface level or inside a specific processor directory.

```typescript
// Core invocation context — always present
import { Invocation } from '../interface';      // from inside a processor subdirectory
import { Invocation } from './interface';       // from the interface root (rare)

// Processor-specific Self type — only in scripts that receive 'self'
import { Self } from './definition';

// Global logger — available everywhere
import { LOG } from '@eip/core';

// Value resolvers (env vars, code tables, etc.)
import { Resolvers } from '@eip/core';

// Utility types used in generated .d.ts files
import { Flatten, MapLike } from '@eip/core';
```

---

## The `Invocation` Object

The `invocation` parameter is passed to every script function. It provides read-only access to the execution context: input data, upstream processor results, and error state.

### Shape

```typescript
interface Invocation {
  // Access attributes of any processor in this interface, keyed by scriptIdentifier
  processors: {
    [scriptIdentifier: string]: ProcessorAttributes;
  };

  // Interface-level attributes (rarely used directly)
  attributes: InvocationAttributes;

  // Error management
  setError(value: any): void;
  getError(): any;
  hasError(): boolean;
  resetError(): void;
}
```

### The `scriptIdentifier`

Each processor has a `scriptIdentifier` — a camelCase string you assign in the config JSON. This is the key used to access that processor's attributes via `invocation.processors.<scriptIdentifier>`. Examples: `"lambda"`, `"iteration"`, `"validateIban"`, `"ibanApiCall"`.

---

## Processor Attribute Access Patterns

### Lambda Processor (`scriptIdentifier: "lambda"` by convention)

```typescript
invocation.processors.lambda.input          // Input[] — array of input objects from the caller
invocation.processors.lambda.callingUserId  // string — user ID who invoked this lambda
```

`input` contains one object per invocation item, with fields matching the signature's `inputs` definition:
```typescript
// If signature has inputs: [{name: "iban"}, {name: "countryCode"}]
const item = invocation.processors.lambda.input[0];
item.iban        // string
item.countryCode // string
```

### Iteration Processor (`scriptIdentifier: "iteration"` by convention)

```typescript
invocation.processors.iteration.element   // Current array item being processed (single object)
invocation.processors.iteration.index     // number — zero-based position in input array
invocation.processors.iteration.result    // Output[] — accumulated results from all iterations so far
```

The type of `element` is automatically inferred from `provideData()`'s return type.

### TypeScript Processor (any `scriptIdentifier`)

```typescript
invocation.processors.myProcessor.result           // Return value of process()
invocation.processors.myProcessor.cleanedIban      // Custom attribute set via self.withAttribute('cleanedIban', ...)
invocation.processors.myProcessor.validationScore  // Any other attribute set via self.withAttribute()
```

The available attributes are defined in the processor's `attributes.d.ts` and extended by the `result` field via `api.d.ts`.

### REST Consumer Processor (any `scriptIdentifier`)

```typescript
invocation.processors.ibanApiCall.body        // ResponseBody — parsed JSON response body
invocation.processors.ibanApiCall.statusCode  // number — HTTP status code (200, 404, 500, ...)
invocation.processors.ibanApiCall.headers     // MapLike<string, string> — response headers
invocation.processors.ibanApiCall.cookies     // MapLike<string, string> — response cookies
```

`MapLike<string, string>` supports standard property access: `headers['Content-Type']`.

---

## The `Self` Object

The `self` parameter controls the processor's output and routing. Its interface differs by processor type.

### TypeScript Processor `Self`

Used in the `process(invocation, self)` function of a TypeScript processor:

```typescript
interface Self {
  // Store a named value on this processor, accessible to all downstream processors
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;

  // Route execution to a named outlet (must match an outlet name in the config)
  withOutlet(outletId: Outlet): Self;
}
```

Both methods return `Self`, so calls can be chained:

```typescript
return self
  .withOutlet('OK')
  .withAttribute('cleanedIban', iban)
  .withAttribute('bankCode', iban.substring(4, 12));
```

**Rules:**
- You can call `withAttribute` without calling `withOutlet` — routing defaults to `Standard`
- You can call `withOutlet` without calling `withAttribute` — no attributes are stored
- Calling `withOutlet` multiple times overwrites the previous outlet selection
- `Outlet` type is defined in `definition.d.ts` and lists all non-Standard outlet names

### REST Consumer `Self`

Used in the `prepareRequest(invocation, self)` function:

```typescript
interface Self {
  // Add an HTTP request header
  withHeader(name: string, value: string): Self;

  // Add a cookie to the request
  withCookie(name: string, value: string): Self;

  // Fill a path parameter placeholder (e.g. /users/{userId}/)
  withPathParam<T extends keyof PathParams>(paramId: T, value: PathParams[T]): Self;

  // Add a query string parameter (supports multiple values for the same key)
  withQueryParam<T extends keyof QueryParams>(paramId: T, ...value: QueryParams[T][]): Self;
}
```

**Note:** `prepareRequest` does not return a value. Side effects on `self` configure the request.

```typescript
export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withHeader('Accept', 'application/json')
    .withHeader('Authorization', `Bearer ${Resolvers.environmentVariables.resolveBySetting('apiToken')}`)
    .withPathParam('userId', invocation.processors.iteration.element.userId)
    .withQueryParam('expand', 'addresses', 'contacts')
    .withQueryParam('format', 'json');
}
```

---

## The `LOG` Object

Global structured logger. Available in all script files via `import { LOG } from '@eip/core'`.

```typescript
// Log at different severity levels
LOG.trace(message: string): void;
LOG.debug(message: string): void;
LOG.info(message: string): void;
LOG.warn(message: string): void;
LOG.error(message: string): void;

// Check if a level is enabled before constructing expensive messages
LOG.isTraceEnabled(): boolean;
LOG.isDebugEnabled(): boolean;
LOG.isInfoEnabled(): boolean;
LOG.isWarnEnabled(): boolean;
LOG.isErrorEnabled(): boolean;
```

**Usage patterns:**

```typescript
// Simple message
LOG.info('Starting IBAN validation');

// With dynamic data (guard expensive string ops behind level check)
if (LOG.isDebugEnabled()) {
  LOG.debug(`Validating IBAN: ${iban} for user ${invocation.processors.lambda.callingUserId}`);
}

// Error logging
LOG.error(`Unexpected status code: ${invocation.processors.apiCall.statusCode}`);
```

---

## The `Resolvers` Object

Resolves configuration values from the BSI platform at runtime. Available via `import { Resolvers } from '@eip/core'`.

### Environment Variables

```typescript
// Resolve by setting key (key is defined in the interface's settings configuration)
const apiKey: string = Resolvers.environmentVariables.resolveBySetting('myApiKey');
```

Setting keys are strings that map to environment-specific values (dev / test / prod). The resolved value is always a `string`.

### Other Resolvers

Additional resolvers may be available depending on system configuration:

```typescript
Resolvers.codes          // BSI code table resolver — resolves coded values to labels
Resolvers.collections    // Collection resolver — resolves collection members
```

---

## Script Names, Functions, and Return Values

### Lambda Processor — `output.ts`

**Function signature:**
```typescript
export function provideOutput(invocation: Invocation): Output
```

**Purpose:** Returns the final output array sent back to the lambda caller.

**Return value:** Must be an array of objects matching the signature's output fields. Typically sourced from `invocation.processors.iteration.result`.

```typescript
import { Invocation } from '../interface';

export function provideOutput(invocation: Invocation) {
  return invocation.processors.iteration.result;
}
```

---

### Iteration Processor — `data.ts`

**Function signature:**
```typescript
export function provideData(invocation: Invocation)
```

**Purpose:** Returns the array of items to iterate over.

**Return value:** Must be an array. Each element becomes `invocation.processors.iteration.element` during its iteration.

```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  return invocation.processors.lambda.input;
}
```

---

### Iteration Processor — `result.ts`

**Function signature:**
```typescript
export function provideResult(invocation: Invocation)
```

**Purpose:** Returns the result object for the current iteration item. Called once per item after all `Iteration`-outlet processors have run. The returned value is appended to `invocation.processors.iteration.result`.

**Return value:** Any value or object. Usually the `result` of the last meaningful downstream processor.

```typescript
import { Invocation } from '../interface';

export function provideResult(invocation: Invocation) {
  // Use the last processor's result; fall back to a prior one if needed
  return invocation.processors.enrichData.result
    ?? invocation.processors.validateIban.result;
}
```

---

### TypeScript Processor — `script.ts`

**Function signature:**
```typescript
export function process(invocation: Invocation, self: Self)
```

**Purpose:** Main processing logic. Can return a value (stored as `result`), route to an outlet, or set named attributes.

**Return value options:**

**1. Return a structured object (becomes `result`, routes to `Standard`):**
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

**2. Route to a named outlet and set attributes (return value of `self.withOutlet()`):**
```typescript
export function process(invocation: Invocation, self: Self) {
  const iban = invocation.processors.iteration.element.iban?.trim();
  if (!iban) {
    return self.withOutlet('Error').withAttribute('cleanedIban', null);
  }
  return self.withOutlet('OK').withAttribute('cleanedIban', iban);
}
```

**3. Return a `LambdaResultError` (propagates an error to the lambda caller):**
```typescript
export function process(invocation: Invocation, self: Self) {
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'IBAN is invalid — please provide a valid IBAN'
  };
}
```

**4. No return / void (only outlet routing matters):**
```typescript
export function process(invocation: Invocation, self: Self) {
  self.withOutlet('OK');
  // explicit return not needed; return type is void
}
```

---

### REST Consumer Processor — `script.ts`

**Function signature:**
```typescript
export function prepareRequest(invocation: Invocation, self: Self): void
```

**Purpose:** Configures the outgoing HTTP request. No return value.

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  const element = invocation.processors.iteration.element;
  self
    .withQueryParam('iban', invocation.processors.prepare.cleanedIban)
    .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('ibanApiKey'))
    .withHeader('Accept', 'application/json');
}
```

---

## Script / Function Quick Reference

| Processor Type | Script File | Exported Function | Receives `self`? |
|---|---|---|---|
| Lambda (CrmLambda) | `output.ts` | `provideOutput(invocation)` | No |
| Iteration | `data.ts` | `provideData(invocation)` | No |
| Iteration | `result.ts` | `provideResult(invocation)` | No |
| TypeScript | `script.ts` | `process(invocation, self)` | Yes |
| REST Consumer | `script.ts` | `prepareRequest(invocation, self)` | Yes |

---

## Auto-Generated Type Definition Files

The BSI EIP platform auto-generates `.d.ts` files to give scripts full type safety. These files appear in the config JSON as script entries with `readOnly: true`. You must include them with the correct content when generating configs — they are never written by hand during development, but the generator must produce them accurately.

### Interface-Level `interface.d.ts`

**Location in config:** processorId = null (interface-level), readOnly = true
**Purpose:** Aggregates all processor attributes into a single `Invocation` type used by all scripts.

```typescript
// Auto-generated — one import per processor in the interface
import { _Attributes as _lambdaAttributes } from './lambda/api';
import { _Attributes as _iterationAttributes } from './iteration/api';
import { _Attributes as _validateIbanAttributes } from './validateIban/api';
import { _Attributes as _ibanApiCallAttributes } from './ibanApiCall/api';
// ... one per processor, using scriptIdentifier as the directory name

export interface ProcessorAttributes {
  lambda: _lambdaAttributes;
  iteration: _iterationAttributes;
  validateIban: _validateIbanAttributes;
  ibanApiCall: _ibanApiCallAttributes;
  // one entry per processor, key = scriptIdentifier
}

export interface InvocationAttributes {
  // interface-level attributes (typically empty)
}

export interface Invocation {
  attributes: InvocationAttributes;
  processors: ProcessorAttributes;
  setError(value: any): void;
  getError(): any;
  hasError(): boolean;
  resetError(): void;
}
```

**Generation rule:** One import and one `ProcessorAttributes` entry per processor in the interface, in the order the processors appear in the config.

---

### Per-Processor `api.d.ts`

**Location in config:** processorId = `{this-processor-uuid}`, readOnly = true
**Purpose:** Defines the `_Attributes` type that downstream processors see via `invocation.processors.<scriptIdentifier>`.

**For TypeScript processors:**
```typescript
import { Attributes } from './attributes';
import { process } from './script';

export interface _Attributes extends Omit<Attributes, 'result'> {
  result: ReturnType<typeof process>;
}
```
`Attributes` contains custom attributes (from `self.withAttribute()`). `result` is the return type of `process()`.

**For REST Consumer processors:**
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

**For Iteration processors:**
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
`Flatten<T>` unwraps one level of array — so if `provideData` returns `Item[]`, `element` is `Item`.

**For Lambda processors:**
```typescript
export type Input = LambdaInput[];
export type Output = LambdaOutput[];

export interface _Attributes {
  input: Input;
  callingUserId: string;
}

export interface LambdaInput {
  iban: string;           // one field per signature.inputs entry
  countryCode?: string;   // mandatory: false → optional
}

export interface LambdaOutput {
  isValid: boolean;       // one field per signature.outputs entry
  bic?: string;
}
```
Input/output field types are derived from the `typeId` in the signature fields. Mapping: `Text` → `string`, `Boolean` → `boolean`, `Integer` → `number`, `Decimal` → `number`.

---

### Per-Processor `definition.d.ts`

**Location in config:** processorId = `{this-processor-uuid}`, readOnly = true, scriptKind = `"private-api"`
**Purpose:** Defines the `Self` type available in the processor's script.

**For TypeScript processors:**
```typescript
import { Attributes } from './attributes';

// All non-Standard outlet names; empty union ('never') if no custom outlets
export type Outlet = 'OK' | 'Error';

export interface Self {
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;
  withOutlet(outletId: Outlet): Self;
}
```
If the processor has no custom outlets (only `Standard`), use `export type Outlet = never;` and `withOutlet` will accept no arguments.

**For REST Consumer processors:**
```typescript
import { PathParams, QueryParams, RequestBody } from './restapi';

export interface Self {
  withHeader(name: string, value: string): Self;
  withCookie(name: string, value: string): Self;
  withPathParam<T extends keyof PathParams>(paramId: T, value: PathParams[T]): Self;
  withQueryParam<T extends keyof QueryParams>(paramId: T, ...value: QueryParams[T][]): Self;
}
```

---

### Per-Processor `attributes.d.ts`

**Location in config:** processorId = `{this-processor-uuid}`, readOnly = false
**Purpose:** Declares the custom attributes that this TypeScript processor stores via `self.withAttribute()`. User-editable — must be updated whenever new `withAttribute` calls are added to `script.ts`.

**When the processor stores attributes:**
```typescript
export interface Attributes {
  cleanedIban: string | null;
  bankCode: string;
}
```

**When the processor stores no attributes:**
```typescript
export interface Attributes {}
```

Only TypeScript processors have an `attributes.d.ts`. REST Consumer and other types do not.

---

### Per-Processor `restapi.d.ts`

**Location in config:** processorId = `{this-processor-uuid}`, readOnly = false
**Purpose:** Type stubs for the REST Consumer's request and response shapes. Initially set to `any` for flexibility; can be tightened for type safety.

Only REST Consumer processors have a `restapi.d.ts`.

**Default (permissive, always safe to start with):**
```typescript
export type PathParams = any;
export type QueryParams = any;
export type RequestBody = any;
export type ResponseBody = any;
```

**Tightened (for better type checking):**
```typescript
export type PathParams = {
  userId: string;
};
export type QueryParams = {
  format?: string;
  expand?: string;
};
export type RequestBody = never;
export type ResponseBody = {
  valid: boolean;
  bankCode: string;
  bic: string;
  bankName: string;
};
```

---

## Complete `.d.ts` File Set by Processor Type

| Processor Type | `api.d.ts` | `definition.d.ts` | `attributes.d.ts` | `restapi.d.ts` |
|---|---|---|---|---|
| TypeScript | Yes | Yes | Yes | No |
| REST Consumer | Yes | Yes | No | Yes |
| Iteration | Yes | No | No | No |
| Lambda (CrmLambda) | Yes | No | No | No |
| All others | Usually No | No | No | No |

---

## CRM Integration

### Mutations (`@eip/crm-mutation`)

Import:
```typescript
import { Mutations } from '@eip/crm-mutation';
```

Create and queue a CRM mutation:
```typescript
export function prepareMutations(invocation: Invocation, self: Self) {
  self.withMutations(Mutations.create('CrmCustomerUpdate', {
    customerKey: invocation.processors.customer_iteration.element.id,
    y_weatherScore: invocation.processors.invokeLambda.data[0].score
  }));
}
```

`Mutations.create(mutationType, fields)`:
- `mutationType`: string name from the BSI mutation registry (e.g., `'CrmCustomerUpdate'`, `'CrmTaskCreate'`)
- `fields`: object with mutation-specific field names and values
- Discover available mutations and their fields at `{baseUrl}/l/cpd-tools/mutationtypes/{name}`

`self.withMutations(mutation)`: queues the mutation for execution
`self.withModifiedByUsername(username: string)`: log the mutation under a specific user
`self.withRunAsUsername(username: string)`: execute with another user's permissions

The CRM Mutation processor's `prepareMutations` script (in `data.ts`) uses these APIs. Script function name must be `prepareMutations`.

### CRM Code Constants (`@eip/crm-core`)

Import:
```typescript
import { Codes } from '@eip/crm-core';
```

Access CRM code values:
```typescript
Codes.AttributeUserDefinedCodes.WeatherScoreFantastic  // UUID of the "Fantastisch" code
Codes.AttributeUserDefinedCodes.WeatherScoreGood       // UUID of the "Gut" code
```

Naming convention: `Codes.AttributeUserDefinedCodes.{CodeListName}{CodeValueName}` — both in PascalCase without spaces. The exact constants depend on the BSI instance's data model configuration.

Example usage in scoring logic:
```typescript
const SCORE_TIERS = [
  [8, Codes.AttributeUserDefinedCodes.WeatherScoreFantastic],
  [5, Codes.AttributeUserDefinedCodes.WeatherScoreGood],
  [3, Codes.AttributeUserDefinedCodes.WeatherScoreTolerable],
  [0, Codes.AttributeUserDefinedCodes.WeatherScoreBad],
] as const;
const score = SCORE_TIERS.find(([min]) => total >= min)[1];
```

Discover code values at `{baseUrl}/l/cpd-tools/codetypes/{codeTypeName}`. See `bsi-api-discovery.md`.

### Invoke Lambda Results

When a processor calls `Invoke Lambda`, results are accessed via:
```typescript
invocation.processors.invokeLambda.data          // LambdaOutput[] — array of results
invocation.processors.invokeLambda.data[0].score // first result's output field
invocation.processors.invokeLambda.error         // LambdaError[] — if any errors occurred
```

The `data` array has one entry per lambda invocation input element.

### Local Routines

Call a Local Routine from any TypeScript processor in the same interface:
```typescript
import { LocalRoutines } from '../interface';

const result = LocalRoutines.weatherApi_localRoutine({ city: 'Bern' });
// result is typed as the Output type defined in the routine's types.d.ts
```

Local Routines are synchronous and return the value from `provideOutput`. They run the complete processor chain defined in the routine's "Aufruf" outlet.

### Self in Invoke Lambda (`prepare.ts`)

The Invoke Lambda processor uses `prepare` (not `process`) as its function name, and its self has different methods:
```typescript
export function prepare(invocation: Invocation, self: Self) {
  self.withInput({ city: city });     // set lambda input (single invocation)
  // or:
  self.withInputs([{city: 'A'}, {city: 'B'}]);  // set multiple inputs
  self.withRunAsUsername('admin');    // optional: run as specific user
}
```

### REST Provider response.ts

The REST Provider's script is named `response.ts` (not `script.ts`) and uses `provideResponse` (not `process`):
```typescript
export function provideResponse(invocation: Invocation, self: Self) {
  self.withStatus(200).withBody(resultData);
  // or:
  self.withStatus(400).withBody({ error: 'bad request' });
  self.withHeader('X-Custom', 'value');
}
```

---

## Common Patterns and Idioms

### Null-safe attribute access

```typescript
// Lambda input fields may be absent even if mandatory — always guard
const iban = invocation.processors.iteration.element.iban ?? '';
const cleaned = iban.trim().replace(/\s+/g, '').toUpperCase();
```

### Chaining withAttribute and withOutlet

```typescript
// Chain is fine; methods return Self
return self
  .withOutlet('Valid')
  .withAttribute('cleanedIban', cleaned)
  .withAttribute('bankCode', cleaned.substring(4, 12));
```

### Accessing REST response body safely

```typescript
const body = invocation.processors.ibanApiCall.body;
const statusCode = invocation.processors.ibanApiCall.statusCode;

if (statusCode !== 200 || !body) {
  LOG.warn(`Unexpected response: ${statusCode}`);
  return self.withOutlet('Error');
}

const isValid = body.valid === true;
```

### Resolving environment variables

```typescript
import { Resolvers } from '@eip/core';

// In prepareRequest or process:
const apiKey = Resolvers.environmentVariables.resolveBySetting('ibanApiKey');
// 'ibanApiKey' is the setting key defined in the interface's environment config
```

### Returning early on validation failure

```typescript
export function process(invocation: Invocation, self: Self) {
  const element = invocation.processors.iteration.element;

  if (!element.iban || element.iban.length < 15) {
    return self.withOutlet('Invalid').withAttribute('cleanedIban', null);
  }

  const cleaned = element.iban.trim().replace(/\s+/g, '').toUpperCase();
  return self.withOutlet('Valid').withAttribute('cleanedIban', cleaned);
}
```

### Using iteration index

```typescript
export function provideResult(invocation: Invocation) {
  // Log progress for long-running iterations
  if (LOG.isDebugEnabled()) {
    LOG.debug(`Processed item ${invocation.processors.iteration.index}`);
  }
  return invocation.processors.transform.result;
}
```

---

## Collections

Collections are persistent key-value stores used for stateful processing. Full reference: `reference/collections-api.md`.

### Import

```typescript
import { Collections } from '../../collections';
```

(Path is relative from inside a processor subdirectory.)

### Core API

```typescript
// Read a single value by key
const value = Collections.get('collectionName').get(key);
// Returns the stored value, or undefined if key not found

// Write a value immediately
Collections.get('collectionName').putImmediately(key, value);

// Delete a value immediately
Collections.get('collectionName').removeImmediately(key);

// List entries with filtering
const entries = Collections.get('collectionName').list({
  maxResults: 100,
  valueRestrictions: [
    Collections.jsonPath()
      .property('fieldName')
      .condition(b => b.lt(b.filterPath(), threshold))
  ]
});
// entries: Array<{ key: K, value: V }>
// entries.map(e => e.value.someField)   — extract specific fields
```

### JSON Path Filter Builder

```typescript
Collections.jsonPath()
  .property('retryCount')
  .condition(b => b.lt(b.filterPath(), 5))  // retryCount < 5
// Other comparisons: b.gt, b.eq, b.ne, b.le, b.ge
// b.filterPath() references the value navigated to by .property()
```

---

## Hash Utility

```typescript
import { Hash } from '@eip/utils';

// Compute MD5 hash of any value (string, number, object, array)
const hash = Hash.md5(anyValue);
// Returns: string (hex digest)

// Typical use: change detection
const cached = Collections.get('processedRecords').get(record.id);
if (cached && cached.hash === Hash.md5(record)) {
  // record unchanged — skip
}
```

---

## `invocation.attributes` — Shared State Between Processors

Interface-level attributes persist across the entire processor chain for one run. They are set by writing to `invocation.attributes` directly (not via `self`).

### Declaration

In the interface-level `attributes.d.ts` (processorId: null, readOnly: false):

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

### Writing

```typescript
// In a TypeScript processor's process() function:
invocation.attributes.record = {
  id: parseInt(element.nr),
  task: element.betreff,
  urgency: element.dringlichkeit,
  userName: element.benutzer
};
// Note: mutate invocation.attributes directly — no self.withAttribute() needed
```

### Reading

```typescript
// In any downstream processor:
const record = invocation.attributes.record;
const id = record.id;
```

**Contrast with processor attributes** (set via `self.withAttribute()`):
- `invocation.attributes` — interface-wide, declared in interface-level `attributes.d.ts`, mutated directly
- `self.withAttribute('x', v)` → `invocation.processors.{id}.x` — processor-specific, declared in processor-level `attributes.d.ts`

---

## `self.withAttribute` — Processor-Level Custom Attributes

TypeScript processors can expose named values to downstream processors:

```typescript
// In processor 'validateAndMap':
self.withAttribute('issues', ['error 1', 'error 2']);

// In a downstream processor:
const issues = invocation.processors.validateAndMap.issues;
// Type: string[] (from validateAndMap's attributes.d.ts)
```

**Processor `attributes.d.ts`** (processorId = this processor's UUID, readOnly: false):
```typescript
export interface Attributes {
  issues: string[];
}
```

**`definition.d.ts`** (auto-generated):
```typescript
import { Attributes } from './attributes';

export interface Self {
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;
  withOutlet(outletId: Outlet): Self;
}
```

---

## `outletScriptIds` — Multi-Outlet Routing from TypeScript

TypeScript processors can route to named outlets via `self.withOutlet('name')`. The outlet names must be declared in `customConfig.outletScriptIds`:

### In `customConfig`

```json
{
  "_type": "interfaces.TypeScriptProcessorConfig",
  "_typeVersion": "interfaces-23.2.018",
  "outletScriptIds": {
    "unchanged":       "{outlet-uuid-1}",
    "modify data":     "{outlet-uuid-2}",
    "missing mapping": "{outlet-uuid-3}"
  }
}
```

The values must be the **`id`** of the corresponding `OutletConfig` objects in the `outlets` array.

### In the `outlets` array

Custom outlets (those declared in `outletScriptIds`) use `descriptorId: null`:

```json
{
  "id": "{outlet-uuid-1}",
  "gid": "{outlet-gid-1}",
  "name": "Kein Änderungen",
  "descriptorId": null,
  "executionType": "default",
  "presentation": "default",
  "targetProcessorId": null
}
```

The Standard outlet remains with its regular descriptorId but is typically hidden:
```json
{
  "name": "Standard",
  "descriptorId": "c4b09fff-0dae-4726-bdeb-12fd01ddc2da",
  "presentation": "hidden",
  "targetProcessorId": null
}
```

### In `definition.d.ts` (auto-generated)

```typescript
// The Outlet type is the union of all outletScriptIds keys:
export type Outlet = 'missing mapping' | 'modify data' | 'unchanged';

export interface Self {
  withAttribute<T extends keyof Attributes>(attributeId: T, value: Attributes[T]): Self;
  withOutlet(outletId: Outlet): Self;
}
```

### In `script.ts`

```typescript
export function process(invocation: Invocation, self: Self) {
  if (unchanged) {
    self.withOutlet('unchanged');
    return;
  }
  if (hasIssues) {
    self.withAttribute('issues', issues).withOutlet('missing mapping');
    return;
  }
  self.withOutlet('modify data');
  return mutationObject;  // returned value goes to the next processor as .result
}
```

---

## `ProcessorTypes` — Type-Safe Mutation Builders

`ProcessorTypes` provides typed mutation builders, avoiding manual field construction.

```typescript
import { ProcessorTypes } from '@eip/core';

// Create a task mutation (create or update)
return ProcessorTypes.dataMutation.createModifyTask({
  id: cachedTaskKey,     // undefined = create new task; string = update existing
  highPriority: true,
  subject: 'Task subject',
  responsible: userId    // CRM user key
});
// Return value is passed to CRM Mutation processor via self.withMutations()
```

`id` is the `affectedItemKey` from a previous successful mutation (stored in a collection).

**Note:** `ProcessorTypes.dataMutation` is one of the available mutation namespaces. The exact available namespaces depend on the BSI CRM configuration.

---

## `Resolvers.crmEntities` — CRM Entity Resolution

```typescript
import { Resolvers } from '@eip/core';

// Resolve a CRM user by username
const userId = Resolvers.crmEntities.resolveUser({
  restrictions: {
    username: 'vicky.valetti'   // BSI CRM login name
  }
});
// Returns: string (CRM entity key) | undefined (if not found)
```

---

## CRM Mutation Response (Extended)

The CRM Mutation processor exposes a complete response via `invocation.processors.{id}.response`:

```typescript
// Full MutationResponse type (from api.d.ts):
interface MutationResult {
  mutationRef: string;
  mutationTransactionRef: string;
  affectedItemKey: string;      // CRM key of the created/updated record
  correlationId: string;
  status: string;               // compare to Codes.DataMutationStatus.Ok
  statusCode: string;
  message: string;
}

interface MutationResponse {
  mutationResults: MutationResult[];
  requestRef: string;
  keyMappings: MapLike<string, string>;
  status: 'ok' | 'error' | 'cancelled';
  transactionRef: string;
  errorCode: string;
  errorMessage: string;
  errorMessageOrigin: string;
}
```

### Checking mutation status

```typescript
import { Codes } from '@eip/crm-core';

const resp = invocation.processors.mutation.response;
if (resp.mutationResults[0].status !== Codes.DataMutationStatus.Ok) {
  // mutation failed
  return;
}

// Success — get the created/updated record's CRM key:
const crmKey = resp.mutationResults[0].affectedItemKey;
```

`Codes.DataMutationStatus.Ok` is the string constant representing a successful mutation status.

---

## Type Mapping: Signature Field `typeId` → TypeScript

Used when generating `LambdaInput` / `LambdaOutput` interfaces from signature field definitions:

| Signature `typeId` | TypeScript type |
|---|---|
| `Text` | `string` |
| `Boolean` | `boolean` |
| `Integer` | `number` |
| `Decimal` | `number` |
| `Date` | `string` (ISO date string) |
| `DateTime` | `string` (ISO datetime string) |
| `EntityKey` | `string` |
| Any other / unknown | `any` |

Fields with `mandatory: false` become optional (`?`) in the generated interface.
