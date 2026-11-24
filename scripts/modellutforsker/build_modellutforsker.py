#!/usr/bin/env python3
"""
Bygger modellutforskeren for Nasjonal arkitektur fra YAML-eksporten av Archi-modellen.

Skriptet leser YAML-filen, gjør om elementer, relasjoner og diagrammer (views) til
et kompakt dataformat, og setter dataene inn i template.html. Resultatet er én
selvstendig HTML-fil som kan legges ut på GitHub Pages.

Skriptet kjøres av bygg_lokalt.py fra rotmappen i repoet. Det kan også kjøres alene:
    python scripts/modellutforsker/build_modellutforsker.py

Standard er å lese data/nasjonal-arkitektur.yaml og skrive docs/modellutforsker/index.html.
Andre stier kan angis med --yaml og --out.

Krav: Python 3.9 eller nyere og PyYAML (pip install pyyaml).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("Mangler PyYAML. Installer med: pip install pyyaml")

HERE = Path(__file__).resolve().parent
PLACEHOLDER = "__NA_DATA__"


def _txt(value) -> str:
    return (value or "").strip() if isinstance(value, str) else ("" if value is None else str(value).strip())


def _num(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def convert(model: dict) -> dict:
    """Gjør om YAML-modellen til dataformatet modellutforskeren forventer."""
    elements = model.get("elements") or {}
    relationships = model.get("relationships") or {}
    views = model.get("views") or {}

    els = {}
    for eid, e in elements.items():
        els[eid] = {
            "id": eid,
            "t": e.get("type", ""),
            "n": _txt(e.get("name")),
            "d": _txt(e.get("documentation")),
            "p": e.get("properties") or {},
            "f": e.get("folder_path") or [],
        }

    rels = {}
    for rid, r in relationships.items():
        src, tgt = r.get("source_id"), r.get("target_id")
        if src not in els or tgt not in els:
            # Relasjoner til relasjoner eller til elementer som mangler hoppes over.
            continue
        rels[rid] = {
            "id": rid,
            "t": (r.get("type") or "").replace("Relationship", ""),
            "n": _txt(r.get("name")),
            "s": src,
            "g": tgt,
            "d": _txt(r.get("documentation")),
        }

    # Oppslag for å finne relasjonen bak en kobling i et diagram når relasjons-ID mangler.
    by_pair: dict[tuple[str, str], str] = {}
    for r in rels.values():
        by_pair.setdefault((r["s"], r["g"]), r["id"])

    out_views = []
    for vid, v in sorted(views.items(), key=lambda kv: _txt(kv[1].get("name"))):
        nodes = {}
        for nid, n in (v.get("nodes") or {}).items():
            b = n.get("bounds") or {}
            nodes[nid] = {
                "e": n.get("archimate_element_id") or "",
                "par": n.get("parent_node_id"),
                "x": _num(b.get("x")), "y": _num(b.get("y")),
                "w": _num(b.get("width")), "h": _num(b.get("height")),
                "k": n.get("type", ""),
            }

        def absolute(nid: str) -> tuple[float, float, int]:
            n = nodes[nid]
            x, y, depth, p = n["x"], n["y"], 0, n["par"]
            seen = set()
            while p and p in nodes and p not in seen:
                seen.add(p)
                x += nodes[p]["x"]; y += nodes[p]["y"]; depth += 1
                p = nodes[p]["par"]
            return x, y, depth

        vnodes = []
        for nid, n in nodes.items():
            if n["k"] != "DiagramObject" or n["e"] not in els:
                continue
            x, y, depth = absolute(nid)
            vnodes.append({"id": nid, "e": n["e"], "x": x, "y": y, "w": n["w"], "h": n["h"],
                           "dp": depth, "par": n["par"]})

        conns = []
        for c in (v.get("connections") or {}).values():
            s, g = nodes.get(c.get("source_node")), nodes.get(c.get("target_node"))
            if not s or not g:
                continue
            rid = c.get("relationship_id") or by_pair.get((s["e"], g["e"]), "")
            conns.append({"s": c["source_node"], "g": c["target_node"], "r": rid if rid in rels else ""})

        out_views.append({"id": vid, "n": _txt(v.get("name")), "d": _txt(v.get("documentation")),
                          "nodes": vnodes, "conns": conns})

    meta = model.get("model") or {}
    return {
        "model": {"id": meta.get("id", ""), "name": meta.get("name", ""), "version": meta.get("version", "")},
        "els": els,
        "rels": rels,
        "views": out_views,
    }


def build(yaml_path: Path, template_path: Path, out_path: Path, generated: str | None) -> dict:
    model = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    for key in ("elements", "relationships", "views"):
        if key not in model:
            raise SystemExit(f"Fant ikke '{key}' i {yaml_path}. Er dette YAML-eksporten fra Archi?")
    data = convert(model)
    if generated:
        data["generated"] = generated

    template = template_path.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise SystemExit(f"Malen {template_path} mangler plassholderen {PLACEHOLDER}.")
    # Hindrer at tekst i dokumentasjonen kan avslutte <script>-blokken.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = template.replace(PLACEHOLDER, payload)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return data


def main() -> None:
    ap = argparse.ArgumentParser(description="Bygg modellutforskeren for Nasjonal arkitektur fra Archi-YAML.")
    ap.add_argument("--yaml", type=Path, default=Path("data/nasjonal-arkitektur.yaml"),
                    help="Sti til YAML-eksporten av modellen (standard: data/nasjonal-arkitektur.yaml)")
    ap.add_argument("--out", type=Path, default=Path("docs/modellutforsker/index.html"),
                    help="Hvor HTML-filen skal skrives (standard: docs/modellutforsker/index.html)")
    ap.add_argument("--template", type=Path, default=HERE / "template.html", help="HTML-malen (standard: template.html ved siden av skriptet)")
    ap.add_argument("--no-date", action="store_true", help="Ikke vis genereringsdato (gir uendret fil når modellen er uendret)")
    args = ap.parse_args()

    generated = None if args.no_date else dt.date.today().strftime("%d.%m.%Y")
    data = build(args.yaml, args.template, args.out, generated)
    print(f"Modellutforsker skrevet til {args.out}: {len(data['els'])} elementer, "
          f"{len(data['rels'])} relasjoner, {len(data['views'])} diagrammer "
          f"(modellversjon {data['model']['version'] or 'ukjent'}).")


if __name__ == "__main__":
    main()
