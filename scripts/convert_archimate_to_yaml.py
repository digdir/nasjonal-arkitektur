import xml.etree.ElementTree as ET
import yaml
import sys
import argparse

def parse_archimate(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define namespaces to handle them correctly or strip them
    # ElementTree adds the namespace URI in curly braces e.g., {http://www.archimatetool.com/archimate}model
    ns_map = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

    def get_tag_name(elem):
        return elem.tag.split('}')[-1]

    data = {
        'model': {
            'id': root.get('id', ''),
            'name': root.get('name', ''),
            'version': root.get('version', '')
        },
        'elements': {},
        'relationships': {},
        'views': {}
    }

    def process_element(elem, current_path):
        tag = get_tag_name(elem)
        
        if tag == 'folder':
            new_path = current_path + [elem.get('name', '')]
            for child in elem:
                process_element(child, new_path)
        elif tag == 'element':
            xsi_type = elem.get(f"{{{ns_map['xsi']}}}type", '')
            element_id = elem.get('id')
            
            # Extract common child data
            doc = ''
            properties = {}
            for child in elem:
                child_tag = get_tag_name(child)
                if child_tag == 'documentation':
                    doc = child.text if child.text else ''
                elif child_tag == 'property':
                    properties[child.get('key')] = child.get('value')
            
            if 'Relationship' in xsi_type:
                data['relationships'][element_id] = {
                    'type': xsi_type.split(':')[-1] if ':' in xsi_type else xsi_type,
                    'name': elem.get('name', ''),
                    'source_id': elem.get('source', ''),
                    'target_id': elem.get('target', ''),
                    'documentation': doc,
                    'properties': properties
                }
            elif 'DiagramModel' in xsi_type:
                # Process view
                view_data = {
                    'type': xsi_type.split(':')[-1] if ':' in xsi_type else xsi_type,
                    'name': elem.get('name', ''),
                    'documentation': doc,
                    'properties': properties,
                    'nodes': {},
                    'connections': {}
                }
                
                def process_view_child(view_child):
                    vc_tag = get_tag_name(view_child)
                    if vc_tag == 'child':
                        node_id = view_child.get('id')
                        node_data = {
                            'type': view_child.get(f"{{{ns_map['xsi']}}}type", '').split(':')[-1],
                            'archimate_element_id': view_child.get('archimateElement', ''),
                            'bounds': {}
                        }
                        for b_child in view_child:
                            bc_tag = get_tag_name(b_child)
                            if bc_tag == 'bounds':
                                node_data['bounds'] = {
                                    'x': b_child.get('x'),
                                    'y': b_child.get('y'),
                                    'width': b_child.get('width'),
                                    'height': b_child.get('height')
                                }
                            elif bc_tag == 'sourceConnection':
                                conn_id = b_child.get('id')
                                view_data['connections'][conn_id] = {
                                    'type': b_child.get(f"{{{ns_map['xsi']}}}type", '').split(':')[-1],
                                    'relationship_id': b_child.get('relationship', ''),
                                    'source_node': b_child.get('source', ''),
                                    'target_node': b_child.get('target', '')
                                }
                        view_data['nodes'][node_id] = node_data
                        
                        # recursively process children of view_child (nested objects in views)
                        for b_child in view_child:
                            if get_tag_name(b_child) == 'child':
                                process_view_child(b_child)
                
                for child in elem:
                    process_view_child(child)
                
                data['views'][element_id] = view_data
            else:
                # Normal element
                data['elements'][element_id] = {
                    'type': xsi_type.split(':')[-1] if ':' in xsi_type else xsi_type,
                    'name': elem.get('name', ''),
                    'documentation': doc,
                    'properties': properties,
                    'folder_path': current_path
                }
        else:
            # Other root-level items or unknown
            pass

    for child in root:
        process_element(child, [])

    return data

def main():
    parser = argparse.ArgumentParser(description="Convert ArchiMate to YAML")
    parser.add_argument("input_file", help="Path to the .archimate file")
    parser.add_argument("output_file", help="Path to the output .yaml file")
    args = parser.parse_args()

    print(f"Reading from {args.input_file}...")
    data = parse_archimate(args.input_file)
    
    print(f"Writing to {args.output_file}...")
    with open(args.output_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print("Done!")

if __name__ == "__main__":
    main()
