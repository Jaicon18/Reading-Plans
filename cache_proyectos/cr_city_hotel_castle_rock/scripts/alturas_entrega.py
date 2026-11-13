"""U-175 / U-176 (CR City Hotel rev19): copia las dos lecturas ciegas de alturas a la entrega.
Auditoria/ALTURAS_IMPRESAS_A.csv / _B.csv, ALTURAS_CUARTOS_A / _B, imágenes en Auditoria/alturas_img/A y /B (ruta relativa), y la tabla
final ALTURAS_IMPRESAS.csv / ALTURAS_CUARTOS.csv = A cuando A = B (± 1/4"); donde A != B, la fila resuelta de
<dir>/ALTURAS_AB_RESOLUCION.csv (Wall ID, Resolution, Image, Printed H, Source, Operation, Status) con su recorte dirigido.
Uso: alturas_entrega.py <dir con A/ y B/> <carpeta_entrega_rev>"""
import csv
import os
import json
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
        cols = list(dict.fromkeys(k for r in filas for k in r))          # rev20: columnas 'side' / 'faces' (BE-CR37) en los renglones SOF / BW
        w = csv.DictWriter(f, fieldnames=cols, restval="")
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
# rev20 / BE-CR35 (U-176 (1)): soffits / beam wraps con Depth en Bluebeam (= ancho desarrollado del board por LF, no una altura de wall)
# pasan por la DOBLE LECTURA CIEGA: H-A / H-B (scratchpad blind_sof/A, /B, 12-nov) se agregan a ALTURAS_IMPRESAS_A / _B con su recorte, y la
# tabla final toma la resolución (A = B, o el mayor medido / la cota impresa, U-017) - ningún renglón "not blind"
I20 = '/root/cr/work/etapas/4_canon/img/rev20'
_bw = '/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad/bw_resol/BW_RESOL.json'
_bwr = json.load(open(_bw)) if os.path.isfile(_bw) else None
SOFS = []   # (ids, A, B, final, fuente, operación, estado, imgA, imgB, resolución)
_corr_src = ("7/A7.23 WALL DETAIL - CORRIDOR CEILING (3/4\" = 1'-0\"): per side corridor face '6 1/2\"' + box bottom '4 1/2\"' + box face to the cove "
             "'4 1/2\"' + cove bottom '7 3/4\"' = 23 1/4\"; face against the wall = 'WOOD WALL PANEL RE: ELEVATIONS' (not drywall); 1/A7.23 RCP "
             "'8' - 4 1/2\"' = bottom of both boxes. Soffit board developed width per LF; Depth in Bluebeam = board strip, not a wall height")
for k_ in ("SOF-L2-01", "SOF-L2-02", "SOF-L3-316", "SOF-L3-318", "SOF-L4-02"):
    SOFS.append((k_, 1.94, 1.94, 1.9375, _corr_src, "(6.5 + 4.5 + 4.5 + 7.75) / 12 = 1.9375", "CONFIRMED", f"{I20}/SOF-corridor_7-A7.23_DIMS.png",
                 f"{I20}/B_SOF-CORR_A7.23_det7_dims.png", "H-A = H-B (each face printed on 7/A7.23); 7/A7.23 prints the corridor face 6 1/2\" and the box face 4 1/2\" on one side; on the other side they close with the printed 2\" step (2\" + 4 1/2\" = 6 1/2\", 6 1/2\" - 2\" = 4 1/2\"): the same 23 1/4\" per side; DIFFUSER BOX 5 1/4\" loaded gross, Review Item (one side 1.50 ft at diffusers)"))
for k_ in ("SOF-L2-SCN", "SOF-L2-SCS", "SOF-L3-SCN", "SOF-L3-SCS", "SOF-L4-SCN", "SOF-L4-SCS"):
    SOFS.append((k_, 3.06, 3.02, 5.04, "12/A9.03 'SOFFIT AROUND HOUSING' (1 1/2\" = 1'-0\", no dimension printed): measured at the printed scale outer face 14.87\" + "
                 "bottom 4.49\" + inner face 14.37\" + return 3.00\" + shaft-side face 23.73\" = 60.46\". Soffit board developed width per LF; Depth in Bluebeam = board strip",
                 "(14.87 + 4.49 + 14.37 + 3.00 + 23.73) / 12 = 5.04", "DERIVED", f"{I20}/SOF-SC_12-A9.03.png", f"{I20}/B_SOF-SC_A9.03_det12.png",
                 "H-A 3.06 / H-B 3.02 both OMITTED the shaft-side gypsum face (23.73\", on wood blocks in front of the masonry shaft wall); U-181 audit "
                 "re-measured all 5 faces in vectors = 5.04 (rev19 5.039); image Auditoria U181_2_A903_det12_faces"))
for k_ in ("SOF-L2-01P", "SOF-L2-02P", "SOF-L3-316P", "SOF-L3-318P", "SOF-L4-02P"):   # rev20: cara de la caja derecha en el plenum (7/A7.23)
    SOFS.append((k_, 0.917, 0.97, 0.9688, "7/A7.23 WALL DETAIL - CORRIDOR CEILING: right-hand soffit box, corridor face drawn as gypsum ABOVE the GYP-1 "
                 "8'-11\" field up to the underside of the rated assembly: printed '9 1/2\"' + '2 1/8\"' = 11 5/8\"; one side only (the diffuser box "
                 "side has no face above the field). Board face height; Depth in Bluebeam = board strip", "(9.5 + 2.125) / 12 = 0.9688", "DERIVED",
                 f"{I20}/A_SOF-PLEN_7-A7.23.png", f"{I20}/B_SOF-PLEN_7-A7.23.png",
                 "H-A 0.917 (11\" above the 5/8\" field board) / H-B 0.97 (11 5/8\" to the 8'-11\" line): the printed 9 1/2\" + 2 1/8\" = 11 5/8\" (U-146 larger)"))
for _lv, _rm in (("L2", "217"), ("L3", "317")):   # rev20: lazo de banda del vestíbulo y caja de borde del WS-1 del lobby (1/A7.23, 2/A7.23)
    SOFS.append((f"SOF-{_lv}-{_rm}V", 1.94, 1.46, 1.9375, f"Lobby {_rm} vestibule band loop: same section as the corridor band 7/A7.23 (printed 7 3/4\" cove bottom, "
                 "4 1/2\" box face, 4 1/2\" box bottom, 6 1/2\" field face) = 23 1/4\" one side. Soffit board developed width per LF; Depth in Bluebeam = board strip",
                 "(7.75 + 4.5 + 4.5 + 6.5) / 12 = 1.9375", "DERIVED", f"{I20}/A_SOF-LOBBY_{_lv}.png", f"{I20}/B_SOF-LOBBY_{_lv}.png",
                 "H-A 1.94 (7/A7.23 section) / H-B 1.46 (left out the cove bottom 7 3/4\" and used 6 1/2\" on both box faces): the printed 7/A7.23 section governs"))
    SOFS.append((f"SOF-{_lv}-{_rm}B", 1.29, 2.21, 2.2083, f"Lobby {_rm} border box around the WS-1 panel: tags 8'-0\" (border) and GYP-1 8'-11\" (field) -> 11\" faces; "
                 "bottom 4 1/2\" and board on both faces full height drawn in 5/A7.23 and 6/A7.23. Soffit board developed width per LF; Depth in Bluebeam = board strip",
                 "(11 + 4.5 + 11) / 12 = 2.2083", "DERIVED", f"{I20}/A_SOF-LOBBY_{_lv}.png", f"{I20}/B_SOF-LOBBY_{_lv}.png",
                 "H-A 1.29 (outer face + bottom) / H-B 2.21 (both faces + bottom, as 5/A7.23 and 6/A7.23 draw): drawn = loaded, the larger"))
SOFS.append(("BW-L1-NORTH", 1.4733, 1.38, 1.4733, "FS-1 wrap of the grid-1 north edge beams W24X68 (MF) D-H and W24X55 (MF) B-D (S1.02): one exposed side "
             "(south) d - 16 1/2\" + bottom bf + build-up 1 1/8\" (A5.00), AISC d / bf; 4/S3.08 governs. Beam wrap developed width per LF; Depth = board strip",
             "(29.06 x 1.54 + 17.06 x 1.36) / 46.12 = 1.4733", "DERIVED", f"{I20}/A_BW-NORTH_S102.png", f"{I20}/B_BW-NORTH_S102.png",
             "H-A 67.9 SF (1.4733) / H-B 63.6 SF (1.38, without build-up at one corner): the larger"))
SOFS.append(("SOF-L1-01", 1.29, 1.29, 1.25, "5/A7.31 DETAIL - LOBBY CEILING: printed downstand face '10 3/4\"' + half of the shared bottom (7 1/2\" + 2 x 1/2\" = 8 1/2\") per LF of "
             "coffer perimeter = 15\". Soffit board developed width per LF; Depth in Bluebeam = board strip", "(10.75 + 8.5 / 2) / 12 = 1.25", "DERIVED",
             f"{I20}/SOF-L1-01_5-A7.31.png", f"{I20}/B_SOF-L1-01_A7.31_det5.png",
             "H-A = H-B 1.29 with the MEASURED face 11.24\"; U-017: the printed '10 3/4\"' governs -> 1.25 (the 1/2\" behind the wood border is the same face); Review Item"))
SOFS.append(("SOF-L4-01", 8.58, 8.58, 8.59, "11/A6.01 'GYP BD SOFFIT AT FCU. CONTINUES FULL WIDTH OF STAIR.' (1/4\" = 1'-0\", no soffit dimension printed): bottom 6.59 ft + face 2.0 ft "
             "measured at the printed scale; run = 7/A6.01 '8' - 8 3/4\"'. Soffit board developed width per LF", "6.59 + 2.0 = 8.59", "DERIVED",
             f"{I20}/SOF-L4-01_11-A6.01.png", f"{I20}/B_SOF-L4-01_A6.01_det11.png", "H-A = H-B 8.58; canon 8.59 (0.01 ft, within 1/4\"): canon kept"))
if _bwr:
    SOFS.append(("BW-L1-RETAIL", _bwr["A"], _bwr["B"], _bwr["final"], _bwr["source"], _bwr["op_alturas"], "DERIVED", f"{I20}/BW-L1-RETAIL_S1.02.png",
                 f"{I20}/B_BW-L1-RETAIL_S1.02.png", _bwr["resolucion"]))
_ya = {r["Wall ID"] for r in final}
# BE-CR37 (rev20, lados_fallas): cada cara con UN solo lado ('both' = la misma cota en los dos lados del corridor); la derivación de qué
# lado está impreso va en la Resolution, no en 'faces' (las palabras de la nota se leían como lados mezclados)
LADOS = {"corr": ("both", "corridor face 6 1/2\" both; box bottom 4 1/2\" both; box face to cove 4 1/2\" both; cove bottom 7 3/4\" both"),
         "sc": ("single", "outer face 14.87\" single; bottom 4.49\" single; inner face 14.37\" single; return 3.00\" single; shaft-side face 23.73\" single (12/A9.03 measured)"),
         "cof": ("single", "downstand face 10 3/4\" single (5/A7.31 printed); half of the shared bottom 8 1/2\" / 2 single (7 1/2\" + 2 x 1/2\" printed)"),
         "plen": ("single", "right-box corridor face above the GYP-1 field 11 5/8\" single (7/A7.23 printed 9 1/2\" + 2 1/8\")"),
         "lobv": ("single", "cove bottom 7 3/4\" single; box face 4 1/2\" single; box bottom 4 1/2\" single; field face 6 1/2\" single (7/A7.23 printed)"),
         "lobb": ("single", "outer face 11\" single; bottom 4 1/2\" single; inner face 11\" single (5/A7.23, tags 8'-0\" / 8'-11\")"),
         "bwn": ("single", "one beam side face (d - 16 1/2\" + 1 1/8\") single; bottom bf + 1 1/8\" single (4/S3.08, AISC)"),
         "l4": ("single", "FCU face 2.0 ft single; bottom 6.59 ft single (11/A6.01 measured)")}
def _grupo(k):
    if k in ("SOF-L2-217V", "SOF-L3-317V"):
        return "lobv"
    if k in ("SOF-L2-217B", "SOF-L3-317B"):
        return "lobb"
    if k == "BW-L1-NORTH":
        return "bwn"
    if k.endswith("P") and k[:-1] in ("SOF-L2-01", "SOF-L2-02", "SOF-L3-316", "SOF-L3-318", "SOF-L4-02"):
        return "plen"
    return "corr" if k in ("SOF-L2-01", "SOF-L2-02", "SOF-L3-316", "SOF-L3-318", "SOF-L4-02") else "sc" if "-SC" in k else "cof" if k == "SOF-L1-01" \
        else "l4" if k == "SOF-L4-01" else "bw"
for k_, a_, b_, f_, s_, o_, st_, ia_, ib_, res_ in SOFS:
    fa.append({"Wall ID": k_, "Printed H": f"{a_}", "Source": "H-A blind reading (soffit developed width): " + s_, "Operation": "", "Status": "DERIVED",
               "Image": img(ia_, A, "A")})
    fb.append({"Wall ID": k_, "Printed H": f"{b_}", "Source": "H-B blind reading (soffit developed width): " + s_, "Operation": "", "Status": "DERIVED",
               "Image": img(ib_, B, "B")})
    _ir = f"{I20}/SOF-SC_12-A9.03_5faces_U181.png" if "-SC" in k_ else f"{I20}/SOF-PLEN_7-A7.23_RES.png" if _grupo(k_) == "plen" else ia_   # U-181: caras circuladas
    x_ = {"Wall ID": k_, "Resolution": res_, "Image": img(_ir, R, "resolucion"), "Printed H": f"{f_:.4f}", "Source": s_, "Operation": o_, "Status": st_}
    side_, faces_ = LADOS.get(_grupo(k_)) or ((_bwr or {}).get("side", "single"), (_bwr or {}).get("faces", ""))
    x_["side"], x_["faces"] = side_, faces_
    resol[k_] = x_
    final = [r for r in final if r["Wall ID"] != k_]
    final.append({"Wall ID": k_, "Printed H": x_["Printed H"], "Source": s_, "Operation": o_, "Status": st_, "Image": x_["Image"],
                  "side": side_, "faces": faces_})
# U-181 (rev19) restaurado en rev20: renglones partidos de un wall ya leído (cara de baño W.R. de los demising DW.4, A0.06 GN 11) = misma
# altura que su renglón padre ' A'. BE-CR35: van también en A y en B (la lectura ciega del padre, misma cara física), no solo en la final.
_can = json.load(open('/root/cr/work/etapas/4_canon/takeoff_canon.json'))
_por = {r["Wall ID"]: r for r in final}
_pa, _pb = {r["Wall ID"]: r for r in fa}, {r["Wall ID"]: r for r in fb}
_ids = set(_por)
for _w in _can['walls'] + _can['existing_walls']:
    _i = _w['id']
    _p = _i[:-2] + ' A' if len(_i) > 2 and _i[-2] == ' ' else None
    if _i in _ids or _p not in _por or _p not in _pa or _p not in _pb:
        continue
    _pre = f"[split row of {_p} (bath face W.R., A0.06 GN 11), same height as its parent] "
    for _lst, _src in ((final, _por), (fa, _pa), (fb, _pb)):
        _r = dict(_src[_p]); _r["Wall ID"] = _i; _r["Source"] = _pre + _r["Source"]
        _lst.append(_r)
    _ids.add(_i)
escribir("ALTURAS_IMPRESAS_A.csv", fa)
escribir("ALTURAS_IMPRESAS_B.csv", fb)
escribir("ALTURAS_AB_RESOLUCION.csv", list(resol.values()))
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
