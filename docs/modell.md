# Dokumentasjon av Nasjonal arkitektur modell

## Innledning

Denne siden presenterer den tekniske modelleringen av Nasjonal arkitektur, som er utformet i modelleringsverktøyet [Archi](https://www.archimatetool.com/). Denne strukturen fungerer som basis for dyptgående analyse og oversikt. Innholdet her retter seg spesielt mot målgrupper som har behov for innsikt på et mer teknisk og strukturelt nivå – enten målet er å gjenbruke arkitekturkonseptene i egne prosjekter, analysere sammenhenger, eller bygge videre på rammeverket.

Nasjonal arkitektur skal være et levende, maskinlesbart og strategisk verktøy, og skal kunne knyttes til andre relevante datakilder. I den sammenheng er det viktig at datagrunnlaget kan benyttes og tilrettelegges for ulike analyser ved hjelp av KI. Det er ulike måter å dekke et slikt behov, men vi ønsker å etablere den som en Kunnskapsgraf (Knowledge Graph), les mer om dette her:

- [Nasjonal arkitektur som Kunnskapsgraf](kunnskapsgraf-maal.md)

## Last ned filer

Her kan du laste ned selve arkitekturmodellen i ulike formater:

<style>
  .md-typeset table th, .md-typeset table td {
    border: 1px solid var(--md-typeset-table-color, #e0e0e0);
  }
</style>

| Filformat                                                             | Beskrivelse                                                                                                                                                                                                                                                                          |
| :-------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[ArchiMate](Nasjonal%20Arkitektur%20kapabilitetsmodell.archimate)** | Originalmodellen. Kan åpnes i [Archi](https://www.archimatetool.com/) eller andre verktøy som støtter ArchiMate. |
| **[YAML](nasjonal-arkitektur.yaml)**                                  | En strukturert data-representasjon av modellen, egnet for analyse, maskinell lesing og KI-agenter.                                                                                                                                                                                   |
| **[Turtle](nasjonal-arkitektur.ttl)**                                 | Turtle-representasjon av modellen (Archi-xml til RDF Turtle), basert på [archimate-RDF-vocabular](https://htmlpreview.github.io/?https://github.com/AlbertoDMendoza/archimate_ontology/blob/main/archimate.html). En strukturert representasjon av modellen i RDF Turtle (lenkede data), egnet for resonnering, analyse, maskinell lesing og KI-agenter. |

## Utforsk modell


Du kan se HTML-rapporten generert fra Archi her:
- **[Åpne interaktiv Archi-rapport](interaktiv-modell.md)**

> **Merk:** Denne dokumentasjonen skal forbedres! Inntil videre kan du få tilgang til all dokumentasjon ved å **[Åpne interaktiv Archi-rapport](interaktiv-modell.md)**.

Arkitekturen er beskrevet gjennom følgende visuelle views:

### [001-Metamodell](001-Metamodell.md)

Modellen for Nasjonal arkitektur viser kjernebegrepene i metamodellen for Nasjonal arkitektur og hvordan kapabiliteter, ressurser, tiltak, gap, mål og effektmål henger sammen.

### [01-Nasjonal arkitektur - Hovedkapabiliteter](01-Nasjonal arkitektur - Hovedkapabiliteter.md)

Denne viser Nivå 1 til Nivå 2 av kapabiliteter i Nasjonal arkitektur:

### [02-Nasjonal Arkitektur - Kapabilitetskart alle nivåer](02-Nasjonal Arkitektur - Kapabilitetskart alle niver.md)

Den konkrete kapabilitetsmodellen for Nasjonal arkitektur er organisert i tre nivåer, denne viser alle nivåene:

### [03-Arkitekturprinsipper og NA](03-Arkitekturprinsipper og NA.md)

Denne viser (grovt) relasjonene mellom nasjonale arkitekturprinsipper og Nasjonal arkitektur hovedkapabiliteter (Nivå 2)

### [04-Digitaliseringsstrategiens mål og NA](04-Digitaliseringsstrategiens ml og NA.md)

Digitaliseringsstrategiens mest relevante mål for Nasjonal arkitektur 

### [05-EIF lagmodell](05-EIF lagmodell.md)

EIF lagmodell fra EU, rammeverk for digital samhandling.



<small>Sist oppdatert: 16. juli 2026</small>
