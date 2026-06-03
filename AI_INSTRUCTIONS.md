# Instruksjoner for AI og LLM-agenter

Dette prosjektet inneholder modeller for Nasjonal Arkitektur.

## 1. Datakilde (YAML vs ArchiMate)
Når du (AI) blir bedt om å hente data, utføre analyser, eller svare på spørsmål om Nasjonal Arkitektur basert på innholdet i dette repoet, **skal du alltid bruke YAML-filen** som din primære datakilde:
- **Bruk primært:** `data/nasjonal-arkitektur.yaml`

Du skal **IKKE** prøve å parse `.archimate`-filen i `model/`-mappen direkte for analyse, med mindre brukeren eksplisitt ber deg om det. YAML-filen er prosjektets vedtatte "mellomformat", og inneholder de samme dataene strukturert på en måte som er mye enklere å prosessere og lese.

## 2. Arbeidsflyt for dokumentasjon
- Markdown-dokumentasjonen i `docs/` genereres automatisk fra YAML-filen og innhold i `templates/` via scriptene `bygg_lokalt.py` / `scripts/generate_docs.py`.
- **VIKTIG:** Ikke gjør manuelle innholdsendringer direkte i filene i `docs/`. Disse overskrives ved hver generering!
- **Arkitektur-data:** Endres i selve kilden (ArchiMate) og konverteres.
- **Tekst- og introduksjonssider:** Sider som gjelder forside, innledninger eller egne Markdown-sider (som f.eks målbilde), håndteres via mappen `templates/`. Endringer av fast tekst skal gjøres der! Hvis du får beskjed om å lage eller redigere dokumentasjon som ikke er en del av ArchiMate-modellen, må du gjøre det i `templates/` og eventuelt oppdatere `scripts/generate_docs.py` og `mkdocs.yml` for å få den inkludert.
- **Struktur på de autogenererte visningene:** Gjøres ved å endre Python-koden i `scripts/generate_docs.py`.
- Kjør alltid `python bygg_lokalt.py` når du har gjort endringer for å teste om det fungerer.

## 3. Språk
- **Alltid** svar på norsk når du kommuniserer med brukeren.
- Fremtidige analyser, uttrekk, oppsummeringer og generering av dokumentasjon skal **alltid** gjøres på **norsk bokmål**, med mindre brukeren eksplisitt ber om noe annet.
