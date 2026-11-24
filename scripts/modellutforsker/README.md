# Modellutforsker for Nasjonal arkitektur

Modellutforskeren er én selvstendig HTML-fil som gjør hele Archi-modellen navigerbar:
nettverksgraf, kapabilitetskart, diagrammene fra Archi, mål og prinsipper, og en katalog
over alle elementer og relasjoner. Filen bygges fra `data/nasjonal-arkitektur.yaml`, så den
alltid viser samme innhold som modellen.

## Innhold

| Fil | Hva den gjør |
|---|---|
| `build_modellutforsker.py` | Leser YAML-filen og skriver ferdig HTML til `docs/modellutforsker/index.html` |
| `template.html` | Utseende og logikk. Dataene settes inn der det står `__NA_DATA__` |

## Bygging

Modellutforskeren bygges av `python bygg_lokalt.py`, etter at YAML-filen er laget fra den
nyeste modellen i `model/`. Skriptet kan også kjøres alene fra rotmappen i repoet:

```bash
python scripts/modellutforsker/build_modellutforsker.py
```

Valget `--no-date` fjerner genereringsdatoen i toppen. Da endres filen bare når modellen endres.

Skriptet forventer YAML med nøklene `model`, `elements`, `relationships` og `views`. Koblinger
i diagrammene som mangler relasjons-ID kobles til riktig relasjon ved å matche kilde- og
målelement.

`docs/modellutforsker/index.html` overskrives ved hver bygging og skal ikke redigeres.

## Publisering

Utforskeren publiseres som en del av nettstedet på to måter:

- Innebygd i siden `modellutforsker-visning.md` (mal i `templates/`), med en iframe. Da viser
  utforskeren en knapp for å åpne den i egen fane, i tillegg til fullskjermknappen.
- Alene på adressen `…/modellutforsker/`, som det lenkes til fra modellsiden.

Startvisningen velges med adressen:

| Adresse | Viser |
|---|---|
| `#nettverk` | Nettverksgrafen (standard) |
| `#kart` | Kapabilitetskartet |
| `#diagrammer`, `#diagram-1` til `#diagram-6` | Diagrammene fra Archi |
| `#motivasjon` | Mål og prinsipper |
| `#katalog` | Katalogen |
| `#id-...` | Et bestemt element, med detaljpanelet åpent |

Utforskeren henter d3 fra cdnjs og skrifttypen fra Google Fonts.

## Endre utseende eller oppførsel

Gjør endringene i `template.html` og kjør byggingen på nytt. Rør ikke linjen
`const DATA = __NA_DATA__;`, den byttes ut med modellinnholdet ved bygging.
