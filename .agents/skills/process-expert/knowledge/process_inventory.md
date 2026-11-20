# BSI Process Inventory

> Quelle: 10 BSI-CustomerSuite-Exporte vom 2026-06-24 (`bsi-crm-2026-06-24_15-05-14` … `_15-09-39`).
> Produkt: `crm`, Exportformat `bsiscout.ConfigurationTransfer` (Typversionen crm-22.0.0 … crm-24.2.x).
> Mandant/Domäne (abgeleitet aus E-Mail-Konten `*@cargarantie.com`): **CarGarantie** — Kfz-Garantie/-Versicherung. *(Annahme, belegt durch `email-accounts/`)*
> Backend-Integration (abgeleitet aus Lambda-Step-Namen): **IBM i (AS/400)** und **CS-API** als führende Bestandssysteme. *(belegt durch lambda-bindings: „Daten zu IBM i pushen", „Kunde aus IBM i laden", „Start Push zu CS-API")*

## 0. Export-Struktur (Faktenlage)

Jeder Export ist ein ZIP mit:

| Datei/Ordner | Inhalt |
|---|---|
| `index.json` | `bsiscout.ConfigurationTransferIndex` — Liste aller Items mit `uid`, `names` (de/en/it/fr), `referencedItems`, `resourcePath` |
| `export-definition.json` | `bsiscout.ConfigurationExportDefinition` — `rootTransferIds` (Wurzelobjekt des Exports), `productId` |
| `export-log.txt` | Exportprotokoll |
| `codes/Prozess-45831/*.json` | **Prozessdefinitionen** (`crm.ProcessTransfer`) — der eigentliche Ablauf |
| `codes/Prozessgruppen-45831/*.json` | **Prozessgruppen** (`crm.CrmCode`, codeType 45831) — Kategorisierung |
| `codes/*` | Stammdaten-Codes: Sprachen, Rollen, Teamtypen, Virtuelle Teams, Berechtigungsstufen, Fehlermeldungen, Kanäle, Sparten, Länder, Ereignistypen, Felder etc. |
| `primary-processes/*.json` | `crm.PrimaryProcessIdTransfer` — nur ID-/Referenzhüllen (Globale Referenz), **keine** Ablauflogik |
| `datamodel/{entities,fields,categories}` | Datenmodell-Erweiterungen (z. B. Beschwerdeführer, Dublette, Bankverbindung, Fahrzeug) |
| `lambda-bindings/*.json` | `bsiscout.LambdaBinding` — Integrationsaufrufe (Low-Code/EIP), `lambdaConsumerId`, `lambdaId`, `inputs`/`outputs` mit DataModel-Selections |
| `email-accounts/*.json` | Postfächer für Outbound-/Service-Mails |
| `global-texts/`, `lambda-bindings/` | Textbausteine, Integrationsbindungen |

**Aufbau einer Prozessdefinition** (`crm.ProcessTransfer`):
- `processConfig` (`crm.ProcessConfig`): `name`, `gid`, `id`, `processStepGroups[]` (visuelle Swimlanes/Gruppen mit Farbe), `processSteps[]` (Graph-Knoten: `typeId`, `outlets[]` mit `targetProcessStepId` + `configurationName` als Verbindungslabel, `position`, `groupId`).
- `processDefinition` (`crm.ProcessDefinition`): `activeProcessInputs`, `availableTemplateUids` (Dokument-/Korrespondenzvorlagen), `escalationSlaTimeConfig`, `overdueSlaTimeConfig`, `processResponsibleTeamUid`, `reopenCaseStepUid`/`reopenCaseTypeUid` (Wiederaufnahme), `processAvailabilityUid`, `processCaseCreationUid`.
- `processStepDefinitions[]` (`crm.ProcessStepDefinition`): fachliche Konfiguration je Step — `stepDefinitionKey` (endet auf `j<typeId>`), `languageItems[]` (Step-Name de/en/it/fr), `bindings[]` (Datenanbindung über `DataModelRelationSelection`/`DataModelAttributeSelection`), `responsibility` (Zuständigkeit), `outlets`, `visibleAttributes`, `selectedTemplateUids`, `plannedTimeInSeconds`, SLA-Felder.

## 1. Kleine Exporte (9×): Prozessgruppen

Diese 9 Exporte enthalten je **eine Prozessgruppe** (`crm.CrmCode`, codeType `45831`, `scriptIdentifier = Process.<Name>`) plus die referenzierten Sprach-Codes. Es sind **Kategorien/Container für Prozesse**, keine Ablauflogik.

| Export | Prozessgruppe | scriptIdentifier | sortcode |
|---|---|---|---|
| 15-05-14 | Customer Agents | `Process.*` | — |
| 15-05-33 | Social Media | | |
| 15-05-43 | SEPA-Mandat | | |
| 15-06-01 | Service | `Process.Service` | 30 |
| 15-06-10 | Marketing | | |
| 15-06-24 | Vertrieb | | |
| 15-06-33 | Snapview | | |
| 15-06-41 | Companion | | |
| 15-06-51 | Vertrieb (2. ID) | | |

> Auffälligkeit: Es existieren **zwei** Prozessgruppen mit Namen „Vertrieb" (IDs `…j1000009382` und `…j1000116592`). Mögliche Dublette oder bewusste Mandanten-/Spartentrennung — **offene Frage**.

## 2. Großer Export (15-09-39): 19 Prozesse + Stammdaten

Wurzelobjekt: Prozess „Kunde – Daten ändern". Der Export zieht über `referencedItems` **18 weitere abhängige Prozesse** sowie das gesamte benötigte Datenmodell, Lambda-Bindings, Codes und E-Mail-Konten nach (transitive Abhängigkeitsauflösung).

Komplexität = Step-Anzahl: **einfach** ≤10 · **mittel** 11–30 · **komplex** 31–60 · **sehr komplex** >60.

| # | Prozess (Version) | Steps | Gruppen | Lambda-Steps | Domäne / Zweck | Kern-Entitäten | Komplexität | Reopen |
|---|---|---:|---:|---:|---|---|---|:--:|
| 1 | Kunde – Daten ändern (29.0.0) | 57 | 9 | 4 | Stammdatenänderung Kunde (Name/Adresse/Form/Themengebiet) inbound + Self-Service, Push zu IBM i | CrmCase, CrmCustomer | komplex | ✓ |
| 2 | Vertrag – Daten ändern (4.0.0) | 43 | 8 | 6 | Vertragsdaten ändern (KM-Stand, Vertragsbeginn, Bankdaten) inbound + Self-Service, Push IBM i | CrmCase, Contract | komplex | – |
| 3 | Vertrag – Einzelvertrag ändern (10.0.0) | 33 | 9 | 2 | Einzelvertragsänderung mit Kundensuche, Nachladen, Korrespondenz | CrmCase | komplex | – |
| 4 | Vertrag – Einzelvertrag beenden (1.4.0) | 26 | 8 | 1 | Vertragskündigung/-beendigung mit Wiedervorlage & Bestätigung | CrmCase | mittel | – |
| 5 | Kunde – Halterwechsel durchführen (7.0.0) | 25 | 6 | 1 | Halterwechsel Fahrzeug mit Vertrag nachladen, Ablehnung/Erfolg, Unterlagen | CrmCase | mittel | – |
| 6 | Fahrzeug – Daten ändern (1.0.0) | 20 | 5 | 2 | Fahrzeugdaten ändern inbound + Self-Service, Push IBM i | CrmCase, InsuredObject | mittel | – |
| 7 | Stammdaten Sales Location bearbeiten (6.0.0) | 20 | 7 | 1 | Händler-/Standortstammdaten mit **4-Augen-Freigabe**, Update Branch | CrmCase, DealerProduct | mittel | – |
| 8 | Ansprechpartner anlegen (12.0.0) | 13 | 4 | 0 | Neuen Ansprechpartner + initiale Beziehung anlegen | CrmCase | mittel | – |
| 9 | Ansprechpartner bearbeiten (10.0.0) | 16 | 5 | 0 | Ansprechpartner ändern/deaktivieren mit Vorher-Stand & Abbruch | CrmCase | mittel | – |
| 10 | Beschwerde (telefonisch) (7.0.0) | 26 | 8 | 0 | Telefonische Beschwerdeaufnahme, Abklärung (tel./schriftl.), KYC, Empfangsbestätigung | CrmCase, Beschwerdeführer | mittel | – |
| 11 | Abklärung zu Beschwerde (3.0.0) | 5 | 0 | 0 | Sub-/Abklärungsprozess zur Beschwerde, Vorlagenauswahl | CrmCase | einfach | – |
| 12 | KYC-Authentifizierung (17.0.0) | 5 | 2 | 0 | Kundenidentifikation/-authentifizierung (erfolgreich/nicht) | CrmCase | einfach | ✓ |
| 13 | Portalzugang für Kunden freischalten (4.0.0) | 8 | 0 | 1 | Portalzugang prüfen & freischalten via Lambda | CrmCase, CrmCustomer | einfach | – |
| 14 | Neue Kommunikation (7.0.0) | 25 | 4 | 0 | Outbound-/neue Kommunikation (Service/Schaden), Kundensuche, Vorlagen | CrmCase, Root | mittel | – |
| 15 | Kommunikation beantworten (ohne Kundenauswahl) (11.0.0) | 52 | 5 | 0 | E-Mail-/Telefon-Antwort ohne Kundenkontext, Themengebiets-/Dokumenttyp-Zuweisung | CrmCase, Root | komplex | ✓ |
| 16 | Kommunikation weiterleiten (CSS-extern) (1.0.0) | 23 | 3 | 0 | Weiterleitung an externe Stellen (Schaden/Service), Vorlagen | CrmCase, Root | mittel | – |
| 17 | Kommunikation – Themengebiet und Team zuweisen (6.0.0) | 11 | 2 | 2 | Routing: Themengebiet/Team einer Kommunikation zuweisen (Lambda) | CrmCase, Root | mittel | ✓ |
| 18 | Kundenanfrage beantworten (40.0.0) | 85 | 7 | 3 | Zentraler Service-/Inbound-Prozess: Suche, Nachladen, E-Mail/Telefon, Versand | CrmCase, Root | sehr komplex | ✓ |
| 19 | Dokument – Dokumenttyp zuweisen (16.0.0) | 91 | 14 | 17 | Dokumentklassifizierung mit Einzel-/Mehrfach-/Restzuweisung, fachl. Prüfung, viele Lambdas | CrmCase, Root | sehr komplex | – |

### Verantwortlichkeit / Rollen (Faktenlage)
- **`responsibility.responsibleTypeUid` wird in 546 Steps mit *einem einzigen* Typ (`…j71401`) belegt.** Zuständigkeit wird durchgängig über **virtuelle Teams** (`processResponsibleTeamUid`, `responsibleTeamUid`) statt über Einzelrollen gesteuert.
- Konfigurierte virtuelle Teams (`codes/Virtuelle_Teams-109730`): Team_IDD, Serviceleitung, Team_Vertragsanlage, StornoMahnungen_Schaden, Team_Storno, Team_Anfragen, Schadenmeldungen_AG, Schadenleitung, Kundendienst, OCG_Backoffice_Admin, Team_Änderung, GB_English_Claims, CampGarantie u. a.
- Technische Rollen (`codes/Rollen-81726`): nur Administration, Administrator, Entwicklung → **System-/Admin-Rollen**, nicht fachliche Prozessrollen.
- Berechtigungsstufen (`codes/Berechtigungsstufen-180508`): Öffentlich, Geschützt, Vertraulich, Geheim.
- Betreuer-Typen (`codes/Typen-113690`): Hauptbetreuer, Betreuer.

### Schnittstellen (Faktenlage aus `lambda-bindings/`)
Integrationen sind durchgängig als **Lambda-Aufrufe** (Step-Typ `209754` + asynchrone Varianten) modelliert. Wiederkehrende Integrationszwecke:
- **IBM i laden/pushen**: „Kunde aus IBM i laden", „Daten zu IBM i pushen" (Kunde, Vertrag, Fahrzeug).
- **CS-API**: „Start Push zu CS-API" (Vertrag).
- **Hintergrundänderungen**: „Bankverbindung/Bankdaten/Vertragsbeginn/Kilometerstand/Kundenform/Namensänderung im Hintergrund ändern".
- **Dokument**: „Lambda für Einzel-/Mehrfach-/Restzuweisung", „Dokumenttyp anhand Dateityp", „Fachl. Prüfung starten", „Neuste Verlängerungsstufe finden".
- **Button-Tiles** (`crmlambdaButtonTile`): „Search KVK", „Registerportal", „Aufgabe erstellen".

### Auffälligkeiten (Inventar-Ebene)
- Dublette „Vertrieb"-Prozessgruppe (s. o.).
- Prozess „Dokument – Dokumenttyp zuweisen" (91 Steps, 14 Gruppen, 17 Lambdas) und „Kundenanfrage beantworten" (85 Steps) sind **Komplexitäts-Hotspots** → erhöhter Wartungs-/Testaufwand.
- Sehr hohe Vorlagenzahl bei „Kundenanfrage beantworten" (58 Templates) und „Kommunikation beantworten" (55 Templates).
- Mehrere Tippfehler in Gruppen-/Stepnamen (z. B. „Ungültiger sStart", „Starkommunikation", „Vetragsanzeige", „Beschwerdeführe") — siehe Anti-Patterns.
