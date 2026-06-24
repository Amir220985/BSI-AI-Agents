# tools/

Hilfsskripte zur Prüfung von BSI-CustomerSuite-Prozess-Exporten.

## lint_process.py — Prozess-Linter

Statische Prüfung jedes `crm.ProcessTransfer` in einem entpackten Export gegen die
Design-Rules/Anti-Patterns aus [`../knowledge`](../knowledge/).

### Aufruf
```bash
python3 tools/lint_process.py <export-ordner> [--json] [--min-severity ERROR|WARN|INFO]
```
Beispiele:
```bash
python3 tools/lint_process.py examples/bsi-crm-2026-06-24_15-09-39                 # alle Findings
python3 tools/lint_process.py examples/bsi-crm-2026-06-24_15-09-39 --min-severity WARN
python3 tools/lint_process.py examples/bsi-crm-2026-06-24_15-09-39 --json > report.json
```
Der Export-Ordner muss `codes/Prozess-45831/*.json` enthalten. `lambda-bindings/` wird,
falls vorhanden, zur eindeutigen Erkennung von Schnittstellen-Steps genutzt.

### Exit-Codes
- `0` keine ERRORs · `1` mindestens ein ERROR · `2` keine Prozessdateien gefunden

→ direkt als CI-/Pre-Export-Gate nutzbar.

### Geprüfte Regeln
| Schwere | Regel | Prüfung |
|---|---|---|
| ERROR | R1 | Start-/End-Step fehlt; Outlet ohne auflösbares Ziel; Outlet auf nicht existierenden Step |
| ERROR | R5/AP5 | Schnittstellen-/Lambda-Step ohne behandelten Fehlerpfad |
| WARN | LINT | Leere Verzweigung (mehrere Outlets auf dasselbe Ziel) |
| WARN | R1 | Sackgasse (Nicht-End-Step ohne Ausgang); Step vom Start nicht erreichbar |
| WARN | R2/AP7 | > 8 Steps ohne Gruppen |
| WARN | R8/AP1 | Tippfehler/auffällige Zeichen in Namen |
| INFO | R3/AP2 | Monolith-Verdacht (≥ 40 Steps) |
| INFO | R5 | Hintergrund-/Async-Step (Fehlerbehandlung außerhalb des Flows verifizieren); abgesicherte Schnittstellen |
| INFO | R6/AP9 | Entscheidungs-/Schnittstellen-Step ohne notes; nur generische Outlet-Labels (A/B/C) |
| INFO | R8 | Step ohne Namen |

### Wichtige Implementierungsdetails
- **Outlet-Ziel-Auflösung auf zwei Wegen:** (1) `targetProcessStepId`; (2) falls null, über geteilte
  `descriptorId` — ein Outlet ohne eigenes Ziel erbt das Ziel eines Geschwister-Outlets mit
  gleicher `descriptorId`. Nur wenn beides fehlschlägt, gilt ein Outlet als **echt offen** (ERROR R1).
  *(Ohne diese Auflösung entstehen massiv falsch-positive „offene Verzweigung"- und
  „unerreichbar"-Meldungen — verifiziert: 8 von 11 Null-Target-Outlets sind über descriptorId verbunden.)*
- **Step-Typen** (201503 Start, 201504 End, 209754 Lambda, 209153 Kriterien, 216266 Hintergrund …)
  stammen aus [`../knowledge/bsi_step_type_catalog.md`](../knowledge/bsi_step_type_catalog.md) und sind
  als Konstanten oben im Skript pflegbar.
- **Tippfehler-Liste** (`KNOWN_TYPOS`) ist kuratiert (aus dem Beispiel-Datensatz) und bewusst konservativ,
  um Fehlalarme zu vermeiden; erweiterbar.

### Bekannte Grenzen
- „Vom Start nicht erreichbar" kann von echten offenen Outlets **oder** von mehreren Einstiegspunkten
  (z. B. separater Self-Service-Einstieg) herrühren — gemeinsam mit den R1-ERRORs bewerten.
- Step-Typ-Semantik ist abgeleitet, nicht offiziell (s. Katalog-Vorbehalt).

### Referenzlauf (Beispiel-Export `bsi-crm-2026-06-24_15-09-39`)
19 Prozesse → **5 ERROR** (2× AP5: „Start Push zu CS-API", „Lambda aufrufen [Fahrzeug Self-Service]";
3× offene Outlets), 26 WARN, 379 INFO. Deckt sich mit
[`../knowledge/audit_ap5_schnittstellen_fehlerpfade.md`](../knowledge/audit_ap5_schnittstellen_fehlerpfade.md).
