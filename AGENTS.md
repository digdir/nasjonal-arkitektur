# Instruksjoner for AI og LLM-agenter

Dette prosjektet inneholder modeller for Nasjonal Arkitektur.

## 1. Datakilde (YAML vs ArchiMate)

Når du (AI) blir bedt om å hente data, utføre analyser, eller svare på spørsmål om Nasjonal Arkitektur basert på innholdet i dette repoet, **skal du alltid bruke YAML-filen** som din primære datakilde:

- **Bruk primært:** `data/nasjonal-arkitektur.yaml`

Du skal **IKKE** prøve å parse `.archimate`-filen i `model/`-mappen direkte for analyse, med mindre brukeren eksplisitt ber deg om det. YAML-filen er prosjektets vedtatte "mellomformat", og inneholder de samme dataene strukturert på en måte som er mye enklere å prosessere og lese.

### Strukturen i datafilene

- `data/nasjonal-arkitektur.yaml` har fire toppnivånøkler: `model` (id, navn, versjon), `elements`, `relationships` og `views`. De tre siste er oppslag der nøkkelen er ArchiMate-id-en.
  - Elementer har `type` (f.eks. `Capability`, `Resource`, `Goal`, `Principle`, `Grouping`), `name`, `documentation`, `properties` og `folder_path`.
  - Relasjoner har `type`, `name`, `source_id`, `target_id`, `documentation` og `properties`.
  - Visninger har `nodes` (med `archimate_element_id` og `parent_node_id`) og `connections`.
- Kapabilitetshierarkiet (nivå 1–3) er uttrykt med `AggregationRelationship` mellom kapabiliteter, der `source_id` er den overordnede. Kapabiliteter er koblet til arkitekturprinsippene med `RealizationRelationship`.
- `data/nasjonal-arkitektur.ttl` inneholder de samme dataene som RDF (Turtle), med ArchiMate-vokabularet (`archimate:`) og prefikset `na:` for modellens elementer. Bruk den når en oppgave krever grafspørringer (f.eks. SPARQL) eller lenkede data. Ellers gjelder YAML-regelen over.

## 2. Kommandoer

```bash
python bygg_lokalt.py                # bygg alt: ArchiMate → YAML/TTL → docs/
python -m mkdocs serve               # forhåndsvis nettstedet på http://127.0.0.1:8000
bygg_og_publiser.bat "melding"       # bygg, commit alle endringer og push til main (publiserer)
```

## 3. Arbeidsflyt for dokumentasjon

- Dokumentasjonen i `docs/` bygges med `python bygg_lokalt.py`, som:
  1. finner den nyeste `.archimate`-filen i `model/` og konverterer den til `data/nasjonal-arkitektur.yaml` og `data/nasjonal-arkitektur.ttl`,
  2. kjører `scripts/generate_docs.py`, som lager Markdown-sidene i `docs/` fra malene i `templates/` og kopierer Archis HTML-eksport fra `model/html-export/` til `docs/archimate-report/`,
  3. kopierer modellen, YAML-filen og TTL-filen til `docs/` for nedlasting,
  4. kjører `scripts/bygg_oppsettpakke.py`, som pakker `arkitekturassistent/` og `data/nasjonal-arkitektur.yaml` til `docs/arkitekturassistent-oppsettpakke.zip`.
- **VIKTIG:** Ikke gjør manuelle endringer i Markdown-filene i `docs/`, i `docs/archimate-report/` eller i nedlastingsfilene i `docs/`. Disse overskrives ved hver bygging!
- **Arkitektur-data:** Endres i selve kilden (ArchiMate) og konverteres. Den interaktive Archi-rapporten eksporteres fra Archi til `model/html-export/`.
- **Tekst- og innholdssider:** Alle sider (forside, innledninger og egne sider som f.eks. målbilde) håndteres via mappen `templates/`. Endringer av tekst skal gjøres der! Hvis du skal lage en ny side, må du legge den i `templates/` og oppdatere `scripts/generate_docs.py` og `mkdocs.yml` for å få den inkludert.
- **Bilder og figurer:** Legges direkte i `docs/images/` (det finnes ingen bildemappe under `templates/`). Unngå æ, ø og å i filnavn, og slett gamle bilder fra repoet når de byttes ut. Med Markdown-syntaks (`![tekst](images/<filnavn>)`) justerer MkDocs stien automatisk. I rå HTML (f.eks. `<figure>`) må stien skrives relativt til den publiserte siden, f.eks. `../images/<filnavn>` for undersider.
- **Arkitekturassistenten:** Mappen `arkitekturassistent/` er kilden for oppsettpakken (systeminstruks, ressursoversikt, datasettfil, Digitaliseringsrundskrivet og `LESMEG.md`).
  - Ikke legg `nasjonal-arkitektur.yaml` i mappen. Den hentes alltid fra `data/` ved bygging, og byggingen stopper hvis den ligger der.
  - Det skal være nøyaktig én `Systeminstruks-*.md`. Versjonen står i filnavnet; ved ny versjon erstattes den gamle filen.
  - Plassholdere som `{{systeminstruks_fil}}` i `LESMEG.md` og `templates/arkitekturassistent.md` fylles inn ved bygging.
  - `docs/arkitekturassistent.md`, `docs/arkitekturassistent-oppsett.md` og zip-filen genereres og skal ikke redigeres. Stilen til figuren ligger i `docs/stylesheets/arkitekturassistent.css` og vedlikeholdes manuelt.
- Kjør alltid `python bygg_lokalt.py` når du har gjort endringer for å teste om det fungerer.

## 4. Publisering

- Nettstedet publiseres til GitHub Pages (grenen `gh-pages`) av en GitHub Action ved hver push til `main`.
- Actionen bygger nettstedet fra `docs/` slik det ligger i repoet, men kjører **ikke** `bygg_lokalt.py`. Kjør derfor `bygg_lokalt.py` lokalt og commit resultatet i `docs/` sammen med endringene i `templates/`.
- `site/` er en lokal byggemappe fra MkDocs og skal ikke committes (den står i `.gitignore`).
- Commit og push bare når brukeren ber om det.

## 5. Språk

- **Alltid** svar på norsk når du kommuniserer med brukeren.
- Fremtidige analyser, uttrekk, oppsummeringer og generering av dokumentasjon skal **alltid** gjøres på **norsk bokmål**, med mindre brukeren eksplisitt ber om noe annet.
