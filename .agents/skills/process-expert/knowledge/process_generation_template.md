# BSI Process Generation Template

> Vorlage zur fachlichen **und** technischen Beschreibung eines neuen BSI-CustomerSuite-Prozesses.
> Vor Nutzung: passende Patterns aus `process_patterns.md` wählen, Design-Rules aus `bsi_process_design_rules.md` anwenden, Step-Typen aus `bsi_step_type_catalog.md` referenzieren.
> Felder mit `‹…›` ausfüllen. Unklares als **Annahme** oder **offene Frage** markieren.

---

## 1. Prozess-Steckbrief

| Feld | Wert |
|---|---|
| **Prozessname** | ‹fachlich, eindeutig, fehlerfrei – vgl. R8› |
| **Technischer Name / scriptIdentifier** | ‹z. B. `Process.‹Name›`› |
| **Version** | ‹x.y.z› |
| **Prozessgruppe** | ‹Service / Vertrieb / Marketing / … (codeType 45831)› |
| **Domäne / Use Case** | ‹…› |
| **Fachlicher Zweck (1–2 Sätze)** | ‹…› |
| **Komplexität (erwartet)** | einfach / mittel / komplex / sehr komplex |
| **Verwandte Patterns** | ‹P1, P2, …› |

## 2. Ziel & Akzeptanzkriterien

- **Ziel:** ‹Was ist nach erfolgreichem Durchlauf erreicht?›
- **Akzeptanzkriterien:**
  - [ ] ‹messbares Kriterium 1›
  - [ ] ‹…›

## 3. Auslöser & Voraussetzungen

| | |
|---|---|
| **Auslöser / Start** | ‹Inbound-Kommunikation / Self-Service / manuell / Ereignis / Subprozess-Start› |
| **Eingangsvoraussetzungen** | ‹Pflicht-Inputs, vorhandene Entität, Berechtigung› |
| **Prozess-Input** | ‹activeProcessInputs: Entität(en), z. B. CrmCase → CrmCustomer› |

## 4. Beteiligte Rollen / Teams

| Schritt/Phase | Verantwortliches Team/Rolle | enforceResponsibility | Bemerkung |
|---|---|---|---|
| ‹Bearbeitung› | ‹Team_…› | ja/nein | |
| ‹Freigabe (4-Augen)› | ‹Team_… ≠ Bearbeiter (R11)› | **ja** | |
| ‹Automatik› | – | – | kein Bearbeiter |

## 5. Beteiligte Objekte / Datenmodell

| Entität | Rolle im Prozess | relevante Attribute |
|---|---|---|
| CrmCase | Geschäftsvorfall | |
| ‹CrmCustomer / Contract / InsuredObject / PaymentMethod / …› | | |

## 6. Statusmodell / Phasen (Gruppen)

| Gruppe (Swimlane) | Fachliche Phase |
|---|---|
| ‹Steuerung› | |
| ‹Erfassung/Bearbeitung› | |
| ‹Prüfung/Freigabe› | |
| ‹Backend-Push› | |
| ‹Abschluss› | |

## 7. Prozessschritte (Flow)

> Pro Step: Name · Step-Typ (typeId aus Katalog) · Outlets (Label → Ziel) · Verantwortung · Bindings.

| # | Step-Name | typeId | Outlets (Label → Ziel) | Verantwortung | Bindings/Daten |
|---|---|---|---|---|---|
| 1 | ‹Start/Steuerung› | 138297 | A → 2 | | |
| 2 | ‹Verzweigung …?› | 209153 | ja → 3 / nein → … | | Kriterium: ‹…› |
| … | | | | | |
| n | ‹Geschäftsvorfall abschließen› | 10049 | – | | |

## 8. Validierungen & fachliche Regeln

- Pflichtfelder: ‹…›
- Format-/Prüfregeln: ‹z. B. E-Mail/Telefon-Format vor Push (R13)›
- Statusabhängigkeiten / Sichtbarkeiten: ‹…›
- Freigabelogik: ‹…›

## 9. Schnittstellen / Integration

| Aufruf | Lambda/Prototype | Richtung | Input (DataModel-Selection) | Output | Fehlerbehandlung |
|---|---|---|---|---|---|
| ‹Kunde aus IBM i laden› | ‹lambdaId/prototypeName› | read | ‹containerEntityId/joins› | | „Lambda erfolgreich?" → nein: ‹…› |
| ‹Daten zu IBM i pushen / CS-API› | | write | | | Retry/Eskalation (R5) |

## 10. Fehlerbehandlung & Sonderpfade

- Schnittstellenfehler: ‹Pattern P2 — manuelle Nachbearbeitung›
- Abbruch durch Bearbeiter: ‹Abbruch-Info-Step, Zustand›
- Rückgabe-/Korrekturschleife: ‹von Prüf-Step zurück zu Bearbeitung›
- Wiederaufnahme (Reopen): ‹reopenCaseStepUid setzen? ja/nein (R4)›

## 11. SLA, Eskalation, Wiedervorlage

| | |
|---|---|
| escalationSlaTimeConfig | ‹Frist / Warnung% / Team› |
| overdueSlaTimeConfig | ‹…› |
| defaultFollowUpTime | ‹Wiedervorlagefrist› |
| Wartepunkte (150292) mit Timeout | ‹R18› |

## 12. Korrespondenz / Vorlagen

- availableTemplateUids: ‹Liste›
- E-Mail-Account(s): ‹css-outbound@… / sparte-spezifisch›
- Kanal/Sparte über Vorlagenselektion statt Pfad-Duplikat (R16)

## 13. Berechtigungen & Sichtbarkeit

- Berechtigungsstufe(n): ‹Öffentlich/Geschützt/Vertraulich/Geheim›
- visibleAttributes je Step: ‹…›

## 14. Offene Fragen / Annahmen

- ‹…›

---

### Generierungs-Hinweis (für Agent)
Beim tatsächlichen Erzeugen eines importierbaren ZIP-Exports gelten die technischen Vorgaben aus
`bsi-ai-development/.agents/skills/process-expert/` (process_step_registry, Bindings, Outlets, stepConfiguration) und `export-expert/`. Dieses Template liefert die **fachliche Spezifikation**, aus der dann die konkrete `crm.ProcessTransfer`-Struktur (`processConfig` + `processDefinition` + `processStepDefinitions`) gebaut wird.
