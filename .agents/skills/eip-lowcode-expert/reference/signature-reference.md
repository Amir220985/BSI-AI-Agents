# Lambda Signature Reference

## Overview

A **Signature** defines the callable contract of a Lambda interface: what inputs it expects and what outputs it returns. The signature is the API surface that callers use when invoking the lambda from outside BSI EIP.

The signature lives inside the `CrmLambdaProcessorConfig` of the **entry Lambda processor** — the first processor in the interface pipeline. It is also what generates the `LambdaInput` and `LambdaOutput` TypeScript interfaces in `api.d.ts`.

---

## Signature Structure

```json
{
  "_type": "bsiscout.Signature",
  "_typeVersion": "bsiscout-24.1.001",
  "id": "{signature-uuid}",
  "name": {
    "en": "IBAN Validation",
    "fr": "Validation de compte IBAN",
    "it": "Verifica IBAN",
    "und": "IBAN Validierung"
  },
  "description": {
    "en": "Validates an IBAN and returns bank metadata.",
    "fr": "Valide un IBAN et retourne les métadonnées bancaires.",
    "it": "Verifica un IBAN e restituisce i metadati bancari.",
    "und": "Validiert eine IBAN und gibt Bankmetadaten zurück."
  },
  "inputTypeId": "List:Dyn:LambdaInput",
  "outputTypeId": "List:Dyn:LambdaOutput",
  "inputs": [ ],
  "outputs": [ ]
}
```

### Fixed Values

| Field | Value | Notes |
|---|---|---|
| `_type` | `"bsiscout.Signature"` | Always this value |
| `_typeVersion` | `"bsiscout-24.1.001"` | Always this value |
| `inputTypeId` | `"List:Dyn:LambdaInput"` | Always this value — do not change |
| `outputTypeId` | `"List:Dyn:LambdaOutput"` | Always this value — do not change |

### Variable Fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Generate a fresh UUID per signature |
| `name` | yes | Localized map — see multilingual format below |
| `description` | yes | Localized map; can be `{}` or omit keys if no description |
| `inputs` | yes | Array of `SignatureProperty` — may be empty |
| `outputs` | yes | Array of `SignatureProperty` — may be empty |

---

## SignatureProperty Structure

Both `inputs` and `outputs` are arrays of `SignatureProperty` objects:

```json
{
  "_type": "bsiscout.SignatureProperty",
  "_typeVersion": "bsiscout-24.1.001",
  "identifier": "iban",
  "name": {
    "en": "IBAN",
    "und": "IBAN"
  },
  "description": null,
  "mandatory": true,
  "type": "Text250"
}
```

### SignatureProperty Fields

| Field | Required | Applies To | Notes |
|---|---|---|---|
| `_type` | yes | both | Always `"bsiscout.SignatureProperty"` |
| `_typeVersion` | yes | both | Always `"bsiscout-24.1.001"` |
| `identifier` | yes | both | camelCase name used in TypeScript code (e.g., `iban`, `bankCode`, `isValid`) |
| `name` | yes | both | Localized display name shown in UI |
| `description` | no | both | Localized description or `null` |
| `mandatory` | yes | inputs only | `true` if the input is required; omit or set to `false` for optional inputs; not needed for outputs |
| `type` | yes | both | Data type — see type reference below |

---

## Available Data Types

> **Full type reference:** All 55+ types with Java types, TypeScript equivalents, and examples: [`data-types-reference.md`](data-types-reference.md)

Most commonly used types:

| Type | Description | TypeScript Equivalent | Notes |
|---|---|---|---|
| `Text60` | Short text up to 60 characters | `string` | Codes: BIC, sort code, postal code, currency |
| `Text250` | Short text up to 250 characters | `string` | Most common text type for API fields |
| `Text500` | Text up to 500 characters | `string` | Error messages, descriptions |
| `Text` | Long text (no length limit) | `string` | LLM outputs, free-form text |
| `Boolean` | true / false | `boolean` | Flags, validation results |
| `Long` | Integer (64-bit) | `number` | Integers, counts |
| `Integer` | Integer (internally: Long) | `number` | Integers |
| `Decimal` | Decimal number | `number` | Amounts, decimal values |
| `Date` | Date only | `string` | ISO `YYYY-MM-DD` |
| `DateTime` | Date and time | `string` | ISO `YYYY-MM-DDTHH:mm:ss` |
| `EmailAddress` | Email with validation | `string` | |
| `PhoneNumber` | Phone number | `string` | |
| `IBAN` | IBAN with formatting | `string` | |
| `URI` | URL/URI | `string` | |
| `EntityKey` | CRM object reference | `string` | |
| `Key:Entity:CrmCode:{uuid}` | CRM code reference | `string` | Reference to a CRM code list; UUID identifies the list; discover via discovery API |
| `Currency` | Currency code (CHF, EUR…) | `string` | |

Weitere Typen (Datum-Varianten, Binärdaten, Vektoren, System-Typen) → [`data-types-reference.md`](data-types-reference.md).

**Rules of thumb:**
- Short codes and identifiers → `Text60`
- Normal text inputs → `Text250`
- Yes/No fields → `Boolean` (not `Text`)
- Numbers → `Long` (integer) or `Decimal` (decimal)

---

## Multilingual Name Format

Names and descriptions use a map of locale codes to string values:

| Locale Code | Language | Notes |
|---|---|---|
| `"und"` | Default / German | Displayed when no specific locale matches; required in all name fields |
| `"en"` | English | |
| `"fr"` | French | |
| `"it"` | Italian | |

The `"und"` key is the fallback. In a BSI context, `"und"` text is typically the German label.

You can provide only `"und"` when multilingual support is not required:

```json
"name": { "und": "IBAN" }
```

Or provide all four locales for fully localized interfaces:

```json
"name": {
  "en": "Bank Code",
  "fr": "Code bancaire",
  "it": "Codice bancario",
  "und": "Bankleitzahl"
}
```

---

## Dynamic Type IDs

Some type IDs contain embedded identifiers and follow a parameterized pattern:

### `Key:Entity:CrmCode:{uuid}`

Used when a signature field represents a CRM code list selection.

```json
{
  "_type": "bsiscout.SignatureProperty",
  "_typeVersion": "bsiscout-24.1.001",
  "identifier": "score",
  "name": { "en": "Weather score", "und": "Wetterbewertung" },
  "type": "Key:Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c"
}
```

The UUID (`9ac81c27-0a86-459c-ba62-482fee56739c`) is the technical ID of the CRM code list.

**How to find the UUID:**
1. Query `{baseUrl}/l/cpd-tools/codetypes` to list all codetype names
2. Query `{baseUrl}/l/cpd-tools/codetypes/{name}` to see the code values
3. The code list UUID is the same as what appears in `Key:Entity:CrmCode:{uuid}` — it can be found in the CRM data model configuration JSON or from the ZIP's `01-crm/` folder

**TypeScript mapping:**
In TypeScript, this type maps to `string`. The actual runtime value is the UUID of the selected code entry, accessible via `Codes.AttributeUserDefinedCodes.XxxYyy` from `@eip/crm-core`.

**Discovery:** See [`bsi-api-discovery.md`](bsi-api-discovery.md) for how to query the codetype API.

---

## Complete Examples

### Minimal Signature (German Only)

```json
{
  "_type": "bsiscout.Signature",
  "_typeVersion": "bsiscout-24.1.001",
  "id": "{uuid}",
  "name": { "und": "Mein Lambda" },
  "description": { "und": "Beschreibung des Lambdas." },
  "inputTypeId": "List:Dyn:LambdaInput",
  "outputTypeId": "List:Dyn:LambdaOutput",
  "inputs": [
    {
      "_type": "bsiscout.SignatureProperty",
      "_typeVersion": "bsiscout-24.1.001",
      "identifier": "customerId",
      "name": { "und": "Kunden-ID" },
      "description": null,
      "mandatory": true,
      "type": "Text60"
    }
  ],
  "outputs": [
    {
      "_type": "bsiscout.SignatureProperty",
      "_typeVersion": "bsiscout-24.1.001",
      "identifier": "valid",
      "name": { "und": "Gültig" },
      "description": null,
      "type": "Boolean"
    }
  ]
}
```

### Full Signature: IBAN Validation (Four Languages)

```json
{
  "_type": "bsiscout.Signature",
  "_typeVersion": "bsiscout-24.1.001",
  "id": "{uuid}",
  "name": {
    "en": "IBAN Validation",
    "fr": "Validation de compte IBAN",
    "it": "Verifica IBAN",
    "und": "IBAN Validierung"
  },
  "description": {
    "en": "Validates an IBAN and returns bank metadata.",
    "fr": "Valide un IBAN et retourne les métadonnées bancaires.",
    "it": "Verifica un IBAN e restituisce i metadati bancari.",
    "und": "Validiert eine IBAN und gibt Bankmetadaten zurück."
  },
  "inputTypeId": "List:Dyn:LambdaInput",
  "outputTypeId": "List:Dyn:LambdaOutput",
  "inputs": [
    {
      "_type": "bsiscout.SignatureProperty",
      "_typeVersion": "bsiscout-24.1.001",
      "identifier": "iban",
      "name": { "en": "IBAN", "fr": "IBAN", "it": "IBAN", "und": "IBAN" },
      "description": null,
      "mandatory": true,
      "type": "Text250"
    }
  ],
  "outputs": [
    {
      "_type": "bsiscout.SignatureProperty",
      "_typeVersion": "bsiscout-24.1.001",
      "identifier": "valid",
      "name": { "en": "Valid", "fr": "Valide", "it": "Valido", "und": "Gültig" },
      "description": null,
      "type": "Boolean"
    },
    {
      "_type": "bsiscout.SignatureProperty",
      "_typeVersion": "bsiscout-24.1.001",
      "identifier": "bankCode",
      "name": { "en": "Bank Code", "fr": "Code bancaire", "it": "Codice bancario", "und": "Bankleitzahl" },
      "description": null,
      "type": "Text60"
    },
    {
      "_type": "bsiscout.SignatureProperty",
      "_typeVersion": "bsiscout-24.1.001",
      "identifier": "bankName",
      "name": { "en": "Bank Name", "fr": "Nom de la banque", "it": "Nome della banca", "und": "Bankname" },
      "description": null,
      "type": "Text250"
    },
    {
      "_type": "bsiscout.SignatureProperty",
      "_typeVersion": "bsiscout-24.1.001",
      "identifier": "bic",
      "name": { "en": "BIC", "fr": "BIC", "it": "BIC", "und": "BIC" },
      "description": null,
      "type": "Text60"
    }
  ]
}
```

---

## Relation to `api.d.ts`

The signature defines the TypeScript types available in every processor's script through `api.d.ts`. The mapping from signature to TypeScript is:

### Type Mapping

| Signature Type | TypeScript Type |
|---|---|
| `Text250` | `string` |
| `Text60` | `string` |
| `Text` | `string` |
| `Boolean` | `boolean` |
| `Decimal` | `number` |
| `Long` | `number` |
| `Date` | `string` |
| `DateTime` | `string` |

### Optionality Mapping

- Input properties with `mandatory: true` → required field (no `?`)
- Input properties with `mandatory: false` or missing → optional field (`?`)
- Output properties → always optional (`?`), because the lambda may not always populate every field

### Example Mapping

Given the IBAN Validation signature above, the generated `api.d.ts` would contain:

```typescript
// Generated from signature.inputs
export interface LambdaInput {
  iban: string;         // mandatory: true → required
}

// Generated from signature.outputs
export interface LambdaOutput {
  valid?: boolean;      // Boolean → boolean, outputs are always optional
  bankCode?: string;    // Text60 → string
  bankName?: string;    // Text250 → string
  bic?: string;         // Text60 → string
}
```

In TypeScript scripts, the invocation input is accessed as:

```typescript
export function execute(invocation: Invocation, self: Self) {
  const iban: string = invocation.input.iban;
  // invocation.input is typed as LambdaInput
}
```

And outputs are set as:

```typescript
invocation.output.valid = true;
invocation.output.bankCode = 'XXXXXX';
// invocation.output is typed as LambdaOutput
```

---

## Common Mistakes

- **Omitting `"und"` from name maps** — `"und"` is the required fallback locale; always include it.
- **Using `mandatory` on output properties** — outputs are never mandatory; the field only applies to inputs.
- **Using non-camelCase identifiers** — identifiers become TypeScript property names; use `camelCase` (`bankCode`, not `bank_code` or `BankCode`).
- **Choosing `Text` when `Text250` or `Text60` suffices** — prefer narrower types; `Text` is for genuinely long content.
- **Forgetting to update `api.d.ts`** — when the signature changes, the TypeScript interface file must be regenerated to match.
- **Duplicating identifier names** — each identifier must be unique within `inputs` and unique within `outputs`; the same name can appear in both if semantically appropriate.
- **Using `EntityKey` instead of `Key:Entity:CrmCode:{uuid}` for code list fields** — when an output represents a CRM code selection (e.g., a status or category code), use `Key:Entity:CrmCode:{uuid}` with the specific code list UUID. Use `EntityKey` for free-form CRM object references.
