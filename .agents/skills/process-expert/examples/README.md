# Process Spezialist – Beispiele

Dieses Verzeichnis enthält bewährte Vorlagen und Beispiel-Prozesse aus realen Projekten für die Prozess-Engine der BSI CustomerSuite.

## Übersicht der Beispiele

### `bsi-2026-06-23_14-08-35.zip`
Export aus einem produktiven BSI CustomerSuite-System (Version 25.2, `crm-25.2.007`).

**Enthält 41 vollständige Business-Prozesse** aus dem Bereich CRM/Kundenservice, aufgeteilt nach Domänen:

#### Allgemeine Kundeninteraktion (einfache Prozesse, 2–4 Steps)
| Prozess | Version | Steps | Besonderheit |
|---|---|---|---|
| Allgemeine Anfrage | 1.0.0 | 3 | Minimalbeispiel: Start → Interaktion → Ende |
| Angebotsanfrage | 1.0.0 | 3 | Wie Allgemeine Anfrage, anderes Formular |
| Serviceanfrage | 1.0.0 | 3 | Einfacher Servicefall |
| Interesse bearbeiten | 1.0.0 | 3 | 2× vorhanden (unterschiedliche typeId-Varianten) |
| Kommunikation erstellen | 1.0.0 | 3 | Kommunikationserfassung |
| Aufgabe erstellen | 1.0.0 | 3 | To-do-Anlage |
| Sonstiges | 1.0.0 | 8 | Fallback-Prozess mit Verzweigungen |
| Chat Agent | 0.0.3 | 3 | KI-Chat-Eingang |
| Voice Agent | 0.0.1 | 2 | Nur Start+Ende (Stub) |

#### Kundenstamm & Compliance
| Prozess | Version | Steps | Besonderheit |
|---|---|---|---|
| Kunde erfassen | 1.0.0 | 3 | Neuanlage |
| Person erfassen | 1.0.0 | 3 | Personenanlage |
| Adressänderung | 1.0.0 | 4 | Mit Adressänderungs-Step |
| Werbesperre bearbeiten | 1.0.0 | 3 | Opt-out |
| Kontaktsperre setzen | 1.0.0 | 3 | Kontaktsperre |
| Löschen auf Verlangen | 1.0.0 | 3 | DSGVO-Löschprozess |

#### Vertrieb & Angebote
| Prozess | Version | Steps | Besonderheit |
|---|---|---|---|
| Neuer Auftrag | 2.0.0 | 8 | Mehrstufig, Gruppen (Vertrieb + Pricing-Board) |
| Neues Angebot erstellen | 1.0.0 | 9 | Komplex, mit Lambda-Steps |
| Terminvereinbarung | 1.0.0 | 5 | Terminschritt + Korrespondenz |
| Besprechung starten | 1.0.0 | 6 | Mit Lambda-Step |
| Planung Probefahrt | 1.0.0 | 3 | Probefahrtplanung |
| Nachfassen Probefahrt | 1.0.0 | 8 | Nachbearbeitung |
| Besuch nachbereiten | 0.0.5 | 9 | Viele Step-Typen, Lambda |
| Marketingaktion freigeben | 1.0.0 | 7 | Freigabe-Workflow |
| Freigabe | 1.0.0 | 4 | Generischer Freigabeprozess |

#### Beschwerden & Rückfragen
| Prozess | Version | Steps | Besonderheit |
|---|---|---|---|
| Beschwerde | 2.0.0 | 11 | Komplex, viele Verzweigungen |
| Abklärung zu Beschwerde | 1.0.0 | 5 | Eskalationssub-Prozess |
| Rückfrage zur Deckung | 1.0.0 | 6 | Mit Lambda + Korrespondenz |
| Kundenanfrage beantworten | 1.0.0 | 4 | Mit Dokumentvorlagen-Step |
| Meldung beantworten | 1.0.0 | 3 | Einfache Antwort |

#### Finanzen & Zahlungen
| Prozess | Version | Steps | Besonderheit |
|---|---|---|---|
| Rechnungsstellung | 1.0.0 | 3 | Rechnungserstellung |
| Lastschriftrückgabe und Fehlerverarbeitung | 1.0.0 | 15 | Komplexester Prozess: viele Lambda-Steps, Fallunterscheidungen |
| Mandat kündigen | 1.0.0 | 2 | Minimalfall: nur Start+Ende |
| Retourenverarbeitung | 1.0.0 | 12 | Viele verschiedene Step-Typen |
| Betrugsverdacht prüfen | 1.0.0 | 11 | Backend-schwer, mehrere Lambda-Aufrufe |

#### Kommunikation & Agenten
| Prozess | Version | Steps | Besonderheit |
|---|---|---|---|
| Mail Agent | 0.0.1 | 13 | Komplexer KI-Mail-Routing-Prozess |
| Ausgehende Mail | 0.0.2 | 4 | Mit Lambda + Dokumentvorlage, Process-Automation |
| Reaktion erfassen | 1.0.0 | 3 | Eingehende Reaktionserfassung |
| Neues Posting | 1.0.0 | 7 | Social-Media-Posting, spezielle Step-Typen |

#### Wissen & Content
| Prozess | Version | Steps | Besonderheit |
|---|---|---|---|
| Know-how-Eintrag überarbeiten | 1.0.0 | 3 | Wissensbasis-Pflege |
| Informationen zu Superbikes | 1.0.0 | 7 | Produktinformation |

---

## BSI Prozess-Konfiguration – Struktur

### Minimaler Prozess (Start → Schritt → Ende)
```json
{
  "_type": "crm.ProcessTransfer",
  "_typeVersion": "crm-25.2.007",
  "processConfig": {
    "_type": "crm.ProcessConfig",
    "_typeVersion": "crm-23.2.001",
    "id": "<UUID>",
    "gid": "<UUID>",
    "name": "Prozessname",
    "automationModeUid": "1;112192;106064;j219936;j219935",
    "processStepGroups": [],
    "processSteps": [
      {
        "_type": "crm.ProcessStepConfig",
        "_typeVersion": "crm-23.2.001",
        "id": "<UUID>",
        "gid": "<UUID>",
        "typeId": "201503",
        "backend": false,
        "hideBackButton": true,
        "outlets": [
          {
            "_type": "crm.ProcessStepOutletConfig",
            "_typeVersion": "crm-23.2.001",
            "id": "1;112215;206820;s<UUID>",
            "configurationName": "A",
            "defaultButton": true,
            "button": true,
            "presentation": "primary",
            "targetProcessStepId": "<UUID-des-nächsten-Steps>",
            "sortcode": 10
          }
        ],
        "bindings": [],
        "responsibility": { "_type": "crm.AssignResponsibility", "_typeVersion": "crm-25.1.001" },
        "_contributions": [
          { "_type": "crm.ProcessAutomationLambdaBindingContribution", "_typeVersion": "crm-25.2.011", "lambdaBindingDo": null }
        ]
      }
    ]
  }
}
```

### Wichtige Felder in `ProcessStepConfig`

| Feld | Pflicht | Beschreibung |
|---|---|---|
| `id` | ja | Eindeutige UUID des Steps innerhalb des Prozesses |
| `gid` | ja | Globale UUID (für Cross-Prozess-Referenzen) |
| `typeId` | ja | Bestimmt das Formular/Verhalten des Steps — siehe Registry |
| `backend` | ja | `true` = serverseitiger Step ohne UI |
| `hideBackButton` | nein | Zurück-Button im UI ausblenden |
| `outlets` | nein | Ausgänge zu Folge-Steps |
| `bindings` | nein | Datenbindungen für vorausgefüllte Felder |
| `groupId` | nein | Zuordnung zu einer `ProcessStepGroup` (Swim-Lane) |
| `responsibility` | nein | Zuständigkeit (Team, Rolle, Berater) |

### `ProcessStepGroups` (Swim-Lanes)
```json
"processStepGroups": [
  {
    "_type": "crm.ProcessStepGroupConfig",
    "_typeVersion": "crm-23.2.001",
    "id": "<UUID>",
    "name": "Vertrieb",
    "color": "color1"
  }
]
```
Verfügbare Farben: `color1` bis (mindestens) `color3`.

### Lambda-aufrufen-Step (typeId 209754)
Für jeden Step mit `typeId: 209754` muss eine Lambda-Binding-Datei im Ordner `lambda-bindings/` mitgeliefert werden:
- Dateiname: `<Prozessname>_-_<Schrittname>-crminvokeLambdaProcessStep<stepId>.json`
- `_type`: `bsiscout.LambdaBinding`
- Definiert die Eingabe-Parameter, die aus dem CRM-Datenmodell an das EIP-Interface übergeben werden.

### Korrespondenz-Step (typeId 168901)
Ähnlich wie Lambda-Step, aber mit Prefix `crmdocTemplateCorrespondenceProcessStep`:
- Dateiname: `<Prozessname>_-_<Schrittname>-crmdocTemplateCorrespondenceProcessStep<stepId>.json`
- Lambda-Inputs typischerweise: `subject`, `body`
