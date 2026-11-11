"""One PNG per marked sheet (U-158 names): '<SHEET> - IMAGE ONLY (not editable) - walls|ceilings|walls and ceilings <REV>.png'
(Page Label printed on the sheet, never pNN), Xfinity - Interquest:
  A2.0 partition plan  -> walls    (W2 walls + CF column wraps, canon bands)
  A1.0 demolition plan -> walls    (DEMO-01..09 demolished walls, etapas/6_markups/demo_geom.json)
  A3.0 RCP             -> ceilings (SOF-01 gyp header + EXCLUDED rooms of rcp_cuartos.json)
The page is rendered from the editable markups PDF of this run (etapas/6_markups/markups_con_excluded.pdf: the same annotations the
estimator opens in Bluebeam), lightened, and every element is labelled with its ID exactly as the Excel (Partition Takeoff ids from
familias_out.json partition_types, DEMO / SOF ids of the Material Summary) + its LF / SF from the same files; title block with
project, sheet, date and a legend in schedule order. Geometry = canon bands / demo polylines / rcp polygons (no measurement here).
Use: python3 bitacora.py run scripts/imagenes_hoja.py <tools_dir> <clean.pdf>"""
import glob, json, os, sys
sys.path.insert(0, sys.argv[1])
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont
import etiquetas
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
M6 = os.path.join(K, "etapas", "6_markups")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
fo = json.load(open(os.path.join(C4, "out", "familias_out.json")))
demo = json.load(open(os.path.join(M6, "demo_geom.json")))
rcp = json.load(open(os.path.join(M6, "rcp_polys.json")))
cuartos = json.load(open(os.path.join(M6, "rcp_cuartos.json")))
sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
PAG = {v: int(k) for k, v in sm.items()}
doc = fitz.open(os.path.join(M6, "markups_con_excluded.pdf"))
DPI = 100
F = DPI / 72.0
OUT = os.path.join(K, "etapas", "7_imagenes")
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, "* - IMAGE ONLY (not editable) - *.png")):
    os.remove(f)                                         # one PNG per sheet, no stale duplicates
REV = os.environ.get("REV", "rev1")
FECHA = f"2026-11-11 ({REV})"
PROY = "Xfinity - Interquest, Colorado Springs, CO (BCI National)"
DISP = {"W2": "Type W2 - 5/8\" Type X both sides over 3-5/8\" 20 ga studs @ 16\", slab to 6\" above ceiling, braced (2/A2.0, 4/A2.0)",
        "CF": "CF - column furring, 5/8\" Type X over 2-1/2\" studs (5/A2.0)",
        "DEMO": "DEMO - existing interior wall removed, gypsum board + metal framing (A1.0 key 7), SF = LF x H",
        "SOF": "SOF-01 - 5/8\" Type X gyp. bd. header 8'-6\" AFF (A3.0), framing as type W2",
        "EXCLUDED": "EXCLUDED - room not quantified (grey outline + red text with the printed reason and sheet)"}
COL = {"W2": (220, 20, 20), "CF": (0, 110, 220), "DEMO": (230, 70, 0), "SOF": (0, 150, 60), "EXCLUDED": (120, 120, 120)}
xid = {}
for t, x in fo["partition_types"]["types"].items():
    for f in x["filas"]:
        for p in f["wall"].split("+"):
            xid[p] = (f["wall"], f["lf"])
items = {}
for w in c["walls"]:
    b = w["band"]
    sh = b["sheet"]
    m = (b["c0"] + b["c1"]) / 2
    if b["ori"] == "H":
        pts = [(b["lo"], m), (b["hi"], m)]
    elif b["ori"] == "V":
        pts = [(m, b["lo"]), (m, b["hi"])]
    else:                                                 # BOX: x = c0..c1, y = lo..hi
        pts = [(b["c0"], b["lo"]), (b["c1"], b["lo"]), (b["c1"], b["hi"]), (b["c0"], b["hi"]), (b["c0"], b["lo"])]
    wid, lf = xid.get(w["id"], (w["id"], w["length_ft"]))
    items.setdefault(sh, []).append((w["tag"], pts, f"{wid}  {lf:.2f} LF", "walls"))
for e in demo:
    items.setdefault(e["sheet"], []).append(("DEMO", [tuple(p) for p in e["polyline"]], f"{e['id']}  {e['sf']:,.2f} SF", "walls"))
for e in rcp:
    for ln in e.get("lines") or []:
        items.setdefault(e["sheet"], []).append(("SOF", [tuple(p) for p in ln], f"{e['id']}  {e['lf']:.2f} LF / "
                                                 f"{e['lf'] * e['depth_ft']:.2f} SF board", "ceilings"))
vistos = set()
for r in cuartos["rooms"]:
    sh_r = r.get("draw_sheet") or r["sheet"]               # A2.0 rows of rcp_cuartos are drawn on the A3.0 RCP
    if r["disposition"] == "exclusion" and (sh_r, r["room"]) not in vistos:
        vistos.add((sh_r, r["room"]))
        items.setdefault(sh_r, []).append(("EXCLUDED", [tuple(p) for p in r["polygon"]] + [tuple(r["polygon"][0])],
                                                 (r["name"] if r["room"] == r["name"] else f"{r['name']} {r['room']}") + ": EXCLUDED",
                                                 "ceilings"))
try:
    fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    fT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    fL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
except OSError:
    fnt = fT = fL = ImageFont.load_default()
ORDEN = ["W2", "CF", "DEMO", "SOF", "EXCLUDED"]
res = {}
EXL = {}
for sh in sorted(items):
    its = items[sh]
    pg = doc[PAG[sh] - 1]
    pix = pg.get_pixmap(dpi=DPI, annots=True)            # visible (rotated) frame, with the editable markups drawn
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.25)
    dr = ImageDraw.Draw(im)
    labs, segs, tot = [], [], {}
    # R2 M11: an EXCLUDED room label is written INSIDE its own room (never with a leader into the next room): white box,
    # font reduced / two lines until it fits the room, placed where it covers the least printed text (room tags) and red text.
    obst = []
    for b in pg.get_text("blocks"):
        if str(b[4]).strip():
            q_ = fitz.Rect(b[:4]) * pg.rotation_matrix
            q_.normalize()
            obst.append(fitz.Rect(q_.x0 * F, q_.y0 * F, q_.x1 * F, q_.y1 * F))
    for a in pg.annots() or []:
        if a.type[1] == "FreeText" or (a.info.get("subject") or "") not in ("EXCLUDED", ""):
            q_ = a.rect * pg.rotation_matrix
            q_.normalize()
            obst.append(fitz.Rect(q_.x0 * F, q_.y0 * F, q_.x1 * F, q_.y1 * F))
    for t, pts, lab, kind in its:
        if t != "EXCLUDED":
            continue
        X0, Y0 = min(p[0] for p in pts) * F, min(p[1] for p in pts) * F
        X1, Y1 = max(p[0] for p in pts) * F, max(p[1] for p in pts) * F
        best = None
        for sz in (14, 13, 12, 11, 10, 9, 8):
            try:
                fx = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
            except OSError:
                fx = fnt
            for lines in ([lab], lab.rsplit(" ", 1) if lab.endswith("EXCLUDED") else [lab]):
                lines = [lines[0].rstrip(":") + ":" if len(lines) > 1 else lines[0]] + lines[1:]
                w_ = max(dr.textlength(s, font=fx) for s in lines) + 8
                h_ = (sz + 4) * len(lines) + 4
                if w_ > (X1 - X0) - 6 or h_ > (Y1 - Y0) - 6:
                    continue
                for fy in (0.2, 0.35, 0.5, 0.65, 0.8, 0.1, 0.9):
                    cy = Y0 + (Y1 - Y0) * fy
                    r_ = fitz.Rect((X0 + X1) / 2 - w_ / 2, cy - h_ / 2, (X0 + X1) / 2 + w_ / 2, cy + h_ / 2)
                    if r_.y0 < Y0 + 3 or r_.y1 > Y1 - 3:
                        continue
                    pen = sum((r_ & o).get_area() for o in obst if r_.intersects(o))
                    if best is None or pen < best[0] - 1e-6:
                        best = (pen, r_, lines, fx, sz)
            if best is not None and best[0] == 0:
                break
        if best is None:
            sys.exit(f"{sh}: EXCLUDED label '{lab}' does not fit inside its room")
        _, r_, lines, fx, sz = best
        dr.rectangle([r_.x0, r_.y0, r_.x1, r_.y1], fill=(255, 255, 255), outline=COL[t], width=2)
        for i_, s_ in enumerate(lines):
            dr.text((r_.x0 + 4, r_.y0 + 3 + i_ * (sz + 4)), s_, fill=(90, 90, 90), font=fx)
        tot.setdefault(t, [0, kind])[0] += 1
        EXL.setdefault(sh, []).append({"label": lab, "box_px": [round(v) for v in r_],
                                                                           "room_px": [round(X0), round(Y0), round(X1), round(Y1)]})
    for t, pts, lab, kind in its:
        if t == "EXCLUDED":
            continue
        q = [(x * F, y * F) for x, y in pts]
        dr.line(q, fill=COL[t], width=6 if t != "DEMO" else 5)
        segs += list(zip(q, q[1:]))
        mx = sum(p[0] for p in q) / len(q); my = sum(p[1] for p in q) / len(q)
        labs.append({"text": lab, "anchor": (mx, my), "color": COL[t], "own": list(zip(q, q[1:]))})
        tot.setdefault(t, [0, kind])[0] += 1
    etiquetas.colocar(dr, labs, fnt, im.size, obstaculos=segs, ancho_linea=2)
    kinds = sorted({v[1] for v in tot.values()})
    kind = "walls and ceilings" if len(kinds) > 1 else kinds[0]
    tipos = [t for t in ORDEN if t in tot]
    h = 70 + 26 * len(tipos)
    dr.rectangle([20, 20, 1500, 20 + h], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    dr.text((34, 28), f"{PROY} - {sh} - IMAGE ONLY (not editable) - {kind} - {FECHA}", fill=(0, 0, 0), font=fT)
    y = 74
    for t in tipos:
        dr.line([(40, y + 9), (110, y + 9)], fill=COL[t], width=7)
        dr.text((124, y), f"{DISP[t]}  ({tot[t][0]} element(s))", fill=(0, 0, 0), font=fL)
        y += 26
    out = os.path.join(OUT, f"{sh} - IMAGE ONLY (not editable) - {kind} {REV}.png")
    im.save(out)
    chk = Image.open(out)
    assert chk.size == im.size
    res[sh] = {"png": out, "items": len(its), "por_tipo": {k: v[0] for k, v in tot.items()}, "kind": kind}
json.dump(res, open(os.path.join(OUT, "imagenes_hoja.json"), "w"), indent=1)
json.dump(EXL, open(os.path.join(M6, "excluded_labels_png.json"), "w"), indent=1)
print(json.dumps({k: [os.path.basename(v["png"]), v["por_tipo"]] for k, v in res.items()}))
