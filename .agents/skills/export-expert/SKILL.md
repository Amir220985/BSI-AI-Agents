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

### 1. Verwendung der EIP-Steps-Registry
Sämtliche für die Schnittstellenerstellung verfügbaren Steps müssen aus der zentralen Registry abgerufen und referenziert werden:
- **Registry-Pfad**: `registry/eip_step_registry.json`
- Konsultiere immer diese Datei, um die genauen Typdefinitionen, Eingabe- und Ausgabeparameter sowie Metadaten der Steps zu prüfen.

### 2. Der Low-Code-Step (TypeScript)
Wenn Standard-Steps nicht ausreichen oder komplexe Validierungen, Transformationen oder bedingte Logik benötigt werden, greifst du auf den **Low-Code-Step** zurück:
- Implementiere die Logik in **TypeScript**.
- Achte auf sauberen, performanten und fehlerresistenten Code (z.B. defensives Programming gegen Null- oder Undefined-Werte).
- Nutze die vordefinierten Typen und Schnittstellen der BSI CustomerSuite.

### 3. Vorgehensweise bei der Interface-Erstellung
1. **Quellen-Auswahl**: Prüfe in `exports/`, welche fertigen Konfigurationen es gibt, die in die Export-Datei übernommen werden sollen.
2. **Zusammensetzung**: Setze aus den Quellen eine valide ZIP-Datei zusammen, die in BSI importiert werden kann.

### 4. Konsistenzregel für den Index (KRITISCH)

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

### 5. Pflichtfelder index.json je Produkttyp (KRITISCH)

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

Die `45831` ist die BSI-Standard-Prozessgruppe. Für neue (nicht aus einem Livesystem exportierte) Prozesse: synthetische UID `1;1;1;j<großeZahl>;j45831` verwenden — BSI nutzt `globalUniqueId` zur Duplikaterkennung.

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

### 6. `globalUniqueId` in index.json (KRITISCH)

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

### 7. Checkliste bei „Fehlerhafte Index-Datei" (KRITISCH)

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

### 8. Verwendung von Best-Practice-Beispielen
- **Beispiele-Pfad**: `.agents/skills/export-expert/examples/`
- Konsultiere bei der Erstellung neuer ZIP-Dateien immer die Beispiele und die zugehörige [README.md](examples/README.md) in diesem Ordner, um bestehende Pattern und Implementierungsstile zu übernehmen.