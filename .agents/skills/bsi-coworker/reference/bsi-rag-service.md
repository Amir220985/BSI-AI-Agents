# BSI RAG MCP Service — Dokumentations-Suchserver

Repository: `gitlab.adesso-group.com/collaborate/sandbox/819261d3/ai-services/bsi-mcp-service`  
Lokal (VPN nötig): klonen nach `/tmp/bsi-mcp-service` oder festes Verzeichnis.  
Verantwortlich: Robin (adesso)

## Was ist das?

Ein **lokaler, privater MCP-Server**, der die BSI Customer Suite Dokumentation semantisch durchsuchbar macht. Kein LLM läuft im Server — er macht reines Retrieval + Reranking und gibt zitierte Chunks zurück. 32.906 Chunks aus einem Struktur-erhaltenden Crawl der Original-Docs.

**Wann nutzen:** Wenn ich während einer Live-Aufgabe unsicher bin, wie ein Feature funktioniert oder konfiguriert wird. Statt zu raten → `search_docs("Meine Frage")` liefert zitierte Abschnitte aus der Originaldokumentation.

---

## Tools (wenn Server läuft)

| Tool | Signatur | Zweck |
|---|---|---|
| `search_docs` | `query, top_k=5, component=None` | Semantische Suche; liefert `text`, `score`, `file_name`, `component`, `source_url` |
| `get_document` | `identifier` | Vollständiges `.md` via `relative_path` oder `file_name` |
| `list_components` | — | Alle verfügbaren Doc-Bereiche (Filter für `search_docs`) |
| `search_datamodel` | `query, module=None, customized_only=False, top_k=20` | Struktursuche im **konfigurierten Datenmodell** (CSV, live) |
| `get_entity` | `entity_id` | Alle konfigurierten Elemente einer Entität |
| `list_datamodel_modules` | — | Module im Datenmodell (Filter für `search_datamodel`) |

### Datamodel-Tools (besonders wertvoll)
Das Datenmodell wird aus einer CSV exportiert, die sich **mehrfach pro Stunde ändern kann** (Customer Suite erlaubt Konfiguration jederzeit). Deshalb kein Embedding — lexikalische Suche. Nutze `search_datamodel` um herauszufinden, welche **Entitäten, Attribute und Feldgruppen** beim konkreten Kunden konfiguriert sind. Dann `get_entity` für alle Elemente einer Entität.

---

## Server starten

```bash
# Voraussetzung: Python 3.11 + uv, Repo geklont
cd /pfad/zu/bsi-mcp-service
.venv/bin/python scripts/serve.py
# Läuft dann auf http://127.0.0.1:8000/mcp (~25-30s Startzeit wegen Modell-Loading)
```

Nach dem Start können sowohl Claude Code als auch Claude Desktop darauf zugreifen (HTTP-Bridge via `.mcp.json`).

---

## Verfügbare Dokumentations-Komponenten (components)

| Component | Inhalt |
|---|---|
| `pink-book` | Developer/Admin-Referenz: Entitäten, Konfiguration, Business-Prozesse, Lambdas, Programmierung |
| `main` | Hauptdokumentation (Versionen 23.2–26.1) |
| `release-notes` | Release Notes 22.0 bis **26.2** (aktuellste verfügbare Version) |
| `business-solutions` | Best Practices + Konfigurationsrichtlinien (branchenspezifisch) |
| `techdoc-crm` | Technische CRM-Dokumentation |
| `techdoc-cx` | Technische CX-Dokumentation |
| `techdoc-eip` | Technische EIP-Dokumentation |
| `techdoc-ml` | Technische ML/AI-Dokumentation |
| `extensions` | CRM-Extensions, CX Factories, Guidelines |
| `scout-docs` | BSI Scout Development |
| `banking` | Banking-spezifisch (Finnova) |
| `insurance` | Versicherungs-spezifisch (Versionen 23.2–26.1) |
| `health` | Gesundheitswesen |
| `retail` | Einzelhandel |
| `space` | Deployment, Monitoring, Getting Started, Troubleshooting |
| `mpi` | Multi-Property Interface |
| `cx-design` | CX Design Creator |

---

## Offline-Alternative: crawled_docs direkt lesen

Wenn der Server nicht läuft, sind die Docs als lokale Markdown-Dateien verfügbar:

```
/tmp/bsi-mcp-service/crawled_docs/
  pink-book/26.1/          # Developer-Referenz (aktuell)
  main/26.1/               # Hauptdoku (aktuell)
  release-notes/26.2/      # Neueste Release Notes
  business-solutions/      # Best Practices + Konfigurationsrichtlinien
  techdoc-crm/26.1/        # Technische CRM-Doku
  ...
```

Ohne Server: direkt mit `Read` oder `Bash cat` lesen.

---

## Release 26.1 — Wichtigste Neuerungen (für CoWorker relevant)

**AI-Prozessautomatisierung (4 Stufen):**
- `Keine` → Standard-Prozess
- `Companion` → AI-Chat im Assistenten-Schritt
- `Review` → Companion schlägt Feldwerte + nächste Aktion vor (beim Öffnen automatisch)
- `Automatisch` → Companion führt Schritt komplett im Hintergrund aus (nur Free Step + Korrespondenzschritt)

Konfiguration im Prozess-Designer: Schieberegler global oder pro Schritt. Farbliche Visualisierung des Automatisierungsgrads.

**Live-Impulse** (für Telefon/Videogespräche mit BSI Snapview):
- Element `Gesprächsprotokoll für BSI Snapview` → Transkription in Echtzeit
- Element `Basis-Konfiguration AI-Impulse` → kontextbezogene Handlungsvorschläge live im Gespräch

**Input Management** (E-Mail-Verarbeitung): Präzisere Anliegen- und Kundenerkennung mit AI.

**BSI Elements**: Fachliche Pakete, die mit wenigen Klicks aktiviert werden können.

**Code Companion**: Unterstützt Konfiguratoren bei Systemanbindungen und komplexen Anforderungen.

**Agent Relationship Management (ARM)**: Orchestrierung der Interaktion zwischen AI-Agents des Endkunden und BSI Customer Agents.

---

## Pink Book 26.1 — Wichtige Erkenntnisse

### 360°-Sichten (Konfigurationsrichtlinien)
- Jedes Objekt braucht mindestens eine 360°-Sicht
- **4-spaltiges Design** bevorzugt; Standard-Breite 1335 Pixel
- Erste Sicht: Visitenkarte oben links → Geschäftsbeziehung → Kundeninfo → Einstufung/intern → Kommunikationen
- **Stack-Kachel**: für rollenspezifische Kacheln (z.B. Sales sieht Cash-Flow, Marketing sieht Marketing-Intensität)
- Tabellen können **mehrere Entitäten traversieren** (z.B. Kunde → Geschäftsvorfälle → Dokumente)
- Beim Vorschau-Filter: nach Datensatz (z.B. Kunde mit >50 Kommunikationen) vorfiltern
- **HTML-Kacheln**: kein JavaScript, kein komplexes CSS
- Konfigurationsexport/-import pro 360°-Sicht möglich (seit 22.0.40 auch Löschung übertragbar)

### Entitätskonzept
- **Hauptentität**: kann eigenständig existieren ODER wird unabhängig verarbeitet (Kunden, Aufträge, Kommunikationen, GeVos)
- **Subentität**: braucht eine Hauptentität zum Existieren (Gesprächsthemen, Interessen, Reisedaten)
- Beide haben: 360°-Sichten, Dossier-Ordner, Menüs, Dokumentvorlagen, Lambdas, Spalten, Tabellen

### Prozess-Konfigurationsrichtlinien
- Button `Weiter` = normaler Prozessfluss (immer so benennen)
- Kachel-Farbschema: Blau-invertiert = Schritte/Werkzeuge/neue Prozesse, Braun-invertiert = externe Systeme
- Prozessattribute nicht als DB-Spalten (außer für häufige, tabellarisch angezeigte Attribute)
- Pro Schritt: Arbeitsanweisungen nur wenn Mehrwert, keine HTML-Anleitungen auf Free Steps
