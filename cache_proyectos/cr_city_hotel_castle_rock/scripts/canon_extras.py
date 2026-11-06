#!/usr/bin/env python3
"""CR City Hotel - campos del canon que leen los chequeos (BE-CR29, recheck v81cf57); NO cambian cantidades.
(1) framed_soffits: cada soffit de la lectura (etapas/2_lectura/A/L*.json 'soffits') con sus caras impresas (fondo + cara vertical, o
    solo la vertical en un coffer), su framing tal como lo lee la lectura (7/A7.23: side boxes 2x wood = Div. 06 EXCLUDED) y su fuente.
    Las cantidades siguen en misc_items SOF-* (build_canon); canon.py no lee framed_soffits.
(2) types_none_reason: cada type del Partition Type Schedule (fichas.json) que ningún wall usa -> A0.06 GN 2 'NOT ALL PARTITION
    TYPES DELINEATED MAY BE USED' (no tagueado en ninguna planta del set; barrido de tags en etapas/1_inventario)."""
import json, glob, re
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
