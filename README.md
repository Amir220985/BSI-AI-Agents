# BSI AI Development

KI-gestützte Entwicklungsumgebung für die **BSI CustomerSuite**. Dieses Repository enthält spezialisierte Agent-Skills, Registries und Beispiel-Exporte, die es Claude Code ermöglichen, BSI-Konfigurationen (Prozesse, Schnittstellen, Exporte) automatisiert zu erstellen und zu validieren.

---

## Inhalt

```
.agents/skills/          # Spezialisierte Agent-Skills
  cx-design/             # BSI CX Master Template Web: Kundendesign einrichten & anpassen
  cx-expert/             # BSI CX (studio): Customer Stories & Marketing Automation
  eip-lowcode-expert/    # EIP-Schnittstellen & Low-Code (TypeScript)
  export-expert/         # BSI ZIP-Export-Erstellung & Validierung
  process-expert/        # Business-Prozesse (BSI CRM) & Step-Registry
.antigravity/            # Globale Systemregeln
CLAUDE.md                # Projekt-Konfiguration für Claude Code
```

---

## Skills & Fähigkeiten

### 1. Process Expert — Business-Prozesse erstellen

**Skill:** `.agents/skills/process-expert/`

Erstellt vollständige, importierbare BSI-Prozess-Konfigurationen als ZIP-Exporte.

**Was der Agent kann:**
- Neue Business-Prozesse aus natürlichsprachlicher Beschreibung generieren
- Steps aus der zentralen Registry auswählen und korrekt verschalten
- Verzweigungslogik (Kriterien-Step) mit verschachtelten DataModel-Constraints konfigurieren
- Bindings, Outlets und stepConfiguration für komplexe Steps automatisch befüllen
- Valide ZIP-Exporte erstellen, die direkt in BSI importiert werden können

**Registry:** `process_step_registry.json` v3.0.0 — 123 Steps mit Feldern:

| Feld | Beschreibung |
|---|---|
| `requiredBindings` | Pflicht-Bindings mit vollständigem JSON-Beispiel |
| `stepConfigurationType` | `_type` der `stepConfiguration` |
| `stepConfigurationTemplate` | Vollständiges Template |
| `outletDescriptors` | Outlet-Struktur (inkl. "Keine Treffer") |
| `indexRequirements` | Zusätzliche Index-Items für den Export |
| `constraintPattern` | Constraint-Struktur für Verzweigungsschritte |

**Angereicherte Steps:** Start (201503), Ende (201504), Adressen ändern (176353), Kriterien (209153), Kachelschritt (138297), Korrespondenz erstellen (168901), Informationen anzeigen (10048)

**Beispielprozesse (validiert):**
- Adressänderung Kunde — Start → Adressen ändern → Ende
- Kundenformprüfung — Start → Kriterien (Kundenform) → [Korrespondenz | Kachelschritt] → Ende

---

### 2. CX Expert — Customer Stories (Marketing Automation)

**Skill:** `.agents/skills/cx-expert/`

Erstellt importierbare BSI-CX-Konfigurationen (Produkt **`studio`**): Customer Stories mit Steps, Content, Designs, Flavors und Indikatoren.

**Was der Agent kann:**
- Customer Stories aus natürlichsprachlicher Beschreibung entwerfen
- Steps aus der CX-Step-Registry wählen (5 Step-Arten: Teilnehmer/Logik/Daten/Push/Prozedur) und über Outlets (`targetStepGid`) verschalten
- Content (E-Mail, Landingpage, SMS, Dokument …) und Designs verknüpfen
- Valide studio-ZIPs erstellen (auch Multi-Paket CX+CRM via `multi-index.json`)

**Registry:** `registry/cx_step_registry.json` v1.0.0 — 59 Step-Typen (aus 20 Beispiel-Stories / 489 Steps), Schlüssel = `customConfig._type`.

**Knowledge Base:** Exportformat, Step-Katalog, Story-Inventar, Content/Design, Patterns, Glossar, Designregeln, Generierungs-Template, Review-Checkliste.

**Grundlage:** 17 reale CX-Exporte (`examples/`) + BSI-CX-Help-Center-Doku.

---

### 3. EIP Low-Code Expert — Schnittstellen & Integrationen

**Skill:** `.agents/skills/eip-lowcode-expert/`

Erstellt EIP-Schnittstellen (Interfaces) für die BSI Enterprise Integration Platform.

**Was der Agent kann:**
- EIP-Interfaces aus Standard-Steps zusammenstellen
- Komplexe Transformations- und Validierungslogik als TypeScript (Low-Code-Step) implementieren
- Korrekte `_typeVersion`-Werte je BSI-Version setzen (kritisch für fehlerfreien Import)
- Neue Projekte anlegen und Interfaces darin einbetten
- Valide Interface-JSON-Dateien für den ZIP-Export generieren

**Bekannte Step-Typen:**
- HTTP-Requests, XML/JSON-Parser, DB-Adapter
- Iteration (`interfaces.IterationProcessorConfig`)
- CRM DataModel Search (`interfaces.CrmDataModelSearchProcessorConfig`)
- Low-Code (TypeScript) für beliebige Logik

**Beispiele:** IBAN-Validierung, CSV-Import, CRM-Export, API-Trigger

---

### 4. Export Expert — ZIP-Export-Erstellung

**Skill:** `.agents/skills/export-expert/`

Stellt sicher, dass generierte Konfigurationen als valide BSI-Import-ZIPs verpackt werden.

**Was der Agent kann:**
- `index.json` mit korrekten Pflichtfeldern je Produkttyp (`crm` / `interfaces`) aufbauen
- `globalUniqueId` aus BSI-UIDs ableiten (Ableitungsregeln für alle UID-Muster)
- `transferType: full` vs. `reference-only` korrekt zuweisen
- `primary-processes`-Dateien im richtigen Format (`crm.PrimaryProcessIdTransfer`) erstellen
- Inkonsistente Index-Referenzen erkennen und korrigieren

**Unterstützte Export-Typen:**

| Typ | `productId` | Pflichtfelder |
|---|---|---|
| CRM-Prozess | `crm` | `productIdentifier`, `productVersion`, `valueMigrationIds` |
| EIP-Interface | `interfaces` | — |

---

### 5. CX Design Expert — BSI CX Master Template einrichten

**Skill:** `.agents/skills/cx-design/`

Richtet neue BSI CX Master Template Web-Projekte ein und passt sie vollständig an das Kundendesign an.

**Was der Agent kann:**
- GitHub-Release herunterladen, entpacken und `npm install` ausführen
- Schriften (Google Fonts / lokal), Logo und Favicon einbinden
- Kundenfarben analysieren und in `variables.scss` + `properties.js` eintragen
- Bootstrap-Overrides und SCSS-Token-Struktur aufbauen
- Footer als ContentElement erstellen und in `design.js` registrieren
- Navigation in `navigation.scss` vollständig implementieren
- Bestehende BSI-Content-Elemente ans Kundendesign anpassen (SCSS, StyleConfigs)
- Neue ContentElements, Includes und PageIncludes anlegen

**Einstiegspunkt:** `/cx-setup` — orchestriert alle weiteren Sub-Skills (`cx-brand`, `cx-fonts`, `cx-colors`, `cx-layout`, `cx-elements-customize`, `cx-element-create`)

---

<<<<<<< README.md
## Einrichtung

### 1. Repository auschecken

```bash
git clone <repo-url>
cd bsi-core-ai-system
```

### 2. API-Key hinterlegen

Lege eine `.env`-Datei im Projektverzeichnis an (wird nicht eingecheckt):

```bash
echo 'BSI_MCP_API_KEY=dein-api-key' > .env
```

Den API-Key erhältst du vom Projektverantwortlichen.

### 3. Setup-Skript ausführen

**macOS / Linux:**
```bash
./setup.sh
source ~/.zshrc
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

Das Skript konfiguriert automatisch:
- **Claude Code CLI** — trägt den API-Key in `~/.zshrc` ein, sodass `.claude/settings.json` den MCP-Server erkennt
- **Claude Desktop App** — patcht `~/Library/Application Support/Claude/claude_desktop_config.json` mit dem `mcp-remote`-Eintrag

### 4. Apps neu starten

Claude Code und/oder die Claude Desktop App neu starten. Der MCP-Server **azure-knowledge-base** ist danach verfügbar und ermöglicht semantische Suche in der BSI-Dokumentation direkt aus dem Chat.
=======
### 5. BSI CoWorker — Live-Bedienung der Customer Suite

**Skill:** `.agents/skills/bsi-coworker/`

Bedient eine **laufende BSI-Customer-Suite-Instanz** interaktiv über eine **aktive Chrome-Session des Users** — im Gegensatz zu den drei anderen Skills, die Export-Dateien *erzeugen*.

**Was der Agent kann:**
- Ziel-URL und Umgebung (DEV/INT/TEST/PROD) abfragen bzw. ableiten
- Den User zum **manuellen Login** in Chrome auffordern und mit der aktiven Session weiterarbeiten
- In der Suite navigieren (CRM, CX, Insight, AI, EIP), Datensätze suchen/pflegen, Assistenten/Prozesse ausführen
- Verändernde und destruktive Aktionen über **Freigabe-Gates** absichern, PROD gesondert schützen, Dry-Run/Preview nutzen

**Sicherheitsgrundsatz:** Der Agent fragt **niemals** Credentials ab, speichert/protokolliert keine Zugangsdaten und interagiert ausschließlich mit **freigegebenen** BSI-Tabs. Technische Basis: Claude-in-Chrome-MCP.

**Komponenten:** `ChromeSessionManager`, `BSISessionContext`, `BSIEnvironmentResolver`, `BSILoginGuard`, `BSITabController`, `BSIPageNavigator`, `BSISafetyGuard` (siehe `reference/session-architektur.md`).
>>>>>>> README.md

---

## Verwendung

Das Repository unterstützt zwei KI-Plattformen:

### Claude Code (Anthropic)

Die Skills werden automatisch aktiviert, wenn Claude Code in diesem Verzeichnis gestartet wird. Die `CLAUDE.md` definiert, welche Skills für welche Aufgaben genutzt werden.

### Google Antigravity

Alternativ kann das Repo mit **Google Antigravity** genutzt werden. Die globalen Systemregeln und Verhaltensrichtlinien liegen in `.antigravity/system_rules.md` und werden von Antigravity beim Start des Workspaces automatisch eingelesen.

**Beispiel-Prompts:**

```
"Erstelle mir einen Prozess, der einen Kunden als Input nimmt und je nach
Kundenform (Person / Organisation) unterschiedliche Schritte ausführt."

"Baue ein EIP-Interface, das Kundendaten aus einer CSV-Datei liest,
die IBAN validiert und das Ergebnis per HTTP an eine externe API sendet."
```

---

## Voraussetzungen

- **Claude Code** oder **Google Antigravity** mit Zugriff auf dieses Repository
- **BSI CustomerSuite** ab Version 26.1.x (Zielversion für Exports)
- Für Importe: BSI-Instanz mit Import-Berechtigung

---

## Roadmap / Geplante Skills

- **Datenmodell-Agent** — Automatische Auskunft über CRM-Entitäten, Relationen und Attribut-UIDs (ersetzt manuelle UID-Recherche für Kriterien-Steps)
- **Validierungs-Agent** — Automatische Prüfung generierter ZIPs vor dem Import
- **Context-Kunde-Agent** — Kundenspezifische Konfigurationen und Vorlagen verwalten
