"""Bygger oppsettpakken for Arkitekturassistenten.

Pakken består av filene i arkitekturassistent/ og masterfilen
data/nasjonal-arkitektur.yaml, og skrives til
docs/arkitekturassistent-oppsettpakke.zip.

Plassholderen {{systeminstruks_fil}} i LESMEG.md erstattes med filnavnet til
systeminstruksen, slik at veiledningen alltid viser riktig versjon.

Zip-filen er deterministisk (sortert innhold og faste tidsstempler), slik at
en ny bygging uten endringer gir en identisk fil.

Hjelpefunksjonene her brukes også av generate_docs.py.
"""
import glob
import io
import os
import re
import sys
import zipfile

KILDEMAPPE = 'arkitekturassistent'
YAML_MASTER = os.path.join('data', 'nasjonal-arkitektur.yaml')
ZIP_FIL = os.path.join('docs', 'arkitekturassistent-oppsettpakke.zip')
ROTMAPPE_I_ZIP = 'arkitekturassistent'
LESMEG = 'LESMEG.md'

# Filer som alltid må finnes i kildemappen (i tillegg til systeminstruksen)
PAKREVDE_FILER = [LESMEG, 'na_ressursoversikt.md', 'Hent-ressurs-resultat-liten.csv']

# Filer som systemet kan legge igjen, og som ikke skal med i pakken
IGNORER = {'desktop.ini', 'thumbs.db', '.ds_store'}

# Fast tidsstempel for alle filer i zip-filen (gir identisk fil ved ny bygging)
FAST_TIDSPUNKT = (2020, 1, 1, 0, 0, 0)


class PakkeFeil(Exception):
    """Feil i innholdet i kildemappen."""


def finn_systeminstruks(mappe=KILDEMAPPE):
    """Returnerer filnavnet til systeminstruksen. Det skal finnes nøyaktig én."""
    treff = sorted(glob.glob(os.path.join(mappe, 'Systeminstruks-*.md')))
    if len(treff) != 1:
        navn = ', '.join(os.path.basename(t) for t in treff) or 'ingen'
        raise PakkeFeil(
            f"Fant {len(treff)} systeminstruks-filer i {mappe}/ ({navn}). "
            "Det skal være nøyaktig én fil som heter Systeminstruks-*.md. "
            "Fjern den gamle versjonen når du legger inn en ny."
        )
    return os.path.basename(treff[0])


def les_instruksversjon(mappe=KILDEMAPPE):
    """Leser versjonsnummeret fra linjen '**Versjon:** x' i systeminstruksen."""
    sti = os.path.join(mappe, finn_systeminstruks(mappe))
    with open(sti, 'r', encoding='utf-8') as f:
        for linje in f:
            m = re.match(r'\*\*Versjon:\*\*\s*(.+)', linje.strip())
            if m:
                return m.group(1).strip()
    return 'ukjent'


def les_startinstruks(mappe=KILDEMAPPE):
    """Henter startinstruksen (første ```text-blokk) fra LESMEG.md, med plassholdere fylt inn."""
    with open(os.path.join(mappe, LESMEG), 'r', encoding='utf-8') as f:
        tekst = f.read()
    m = re.search(r'```text\n(.*?)\n```', tekst, re.DOTALL)
    if not m:
        raise PakkeFeil(f"Fant ikke startinstruksen (en ```text-blokk) i {mappe}/{LESMEG}.")
    return fyll_inn(m.group(1).strip())


def plassholdere(mappe=KILDEMAPPE):
    """Verdiene som brukes for {{...}}-plassholdere i LESMEG.md og dokumentasjonen."""
    return {
        'systeminstruks_fil': finn_systeminstruks(mappe),
        'instruks_versjon': les_instruksversjon(mappe),
    }


def fyll_inn(tekst, verdier=None):
    """Erstatter {{navn}} med verdier. Stopper hvis en plassholder ikke fylles inn."""
    if verdier is None:
        verdier = plassholdere()
    for navn, verdi in verdier.items():
        tekst = tekst.replace('{{' + navn + '}}', verdi)
    rest = sorted(set(re.findall(r'\{\{\s*[\w-]+\s*\}\}', tekst)))
    if rest:
        raise PakkeFeil(f"Plassholdere som ikke ble fylt inn: {', '.join(rest)}")
    return tekst


def _filer_i_pakken():
    """Returnerer en sortert liste med (navn i pakken, kildesti)."""
    if not os.path.isdir(KILDEMAPPE):
        raise PakkeFeil(f"Finner ikke mappen {KILDEMAPPE}/.")

    finn_systeminstruks()  # kontrollerer at det finnes nøyaktig én
    mangler = [f for f in PAKREVDE_FILER if not os.path.isfile(os.path.join(KILDEMAPPE, f))]
    if mangler:
        raise PakkeFeil(f"Mangler påkrevde filer i {KILDEMAPPE}/: {', '.join(mangler)}")
    if not os.path.isfile(YAML_MASTER):
        raise PakkeFeil(f"Finner ikke {YAML_MASTER}. Kjør konverteringen fra ArchiMate først.")

    filer = []
    for navn in os.listdir(KILDEMAPPE):
        sti = os.path.join(KILDEMAPPE, navn)
        if not os.path.isfile(sti) or navn.startswith('.') or navn.lower() in IGNORER:
            continue
        if navn == os.path.basename(YAML_MASTER):
            raise PakkeFeil(
                f"{KILDEMAPPE}/{navn} skal ikke ligge i mappen. "
                f"YAML-filen hentes alltid fra {YAML_MASTER} ved bygging."
            )
        filer.append((navn, sti))
    filer.append((os.path.basename(YAML_MASTER), YAML_MASTER))
    return sorted(filer)


def bygg_pakke():
    verdier = plassholdere()
    buffer = io.BytesIO()
    filer = _filer_i_pakken()

    with zipfile.ZipFile(buffer, 'w') as zf:
        for navn, sti in filer:
            with open(sti, 'rb') as f:
                data = f.read()
            if navn == LESMEG:
                data = fyll_inn(data.decode('utf-8'), verdier).encode('utf-8')

            info = zipfile.ZipInfo(f"{ROTMAPPE_I_ZIP}/{navn}", date_time=FAST_TIDSPUNKT)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # Unix, slik at filrettighetene under tolkes likt overalt
            info.external_attr = 0o644 << 16
            zf.writestr(info, data, compresslevel=9)

    innhold = buffer.getvalue()
    os.makedirs(os.path.dirname(ZIP_FIL), exist_ok=True)

    uendret = False
    if os.path.isfile(ZIP_FIL):
        with open(ZIP_FIL, 'rb') as f:
            uendret = f.read() == innhold
    if not uendret:
        with open(ZIP_FIL, 'wb') as f:
            f.write(innhold)

    print(f"Oppsettpakke: {ZIP_FIL} ({len(innhold) / 1024 / 1024:.1f} MB, {len(filer)} filer, "
          f"systeminstruks {verdier['systeminstruks_fil']}, versjon {verdier['instruks_versjon']})"
          + (" (uendret)" if uendret else ""))
    for navn, _ in filer:
        print(f"  - {navn}")


if __name__ == '__main__':
    try:
        bygg_pakke()
    except PakkeFeil as e:
        print(f"Feil: {e}")
        sys.exit(1)
