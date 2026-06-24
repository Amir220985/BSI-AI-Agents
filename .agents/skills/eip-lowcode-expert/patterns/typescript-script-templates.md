# TypeScript Script Templates for BSI EIP

Complete, ready-to-use TypeScript templates for all script types. Copy, adapt field names, and use directly.

## Key Rules

Before writing any script, remember:

- Always import `Invocation` from `'../interface'` (one level up from the processor folder)
- Always import `Self` from `'./definition'` — this is auto-generated and read-only; it declares available outlets and attributes
- Use `LOG` from `'@eip/core'` for logging (`LOG.error(...)`, `LOG.warn(...)`, `LOG.info(...)`)
- Use `Resolvers` from `'@eip/core'` to read environment variables
- The `javaScript` field in the config holds the compiled ES5 output. When generating configs without a compiler available, set `javaScript: null` — the system compiles TypeScript on save
- Auto-generated files (`readOnly: true`) must be included in the config but never manually edited; set `javaScript: null` for them
- `self.withOutlet()` selects the routing outlet; if omitted, the `Standard` outlet is used
- `self.withAttribute()` stores a value that downstream processors can read as `invocation.processors.<name>.<attributeId>`
- The function name matters: TypeScript processors use `process()`, Lambda uses `provideOutput()`, Iteration uses `provideData()` and `provideResult()`, REST Consumer uses `prepareRequest()`

## Standard Scripts by Processor Type

### Lambda `output.ts`

Returns the final output of the Lambda. For the Iteration pattern, this is always `iteration.result` (the collected array).

```typescript
import { Output } from './api';
import { Invocation } from '../interface';

export function provideOutput(invocation: Invocation): Output {
  return invocation.processors.iteration.result;
}
```

Compiled JS:
```javascript
export function provideOutput(invocation) {
    return invocation.processors.iteration.result;
}
```

### Iteration `data.ts`

Returns the array to iterate over. Almost always the Lambda input.

```typescript
import { Invocation } from '../interface';

export function provideData(invocation: Invocation) {
  const r = invocation.processors.lambda.input;
  return r;
}
```

Compiled JS:
```javascript
export function provideData(invocation) {
    const r = invocation.processors.lambda.input;
    return r;
}
```

### Iteration `result.ts`

Returns the per-item result to be collected into the array. The `||` picks whichever processor ran last: `prepare` if it short-circuited with a validation error, `transform` if the API was called.

```typescript
import { Invocation } from '../interface';

export function provideResult(invocation: Invocation) {
  return invocation.processors.prepare.result || invocation.processors.transform.result;
}
```

Compiled JS:
```javascript
export function provideResult(invocation) {
    return invocation.processors.prepare.result || invocation.processors.transform.result;
}
```

If there is no `prepare` processor (Iteration connects directly to REST Consumer):
```typescript
import { Invocation } from '../interface';

export function provideResult(invocation: Invocation) {
  return invocation.processors.transform.result;
}
```

### TypeScript `prepare/script.ts`

Input cleaning and validation. Routes `OK` (proceed to API) or `Error` (early exit with error result).

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

Compiled JS (real output from IBAN example):
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

Note: The attribute declared via `self.withAttribute('cleanedIban', ...)` must be declared in `prepare/attributes.d.ts`:
```typescript
export interface Attributes {
  cleanedIban: String
}
```

### REST Consumer `script.ts`

Prepares the outgoing HTTP request. GET example with API key from environment settings.

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

Compiled JS (real output from IBAN example):
```javascript
import { Resolvers } from '@eip/core';
export function prepareRequest(invocation, self) {
    self
        .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('ibanApiKey'))
        .withQueryParam('format', 'json')
        .withQueryParam('iban', invocation.processors.prepare.cleanedIban);
}
```

The REST Consumer `Self` interface methods:
- `withQueryParam(name, value)` — appends a URL query parameter
- `withPathParam(name, value)` — fills a `{placeholder}` in the path
- `withHeader(name, value)` — adds an HTTP header
- `withCookie(name, value)` — adds a cookie
- `withBody(value)` — sets the request body (POST/PUT only)

There is no `withOutlet()` on REST Consumer — routing is purely by HTTP status code (Standard outlet for 2xx, Sonstige for others).

### TypeScript `transform/script.ts`

Parses the API response, routes `Valid` / `Invalid` / `Error`. This is the real script from the IBAN example.

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

Compiled JS (real output from IBAN example):
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

### Test File `testIbanValidation.ts`

Tests use the `TestDriver` harness. Key patterns: `startWith` / `stopAfter` to isolate a processor, `processorAttributes` to inject mock state.

This is the real test file from the IBAN example:

```typescript
import { TestDriver } from './testDefinition';
import { describe, test, expect } from '@eip/testing';

describe('IBAN validiation', () => {

  test('ValidIban', () => {
    let testInvocation = TestDriver.createTest()
      .startWith('transform')
      .stopAfter('transform')
      .processorAttributes('restConsumer', a => a.attributes({
        "body": {
          "bank_data": {
            "account": "0532013000",
            "address": "Venloer Str. 288",
            "bank": "Commerzbank",
            "bank_code": "37040044",
            "bic": "COBADEFFXXX",
            "branch": null,
            "branch_code": "",
            "city": "Köln",
            "country": "Germany",
            "country_iso": "DE",
            "email": null,
            "fax": null,
            "phone": null,
            "state": null,
            "www": null,
            "zip": "50447"
          },
          "errors": [],
          "sepa_data": {
            "B2B": "YES",
            "COR1": "YES",
            "SCC": "YES",
            "SCT": "YES",
            "SDD": "YES"
          },
          "validations": {
            "account": { "code": "002", "message": "Account Number check digit is correct" },
            "chars": { "code": "006", "message": "IBAN does not contain illegal characters" },
            "country_support": { "code": "007", "message": "Country supports IBAN standard" },
            "iban": { "code": "001", "message": "IBAN Check digit is correct" },
            "length": { "code": "003", "message": "IBAN Length is correct" },
            "structure": { "code": "005", "message": "IBAN structure is correct" }
          }
        },
        "cookies": {},
        "statusCode": 200
      }))
      .test();

    let result = testInvocation.processors.transform.result;

    expect(result.valid).toBeTrue;
    expect(result.bic).toBe('COBADEFFXXX');
    expect(result.bankCode).toBe('37040044');
    expect(result.bankName).toBe('Commerzbank');
  });

  test('InvalidIban', () => {
    let testInvocation = TestDriver.createTest()
      .startWith('transform')
      .stopAfter('transform')
      .processorAttributes('restConsumer', a => a.attributes({
        "body": {
          "bank_data": {
            "account": "0532019000",
            "address": "",
            "bank": "",
            "bank_code": "34040044",
            "bic": "",
            "branch": "",
            "branch_code": "",
            "city": "",
            "country": "Germany",
            "country_iso": "DE",
            "email": "",
            "fax": "",
            "phone": "",
            "state": "",
            "www": "",
            "zip": ""
          },
          "errors": [],
          "sepa_data": {
            "B2B": "NO",
            "COR1": "NO",
            "SCC": "NO",
            "SCT": "NO",
            "SDD": "NO"
          },
          "validations": {
            "account": { "code": "201", "message": "Account Number check digit not correct" },
            "chars": { "code": "006", "message": "IBAN does not contain illegal characters" },
            "country_support": { "code": "007", "message": "Country supports IBAN standard" },
            "iban": { "code": "202", "message": "IBAN Check digit not correct" },
            "length": { "code": "003", "message": "IBAN Length is correct" },
            "structure": { "code": "005", "message": "IBAN structure is correct" }
          }
        },
        "cookies": {},
        "statusCode": 200
      }))
      .test();

    expect(testInvocation.outlet).toEqual('Invalid');
  });

  test('404', () => {
    let testInvocation = TestDriver.createTest()
      .startWith('transform')
      .stopAfter('transform')
      .processorAttributes('restConsumer', a => a.attributes({
        "statusCode": 404
      }))
      .test();

    expect(testInvocation.outlet).toEqual('Error');
  });

  test('InvalidAPIKey', () => {
    let testInvocation = TestDriver.createTest()
      .startWith('transform')
      .stopAfter('transform')
      .processorAttributes('restConsumer', a => a.attributes({
        "body": {
          "bank_data": {},
          "errors": [
            {
              "code": "301",
              "message": "API Key is invalid"
            }
          ],
          "sepa_data": {},
          "validations": {}
        },
        "cookies": {},
        "statusCode": 200
      }))
      .test();

    expect(testInvocation.outlet).toEqual('Error');
    expect(testInvocation.processors.transform.result.displayMessage).toBe('API Key is invalid');
  });
});
```

Key TestDriver patterns:
- `.startWith('transform')` — begins execution at the `transform` processor, skipping everything before it
- `.stopAfter('transform')` — stops execution after `transform` (useful when transform has no downstream)
- `.processorAttributes('restConsumer', a => a.attributes({...}))` — injects mock attributes into a processor, as if it had already run
- `testInvocation.outlet` — the name of the outlet the last processor routed to
- `testInvocation.processors.transform.result` — the return value of the `process()` function

---

## Template Library

The following templates are complete, working scripts for common variations. Adapt field names and API-specific logic.

### Template 1: Simple Pass-Through Lambda (Invoke Lambda Pattern)

A Lambda that calls another Lambda and returns its result directly. No Iteration, no REST Consumer.

**`lambda/output.ts`:**
```typescript
import { Output } from './api';
import { Invocation } from '../interface';

export function provideOutput(invocation: Invocation): Output {
  return invocation.processors.invokeOtherLambda.result;
}
```

**`invokeOtherLambda/script.ts`** (TypeScript processor that invokes another Lambda):
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  let input = invocation.processors.lambda.input;
  // Build the call payload for the downstream Lambda
  self.withAttribute('callPayload', input);
  self.withOutlet('OK');
}
```

---

### Template 2: REST API with POST Body

Input data is sent as a JSON body in a POST request. The `customConfig` must have `httpMethod: "post"`.

**`prepare/script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  let data = invocation.processors.iteration.element;

  if (!data.email || data.email.trim().length === 0) {
    self.withOutlet('Error');
    return {
      "_type": "bsiscout.LambdaResultError",
      displayMessage: 'Email address is required'
    };
  }

  self.withOutlet('OK');
  self.withAttribute('payload', {
    email: data.email.toLowerCase().trim(),
    firstName: data.firstName,
    lastName: data.lastName
  });
}
```

**`restConsumer/script.ts`** (POST with JSON body):
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withHeader('Authorization', 'Bearer ' + Resolvers.environmentVariables.resolveBySetting('myApiToken'))
    .withHeader('Content-Type', 'application/json')
    .withBody(invocation.processors.prepare.payload);
}
```

**`transform/script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { LOG } from '@eip/core';

export function process(invocation: Invocation, self: Self) {
  if (invocation.processors.restConsumer.statusCode === 201 ||
      invocation.processors.restConsumer.statusCode === 200) {
    let body = invocation.processors.restConsumer.body;
    self.withOutlet('OK');
    return {
      success: true,
      externalId: body.id
    };
  }

  LOG.error('API returned status ' + invocation.processors.restConsumer.statusCode);
  self.withOutlet('Error');
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'Failed to create record in external system'
  };
}
```

---

### Template 3: REST API with Path Parameters

The input value is part of the URL path, not a query parameter. Example: `GET /api/v1/persons/{personId}`.

**`restConsumer/restapi.d.ts`** (declare path param types — editable, not readOnly):
```typescript
export type PathParams = { personId: string };
export type QueryParams = any;
export type RequestBody = any;
export type ResponseBody = any;
```

**`restConsumer/script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withHeader('X-Api-Key', Resolvers.environmentVariables.resolveBySetting('externalApiKey'))
    .withPathParam('personId', invocation.processors.prepare.cleanedPersonId);
}
```

The REST Consumer `customConfig.path` must contain the placeholder: `"/api/v1/persons/{personId}"`.

**`transform/script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

export function process(invocation: Invocation, self: Self) {
  let statusCode = invocation.processors.restConsumer.statusCode;

  if (statusCode === 404) {
    self.withOutlet('NotFound');
    return { found: false };
  }

  if (statusCode === 200) {
    let person = invocation.processors.restConsumer.body;
    self.withOutlet('Found');
    return {
      found: true,
      name: person.fullName,
      email: person.email
    };
  }

  self.withOutlet('Error');
  return {
    "_type": "bsiscout.LambdaResultError",
    displayMessage: 'Unexpected status: ' + statusCode
  };
}
```

---

### Template 4: Multi-Step Validation in prepare

Two validations before calling the API: format check (regex), then range/business logic check.

**`prepare/script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';

const AMOUNT_REGEX = /^\d+(\.\d{1,2})?$/;
const MAX_AMOUNT = 1_000_000;

export function process(invocation: Invocation, self: Self) {
  let data = invocation.processors.iteration.element;
  let rawAmount = String(data.amount || '').trim();

  // Step 1: Format check
  if (!AMOUNT_REGEX.test(rawAmount)) {
    self.withOutlet('Error');
    return {
      "_type": "bsiscout.LambdaResultError",
      displayMessage: 'Amount must be a number with at most 2 decimal places'
    };
  }

  let amount = parseFloat(rawAmount);

  // Step 2: Range check
  if (amount <= 0 || amount > MAX_AMOUNT) {
    self.withOutlet('Error');
    return {
      "_type": "bsiscout.LambdaResultError",
      displayMessage: 'Amount must be between 0.01 and 1,000,000'
    };
  }

  self.withOutlet('OK');
  self.withAttribute('normalizedAmount', amount);
  self.withAttribute('currency', (data.currency || 'CHF').toUpperCase());
}
```

**`prepare/attributes.d.ts`** (declare the two attributes):
```typescript
export interface Attributes {
  normalizedAmount: number;
  currency: string;
}
```

**`restConsumer/script.ts`:**
```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withQueryParam('apiKey', Resolvers.environmentVariables.resolveBySetting('fxApiKey'))
    .withQueryParam('amount', String(invocation.processors.prepare.normalizedAmount))
    .withQueryParam('currency', invocation.processors.prepare.currency);
}
```

---

### Template 5: Error Accumulation Pattern

The `transform` processor collects multiple validation errors into a single error message, rather than failing on the first one.

```typescript
import { Self } from './definition';
import { Invocation } from '../interface';
import { LOG } from '@eip/core';

export function process(invocation: Invocation, self: Self) {
  let statusCode = invocation.processors.restConsumer.statusCode;
  let body = invocation.processors.restConsumer.body;

  if (statusCode !== 200) {
    self.withOutlet('Error');
    return {
      "_type": "bsiscout.LambdaResultError",
      displayMessage: 'API call failed with status ' + statusCode
    };
  }

  // Accumulate all validation errors
  let errors: string[] = [];

  if (body.fieldErrors) {
    for (let fieldError of body.fieldErrors) {
      errors.push(fieldError.field + ': ' + fieldError.message);
    }
  }

  if (body.globalErrors) {
    for (let globalError of body.globalErrors) {
      errors.push(globalError.message);
    }
  }

  if (errors.length > 0) {
    let combinedMessage = errors.join('; ');
    LOG.warn('Validation errors: ' + combinedMessage);
    self.withOutlet('Invalid');
    return {
      "_type": "bsiscout.LambdaResultError",
      displayMessage: combinedMessage
    };
  }

  self.withOutlet('Valid');
  return {
    valid: true,
    confirmedId: body.confirmedId
  };
}
```

---

## The `javaScript` Field

Each `TypeScriptConfig` in the JSON has both `typeScript` (source) and `javaScript` (compiled output) fields.

**When generating configs:**
- Set `javaScript: null` if you only have TypeScript — the system will compile it when the interface is imported or saved
- Set `javaScript` to the compiled string if you want to include the precompiled version (faster import, no compile step needed)

**Compilation rules:**
- Type annotations are stripped
- `import type` statements are removed
- Regular `import` statements for runtime values (like `LOG`, `Resolvers`) are preserved
- The output is ES module format (uses `export function`, not `module.exports`)
- No minification — comments are preserved

**Real compiled outputs from IBAN example** (verbatim, for reference):

`prepare/script.ts` compiled:
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

`restConsumer/script.ts` compiled:
```javascript
import { Resolvers } from '@eip/core';
export function prepareRequest(invocation, self) {
    self
        .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('ibanApiKey'))
        .withQueryParam('format', 'json')
        .withQueryParam('iban', invocation.processors.prepare.cleanedIban);
}
```

`transform/script.ts` compiled:
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

`iteration/data.ts` compiled:
```javascript
export function provideData(invocation) {
    const r = invocation.processors.lambda.input;
    return r;
}
```

`iteration/result.ts` compiled:
```javascript
export function provideResult(invocation) {
    return invocation.processors.prepare.result || invocation.processors.transform.result;
}
```

`lambda/output.ts` compiled:
```javascript
export function provideOutput(invocation) {
    return invocation.processors.iteration.result;
}
```
