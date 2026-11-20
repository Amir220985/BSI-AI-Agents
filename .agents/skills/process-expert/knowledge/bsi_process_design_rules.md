# BSI Process Design Rules

> Konkrete, prüfbare Regeln für zukünftige BSI-CustomerSuite-Prozessmodellierung.
> Abgeleitet aus Patterns (`process_patterns.md`) und Anti-Patterns (`process_anti_patterns.md`).
> Jede Regel ist als Review-Kriterium formuliert (erfüllbar/prüfbar).

## A. Struktur & Lebenszyklus

- **R1 – Klarer Start und Endzustand.** Jeder Prozess hat genau einen fachlichen Einstieg und mindestens einen expliziten Abschluss-Step (`typeId 10049`, „Geschäftsvorfall abschließen"). Keine offenen Outlets ohne Ziel.
- **R2 – Gruppen ab Größe.** Prozesse mit > 8 Steps werden in `processStepGroups` (Swimlanes) gegliedert; Gruppennamen beschreiben fachliche Phasen (vgl. „Inbound – Steuerung", „Änderungen zu IBM i pushen"). *(gegen AP7)*
- **R3 – Monolithen vermeiden.** Prozesse > ~40 Steps werden geprüft, ob wiederkehrende Blöcke als eigenständige Prozesse/Subprozesse (Pattern P5: starten `117298` / abwarten `150292`) ausgelagert werden können. *(gegen AP2)*
- **R4 – Wiederaufnahme bewusst setzen.** Wenn ein abgeschlossener Geschäftsvorfall wieder geöffnet werden darf, `reopenCaseStepUid`/`reopenCaseTypeUid` setzen (wie bei Kunde-Daten-ändern, KYC). Sonst bewusst leer lassen und im Konzept begründen.

## B. Verzweigung & Fehlerbehandlung

- **R5 – Schnittstellen sind fehlertolerant.** Jedem Lambda-/Schnittstellen-Step (`209754`, Hintergrund `216266`) folgt ein Kriterien-Step „Lambda erfolgreich?" (`209153`) mit **behandeltem** „nein"-Zweig (Korrektur, Retry oder Eskalation) — niemals nur eine Info-Sackgasse. *(Pattern P2, gegen AP5)*
- **R6 – Entscheidungen sind nachvollziehbar.** Outlets von Kriterien-Steps tragen sprechende Labels statt nur „A/B/C"; die Entscheidungsbedingung wird in `notes` fachlich dokumentiert. *(gegen AP9)*
- **R7 – Idempotenz/Reihenfolge bei Backend-Push.** Vor dem Push wird der „Vorher-Stand" gespeichert (`133850`); der Push-Aufruf muss bei Wiederholung sicher sein (Konzeptannahme dokumentieren).

## C. Benennung & Konsistenz

- **R8 – Namenskonvention.** Step-/Gruppen-/Statusnamen sind fachlich, eindeutig, fehlerfrei und mehrsprachig gepflegt (de/en/it/fr — wie im Datenmodell vorgesehen). Kein „sStart", „Vetrag", doppelte Klammern. Namens-Lint vor jedem Export. *(gegen AP1)*
- **R9 – Keine Dubletten in Stammdaten.** Prozessgruppen/Codes sind eindeutig; vor Anlage Dublettenprüfung (vgl. doppelte „Vertrieb"-Gruppe). *(gegen AP8)*

## D. Rollen & Berechtigungen

- **R10 – Zuständigkeit explizit.** Jeder bearbeitende Step hat eine definierte `responsibility` (`responsibleTeamUid`/`responsibleTeamRoleUid`). Automatik-Steps sind als solche erkennbar (kein Bearbeiter).
- **R11 – Vieraugenprinzip erzwingen.** Bei Freigabeprozessen sind Bearbeiter und Freigeber organisatorisch getrennt; der Freigabe-Step nutzt `enforceResponsibility` und ein vom Bearbeiter verschiedenes Team/Rolle. Funktionstrennung wird dokumentiert. *(Pattern P3, gegen AP6)*
- **R12 – Trennung Rollen- vs. Prozesslogik.** Fachliche Steuerung läuft über Teams/Berechtigungen, nicht über hartkodierte Verzweigungen auf Personen.

## E. Daten & Validierung

- **R13 – Validierung vor Schnittstelle.** Pflichtfeld- und Formatprüfungen (z. B. „E-Mail/Telefon – Falsches Format") erfolgen **vor** dem Backend-Push, nicht danach.
- **R14 – Datenanbindung sauber.** Bindings nutzen definierte `DataModelRelationSelection`/`-AttributeSelection` mit korrekter `containerEntityId` und `joins`; keine losen/uneindeutigen Selektionen.
- **R15 – Snapshot für Review/Rollback.** Vor genehmigungs-/backendrelevanten Änderungen „Vorher-Stand speichern" (`133850`) für 4-Augen-Vergleich und Fehler-Rollback.

## F. Kommunikation & Korrespondenz

- **R16 – Vorlagen statt Pfad-Duplikate.** Kanal-/Sparten-Unterschiede über Vorlagen-/Attributselektion abbilden, nicht über parallele Step-Ketten. *(gegen AP3)*
- **R17 – Gemeinsamer Kern, getrennte Steuerung.** Inbound/Self-Service teilen den fachlichen Kern; nur Einstieg/Berechtigung unterscheidet sich. *(gegen AP4)*

## G. SLA, Eskalation, Orchestrierung

- **R18 – Wartepunkte mit Frist.** Jeder „abwarten"-Step (`150292`) auf einen Subprozess hat SLA/Eskalation oder Timeout, um Deadlocks zu vermeiden. *(Pattern P5)*
- **R19 – Eskalation/Überfälligkeit konfigurieren.** Bei zeitkritischen Prozessen `escalationSlaTimeConfig`/`overdueSlaTimeConfig` und ggf. `defaultFollowUpTimeInSeconds` setzen.

## H. Dokumentation

- **R20 – Fachliche Begründung.** Entscheidungs- und Schnittstellen-Steps haben gepflegte `notes`; der Prozess hat eine fachliche Kurzbeschreibung. *(gegen AP9)*

---

### Schnell-Checkliste „Definition of Done" für einen neuen Prozess
1. Start + Abschluss-Step vorhanden (R1).
2. Jeder Lambda-Step hat behandelten Fehlerpfad (R5).
3. Gruppen vorhanden, sprechende Namen, kein Tippfehler (R2, R8).
4. Zuständigkeiten gesetzt, Vieraugen erzwungen wo nötig (R10, R11).
5. Validierung vor Push (R13).
6. SLA/Wartepunkte abgesichert (R18, R19).
7. `notes` an Entscheidungen/Schnittstellen (R20).
