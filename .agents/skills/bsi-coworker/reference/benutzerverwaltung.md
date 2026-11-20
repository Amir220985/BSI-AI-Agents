# Benutzerverwaltung & Berechtigungen

Navigationspfad: **Administration → Benutzerverwaltung**
Quelle: BSI CRM Handbuch Admin Ocean FSR1, Kapitel 10.

## Berechtigungsmodell (Übersicht)

```
Benutzer → hat Rollen → Rollen haben Funktionen → Funktionen haben Level
```

- **Funktion**: Vorgegeben, nicht administrierbar (z.B. „Aufgaben lesen", „Globale Suche verwenden"). Definiert Read/Create/Update/Delete oder Aktionsberechtigungen.
- **Rolle**: Sammlung von Funktionen. Nicht hierarchisch. Ein Benutzer kann mehrere Rollen haben. Typ: intern oder extern.
- **Level**: Bestimmt den Datenumfang pro Funktion → drei Level:

| Level | Bedeutung |
|---|---|
| **Alle** | Uneingeschränkter Zugriff auf alle Daten im System |
| **Eigene** | Nur Datensätze, an denen der Benutzer direkt verknüpft ist (Verantwortlicher, Betreuer, Besitzer) |
| **Organisationseinheit** | Alle Datensätze, die zur eigenen OE (und darunter liegenden OEs) gehören |
| **Bestandsabgegrenzt** | Wie Alle/Eigene/OE, aber auf einen Bestand (Mandant) beschränkt |

## Organisationseinheiten (OE)
Administration → Benutzerverwaltung → Organisationseinheit

- Hierarchische Struktur (Master-OE oben, dann Abteilungen/Teams/Büros)
- Jeder Benutzer gehört **eindeutig** einer OE an
- OE bestimmt, **wo** Objekte des Benutzers im Baum hängen (nicht die Berechtigungen selbst)
- Berechtigungen werden ausschließlich über Rollen & Funktionen gesteuert
- Neue OEs über Menüzeile erstellen; Berechtigungen nach Änderung über Menüzeile neu laden

## Virtuelle Teams
Administration → Benutzerverwaltung → Virtuelle Teams

- Benutzergruppen quer zu OE-Grenzen (abteilungsübergreifend möglich)
- Typisch: Contact Center (GeVo-Zuweisung), Betreuungsgruppen
- Benutzer kann in mehreren virtuellen Teams sein
- Jedes Team hat eine besitzdefinierende OE (für Berechtigungsprüfung)
- Teamtyp aus Werteliste wählen

## Benutzer anlegen (intern)
Administration → Benutzerverwaltung → Benutzer → Alle Internen

Voraussetzung: Erst Kunden anlegen (Person mit interner Organisation verknüpft), dann Benutzer.

1. Benutzernamen setzen
2. Passwort vergeben
3. Kunden verknüpfen (nur Kunden ohne bestehenden Benutzer wählbar)
4. Besitzdefinierende OE zuweisen
5. Rollen zuweisen (+ pro Rolle: OE-Scope, wenn Level=OE)

Weitere Aktionen in der Menüzeile:
- **Fokus nehmen**: Kundendossier des Benutzers öffnen
- **Deaktivieren**: Benutzer, der das Unternehmen verlassen hat
- **Generaländerung**: Alle Daten (Betreuungen, Aufträge, Komm., Aufgaben, Marketing) auf anderen Benutzer übertragen
- **Berechtigungen neu laden**: Nach Rollenänderungen

## Externe Benutzer
Administration → Benutzerverwaltung → Benutzer → Alle Externen
- Z.B. Zugriff auf Tickettool für Kunden/Partner
- Manuell anlegen oder via LDAP
- Dürfen keine internen Rollen zugewiesen bekommen

## Rollen verwalten
Administration → Benutzerverwaltung → Rollen

- Neue Rolle erstellen (nur Typ = intern/extern einstellbar)
- **Rollen kopieren** (inkl. aller Funktionen): schnellste Art, ähnliche Rollen zu erstellen
- **Rollen zusammenlegen**: alle Funktionen in eine Rolle vereinen
- Deaktivieren: alle Benutzer mit dieser Rolle verlieren sofort die Berechtigungen
- Nach Funktionsänderung: „Berechtigungen neu laden" in Menüzeile

## Wichtige Funktionen & Tipps
- `Change Business Owner`: Bearbeiten berechtigungsbestimmender Auftragsdaten (z.B. Betreuer zuweisen) — Verkaufsleiter typischerweise
- `Change Legal Entity Owner`: Analog für Partner
- **LDAP-Sync**: Benutzer aus Active Directory synchronisieren
- **Favoriten, Kategorien, Optionen**: Pro Benutzer verwaltbar

## Bestände (Mandanten)
- Logische Datenabgrenzung innerhalb eines Systems (Multi-Mandanten-Fähigkeit)
- „Der Anwender darf Daten aus Bestand X sehen" = Berechtigung für alle Daten dieses Bestands
- Standardmäßig Einzel-Bestand; Mehrbestandssysteme brauchen spezielle Planung mit BSI

## Monitoring → Tutorials
Administration → Monitoring → Tutorials: Zeigt, welcher Benutzer wann welches Tutorial abgeschlossen hat.
