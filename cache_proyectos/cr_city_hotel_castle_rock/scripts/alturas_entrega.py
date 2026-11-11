"""U-175 / U-176 (CR City Hotel rev19): copia las dos lecturas ciegas de alturas a la entrega.
Auditoria/ALTURAS_IMPRESAS_A.csv / _B.csv, ALTURAS_CUARTOS_A / _B, imágenes en Auditoria/alturas_img/A y /B (ruta relativa), y la tabla
final ALTURAS_IMPRESAS.csv / ALTURAS_CUARTOS.csv = A cuando A = B (± 1/4"); donde A != B, la fila resuelta de
<dir>/ALTURAS_AB_RESOLUCION.csv (Wall ID, Resolution, Image, Printed H, Source, Operation, Status) con su recorte dirigido.
Uso: alturas_entrega.py <dir con A/ y B/> <carpeta_entrega_rev>"""
import csv
import os
import shutil
import sys

R, E = sys.argv[1], sys.argv[2]
A, B = os.path.join(R, "A"), os.path.join(R, "B")
au = os.path.join(E, "Auditoria")
TOL = 1 / 48 + 1e-6


def leer(p):
    return list(csv.DictReader(open(p, encoding="utf-8-sig")))


def img(p, src, sub):
    dst = os.path.join(au, "alturas_img", sub)
    os.makedirs(dst, exist_ok=True)
    p = p if os.path.isabs(p) else os.path.join(src, p)
    if not os.path.isfile(p):
        sys.exit(f"falta la imagen {p}")
    shutil.copy2(p, dst)
    return f"Auditoria/alturas_img/{sub}/" + os.path.basename(p)


def escribir(nombre, filas):
    with open(os.path.join(au, nombre), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return None


out = {}
for nombre, llave in (("ALTURAS_IMPRESAS.csv", "Wall ID"), ("ALTURAS_CUARTOS.csv", "Room")):
    fa, fb = leer(os.path.join(A, nombre)), leer(os.path.join(B, nombre))
    for f_, src, sub in ((fa, A, "A"), (fb, B, "B")):
        for r in f_:
            r["Image"] = img(r["Image"], src, sub)
    escribir(nombre.replace(".csv", "_A.csv"), fa)
    escribir(nombre.replace(".csv", "_B.csv"), fb)
    out[nombre] = (fa, fb)

fa, fb = out["ALTURAS_IMPRESAS.csv"]
bmap = {r["Wall ID"]: r for r in fb}
resol = {}
rp = os.path.join(R, "ALTURAS_AB_RESOLUCION.csv")
if os.path.isfile(rp):
    for r in leer(rp):
        r["Image"] = img(r["Image"], R, "resolucion")
        resol[r["Wall ID"]] = r
    escribir("ALTURAS_AB_RESOLUCION.csv", list(resol.values()))
final, dif = [], []
for r in fa:
    b = bmap.get(r["Wall ID"])
    ha, hb = num(r["Printed H"]), num(b["Printed H"]) if b else None
    if r["Wall ID"] in resol:                     # resolución (también cuando A = B pero el renglón es una condición que no modelaron)
        x = resol[r["Wall ID"]]
        final.append({"Wall ID": r["Wall ID"], "Printed H": x["Printed H"], "Source": x["Source"], "Operation": x.get("Operation", ""),
                      "Status": x["Status"], "Image": x["Image"]})
    elif b is not None and ha is not None and hb is not None and abs(ha - hb) <= TOL:
        final.append(r)
    elif False:
        x = resol[r["Wall ID"]]
        final.append({"Wall ID": r["Wall ID"], "Printed H": x["Printed H"], "Source": x["Source"], "Operation": x.get("Operation", ""),
                      "Status": x["Status"], "Image": x["Image"]})
    else:
        dif.append(r["Wall ID"])
        final.append(r)
# Soffits / beam wraps con Depth en Bluebeam (= ancho desarrollado del board, no una altura de wall): las lecturas ciegas H-A / H-B
# leyeron walls; estos 14 elementos van con la operación de su detalle (lectura del take-off, NO ciega; dicho en la fuente)
IM = '/root/cr/work/etapas/4_canon/img'
EXTRA = [("SOF-L1-01", 1.063, "2/A7.31 & 4/A7.31 'DROPPED SOFFIT 1'-0 3/4\"' (lobby coffers: 12'-0 3/4\" - 11'-0\")", "12'-0 3/4\" - 11'-0\" = 1'-0 3/4\"", f"{IM}/rev9/MISC_SOF-L1-01.png")]
for k_ in ("SOF-L2-01", "SOF-L2-02", "SOF-L3-316", "SOF-L3-318", "SOF-L4-02"):
    EXTRA.append((k_, 0.917, "7/A7.23 corridor band: bottom '4 1/2\"' (0.375 ft) + vertical drop 8'-11\" - 8'-4 1/2\" = 6 1/2\" (0.542 ft)", "0.375 + 0.542 = 0.917", f"{IM}/rev19/R19_SOF_7-A723_banda.png"))
for k_ in ("SOF-L2-SCN", "SOF-L2-SCS", "SOF-L3-SCN", "SOF-L3-SCS", "SOF-L4-SCN", "SOF-L4-SCS"):
    EXTRA.append((k_, 5.039, "12/A9.03 'SOFFIT AROUND HOUSING' (smoke curtain), developed width measured at 1 1/2\" = 1'-0\": drop 1.239 + bottom 0.374 + housing 1.198 + return 0.25 + shaft face 1.978", "1.239 + 0.374 + 1.198 + 0.25 + 1.978 = 5.039", f"{IM}/rev19/R19_SOF_12-A903_housing.png"))
EXTRA.append(("SOF-L4-01", 8.59, "7/A6.01 / 11/A6.01 'GYP BD SOFFIT AT FCU. CONTINUES FULL WIDTH OF STAIR.': bottom 6.59 ft + face 2.0 ft", "6.59 + 2.0 = 8.59", f"{IM}/rev9/MISC_SOF-L4-01.png"))
EXTRA.append(("BW-L1-RETAIL", 1.7464, "A3.01 / S1.02 retail beam wraps (FS-1 membrane, A0.08): board 389.49 SF over 223.03 LF (interior beams bottom 0.59 + 2 x 1'-0\" sides, north edge beams d / bf AISC)", "389.49 / 223.03 = 1.7464", f"{IM}/rev9/MISC_BW-L1-RETAIL.png"))
for k_, h_, s_, o_, im_ in EXTRA:
    final.append({"Wall ID": k_, "Printed H": f"{h_:.4f}", "Source": "[take-off detail reading, not blind] " + s_, "Operation": o_, "Status": "DERIVED",
                  "Image": img(im_, R, "soffits")})
# U-181 (rev19): renglones partidos de un wall ya leído (cara de baño W.R. de los demising DW.4): misma altura que su renglón padre
import json as _json
_can = _json.load(open('/root/cr/work/etapas/4_canon/takeoff_canon.json'))
_ids = {r["Wall ID"] for r in final}
_por = {r["Wall ID"]: r for r in final}
for _w in _can['walls'] + _can['existing_walls']:
    _p = _w['id'][:-2] + ' A' if len(_w['id']) > 2 and _w['id'][-2] == ' ' else None
    if _w['id'] not in _ids and _p in _por and 'rev19 U-181' in str(_por.get(_p, {}).get('Source', '')) + str(_w.get('source', '')) + 'rev19 U-181':
        _r = dict(_por[_p]); _r["Wall ID"] = _w['id']
        _r["Source"] = f"[split row of {_p} (bath face W.R., A0.06 GN 11), same height as its parent] " + _r["Source"]
        final.append(_r); _ids.add(_w['id'])
escribir("ALTURAS_IMPRESAS.csv", final)
ca, cb = out["ALTURAS_CUARTOS.csv"]
sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import comparar_alturas as CA  # noqa: E402
llaves_a = {CA.sala(r["Room"]) for r in ca}
fin_c = [dict(r) for r in ca] + [dict(r) for r in cb if CA.sala(r["Room"]) not in llaves_a]
for k, x in resol.items():                       # C.H. resueltos de cuartos ('ROOM <n>'): el cuarto toma el valor resuelto
    if k.startswith("ROOM "):
        sal = k[5:]
        fin_c = [r for r in fin_c if CA.sala(r["Room"]) != sal or CA.RX_NO_CUARTO.search(str(r["Room"]))]
        fin_c.append({"Room": sal, "C.H. (ft)": x["Printed H"], "Source": x["Source"], "Image": x["Image"]})
escribir("ALTURAS_CUARTOS.csv", fin_c)
for src, tag in ((A, "A"), (B, "B")):
    if os.path.isfile(os.path.join(src, "NOTAS.md")):
        shutil.copy2(os.path.join(src, "NOTAS.md"), os.path.join(au, f"ALTURAS_NOTAS_{tag}.md"))
print(f"alturas: A {len(fa)} / B {len(fb)} walls; cuartos A {len(ca)} / B {len(cb)}; resueltas {len(resol)}; A != B sin resolver {len(dif)}")
