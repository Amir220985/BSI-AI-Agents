# BSI EIP Configuration Generator

This directory is the knowledge base for generating BSI EIP Lambda interface configurations. It contains reference documentation, annotated examples, and the skill guide that Claude uses to produce new configurations.

**Target platform:** BSI EIP product version 26.1.8

---

## What Is This?

BSI EIP interfaces are defined as JSON configuration files inside ZIP archives. The ZIP is imported directly into a BSI EIP installation. This generator provides:

- **Reference documentation** — precise field-by-field specs for every file format.
- **Annotated examples** — complete, real configurations with every decision explained.
- **A generation skill** — a step-by-step guide for Claude to follow when producing new configs.

The canonical use case is: *"I need a Lambda that calls API X and returns data Y — generate the configuration ZIP."*

---

## Directory Structure

```
generator/
├── README.md                          ← this file
├── skill-generate-eip-config.md       ← the generation skill (start here for new configs)
│
├── reference/
│   ├── zip-package-format.md          ← ZIP structure, index.json, export-definition.json
│   ├── interface-config.md            ← InterfaceConfig JSON: all top-level fields, processors, scripts
│   ├── outlets-and-routing.md         ← OutletConfig: descriptor IDs, outletScriptIds, routing patterns
│   ├── processor-types-catalog.md     ← All processor type UUIDs, customConfig structures, scripts
│   ├── signature-reference.md         ← Signature and SignatureProperty structure, multilingual names
│   ├── data-types-reference.md        ← All 55+ data types: IDs, Java types, TypeScript types, examples
│   ├── environment-variables.md       ← API-Keys via Resolvers.environmentVariables
│   ├── typescript-scripting-api.md    ← Invocation, Self, LOG, Resolvers, Collections API reference
│   ├── collections-api.md             ← Collections: persistenter Key-Value-Store
│   ├── bsi-api-discovery.md           ← Discovery-APIs: Codetypes & Mutations
│   ├── multi-package-zip.md           ← Multi-package ZIP: multi-index.json, stage types, CRM + interfaces
│   ├── crm-field-transfer.md          ← CRM field via config transfer: DomainKey, field definition, flags
│   ├── interfaces-index-structure.md  ← referencedItems as objects, globalUniqueId prefixes, Project type
│   ├── crm-data-search-processor.md   ← CrmDataModelSearchProcessorConfig v26.1.001, selection structure
│   └── powershell-zip-encoding.md     ← PowerShell stdin encoding pitfalls, UTF-8-no-BOM, ZIP creation
│
└── examples/
    ├── iban-validation/               ← 5-processor REST Lambda (Standard-Pattern)
    │   ├── ANNOTATION.md              ← Deeply annotated walkthrough (primary reference)
    │   ├── _source.zip                ← Original ZIP exported from BSI EIP
    │   ├── export-definition.json     ← Extracted: export descriptor
    │   ├── export-log.txt             ← Extracted: informational log
    │   ├── index.json                 ← Extracted: transfer manifest
    │   ├── interfaces/
    │   │   └── IBAN_validation-af8cb193-e289-48d9-a9b6-36e30941909c.json
    │   └── projects/
    │       └── IBAN-4ebaedb9-6f31-408d-bd36-9e36f8b3a357.json
    ├── weather-api/                   ← Lambda + REST Provider + Ad-Hoc Batch (komplexes Beispiel)
    │   ├── ANNOTATION.md              ← Full walkthrough of both interfaces
    │   ├── _source.zip
    │   ├── 01-crm/                    ← CRM Datenmodell (Codes + Felder)
    │   └── 02-interfaces/             ← Interfaces + WebAPIs + Projekt
    └── csv-import/                    ← Input Interface mit CSV, Collections, Retry-Pattern
        ├── ANNOTATION.md              ← Walkthrough aller 13 Processors + Collections + Patterns
        ├── _source.zip
        ├── interfaces/
        ├── projects/
        ├── presets/                   ← CSV format configuration
        └── collections/               ← mappings, retries, processedRecords
```

---

## How to Generate a New Configuration

Read `skill-generate-eip-config.md`. It is the complete guide.

**Summary of the process:**

0. Ask for the customer's base URL — needed for Discovery APIs (codetypes, mutations). See `reference/bsi-api-discovery.md`. For CRM integrations, query the relevant codetypes and mutation types before generating.
1. Gather requirements: Lambda name, inputs, outputs, API URL/method, auth scheme, response shape.
2. Plan the pipeline: `Lambda → Iteration → prepare → REST Consumer → transform` (standard pattern).
3. Generate fresh UUIDs for all variable entities (never reuse example UUIDs).
4. Generate the 5 files: `export-definition.json`, `index.json`, `projects/{Name}-{uuid}.json`, `interfaces/{Name}-{uuid}.json`, and optionally `export-log.txt`.
5. Write the TypeScript scripts for each processor.
6. Save files to disk in the correct directory structure.
7. Zip with: `zip -r bsi-eip-{timestamp}.zip export-definition.json index.json interfaces/ projects/`

The skill file contains a pre-generation checklist — always verify it before finalizing the ZIP.

---

## How to Understand an Existing Configuration

Read `examples/iban-validation/ANNOTATION.md`.

That document walks through every processor, every script, every outlet, and every field in the IBAN validation configuration. It explains:

- Why each processor exists and what it does.
- How the TypeScript scripts connect to each other via `invocation.processors.*`.
- How outlets wire the pipeline together.
- How the signature defines the Lambda's public contract.
- How to adapt the configuration for a different REST API (8-step guide).
- What to configure in BSI EIP after import (environment variables).

For questions about specific JSON structures or field semantics, consult the relevant reference file directly.

---

## Quick Reference

The most frequently needed values when generating configurations. Copy these exactly.

### Interface Type

| Thing | UUID |
|---|---|
| Lambda interface `typeId` | `2512c737-a73b-4f78-9ae2-098ac6d291bd` |
| Ad-Hoc interface `typeId` | `f72f9f76-fb2d-4579-b397-471b2ed4c4e3` |
| Input interface `typeId` | `ce4bb086-02d6-4cee-9509-7b0dadaa6654` |

### Fixed User

| Thing | UUID |
|---|---|
| Admin `responsible.userId` | `36317f78-6040-4648-936d-e8b66b394c0b` |

### Processor Type UUIDs

| Processor | `typeId` |
|---|---|
| Lambda (CRM Lambda) | `ec06bfe3-faab-4c2c-83bc-8420789d3479` |
| Iteration | `21c361ec-5dec-4f13-9767-442db1adb3a3` |
| TypeScript | `ffd19a7a-7613-40c0-876a-5d9a6eca66b6` |
| REST Consumer | `f069aa44-fb5c-469e-a727-705ca7072fee` |
| Temporal Trigger | `406211f6-7b91-4790-b492-feb3e7cac22c` |
| Manual Trigger | `b4447959-8495-4a20-83e1-e3e0384c5935` |
| CSV Processor | `1245030d-3b73-42fb-a7a8-3ed91b729303` |
| CRM Data Search | `633d02d2-bda7-450d-a399-277644d39082` |
| CRM Mutation | `cf9ee65c-a489-4250-b76a-7b1741868c0f` |
| Invoke Lambda | `9d107af5-8cdc-4138-bbdf-fc5383ece181` |
| REST Provider | `01eb3948-507e-4ff4-bb31-525bab2b3e08` |
| Local Routine | `9332ef6a-024d-42d7-91ab-01c3d4121750` |

### Outlet Descriptor IDs

| Processor | Outlet Name | Descriptor ID |
|---|---|---|
| Lambda | Aufruf | `78861a9e-e99c-47c7-913b-6bf685f5557b` |
| Lambda | Abgeschlossen | `738f1301-f558-40b5-bbfc-e869a5832156` |
| Iteration | Iteration | `da7bac4b-8a6c-4fd7-abf3-7ca5d1a78575` |
| Iteration | Abgeschlossen | `dd8f5806-3156-4697-97c0-dd069570f2e6` |
| TypeScript | Standard | `c4b09fff-0dae-4726-bdeb-12fd01ddc2da` |
| REST Consumer | Standard | `6a132916-f955-4dbd-a377-2c3ee21e7fcb` |
| REST Consumer | Sonstige | `c95394e3-50c2-4b7c-9529-3149328355e9` |
| Local Routine | Aufruf | `885d0c0b-3b59-4c13-85af-a061fd11eb66` |
| REST Provider | Aufruf | `6891417a-17b6-42a1-850a-da8effff4d13` |
| REST Provider | Abgeschlossen | `1cbc92dc-5491-43f2-8e80-8e25556052dd` |
| Temporal Trigger | Standard | `b3f5da65-ba2e-40ab-9983-a4e34544ff28` |
| Manual Trigger | Standard | `d20e1c72-467d-4af8-9c19-0027cd18c901` |
| CSV Processor | Standard | `ed9dfe53-c48e-4551-b398-b1c2598726a8` |
| CRM Data Search | Standard | `59c636c9-ccce-4650-8460-f7025a556cd2` |
| Invoke Lambda | Standard | `cce40eff-3c00-45fc-b569-74c5eb3710b7` |
| CRM Mutation | Standard | `6c0f1af6-2051-4fd5-947b-398c59418229` |
| CRM Mutation | Fehler | `f3aac37d-ce3b-45d0-8c52-b157854d2e8f` |

### The 8 `valueMigrationIds` (copy verbatim into every `index.json`)

```json
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
```

These are fixed constants for EIP product version 26.1.8. Never regenerate them.

### IBAN Example Processor IDs (for reference only — never reuse in new configs)

| Processor | `id` |
|---|---|
| lambda | `12cfe4f1-96f8-4681-8dd5-cae9dfba4632` |
| iteration | `a8d5e05c-5275-49a6-9e8c-e3a782da52e1` |
| prepare | `a69ffd89-6b06-48e5-84e4-fd41d44682d2` |
| restConsumer | `d9198b4b-be1c-463c-b968-4624fd5b55b7` |
| transform | `5d00b8c8-876d-41ab-a81d-49eafae8061e` |

---

## Adding a New Example

When you export a new working configuration from BSI EIP and want to add it to this knowledge base:

1. Create a new directory under `examples/`, named after the interface (e.g. `examples/address-validation/`).
2. Extract the ZIP contents into that directory, preserving the `interfaces/` and `projects/` subdirectories.
3. Copy the `_source.zip` into the directory for reference.
4. Write an `ANNOTATION.md` in the new directory, following the structure of `examples/iban-validation/ANNOTATION.md`:
   - Data flow diagram
   - Signature explained (inputs, outputs)
   - Each processor with its customConfig, outlets, and scripts
   - TypeScript script inventory
   - Test suite explanation
   - Adaptation guide for similar use cases
   - Post-import setup steps

5. Update this README to add the new example to the directory structure listing.

The more detailed the annotation, the more reliably Claude can generate similar configurations without errors.
