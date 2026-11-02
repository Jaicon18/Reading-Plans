"""One PNG per marked sheet (A-202, A-221, A-050, A-052) at the sheet's own scale (full sheet, 100 dpi, clean PDF):
color per type, legend in schedule order (A-202: M2.1, M3.5, W4, W4.1, W6, W8, SW6, then EXISTING board-only, OTHER
FRAMING soffit, DEMO), every element labelled with its Wall ID exactly as the Excel (Partition Takeoff wall ids from
familias_out.json partition_types; board-only ids; DEMO ids) + LF from the same files; title with project, sheet, date.
Geometry = canon bands / paths / demo polylines (no measurement here).
Use: python3 bitacora.py run scripts/imagenes_hoja.py <tools_dir> <clean.pdf>"""
import json, os, sys
sys.path.insert(0, sys.argv[1])
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont
import etiquetas
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
fo = json.load(open(os.path.join(C4, "out", "familias_out.json")))
demo = json.load(open(os.path.join(K, "etapas", "6_markups", "demo_geom.json")))
doc = fitz.open(sys.argv[2])
DPI, F = 100, 100 / 72.0
OUT = os.path.join(K, "etapas", "7_imagenes")
DISP = {"INFILL": "INFILL 6\" metal (untagged, D3/A-624)", "DEMO": "DEMO (demolition, SF in label)"}
FECHA = "2026-11-02 (rev3)"
ORDEN = ["M2.1", "M3.5", "INFILL", "W4", "W4.1", "W6", "W8", "SW6", "EXISTING (board only)", "OTHER FRAMING - SOFFIT SIDE", "DEMO"]
COL = {"M2.1": (220, 20, 20), "M3.5": (0, 110, 220), "INFILL": (200, 0, 160), "W4": (0, 150, 60), "W4.1": (120, 190, 0), "W6": (255, 130, 0),
       "W8": (140, 50, 190), "SW6": (0, 170, 170), "EXISTING (board only)": (130, 130, 130),
       "OTHER FRAMING - SOFFIT SIDE": (0, 75, 165), "DEMO": (230, 70, 0)}
# Excel wall ids (partition_types groups collinear walls: e.g. M3.5-01 + MB-01 = one Excel row)
xid = {}
for t, x in fo["partition_types"]["types"].items():
    for f in x["filas"]:
        for p in f["wall"].split("+"):
            xid[p] = (f["wall"], f["lf"])
for o in fo["partition_types"].get("other_framing") or []:
    xid[o["id"]] = (o["id"], o.get("lf") or 0)


def tipo_ex(eid):
    s = eid[2:] if eid.startswith("R-") else eid
    t = s.split("-")[0]
    return t if t in COL else "EXISTING (board only)"


items = {}
for w in c["walls"]:
    b = w["band"]; sh = b["sheet"]
    if b["ori"] == "H":
        pts = [(b["lo"], (b["c0"] + b["c1"]) / 2), (b["hi"], (b["c0"] + b["c1"]) / 2)]
    else:
        pts = [((b["c0"] + b["c1"]) / 2, b["lo"]), ((b["c0"] + b["c1"]) / 2, b["hi"])]
    t = "OTHER FRAMING - SOFFIT SIDE" if w["element"] == "soffit_side" else w["tag"]
    t = "INFILL" if t == "INFILL" else t
    wid, lf = xid.get(w["id"], (w["id"], w["length_ft"]))
    lab = f"{wid}  {lf:.2f} LF" if wid == w["id"] else f"{wid} [{w['id']} {w['length_ft']:.2f}]  {lf:.2f} LF"
    items.setdefault(sh, []).append((t, pts, lab))
for e in c["existing_walls"]:
    items.setdefault(e["sheet"], []).append((tipo_ex(e["id"]), [tuple(p) for p in e["path"]], f"{e['id']}  {e['length_ft']:.2f} LF"))
for e in demo:
    items.setdefault(e["sheet"], []).append(("DEMO", [tuple(p) for p in e["polyline"]], f"{e['id']}  {e['sf']:.1f} SF"))
AREAS = json.load(open(os.path.join(K, "etapas", "6_markups", "areas.json")))
ACOL = {"GYP CEILING": (0, 140, 60), "SOFFIT BOTTOM": (0, 75, 165), "LEVEL 5": (200, 0, 160), "ROOF HATCH SHAFT": (120, 60, 0),
        "PIN & SLEEVE RECESS": (0, 110, 220)}
for a in AREAS:
    lab = a["contents"].split(" · ")
    items.setdefault(a["sheet"], []).append(("AREA:" + a["subject"], [tuple(p) for p in a["pts"]] + [tuple(a["pts"][0])],
                                             " · ".join(lab[:3])[:60]))
for k, v in ACOL.items():
    COL["AREA:" + k] = v
    DISP["AREA:" + k] = k.title() + " (area / item, label from the take-off)"
ORDEN += ["AREA:" + k for k in ACOL]
PAG = {"A-202": 13, "A-221": 15, "A-050": 6, "A-052": 7}
try:
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
    fT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    fL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
except OSError:
    fnt = fT = fL = ImageFont.load_default()
res = {}
for sh, pg in PAG.items():
    its = items.get(sh) or []
    pix = doc[pg - 1].get_pixmap(dpi=DPI)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.35)
    dr = ImageDraw.Draw(im)
    labs, segs, tot = [], [], {}
    for t, pts, lab in its:
        q = [(x * F, y * F) for x, y in pts]
        dr.line(q, fill=COL[t], width=7 if t != "DEMO" else 5)
        for a, b in zip(q, q[1:]):
            segs.append((a, b))
        mx = sum(p[0] for p in q) / len(q); my = sum(p[1] for p in q) / len(q)
        labs.append({"text": lab, "anchor": (mx, my), "color": COL[t], "own": list(zip(q, q[1:]))})
        tot[t] = tot.get(t, 0) + 1
    etiquetas.colocar(dr, labs, fnt, im.size, obstaculos=segs, ancho_linea=2)
    tipos = [t for t in ORDEN if t in tot]
    h = 70 + 26 * len(tipos)
    dr.rectangle([20, 20, 1180, 20 + h], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    dr.text((34, 28), f"Chick-fil-A #2284 River Point - {sh} - marked take-off - {FECHA}", fill=(0, 0, 0), font=fT)
    y = 74
    for t in tipos:
        dr.line([(40, y + 9), (110, y + 9)], fill=COL[t], width=7)
        dr.text((124, y), f"{DISP.get(t, t)}  ({tot[t]} element(s))", fill=(0, 0, 0), font=fL)
        y += 26
    out = os.path.join(OUT, f"{sh}_marked_by_type_rev3.png")
    im.save(out)
    res[sh] = {"png": out, "items": len(its), "por_tipo": tot}
json.dump(res, open(os.path.join(OUT, "imagenes_hoja.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
