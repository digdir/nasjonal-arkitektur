import yaml
import os
from collections import defaultdict

def generate_markdown(yaml_file, docs_dir):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    elements = data.get('elements', {})
    
    # Group elements by type
    by_type = defaultdict(list)
    for el_id, el_data in elements.items():
        el_type = el_data.get('type', 'Unknown')
        by_type[el_type].append(el_data)
        
    # Create docs dir if not exists
    os.makedirs(docs_dir, exist_ok=True)
    
    # Generate index.md
    with open(os.path.join(docs_dir, 'index.md'), 'w', encoding='utf-8') as f:
        f.write(f"# {data.get('model', {}).get('name', 'Nasjonal Arkitektur')}\n\n")
        f.write("Velkommen til dokumentasjonen for Nasjonal Arkitektur.\n\n")
        f.write("## Innhold\n")
        for el_type in sorted(by_type.keys()):
            f.write(f"- [{el_type}]({el_type}.md)\n")
            
    # Generate a markdown file for each type
    for el_type, items in by_type.items():
        with open(os.path.join(docs_dir, f'{el_type}.md'), 'w', encoding='utf-8') as f:
            f.write(f"# {el_type}s\n\n")
            
            # Sort items by name
            items = sorted(items, key=lambda x: x.get('name', ''))
            
            for item in items:
                f.write(f"## {item.get('name', 'Uten navn')}\n\n")
                doc = item.get('documentation', '')
                if doc:
                    f.write(f"{doc}\n\n")
                
                props = item.get('properties', {})
                if props:
                    f.write("**Egenskaper:**\n\n")
                    for k, v in props.items():
                        f.write(f"- **{k}:** {v}\n")
                    f.write("\n")
                
                f.write("---\n\n")
                
    print(f"Generated {len(by_type)} markdown files in {docs_dir}")

if __name__ == '__main__':
    generate_markdown('data/nasjonal-arkitektur.yaml', 'docs')
