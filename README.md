# Nasjonal arkitektur for et felles digitalt økosystem

Dette er kildekoden og byggemiljøet for dokumentasjonen av [Nasjonal arkitektur](https://digdir.no/nasjonal-arkitektur).

## Om prosjektet

Dette repositoryet inneholder skript, konfigurasjon og kildedata (som eksporterte ArchiMate- og YAML-filer) som brukes til å bygge og publisere dokumentasjonen for rammeverksmodellen.

Dokumentasjonen publiseres ved hjelp av **MkDocs** (Material for MkDocs).
Selve dokumentasjonen finner du publisert på GitHub Pages for dette prosjektet.

## Hvordan bygge dokumentasjonen lokalt

For å generere Markdown-filene og bygge siden, kan du bruke Python-skriptet som ligger i rotmappen:

```bash
python bygg_lokalt.py
```

Dette vil:

1. Konvertere ArchiMate-modellen til YAML.
2. Konvertere modellen til Turtle (TTL).
3. Generere Markdown-dokumentasjon basert på YAML-filen og tekstmaler i `templates/`-mappen.
4. Kopiere nødvendige filer inn i `docs/`-mappen slik at MkDocs kan bruke dem.

For å se resultatet lokalt, kan du kjøre (krever at MkDocs er installert):

```bash
mkdocs serve
(eller: python -m mkdocs serve)
```

## Maler og innhold

Hvis du vil endre den statiske teksten på for eksempel forsiden eller introduksjonen til modell-siden, gjør du dette ved å endre Markdown-filene som ligger under mappen `templates/`. Endringer derfra vil automatisk bli bakt inn i dokumentasjonen neste gang den bygges.
