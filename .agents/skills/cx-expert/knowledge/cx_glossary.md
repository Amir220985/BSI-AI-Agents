# BSI CX – Glossar

> Begriffe aus BSI CX (`studio`), belegt durch Beispiel-Exporte und Help-Center-Doku.

## Kernobjekte
| Begriff (`_type`) | Bedeutung |
|---|---|
| **Story** (`studio.StoryConfig`) | Customer Story — der automatisierte Ablauf, aus Steps aufgebaut. Kleinste lauffähige Einheit der Marketing Automation. |
| **Step** (`studio.StepConfig`) | Baustein einer Story; kleinste Gestaltungseinheit. Hat `customConfig` (Identität via `_type`), Outlets, Attribute. |
| **Steplet** (`…StepletConfig`) | Die konkrete Step-Konfiguration im `customConfig`; ihr `_type` bestimmt den Step-Typ. |
| **Outlet** (`studio.OutletConfig`) | Ausgang eines Steps; verbindet via `targetStepGid` zum Folge-Step. Kann Indikatoren und Outlet-Funktionen tragen. |
| **Flavor** (`studio.FlavorConfig`) | Story-Typ/Kategorie (z. B. Journey, Mailing). Pflicht je Story; definiert verfügbare KPIs. |
| **Content** (`studio.Content`) | Inhalt für Push-Steps (E-Mail, Landingpage, SMS, Dokument …), mehrsprachig, typisiert. |
| **Design** (`studio.DesignConfig`) | Layoutvorlage für designfähige Content-Typen. |
| **Indikator** (`studio.indicator`) | KPI-Zähler (Versendet, Gelesen, Conversion, Bounces, Umsatz …). |
| **Media-Library-Item** | Mediathek-Objekt (Bild/Dokument) zur Verwendung in Content/Design. |
| **Konfigurierter Step** (`studio.configuredStep`) | Per Low-Code/JavaScript erstellter Custom-Step (Administration › CX › Konfigurierte Steps). |

## Story-Konzepte
| Begriff | Bedeutung |
|---|---|
| **Teilnehmer** | Personen/Datensätze, die durch die Story laufen (aus CRM, CSV, Webshop, ERP …). |
| **Story-Attribut** (`studio.PropertyConfig` auf Story) | Daten, die über die Story hinweg getragen werden. |
| **Step-Attribut** | Vom Step erzeugte Daten, in Folge-Steps via Picker nutzbar. |
| **Substory** | Wiederverwendbarer Teil-Flow (`substory=true`), via Prozedur-Steps eingebunden. |
| **Muster/Template** (`template=true`) | Vorlage zur Neuanlage von Stories. |
| **Status** | `draft` (Entwurf) → `live` → `sunset` (auslaufend); danach archiviert. |
| **executionType** | `manual` (manuell gestartet) / `auto` (automatisch). |
| **Versionierung** | Neue Version übernimmt den Lead, alte läuft im Sunset-Modus aus. |
| **Indikator/KPI** | Erfolgsmessung in Mission Control; KPIs pro Flavor definiert. |
| **Outlet-Funktion** (`studio.outlet-function-type`) | Funktion direkt am Step-Ausgang (z. B. Attribut setzen, Weiterleitung, Zeitpunkt) — ersetzt teils Folge-Steps. |

## Step-Arten (Doku)
**Teilnehmer · Logik · Daten · Push · Prozedur** (+ Hilfsgruppen Attribute/Web-Online/Prototyping). Siehe `cx_step_type_catalog.md`.

## Content-Typen
`email`, `landing-page`, `word-document`, `pdf-document`, `sms`, `news-snippet`, `whatsapp`, `gespraechsleitfaden`, `ical`, `preview`. Siehe `cx_content_and_design.md`.

## Technik / Export
| Begriff | Bedeutung |
|---|---|
| **studio** | Produkt-Identifier von BSI CX in Exporten (`productId`/`productIdentifier`). |
| `bsiscout.ConfigurationTransferIndex` | Manifest (`index.json`). |
| `bsiscout.IdConfigurationTransferId` | ID-Form `studio.<Typ>Id:<uuid>`. |
| `studio.UuIdWithRevisionConfigurationTransferId` | ID mit Revision (Content/Design/Story-Partial). |
| `valueMigrationIds` | Pflicht-UUIDs in der studio-`index.json` (aus Beispiel übernehmen). |
| `multi-index.json` (`bsiscout.ConfigurationTransferMultiIndex`) | Multi-Produkt-Paket (CRM + studio), Stages mit `rootPath`/`foreignIdMappings`. |
| **crocus** | Namespace für Low-Code/konfigurierte bzw. kundenspezifische Steps (`crocus.*StepletConfig`). |
| **start** | Namespace für Querschnitt (Ordner, Verantwortliche): `start.folder`, `start.responsible`. |
| **suite** | Suite-weite Einstellungen: `suite.setting`. |

## Domänen-Integrationen (Beispiele)
- **inSign** (`crocus.PushInsign`) — elektronische Signatur / QES.
- **ExecuteBrain** — Machine-Learning-/AI-Step („Brain").
- **CRM-Trigger** (`crocus.CrmTriggerProducer`) — Story-Auslöser aus BSI CRM.
