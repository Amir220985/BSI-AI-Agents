# Umgebungs-Erkennung — DEV / INT / TEST / PROD

Vor **jeder** verändernden Aktion muss die Zielumgebung eindeutig feststehen. Die Erkennung liefert immer eines von: `DEV`, `INT`, `TEST`, `PROD` oder `UNBEKANNT`. Bei `UNBEKANNT` **fragst du den User** — du rätst nie.

## Signale (in dieser Reihenfolge)
1. **Explizite Userangabe** — wenn der User die Umgebung nennt, hat sie Vorrang.
2. **URL-Muster** (Hostname/Subdomain/Pfad) — siehe Heuristik unten.
3. **Seitentitel / sichtbare Umgebungs-Badges** — viele BSI-Instanzen zeigen Umgebung/Mandant im Titel oder in der Desktopleiste.
4. **Sichtbare Hinweise im Cockpit/in der Oberfläche** — Reiter, Kacheln oder Badges mit Bezeichnungen wie „Entwicklung", „Test", „Integration", „Produktion" oder ein Mandanten-/Demo-Name (z. B. „trials", „Demo") sind ein **schwaches Indiz**, kein Beweis. Sie können ein Fachbereich statt einer Umgebung sein (z. B. ein Cockpit-Reiter „Entwicklung" als Abteilung). Nutze sie nur **bestätigend** zu URL/Userangabe — bei Widerspruch zur URL gewinnt die strengere Einstufung, und du fragst nach.

## URL-Konvention (BSI-Standard, verbindlich)
Nicht-produktive BSI-Instanzen tragen ein **Umgebungs-Präfix als Subdomain-Label**. Fehlt jedes dieser Label (die Domain beginnt direkt mit dem Mandantennamen), handelt es sich **mit hoher Wahrscheinlichkeit um PROD**.

| Präfix-Label im Host | Umgebung |
|---|---|
| `dev.` | DEV (Entwicklung) |
| `trials.` | Trial / Demo (Sandbox) |
| `test.` | TEST |
| `config.` | Konfiguration |
| `mig.` | Migration |
| **kein** solches Präfix (Host beginnt mit dem Mandanten) | **PROD (hohe Wahrscheinlichkeit)** |

**Beispiele:**
- PROD: `https://ovb.bsi.cloud/bsicrm/` — kein Präfix → Produktion
- TEST: `https://test.ovb.bsi.cloud/bsicrm/` — `test.` → Testumgebung

> Das Präfix kann auch nicht-führend auftreten (z. B. `bsi-2005.trials.bsi-software.com` → Trial). Suche das Label irgendwo in der Subdomain; ist **keines** der fünf Label vorhanden, gilt **PROD**.

**Sicherheitsregel:** Ist aus der URL **kein** eindeutiges Nicht-PROD-Präfix ablesbar, behandelst du die Instanz **wie PROD**, bis der User das Gegenteil bestätigt. Lieber eine Rückfrage zu viel als eine ungewollte PROD-Änderung.

## Pflicht-Rückfrage vor dem Start (immer)
**Bevor** du mit der eigentlichen Aufgabe beginnst, lässt du dir die erkannte Umgebung **immer** vom User bestätigen — auch wenn die URL eindeutig wirkt. Irren ist menschlich, und eine Änderung auf der falschen Umgebung ist teuer.

Formuliere konkret, z. B.:
> „Ich erkenne **`<URL>`** als **`<UMGEBUNG>`**. Ist das die richtige Zielumgebung für diese Aufgabe? Bitte bestätige, bevor ich starte."

Erst nach klarer Bestätigung beginnst du. Bei verändernden Aktionen auf PROD gilt zusätzlich die Doppelbestätigung aus [safety-guardrails.md](safety-guardrails.md).

## Mehrere Instanzen offen
Sind mehrere BSI-Tabs/-Fenster geöffnet, **kläre die Zielumgebung eindeutig**, bevor du handelst — nenne dem User die erkannten URLs zur Auswahl.

## PROD-Markierung
Sobald PROD erkannt/angenommen ist:
- Kennzeichne den Kontext im Gespräch sichtbar als **„PROD"**.
- Aktiviere die verschärften Freigaben aus [safety-guardrails.md](safety-guardrails.md) (Doppelbestätigung für jede Änderung).
- Im Zweifel **nur lesen**, nicht schreiben.
