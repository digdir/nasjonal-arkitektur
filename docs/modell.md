# Rammeverksmodell for Nasjonal arkitektur

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

Arkitekturen er beskrevet gjennom følgende visuelle views:

- [001-Metamodell](001-Metamodell.md)
- [01-Nasjonal arkitektur - Hovedkapabiliteter](01-Nasjonal arkitektur - Hovedkapabiliteter.md)
- [02-Nasjonal Arkitektur - Kapabilitetskart alle nivåer](02-Nasjonal Arkitektur - Kapabilitetskart alle niver.md)
- [03-Arkitekturprinsipper og NA](03-Arkitekturprinsipper og NA.md)
- [04-Digitaliseringsstrategiens mål og NA](04-Digitaliseringsstrategiens ml og NA.md)
- [05-EIF lagmodell](05-EIF lagmodell.md)
