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
        v_doc = view_data.get('documentation', '')
        view_files.append((v_name, f"{safe_name}.md", v_doc))
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {v_name}\n\n")
            
            f.write("> **Merk:** Denne dokumentasjonen skal forbedres! Inntil videre kan du få tilgang til all dokumentasjon ved å **[Åpne interaktiv Archi-rapport](interaktiv-modell.md)**.\n\n")
            
            if img_rel_path:
                f.write(f"![{v_name}]({img_rel_path})\n\n")
            else:
                f.write(f"> *Kunne ikke finne bildet for viewet i HTML-eksporten.*\n\n")
                
            if v_doc:
                f.write(f"## Beskrivelse\n\n{v_doc}\n\n")
                
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
        f.write("Arkitekturen er beskrevet gjennom følgende visuelle views:\n\n")
        
        view_files.sort(key=lambda x: x[0])
        for v_name, v_file, v_doc in view_files:
            f.write(f"### [{v_name}]({v_file})\n\n")
            if v_doc:
                # Add a brief summary (first line/paragraph) if it exists
                summary = v_doc.split('\n')[0]
                f.write(f"{summary}\n\n")

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
    months = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
    now = datetime.datetime.now()
    date_str = f"{now.day}. {months[now.month - 1]} {now.year}"
    footer = f"\n\n<small>Sist oppdatert: {date_str}</small>\n"
    
    for md_file in glob.glob(os.path.join(docs_dir, '*.md')):
        with open(md_file, 'a', encoding='utf-8') as f:
            f.write(footer)

    print(f"Generated {len(view_files)} view documents with HTML-exported PNGs in {docs_dir}")

if __name__ == '__main__':
    generate_markdown('data/nasjonal-arkitektur.yaml', 'docs')
