"""Grand Kia U-175 / U-176: final height table from the two blind readings (H-A, H-B) + the directed A/B resolution.
Writes alturas/FINAL/: ALTURAS_IMPRESAS_A.csv, ALTURAS_IMPRESAS_B.csv, ALTURAS_IMPRESAS.csv (final), ALTURAS_AB_RESOLUCION.csv,
ALTURAS_CUARTOS_A.csv, ALTURAS_CUARTOS_B.csv, ALTURAS_CUARTOS.csv. The final value = A = B when they agree (± 0.021 ft), else the
resolved value (directed crop). RFI-07 walls (two printed heights: A132 8'-0" vs A211 9'-0") carry the higher printed value.
build_canon.py applies ALTURAS_IMPRESAS.csv to every wall / demo element (height_ft, height_op, height_source)."""
import csv, os
W = '/root/gk/work/alturas'
F = f'{W}/FINAL'
os.makedirs(F, exist_ok=True)
COLS = ["Wall ID", "Printed H", "Source", "Operation", "Status", "Image"]


def rd(p):
    return list(csv.DictReader(open(p, encoding='utf-8-sig')))


def wr(p, rows, cols):
    with open(p, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)


L = {}
for r in ('A', 'B'):
    rows = []
    for p in ('Z1', 'Z2', 'Z3', 'DEMO'):
        rows += rd(f'{W}/{r}/{p}/ALTURAS_IMPRESAS.csv')
    for x in rows:
        x['Wall ID'] = x['Wall ID'].strip()
    wr(f'{F}/ALTURAS_IMPRESAS_{r}.csv', rows, COLS)
    L[r] = {x['Wall ID']: x for x in rows}
    wr(f'{F}/ALTURAS_CUARTOS_{r}.csv', rd(f'{W}/{r}/Z3/ALTURAS_CUARTOS.csv'), ["Room", "C.H. (ft)", "Source", "Image"])
RES = {}
for p in ('WALLS', 'DEMO'):
    f = f'{W}/RESOL/{p}/ALTURAS_AB_RESOLUCION.csv'
    if os.path.isfile(f):
        for x in rd(f):
            RES[x['Wall ID'].strip()] = x
RFI07 = {"B-Z3-01", "B-Z3-02", "H-Z3-01", "F-Z3-01"}
final, resol, falta = [], [], []
for k, a in L['A'].items():
    b = L['B'][k]
    if k in RFI07:
        final.append({"Wall ID": k, "Printed H": "9.5", "Status": "DERIVED", "Image": a['Image'],
                      "Source": "RFI-07 (open): A211 3/A211 and 4/A211 print 9'-0\" to the ceiling line, A132 tags 8'-0\"; higher printed value loaded + 0'-6\" (A550)",
                      "Operation": "9'-0\" + 0'-6\" = 9.5"})
        resol.append({"Wall ID": k, "Resolution": f"Both readers read the A132 tag 8'-0\" + 6\" = 8.5; loaded 9.5 per RFI-07 (A211 prints 9'-0\"), delta -1.0 ft if the RCP governs", "Image": a['Image']})
        continue
    if abs(float(a['Printed H']) - float(b['Printed H'])) <= 0.021:
        final.append(a)
        continue
    r = RES.get(k)
    if not r:
        falta.append(k)
        continue
    final.append({"Wall ID": k, "Printed H": r['Final H'], "Source": r['Source'], "Operation": r['Operation'],
                  "Status": r['Status'], "Image": r['Image']})
    resol.append({"Wall ID": k, "Resolution": f"[{r['Chosen']}] {r['Resolution']}", "Image": r['Image']})
# soffit / cove / fascia / header markups: Depth = developed board width of the element = misc board SF / LF of the RCP markup
# (rcp_polys.json: the same LF and Depth the Bluebeam markup carries), circled crop of the drawn line(s) on its RCP sheet
import json, re
MG = json.load(open('/root/gk/work/etapas/4_canon/misc_gen.json'))
BRD = {m['ref'][:-6]: m for m in MG['misc_items'] if m['ref'].endswith(' board')}   # soffits + EXT / WR / RI-18 line markups
RP = [p for p in json.load(open('/root/gk/work/etapas/6_markups/rcp_polys.json')) if p.get('kind') == 'line']
import pymupdf
from PIL import Image, ImageDraw
sm = json.load(open('/root/gk/work/sheetmap.json'))
_doc = pymupdf.open('/root/gk/work/plans/GK_set_SIN_MARKUPS.pdf')
for sx in RP:
    sid, m = sx['id'], BRD.get(sx['id'])
    if not m:
        continue
    lf, dev = float(sx['lf']), float(sx['depth_ft'])
    pg = _doc[sm[sx['sheet']] - 1]
    pts = [q for ln in sx['lines'] for q in ln]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    clip = pymupdf.Rect(min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60)
    z = 2.0
    pix = pg.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples); dr = ImageDraw.Draw(im)
    for ln in sx['lines']:
        dr.line([((q[0] - clip.x0) * z, (q[1] - clip.y0) * z) for q in ln], fill=(255, 0, 0), width=5)
    dr.ellipse([20, 20, pix.width - 20, pix.height - 20], outline=(255, 0, 0), width=4)
    os.makedirs(f'{F}/img', exist_ok=True); img = f'{F}/img/{sid.replace(" ", "_")}_{sx["sheet"]}.png'; im.save(img)
    final.append({"Wall ID": sid, "Printed H": round(dev, 3), "Status": "DERIVED", "Image": img,
                  "Source": f"{sx['sheet']} {sid} ({sx.get('nhoja')}): developed board width / face height = board SF of the element / LF of its drawn line ({str(m.get('source', ''))[:160]})",
                  "Operation": f"{m['qty']} / {lf} = {round(m['qty'] / lf, 3)}"})
wr(f'{F}/ALTURAS_IMPRESAS.csv', final, COLS)
# rooms: A = B (8.167 vs 8.17 is the same 8'-2"), else the resolved row 'ROOM <n>'
ca = rd(f'{W}/A/Z3/ALTURAS_CUARTOS.csv'); cb = {x['Room'].strip().upper(): x for x in rd(f'{W}/B/Z3/ALTURAS_CUARTOS.csv')}
cf = []
for x in ca:
    y = cb.get(x['Room'].strip().upper()) or x
    va, vb = x['C.H. (ft)'].strip(), y['C.H. (ft)'].strip()
    if va == vb or (va and vb and abs(float(va) - float(vb)) <= 0.021):
        cf.append(x); continue
    num = x['Room'].split()[0]
    r = RES.get(f'ROOM {num}')
    if not r:
        falta.append(f'ROOM {num}'); cf.append(x); continue
    cf.append({"Room": x['Room'], "C.H. (ft)": r['Final H'], "Source": r['Source'], "Image": r['Image']})
    resol.append({"Wall ID": "ROOM " + num, "Resolution": f"[{r['Chosen']}] {x['Room']}: {r['Resolution']}", "Image": r['Image']})
# ceiling ZONES of one room with their own printed tag (U-176 control 4: a room with two printed C.H. is two keys; the
# faces of the walls in each zone carry the zone name - canon_patch.json)
_img = {x['Room'].split()[0]: x.get('Image', '') for x in cf}
cf += [
 {"Room": "Showroom south ceiling zone (21-0 tag, south of the sloped line kn 16)", "C.H. (ft)": "21.0", "Image": _img.get('101', ''),
  "Source": "A131 RCP room 101 SHOWROOM prints \"21-0 PGB P-7\" south of the sloped soffit line (kn 16) and \"22-0 PGB P-7\" in the north field"},
 {"Room": "Lounge field ceiling (outside the 10-9 WC-1 cloud)", "C.H. (ft)": "10.0", "Image": _img.get('107', ''),
  "Source": "[DERIVED] room 107 LOUNGE field (no tag; A131 '10-9 WC-1' is the center cloud): A300 B-B ceiling y1171.68, F.F. y1261.68: (1261.68-1171.68)/9 = 10.0"},
 {"Room": "Lounge casework alcoves (8-0 PGB P-7 tag)", "C.H. (ft)": "8.0", "Image": _img.get('107', ''),
  "Source": "A131 RCP room 107 LOUNGE: leader tags \"8'-0\" PGB P-7\" to the casework alcoves north of MEN 121 (A300 B-B alcove soffit 7.99)"},
 {"Room": "Corridor at door 143A", "C.H. (ft)": "10.0", "Image": "/root/gk/work/alturas/B/Z2/img/A131_RCP_sur_oficinas.png",
  "Source": "A131 RCP prints \"10'-0\" PGB P-7\" in the corridor at door 143A (both readings)"},
]
wr(f'{F}/ALTURAS_CUARTOS.csv', cf, ["Room", "C.H. (ft)", "Source", "Image"])
wr(f'{F}/ALTURAS_AB_RESOLUCION.csv', resol, ["Wall ID", "Resolution", "Image"])
print(len(final), 'final heights;', len(resol), 'resolutions;', 'MISSING:', falta)
