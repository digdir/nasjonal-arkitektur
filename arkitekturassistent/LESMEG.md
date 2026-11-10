# Arkitekturassistenten – sett opp assistenten i ditt eget KI-verktøy

Denne veiledningen forklarer hvordan du setter opp og bruker Arkitekturassistenten i et KI-verktøy du selv har tilgang til, for eksempel Claude, ChatGPT, Microsoft 365 Copilot eller Gemini. Assistenten kjører i ditt eget verktøy og på din egen lisens.

> **Under arbeid:** Digitaliseringsdirektoratet (Digdir) arbeider med å gjøre Arkitekturassistenten tilgjengelig som en brukervennlig KI-tjeneste og som en del av et fremtidig agentisk rammeverk. Inntil videre kan du kjøre den i ditt eget KI-verktøy slik det er beskrevet her.

## 1. Hva er Arkitekturassistenten?

Arkitekturassistenten hjelper deg å vurdere egne behov, prosjekter og dokumenter opp mot Nasjonal arkitektur for samhandling og det felles digitale økosystemet i Norge.

Assistenten er ikke et eget program. Den består av en **systeminstruks**, som forteller KI-verktøyet hvordan det skal arbeide, og et **kunnskapsgrunnlag** med kapabiliteter, arkitekturprinsipper, fellesløsninger og datasett. Når du laster opp disse filene i ditt eget KI-verktøy, arbeider verktøyet som Arkitekturassistenten.

Assistenten kan hjelpe deg på tre måter:

- **Spørsmål om kunnskapsgrunnlaget.** Eksempel: «Hvilke kapabiliteter finnes under Datadeling?» Du får et direkte svar.
- **Drøfting av et case.** Eksempel: «La oss drøfte dette caset» eller «Hva er det egentlige problemet her?» Assistenten drøfter i dialog, utfordrer problemforståelsen og stiller oppfølgingsspørsmål, uten å lage en full analyse.
- **Full analyse av et behov, prosjekt eller dokument.** Du får en strukturert analyse med behov, kapabiliteter og prinsipper, gjenbrukbare fellesløsninger og datasett, dekning og gap, alternative tiltak, en tom evalueringsmal, en foreløpig vurdering og en oppsummering for prosjektleder og styringsgruppe.

Assistenten svarer på grunnlag av filene du laster opp. Den finner ikke på fellesløsninger, prinsipper eller kapabiliteter, og den sier fra hvis en kilde mangler.

## 2. Filene i oppsettpakken

| Fil | Innhold | Bruk |
| :--- | :--- | :--- |
| `{{systeminstruks_fil}}` | Systeminstruksen: rollen, arbeidsmåten og formatet på analysene. | Påkrevd |
| `nasjonal-arkitektur.yaml` | Modellen for Nasjonal arkitektur: kapabilitetskartet (nivå 1–3) og arkitekturprinsippene. | Påkrevd |
| `na_ressursoversikt.md` | Fellesløsninger og fellesressurser: løsninger, standarder og veiledning, samhandlingsarenaer og økonomiske og juridiske virkemidler. | Påkrevd |
| `Hent-ressurs-resultat-liten.csv` | Gjenbrukbare datasett fra Felles datakatalog (data.norge.no). | Påkrevd |
| `Digitaliseringsrundskrivet.md` | Digitaliseringsrundskrivet. Brukes bare til å forankre anbefalingene i statlige krav og anbefalinger. | Valgfri |
| `LESMEG.md` | Denne veiledningen. | Lastes ikke opp |

> **Merk:** Systeminstruksen nevner også Nasjonal digitaliseringsstrategi som kilde. Den er ikke med i pakken. Hvis assistenten sier at strategien mangler, kan du se bort fra det.

Ressursoversikten og datasettfilen er store. Bruk derfor helst verktøyets funksjon for prosjekt eller egen assistent (alternativ 1 nedenfor). Da slipper du også å laste opp filene på nytt hver gang.

## 3. Oppsett steg for steg

Systeminstruksen lastes alltid opp som en fil, sammen med de andre filene. I feltet for instruksjoner limer du bare inn en kort **startinstruks**. Slik fungerer oppsettet likt i alle verktøyene, også der instruksfeltet har en grense for antall tegn.

### Startinstruksen

Kopier denne teksten:

```text
Du er Arkitekturassistenten. Les hele filen {{systeminstruks_fil}} før du svarer, og følg instruksene i den gjennom hele samtalen. Bruk de andre opplastede filene som kunnskapsgrunnlag, slik systeminstruksen beskriver. Svar på norsk.
```

### Alternativ 1: Prosjekt eller egen assistent (anbefalt)

1. Opprett et nytt prosjekt eller en egen assistent i KI-verktøyet (se tabellen nedenfor).
2. Lim inn startinstruksen i feltet for instruksjoner.
3. Last opp alle filene i pakken unntatt `LESMEG.md` som kunnskap eller filer. Systeminstruksen skal også lastes opp.
4. Start en ny samtale.

### Alternativ 2: Rett i chatten

1. Åpne en ny samtale.
2. Last opp alle filene i pakken unntatt `LESMEG.md` i samme melding.
3. Lim inn startinstruksen som meldingstekst, og send.
4. Gjenta dette for hver nye samtale. Filene huskes ikke mellom samtaler.

Vanlige samtaler uten prosjekt kan ha problemer med å lese så store filer. Fungerer det dårlig, bruk alternativ 1.

### Hvor gjør jeg dette i mitt verktøy?

| KI-verktøy | Bruk | Startinstruksen limes inn i | Filene lastes opp som |
| :--- | :--- | :--- | :--- |
| Claude | Prosjekt | Prosjektinstruksjoner | Prosjektkunnskap |
| ChatGPT | Prosjekt eller egen GPT | Instruksjoner | Filer (prosjekt) eller kunnskap (GPT) |
| Microsoft 365 Copilot | Agent | Instruksjoner | Kunnskap (inntil 20 filer; krever Microsoft 365 Copilot-lisens) |
| Gemini | Gem | Instruksjoner | Kunnskap (inntil 10 filer) |

Tabellen gjelder per november 2026. Verktøyene endres ofte, så sjekk verktøyets egen dokumentasjon hvis noe ser annerledes ut.

### Valg av modell

Standardmodellen i verktøyet holder. Slå ikke på dyp resonnering («thinking») eller dyp research. Det tar lang tid uten å gi bedre analyser.

## 4. Slik starter du

Send en kort melding, for eksempel «Hei» eller «Hva kan du hjelpe meg med?». Bruker du alternativ 2, er startinstruksen den første meldingen.

Assistenten svarer med en kort introduksjon: hva den kan hjelpe med, hvilke kilder den har tilgang til og hva en analyse inneholder. Sjekk at den bekrefter at de fire påkrevde filene er tilgjengelige. Mangler noe, laster du opp filen på nytt.

## 5. Slik legger du inn egne dokumenter

Assistenten blir først nyttig når den får ditt eget materiale å arbeide med.

1. Last opp dokumentene dine i samtalen, for eksempel casebeskrivelse, prosjektbeskrivelse, behovsanalyse, kravliste, beskrivelse av dagens situasjon eller effektmål.
2. Skriv i samme melding hva du vil ha hjelp til, for eksempel:
    - «Lag en full arkitekturanalyse av caset» (analyse)
    - «La oss drøfte dette caset» (drøfting)
    - «Hvilke fellesløsninger kan dekke behov X?» (spørsmål eller drøfting)

    Sier du ikke hva du vil, tolker assistenten opplastet dokumentasjon som en bestilling av full analyse, eller spør deg først.

3. Nevn gjerne egne løsninger, fagsystemer, standarder eller plattformer i domenet ditt. Assistenten tar bare med slike domeneressurser når de er nevnt i materialet ditt.

### Kontekst fra eget program eller domene

Arbeider du i et program, et prosjekt eller et domene med felles rammer, kan du laste opp en egen kontekstfil sammen med casen, for eksempel en beskrivelse av målbilde, aktører, prinsipper og løsninger i domenet. Assistenten bruker den som en del av din dokumentasjon. Uten slik kontekst vurderes caset bare opp mot det nasjonale kunnskapsgrunnlaget, og viktige forutsetninger i domenet kan bli oversett.

Last opp både kontekstfilen og casen før du ber om analyse eller drøfting, og si hvordan kontekstfilen skal brukes. For eksempel: «Her er konteksten for programmet vårt og casebeskrivelsen. Bruk kontekstfilen som grunnlag og lag en arkitekturanalyse av caset.»

## 6. Tips

- Jo mer konkret beskrivelsen er (mål, behov, aktører, krav, dagens situasjon), jo bedre blir analysen. Er beskrivelsen for overordnet, stiller assistenten 1–3 oppfølgingsspørsmål før den analyserer.
- Prosjekter og kunnskapsbaser søker ofte i filene i stedet for å lese alt. Mangler noe i et svar, kan du be assistenten sjekke en bestemt kapabilitet, fellesløsning eller et bestemt datasett.
- Følger ikke assistenten arbeidsmåten eller disposisjonen, kan du be den lese systeminstruksen på nytt.
- Etter en analyse kan du korrigere behov, effektmål eller antagelser. Assistenten kjører da analysen på nytt fra delen som berøres.
- Vil du ha analysen som samlet dokument (Word, PDF eller Markdown), ber du om det til slutt.
- Les alltid resultatet kritisk. Analysen er en foreløpig vurdering og et innspill til videre arbeid, ikke et vedtak.

## 7. Husk

- Følg virksomhetens retningslinjer for bruk av KI-verktøy.
- Ikke last opp personopplysninger, taushetsbelagt eller gradert informasjon med mindre KI-verktøyet ditt er godkjent for det i virksomheten din.
- Kunnskapsgrunnlaget oppdateres jevnlig. Siste versjon av oppsettpakken finner du på <https://digdir.github.io/nasjonal-arkitektur/arkitekturassistent/>.
