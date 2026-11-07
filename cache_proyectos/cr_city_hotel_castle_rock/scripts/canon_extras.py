#!/usr/bin/env python3
"""CR City Hotel - campos del canon que leen los chequeos (BE-CR29, recheck v81cf57); NO cambian cantidades.
(1) framed_soffits: cada soffit de la lectura (etapas/2_lectura/A/L*.json 'soffits') con sus caras impresas (fondo + cara vertical, o
    solo la vertical en un coffer), su framing tal como lo lee la lectura (7/A7.23: side boxes 2x wood = Div. 06 EXCLUDED) y su fuente.
    Las cantidades siguen en misc_items SOF-* (build_canon); canon.py no lee framed_soffits.
(2) types_none_reason: cada type del Partition Type Schedule (fichas.json) que ningún wall usa -> A0.06 GN 2 'NOT ALL PARTITION
    TYPES DELINEATED MAY BE USED' (no tagueado en ninguna planta del set; barrido de tags en etapas/1_inventario)."""
import json, glob, re, collections
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
ref = {str(m.get('ref', '')).replace(' board', ''): m for m in c.get('misc_items') or [] if str(m.get('ref', '')).startswith('SOF-') and str(m.get('ref', '')).endswith(' board')}
fs = []
for f in sorted(glob.glob(f'{W}/etapas/4_canon/resuelto_L*.json')):   # misma fuente que build_canon
    fl = re.search(r"L\d", f.split("/")[-1]).group(0)
    for si, s in enumerate(json.load(open(f)).get('soffits') or []):
        sid = s.get('id') or f"SOF-{fl}-{si + 1:02d}"
        if sid not in ref:
            continue
        op = str(ref[sid].get('op') or '')
        loc = str(s.get('where') or s.get('location') or s.get('room') or '')
        caras = []
        mb = re.search(r"([\d.]+) bottom", op); mv = re.search(r"([\d.]+)(?: ft)? (?:vertical|face)", op)
        if mb and float(mb.group(1)) > 0:
            caras.append({"side": "bottom", "layers": 1, "width_ft": float(mb.group(1)), "source": op})
        if mv and float(mv.group(1)) > 0:
            caras.append({"side": "vertical", "layers": 1, "height_ft": float(mv.group(1)), "source": op})
        if 'coffer' in loc.lower():
            fr = "metal suspension (USG drywall suspension, 2/A7.31 coffers): no studs"
        elif re.search(r"7/A7\.23|cove|band|corridor", loc + str(s.get('detail')), re.I):
            fr = ("7/A7.23 'WALL DETAIL - CORRIDOR CEILING': cove boxes drawn as 2x wood blocking (Div. 06 EXCLUDED, U-139); GYP-1 legend "
                  "'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING' -> R-ALC-01 metal option: 2 lines of soffit track per LF, no studs")
        else:
            fr = ("framing not printed: GYP-1 legend 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING' (no metal studs in either option) "
                  "-> R-ALC-01 metal option: soffit track loaded")
        fs.append({"id": sid, "element": "soffit", "floor": fl, "where": loc, "lf": s.get('lf'), "detail": s.get('detail') or ("7/A7.23 (typ. corridor cove)" if 'A7.23' in fr else None),
                   "framing": fr, "faces": caras, "qty_in": f"misc_items '{sid} board' / '{sid} track'",
                   "note": "vertical face only: coffer perimeter / one side against structure" if len(caras) == 1 else None,
                   "source": ref[sid].get('source')})
c['framed_soffits'] = fs
fi = json.load(open(f'{W}/indep/fichas.json'))['types']
usados = {str(e.get('type_id')) for e in c['existing_walls']}
tnr = c.setdefault('types_none_reason', {})
n = 0
for t in fi:
    if t not in usados and t not in tnr and not any(t.startswith(k + '-') or t == k for k in tnr):
        tnr[t] = "not tagged on any plan of the set (tag sweep etapas/1_inventario): A0.06 GN 2 'NOT ALL PARTITION TYPES DELINEATED MAY BE USED'"
        n += 1
json.dump(c, open(CP, 'w'), indent=1)
print('framed_soffits', len(fs), '| types sin uso con motivo', n, '| soffits en misc sin lectura', sorted(set(ref) - {x['id'] for x in fs}))
# (3) rcp_tags (rev4, BE-CR30): barrido de TODOS los tags de ceiling de gypsum (GYP-x, sin el ':' de la leyenda) impresos en las hojas
#     de RCP del set; cada tag -> sus renglones cargados (ceilings[] / misc '... board') o none_reason con N/HOJA.
import pymupdf as fitz
_D = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
_HS = list(json.load(open(f'{W}/set_texto.json'))['hojas'])
_RET = ("inside RETAIL 124 (between the storefront grid 7 and grid 8; RETAIL 124 room tag and '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY "
        "FUTURE TENANT' on 1/A2.01) = by tenant, RFI-05 (delta +346.4 SF if ours)")
_BATH = r"(?i)^L[234] (Bath \d{3}|\d{3} bath)"
MAPA = {  # (hoja, x, y) del tag impreso -> regex del cuarto en los renglones del canon, o motivo
    ("A3.01", 665, 545): r"^L1 GENERATOR 103", ("A3.01", 1265, 993): _RET, ("A3.01", 1385, 479): r"^L1 TOILET 111",
    ("A3.01", 659, 370): r"^L1 ELEC 104", ("A3.01", 835, 936): r"^L1 LOBBY - field", ("A3.01", 901, 878): r"^L1 LOBBY - coffers",
    ("A3.01", 1277, 472): r"^L1 TOILET 110", ("A3.01", 1331, 439): r"^L1 JANITOR 109", ("A3.01", 752, 1131): r"^L1 ELEVATOR CONTROLS 116",
    ("A3.01", 989, 1052): r"^L1 TOILET 113", ("A3.01", 868, 1052): r"^L1 TOILET 112",
    ("A3.02", 802, 396): r"^L2 Cleaning 215 - GYP-1",
    ("A7.05", 1022, 704): r"^L[23] (Linen 222|Cleaning 223|32[23] closet)", ("A7.05", 1128, 704): r"^L[23] (Linen 222|Cleaning 223|32[23] closet)",
    ("A7.23", 2400, 1002): r"^L[234] (Corridor [23]16|412 Corridor)", ("A7.24", 1223, 1380): r"^L[234] (Corridor [23]18|412 Corridor)",
    ("A7.31", 2097, 1501): _RET, ("A7.31", 2230, 468): r"^L1 (TOILET 11[01]|JANITOR 109)", ("A7.31", 1440, 1162): r"^L1 LOBBY - coffers",
    ("A7.50", 1470, 396): r"^L1 ELEVATOR CONTROLS 116", ("A7.50", 1823, 248): r"^L1 HALL between TOILET 112/113", ("A7.50", 1740, 126): r"^L1 LOBBY south strip",
}
_filas = [(str(m.get('source') or ''), m['ref']) for m in c['misc_items'] if str(m.get('ref', '')).startswith('CLG-') and m['ref'].endswith((' board', ' liner'))]
_filas += [(str(x.get('room') or ''), f"ceilings[{i}] {x.get('assembly', {}).get('id', '')}") for i, x in enumerate(c['ceilings'])]
RX_T = re.compile(r"^(GYP|GWB|GB)-\d{1,2}$")
tags = []
for sh in _HS:
    if not re.match(r"A[37]\.", sh):
        continue
    ws = _D[_HS.index(sh)].get_text('words')
    for w in ws:
        if not RX_T.match(w[4]):
            continue
        x, y = round(w[0]), round(w[1])
        alto = ' '.join(z[4] for z in ws if abs(z[1] - w[3]) < 12 and z[1] > w[1] + 2 and abs(z[0] - w[0]) < 30)[:14]
        k = min((kk for kk in MAPA if kk[0] == sh), key=lambda kk: abs(kk[1] - x) + abs(kk[2] - y), default=None)
        if k is not None and abs(k[1] - x) + abs(k[2] - y) > 6:
            k = None
        ent = {"sheet": sh, "tag": w[4], "height": alto, "xy": [x, y]}
        regla = MAPA.get(k) if k else (_BATH if "8' - 6" in alto else None)
        if regla is None:
            ent['none_reason'] = None
        elif regla.startswith('inside '):
            ent['none_reason'] = regla
        else:
            ent['rows'] = sorted({r for s_, r in _filas if re.search(regla, s_)})
            ent['match'] = regla
        tags.append(ent)
c['rcp_tags'] = tags
c['rcp_tags_sweep'] = {"source": "every word GYP-n / GWB-n / GB-n (not the legend 'GYP-n:') on the A3.xx / A7.xx sheets of the set (pymupdf words)",
                       "per_sheet": dict(collections.Counter(t['sheet'] for t in tags))}
json.dump(c, open(CP, 'w'), indent=1)
sin = [t for t in tags if not t.get('rows') and not t.get('none_reason')]
print('rcp_tags', len(tags), '| sin renglon ni motivo', len(sin), [(t['sheet'], t['xy'], t['height']) for t in sin])
