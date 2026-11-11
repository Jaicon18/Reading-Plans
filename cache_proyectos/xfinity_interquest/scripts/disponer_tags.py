"""Disposition of every inventory candidate PAnnnn / PCnnnn by program (HFT Loveland: single-letter wall tags A..E, so
inventario_tags.py could not count any tag and left 490 partition_ambiguo + 147 partition_candidato).
 1. counted: a wall tag the reading located ("<sheet> <T> tag @ (x,y)" in walls[].tag_ids) is matched to the
    inventory occurrence of the SAME type on the SAME sheet within R_PT pt -> its PA/PC id is added to tag_ids;
 2. every other PA / PC goes to canon tags_descartados {id, motivo, imagen}: motivo = the inventory motivo in English
    (loose text / note / legend, non-plan sheet, sheet without symbol reference, out-of-schedule symbol text such as
    sheet numbers / equipment / grid tags) + its sheet; imagen = its verified inventory crop (recortes/).
No quantity is touched. Writes etapas/4_canon/takeoff_canon.json in place + etapas/4_canon/tags_disposicion.json.
Use: python3 bitacora.py run scripts/disponer_tags.py"""
import json, math, os, re, sys
from collections import Counter
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
P = os.path.join(C4, "takeoff_canon.json")
INV = os.path.join(K, "etapas", "1_inventario", "inventario.json")
REC = os.path.join(K, "etapas", "1_inventario", "recortes")
R_PT = 12.0
c = json.load(open(P))
inv = json.load(open(INV))
oc = inv["ocurrencias"]
cand = list(oc.get("partition_ambiguo") or []) + list(oc.get("partition_candidato") or [])
by_id = {o["id"]: o for o in cand}
RX = re.compile(r"^\s*([A-Z]{1,3}\d[\w.]*)\s+(\S+)\s+tag\s*@\s*\(\s*([\d.]+)\s*,\s*([\d.]+)\s*\)")
EN = [(r"sin s.mbolo cerrado alrededor", "loose letter with no closed symbol around it (note text, legend or label: not a wall tag)"),
      (r"la hoja no tiene types de varios caracteres", "sheet without multi-character tags in symbols to calibrate size / radius: letter of a note, grid bubble, detail or legend (not a wall tag)"),
      (r"hoja que no es de planta", "sheet that is not a plan (title without PLAN): detail / elevation / schedule / note text, not a wall tag"),
      (r"NO est. en el schedule", "symbol text that is not a partition type of the A4.1 schedule (sheet number, grid / equipment / keynote / detail tag)"),
      (r"tama.o|radio", "letter size or symbol radius different from the wall tags of its sheet (grid bubble, detail callout or note)")]


def motivo_en(o):
    m = str(o.get("motivo") or "")
    for rx, t in EN:
        if re.search(rx, m, re.I):
            return t
    return "not a wall tag: " + m


usados, n_add = {}, 0
for w in c.get("walls") or []:
    ids = list(w.get("tag_ids") or [])
    new = []
    for t in ids:
        t = str(t)
        if re.fullmatch(r"P[AC]\d{4}", t):
            usados[t] = w["id"]
            new.append(t)
            continue
        new.append(t)
        m = RX.match(t)
        if not m:
            continue
        sh, ty, x, y = m.group(1), m.group(2), float(m.group(3)), float(m.group(4))
        best = min(((math.dist(o["center_pt"], (x, y)), o) for o in cand
                    if o.get("sheet") == sh and str(o.get("type") or o.get("text")) == str(w.get("tag")) == ty), default=None,
                   key=lambda z: z[0])
        if best and best[0] <= R_PT and best[1]["id"] not in usados:
            usados[best[1]["id"]] = w["id"]
            new.append(best[1]["id"])
            n_add += 1
    w["tag_ids"] = new
prev = {str(t.get("id")): t for t in c.get("tags_descartados") or [] if isinstance(t, dict) and t.get("id")}
desc = []
for o in cand:
    i = o["id"]
    if i in usados:
        continue
    img = os.path.join(REC, o.get("png") or "")
    if not o.get("png") or not os.path.exists(img):
        sys.exit(f"{i}: inventory crop missing ({o.get('png')})")
    t = prev.get(i) or {}
    desc.append({"id": i, "type": o.get("type") or o.get("text"), "sheet": o.get("sheet"), "page": o.get("page"),
                 "motivo": t.get("motivo") or f"{motivo_en(o)} - {o.get('sheet')} p.{o.get('page')} text '{o.get('text')}'",
                 "imagen": t.get("imagen") or t.get("img") or img})
ids_desc = {d["id"] for d in desc}
desc += [t for i, t in prev.items() if i not in ids_desc and i not in usados]
c["tags_descartados"] = desc
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
res = {"candidates": len(cand), "counted_in_tag_ids": sorted(usados.items()), "added_now": n_add, "discarded": len(desc),
       "by_reason": Counter(d["motivo"].split(" - ")[0] for d in desc)}
json.dump(res, open(os.path.join(C4, "tags_disposicion.json"), "w"), indent=1, ensure_ascii=False)
print(f"{len(cand)} PA/PC candidates: {len(usados)} counted in walls[].tag_ids ({n_add} matched now), {len(desc)} discarded with motivo + crop")
for k, v in res["by_reason"].most_common():
    print(f"  {v:4d}  {k[:110]}")
sys.exit(0 if len(usados) + len([d for d in desc if d['id'] in by_id]) == len(cand) else 1)
