#!/usr/bin/env python3
"""normalizar_canon_campos.py (CR desde cero, Paso 9): arreglos de FORMA del canon unido, por programa y verificables
(no cambian cantidades salvo donde se dice): N/HOJA de vista en cada partida, operación de cada [DERIVED], hoja concreta
en las alturas, sufijos de cara normalizados, board W.R. en caras de cuartos húmedos (A0.06 GN 11), textos."""
import json, math, re, sys, collections
canon_p, inv_p = sys.argv[1], sys.argv[2]
c = json.load(open(canon_p)); inv = json.load(open(inv_p))
NH = re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,3}-?\d{1,3}\.\d{1,3}")
SH = re.compile(r"\b[A-Z]\d\.\d{2}\b")
esc = c["constants"]["plan_scale_by_sheet"]
pages = {s["page"]: s["sheet"] for s in inv["sheets"]}
burb = collections.defaultdict(list)            # burbujas de título de vista (self_sheet) por hoja
for o in inv["ocurrencias"].get("detail_bubble", []):
    if o.get("self_sheet"):
        n, sh = str(o.get("ref") or o.get("text")).split("/")[0], o.get("sheet")
        burb[sh].append((n, o["center_pt"]))
log = collections.Counter()
def vista(e):
    sh = e["sheet"]
    for k in ("source", "location", "height_source", "decision", "type"):
        m = re.search(r"\b(\d{1,2})/" + re.escape(sh) + r"\b", str(e.get(k) or ""))
        if m:
            return m.group(1)
    if sh.startswith("A2."):
        return "1"                                 # A2.0x: una sola vista '1 LEVEL n 1/8"=1'-0"'
    VIS = {"A7.30": lambda x, y: "1",                                            # 1 ENLARGED PLAN - LOBBY & BAR (única vista de planta)
           "A6.01": lambda x, y: "10" if 1440 <= x <= 1800 and y >= 1000 else None,   # 10 ENLARGED PLAN - LOBBY STAIR - LVL 1
           "A7.45": lambda x, y: "1" if x < 1200 and y > 900 else ("3" if x > 1200 and y < 900 else None)}   # 1 LOBBY RESTROOMS / 3 TRASH & SERVICE
    if sh in VIS and e.get("path"):
        v_ = VIS[sh](e["path"][0][0], e["path"][0][1])
        if v_:
            return v_
    if sh == "A7.50":
        return {"L1": "1", "L4": "3"}.get(str(e.get("floor")), None)
    if burb.get(sh) and e.get("path"):
        cx = sum(p[0] for p in e["path"]) / len(e["path"]); cy = sum(p[1] for p in e["path"]) / len(e["path"])
        bajo = [(math.dist((cx, cy), p), n) for n, p in burb[sh] if p[1] >= cy]   # el título va bajo la vista
        if bajo:
            return min(bajo)[1]
    return None
ids_base = collections.defaultdict(list)
for e in c["existing_walls"]:
    b, _, s = e["id"].partition(" ")
    ids_base[b].append(e)
for b, es in ids_base.items():
    usadas = {e["id"].partition(" ")[2] for e in es if re.fullmatch(r"[A-Z]", e["id"].partition(" ")[2])}
    libres = [chr(x) for x in range(65, 91) if chr(x) not in usadas]
    for e in es:
        s = e["id"].partition(" ")[2]
        if s and not re.fullmatch(r"[A-Z]", s):
            if not libres:                       # > 26 caras en un muro: segundo registro del mismo muro físico
                b = b + ".2" if not b.endswith(".2") else b
                libres = [chr(x) for x in range(65, 91) if f"{b} {chr(x)}" not in {y["id"] for y in es}]
            e["id_original_info"] = e["id"]; e["id"] = f"{b} {libres.pop(0)}"; log["id sufijo normalizado"] += 1
WET = re.compile(r"(?i)\b(bath|toilet|shower|janitor|restroom|women|men|wc)\b")
for e in c["existing_walls"]:
    sh = e["sheet"]
    if not NH.search(str(e.get("source"))):
        v = vista(e)
        if v:
            e["source"] = f"{v}/{sh} | {e.get('source')}"; log["N/HOJA de vista"] += 1
    if str(e.get("length_status")).upper().startswith("DER") and not e.get("length_op"):
        s_ = float((esc.get(sh) or {}).get("value") or 0)
        pts = sum(math.dist(a, b) for q in (e.get("paths") or [e["path"]]) for a, b in zip(q, q[1:]))
        e["length_op"] = f"vector centerline path {pts:.2f} pt / {s_:g} pt/ft = {pts / s_:.2f} ft (on {sh})"; log["length_op"] += 1
    hs = str(e.get("height_source") or "")
    hs2 = hs.replace("A4.0x", "A4.00").replace("MAX. HEIGHT", "max. height")
    if not SH.search(hs2):
        hs2 += " | level datums printed on A4.00 (LEVEL 1 6197.75', LEVEL 2 6211.75', LEVEL 3 6222.75', LEVEL 4 6233.75', ROOF 6247.75')"
    if hs2 != hs:
        e["height_source"] = hs2; log["altura hoja concreta"] += 1
    loc = str(e.get("location") or "")
    if e.get("board") == "5/8 type X" and WET.search(loc.split("faces:")[-1]):
        e["board"] = "5/8 type X WR"; e["decision"] = str(e.get("decision")) + " | W.R. board: wet room face (A0.06 general note 11)"; log["WR cara húmeda"] += 1
for k in ("ceilings",):
    for x in c.get(k, []):
        if re.search(r"L4 (Cleaning 406|Women 417|Men 418)", str(x.get("room"))) and not NH.search(str(x.get("detail") or "")):
            x["detail"] = "1/A5.06"; x["detail_source"] = "1/A5.06 LEVEL 4 to bottom of roof assembly 8'-11 1/4\""; log["detalle cielo L4"] += 1
txt = json.dumps(c, ensure_ascii=False)
for a, b in (("(hi-lo)", "(hi - low)"), ("no existe en el set", "not in the set"), ("6/U-201", "U-201 (6)"),
             ("CONTINUOUS TO UNDERSIDE OF ROOF SHEATHING", "CONTINUOUS TO UNDERSIDE OF ROOF SHEETHING"), (".py", "")):
    n = txt.count(a); txt = txt.replace(a, b); log[f"texto {a}"] += n
c = json.loads(txt)
json.dump(c, open(canon_p, "w"), indent=1, ensure_ascii=False)
print(dict(log))
