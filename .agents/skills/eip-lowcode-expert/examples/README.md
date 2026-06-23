# EIP Low-Code & Integrations-Beispiele

Dieses Verzeichnis enthält bewährte Vorlagen, TypeScript-Skripte und Beispiel-Pipelines aus realen Projekten für die Enterprise Integration Platform (EIP) von BSI.

## Übersicht der Beispiele

* **[IBAN_validation.json](file:///Users/melvin.vogt/Workspace/bsi-core-ai-system/.agents/skills/eip-lowcode-expert/examples/IBAN_validation.json)**
  * **Typ**: EIP-Interface-Konfiguration (`interfaces.InterfaceConfig`)
  * **Trigger**: CRM-Lambda-Trigger (`CrmLambdaProcessorConfig`) – dient als Einstiegs- bzw. Trigger-Punkt für Aufrufe aus anderen Teilen der BSI CustomerSuite.
  * **Ablauf**:
    1. **Einstieg (`lambda`)**: Nimmt die `iban` (Text) entgegen.
    2. **Aufbereitung (`prepare`)**: TypeScript-Skript entfernt Leerzeichen und prüft auf ungültige Zeichen (RegEx).
    3. **REST-Abfrage (`restConsumer`)**: Führt einen GET-Request an `api.iban.com` aus. Der API-Key wird sicher über `Resolvers.environmentVariables.resolveBySetting('ibanApiKey')` geladen.
    4. **Transformation & Validierung (`transform`)**: TypeScript-Skript validiert das JSON-Response-Objekt auf Fehler- und Statuscodes und gibt die Bankdaten (`valid`, `bankCode`, `bic`, `bankName`) zurück.
  * **Besonderheiten**:
    * Zeigt, wie Umgebungsvariablen im Integrationskontext aufgelöst werden.
    * Beinhaltet eine vollständige Test-Suite (`testIbanValidation.ts`) mit Mocks des REST-Consumers (`TestDriver.createTest()`).

* **[Import_CSV.json](file:///Users/melvin.vogt/Workspace/bsi-core-ai-system/.agents/skills/eip-lowcode-expert/examples/Import_CSV.json)**
  * **Typ**: EIP-Interface-Konfiguration (`interfaces.InterfaceConfig`)
  * **Trigger**: Zeitgesteuerter Trigger (`TriggerTemporalProcessorConfig`) oder Manueller Trigger (`TriggerManualProcessorConfig`).
  * **Ablauf (3 Phasen)**:
    1. **Fetch**: Simuliert das Einlesen von CSV-Zeilen (`simulateFetch` TypeScript-Step) und wandelt sie in ein Listen-Objekt um (`csv` Step).
    2. **Process**: Iteriert über jede Zeile:
       - **Validierung & Mapping**: TypeScript-Step `validateAndMap` prüft die Zeile, schaut im Key-Value-Store `mappings` (Collection) nach der Dringlichkeit und löst den Benutzernamen über `Resolvers.crmEntities.resolveUser` auf.
       - **CRM-Mutation**: Step `mutation` schreibt den Record in das CRM.
       - **Erfolgsbehandlung**: Bei Erfolg wird ein MD5-Hash des Records und der CRM-Objekt-Key in `processedRecords` (Collection) gespeichert, um Dubletten bei wiederholter Ausführung zu vermeiden. Ein eventueller Retry-Eintrag wird gelöscht.
       - **Fehlerbehandlung**: Schlägt das Mapping fehl, wird der Datensatz mit Fehlerursache und Zähler (RetryCount) in `retries` (Collection) abgelegt.
    3. **Retry**: Liest über `listCollection` (TypeScript-Step) die fehlerhaften Einträge aus `retries` aus, filtert auf `< 5` Versuche (mittels `Collections.jsonPath().property('retryCount').condition(...)`) und speist sie erneut in den Process-Teil ein.
  * **Besonderheiten**:
    * **Umgang mit Collections (Key-Value-Stores)**:
      * Import: `import { Collections } from '../../collections';`
      * Wert lesen: `Collections.get('name').get(key)`
      * Wert schreiben/aktualisieren: `Collections.get('name').putImmediately(key, value)`
      * Wert löschen: `Collections.get('name').removeImmediately(key)`
      * Abfragen & Filtern: `Collections.get('name').list({ maxResults, valueRestrictions: [...] })`
    * Zeigt fortgeschrittenes Retry-Handling und Change-Detection (unchanged records) mithilfe von MD5-Hashes (`Hash.md5(record)`).

* **[export_crm.json](export_crm.json)**
  * **Typ**: EIP-Interface-Konfiguration (`interfaces.InterfaceConfig`)
  * **Trigger**: Routine-Trigger (`RoutineProcessorConfig`) – wird als Routine aus anderen Interfaces heraus aufgerufen.
  * **Ablauf**:
    Modularer Export aller zentralen CRM-Entitäten, aufgeteilt in thematische Gruppen (Customer, City, Task, Communication, Business, Documents, Case, Ereignisse, Codes, Chat Conversation).
    Pro Gruppe: `CrmDataModelSearch` → TypeScript `recode*`-Step → Iteration → TypeScript `store*`-Step, der die Daten per `Collections.putImmediately` in einer benannten Collection ablegt.
  * **Besonderheiten**:
    * Zeigt, wie ein groß angelegter Multi-Entitäten-Export mit Gruppen strukturiert wird.
    * Nutzt eine gemeinsame `recodeCode()`-Hilfsfunktion aus `scripts/helper` für das Umschlüsseln von Code-Referenzen auf `globalKey`.
    * Collections dienen als Zwischenspeicher und werden von nachgelagerten Import-Interfaces wieder ausgelesen.

* **[export_project.json](export_project.json)**
  * **Typ**: EIP-Interface-Konfiguration (`interfaces.InterfaceConfig`)
  * **Trigger**: Routine-Trigger (`RoutineProcessorConfig`) oder Manueller Trigger (`TriggerManualProcessorConfig`).
  * **Ablauf (3 parallele Export-Stränge)**:
    1. **Customer Project**: `exportProjectCustomers` (Routine) → `searchCustomersProject` (DataModelSearch) → `recodeCustomerProject` (TypeScript) → `customersProjectIteration` → `storeCustomerProject` (Collections `customers_project`)
    2. **Occurence Project**: `exportProjectOccurrences` (Routine) → `searchOccurrencesProject` (DataModelSearch, exportiert Region, Branche, Ereignisstatus) → `recodeOccurenceProject` (TypeScript) → `occurrencesProjectIteration` → `storeOccurrenceProject`
    3. **Social Media Post Project**: `exportProjectSocialMediaPost` (Routine) → `searchSocialMediaPostProject` (DataModelSearch, exportiert Channel, Platform, Sentiments etc.) → `recodeSocialMediaPostProject` (TypeScript) → `socialMediaPostProjectIteration` → `storeSocialMediaPostProject`
  * **Besonderheiten**:
    * Alle drei Stränge werden über einen gemeinsamen `execute_routines`-TypeScript-Step koordiniert.
    * Zeigt, wie projektspezifische Volta-Konfigurationen (Custom Entities wie `Y-SocialMediaPost`) exportiert werden.
    * Iterationen laufen mit `workerThreads: 5` bzw. `15` für parallele Verarbeitung.

* **[import_crm.json](import_crm.json)**
  * **Typ**: EIP-Interface-Konfiguration (`interfaces.InterfaceConfig`)
  * **Trigger**: Routine-Trigger (`RoutineProcessorConfig`) – als `runImport_full` aus dem Trigger-Interface aufgerufen.
  * **Ablauf**:
    Vollständiger CRM-Import über separate Gruppen: Customers/Users, Tasks, Communications, Businesses, Customer Advisors, Customer Relations, Cities. Pro Gruppe: LocalRoutine als Einstieg → TypeScript zum Auflisten der Collection-Einträge → Iteration → TypeScript-Step mit Mutations-Vorbereitung → `CrmMutationProcessorConfig`. Operationen umfassen Create Customer, Update Customer Advisor, Update Customer Relation, Create Business u.a.
  * **Besonderheiten**:
    * Zeigt das vollständige Import-Pattern mit `LocalRoutines` für modulare Wiederverwendung.
    * Nutzt `resolveImportedReference()`, `resolveCodeByReference()`, `resolveCrmCustomerByReference()` aus `scripts/helper` sowie `timeShift()` aus `scripts/timeshift` für Zeitzonenhandling.
    * Outlet-Steuerung mit `hasMutations` / `noMutations` vermeidet unnötige Mutation-Aufrufe bei unveränderter Datenlage.

* **[import_project.json](import_project.json)**
  * **Typ**: EIP-Interface-Konfiguration (`interfaces.InterfaceConfig`)
  * **Trigger**: Routine-Trigger (`runProjectImport_full`) oder LocalRoutine (`importProjectSocialMediaPosts`).
  * **Ablauf**:
    1. **Import: Full** – `runProjectImport_full` (Routine) → `manualProjectImportFull` (TypeScript) ruft `LocalRoutines.importProjectSocialMediaPosts()` auf.
    2. **Import: Social Media Posts** – `importProjectSocialMediaPosts` (LocalRoutine) → `listSocialMediaPostsProject` (TypeScript, liest aus Collection `socialMediaPosts_project`) → `iterationSocialMediaPostsProject` → `socialMediaPostProjectStoreMappings` (prüft per `resolveImportedReference`, ob Update nötig, ruft `LocalRoutines.createSocialMediaPost()` auf).
    3. **Operation: Create Social Media Post** – `createSocialMediaPost` (LocalRoutine) → `prepareCreateSocialMediaPost` (TypeScript, baut Mutations-Objekt) → bei `hasMutations`: `createSocialMediaPostMutations` (CrmMutation).
  * **Besonderheiten**:
    * Zeigt das `LocalRoutine`-Pattern für wiederverwendbare Teilprozesse innerhalb eines Interfaces.
    * Mutations werden mit `ProcessorTypes.dataMutation.createModifyEntityMutation()` aufgebaut.
    * Update-Operationen werden mit einer `LOG.warn` bewusst übersprungen (nur Create unterstützt).

* **[trigger_import.json](trigger_import.json)**
  * **Typ**: EIP-Interface-Konfiguration (`interfaces.InterfaceConfig`)
  * **Trigger**: Manueller Trigger (`TriggerManualProcessorConfig`)
  * **Ablauf**:
    1. **Manueller Trigger** → `typescript` (TypeScript-Step) ruft `Routines.runImport_full(null)` auf.
  * **Besonderheiten**:
    * Schlankstes mögliches Trigger-Interface (2 Steps).
    * Zeigt das Pattern, ein komplexes Routine-Interface (`import_crm`) von außen manuell anzustoßen.
    * Voraussetzung laut `notes`: Das Interface „Import" muss zuvor auf `live` gesetzt sein.

### Dateinamenskonventionen
- Low-Code-TypeScript-Dateien: `*.ts`
- Interface-Konfigurationen: `*.json`

