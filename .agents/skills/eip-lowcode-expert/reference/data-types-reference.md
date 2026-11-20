# BSI EIP — Data Types Reference

Complete reference of all available data types for `bsiscout.SignatureProperty.type` in Lambda signatures and as field types in composites.

The type ID (string value in the configuration) corresponds to the static `ID` field of the respective Java class in `bsi.scout/com.bsiag.scout.rt.datamodel/.../type/builtin/`.

---

## Types for Lambda Signatures (Practical)

These types are recommended for inputs and outputs in `bsiscout.SignatureProperty`:

### Text Types

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `Text` | `String` | `string` | Unlimited text |
| `Text60` | `String` | `string` | Text up to 60 characters |
| `Text250` | `String` | `string` | Text up to 250 characters (most common text type) |
| `Text500` | `String` | `string` | Text up to 500 characters |
| `PlainText` | `String` | `string` | Long plain text (no formatting) |
| `Html` | `String` | `string` | HTML-formatted text |
| `RichText` | `String` | `string` | Rich text content |

**Which text type to use:**
- Short codes (BIC, postal code): `Text60`
- Names, labels, short values: `Text250`
- Descriptions, error messages: `Text500` or `Text`
- LLM outputs, free-form text: `Text`

### Numeric Types

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `Long` | `Long` | `number` | Integer (64-bit) |
| `Integer` | `Long` | `number` | Integer, stored internally as Long |
| `Decimal` | `BigDecimal` | `number` | Decimal number (up to 19 digits, arbitrary precision) |
| `Percent` | `BigDecimal` | `number` | Percentage value (0–100) |
| `Year` | `Integer` | `number` | Year number |

### Boolean

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `Boolean` | `Boolean` | `boolean` | Boolean value |

### Date/Time Types

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `Date` | `Date` | `string` | Date (no time), ISO-8601: `YYYY-MM-DD` |
| `DateTime` | `Date` | `string` | Date with time, ISO-8601: `YYYY-MM-DDTHH:mm:ss` |
| `Time` | `Date` | `string` | Time of day |
| `Anniversary` | `Date` | `string` | Anniversary (day + month, no year) |
| `Duration` | `Long` | `number` | Duration |
| `DurationInMilliseconds` | `Long` | `number` | Duration in milliseconds |
| `TimePeriod` | — | `object` | Time period (from–to) |
| `YearToDate` | — | `object` | Year-to-date range |

### Contact & Format Types

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `EmailAddress` | `String` | `string` | Email address (with format validation) |
| `PhoneNumber` | `String` | `string` | Phone number (with formatting) |
| `IBAN` | `String` | `string` | IBAN (with formatting and validation) |
| `URI` | `String` | `string` | URI/URL |

### Reference Types (CRM Keys)

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `EntityKey` | `IEntityKey` | `string` | BSI CRM entity key (reference to a CRM object) |
| `StringEntityKey` | `String` | `string` | Entity key as string |

**Note:** `EntityKey` and `StringEntityKey` are used for CRM object references (e.g. customer ID, contract ID). In TypeScript they appear as `string`.

### Currency Types

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `Currency` | `String` | `string` | Currency code (e.g. `"CHF"`, `"EUR"`) |
| `CurrencyAmount` | `BigDecimal` | `number` | Monetary value (always combined with a currency) |
| `CurrencyDate` | `Date` | `string` | Date for currency conversion |

### Binary Types

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `BinaryData` | `byte[]` | `string` | Binary data (Base64-encoded) |
| `BinaryRef` | — | `string` | Reference to binary data |
| `BinaryResource` | — | `object` | Resource with binary data |
| `BinaryResourceRef` | — | `string` | Reference to BinaryResource |

### AI/ML Types (Vectors)

| Type ID | Java Type | TypeScript Type | Description |
|---------|-----------|-----------------|-------------|
| `FloatVector` | `float[]` | `number[]` | Arbitrary float vector |
| `Embedding1024` | `float[]` | `number[]` | Embedding vector with 1024 dimensions |
| `Embedding2560` | `float[]` | `number[]` | Embedding vector with 2560 dimensions |
| `Embedding3584` | `float[]` | `number[]` | Embedding vector with 3584 dimensions |
| `Embedding4096` | `float[]` | `number[]` | Embedding vector with 4096 dimensions |
| `Embedding8960` | `float[]` | `number[]` | Embedding vector with 8960 dimensions |

---

## System-Internal Types

These types exist in the system but are typically **not suitable for Lambda signatures** (too specialized or internal):

| Type ID | Description |
|---------|-------------|
| `LocalizedText` | Multi-language text as a map |
| `DoEntity` | Generic Scout Data Object |
| `Formula` | Formula expression |
| `PasswordHashAndSalt` | Secured password (internal type) |
| `Locale` | Language setting |
| `ApplicationLocale` | Application language setting |
| `DateFormat` | Date format specification |
| `NumberFormat` | Number format specification |
| `TimeUnit` | Time unit (seconds, minutes, …) |
| `TruncateDateType` | Date truncation type |
| `DataModelEntityId` | Internal entity ID in the data model |
| `DataModelTypeId` | Internal type ID in the data model |
| `QualifiedDataModelItemId` | Fully qualified data model item ID |
| `BucketType` | Bucket type for analytics |
| `UserAgent` | Browser/client user agent |
| `MutationTransactionStatus` | Status of a CRM mutation |

---

## Dynamic Types (with Format Specification)

These types have parameterized IDs in the format `{TypeName}:{formatSpec}`:

| Type ID Format | Description |
|----------------|-------------|
| `FormattedLong:{spec}` | Integer with formatting |
| `FormattedDecimal:{spec}` | Decimal with formatting |
| `FormattedDateTime:{spec}` | Date/time with formatting |
| `FormattedCurrencyAmount:{spec}` | Currency amount with formatting |

These are rarely used directly in signatures in practice.

---

## Mapping: Signature Type → TypeScript Interface Field

When the generator produces the Lambda `api.d.ts`, signature types are translated to TypeScript types:

| Signature Type | TypeScript Field Type | Note |
|---|---|---|
| `Text`, `Text60`, `Text250`, `Text500` | `string` | |
| `PlainText`, `Html`, `RichText` | `string` | |
| `EmailAddress`, `PhoneNumber`, `IBAN`, `URI` | `string` | |
| `EntityKey`, `StringEntityKey` | `string` | |
| `Currency` | `string` | Currency code |
| `Boolean` | `boolean` | |
| `Long`, `Integer`, `Decimal`, `Percent`, `Year` | `number` | |
| `CurrencyAmount` | `number` | |
| `Date`, `DateTime`, `Time`, `Anniversary` | `string` | ISO-8601 format |
| `Duration`, `DurationInMilliseconds` | `number` | |
| `FloatVector`, `Embedding*` | `number[]` | Float array |
| `BinaryData` | `string` | Base64 |
| `BinaryRef`, `BinaryResourceRef` | `string` | |
| `BinaryResource` | `object` | |

**Outputs are always optional in TypeScript (`?`)**:
```typescript
export interface LambdaOutput {
  valid?: boolean;     // Boolean → boolean, optional
  bankCode?: string;   // Text60 → string, optional
  amount?: number;     // Decimal → number, optional
}
```

**Inputs are optional or required depending on the `mandatory` flag**:
```typescript
export interface LambdaInput {
  iban: string;        // mandatory: true → no ?
  format?: string;     // mandatory: false → with ?
}
```
