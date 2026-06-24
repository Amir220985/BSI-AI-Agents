# BSI Process Review Checklist

> Zur fachlichen und technischen Prüfung von BSI-Prozesskonzepten, -Exporten, RFP-Antworten oder Angeboten.
> Jede Position verweist auf die zugrunde liegende Design-Rule (R…) bzw. das Anti-Pattern (AP…).
> Bewertung je Block: **stark / solide / kritisch / unklar** (mit Kurzbegründung).

## 1. Fachliche Klarheit
- [ ] Zweck des Prozesses in 1–2 Sätzen eindeutig beschrieben.
- [ ] Genau ein fachlicher Start; mindestens ein expliziter Abschluss-Step (`10049`). *(R1)*
- [ ] Alle Endzustände definiert; keine offenen Outlets/Sackgassen.
- [ ] Entscheidungspunkte fachlich nachvollziehbar; Outlet-Labels sprechend (nicht nur A/B/C). *(R6, AP9)*
- [ ] Rollen/Teams und Verantwortlichkeiten je Step klar. *(R10)*

**Bewertung Fachliche Klarheit:** ‹stark/solide/kritisch/unklar› — ‹Begründung›

## 2. Technische Robustheit
- [ ] Jeder Schnittstellen-/Lambda-Step (`209754`/`216266`) hat „Lambda erfolgreich?" (`209153`) mit **behandeltem** Fehlerzweig. *(R5, AP5)*
- [ ] Validierung (Pflichtfeld/Format) erfolgt **vor** Backend-Push. *(R13)*
- [ ] Bindings nutzen saubere `DataModelRelationSelection`/`-AttributeSelection` mit korrekter `containerEntityId`/`joins`. *(R14)*
- [ ] „Vorher-Stand" gespeichert, wo Rollback/4-Augen nötig. *(R15)*
- [ ] Wartepunkte (`150292`) auf Subprozesse mit SLA/Timeout. *(R18)*
- [ ] Eskalation/Überfälligkeit konfiguriert, wo zeitkritisch. *(R19)*

**Bewertung Technische Robustheit:** ‹…›

## 3. Rollen, Berechtigungen, Compliance
- [ ] Zuständigkeit (`responsibleTeamUid`) je bearbeitendem Step gesetzt. *(R10)*
- [ ] Vieraugenprinzip: Bearbeiter ≠ Freigeber, `enforceResponsibility` am Freigabe-Step. *(R11, AP6)*
- [ ] Rollen-/Prozesslogik getrennt; keine Personen-Hardcodierung. *(R12)*
- [ ] Berechtigungsstufe passend (Öffentlich/Geschützt/Vertraulich/Geheim).
- [ ] Keine personenbezogenen Daten/Secrets in Konfiguration/Export.

**Bewertung Rollen/Berechtigungen:** ‹…›

## 4. Wartbarkeit & Struktur
- [ ] Prozesse > 8 Steps in sinnvolle Gruppen gegliedert. *(R2, AP7)*
- [ ] Prozesse > ~40 Steps auf Auslagerung in Subprozesse geprüft. *(R3, AP2)*
- [ ] Keine Tippfehler / inkonsistente Namen; mehrsprachig gepflegt. *(R8, AP1)*
- [ ] Keine Dubletten (Codes/Prozessgruppen). *(R9, AP8)*
- [ ] Inbound/Self-Service teilen fachlichen Kern statt Doppelpflege. *(R17, AP4)*
- [ ] Kanal/Sparte über Vorlagen-/Attributselektion statt parallele Pfade. *(R16, AP3)*

**Bewertung Wartbarkeit:** ‹…›

## 5. Wiederverwendbarkeit
- [ ] Prozess folgt erkennbaren Patterns (P1–P12) oder begründet Abweichung.
- [ ] Wiederkehrende Blöcke als eigenständige/Subprozesse modelliert.
- [ ] Logik generisch genug für andere Entitäten/Sparten.

**Bewertung Wiederverwendbarkeit:** ‹…›

## 6. Dokumentation
- [ ] Fachliche Kurzbeschreibung vorhanden.
- [ ] `notes` an Entscheidungs- und Schnittstellen-Steps gepflegt. *(R20, AP9)*
- [ ] Offene Fragen/Annahmen explizit markiert.

**Bewertung Dokumentation:** ‹…›

---

## Gesamturteil
| Dimension | Bewertung | Wichtigste Findings |
|---|---|---|
| Fachliche Klarheit | | |
| Technische Robustheit | | |
| Rollen/Berechtigungen | | |
| Wartbarkeit | | |
| Wiederverwendbarkeit | | |
| Dokumentation | | |

**Empfehlung:** ‹freigeben / mit Auflagen / überarbeiten› — ‹Top-3-Maßnahmen›
