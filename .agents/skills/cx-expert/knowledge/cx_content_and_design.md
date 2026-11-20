# BSI CX – Content, Design & Medien

> Abgeleitet aus `examples/` und der BSI-CX-Help-Center-Doku.

## Content (`studio.Content`)

Content liefert den Inhalt für **Push-Steps** (Touchpoints). Ein Content ist mehrsprachig, hat einen **Content-Typ** und – bei E-Mail/Landingpage/Gesprächsleitfaden/Vorschau – ein **Design**.

**Ablage im Export:** Ordner pro Content/Version:
```
contents/<Name>_(<contentType>)_-_Version_<n>-<uuid>-<rev>/
├── content.json                  # studio.Content (Metadaten)
└── content-resource-<lang>.html  # eigentlicher Inhalt je Sprache (z. B. de-CH)
```

**`content.json` – wichtige Felder:**
| Feld | Bedeutung |
|---|---|
| `contentType` | Content-Typ (s. u.) |
| `name`, `status` | Bezeichnung, Status (Pflichtfelder) |
| `storyGid` | Verknüpfung zur Story (oder leer = freier Content) |
| `contentRevision`, `latestRevision` | Versionierung |
| `folderId` | Ablageordner |
| `validFromDate`, `validUntilDate` | Gültigkeit |
| `tags` | Schlagworte |

### Content-Typen (10, laut Doku)
| Typ (`contentType`) | Verwendung | Design? | Kann enthalten |
|---|---|---|---|
| `email` | E-Mail/Newsletter | ja | Platzhalter, Iteratoren, Links, News Snippets, Varianten |
| `landing-page` | einzelne HTML-Seite | ja | Platzhalter, Iteratoren, Links, Formulare, News Snippets, Varianten |
| `word-document` | Brief/Anlage/Download (PDF-Ausgabe möglich) | nein | Platzhalter |
| `pdf-document` | Brief/Anlage/Download | nein | Formulare |
| `sms` | SMS | nein | Platzhalter, Links |
| `news-snippet` | Snippet für E-Mail/Web | nein | empfängerspezifisch |
| `whatsapp` | WhatsApp-Nachricht | nein | Platzhalter, Links |
| `gespraechsleitfaden` | Outbound-Call-Leitfaden | ja | Platzhalter, Links, Varianten |
| `ical` | Kalendereintrag | nein | Platzhalter, Links |
| `preview` | Vorschau für Mitmachen-Stories | ja | Platzhalter, Iteratoren, Links, Formulare, News Snippets, Varianten |

In den Beispiel-Exporten vertreten: `landing-page` (33), `email` (11), `word-document` (7), `sms` (2), `preview` (1).

### Personalisierungs-Bausteine
- **Platzhalter**: werden aus dem Content ausgelesen und in der Story mit Daten ersetzt.
- **Varianten**: bedingter Content (Sichtbarkeit von Elementen je Bedingung).
- **Iteratoren / Links / Formulare / News Snippets**: je nach Content-Typ.
- **Sprachversionen**: je `content-resource-<lang>.html`; verfügbare Sprachen via Administration › Einstellungen › CX.
- **Barrierefreiheit**: Alt-Texte, Textsprache, URL-Beschreibungen.

## Design (`studio.DesignConfig`)

Layoutvorlage für die designfähigen Content-Typen (`email`, `landing-page`, `gespraechsleitfaden`, `preview`). Content referenziert ein Design; „Design aktualisieren" hebt Content auf die neuste Design-Version. Ablage analog Content als Ordner `designs/<…>-<uuid>-<rev>/design.json` + Ressourcen.

## Medien (`studio.media-library-item`)

Mediathek-Objekte (Bilder/Dokumente): Ordner `media-library-items/<datei>-<uuid>/` mit Binärdatei + `media-library-item.json`. Werden in Content/Design referenziert; Alt-Text für Barrierefreiheit hinterlegbar.

## Verknüpfungslogik (für Generierung wichtig)
1. **Push-Step → Content**: Der Push-Step (z. B. `SendEmail`, `LandingPage`) referenziert einen Content.
2. **Content → Design**: designfähige Content-Typen referenzieren ein Design.
3. **Content/Design → Medien**: über `media-library-item`-IDs.
4. **Content → Story**: `content.json.storyGid`.

Alle referenzierten Artefakte müssen im Export als eigene Index-Items vorhanden sein (`full`, mitgeliefert) oder im Zielsystem existieren (`reference-only`) — siehe `cx_export_format.md` §4 und export-expert.

## Strukturänderungen = neue Version
Laut Doku: Ändert sich die **Struktur** eines Contents (neue Platzhalter, andere Links/Formulare), muss eine **neue Content-Version** erstellt werden, weil dies die Story-Struktur beeinflusst. Reine Textkorrekturen aktualisieren den Content ohne neue Version.
