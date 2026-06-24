# Environment Variables Reference

## Overview

**Environment variables** are named configuration values stored in BSI EIP system settings. They allow interface configurations to reference secrets (API keys, passwords, tokens) and environment-specific values without hardcoding them into scripts or the exported configuration ZIP.

When you import an interface configuration, the environment variable values are **not included** — they must be configured separately in the target BSI EIP system. This makes it safe to share or version-control configurations.

---

## Configuring Environment Variables in BSI EIP

Environment variables are managed in BSI EIP under **Settings → Environment Variables** as a JSON object. Each key is the variable name; each value describes the stored value and whether it is encrypted.

```json
{
  "ibanApiKey": {
    "_type": "interfaces.EnvironmentVariableValue",
    "_typeVersion": "interfaces-22.0.1001",
    "crypt": false,
    "value": "YOUR-API-KEY-HERE"
  },
  "anotherSecret": {
    "_type": "interfaces.EnvironmentVariableValue",
    "_typeVersion": "interfaces-22.0.1001",
    "crypt": true,
    "value": "ENCRYPTED-VALUE"
  }
}
```

### EnvironmentVariableValue Fields

| Field | Type | Description |
|---|---|---|
| `_type` | string | Always `"interfaces.EnvironmentVariableValue"` |
| `_typeVersion` | string | Always `"interfaces-22.0.1001"` |
| `crypt` | boolean | `false` = value is stored as plain text; `true` = value is stored encrypted |
| `value` | string | The actual value (plain text string, or the encrypted representation if `crypt: true`) |

### `crypt` Field Behavior

- `crypt: false` — the value is stored and displayed as plain text in the settings UI. Use for non-sensitive configuration values.
- `crypt: true` — the value is stored in encrypted form. BSI EIP handles the encryption; you provide the plain text value and the system encrypts it on save.

For generated configurations, always document required environment variables with their key names so the administrator knows what values to configure.

---

## Using Environment Variables in TypeScript Scripts

In TypeScript scripts, access environment variables through the `Resolvers` object imported from `@eip/core`:

```typescript
import { Resolvers } from '@eip/core';
```

Resolve a variable by its key name:

```typescript
const apiKey = Resolvers.environmentVariables.resolveBySetting('ibanApiKey');
```

The call resolves the variable at runtime and returns its string value. If the variable is not configured in the BSI EIP system, an error is thrown at runtime.

---

## Common Use Cases

### API Key as Query Parameter

The most common pattern: pass the API key as a query parameter in the `prepareRequest` function of a TypeScript processor used before a REST Consumer.

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('ibanApiKey'))
    .withQueryParam('format', 'json')
    .withQueryParam('iban', invocation.processors.prepare.cleanedInput);
}
```

### API Key as HTTP Header

For services that expect the key in a header (e.g., `Authorization`, `X-API-Key`):

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withHeader('X-API-Key', Resolvers.environmentVariables.resolveBySetting('myServiceApiKey'))
    .withQueryParam('input', invocation.input.iban);
}
```

### Bearer Token

For OAuth/Bearer token authentication:

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  const token = Resolvers.environmentVariables.resolveBySetting('myServiceBearerToken');
  self
    .withHeader('Authorization', `Bearer ${token}`)
    .withQueryParam('iban', invocation.input.iban);
}
```

### Base URL as Environment Variable

Useful when the API URL differs between test and production environments:

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  const baseUrl = Resolvers.environmentVariables.resolveBySetting('myServiceBaseUrl');
  self
    .withUrl(`${baseUrl}/validate`)
    .withQueryParam('iban', invocation.input.iban);
}
```

---

## Complete Example: REST API with API Key

This shows the full flow: a TypeScript prepare processor using an environment variable, followed by a REST Consumer.

### TypeScript Prepare Processor Script

```typescript
import { Invocation } from '../interface';
import { Self } from './definition';
import { Resolvers } from '@eip/core';

export function prepareRequest(invocation: Invocation, self: Self) {
  self
    .withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('ibanValidationApiKey'))
    .withQueryParam('format', 'json')
    .withQueryParam('iban', invocation.input.iban);
}
```

### Post-Import Configuration

After importing the configuration into BSI EIP, configure the environment variable under **Settings → Environment Variables**:

```json
{
  "ibanValidationApiKey": {
    "_type": "interfaces.EnvironmentVariableValue",
    "_typeVersion": "interfaces-22.0.1001",
    "crypt": false,
    "value": "YOUR-ACTUAL-API-KEY"
  }
}
```

---

## Best Practices

### 1. Always Use Environment Variables for Secrets

Never hardcode API keys, passwords, tokens, or credentials directly in scripts. Always use `Resolvers.environmentVariables.resolveBySetting(...)`.

Bad:
```typescript
self.withQueryParam('api_key', 'abc123secretkey');
```

Good:
```typescript
self.withQueryParam('api_key', Resolvers.environmentVariables.resolveBySetting('myServiceApiKey'));
```

### 2. Use Descriptive Key Names

Key names should be specific enough to identify the service and purpose. Avoid generic names.

| Bad | Good |
|---|---|
| `"key"` | `"ibanValidationApiKey"` |
| `"apikey"` | `"ibanApiKey"` |
| `"password"` | `"openIbanApiKey"` |
| `"url"` | `"ibanServiceBaseUrl"` |

### 3. Document Required Variables

When generating or delivering an interface configuration, always document every environment variable it requires. Include:
- The exact key name
- What value it expects
- Where to obtain the value

Example documentation to include in interface notes:

> **Required Environment Variables**
>
> | Key | Description |
> |---|---|
> | `ibanValidationApiKey` | API key for the IBAN validation service. Obtain from: https://example.com/api |
> | `ibanServiceBaseUrl` | Base URL of the IBAN service, e.g. `https://api.example.com/v1` |

### 4. The Configuration ZIP Does Not Contain Variable Values

The exported configuration ZIP contains only the interface structure and scripts. Environment variable values are **never exported**. After import, an administrator must manually configure all required environment variables before the interface can run successfully.

### 5. Test Environment Isolation

Use different environment variable values per BSI EIP environment (dev, test, production) to point to the appropriate external service endpoints and use appropriate API credentials.

---

## Naming Convention Summary

Follow these conventions for environment variable key names:

- Use **camelCase** (e.g., `ibanApiKey`, not `IBAN_API_KEY` or `iban-api-key`)
- Include the **service name** in the key (e.g., `ibanValidationApiKey`, `openIbanApiKey`)
- For URLs: suffix with `BaseUrl` (e.g., `ibanServiceBaseUrl`)
- For API keys: suffix with `ApiKey` (e.g., `ibanValidationApiKey`)
- For tokens: suffix with `Token` or `BearerToken` (e.g., `myServiceBearerToken`)
- For passwords: suffix with `Password` (e.g., `dbPassword`)
