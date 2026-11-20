# BSI CX – Designregeln

> Prüfbare Regeln für die Erstellung von BSI-CX-Stories (productId `studio`). Abgeleitet aus Patterns, Beispielen und Help-Center-Doku.

## A. Story-Struktur
- **CXR1 – Teilnehmer-Start.** Jede Story beginnt mit mindestens einem **Teilnehmer-Step** (z. B. `EntryPointProducer`, `CrmCustomerProducer`, `crocus.CrmTriggerProducer`). Ohne Teilnehmer-Quelle läuft keine Story.
- **CXR2 – Flavor zwingend.** Jede Story hat eine gültige `flavorId`. Der Flavor muss im Export als `full` enthalten oder im Zielsystem vorhanden (`reference-only`) sein.
- **CXR3 – Erreichbarkeit & Abschluss.** Alle Steps sind vom Start aus über Outlets erreichbar; jeder Pfad endet definiert (Output-/End-Step, Substory-Response oder bewusster Endpunkt). Keine verwaisten Steps.
- **CXR4 – Outlet-Verschaltung.** Aktive Outlets sind über `targetStepGid` mit Folge-Steps verbunden. Keine aktiven, unverbundenen Outlets ohne Zweck.

## B. Logik & Robustheit
- **CXR5 – Verzweigung vollständig.** Bei `BranchBy…`-Steps sind alle relevanten Ausgänge behandelt (inkl. „sonst"/Negativfall). Kein Teilnehmer bleibt unbeabsichtigt stecken.
- **CXR6 – Fork/Join paarweise.** Jeder `ForkFlow` (Trennung) hat eine passende `JoinFlow`-Strategie bzw. definierte Enden je Zweig.
- **CXR7 – Integrationen fehlertolerant.** Push-/Integrations-Steps zu externen Diensten (`crocus.PushInsign`, `ConfiguredInvokeLambda`, `HttpServiceProviderProducer`) haben einen behandelten Fehler-/Timeout-Pfad (Verzweigung auf Ergebnis, Retry oder Eskalation) — analog R5 des process-expert.
- **CXR8 – Wartepunkte mit Zeitlogik.** `DelayByInterval`/`DelayUntilFixDate` und reaktionsabhängige Outlets (gelesen/ungelesen) mit sinnvollem `temporalConfig`; keine unbegrenzten Wartezustände.

## C. Content & Personalisierung
- **CXR9 – Push-Step braucht Content.** Jeder Push-Step referenziert vorhandenen Content passenden Typs; designfähige Content-Typen (`email`, `landing-page`, `gespraechsleitfaden`, `preview`) referenzieren ein Design.
- **CXR10 – Platzhalter belegt.** Alle im Content verwendeten Platzhalter werden in der Story mit Daten versorgt (Story-/Step-Attribute oder CRM-Felder).
- **CXR11 – Mehrsprachigkeit konsistent.** Benötigte Sprachversionen (`content-resource-<lang>.html`) sind vorhanden; Standardsprache gesetzt.
- **CXR12 – Strukturänderung = neue Version.** Strukturelle Content-Änderungen (neue Platzhalter/Links/Formulare) erfordern eine neue Content-Version.

## D. Messung & Datenschutz
- **CXR13 – KPIs definiert.** Erfolgsrelevante Outlets tragen Indikatoren (`indicatorIds`) bzw. `SetIndicators`; KPIs sind über den Flavor verfügbar.
- **CXR14 – Datenschutz/Retention.** `dataRetentionPeriod`, `crmAnonymization` und Opt-in-Prüfungen (`BranchByCrmCustomerOptIn`, Werbesperre) bewusst setzen, wo personenbezogene Kommunikation erfolgt.

## E. Export & Validität (mit export-expert)
- **CXR15 – productId studio.** `export-definition.json` und `index.json` mit `productId`/`productIdentifier: "studio"`, `productVersion`, `valueMigrationIds` (aus Beispiel übernehmen).
- **CXR16 – Index-Konsistenz.** Jede referenzierte ID hat einen Index-Eintrag: `full` (mitgelieferte Artefakte: Story, Content, Design, Flavor, Indikator, Medien, konfigurierte Steps) oder `reference-only` (Standard-Step-Typen, Outlet-Funktionstypen, CRM-Codes; `optionalType: "preserve"`).
- **CXR17 – Ressourcen vollständig.** Content-/Design-/Medien-Ordner enthalten ihre Ressourcendateien (`*.html`, Binärdateien); `resourcePath` zeigt korrekt darauf.
- **CXR18 – Multi-Paket-Reihenfolge.** Bei CX+CRM-Paketen Stages in Importreihenfolge (CRM vor studio, da studio CRM-Codes referenziert) und `foreignIdMappings` pflegen.

## F. Benennung & Wartbarkeit
- **CXR19 – Sprechende Namen.** Stories, Steps (eigene `name`/Bezeichnung) und Gruppen klar und fehlerfrei benennen; Mehrfachverwendung gleicher Step-Typen über Bezeichnung unterscheidbar machen.
- **CXR20 – Wiederverwendung via Substory/Muster.** Wiederkehrende Teil-Flows als Substory (`SubstoryEntry`/`SubstoryResponse`) oder Story als Muster (`template=true`) kapseln.

### Definition of Done (Kurzcheck)
1. Teilnehmer-Start + gültige flavorId (CXR1/CXR2).
2. Alle Steps erreichbar, Pfade enden definiert (CXR3/CXR4).
3. Verzweigungen vollständig, Integrationen mit Fehlerpfad (CXR5/CXR7).
4. Push-Steps mit Content/Design, Platzhalter belegt (CXR9/CXR10).
5. Index konsistent, productId studio, Ressourcen vollständig (CXR15–CXR17).
