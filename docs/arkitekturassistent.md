---
hide:
  - toc
---

# Arkitekturassistenten – KI-hjelp til ditt digitaliseringstiltak

Få hjelp av KI til å se hva prosjektet ditt kan gjenbruke av fellesløsninger og data, og hvilke tiltak som passer. Du setter assistenten opp selv, i ditt eget KI-verktøy, på få minutter.
{: .aa-lead }

Assistenten vurderer behov, prosjekter og dokumenter opp mot Nasjonal arkitektur for samhandling, foreslår tiltak og gir en foreløpig vurdering som prosjektleder og styringsgruppe kan bruke videre. Den er laget for arkitekter, prosjektledere og andre som arbeider med digitaliseringstiltak i offentlig sektor.

!!! info "Under arbeid"

    Digitaliseringsdirektoratet (Digdir) arbeider med å gjøre Arkitekturassistenten tilgjengelig som en brukervennlig KI-tjeneste og som en del av et fremtidig agentisk rammeverk. Inntil videre kan du kjøre den i ditt eget KI-verktøy, for eksempel Claude, ChatGPT, Microsoft 365 Copilot eller Gemini, slik det er beskrevet på denne siden.

## Slik fungerer det

<div class="aa-figur">
<section class="aa-panel" aria-labelledby="aa-maater">
<h3 id="aa-maater">Tre måter å bruke assistenten på</h3>
<div class="aa-modes">
<div class="aa-mode aa-dom"><span class="aa-tag">Spørsmål</span><h4>Spør assistenten</h4><p>Still spørsmål om kunnskapsgrunnlaget: kapabiliteter, prinsipper, fellesløsninger og datasett.</p><span class="aa-out">Du får et direkte svar fra kunnskapsgrunnlaget.</span></div>
<div class="aa-mode aa-kap"><span class="aa-tag">Drøfting</span><h4>Drøft et case</h4><p>Utvikle problemforståelsen i dialog. Assistenten svarer kort, utfordrer caset og stiller høyst ett spørsmål om gangen.</p><span class="aa-out">Du får skarpere problemforståelse og avklarte behov.</span></div>
<div class="aa-marrow"><svg aria-hidden="true" width="54" height="24" viewBox="0 0 54 24"><path d="M2 12 H46" stroke="currentColor" stroke-width="2.5" fill="none"/><path d="M44 5 L52 12 L44 19" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linejoin="round"/></svg><span>Be om full analyse: det som er avklart, blir grunnlaget</span></div>
<div class="aa-mode aa-eff"><span class="aa-tag">Analyse</span><h4>Analyser et case</h4><p>Full analyse i ett svar, fra behov til oppsummering for prosjektleder og styringsgruppe.</p><span class="aa-out">Du får en strukturert analyse, og kan be om et samlet dokument (Word, PDF eller Markdown).</span></div>
</div>
</section>
<section class="aa-panel" aria-labelledby="aa-analyse">
<h3 id="aa-analyse">Slik gjennomføres en analyse</h3>
<ol class="aa-flow">
<li class="aa-dom"><i>Grunnlag</i><h4>Du beskriver</h4><span>Beskrivelse, opplastede dokumenter eller en drøfting</span></li>
<li class="aa-eff"><i>Steg 1</i><h4>Behov og kapabiliteter</h4><span>Behov (også utledede og foreslåtte), effektmål, kapabiliteter og arkitekturprinsipper</span></li>
<li class="aa-eff"><i>Steg 2</i><h4>Ressurser og dekning</h4><span>Alle fellesressurser som er koblet til kapabilitetene, vurderes. Dekning per behov: hel, delvis eller mangler</span></li>
<li class="aa-eff"><i>Steg 3</i><h4>Datasett</h4><span>Datasett fra Felles datakatalog som kan gjenbrukes</span></li>
<li class="aa-kap"><i>Steg 4</i><h4>Forankring og tiltak</h4><span>Nasjonal forankring, hovedfunn, antagelser, to eller tre tiltak og nullalternativet</span></li>
<li class="aa-pri"><i>Steg 5</i><h4>Vurdering</h4><span>Tom evalueringsmal uten skår og en foreløpig vurdering</span></li>
<li class="aa-res"><i>Resultat</i><h4>Oppsummering</h4><span>Oppsummering for prosjektleder og styringsgruppe. Samlet dokument på forespørsel</span></li>
</ol>
</section>
<div class="aa-panel aa-facts">
<div><b>Gjenbruk først</b><span>Alle fellesressurser som er koblet til de aktuelle kapabilitetene, vurderes før et gap erklæres.</span></div>
<div><b>Bygger på kunnskapsgrunnlaget</b><span>Assistenten finner ikke på kapabiliteter, prinsipper eller fellesløsninger, og sier fra når en kilde mangler.</span></div>
<div><b>Du beslutter</b><span>Assistenten skårer ikke tiltakene. Evalueringsmalen fylles ut av prosjektet.</span></div>
</div>
</div>

## Last ned oppsettpakken

[Last ned oppsettpakken (zip)](arkitekturassistent-oppsettpakke.zip){ .md-button .md-button--primary }

Pakken inneholder systeminstruks versjon 2.1 og modellen for Nasjonal arkitektur per 3. november 2026.

| Fil | Innhold |
| :--- | :--- |
| `Systeminstruks-Arkitektur-assistenten-v2_1.md` | Systeminstruksen: rollen, arbeidsmåten og formatet på analysene |
| `nasjonal-arkitektur.yaml` | Kapabilitetskartet og arkitekturprinsippene i Nasjonal arkitektur |
| `na_ressursoversikt.md` | Fellesløsninger og fellesressurser |
| `Hent-ressurs-resultat-liten.csv` | Gjenbrukbare datasett fra Felles datakatalog (data.norge.no) |
| `Digitaliseringsrundskrivet.md` | Digitaliseringsrundskrivet (valgfri, brukes til nasjonal forankring) |
| `LESMEG.md` | Veiledning for oppsett og bruk |

## Kom i gang

1. Opprett et prosjekt eller en egen assistent i KI-verktøyet ditt, for eksempel et prosjekt i Claude eller ChatGPT, en agent i Microsoft 365 Copilot eller en Gem i Gemini.
2. Lim inn startinstruksen nedenfor i feltet for instruksjoner.
3. Last opp alle filene i pakken unntatt `LESMEG.md`, også systeminstruksen, og start en ny samtale.

```text
Du er Arkitekturassistenten. Les hele filen Systeminstruks-Arkitektur-assistenten-v2_1.md før du svarer, og følg instruksene i den gjennom hele samtalen. Bruk de andre opplastede filene som kunnskapsgrunnlag, slik systeminstruksen beskriver. Svar på norsk.
```

Les veiledningen [Oppsett og bruk](arkitekturassistent-oppsett.md) for detaljer per verktøy, hvordan du legger inn egne dokumenter og tips til bruk.

## Forbehold

- Analysene er foreløpige vurderinger og innspill til videre arbeid, ikke vedtak. Les alltid resultatet kritisk.
- Assistenten kjører i ditt eget KI-verktøy og på din egen lisens. Følg virksomhetens retningslinjer for bruk av KI-verktøy.
- Ikke last opp personopplysninger, taushetsbelagt eller gradert informasjon med mindre KI-verktøyet ditt er godkjent for det i virksomheten din.

**Tilbakemeldinger** tas gjerne imot på [nasjonalarkitektur@digdir.no](mailto:nasjonalarkitektur@digdir.no).


<small>Sist oppdatert: 10. november 2026</small>
