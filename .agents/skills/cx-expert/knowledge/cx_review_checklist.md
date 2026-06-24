# BSI CX – Review-Checkliste

> Prüfung von Story-Konzepten/-Exporten vor Auslieferung/Import. Verweise: Designregeln `CXR…`.

## 1. Story-Struktur
- [ ] Teilnehmer-Step am Start vorhanden (CXR1).
- [ ] Gültige `flavorId`; Flavor mitgeliefert oder im Ziel vorhanden (CXR2).
- [ ] Alle Steps vom Start erreichbar, keine verwaisten Steps (CXR3).
- [ ] Alle Pfade enden definiert (Output/End/Substory-Response).
- [ ] Aktive Outlets über `targetStepGid` verbunden (CXR4).

## 2. Logik & Robustheit
- [ ] `BranchBy…`-Verzweigungen vollständig (inkl. Negativfall) (CXR5).
- [ ] `ForkFlow`/`JoinFlow` paarweise/definiert (CXR6).
- [ ] Integrationen (`crocus.*`, `ConfiguredInvokeLambda`, HTTP) mit Fehler-/Timeout-Pfad (CXR7).
- [ ] Wartepunkte mit sinnvollem `temporalConfig`, keine Endlos-Wartezustände (CXR8).

## 3. Content & Personalisierung
- [ ] Jeder Push-Step referenziert Content passenden Typs (CXR9).
- [ ] Designfähige Content-Typen referenzieren ein Design (CXR9).
- [ ] Alle Platzhalter mit Daten versorgt (CXR10).
- [ ] Benötigte Sprachversionen vorhanden, Standardsprache gesetzt (CXR11).
- [ ] Strukturänderungen als neue Content-Version (CXR12).

## 4. Messung & Datenschutz
- [ ] Indikatoren an erfolgsrelevanten Outlets / `SetIndicators` (CXR13).
- [ ] Opt-in/Werbesperre geprüft, Retention/Anonymisierung gesetzt (CXR14).

## 5. Export-Validität (mit export-expert)
- [ ] `productId/productIdentifier: "studio"`, `productVersion`, `valueMigrationIds` gesetzt (CXR15).
- [ ] Index-Konsistenz: jede referenzierte ID hat Eintrag (`full` oder `reference-only` + `optionalType: preserve`) (CXR16).
- [ ] Standard-Step-Typen/Outlet-Funktionen/CRM-Codes als `reference-only` (CXR16).
- [ ] Content-/Design-/Medien-Ordner enthalten alle Ressourcendateien; `resourcePath` korrekt (CXR17).
- [ ] Bei CX+CRM: `multi-index.json`, Stages CRM→studio, `foreignIdMappings` (CXR18).
- [ ] `globalUniqueId` je Item vorhanden (UUID des Objekts; bei CRM-Refs CRM-Regeln des export-expert).

## 6. Benennung & Wartbarkeit
- [ ] Sprechende, fehlerfreie Namen für Story/Steps/Gruppen (CXR19).
- [ ] Wiederkehrende Teil-Flows als Substory/Muster gekapselt (CXR20).

## 7. Import-Test (empfohlen)
- [ ] Test-ZIP in CX-Instanz importiert; Validierung der Story (BSI „Validierung") fehlerfrei.
- [ ] Bei Importfehler: export-expert-Checkliste „Fehlerhafte Index-Datei" durchgehen.

---
## Gesamturteil
| Dimension | Bewertung (stark/solide/kritisch/unklar) | Findings |
|---|---|---|
| Struktur | | |
| Logik/Robustheit | | |
| Content | | |
| Messung/Datenschutz | | |
| Export-Validität | | |

**Empfehlung:** ‹freigeben / mit Auflagen / überarbeiten› — ‹Top-Maßnahmen›
