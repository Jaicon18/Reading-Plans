"""One PNG per marked sheet (every sheet with a wall band or a demolition polyline: A1.1, A4.0, S2.1, D1.0) at the
sheet's own scale (full sheet, 100 dpi, clean PDF): colour per type, legend in schedule order (A, B, C, D, E, then the
other framing VH / RE, then DEMO), every element labelled with its Wall ID exactly as the Excel (Partition Takeoff ids from
familias_out.json partition_types) + LF from the same files; title with project, sheet, date.
Geometry = canon bands / demo polylines (no measurement here).
Use: python3 bitacora.py run scripts/imagenes_hoja.py <tools_dir> <clean.pdf>"""
import json, os, sys
sys.path.insert(0, sys.argv[1])
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont
import etiquetas
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
fo = json.load(open(os.path.join(C4, "out", "familias_out.json")))
demo = json.load(open(os.path.join(K, "etapas", "6_markups", "demo_geom.json")))
sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
PAG = {v: int(k) for k, v in sm.items()}
doc = fitz.open(sys.argv[2])
DPI, F = 100, 100 / 72.0
OUT = os.path.join(K, "etapas", "7_imagenes")
REV = os.environ.get("REV", "rev2")
FECHA = f"2026-11-03 ({REV})"
SCHED = [p["type"] for p in c.get("partition_schedule") or []]
DISP = {"A": "Type A - 6\" stud, 5/8\" gyp each side (A/A4.1)", "B": "Type B - 2-1/2\" stud, 5/8\" gyp one side (B/A4.1)",
        "C": "Type C - 3-5/8\" stud, 5/8\" gyp one side (C/A4.1)", "D": "Type D - 6\" stud, 5/8\" Type X each side, 1-hr (D/A4.1)",
        "E": "Type E - 1-1/2\" metal hat channel @ 24\" O.C. vertical, 5/8\" gyp (E/A4.1)",
        "VH": "Vestibule bulkhead over storefront (1/A5.3)", "RE": "Receiving enclosure CFS 600S162-54 (S2.1)",
        "DEMO": "DEMO - gypsum board + metal framing demolition (SF in label)"}
otros = sorted({w.get("tag") for w in c["walls"]} - set(SCHED))
ORDEN = SCHED + otros + ["DEMO"]
PAL = [(220, 20, 20), (0, 110, 220), (0, 150, 60), (140, 50, 190), (255, 130, 0), (0, 170, 170), (200, 0, 160), (120, 90, 0)]
COL = {t: PAL[i % len(PAL)] for i, t in enumerate(ORDEN[:-1])}
COL["DEMO"] = (230, 70, 0)
xid = {}
for t, x in fo["partition_types"]["types"].items():
    for f in x["filas"]:
        for p in f["wall"].split("+"):
            xid[p] = (f["wall"], f["lf"])
for o in fo["partition_types"].get("other_framing") or []:
    xid[o["id"]] = (o["id"], o.get("lf") or 0)
items = {}
for w in c["walls"]:
    b = w["band"]; sh = b["sheet"]
    if b["ori"] == "H":
        pts = [(b["lo"], (b["c0"] + b["c1"]) / 2), (b["hi"], (b["c0"] + b["c1"]) / 2)]
    else:
        pts = [((b["c0"] + b["c1"]) / 2, b["lo"]), ((b["c0"] + b["c1"]) / 2, b["hi"])]
    wid, lf = xid.get(w["id"], (w["id"], w["length_ft"]))
    lab = f"{wid}  {lf:.2f} LF" if wid == w["id"] else f"{wid} [{w['id']} {w['length_ft']:.2f}]  {lf:.2f} LF"
    items.setdefault(sh, []).append((w["tag"], pts, lab))
for e in demo:
    items.setdefault(e["sheet"], []).append(("DEMO", [tuple(p) for p in e["polyline"]], f"{e['id']}  {e['sf']:,.1f} SF"))
try:
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
    fT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    fL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
except OSError:
    fnt = fT = fL = ImageFont.load_default()
res = {}
for sh in sorted(items):
    its = items[sh]
    pg = doc[PAG[sh] - 1]
    pix = pg.get_pixmap(dpi=DPI)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.35)
    dr = ImageDraw.Draw(im)
    labs, segs, tot = [], [], {}
    for t, pts, lab in its:
        q = [(x * F, y * F) for x, y in pts]   # pages of these sheets have rotation 0
        dr.line(q, fill=COL[t], width=7 if t != "DEMO" else 5)
        segs += list(zip(q, q[1:]))
        mx = sum(p[0] for p in q) / len(q); my = sum(p[1] for p in q) / len(q)
        labs.append({"text": lab, "anchor": (mx, my), "color": COL[t], "own": list(zip(q, q[1:]))})
        tot[t] = tot.get(t, 0) + 1
    etiquetas.colocar(dr, labs, fnt, im.size, obstaculos=segs, ancho_linea=2)
    tipos = [t for t in ORDEN if t in tot]
    h = 70 + 26 * len(tipos)
    dr.rectangle([20, 20, 1280, 20 + h], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    dr.text((34, 28), f"Harbor Freight Tools - Loveland, CO - {sh} - marked take-off - {FECHA}", fill=(0, 0, 0), font=fT)
    y = 74
    for t in tipos:
        dr.line([(40, y + 9), (110, y + 9)], fill=COL[t], width=7)
        dr.text((124, y), f"{DISP.get(t, t)}  ({tot[t]} element(s))", fill=(0, 0, 0), font=fL)
        y += 26
    out = os.path.join(OUT, f"{sh}_marked_by_type_{REV}.png")
    im.save(out)
    res[sh] = {"png": out, "items": len(its), "por_tipo": tot}
json.dump(res, open(os.path.join(OUT, "imagenes_hoja.json"), "w"), indent=1)
print(json.dumps({k: v["por_tipo"] for k, v in res.items()}))
