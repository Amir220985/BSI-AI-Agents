# BSI CX (studio) – Step-Typ-Katalog

> Abgeleitet aus 20 Beispiel-Stories / 489 Steps (`examples/bsi-cx-2026-06-24_*.zip`).
> **Schlüssel = `StepConfig.customConfig._type`** (hier ohne Prefix `studio.`/Suffix `StepletConfig`). Maschinenlesbar: `registry/cx_step_registry.json`.
> Anzeigenamen stammen aus den `studio.step.type`-Index-Items (de-CH). `n` = Vorkommen über alle Beispiel-Stories.
> `crocus.*` = Low-Code/konfigurierte oder kundenspezifische Steps. Bedeutungen tw. *(abgeleitet)*.

## Die fünf Step-Arten (BSI-CX-Doku)
1. **Teilnehmer-Steps** – erzeugen/bringen Teilnehmer in die Story (stehen am Anfang).
2. **Logik-Steps** – verteilen, selektieren, filtern, verzögern, warten, verzweigen.
3. **Daten-Steps** – schreiben Daten ins führende System zurück (v. a. BSI CRM).
4. **Push-Steps** – erzeugen Output/Touchpoints (E-Mail, SMS, Landingpage, Dokument, QR …).
5. **Prozedur-Steps** – step-art-übergreifende Aufgaben (Substory, Lambda, Übergabe).

Zusatzgruppen in diesem Katalog: **Attribute** (Story-Attribute setzen/löschen), **Web/Online** (HTTP, Routing, JavaScript), **Hilfs/Prototyping** (Platzhalter).

---

### Teilnehmer
*Erzeugen/bringen Teilnehmer in die Story (Story-Start).*

| customConfig._type | Anzeigename | n | Wichtige customConfig-Felder |
|---|---|---:|---|
| `EntryPointProducer` | Einstieg | 6 | — |
| `crocus.CrmTriggerProducer` | CRM Trigger | 2 | mappings, triggerQualifier |
| `CrmCustomerProducer` | Kunden suchen | 2 | selection |
| `CrmParticipatableStoryProducer` | Mitmachen | 1 | allowParticipation, availableFor, createParticipantsImmediately, description, endpoint, from |
| `RandomParticipant` | Ziehung | 1 | numberOfParticipants |
| `ForkParticipantProducer` | Teilnehmer fort­führen | 1 | checkAllSteps, participantStatusRestriction, stepOutletMappings, strategy |

### Logik
*Verteilen, filtern, verzögern, verzweigen Teilnehmer.*

| customConfig._type | Anzeigename | n | Wichtige customConfig-Felder |
|---|---|---:|---|
| `BranchByConstraint` | Kriterien | 25 | selections |
| `BranchByFilter` | Filter | 12 | selection |
| `ExecuteBrain` | Brain ausführen | 8 | brainProblemType, featureSelectionMapping, targetOutletMapping, targetPropertyMapping, versionGroupId |
| `ForkFlow` | Trennung | 6 | outlets |
| `DelayByInterval` | Ver­zöger­ung | 5 | delayedConfig |
| `RemoveParticipant` | Teilnehmer löschen | 4 | temporalConfig |
| `JoinFlow` | Zusammen­führung | 4 | — |
| `GenerateValue` | Wert generieren | 3 | propertyId, type, typeConfig |
| `BranchBySingleExecution` | Erstes Mal | 3 | — |
| `BranchByCrmCustomerOptIn` | Werbe­sperre | 3 | channel, checkMode, optInStatusSelection |
| `BranchByExecutionCount` | Erstes Mal | 3 | — |
| `ServiceTime` | Service­zeiten | 2 | modeDelay, serviceDays |
| `DelayUntilFixDate` | Stichtag | 1 | temporalConfig |

### Daten
*Schreiben Daten zurück (v. a. BSI CRM): Kunde, Kommunikation, Score, GV.*

| customConfig._type | Anzeigename | n | Wichtige customConfig-Felder |
|---|---|---:|---|
| `FindBestMatchingCrmCustomer` | Kunde finden | 5 | attributeConstraints, emailAddressProperty, phoneAddressProperty, physicalAddressProperty, setCrmCustomerAttribute |
| `ManageCrmCustomerIdentity` | Benutzer­verwaltung | 4 | authenticatorId, manageIdentityConfig, operationType, userId |
| `ModifyCrmCustomer` | Kunde erfassen | 4 | customer, setCrmCustomerAttribute, addresses |
| `SetIndicators` | Indikatoren setzen | 2 | indicators |
| `CrmCommunication` | Kommuni­kation | 2 | communication, phoneScriptEnabled, documents |
| `CrmFeedback` | Feedback | 1 | executeImmediately, message, outlets, responsible, selectionRestriction |
| `ModifyCrmCustomerScore` | Score setzen | 1 | score, scoreValue |
| `CrmCustomerOptIn` | Opt-in/out | 1 | address, addressPropertyId, byCustomer, optInStatus, optInType |
| `CrmCase` | Geschäfts­vorfall erstellen | 1 | — |
| `crocus.UpdateCase` | Geschäfts­vorfall steuern | 1 | action, caseNo |

### Push
*Erzeugen Output/Touchpoints (E-Mail, SMS, Landingpage, Dokument, QR …).*

| customConfig._type | Anzeigename | n | Wichtige customConfig-Felder |
|---|---|---:|---|
| `LandingPage` | Landing­page, Vorschau | 55 | contentId, contentRevision, cookieValidation, createCommunication, htmlFormNotSentOutletTemporalConfig, noReactionOutletTemporalConfig |
| `SendEmail` | E-Mail | 24 | bucketTesting, contentId, contentRevision, createCommunication, listUnsubscribeHeader, noReactionOutletTemporalConfig |
| `PreferenceCenter` | Preference Center | 11 | modifyConfig, operationType |
| `CreateDocument` | Dokument, Brief | 6 | contentId, contentRevision, createCommunication, documentOutputFormat, filename, storeOutput |
| `crocus.PushInsign` | inSign | 4 | allowInSandbox, callbackForParticipant, caseDisplayName, communicationViaInsign, expiredOutletTemporalConfig, inputFile |
| `Website` | Portal | 2 | authenticationConfig, baseUrlSettingId, cookieName, endpoint, locale, navigationItems |
| `SendSms` | SMS | 2 | contentId, contentRevision, createCommunication, noReactionOutletTemporalConfig, recipient, sender |
| `CreateAndTrackQrCode` | QR-Code | 1 | dimensionInPixels, errorCorrectionLevel, notScannedOutletTemporalConfig, qrCodeScanMode |
| `crocus.PushAeschbachChocolatier` | Aeschbach Choco Greets | 1 | message, recipientCity, recipientCountry, recipientFirstName, recipientLastName, recipientLocale |
| `CreateOneTimePasswordQrCode` | QR-Code Einmal­passwort | 1 | accountName, dimensionInPixels, errorCorrectionLevel, issuer |
| `TimeslotCalendar` | Online-Termin­ver­ein­ba­rung | 1 | desiredUser, rangeFromDate, rangeToDate, slotType |
| `CreateICal` | iCal | 1 | allDay, contentId, contentRevision, endDate, eventDuration, location |

### Prozedur
*Aufgaben-übergreifend: Substory, Lambda, Übergabe an andere Story.*

| customConfig._type | Anzeigename | n | Wichtige customConfig-Felder |
|---|---|---:|---|
| `ConfiguredInvokeLambda` | Analyse starten, Antwort speichern, Analyse | 26 | inputConfigs, outletConfigs, stepId, propertyConfigs, batchConfig |
| `SubstoryResponse` | Substory-Ende | 5 | configuredStepId, outletIds |
| `HandOverToOtherStory` | An Story übergeben | 3 | propertyMappings, targetDraftStoryId, targetStepGid, targetStoryGid |
| `crocus.FindCustomerAddress` | Adresse finden | 1 | electronicAddress |
| `SubstoryEntry` | Substory-Start | 1 | configuredStepId, inputConfigs |
| `ValidateOneTimePassword` | Einmal­passwort validieren | 1 | encryptedSecret, oneTimePassword |

### Attribute
*Setzen/entfernen Story-Attribute (oft via Outlet-Funktion ersetzbar).*

| customConfig._type | Anzeigename | n | Wichtige customConfig-Felder |
|---|---|---:|---|
| `SetStoryProperties` | Attribute setzen | 91 | properties, useConstraint |
| `SetStoryProperty` | Attribut setzen | 15 | property |
| `RemoveProperties` | Attribute löschen | 6 | propertyIds |

### Web/Online
*Online-Touchpoints, Routing, HTTP, JavaScript.*

| customConfig._type | Anzeigename | n | Wichtige customConfig-Felder |
|---|---|---:|---|
| `WebsiteDispatcher` | Nächste Page | 37 | websiteId, websiteNavigationId, websiteRevision |
| `crocus.ExecuteJavaScript` | JavaScript | 34 | outputs, script, inputs |
| `HttpServiceProviderProducer` | Webseiten­aufruf, REST-Eingang, QR-Scan | 19 | dateFormat, dateTimeFormat, decimalSeparator, defaultResponse, endpoint, httpMethod |
| `UrlRedirect` | Weiterleiten | 6 | defaultLocale, urls |
| `HttpResponseBuilder` | HTTP-Antwort | 4 | content, contentType, statusCode |
| `Cookie` | — | 1 | cookieComment, cookieDomain, cookieName, cookiePath, cookieValue, httpOnly |
| `crocus.StringBuilder` | — | 1 | message, storyProperty |

### Hilfs/Prototyping
*Platzhalter-Steps für Prototyping.*

| customConfig._type | Anzeigename | n | Wichtige customConfig-Felder |
|---|---|---:|---|
| `Placeholder` | Platzhalter | 12 | customStepTypeConfig, outletRatios |
| `PlaceholderProducer` | Platzhalter | 3 | numberOfFlows, customStepTypeConfig, outletRatios |

---

## Hinweise zur Verwendung
- **Story-Start** immer mit einem Teilnehmer-Step (häufig `EntryPointProducer` „Einstieg" oder `CrmCustomerProducer`/`crocus.CrmTriggerProducer`).
- **Verzweigung** über `BranchByConstraint` (Kriterien, `selections`), `BranchByFilter`, `BranchByCrmCustomerOptIn` (Werbesperre) u. a. — Outlets je Zweig.
- **Parallelisierung**: `ForkFlow` (Trennung) … `JoinFlow` (Zusammenführung).
- **Output** über Push-Steps; der Inhalt kommt aus verknüpftem **Content** (E-Mail/Landingpage/SMS/Dokument …), siehe `cx_content_and_design.md`.
- **CRM-Rückschreiben** über Daten-Steps (`ModifyCrmCustomer`, `CrmCommunication`, `CrmCase`, `ModifyCrmCustomerScore`, `CrmCustomerOptIn`).
- **Integration/Custom**: `ConfiguredInvokeLambda` (Prozedur) und `crocus.*` (Low-Code/kundenspezifisch, z. B. `PushInsign`).
- **Attribute setzen** lässt sich oft direkt als Outlet-Funktion lösen (statt eigener `SetStoryProperty`-Step) — siehe Doku „Einstellungen auf Step-Ausgängen".

> Vollständigkeit: Der Katalog deckt die in den 17 Beispiel-Exporten **tatsächlich genutzten** Step-Typen ab (59 von vielen verfügbaren). Weitere Steps der Step-Bibliothek sind möglich; bei Bedarf aus neuen Beispiel-Exporten ergänzen.
