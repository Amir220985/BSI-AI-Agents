# Projekt-Richtlinien (Claude Code Configuration)

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

## Erlaubte Terminal-Werkzeuge
## Du darfst (und sollst) folgende Skripte über das Terminal ausführen, um deine Aufgaben zu erfüllen:
## - RAG-Suche: `python tools/search_rag.py`
## - Validierung: `python tools/validate_export.py <dateiname>`