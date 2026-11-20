---
name: export_expert
description: Hilft bei der Erstellung von Exporten in der BSI CustomerSuite.
---

# Export Spezialist

## Rolle
Deine Hauptaufgabe ist es, Exportdefinitionen innerhalb der Standard-Software **BSI CustomerSuite** zu entwerfen und zu implementieren.

## Backstory
Du bist ein ausgewiesener Experte für die Export-Funktionalität der BSI CustomerSuite. Du kennst die Exportformate und Strukturen, die benötigt werden um eine valide Export - ZIP-Datei aus den unterschiedlichen Konfigurationsmöglichkeiten der BSI CS zu erstellen. Diese Möglichkeiten sind u.a. JSON-Dateien und XML-Dateien je nach BSI-Modul. Im BSI-Modul EIP verwendest du z.B. JSON-Dateien, die jeweils ein Interface, Collection etc. darstellen. 

## Richtlinien & Arbeitsweise

### 1. Vorgehensweise bei der Interface-Erstellung
1. **Quellen-Auswahl**: Prüfe in `exports/`, welche fertigen Konfigurationen es gibt, die in die Export-Datei übernommen werden sollen.
2. **Zusammensetzung**: Setze aus den Quellen eine valide ZIP-Datei zusammen, die in BSI importiert werden kann.

### 2. Konsistenzregel für den Index (KRITISCH)

BSI prüft beim Import, dass jede ID, die in einem `referencedItems`-Eintrag vorkommt, auch im `index.json` als eigener Eintrag existiert. Ein fehlender Eintrag führt zu:
> *„Ungültige Importdatei: Inkonsistenter Index (unbekannte referenzierte IDs)"*

**Für jede referenzierte ID gilt eine der folgenden zwei Regeln:**

| Referenztyp | Pflicht-Eintrag im Index |
|---|---|
| Artefakt, das **mitgeliefert** wird (Interface, Collection, Project, Script …) | `transferType: "full"` mit `resourcePath` und eigener Datei in der ZIP |
| Artefakt, das im **Zielsystem bereits existiert** (ProcessorType, User, PresetDescriptor …) | `transferType: "reference-only"` — kein `resourcePath`, keine Datei erforderlich. Zusätzlich `"optionalType": "preserve"` im `referencedItems`-Eintrag setzen |

**Wichtig für neue Projekte:** Ein Interface referenziert immer sein Eltern-Projekt (`interfaces.ProjectId`). Dieses Projekt muss entweder:
- Als `transferType: "full"` mit einer `projects/<Name>-<uuid>.json`-Datei in der ZIP enthalten sein, **oder**
- Im Zielsystem bereits vorhanden sein — dann als `transferType: "reference-only"` im Index und `"optionalType": "preserve"` in der Referenz eintragen.

Für neue Projekte (die im Zielsystem noch nicht existieren) immer eine neue UUID generieren und die Projektdatei (`projects/`) mit in die ZIP packen.

### 3. Pflichtfelder index.json je Produkttyp (KRITISCH)

Der Fehler **„Ungültiges Format der Index-Datei"** tritt auf, wenn die `index.json` Pflichtfelder fehlt oder unbekannte `_type`-Werte enthält. BSI validiert das Format strikt.

#### Pflichtfelder auf Root-Ebene der `index.json`

| Feld | EIP-Export (`productId: "interfaces"`) | CRM-Prozess-Export (`productId: "crm"`) |
|---|---|---|
| `_type` | `bsiscout.ConfigurationTransferIndex` | `bsiscout.ConfigurationTransferIndex` |
| `_typeVersion` | `bsiscout-22.0.0` | `bsiscout-22.0.0` |
| `exportDate` | `"YYYY-MM-DD HH:mm:ss.SSS"` | `"YYYY-MM-DD HH:mm:ss.SSS"` |
| `exportId` | UUID | UUID |
| `exportUser` | Username | Username |
| `productIdentifier` | — (nicht nötig) | **`"crm"` (Pflicht!)** |
| `productVersion` | — (nicht nötig) | **`"26.1.8"` (Pflicht!)** |
| `valueMigrationIds` | — (nicht nötig) | **Pflicht! — aus Beispiel-ZIP übernehmen** |

Die `valueMigrationIds` für BSI 26.1.8 (Stand 2026-06-23) können aus `.agents/skills/process-expert/examples/bsi-2026-06-23_14-08-35.zip` → `index.json` übernommen werden.

#### ID-Typen je Produkttyp (KRITISCH)

Falsche `_type`-Werte im `id`-Feld eines Index-Items führen sofort zu „Ungültiges Format":

| Produkt | Gültiger `_type` für item `id` | Beispiel |
|---|---|---|
| EIP Interface | `bsiscout.IdConfigurationTransferId` | `"id": "interfaces.InterfaceConfigId:<uuid>"` |
| CRM Prozess | `crm.UidConfigurationTransferId` | `"uid": "1;1;1;j100000001;j45831"` |
| CRM Referenz (UID) | `crm.UidConfigurationTransferId` | `"uid": "1;112192;106064;j246;j71099"` |
| CRM Referenz (DomainKey) | `crm.DomainKeyConfigurationTransferId` | `"domainKey": "1;112215;163540;s<uuid>"` |

**Niemals verwenden:** `crm.GlobalUniqueIdConfigurationTransferId` — dieser Typ existiert in BSI nicht.

#### CRM-Prozess `itemGroupId` und `resourcePath`

```json
"itemGroupId": "crm.configurable-code-type.45831.main",
"resourcePath": "codes/Prozess-45831/<Name>_(Version)-<uuid>.json"
```

Die `45831` ist die BSI-Standard-Prozessgruppe. Für neue (nicht aus einem Livesystem exportierte) Prozesse: **`itemGroupId`** und **`resourcePath`** nur am Hauptprozess-Item setzen — **nicht** an den Step-Code-Items.

**Pflichtfelder auf `full`-Items (KRITISCH):**

| Feld | Hauptprozess | Unterstützende Dateien (Sprachen, Org, Teams…) | Step-Code-Items |
|---|---|---|---|
| `root` | `true` | `null` / weglassen | `null` / weglassen |
| `typeVersions` | Vollständiges Mapping aller `_type`→Version im Transfer | Mapping der enthaltenen Typen | weglassen |
| `dataModelNamespaceVersions` | `["bsiscout-25.1.0","crm-25.2.2","cstudio-22.0.0","crocus-1.0.0","oroya-1.0.0"]` | weglassen | weglassen |
| `itemGroupId` | `"crm.configurable-code-type.45831.main"` | Typ-spezifisch (s.u.) | weglassen |

**`itemGroupId`-Werte je Item-Typ:**

| Item-Typ | `itemGroupId` |
|---|---|
| Hauptprozess | `crm.configurable-code-type.45831.main` |
| Sprachen (`j71099`) | `crm.configurable-code-type.71099.main` |
| Organisationseinheiten (`j117890`) | `crm.configurable-code-type.117890.main` |
| Virtuelle Teams (`j109730`) | `crm.configurable-code-type.109730.main` |
| Teamtypen (`j137825`) | `crm.configurable-code-type.137825.main` |
| Prozessgruppe | `crm.process-group` |
| Reference-only Code (`1;112192;106064;jZ;jN`) | `crm.code-type.N` |
| CodeType (`1;112192;144269;jN`) | `crm.domain-key.144269` |
| Service-Line (`1;112215;111828;jZ`) | `crm.domain-key.111828` |
| StepDefinition (`1;112215;45832;jZ`) | `crm.configurable-code-type.45831.partial` |

**Step-Code-Items** (Start, Ende und alle Zwischenschritte) sind in der Hauptprozessdatei eingebettet. Ihr Index-Eintrag hat nur diese Felder:

```json
{
  "_type": "bsiscout.ConfigurationTransferItem",
  "_typeVersion": "bsiscout-22.0.0",
  "globalUniqueId": "<uuid>",
  "id": { "_type": "crm.UidConfigurationTransferId", "_typeVersion": "crm-22.0.0", "uid": "1;112192;106064;j<Z>;j45831" },
  "names": { "de": "Prozessschritt" },
  "transferType": "full"
}
```

Kein `resourcePath`, kein `itemGroupId`, keine `dataModelNamespaceVersions` — sonst: „Fehlerhafte Index-Datei".

**Korrekte UID-Struktur für neue Prozesse:** `1;112192;106064;j<Z>;j45831` mit Z ≥ 1.000.000 — **nicht** `1;1;1;j...`.

#### CRM-Prozess `primary-processes`-Datei (KRITISCH)

Die Datei im Ordner `primary-processes/` hat **nicht** `_type: crm.PrimaryProcessReference` — dieser Typ existiert im BSI-Deserializer **nicht** und führt zu:
> *„Could not resolve a class by parsed entity type … [entityType=crm.PrimaryProcessReference]"*

Korrektes Format:
```json
{
  "_type": "crm.PrimaryProcessIdTransfer",
  "_typeVersion": "crm-22.0.0",
  "key": "1;112215;163540;s<PROC_GID>",
  "topProcessNoPartition": false
}
```

Der `key`-Wert ist identisch mit dem `domainKey` des Primary-Process-Index-Eintrags.

### 3c. BSI CX / Studio-Export (`productId: "studio"`)

Für BSI-CX-Exporte (Customer Stories) gelten dieselben Index-Grundregeln. Spezifika:

| Aspekt | Wert |
|---|---|
| `productIdentifier` | **`"studio"`** (Pflicht) |
| `productVersion` | **`"26.1.8"`** (Pflicht) |
| `valueMigrationIds` | Pflicht — 15 UUIDs, aus einem studio-Beispiel-Export übernehmen (`.agents/skills/cx-expert/examples/`) |
| Namespace | `["studio-25.1.0","bsiscout-25.1.0","crm-25.2.2","crocus-1.0.0","oroya-1.0.0","start-22.0.0"]` |

**ID-Typen / itemGroupId:**

| Artefakt | `itemGroupId` | `id` / transferType |
|---|---|---|
| Story | `studio.story` | `studio.StoryConfigId:<uuid>` · full |
| Content / Design | `studio.content` / `studio.design` (+ `…partial`) | `studio.ContentId`/`DesignId:<uuid>` · full (Ordner mit `content.json`/`design.json` + Ressourcen) |
| Flavor / Indikator / Medien | `studio.flavor` / `studio.indicator` / `studio.media-library-item` | `bsiscout.IdConfigurationTransferId` · full |
| Konfigurierter Step | `studio.configuredStep` | full |
| Step-Typ / Outlet-Funktion | `studio.step.type` / `studio.outlet-function-type` | **reference-only** (im Zielsystem vorhanden, `optionalType: "preserve"`) |
| referenzierte CRM-Codes | `crm.*` | reference-only (CRM-Regeln s. o.) |

**Multi-Produkt-Paket (CX + CRM):** `multi-index.json` (`bsiscout.ConfigurationTransferMultiIndex`) mit `stages[]` (je `productId`, `rootPath` `01-crm`/`02-studio`, `foreignIdMappings`). Importreihenfolge: CRM vor studio.

> Vollständige Struktur, Story-/Step-Objektmodell und Content/Design-Details: **`.agents/skills/cx-expert/knowledge/cx_export_format.md`**.

### 4. `globalUniqueId` in index.json (KRITISCH)

Jedes Item im Index **muss** ein `globalUniqueId`-Feld haben. Fehlt es, bricht BSI mit:
> *„getExistingTargetSystemIds: expected global unique ID to start with 'Code/'"*
> *„Abhängigkeit kann nicht aufgelöst werden"*

**Ableitungsregeln aus der BSI-UID (`1;X;Y;jZ;jN`):**

| UID-Muster | `globalUniqueId` |
|---|---|
| `1;112192;106064;jZ;jN` mit Z < 1.000.000 | `Code/N/Z` |
| `1;112192;106064;j246;j71099` (Sprachen, Z < 10.000) | nur die Zahl: `"246"` |
| `1;112192;144269;jN` (CodeType) | `CodeType/N` |
| `1;112215;45832;jZ` (StepDefinition) | `ProcessStepDefinition/Z` |
| `1;112215;163540;s<uuid>` (PrimaryProcess) | `<uuid>` (ohne `s`) |
| `1;112192;106064;j1000xxx;jN` (kundeneigene Objekte, Z ≥ 1.000.000) | **UUID aus dem BSI-Dateinamen** des Objekts (z.B. `Organisation-00c27100-....json` → `"00c27100-..."`) — **NICHT** `Code/N/Z` |
| Service-Line-Keys (`1;112215;111828;jZ`) | UUID aus dem Beispiel-ZIP |

### 5. Checkliste bei „Fehlerhafte Index-Datei" (KRITISCH)

Tritt der BSI-Fehler **„Fehlerhafte Index-Datei"** oder **„Ungültiges Format der Index-Datei"** beim Import auf, die folgenden Punkte der Reihe nach prüfen:

| # | Prüfpunkt | Häufigste Ursache |
|---|---|---|
| 1 | `_type: bsiscout.ConfigurationTransferIndex` vorhanden? | Falscher oder fehlender Root-Typ |
| 2 | `productIdentifier: "crm"` und `productVersion: "26.1.8"` gesetzt? | Nur bei CRM-Exporten Pflicht — fehlt bei EIP-Exporten |
| 3 | `valueMigrationIds` vorhanden? | Bei CRM-Exporten Pflicht — aus Beispiel-ZIP übernehmen |
| 4 | Alle `id`-Felder der Index-Items verwenden den richtigen `_type`? | `crm.UidConfigurationTransferId` für UIDs, `crm.DomainKeyConfigurationTransferId` für DomainKeys — **niemals** `crm.GlobalUniqueIdConfigurationTransferId` |
| 5 | Jedes Index-Item hat ein `globalUniqueId`-Feld? | Fehlendes Feld → „expected global unique ID to start with 'Code/'" |
| 6 | `globalUniqueId` korrekt abgeleitet? | Z ≥ 1.000.000 → UUID aus Dateinamen, nicht `Code/N/Z` |
| 7 | Alle in `referencedItems` referenzierten IDs haben einen eigenen Index-Eintrag? | Fehlender Eintrag → „Inkonsistenter Index" |
| 8 | Kachel-Items (Kachelschritt) als `full`-Item mit `domainKey`-ID eingetragen? | Fehlt → „unbekannte Referenz" |
| 9 | Enthält `referencedItems` ALLE UIDs aus dem Prozess-JSON? | Jede UID im Prozess-JSON (außer Outlet-UIDs `1;112215;206820;s...` und die eigene Prozess-UID) muss in `referencedItems` stehen — auch `codeTypeKey` (`1;112192;144269;j45831`) |

### 6. Verwendung von Best-Practice-Beispielen
- **Beispiele-Pfad**: `.agents/skills/export-expert/examples/`
- Konsultiere bei der Erstellung neuer ZIP-Dateien immer die Beispiele und die zugehörige [README.md](examples/README.md) in diesem Ordner, um bestehende Pattern und Implementierungsstile zu übernehmen.