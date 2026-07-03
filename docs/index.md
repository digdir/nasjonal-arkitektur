# Nasjonal arkitektur for felles digitalt økosystem

## Innledning

Dette er et tiltak i regjeringens digitaliseringsstrategi. Målet er å sikre et velfungerende felles digitalt økosystem for effektiv samhandling og sammenhengende tjenesteutvikling i offentlig sektor. Tiltaket ledes av Digitaliseringsdirektoratet (Digdir) i tett samarbeid med KS.

Nasjonal arkitektur refererer til de overordnede rammeverkene, standardene, prinsippene og referansearkitekturene som bestemmer hvordan digitale løsninger skal bygges og samhandle på tvers av sektorer og forvaltningsnivåer.  Mens sektorene har egne tilpassede arkitekturer, sørger den nasjonale arkitekturen for at forvaltningen fremstår helhetlig og løser oppgaver effektivt på tvers.

## Metode for beskrivelse av Nasjonal arkitektur

Nasjonal arkitektur skal bidra til å beskrive, utvikle og samordne felles økosystem for digital samhandling. For å gjøre dette på en strukturert måte benyttes kapabilitetskart og kapabilitetsmodellering som metode.

En kapabilitet beskriver hva økosystemet, en sektor, en virksomhet eller et domene må kunne gjøre for å skape verdi. Kapabiliteter beskriver evner på et løsningsuavhengig nivå. De sier ikke hvilken organisasjon, løsning eller teknologi som skal utføre oppgaven, men tydeliggjør hvilke evner som må være til stede for å nå mål, realisere effektmål og understøtte sammenhengende tjenester.

Kapabilitetsmodellen gir dermed et stabilt språk for å beskrive behov på tvers av organisatoriske, teknologiske og sektorvise grenser. Dette er viktig fordi felles økosystem består av mange aktører, løsninger, regelverk, data, standarder og styringsstrukturer. Ved å beskrive hva økosystemet må kunne gjøre, før man beskriver hvordan det skal gjøres, blir det enklere å se sammenhenger, overlapp, mangler og avhengigheter.

Ressurser brukes i modellen for å vise hva som realiserer eller understøtter kapabilitetene. En ressurs kan være en fellesløsning, standard, veiledning, datasett, informasjonsmodell, samhandlingsarena, avtale, finansieringsmekanisme, juridisk rammeverk, kompetansemiljø eller annen byggekloss. Mens kapabiliteter beskriver evnene som trengs, beskriver ressursene hvilke konkrete byggeklosser som finnes eller må utvikles for å gjøre evnene reelle.

Koblingen mellom kapabiliteter og ressurser gjør modellen egnet til analyse. Den kan brukes til å vurdere hvilke kapabiliteter som er godt dekket, hvilke som mangler nødvendige ressurser, hvilke ressurser som brukes på tvers, og hvor det finnes overlapp eller gap. Dette gir grunnlag for å prioritere tiltak, vurdere modenhet og se om dagens arkitektur er tilstrekkelig for å nå ønskede effekter.

Kapabilitetsmodellen er også egnet til å koble nasjonalt og domenespesifikt nivå. Nasjonal arkitektur beskriver generiske og tverrgående kapabiliteter som er relevante for felles økosystem. Domener, sektorer og virksomheter kan konkretisere disse gjennom egne domenekapabiliteter og domeneressurser. På den måten kan modellen gi felles retning uten å måtte beskrive alle detaljer i alle sektorer eller virksomheter.

Metoden gjør det mulig å bruke Nasjonal arkitektur både som oversikt, analysegrunnlag og styringsverktøy. Den kan brukes til å:

- beskrive hvilke evner som er nødvendige i felles økosystem
- vise hvilke ressurser som understøtter kapabilitetene
- identifisere gap mellom dagens situasjon og ønsket situasjon
- vurdere dekningsgrad, modenhet og egnethet
- prioritere konkrete tiltak
- koble tiltak til mål, effektmål og prinsipper
- støtte samordning på tvers av sektorer, virksomheter og domener

Kapabilitetsmodellen er derfor ikke et veikart over enkeltprosjekter eller en katalog over alle løsninger. Den er et felles arkitekturfaglig rammeverk for å forstå hva økosystemet må kunne gjøre, hvilke byggeklosser som finnes, hvor det er mangler, og hvilke tiltak som kan bidra til å utvikle en mer helhetlig og sammenhengende digital offentlig sektor.

## Hva består det felles økosystemet av?

Det realiserte økosystemet består av konkrete ressurser som kan benyttes og gjenbrukes på tvers av aktørene. Ulike typer ressurser er:

- Gjenbrukbare løsninger
- Standarder og veiledninger
- Samhandlingsarenaer og organisering
- Økonomiske og juridiske rammer og virkemidler

## Oversikt over ressurser i felles økosystem

Det er et pågående arbeid i tiltaket å samle inn og publisere oversikt over felles ressurser. For å få oversikt arbeides det med å få på plass en kartleggingsmetode som er konsistent.

Foreløpig er dette lagt ut på følgende side (prototype):

- [Oversikt over felles ressurser](https://suphiro-arch.github.io/NA-kunnskap)

## Nasjonal arkitektur modell

Tiltaket har utviklet en modell som utgangspunkt for å beskrive innholdet og oppbygging av nasjonal arkitektur. Fokuset er på samhandlingsevner i felles økosystem, og arbeidet er basert på [Rammeverk for digital samhandling](https://www.digdir.no/digital-samhandling/rammeverk-digital-samhandling/2148).

Modellert i Archimate (verktøy Archi), og representert i .archimate format.
Modellen er også representert i YAML, for mer effektiv bruk til analyse etc.
Disse kan lastes ned.

Konvertering fra .archimate til .yaml gjøres i et eget script (Python).

Modellen består av følgende elementer:

- **Metamodell**: Modellen for Nasjonal arkitektur viser kjernebegrepene i metamodellen for Nasjonal arkitektur og hvordan kapabiliteter, ressurser, tiltak, gap, mål og effektmål henger sammen.
- **Kapabilitetskart**: Kapabilitetskartet for Nasjonal arkitektur, organisert i tre nivåer:
    - **Nivå 1: Overordnet kapabilitet** beskriver den samlede evnen Nasjonal arkitektur skal bidra til i felles økosystem.
    - **Nivå 2: Hovedkapabilitet** beskriver brede, strategiske kapabilitetsområder som strukturerer modellen.
    - **Nivå 3: Underkapabilitet** beskriver mer konkrete og operasjonelle evner som kan vurderes, forbedres og kobles til ressurser, tiltak, gap og effektmål.
- **Overordnete arkitekturprinsipper**: Overordnete arkitekturprinsipper for offentlig sektor og relasjon til kapabilitetene.
- **Ressurser og løsninger**: Hvordan ressurser og løsninger er knyttet til kapabilitetene. NB! Selve oversikten og listen over ressurser og løsninger finnes på egen side: [Oversikt over felles ressurser](https://suphiro-arch.github.io/NA-kunnskap)
- **Mål i Digitaliseringsstrategien**: Mål som er direkte relevante for kapabilitetene.
- **EIF lagmodell**: European Interoperability Framework (EIF), felles rammeverk for digital samhandling.

## Nasjonal arkitektur kapabilitetskart

Dette er den "viktigste" delen av modellen, sammen med oversikt og relasjon til de faktiske ressurser som innehar kapabiliteter som trengs for å dekke mål og behov i faktiske digitaliseringstiltak. Det er definert 3 nivåer av kapabiliteter inkludert definisjon og dokumentasjon (dokumentasjon forbedres pågående)

***

**Kontakt**: [Nasjonal arkitektur](mailto:nasjonalarkitektur@digdir.no)

**Til GitHub**: [Nasjonal arkitektur på GitHub](https://github.com/digdir/nasjonal-arkitektur)




<small>Sist oppdatert: 3. juli 2026</small>
