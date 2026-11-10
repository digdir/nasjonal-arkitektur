import yaml
import os
import re
import shutil
import glob
import stat
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bygg_oppsettpakke import KILDEMAPPE, LESMEG, PakkeFeil, fyll_inn, les_startinstruks, plassholdere

MONTHS = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]

def remove_readonly(func, path, _exc_info):
    """Windows/OneDrive kan sette mapper som skrivebeskyttet, noe som stopper rmtree."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def modell_dato():
    """Datoen i filnavnet til den nyeste modellen i model/, f.eks. «28. oktober 2026»."""
    filer = sorted(glob.glob('model/*.archimate'))
    if filer:
        m = re.search(r'(\d{4})-(\d{2})-(\d{2})', os.path.basename(filer[-1]))
        if m:
            return f"{int(m.group(3))}. {MONTHS[int(m.group(2)) - 1]} {m.group(1)}"
    return "ukjent dato"

def generate_arkitekturassistent(docs_dir):
    """Lager sidene om Arkitekturassistenten: oversikt (fra mal) og veiledning (fra LESMEG.md)."""
    verdier = plassholdere()
    verdier['modell_dato'] = modell_dato()
    verdier['startinstruks'] = les_startinstruks()

    with open('templates/arkitekturassistent.md', 'r', encoding='utf-8') as f:
        oversikt = fyll_inn(f.read(), verdier)
    with open(os.path.join(docs_dir, 'arkitekturassistent.md'), 'w', encoding='utf-8') as f:
        f.write(oversikt)

    with open(os.path.join(KILDEMAPPE, LESMEG), 'r', encoding='utf-8') as f:
        veiledning = fyll_inn(f.read(), verdier)
    with open(os.path.join(docs_dir, 'arkitekturassistent-oppsett.md'), 'w', encoding='utf-8') as f:
        f.write(veiledning)

def generate_markdown(yaml_file, docs_dir):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(os.path.join(docs_dir, 'images'), exist_ok=True)

    # Sidene om Arkitekturassistenten lages først, slik at en feil i arkitekturassistent/
    # stopper byggingen før de andre sidene skrives om.
    try:
        generate_arkitekturassistent(docs_dir)
    except PakkeFeil as e:
        print(f"Feil i arkitekturassistent/: {e}")
        sys.exit(1)

    # Copy the entire HTML export to docs/archimate-report if it exists
    html_export_dir = 'model/html-export'
    report_dest = os.path.join(docs_dir, 'archimate-report')
    has_report = False
    if os.path.exists(html_export_dir):
        # Tøm målmappen først, slik at filer fra eldre eksporter ikke blir liggende igjen
        if os.path.exists(report_dest):
            shutil.rmtree(report_dest, onerror=remove_readonly)
        shutil.copytree(html_export_dir, report_dest)
        has_report = True
        
        # Skjul den originale Archi-headeren siden vi nå har MkDocs-header i iframe-en
        index_html_path = os.path.join(report_dest, 'index.html')
        if os.path.exists(index_html_path):
            with open(index_html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            html_content = html_content.replace('</head>', '<style>.ui-layout-north { display: none !important; }</style></head>')
            with open(index_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

    index_intro = ""
    try:
        with open('templates/index_intro.md', 'r', encoding='utf-8') as f:
            index_intro = f.read()
    except FileNotFoundError:
        pass

    with open(os.path.join(docs_dir, 'index.md'), 'w', encoding='utf-8') as f:
        if index_intro:
            f.write(index_intro + "\n\n")
        else:
            f.write(f"# {data.get('model', {}).get('name', 'Nasjonal Arkitektur')}\n\n")
            f.write("Velkommen til dokumentasjonen for Nasjonal Arkitektur.\n\n")

    modell_intro = ""
    try:
        with open('templates/modell_intro.md', 'r', encoding='utf-8') as f:
            modell_intro = f.read()
    except FileNotFoundError:
        pass

    with open(os.path.join(docs_dir, 'modell.md'), 'w', encoding='utf-8') as f:
        if modell_intro:
            f.write(modell_intro + "\n\n")
        else:
            f.write("# Rammeverksmodell for Nasjonal arkitektur\n\n")
            f.write("## Utforsk modell\n\n")
        
        if has_report:
            f.write("Du kan se HTML-rapporten generert fra Archi her:\n")
            f.write("- **[Åpne interaktiv Archi-rapport](interaktiv-modell.md)**\n\n")

        f.write("> **Merk:** Denne dokumentasjonen skal forbedres! Inntil videre kan du få tilgang til all dokumentasjon ved å **[Åpne interaktiv Archi-rapport](interaktiv-modell.md)**.\n\n")

    try:
        shutil.copy2('templates/kunnskapsgraf-maal.md', os.path.join(docs_dir, 'kunnskapsgraf-maal.md'))
    except FileNotFoundError:
        pass
        
    try:
        shutil.copy2('templates/ressurser.md', os.path.join(docs_dir, 'ressurser.md'))
    except FileNotFoundError:
        pass

    # Legg til "Sist oppdatert" nederst i alle genererte markdown-filer
    import datetime
    months = MONTHS
    now = datetime.datetime.now()
    date_str = f"{now.day}. {months[now.month - 1]} {now.year}"
    footer = f"\n\n<small>Sist oppdatert: {date_str}</small>\n"
    
    for md_file in glob.glob(os.path.join(docs_dir, '*.md')):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Fjern tidligere "Sist oppdatert"-tagger
        content = re.sub(r'\n*<small>Sist oppdatert:.*?</small>\n*', '', content)
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content + footer)

    print(f"Generated documentation in {docs_dir}")

if __name__ == '__main__':
    generate_markdown('data/nasjonal-arkitektur.yaml', 'docs')
