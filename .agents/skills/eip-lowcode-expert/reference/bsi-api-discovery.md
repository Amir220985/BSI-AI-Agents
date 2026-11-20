# BSI EIP Web API Discovery

## Overview

BSI EIP exposes a set of **discovery endpoints** under the `cpd-tools` path that allow the generator to inspect the CRM data model of a specific BSI instance at runtime. These endpoints return:

- All available **codetypes** (CRM code lists) and their valid values
- All available **mutation types** (CRM write operations) and their field schemas

These endpoints are essential when generating configurations that interact with CRM data — for example, when a signature field references a CRM code list, or when a processor must create or update a CRM entity via `Mutations.create(...)`.

> **Key constraint: The base URL is customer-specific.**
> Every BSI installation has its own base URL. The generator must never hardcode or assume a URL. Always ask the user first.

---

## Asking for the Base URL

Before calling any discovery endpoint, ask the user:

> "What is your BSI EIP base URL?
> Example: `https://bsi-2005.trials.bsi-software.com/bsiinterfaces/web-api`
> This is the root URL for your BSI instance's Web API."

Checklist before making discovery calls:
- [ ] User has provided their base URL
- [ ] URL ends with `/web-api` (not a trailing slash, no extra path segments)
- [ ] URL uses `https://`

Store the base URL as `{baseUrl}` and substitute it into all endpoint patterns below.

---

## Codetypes

CRM code lists (codetypes) define enumerated values for fields like status, category, team role, and customer attributes. There are 800+ codetypes in a typical BSI installation.

### Endpoint 1: List all codetypes

```
GET {baseUrl}/l/cpd-tools/codetypes
```

**Returns:** Array of codetype name strings.

**Example response (excerpt):**
```json
[
  "ActionStatus",
  "CommunicationStatus",
  "CrmCode",
  "CustomerAttribute",
  "TeamRole",
  ...
]
```

**When to use:** When you need to discover what code lists exist in this BSI instance, or when you need to find the name of a codetype before fetching its values.

### Endpoint 2: Get codetype details

```
GET {baseUrl}/l/cpd-tools/codetypes/{codeTypeName}
```

**Returns:** The code values for that codetype.

**Example — `CommunicationStatus`:**
```json
[
  "Done",
  "EscalatedProcessing",
  "EscalatedReaction",
  "Failed",
  "InProgress",
  "Inbox",
  "OverdueProcessing",
  "OverdueReaction",
  "OverdueStep",
  "Pending",
  "Planned"
]
```

**When to use:**
- To validate that a code value the user mentioned actually exists
- To know what values are valid for a code field used in a filter constraint
- To look up the TypeScript name mapping for `Codes.AttributeUserDefinedCodes.Xxx`

---

## Mutation Types

Mutation types define CRM write operations — creating, updating, or deleting CRM entities. There are 300+ mutation types in a typical BSI installation.

### Endpoint 3: List all mutation types

```
GET {baseUrl}/l/cpd-tools/mutationtypes
```

**Returns:** Array of mutation type name strings.

**Naming pattern:** `Crm[Entity][Action]` — for example:
- `CrmCustomerCreate`, `CrmCustomerUpdate`
- `CrmTaskCreate`, `CrmTaskDelete`
- `CrmActionCreate`, `CrmActionUpdate`

Customer-specific mutations are prefixed with `Y_`.

**When to use:** When the user wants to perform a CRM write operation and you need to find the correct mutation type name.

### Endpoint 4: Get mutation type details

```
GET {baseUrl}/l/cpd-tools/mutationtypes/{mutationTypeName}
```

**Returns:** All fields with their types and mandatory flags.

**Example — `CrmTaskCreate`:**

| Field | Type | Mandatory |
|---|---|---|
| `subject` | Text (250 characters) | **yes** |
| `dueDate` | Date | **yes** |
| `highPriority` | Yes/No (boolean) | no |
| `notes` | HTML | no |
| `primaryCustomerKeyRef` | Key of Customer | no |
| `businessKeyRef` | Key of Business | no |
| `contextCustomerKeyRef` | Key of Customer | no |
| `responsibleUserKeyRef` | Key of User | no |
| `responsibleTeam` | Key of Code: Team | no |
| `responsibleTeamRole` | Key of Code: TeamRole | no |
| `categories` | List of Key of Category | no |
| `actionKeyRef` | Key of Action | no |
| `aggregateId` | Key reference | no |
| `id` | Key reference | no |
| `doneDate` | Date | no |
| `mutationRef` | Text | no |
| `dataVersion` | Data version | no |
| `semaphoreToken` | Semaphore token | no |

**When to use:** Before generating a `Mutations.create(...)` call — to know which fields are required and what their types are.

---

## When to Query During Generation

| If the config needs... | Query this endpoint |
|---|---|
| A CRM code reference in the signature (`Key:Entity:CrmCode:{uuid}`) | `GET /codetypes` to find the codetype name, then `GET /codetypes/{name}` to verify values |
| A filter constraint comparing against a code value | `GET /codetypes/{name}` to find valid values; the UUID in `Key:Entity:CrmCode:{uuid}` comes from the CRM data model or the ZIP's `01-crm/` folder |
| A CRM mutation via `Mutations.create(...)` | `GET /mutationtypes/{name}` to see all fields and which are mandatory |
| Listing available mutations to find the right type name | `GET /mutationtypes` |
| Listing available codetypes to find the right name | `GET /codetypes` |
| Calling an existing Lambda (Invoke Lambda processor) | No discovery needed — use the `qualifiedLambdaId` from the target interface's ZIP |

---

## Code Map for TypeScript

When a signature field has type `Key:Entity:CrmCode:{uuid}`, the TypeScript runtime value is the UUID of the selected code entry. These UUIDs can be referenced symbolically via `Codes.AttributeUserDefinedCodes` from `@eip/crm-core`.

**Naming convention:** Strip spaces, apply PascalCase to the codetype name and value name, concatenate.

Examples:
- Codetype `WeatherScore`, value `Fantastic` → `Codes.AttributeUserDefinedCodes.WeatherScoreFantastic`
- Codetype `CommunicationStatus`, value `InProgress` → `Codes.AttributeUserDefinedCodes.CommunicationStatusInProgress`
- Codetype `TeamRole`, value `Advisor` → `Codes.AttributeUserDefinedCodes.TeamRoleAdvisor`

> **Note:** The exact identifiers available depend on the BSI instance configuration. Use the discovery API to verify which codetypes and values are actually present.

---

## Example Discovery Workflow

**Scenario:** Customer wants to create CRM tasks from a processor using `CrmTaskCreate`.

**Steps:**

1. **Ask for the base URL.**
   "What is your BSI EIP base URL? Example: `https://xxx.bsi-software.com/bsiinterfaces/web-api`"

2. **Fetch the mutation type schema.**
   ```
   GET {baseUrl}/l/cpd-tools/mutationtypes/CrmTaskCreate
   ```

3. **Identify required fields.**
   From the response: `subject` (Text 250) and `dueDate` (Date) are mandatory.

4. **Generate the processor code.**
   ```typescript
   const task = Mutations.create('CrmTaskCreate', {
     subject: invocation.input.taskSubject,
     dueDate: invocation.input.dueDate,
     primaryCustomerKeyRef: invocation.input.customerId,  // optional
     notes: invocation.input.notes,                        // optional
   });
   ```

5. **Verify optional fields** the user wants to populate by checking the field list from step 2.

---

**Scenario:** Customer wants a signature output representing a weather score code selection.

**Steps:**

1. **Ask for the base URL** (if not already known).

2. **List codetypes to find the relevant name.**
   ```
   GET {baseUrl}/l/cpd-tools/codetypes
   ```
   Search the result for `WeatherScore` or similar.

3. **Fetch the codetype details to see valid values.**
   ```
   GET {baseUrl}/l/cpd-tools/codetypes/WeatherScore
   ```
   Response: `["Fantastic", "Good", "Neutral", "Bad", "Terrible"]` (example)

4. **Get the code list UUID** from the CRM data model configuration (in the ZIP's `01-crm/` folder) or ask the customer.

5. **Define the signature output.**
   ```json
   {
     "_type": "bsiscout.SignatureProperty",
     "_typeVersion": "bsiscout-24.1.001",
     "identifier": "score",
     "name": { "en": "Weather score", "und": "Wetterbewertung" },
     "type": "Key:Entity:CrmCode:9ac81c27-0a86-459c-ba62-482fee56739c"
   }
   ```

6. **In TypeScript**, set the value using the symbolic constant:
   ```typescript
   invocation.output.score = Codes.AttributeUserDefinedCodes.WeatherScoreFantastic;
   ```
