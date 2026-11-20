# Session-Architektur — Komponenten & Tool-Zuordnung

Die sieben Komponenten sind **logische Verantwortlichkeiten**, keine eigenen Programme. Sie strukturieren, wie du das **Claude-in-Chrome-MCP** (`mcp__Claude_in_Chrome__*`) einsetzt. Leitprinzip: **Session-Handling und Credential-Handling sind strikt getrennt** — du verwaltest den *Zustand* der Session, **niemals** die Anmeldedaten.

> Sollte das Chrome-MCP nicht verbunden sein, bitte den User, die **Claude-in-Chrome-Extension** zu installieren/zu verbinden — **nicht** auf Pixel-Steuerung (computer-use) ausweichen, da Browser dort nur „read"-Tier haben (keine Klicks/Eingaben).

---

## ChromeSessionManager
**Zweck:** Chrome-Session bereitstellen und den erlaubten BSI-Arbeitsbereich abgrenzen.

- Verbundene Browser ermitteln: `list_connected_browsers`.
- Bestehende Session erkennen oder neue Instanz/dedizierte BSI-Chrome-Gruppe nutzen.
- Aktive Tabs auflisten und **erlaubte** BSI-Tabs identifizieren: `tabs_context_mcp`.
- Neue Tabs **nur für BSI-Aufgaben** öffnen: `tabs_create_mcp`.
- **Keine** fremden/privaten Tabs auslesen.

## BSISessionContext
**Zweck:** Den aktuellen Arbeitszustand halten — **ohne** je Credentials zu speichern.

Halte (im Gesprächsverlauf, nicht in Dateien) fest:
- aktuelle **Ziel-URL**
- erkannte **Umgebung** (DEV/INT/TEST/PROD)
- **Login-Status** (bestätigt / offen)
- aktueller **Modul-/Sicht-/Objektkontext** (z. B. „BSI CRM › Kunden › Kunde #4711")

**Verboten:** Benutzername, Passwort, Token, Cookie, Session-ID in irgendeiner Form festzuhalten.

## BSIEnvironmentResolver
**Zweck:** Umgebung eindeutig bestimmen. Details: [umgebung-erkennung.md](umgebung-erkennung.md).
- Aus URL-Mustern, Seitentitel oder Userangabe ableiten.
- **PROD** deutlich markieren.
- Bei Unsicherheit → User fragen, nicht raten.

## BSILoginGuard
**Zweck:** Sicherstellen, dass der **User selbst** einloggt.
- Vor dem Login den **Pflichttext** (siehe SKILL.md) ausgeben.
- **Keine** Login-Formulare automatisch befüllen, keine Credentials aus DOM/Screenshot lesen.
- Browser-**Aktionen erst freigeben**, nachdem der User den Login **bestätigt** hat.
- Gültige Session verifizieren über sichtbare Anker: Navigationsbaum, Desktopleiste, Cockpit/Dashboard, Benutzerprofil-Menü — **nicht** über Credential-Felder.

## BSITabController
**Zweck:** Bewegung auf freigegebene BSI-Tabs begrenzen.
- Relevante BSI-Tabs finden und nur zwischen **freigegebenen** wechseln.
- Neue Tabs ausschließlich für BSI-Aufgaben.
- **Keine** privaten oder fachfremden Tabs lesen. Bei mehreren BSI-Instanzen Zielumgebung klären.

## BSIPageNavigator
**Zweck:** Innerhalb der Suite navigieren und bedienen. UI-Karte: [ui-navigation.md](ui-navigation.md).
- Navigieren: `navigate`; Seiteninhalt erfassen: `read_page` / `get_page_text`; Elemente finden: `find`.
- Interaktion: `computer` (Klicks), `form_input` (Formularfelder) — **nur fachlich freigegebene** Felder.
- Nach jeder Aktion **validieren** (erwartetes Element/Statusmeldung sichtbar?).

## BSISafetyGuard
**Zweck:** Verändernde/destruktive Aktionen absichern. Katalog: [safety-guardrails.md](safety-guardrails.md).
- Destruktive Aktionen **blockieren**, bis Freigabe vorliegt.
- **PROD-Änderungen** gesondert absichern (Doppelbestätigung).
- Löschungen, Veröffentlichungen, Massenänderungen, Rechteänderungen **explizit** bestätigen lassen.
- **Dry-Run/Preview** nutzen, wo die Suite es anbietet (z. B. Vorschau vor Speichern/Versand).
