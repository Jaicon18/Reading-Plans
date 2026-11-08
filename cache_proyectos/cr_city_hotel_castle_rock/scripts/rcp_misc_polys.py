#!/usr/bin/env python3
"""rev7 (COORDINACIÓN 7-nov, pregunta del usuario en Bluebeam A3.04 "por que unos tienen markups y otros no?"): TODO cielo /
soffit cuantificado en misc_items (CLG- / SOF- / RS6- / CAN- / BW- '... board') lleva markup, igual que ceilings[].
Geometría, en este orden (nada a ojo):
 (a) área medida: rectángulos de la operación (vectores) / polígono FS-1 del mismo cuarto / rectángulos leídos en vectores con
     imagen (perimetros_angle.MANUAL). Hoja: la del rectángulo (A2.0x se dibuja en su RCP A3.0x con el desplazamiento medido
     plan->RCP, etapas/6_markups/offset_plan_rcp.json; /324 = hoja ampliada A7.xx a 18 pt/ft). Si el área medida difiere del
     área cargada (piezas restadas: WS-1, coffers, stair), cada rectángulo se escala desde su centroide al área cargada y la
     causa queda escrita en el Contents.
 (b) soffits de corridor: polilíneas sobre los tramos medidos de la operación (y o x impresos) en la cara del corridor.
 (c) sin coordenadas en la fuente (solo dimensiones de un detalle / sección): LOCALIZADOR en la etiqueta impresa del elemento,
     con la medida cargada y la causa escrita (mismo criterio que rcp_polys 'locator').
Salida: entradas {"misc": true, ...} agregadas a etapas/6_markups/rcp_polys.json (las dibuja markups_rcp.py)."""
import json, re, math, sys
import pymupdf as fitz
W = '/root/cr/work'
c = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
P = json.load(open(f'{W}/etapas/6_markups/rcp_polys.json'))
P = [p for p in P if not p.get('misc')]
OFF = json.load(open(f'{W}/etapas/6_markups/offset_plan_rcp.json'))
D = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
SHEET_PG = {v: int(k) - 1 for k, v in json.load(open(f'{W}/etapas/SHEET_MAP.json')).items()}
sys.path.insert(0, f'{W}/scripts')
src_pa = open(f'{W}/scripts/perimetros_angle.py').read()
MANUAL = eval(re.search(r"MANUAL = (\{.*?\n\})", src_pa, re.S).group(1))
RX = re.compile(r"\(\s*(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\)\s*[*x]\s*\(\s*(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\)")
PISO = {'L1': ('A2.01', 'A3.01'), 'L2': ('A2.02', 'A3.02'), 'L3': ('A2.03', 'A3.03'), 'L4': ('A2.04', 'A3.04')}


def rr(t):
    return [tuple(sorted((float(a), float(b)))) + tuple(sorted((float(cc), float(d)))) for a, b, cc, d in RX.findall(t)]


def a_rcp(fl, rects):
    dx, dy = OFF[fl]
    return [(x0 + dx, x1 + dx, y0 + dy, y1 + dy) for x0, x1, y0, y1 in rects]


def capas(x):
    m = re.search(r"x\s*(\d+)\s*layer", str(x.get('op', '')))
    return int(m.group(1)) if m else 1


def cerca(sheet, txt):
    r = D[SHEET_PG[sheet]].search_for(txt)
    return (r[0].x0, r[0].y1 + 6) if r else None


def zigzag(x, y, lf, esc, ancho=380.0, paso=10.0):
    """polilínea de largo exacto lf (ft) a la escala esc, en tramos horizontales de <= ancho pt."""
    L = lf * esc; n = max(1, math.ceil(L / ancho)); s = L / n
    return [[[x, y + k * paso], [x + s, y + k * paso]] for k in range(n)]   # tramos iguales (sin un último tramo mínimo)


import glob as _g
WHERE_TXT = ""
WHERE_ROWS = []


def where_de(fam):
    """'Where it comes from' del renglón del Material Summary de ese board (W.R. / Type C / Type X / cement / shaftliner)."""
    f = str(fam or "")
    for mat, w in WHERE_ROWS:
        if ("W.R" in f) == ("W.R" in mat) and ("Type C" in f) == ("Type C" in mat) and ("Type X" in f) == ("Type X" in mat) \
                and ("cement" in f.lower()) == ("cement" in mat.lower()) and re.search(r"(?i)gyp|board|cement|shaftliner", mat):
            return w
    return WHERE_TXT
_xl = sorted(_g.glob(f'{W}/etapas/8_excel/CR_City_Hotel_Takeoff_FINAL_rev*.xlsx'))
if _xl:
    import openpyxl
    _ms = openpyxl.load_workbook(_xl[-1], read_only=True)["Material Summary"]
    WHERE_ROWS = [(str(r[0] or ""), str(r[8] or "")) for r in _ms.iter_rows(min_row=4, values_only=True)]
    WHERE_TXT = " ".join(w for _, w in WHERE_ROWS)
fs1 = {}
for cx in c.get('ceilings') or []:
    m = re.findall(r"\b([1-4]\d\d)\b", cx['room'])
    if m and cx.get('contorno_polygon') and str(cx.get('contorno', {}).get('sheet', '')).startswith('A2.0'):
        P_ = cx['contorno_polygon']; P_ = P_ if isinstance(P_[0][0], (int, float)) else P_[0]   # rev9: contorno medido (rect. envolvente)
        fs1[(cx['room'][:2], m[0])] = [(min(q[0] for q in P_), max(q[0] for q in P_), min(q[1] for q in P_), max(q[1] for q in P_))] if len(P_) == 4 else rr(cx.get('source', ''))
    elif m and rr(cx.get('source', '')):
        fs1[(cx['room'][:2], m[0])] = rr(cx['source'])
nuevos, LOG = [], []
import glob as _gl
KM = {}
for _f in sorted(_gl.glob(f'{W}/etapas/4_canon/rev9/contornos_*.json')):   # rev9: contornos MEDIDOS (caras de walls / recorrido real)
    for _k, _v in json.load(open(_f)).items():
        KM.setdefault(_k, {}).update(_v)
for _v in KM.values():   # N/HOJA limpia (la primera cita N/HOJA del texto del medidor)
    _m = re.search(r"\b\d{1,2}/A\d\.\d\d\b", str(_v.get('nhoja') or ''))
    _v['nhoja'] = _m.group(0) if _m else _v.get('sheet')

for x in c['misc_items']:
    ref = str(x.get('ref', ''))
    if not ref.endswith(' board') or not re.match(r"(CLG|SOF|RS6|CAN|BW)-", ref):
        continue
    rid = ref[:-6]; fl = rid.split('-')[1][:2]; src = x.get('source', ''); lay = capas(x)
    cits = re.findall(r"\b(\d{1,2}/A\d\.\d\d)\b", (x.get('detail') or '') + ' ' + src)
    wtx = where_de(x.get('familia'))
    nh = next((ct for ct in cits if ct in wtx), next((ct for ct in re.findall(r"\b(\d{1,2}/A\d\.\d\d)\b", wtx)), cits[0] if cits else None))   # la N/HOJA que el Material Summary ya cita
    e = {"misc": True, "nhoja": nh, "id": rid, "board": x.get('familia'), "detail": (x.get('detail') or '')[:80], "qty_board_sf": x['qty']}
    if rid.startswith(('CLG', 'RS6', 'CAN')):
        area = round(x['qty'] / lay, 2); e.update(kind="area", sf=area, layers=lay)
        rects, sheet, como = None, None, None
        if rid in KM and (KM[rid].get('polygons_final') or KM[rid].get('polygons') or KM[rid].get('polygon')):
            k_ = KM[rid]; sheet = k_['sheet']; pols = k_.get('polygons_final') or k_.get('polygons') or [k_['polygon']]
            if k_.get('factor_pendiente'):
                e['sf'] = round(e['sf'] / float(k_['factor_pendiente']), 2)
            if sheet in (PISO[fl][0],):
                dx, dy = OFF[fl]; pols = [[[q[0] + dx, q[1] + dy] for q in P_] for P_ in pols]; sheet = PISO[fl][1]
            e.update(sheet=sheet, polygons=pols, cause=f"contour measured in vectors on {str(k_.get('nhoja')).split(' (')[0]} (wall faces; openings as keyhole)"
                     + (f"; board = drawn plan area x slope factor {k_['factor_pendiente']}" if k_.get('factor_pendiente') else ""))
            nuevos.append(e); continue
        if rid in MANUAL:
            sheet, rects, _, que = MANUAL[rid]; como = f"room read in vectors on {sheet} ({que})"
        elif rr(src):
            rects = rr(src)
            if '/324' in src:
                m = re.search(r"\b(A7\.\d\d)\b", src); sheet = m.group(1) if m else 'A7.31'
            else:
                sheet = PISO[fl][0]
            como = f"rectangle(s) of the measured operation on {sheet}"
        else:
            mL = re.search(r"x(\d+\.?\d*)-(\d+\.?\d*), vertical coord (\d+\.?\d*)-(\d+\.?\d*)", src)
            num = re.findall(r"\b([1-4]\d\d)\b", src.split('|')[0])
            if mL:
                rects = [tuple(float(v) for v in mL.groups())]; sheet = 'A7.31'; como = "lobby polygon of the operation on 1/A7.31"
            elif num and (fl, num[0]) in fs1:
                rects = fs1[(fl, num[0])]; sheet = PISO[fl][0]; como = f"polygon of the FS-1 entry of room {num[0]} on {sheet}"
        if rects and sheet in (PISO[fl][0],):
            rects = a_rcp(fl, rects); sheet = PISO[fl][1]; como += f" -> drawn on its RCP {sheet} (offset plan->RCP {OFF[fl]} pt)"
        if not rects:   # (c) localizador
            sheet, anchor, dims = {
                "CLG-L2-64": ("A3.02", "219", (2 * 10.85, 24.73)),
                "RS6-L3": ("A3.03", None, (6.46, 66.17)),
                "CAN-L1-ENTRY": ("A3.01", "VESTIBULE", (12.0, 4.85))}.get(rid, (PISO[fl][1], None, None))
            esc = 9.0
            if rid == "RS6-L3":   # franja medida x 1007.35-1065.5 (A2.03), largo 66.17 ft sobre 301-304 desde la fachada norte
                x0 = 1007.35 + OFF['L3'][0]; y0 = 353.6 + OFF['L3'][1]
                rects = [(x0, x0 + 6.46 * esc, y0, y0 + 66.17 * esc)]
                como = "strip width measured (1065.5-1007.35)/9 on A2.03/A2.04; length 66.17 ft from the north facade over rooms 301-304"
            else:
                pt = cerca(sheet, anchor) if anchor else None
                if not pt and anchor and cerca(PISO[fl][0], anchor):   # etiqueta solo en el floor plan -> su RCP con el desplazamiento
                    q = cerca(PISO[fl][0], anchor); pt = (q[0] + OFF[fl][0], q[1] + OFF[fl][1])
                if not pt:
                    LOG.append({"id": rid, "falla": f"sin ancla '{anchor}' en {sheet}"}); continue
                w, h = dims if dims else (math.sqrt(area), math.sqrt(area))
                rects = [(pt[0], pt[0] + w * esc, pt[1], pt[1] + h * esc)]
                como = f"LOCATOR at '{anchor}' on {sheet} (entry canopy at the lobby vestibule; the source gives only dimensions: {src.split('|')[0][:120].strip()})"
        med = sum((r[1] - r[0]) * (r[3] - r[2]) for r in rects) / (18.0 if sheet.startswith('A7') else 9.0) ** 2
        k = math.sqrt(area / med) if med else 1.0
        if abs(k - 1) > 0.0025:
            rects = [((r[0] + r[1]) / 2 - (r[1] - r[0]) * k / 2, (r[0] + r[1]) / 2 + (r[1] - r[0]) * k / 2,
                      (r[2] + r[3]) / 2 - (r[3] - r[2]) * k / 2, (r[2] + r[3]) / 2 + (r[3] - r[2]) * k / 2) for r in rects]
            como += f"; measured {med:.1f} SF scaled about each centroid to the loaded {area} SF (pieces deducted in the operation)"
        e.update(sheet=sheet, polygons=[[[r[0], r[2]], [r[1], r[2]], [r[1], r[3]], [r[0], r[3]]] for r in rects], cause=como)
    else:   # SOF / BW: polilínea, Length = LF, Depth = ancho desarrollado
        m = re.match(r"\s*(\d+\.?\d*)\s*LF x \((\d+\.?\d*) bottom \+ (\d+\.?\d*) vertical\)", x['op']) or None
        if m:
            lf, dep = float(m.group(1)), float(m.group(2)) + float(m.group(3))
        elif re.match(r"\s*(\d+\.?\d*) LF x (\d+\.?\d*) ft", x['op']):
            m = re.match(r"\s*(\d+\.?\d*) LF x (\d+\.?\d*) ft", x['op']); lf, dep = float(m.group(1)), float(m.group(2))
        elif re.match(r"\s*(\d+\.?\d*) LF x (\d+\.?\d*) ft vertical", x['op']):
            m = re.match(r"\s*(\d+\.?\d*) LF x (\d+\.?\d*) ft vertical", x['op']); lf, dep = float(m.group(1)), float(m.group(2))
        else:
            m = re.match(r"\s*(\d+\.?\d*) x \((\d+\.?\d*) bottom \+ (\d+\.?\d*) face\)", x['op'])
            lf, dep = float(m.group(1)), float(m.group(2)) + float(m.group(3))
        dx2, dy2 = OFF['L2']; dx3, dy3 = OFF['L3']
        LINEAS = {   # tramos medidos de la operación (coordenadas de A2.0x) en la cara del corridor -> RCP
            "SOF-L2-01": ("A3.02", [[[865.2, 446.8 + dy2], [865.2, 1206.0 + dy2]], [[812.8, 523.2 + dy2], [812.8, 1004.5 + dy2]],
                                    [[812.8, 1141.2 + dy2], [812.8, 1271.0 + dy2]]],
                          "E side y 446.8-1206.0, W side y 523.2-1004.5 and 1141.2-1271.0 (operation) on the corridor 216 faces"),
            "SOF-L2-02": ("A3.02", [[[855.7 + dx2, 1212.0 + dy2], [1421.5 + dx2, 1212.0 + dy2]], [[1421.5 + dx2, 1141.6 + dy2], [1421.5 + dx2, 1209.0 + dy2]],
                                    [[1421.5 + dx2, 1144.6 + dy2], [1617.35 + dx2, 1144.6 + dy2]], [[799.2 + dx2, 1271.0 + dy2], [1478.0 + dx2, 1271.0 + dy2]]],
                          "N 855.7-1421.5 / 1141.6-1209.0 / 1421.5-1617.35 and S 799.2-1478.0 (operation) on the corridor 218 faces"),
            "SOF-L3-316": ("A3.03", [[[812.6, 441 + dy3], [812.6, 1206 + dy3]], [[866.0, 441 + dy3], [866.0, 1206 + dy3]]],
                           "2 sides y 441-1206 (operation) on the corridor 316 faces"),
            "SOF-L3-318": ("A3.03", [[[799.5 + dx3, 1271 + dy3], [1484.6 + dx3, 1271 + dy3]], [[799.5 + dx3, 1212 + dy3], [799.5 + 62.8 * 9 + dx3, 1212 + dy3]],
                                     [[1424.5 + dx3, 1144.5 + dy3], [1424.5 + 21.8 * 9 + dx3, 1144.5 + dy3]],
                                     [[1424.5 + dx3, 1144.5 + dy3], [1424.5 + dx3, 1144.5 + 9.4 * 9 + dy3]]],
                           "S 799.5-1484.6, N 62.8 ft, jog 21.8 ft, returns 9.4 ft (operation) on the corridor 318 faces"),
        }
        if rid in KM and KM[rid].get('lines'):
            k_ = KM[rid]; sheet, lines = k_['sheet'], k_['lines']
            como = f"run measured in vectors on {str(k_.get('nhoja')).split(' (')[0]} (drawn soffit / beam lines)"
        elif rid in LINEAS:
            sheet, lines, como = LINEAS[rid]
        else:
            sheet, anchor = {"SOF-L1-01": ("A7.31", "GYP-1 12' - 0 3/4\""), "SOF-L4-01": ("A6.01", "GYP BD SOFFIT"),
                             "SOF-L4-02": ("A3.04", "412"), "BW-L1-RETAIL": ("A3.01", "WRAP BOTTOM")}[rid]
            pt = cerca(sheet, anchor)
            if not pt:
                LOG.append({"id": rid, "falla": f"sin ancla '{anchor}' en {sheet}"}); continue
            esc = 18.0 if sheet.startswith(('A7', 'A6')) else 9.0
            lines = zigzag(pt[0], pt[1] + 8, lf, esc)
            como = f"LOCATOR at '{anchor}' on {sheet}: LF of the operation ({x['op']}); the plan geometry is not drawn in the source"
        esc = 18.0 if sheet.startswith(('A7', 'A6')) else 9.0
        L = sum(math.dist(a, b) for a, b in lines) / esc
        if abs(L - lf) > 1e-6 and rid in KM and KM[rid].get('lines'):   # recorrido medido: el LF cargado es el medido
            lf = round(L, 2)
        if abs(L - lf) > 1e-6:   # largo exacto = LF cargado (escala la última línea)
            (a, b) = lines[-1]; s_ = math.dist(a, b); falta = (lf - L) * esc
            f = (s_ + falta) / s_; lines[-1] = [a, [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]]
            como += f"; last segment adjusted {L:.2f} -> {lf} LF (loaded)"
        e.update(kind="line", sheet=sheet, lines=lines, lf=lf, depth_ft=round(dep, 4), cause=como)
    nuevos.append(e)
json.dump(P + nuevos, open(f'{W}/etapas/6_markups/rcp_polys.json', 'w'), indent=1)
json.dump({"agregados": [n['id'] for n in nuevos], "fallas": LOG}, open(f'{W}/etapas/6_markups/rcp_misc_log.json', 'w'), indent=1)
print(len(nuevos), "misc markups;", "fallas", LOG)
