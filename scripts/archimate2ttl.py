#!/usr/bin/env python3
"""
Convert Archi .archimate XML to RDF Turtle using the ArchiMate ontology.
Base URI: https://data.digdir.no/nasjonal-arkitektur/
Ontology:  https://purl.org/archimate#

Relationships are represented as named individuals (Option B):
    na:<rel-id>
        a archimate:<RelType>, archimate:Relationship ;
        archimate:identifier "..." ;
        archimate:name "..."@nb ;        # if present
        archimate:source na:<source-id> ;
        archimate:target na:<target-id> .
"""

import sys
import xml.etree.ElementTree as ET
import re

if len(sys.argv) > 2:
    SRC = sys.argv[1]
    DST = sys.argv[2]
else:
    SRC = "Nasjonal Arkitektur kapabilitetsmodell-2026-05-28.archimate"
    DST = "nasjonal-arkitektur.ttl"

BASE  = "https://data.digdir.no/nasjonal-arkitektur/"
ONT   = "https://purl.org/archimate#"
XSI   = "http://www.w3.org/2001/XMLSchema-instance"

# Map ArchiMate relationship type names → ontology class names
# The ontology defines these as both owl:ObjectProperty AND owl:Class (Relationship subclass)
REL_CLASS_MAP = {
    "AssociationRelationship":    "AssociationRelationship",
    "AggregationRelationship":    "AggregationRelationship",
    "CompositionRelationship":    "CompositionRelationship",
    "RealizationRelationship":    "RealizationRelationship",
    "ServingRelationship":        "ServingRelationship",
    "AccessRelationship":         "AccessRelationship",
    "InfluenceRelationship":      "InfluenceRelationship",
    "TriggeringRelationship":     "TriggeringRelationship",
    "FlowRelationship":           "FlowRelationship",
    "SpecializationRelationship": "SpecializationRelationship",
    "AssignmentRelationship":     "AssignmentRelationship",
}

def xsi_type(elem):
    t = elem.get(f"{{{XSI}}}type", "")
    return t.replace("archimate:", "")

def escape_ttl(s):
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return s

def collect_all(root):
    elements = []
    def walk(node):
        for child in node:
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag == "element":
                elements.append(child)
            elif tag == "folder":
                walk(child)
    walk(root)
    return elements

def make_property_node(prop_id, key, value):
    """Render an archimate:Property blank node."""
    lines = []
    esc_key = escape_ttl(key)
    esc_val = escape_ttl(value)
    lines.append(f'na:{prop_id}')
    lines.append(f'    a archimate:Property ;')
    lines.append(f'    archimate:propertyKey "{esc_key}" ;')
    lines.append(f'    archimate:propertyValue "{esc_val}" .')
    return "\n".join(lines)

# ── Parse ────────────────────────────────────────────────────────────────────
tree = ET.parse(SRC)
root = tree.getroot()

model_id   = root.get("id")
model_name = root.get("name", "")
model_ver  = root.get("version", "")

all_elements = collect_all(root)
regular_elems = [e for e in all_elements if not xsi_type(e).endswith("Relationship")]
relationships  = [e for e in all_elements if xsi_type(e).endswith("Relationship")]

# ── Build Turtle ──────────────────────────────────────────────────────────────
out = []

out.append("@prefix rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
out.append("@prefix owl:       <http://www.w3.org/2002/07/owl#> .")
out.append("@prefix rdfs:      <http://www.w3.org/2000/01/rdf-schema#> .")
out.append("@prefix xsd:       <http://www.w3.org/2001/XMLSchema#> .")
out.append("@prefix dct:       <http://purl.org/dc/terms/> .")
out.append("@prefix archimate: <https://purl.org/archimate#> .")
out.append(f"@prefix na:        <{BASE}> .")
out.append("")

# ── Model ────────────────────────────────────────────────────────────────────
out.append("### ── Model ─────────────────────────────────────────────────────────────")
out.append("")
out.append(f"na:{model_id}")
out.append(f"    a archimate:ArchiMate ;")
out.append(f'    archimate:identifier "{model_id}" ;')
out.append(f'    archimate:name "{escape_ttl(model_name)}"@nb ;')
out.append(f'    owl:versionInfo "{model_ver}" .')
out.append("")

# ── Elements ──────────────────────────────────────────────────────────────────
out.append("### ── Elements ──────────────────────────────────────────────────────────")
out.append("")

property_nodes = []  # collect Property individuals to emit at the end

for e in regular_elems:
    eid   = e.get("id")
    ename = e.get("name", "")
    etype = xsi_type(e)

    doc_elem = e.find("documentation")
    doc = doc_elem.text.strip() if doc_elem is not None and doc_elem.text else ""

    props = [(p.get("key",""), p.get("value","")) for p in e.findall("property")
             if p.get("key") and p.get("value")]

    # build predicate list
    preds = []
    preds.append(("a", f"archimate:{etype}"))
    preds.append(("archimate:identifier", f'"{eid}"'))
    preds.append(("archimate:name", f'"{escape_ttl(ename)}"@nb'))
    if doc:
        esc_doc = escape_ttl(doc)
        preds.append(("archimate:documentation", f'"""{esc_doc}"""@nb'))
    for key, val in props:
        prop_node_id = f"prop-{eid}-{re.sub(r'[^A-Za-z0-9]', '-', key)}"
        preds.append(("archimate:hasProperty", f"na:{prop_node_id}"))
        property_nodes.append((prop_node_id, key, val))

    out.append(f"na:{eid}")
    for i, (pred, obj) in enumerate(preds):
        sep = " ." if i == len(preds) - 1 else " ;"
        out.append(f"    {pred} {obj}{sep}")
    out.append("")

# ── Relationships as named individuals ───────────────────────────────────────
out.append("### ── Relationships ─────────────────────────────────────────────────────")
out.append("")

for r in relationships:
    rid     = r.get("id")
    rtype   = xsi_type(r)
    rsource = r.get("source")
    rtarget = r.get("target")
    rname   = r.get("name", "")

    # Some Archi files put access modifier as attribute
    access_type = r.get("accessType", "")

    rel_class = REL_CLASS_MAP.get(rtype, rtype)

    preds = []
    preds.append(("a", f"archimate:{rel_class}, archimate:Relationship"))
    preds.append(("archimate:identifier", f'"{rid}"'))
    if rname:
        preds.append(("archimate:name", f'"{escape_ttl(rname)}"@nb'))
    preds.append(("archimate:source", f"na:{rsource}"))
    preds.append(("archimate:target", f"na:{rtarget}"))
    if access_type:
        preds.append(("archimate:accessType", f'"{access_type}"'))

    out.append(f"na:{rid}")
    for i, (pred, obj) in enumerate(preds):
        sep = " ." if i == len(preds) - 1 else " ;"
        out.append(f"    {pred} {obj}{sep}")
    out.append("")

# ── Property individuals ─────────────────────────────────────────────────────
if property_nodes:
    out.append("### ── Properties (archimate:Property individuals) ────────────────────────")
    out.append("")
    for (prop_id, key, val) in property_nodes:
        out.append(make_property_node(prop_id, key, val))
        out.append("")

ttl_content = "\n".join(out)

with open(DST, "w", encoding="utf-8") as f:
    f.write(ttl_content)

print(f"Elements    : {len(regular_elems)}")
print(f"Relationships: {len(relationships)}")
print(f"Properties  : {len(property_nodes)}")
print(f"Lines       : {ttl_content.count(chr(10))}")
print(f"Written     : {DST}")
