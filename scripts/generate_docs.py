import yaml
import os
import re
import shutil
import glob

def find_exported_image(view_id, html_export_dir='model/html-export'):
    """Find the exported image for a view in the ArchiMate HTML export."""
    # The images are typically located at model/html-export/id-*/images/{view_id}.png
    search_pattern = os.path.join(html_export_dir, '**', 'images', f"{view_id}.png")
    matches = glob.glob(search_pattern, recursive=True)
    if matches:
        return matches[0]
    return None

def copy_view_image(view_id, view_name, docs_dir):
    """Finds the exported image and copies it to docs/images/"""
    safe_name = re.sub(r'[^a-zA-Z0-9_\- ]', '', view_name).strip()
    img_path = os.path.join(docs_dir, 'images', f"{safe_name}.png")
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    
    src_img = find_exported_image(view_id)
    if src_img and os.path.exists(src_img):
        shutil.copy2(src_img, img_path)
        return f"images/{safe_name}.png"
    return None

def generate_markdown(yaml_file, docs_dir):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    elements = data.get('elements', {})
    views = data.get('views', {})
    
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(os.path.join(docs_dir, 'images'), exist_ok=True)
    
    view_files = []
    
    for view_id, view_data in views.items():
        v_name = view_data.get('name', 'Unnamed View')
        safe_name = re.sub(r'[^a-zA-Z0-9_\- ]', '', v_name).strip()
        
        # Copy image from HTML export instead of drawing it
        img_rel_path = copy_view_image(view_id, safe_name, docs_dir)
        
        md_path = os.path.join(docs_dir, f"{safe_name}.md")
        view_files.append((v_name, f"{safe_name}.md"))
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {v_name}\n\n")
            if img_rel_path:
                f.write(f"![{v_name}]({img_rel_path})\n\n")
            else:
                f.write(f"> *Kunne ikke finne bildet for viewet i HTML-eksporten.*\n\n")
                
            if v_name.startswith("01") or v_name.startswith("02"):
                f.write("## Kapabiliteter\n\n")
                
                nodes = view_data.get('nodes', {})
                children_map = {}
                for nid, ndata in nodes.items():
                    pid = ndata.get('parent_node_id')
                    if pid not in children_map:
                        children_map[pid] = []
                    children_map[pid].append(nid)
                    
                def print_hierarchy(node_id, indent=0):
                    ndata = nodes.get(node_id)
                    if not ndata: return
                    el_id = ndata.get('archimate_element_id')
                    
                    if el_id and el_id in elements:
                        el = elements[el_id]
                        name = el.get('name', '')
                        doc = el.get('documentation', '')
                        
                        def_text = ""
                        if doc:
                            for line in doc.splitlines():
                                if "Evne" in line:
                                    start = line.find("Evne")
                                    end = line.find(".", start)
                                    if end != -1:
                                        def_text = line[start:end+1]
                                    else:
                                        def_text = line[start:]
                                    break
                        
                        prefix = "  " * indent
                        f.write(f"{prefix}- **{name}**")
                        if def_text:
                            f.write(f" - *{def_text}*")
                        f.write("\n")
                        
                    for child_id in children_map.get(node_id, []):
                        print_hierarchy(child_id, indent + 1 if el_id else indent)
                        
                for root_id in children_map.get(None, []):
                    print_hierarchy(root_id, 0)
            else:
                f.write("## Elementer i viewet\n\n")
                el_ids = set()
                for nid, ndata in view_data.get('nodes', {}).items():
                    eid = ndata.get('archimate_element_id')
                    if eid and eid in elements:
                        el_ids.add(eid)
                        
                for eid in el_ids:
                    el = elements[eid]
                    f.write(f"### {el.get('name', '')}\n")
                    f.write(f"**Type:** {el.get('type', '')}\n\n")
                    if el.get('documentation'):
                        f.write(f"{el.get('documentation')}\n\n")
                    f.write("---\n\n")

    # Copy the entire HTML export to docs/archimate-report if it exists
    html_export_dir = 'model/html-export'
    report_dest = os.path.join(docs_dir, 'archimate-report')
    has_report = False
    if os.path.exists(html_export_dir):
        shutil.copytree(html_export_dir, report_dest, dirs_exist_ok=True)
        has_report = True
        
        # Inject "Tilbake til forside" link in the HTML report
        index_html_path = os.path.join(report_dest, 'index.html')
        if os.path.exists(index_html_path):
            with open(index_html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            nav_injection = """<ul class="nav navbar-nav navbar-left">
					<li><a href="../index.html"><span class="glyphicon glyphicon-home"></span> Tilbake til forside</a></li>
				</ul>
				<ul class="nav navbar-nav navbar-right">"""
            html_content = html_content.replace('<ul class="nav navbar-nav navbar-right">', nav_injection)
            
            with open(index_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

    readme_content = ""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        pass

    with open(os.path.join(docs_dir, 'index.md'), 'w', encoding='utf-8') as f:
        if readme_content:
            f.write(readme_content + "\n\n")
        else:
            f.write(f"# {data.get('model', {}).get('name', 'Nasjonal Arkitektur')}\n\n")
            f.write("Velkommen til dokumentasjonen for Nasjonal Arkitektur.\n\n")

    with open(os.path.join(docs_dir, 'modell.md'), 'w', encoding='utf-8') as f:
        f.write("# Rammeverksmodell for Nasjonal arkitektur\n\n")
        
        f.write("Denne siden presenterer den tekniske modelleringen av Nasjonal arkitektur, som er utformet i modelleringsverktøyet [Archi](https://www.archimatetool.com/). Denne strukturen fungerer som basis for dyptgående analyse og oversikt. Innholdet her retter seg spesielt mot målgrupper som har behov for innsikt på et mer teknisk og strukturelt nivå – enten målet er å gjenbruke arkitekturkonseptene i egne prosjekter, analysere sammenhenger, eller bygge videre på rammeverket.\n\n")
        
        f.write("## Last ned filer\n\n")
        f.write("Her kan du laste ned selve arkitekturmodellen i ulike formater:\n\n")
        f.write("- **[ArchiMate-fil](Nasjonal%20Arkitektur%20kapabilitetsmodell.archimate)**: Originalmodellen. Kan åpnes i [Archi](https://www.archimatetool.com/) eller andre verktøy som støtter ArchiMate.\n")
        f.write("- **[YAML-fil](nasjonal-arkitektur.yaml)**: En strukturert data-representasjon av modellen, ypperlig for analyse, maskinell lesing og KI-agenter.\n")
        f.write("- **[Turtle-fil](nasjonal-arkitektur.ttl)**: Turtle-representasjon av modellen (Archi-xml til RDF Turtle), basert på [archimate-RDF-vocabular](https://htmlpreview.github.io/?https://github.com/AlbertoDMendoza/archimate_ontology/blob/main/archimate.html). En strukturert representasjon av modellen i RDF Turtle (lenkede data), egnet for resonnering, analyse, maskinell lesing og KI-agenter.\n\n")

        f.write("## Utforsk modell\n\n")
        
        if has_report:
            f.write("Du kan se HTML-rapporten generert fra ArchiMate her:\n")
            f.write("- **[Åpne interaktiv ArchiMate-rapport](archimate-report/index.html)**\n\n")

        f.write("Arkitekturen er beskrevet gjennom følgende visuelle views:\n\n")
        
        view_files.sort(key=lambda x: x[0])
        for v_name, v_file in view_files:
            f.write(f"- [{v_name}]({v_file})\n")

    print(f"Generated {len(view_files)} view documents with HTML-exported PNGs in {docs_dir}")

if __name__ == '__main__':
    generate_markdown('data/nasjonal-arkitektur.yaml', 'docs')
