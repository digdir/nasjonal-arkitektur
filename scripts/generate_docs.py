import yaml
import os
import re
from PIL import Image, ImageDraw, ImageFont

def get_color(el_type):
    el_type = el_type.lower()
    if 'capability' in el_type or 'resource' in el_type or 'courseofaction' in el_type:
        return '#F5DEAA' # Strategy / Capability
    elif 'business' in el_type:
        return '#FFFFB5'
    elif 'application' in el_type:
        return '#B5FFFF'
    elif 'technology' in el_type or 'node' in el_type or 'device' in el_type:
        return '#C9E7B7'
    elif 'motivation' in el_type or 'goal' in el_type or 'principle' in el_type or 'requirement' in el_type or 'outcome' in el_type:
        return '#CCCCFF'
    elif 'note' in el_type:
        return '#FFFFFF'
    else:
        return '#EFEFEF'

def draw_view(view_name, view_data, elements, docs_dir):
    nodes = view_data.get('nodes', {})
    connections = view_data.get('connections', {})
    
    # 1. Compute absolute bounds for all nodes
    abs_bounds = {}
    
    def get_abs(node_id):
        if node_id in abs_bounds:
            return abs_bounds[node_id]
        
        node = nodes.get(node_id)
        if not node: return None
        bounds = node.get('bounds', {})
        if not bounds:
            return None
            
        x = int(bounds.get('x', 0) or 0)
        y = int(bounds.get('y', 0) or 0)
        w = int(bounds.get('width', 100) or 100)
        h = int(bounds.get('height', 50) or 50)
        
        parent_id = node.get('parent_node_id')
        if parent_id and parent_id in nodes:
            res = get_abs(parent_id)
            if res:
                px, py, _, _ = res
                x += px
                y += py
            
        abs_bounds[node_id] = (x, y, w, h)
        return (x, y, w, h)
        
    for nid in nodes.keys():
        get_abs(nid)
        
    if not abs_bounds:
        return None
        
    # 2. Determine image size
    min_x = min(b[0] for b in abs_bounds.values())
    min_y = min(b[1] for b in abs_bounds.values())
    max_x = max(b[0] + b[2] for b in abs_bounds.values())
    max_y = max(b[1] + b[3] for b in abs_bounds.values())
    
    # Add padding
    pad = 50
    width = max_x - min_x + (pad * 2)
    height = max_y - min_y + (pad * 2)
    
    # To avoid huge images if something is wrong
    if width > 8000 or height > 8000:
        width, height = min(width, 8000), min(height, 8000)
    
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.load_default()
    except:
        font = None

    # 3. Draw connections
    for c_id, conn in connections.items():
        src = conn.get('source_node')
        tgt = conn.get('target_node')
        if src in abs_bounds and tgt in abs_bounds:
            sx, sy, sw, sh = abs_bounds[src]
            tx, ty, tw, th = abs_bounds[tgt]
            start = (sx + sw//2 - min_x + pad, sy + sh//2 - min_y + pad)
            end = (tx + tw//2 - min_x + pad, ty + th//2 - min_y + pad)
            draw.line([start, end], fill='black', width=2)
            
    # 4. Draw nodes (sort by area descending so parents are drawn before children)
    sorted_nodes = sorted(abs_bounds.keys(), key=lambda n: abs_bounds[n][2] * abs_bounds[n][3], reverse=True)
    
    for nid in sorted_nodes:
        x, y, w, h = abs_bounds[nid]
        node = nodes[nid]
        el_id = node.get('archimate_element_id')
        el_type = node.get('type', '')
        
        name = ""
        if el_id and el_id in elements:
            name = elements[el_id].get('name', '')
            el_type = elements[el_id].get('type', el_type)
            
        color = get_color(el_type)
        
        rect_x0 = x - min_x + pad
        rect_y0 = y - min_y + pad
        rect_x1 = rect_x0 + w
        rect_y1 = rect_y0 + h
        
        draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=color, outline='black', width=1)
        
        if name:
            words = name.split()
            lines = []
            curr_line = []
            for word in words:
                curr_line.append(word)
                if len(" ".join(curr_line)) > 15:
                    lines.append(" ".join(curr_line))
                    curr_line = []
            if curr_line:
                lines.append(" ".join(curr_line))
                
            text = "\n".join(lines)
            if font:
                draw.text((rect_x0 + 5, rect_y0 + 5), text, fill='black', font=font)
            
    safe_name = re.sub(r'[^a-zA-Z0-9_\- ]', '', view_name).strip()
    img_path = os.path.join(docs_dir, 'images', f"{safe_name}.png")
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    img.save(img_path)
    return f"images/{safe_name}.png"

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
        
        img_rel_path = draw_view(safe_name, view_data, elements, docs_dir)
        
        md_path = os.path.join(docs_dir, f"{safe_name}.md")
        view_files.append((v_name, f"{safe_name}.md"))
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {v_name}\n\n")
            if img_rel_path:
                f.write(f"![{v_name}]({img_rel_path})\n\n")
                
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
            
        f.write("## Last ned filer\n\n")
        f.write("Her kan du laste ned selve arkitekturmodellen i ulike formater:\n\n")
        f.write("- **[ArchiMate-fil](Nasjonal%20Arkitektur%20kapabilitetsmodell.archimate)**: Originalmodellen. Kan åpnes i [Archi](https://www.archimatetool.com/) eller andre verktøy som støtter ArchiMate.\n")
        f.write("- **[YAML-fil](nasjonal-arkitektur.yaml)**: En strukturert data-representasjon av modellen, ypperlig for analyse, maskinell lesing og KI-agenter.\n\n")

        f.write("## Utforsk modellen\n\n")
        f.write("Arkitekturen er beskrevet gjennom følgende visuelle views:\n\n")
        
        view_files.sort(key=lambda x: x[0])
        for v_name, v_file in view_files:
            f.write(f"- [{v_name}]({v_file})\n")

    print(f"Generated {len(view_files)} view documents with PNGs in {docs_dir}")

if __name__ == '__main__':
    generate_markdown('data/nasjonal-arkitektur.yaml', 'docs')
