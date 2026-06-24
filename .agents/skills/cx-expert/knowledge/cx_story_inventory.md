# BSI CX – Story-Inventar (Beispiel-Exporte)

> 20 Customer Stories aus 17 Exporten (`examples/bsi-cx-2026-06-24_*.zip`). Komplexität = Step-Anzahl: einfach ≤10 · mittel 11–25 · komplex 26–60 · sehr komplex >60.

| Story | Status | Steps | Typen | Art | Domäne / Zweck (abgeleitet) |
|---|---|---:|---:|---|---|
| OVB Companion | draft | 179 | 18 | sehr komplex | Großer Companion-/Beratungs-Flow (Finanzvertrieb) |
| Campaign Genius: Silicon Sampling | live | 56 | 9 | komplex | Kampagne mit AI-Sampling |
| Self-Service 2024 | draft | 41 | 18 | komplex | Self-Service-Strecke (Online + CRM) |
| ENRA Antragsstrecke | draft | 24 | 11 | mittel | Antrags-/Onboarding-Strecke |
| inSign – Feststellung wirtschaftl. Berechtigung | draft | 19 | 11 | mittel | KYC/Compliance mit inSign (E-Signatur) |
| Newsletter Anmeldung | draft | 19 | 14 | mittel | Double-Opt-in Newsletter-Anmeldung |
| Schoko-Quiz | draft | 18 | 9 | mittel | Gamification/Quiz-Kampagne |
| NPS Umfrage mit AI | draft | 15 | 13 | mittel | NPS-Befragung mit AI-Auswertung |
| Preference Center Plus | draft | 14 | 6 | mittel (Substory) | Erweitertes Preference Center |
| inSign Demostory | draft | 13 | 8 | mittel | Demo E-Signatur-Strecke |
| inSign Antragsstrecke | live | 11 | 7 | mittel | Antragsstrecke mit E-Signatur |
| Nach Schadenfall | live | 11 | 5 | mittel | After-Sales/Schaden-Nachgang |
| Beispiel Pass | draft | 11 | 9 | mittel | Pass-/Wallet-Beispiel |
| Preference Center (×3) | draft | 9 | 5 | einfach | Präferenzverwaltung (mehrfach) |
| KPI Simulieren für Flavor Mailing | draft | 9 | 4 | einfach | KPI-Simulation/Test |
| SEPA-Mandatsdaten einholen | draft | 8 | 6 | einfach | SEPA-Mandat-Erfassung |
| Newsletter Welcome Mailing (×2) | draft | 7 | 7 | einfach | Welcome-Strecke nach Anmeldung |

## Beobachtungen
- **Status**: überwiegend `draft`; 3 Stories `live` (inSign Antragsstrecke, Nach Schadenfall, Campaign Genius). Keine `sunset` in den Beispielen.
- **Substory**: „Preference Center Plus" ist als Substory modelliert (wiederverwendbarer Teil-Flow, via Prozedur-Steps `SubstoryEntry`/`SubstoryResponse` eingebunden).
- **Mehrfach vorhandene Stories** (Preference Center, Newsletter Welcome Mailing): unterschiedliche Exporte/Mandanten — als wiederverwendbare Muster geeignet.
- **Kanäle/Touchpoints** quer über die Stories: E-Mail, SMS, Landingpage, Dokument, QR-Code, iCal, Website/Portal, Preference Center.
- **AI/ML**: `ExecuteBrain` (Brain) und konfigurierte Lambda-Steps in „NPS Umfrage mit AI", „Campaign Genius", „Schoko-Quiz".
- **Integrationen**: `crocus.PushInsign` (E-Signatur), `crocus.PushAeschbachChocolatier` (kundenspezifisch) → über konfigurierte/Low-Code-Steps.

## Einstiegsempfehlung (Muster nach Komplexität)
- **Einfaches Mailing**: „Newsletter Welcome Mailing" (7 Steps) — Einstieg → E-Mail → Verzweigung gelesen/ungelesen.
- **Opt-in-Strecke**: „Newsletter Anmeldung" (19) — Landingpage + Double-Opt-in + Preference Center.
- **CRM-nah**: „Nach Schadenfall" (11, live) — Daten-Steps + Kommunikation.
- **Self-Service/komplex**: „Self-Service 2024" (41) — Online + CRM + Verzweigungen.
