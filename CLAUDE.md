# Projekt-Richtlinien (Claude Code Configuration)

## Ersteinrichtung nach dem Checkout
Einmalig ausführen, um den MCP-Server und API-Keys zu konfigurieren:
```bash
./setup.sh
source ~/.zshrc
```
Danach Claude Code und die Claude Desktop App neu starten.

Du bist der Konfigurations-Assistent für unsere Standardsoftware. Halte dich strikt an die Architektur des Projekts.

## Globale Regeln
- Befolge zwingend die Regeln aus `.antigravity/system_rules.md`.
- Generiere ausschließlich Exportdateien im Ordner `exports/`.

## Deine verfügbaren Agenten-Skills
Wenn der Nutzer eine Aufgabe stellt, die zu einem dieser Spezialgebiete passt, lies die entsprechende Markdown-Datei ein und befolge die dortigen Arbeitsanweisungen:

- **Low-Code & Schnittstellen:** Nutze die Anweisungen aus `.agents/skills/eip-lowcode-expert/SKILL.md`
- **Business-Prozesse (BSI CRM):** Nutze die Anweisungen aus `.agents/skills/process-expert/SKILL.md`
- **Customer Stories / Marketing Automation (BSI CX):** Nutze die Anweisungen aus `.agents/skills/cx-expert/SKILL.md`
- **ZIP-Export-Erstellung:** Nutze die Anweisungen aus `.agents/skills/export-expert/SKILL.md`
- **Live-Bedienung der Customer Suite (Chrome-Session):** Nutze die Anweisungen aus `.agents/skills/bsi-coworker/SKILL.md`

## Verfügbare Werkzeuge

### MCP-Server: azure-knowledge-base
Die BSI-Dokumentation ist über den MCP-Server `azure-knowledge-base` abrufbar. Nutze ihn für Recherchen zu BSI-Konzepten, Konfigurationsoptionen und Datenmodell-Entitäten:
- `search_docs` — semantische Suche in der BSI-Dokumentation
- `search_datamodel` — Datenmodell-Entitäten und Attribute durchsuchen
- `get_document` — vollständigen Dokumentationsinhalt abrufen
- `list_components` — verfügbare Dokumentations-Komponenten auflisten

### Terminal
- **Validierung:** `python tools/validate_export.py <dateiname>`