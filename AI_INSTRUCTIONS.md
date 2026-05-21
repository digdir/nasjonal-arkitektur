# Instruksjoner for AI og LLM-agenter

Dette prosjektet inneholder modeller for Nasjonal Arkitektur.

## 1. Datakilde (YAML vs ArchiMate)
Når du (AI) blir bedt om å hente data, utføre analyser, eller svare på spørsmål om Nasjonal Arkitektur basert på innholdet i dette repoet, **skal du alltid bruke YAML-filen** som din primære datakilde:
- **Bruk primært:** `data/nasjonal-arkitektur.yaml`

Du skal **IKKE** prøve å parse `.archimate`-filen i `model/`-mappen direkte for analyse, med mindre brukeren eksplisitt ber deg om det. YAML-filen er prosjektets vedtatte "mellomformat", og inneholder de samme dataene strukturert på en måte som er mye enklere å prosessere og lese.

## 2. Arbeidsflyt for dokumentasjon
- Markdown-dokumentasjonen i `docs/` genereres automatisk fra YAML-filen ved hjelp av `scripts/generate_docs.py`. 
- Ikke gjør manuelle innholdsendringer i de autogenererte `.md`-filene i `docs/`. Innhold skal endres i kilden (ArchiMate), som deretter konverteres. Endringer i utseende/struktur på dokumentasjonen gjøres ved å oppdatere scriptet `scripts/generate_docs.py`.

## 3. Språk
- **Alltid** svar på norsk når du kommuniserer med brukeren.
- Fremtidige analyser, uttrekk, oppsummeringer og generering av dokumentasjon skal **alltid** gjøres på **norsk bokmål**, med mindre brukeren eksplisitt ber om noe annet.
