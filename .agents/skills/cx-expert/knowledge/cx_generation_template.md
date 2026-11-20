# BSI CX – Story-Generierungs-Template

> Fachliche + technische Spezifikation einer neuen Customer Story. Vor Nutzung: Patterns (`cx_patterns.md`), Designregeln (`cx_design_rules.md`), Step-Registry (`registry/cx_step_registry.json`) heranziehen. `‹…›` ausfüllen; Unklares als **Annahme**/**offene Frage** markieren.

## 1. Steckbrief
| Feld | Wert |
|---|---|
| Story-Name | ‹…› |
| Flavor | ‹Journey / Mailing / … (flavorId)› |
| Zweck (1–2 Sätze) | ‹…› |
| Auslöser / Teilnehmerquelle | ‹CRM-Trigger / Einstieg / CSV / Webshop …› |
| Kanäle (Touchpoints) | ‹E-Mail / Landingpage / SMS / Dokument / QR …› |
| executionType | ‹auto / manual› |
| Komplexität (erwartet) | einfach / mittel / komplex |
| Verwandte Patterns | ‹CXP1, …› |

## 2. Ziel & KPIs
- **Ziel:** ‹Soll-Ergebnis nach Durchlauf›
- **KPIs/Indikatoren:** ‹Versendet, Gelesen, Conversion, NPS …› (über Flavor verfügbar)
- **Akzeptanzkriterien:** ‹messbar›

## 3. Teilnehmer
| | |
|---|---|
| Teilnehmer-Step | ‹EntryPointProducer / CrmCustomerProducer / crocus.CrmTriggerProducer› |
| Selektion/Quelle | ‹CRM-Selektion, Trigger-Qualifier, CSV …› |
| Teilnehmer-Strategie | ‹Verhalten bei Erzeugung› |

## 4. Story-Attribute
| Attribut | Typ | Quelle | Verwendung |
|---|---|---|---|
| ‹…› | ‹…› | ‹CRM-Feld / Step-Attribut› | ‹Platzhalter / Verzweigung› |

## 5. Step-Flow
> Pro Step: Bezeichnung · customConfig._type (Registry) · Kategorie · Outlets (Name → Ziel-Step) · Content/Integration.

| # | Bezeichnung | customConfig._type | Kategorie | Outlets (Name → Ziel) | Content / Hinweis |
|---|---|---|---|---|---|
| 1 | ‹Einstieg› | `studio.EntryPointProducerStepletConfig` | Teilnehmer | Standard → 2 | |
| 2 | ‹Kriterien?› | `studio.BranchByConstraintStepletConfig` | Logik | ja → 3 / nein → … | Bedingung: ‹…› |
| 3 | ‹E-Mail senden› | `studio.SendEmailStepletConfig` | Push | gelesen → … / ungelesen → … | Content: ‹E-Mail X› |
| … | | | | | |
| n | ‹Abschluss/Daten› | ‹ModifyCrmCustomer / SubstoryResponse› | Daten/Prozedur | – | |

## 6. Content & Design
| Content | Typ | Design | Platzhalter | Sprachen |
|---|---|---|---|---|
| ‹Name› | ‹email / landing-page …› | ‹Design X / –› | ‹{vorname}, …› | ‹de-CH, …› |

## 7. Daten-Rückschreiben (CRM)
| Step | Aktion | Zielobjekt/Feld |
|---|---|---|
| ‹ModifyCrmCustomer› | ‹anlegen/ändern› | ‹CrmCustomer.…› |
| ‹CrmCommunication / CrmCase / Score / OptIn› | ‹…› | ‹…› |

## 8. Integrationen & Fehlerbehandlung
| Integration | Step | Ergebnisprüfung | Fehler-/Timeout-Pfad |
|---|---|---|---|
| ‹inSign / Lambda / HTTP› | ‹crocus.PushInsign / ConfiguredInvokeLambda› | ‹Outlet erfolgreich?› | ‹Retry/Eskalation/Info (CXR7)› |

## 9. Logik & Timing
- Verzweigungen vollständig (alle Zweige behandelt, CXR5).
- Fork/Join paarweise (CXR6).
- Wartepunkte mit `temporalConfig` (CXR8).

## 10. Datenschutz & Messung
- Opt-in/Werbesperre geprüft (`BranchByCrmCustomerOptIn`).
- `dataRetentionPeriod` / `crmAnonymization` gesetzt (CXR14).
- Indikatoren an relevanten Outlets (CXR13).

## 11. Export
- `productId/productIdentifier: "studio"`, `productVersion`, `valueMigrationIds` aus Beispiel.
- Mitgelieferte Artefakte (`full`): Story, Content(+Ressourcen), Design, Flavor, Indikatoren, Medien, konfigurierte Steps.
- `reference-only`: Standard-Step-Typen, Outlet-Funktionstypen, CRM-Codes.
- Bei CX+CRM: Multi-Paket (`multi-index.json`, Stages CRM→studio).
- Ablage in `exports/` analog Exportstruktur; ZIP gemäß **export-expert** zusammensetzen.

## 12. Offene Fragen / Annahmen
- ‹…›

---
**Hinweis:** Dieses Template liefert die Spezifikation. Die konkreten JSON-Objekte (`studio.StoryConfig` + `studio.StepConfig` + Content/Design) immer aus den `examples/` ableiten — keine Strukturen erfinden. Vor Auslieferung `cx_review_checklist.md` durchlaufen.
