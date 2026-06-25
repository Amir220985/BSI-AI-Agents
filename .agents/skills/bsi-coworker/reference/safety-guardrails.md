# Safety-Guardrails — Freigaben, PROD-Absicherung, Dry-Run

Implementiert die Verantwortung von `BSISafetyGuard`. Ziel: **keine ungewollte Veränderung**, besonders nicht auf PROD.

## Aktionsklassen
| Klasse | Beispiele | Verhalten |
|---|---|---|
| **Lesen** | Suchen, Filtern, Datensatz/Reiter öffnen, Diagramm/Report ansehen | Ohne Freigabe erlaubt. Trotzdem nur im fachlich nötigen Rahmen. |
| **Verändernd** | Feld ändern/speichern, Datensatz anlegen, Prozess-/Assistentenschritt ausführen, Kommunikation versenden, Zuweisung/Status ändern | **Freigabe vor Ausführung.** Auf PROD: Doppelbestätigung. |
| **Destruktiv / weitreichend** | Löschen, Veröffentlichen/Publish, Massenänderung (mehrere Datensätze), Rechte-/Berechtigungsänderung, Konfigurations-Import, Jobs starten | **Blockiert bis explizite Freigabe.** Immer einzeln benennen, was passiert und welche Objekte betroffen sind. |

## Freigabe-Gate (vor verändernden Aktionen)
Bevor du eine verändernde/destruktive Aktion ausführst, fasse zusammen und hole **explizit** Freigabe ein:
- **Was** geändert wird (Aktion + konkrete Objekte/Felder/Anzahl)
- **Wo** (Modul/Bereich) und in **welcher Umgebung** (DEV/INT/TEST/**PROD**)
- **Reversibilität** (rückgängig machbar? — z. B. Versand/Veröffentlichung i. d. R. nicht)
- erst nach klarem „Ja" ausführen; bei Unsicherheit nachfragen statt annehmen

## PROD-Sonderregeln
1. Jede verändernde Aktion auf PROD braucht eine **zweite, ausdrückliche Bestätigung** („Ja, auf PROD ausführen").
2. **Massenänderungen, Löschungen, Veröffentlichungen, Rechteänderungen** auf PROD: zusätzlich die **Anzahl/Reichweite** nennen und einzeln bestätigen lassen.
3. Ist die Umgebung nicht eindeutig PROD-frei → wie PROD behandeln (siehe [umgebung-erkennung.md](umgebung-erkennung.md)).

## Dry-Run & Preview
Nutze, wo die Suite es anbietet, **vor** dem endgültigen Schritt:
- **Vorschau** vor Speichern, Versand (E-Mail/SMS/Brief), Veröffentlichung von Aktionen/Stories.
- **Selektions-/Zielgruppen-Vorschau** vor Marketing-Ausführung (Reichweite prüfen).
- **System-Meldungen & Rückfragen der Suite lesen**, nicht reflexhaft bestätigen — sie sind Teil der Sicherheitsprüfung.
- Wo kein Preview existiert: zuerst an **einem** Beispiel-/Testdatensatz validieren, dann erst breiter.

## Abbruch- und Rückfrageregeln
- Erscheint eine unerwartete Warnung/Fehlermeldung → **stoppen**, Meldung dem User zeigen, gemeinsam entscheiden.
- Verlangt eine Aktion Credentials/Bestätigung in einem Login-/Sicherheitsdialog → **dem User übergeben**, nicht selbst ausfüllen.
- Verlierst du den Session-/Kontextbezug (ausgeloggt, falscher Tab, andere Umgebung) → Aktion pausieren, Kontext neu verifizieren.
