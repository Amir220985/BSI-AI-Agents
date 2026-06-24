# BSI Process Glossar

> Begriffe, Status, Rollen, technische Elemente und Konzepte aus den analysierten Exporten.
> Quelle: `bsi-crm-2026-06-24_15-09-39` und 9 Prozessgruppen-Exporte. Wo eine Bedeutung interpretiert ist, ist sie als *(Annahme)* markiert.

## Technische Export-/Konfigurationsobjekte

| Begriff (`_type`) | Bedeutung |
|---|---|
| `bsiscout.ConfigurationTransferIndex` | Manifest eines Exports: alle Items mit UID, mehrsprachigen Namen, Referenzen, Ressourcenpfaden. |
| `bsiscout.ConfigurationExportDefinition` | Export-Header: `rootTransferIds` (Wurzelobjekt(e)), `productId`. |
| `crm.ProcessTransfer` | Container einer exportierten Prozessdefinition. Enthält `processConfig`, `processDefinition`, `processStepDefinitions`. |
| `crm.ProcessConfig` | **Graph/Layout** des Prozesses: `processSteps`, `processStepGroups`, Positionen, Outlets. |
| `crm.ProcessDefinition` | **Fachliche Rahmenkonfiguration**: Inputs, Templates, SLA-/Eskalations-Config, verantwortliches Team, Wiederaufnahme. |
| `crm.ProcessStepConfig` | Ein **Graph-Knoten** (Step) mit `typeId`, `outlets`, `groupId`, `position`. |
| `crm.ProcessStepDefinition` | **Fachliche Step-Konfiguration**: Name (`languageItems`), `bindings`, `responsibility`, `visibleAttributes`, `selectedTemplateUids`, SLA. |
| `crm.ProcessStepGroupConfig` | **Gruppe/Swimlane** im Diagramm (`name`, `color`) — strukturiert Steps fachlich. |
| `crm.ProcessStepOutletConfig` | **Ausgang/Transition** eines Steps: `configurationName` (Label A/B/C…), `targetProcessStepId`, `presentation` (primary/…), `button`, `defaultButton`. |
| `crm.PrimaryProcessIdTransfer` | Referenzhülle „Globale Referenz" auf einen Prozess (keine Logik). |
| `crm.CrmCode` | Wertelisten-Eintrag (Code). Genutzt für Prozessgruppen, Sprachen, Rollen, Teams, Sparten etc. |
| `bsiscout.LambdaBinding` | **Integrationsbindung** (Low-Code/EIP): `lambdaConsumerId`, `lambdaId`, `inputs`/`outputs` mit DataModel-Selections, `prototypeName`. |
| `bsiscout.DataModelRelationSelection` / `…AttributeSelection` | **Datenanbindung**: navigiert über `containerEntityId`, `joins` (`relation`, `targetType`), `selections` (Attribute, `fieldType`). |

## Identifikatoren

| Begriff | Bedeutung |
|---|---|
| `uid` (`crm.UidConfigurationTransferId`) | Mehrteilige UID `mandant;…;objektId;codeTypeId`, z. B. `1;112192;106064;j1000009406;j45831`. `j<n>` = numerische Objekt-/Typ-ID. |
| `gid` | Globale GUID eines Prozesses/Steps (z. B. `96f1abe0-…`). Stabil über Versionen. |
| `id` | Versions-/Instanz-GUID (ändert sich je Prozessversion). |
| `typeId` | Numerischer Step-Typ (siehe `bsi_step_type_catalog.md`). |
| `stepDefinitionKey` | `1;112215;45832;j<typeId>` — verknüpft StepDefinition mit Step-Typ. |
| `codeType 45831` | Code-Typ für **Prozesse und Prozessgruppen**. |
| `scriptIdentifier` | Skript-Name eines Codes, z. B. `Process.Service`. |

## Fachliche Kern-Entitäten (Datenmodell)

| Entität | Bedeutung |
|---|---|
| `CrmCase` | **Geschäftsvorfall** — zentrale Prozessinstanz/Akte. In nahezu jedem Step als `containerEntityId`. |
| `CrmCustomer` | Kunde. |
| `Root` | Wurzel-Kontext der DataModel-Selection (Einstiegspunkt für Joins, z. B. `lambdaContextRelation-case`). |
| `Contract` / Insurancecrm Contract | Vertrag. |
| `InsuredObject` | Versichertes Objekt / Fahrzeug. |
| `PaymentMethod` | Zahlungsart / Bankverbindung. |
| `Beschwerdeführer` (CaseDublicate, CaseEMailAdresses) | Beschwerde-spezifische Sub-Entitäten. |
| `DealerProduct` | Händler-Produkt (Sales Location). |
| `Dublette` (CaseDublicate) | Dubletten-Erkennung. |

## Prozessgruppen (Kategorien, codeType 45831)

Customer Agents · Social Media · SEPA-Mandat · Service (`Process.Service`, sortcode 30) · Marketing · Vertrieb (2×) · Snapview · Companion.
→ Strukturieren das Prozess-Portfolio nach Vertriebs-/Service-/Kanal-Domänen. *(Annahme: Snapview/Companion = BSI-Produktmodule für Co-Browsing bzw. Agent-Assist.)*

## Rollen-, Team- & Berechtigungsmodell

| Begriff | Werte / Bedeutung |
|---|---|
| **Virtuelle Teams** (`Virtuelle_Teams-109730`) | Fachliche Bearbeitungsteams: Team_Anfragen, Team_Änderung, Team_Storno, Team_Vertragsanlage, Kundendienst, Serviceleitung, Schadenleitung, Schadenmeldungen_AG, StornoMahnungen_Schaden, Team_IDD, GB_English_Claims, CampGarantie, OCG_Backoffice_Admin. **Primärer Träger der Prozesszuständigkeit.** |
| **Rollen** (`Rollen-81726`) | Nur technisch: Administration, Administrator, Entwicklung. |
| **Betreuer-Typen** (`Typen-113690`) | Hauptbetreuer, Betreuer. |
| **Berechtigungsstufen** (`Berechtigungsstufen-180508`) | Öffentlich, Geschützt, Vertraulich, Geheim. |
| `responsibility.responsibleTypeUid` | Zuständigkeitstyp je Step. In den Exporten durchgängig **ein** Typ (`…j71401`) → Zuweisung erfolgt über `responsibleTeamUid`/`processResponsibleTeamUid`. |
| `enforceResponsibility` | Erzwingt, dass nur der zuständige Bearbeiter den Step ausführt. |
| `allowTeamUserStart` | Erlaubt jedem Team-Mitglied den Start des Steps. |

## SLA-, Eskalations- & Wiederaufnahme-Konzepte

| Feld | Bedeutung |
|---|---|
| `escalationSlaTimeConfig` | Eskalationsfrist + `escalationWarningPercentage`, `responsibleTeam(Role)Uid`, `automaticAssignCase`. |
| `overdueSlaTimeConfig` | Überfälligkeits-/Überschreitungs-Konfiguration. |
| `defaultFollowUpTimeInSeconds` / `…UnitUid` | Standard-Wiedervorlagefrist. |
| `reopenCaseStepUid` / `reopenCaseTypeUid` / `reopenCaseNewStepDefinitionKey` | **Wiederaufnahme** eines abgeschlossenen Geschäftsvorfalls (Reopen). Gesetzt in: Kunde Daten ändern, KYC, Kommunikation beantworten, Kommunikation Themengebiet zuweisen, Kundenanfrage beantworten. |
| `plannedTimeInSeconds` / `…UnitUid` (Step) | Geplante Bearbeitungszeit je Step. |
| `slaAdjournment` / `slaAdjournmentTypeUid` | SLA-Stundung/-Aussetzung. |

## Korrespondenz & Kommunikation

| Begriff | Bedeutung |
|---|---|
| `availableTemplateUids` / `selectedTemplateUids` | Verfügbare/ausgewählte **Dokument-/E-Mail-Vorlagen** des Prozesses bzw. Steps. |
| `email-accounts` | Outbound-Postfächer (z. B. `css-outbound@…`, `css-test-idd@…`, `css-test-beschwerde@…`). |
| Kanäle (`Kanäle-71074`, `Kanäle-113637`) | Kommunikationskanäle. |
| Reaktionsgruppen (`Reaktionsgruppen-71080`) | z. B. „Anruf-Resultat". |
| Ereignistypen (`Ereignistypen-210109`) | z. B. „Konfiguration". |

## Integration / Backend (abgeleitet)

| Begriff | Bedeutung |
|---|---|
| **IBM i** | AS/400-Bestandssystem; „Kunde/Vertrag/Fahrzeug aus IBM i laden", „Daten zu IBM i pushen". |
| **CS-API** | Schnittstelle „Start Push zu CS-API" (Vertrag). |
| **Lambda** | Low-Code/EIP-Funktion, aus Prozess-Step (`209754`/Hintergrund) aufgerufen. |
| `crmlambdaButtonTile` | Lambda hinter einer Button-Kachel (z. B. „Search KVK", „Registerportal", „Aufgabe erstellen"). |
| „im Hintergrund ändern" | Asynchrone Schreiboperation ins Backend nach fachlicher Erfassung (Dunkelverarbeitung). |

## Wiederkehrende fachliche Konzepte

- **Geschäftsvorfall (GV)** = Prozessinstanz auf `CrmCase`.
- **Inbound vs. Self-Service**: viele Stammdatenprozesse haben getrennte Pfade „Inbound – …" (Agent) und „Self Service – …" (Kunde).
- **Kunden checken und nachladen**: Standard-Gruppe zum Abgleich/Nachladen aus IBM i.
- **Themengebiet- und Team-Zuweisung**: Routing-Mechanik (eigener Prozess + als Subprozess eingebunden).
- **Vorher-Stand speichern**: Snapshot vor Änderung (für 4-Augen-Vergleich/Rollback).
- **Dunkelverarbeitung**: automatischer Hintergrund-Push mit manuellem Fehlerpfad bei „Lambda erfolgreich? = nein".
