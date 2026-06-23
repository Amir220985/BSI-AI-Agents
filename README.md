# BSI AI Development

KI-gestützte Entwicklungsumgebung für die **BSI CustomerSuite**. Dieses Repository enthält spezialisierte Agent-Skills, Registries und Beispiel-Exporte, die es Claude Code ermöglichen, BSI-Konfigurationen (Prozesse, Schnittstellen, Exporte) automatisiert zu erstellen und zu validieren.

---

## Inhalt

```
.agents/skills/          # Spezialisierte Agent-Skills
  eip-lowcode-expert/    # EIP-Schnittstellen & Low-Code (TypeScript)
  export-expert/         # BSI ZIP-Export-Erstellung & Validierung
  process-expert/        # Business-Prozesse & Step-Registry
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

### 2. EIP Low-Code Expert — Schnittstellen & Integrationen

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

### 3. Export Expert — ZIP-Export-Erstellung

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
