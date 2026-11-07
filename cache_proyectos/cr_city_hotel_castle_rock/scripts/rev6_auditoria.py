#!/usr/bin/env python3
"""rev6 = rev5 + auditoría adversarial de COORDINACIÓN (7-nov-2026). Corre después de rev5_codigo.py (E2 vive en banos_cbu.py,
O1 en perimetros_angle.py, E3 en chequeos_biblioteca.be_cf10).
 E1: CLG-L1-11 'LOBBY coffers' fuera. 2/A7.31 y 4/A7.31 imprimen '1'-11 1/4" RATED ASSEMBLY' con el nivel 12'-0 3/4" en su
     underside; 7/A7.31 pone 12'-0 3/4" en el underside de la membrana rated y el cielo suspendido (T grid + ceiling panel) en
     11'-0". El tag de los coffers 'GYP-1 12'-0 3/4"' (1/A7.31, A3.01) = la membrana FS-1 de L1, ya cargada (7,928.8 SF). A0.08:
     'IN THE LOBBY ... WHERE CEILING IS INTENDED TO BE FLAT, GC MAY ADD LAYER OF GYP BD OR INCREASE CHANNEL DEPTH' = opción del GC.
 O2: cove de corridors 7/A7.23 en los 3 niveles con la cara inferior impresa 4 1/2" = 0.375 ft (el 7 3/4" es el DIFFUSER BOX,
     HVAC) + cara vertical 6 1/2" = 0.542 ft; L2 traía 1.0 ft."""
import json, re
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
cambios = []
# ---------- E1
fuera = [x for x in c['misc_items'] if str(x.get('ref', '')).startswith('CLG-L1-11 ')]
assert len(fuera) == 5, [x['ref'] for x in fuera]
board = next(x['qty'] for x in fuera if x['ref'].endswith(' board'))
c['misc_items'] = [x for x in c['misc_items'] if not str(x.get('ref', '')).startswith('CLG-L1-11 ')]
for t in c.get('rcp_tags') or []:
    if 'CLG-L1-11 board' in (t.get('rows') or []):
        t['rows'] = [r for r in t['rows'] if r != 'CLG-L1-11 board']
        if not t['rows']:
            t.pop('rows'); t.pop('match', None)
            t['none_reason'] = ("LOBBY coffers 'GYP-1 12'-0 3/4\"' = the underside of the 1'-11 1/4\" RATED ASSEMBLY (2/A7.31, 4/A7.31, 7/A7.31): "
                                "the L1 FS-1 membrane, already loaded (L1 FS-1 membrane under the LEVEL 2 floor)")
c.setdefault('excluded_items', []).append({
    "id": "CLG-L1-11", "what": "L1 LOBBY coffers as a separate GYP-1 suspended ceiling (538.5 SF + drywall suspension)",
    "why": "2/A7.31 & 4/A7.31 print '1'-11 1/4\" RATED ASSEMBLY' with the 12'-0 3/4\" level at its underside; 7/A7.31 puts 12'-0 3/4\" at the underside of "
           "the rated membrane and the suspended ceiling at 11'-0\": the coffer ceiling IS the FS-1 membrane of L1 (loaded once, 7,928.8 SF). "
           "A0.08 'GC MAY ADD LAYER OF GYP BD OR INCREASE CHANNEL DEPTH' where the lobby ceiling is intended flat = GC option, not in the base.",
    "source": "2/A7.31, 4/A7.31, 7/A7.31, 1/A7.31, A0.08 FS-1 note"})
cambios.append({"n": "E1", "que": "LOBBY coffers CLG-L1-11 removed (= FS-1 membrane already loaded)", "delta": {
    "5/8\" Type X SF": -board, "main tee LF": -134.62, "cross tee LF": -403.88, "angle LF": -92.82, "hanger wire": -17.0},
    "fuente": "2/A7.31, 4/A7.31, 7/A7.31; A0.08"})
# ---------- O2
SOF = {s['id']: s for s in c.get('framed_soffits') or []}
for sid in ('SOF-L2-01', 'SOF-L2-02'):
    s = SOF[sid]; lf = s['lf']
    old = next(f for f in s['faces'] if f['side'] == 'bottom')
    assert abs(old['width_ft'] - 1.0) < 1e-9, old
    new_q = round(lf * (0.375 + 0.542), 2)
    old['width_ft'] = 0.375
    old['source'] = (f"{lf} LF x (0.375 bottom + 0.542 vertical) = {new_q} [7/A7.23 printed: bottom 4 1/2\" (the 7 3/4\" is the DIFFUSER BOX, HVAC), "
                     f"vertical 6 1/2\"; same on L2, L3, L4]")
    for x in c['misc_items']:
        if x.get('ref') == f'{sid} board':
            antes = x['qty']; x['qty'] = new_q
            x['op'] = f"{lf} LF x (0.375 bottom + 0.542 vertical) = {new_q}"
            x['source'] = re.sub(r"$", " | bottom 4 1/2\" = 0.375 ft printed on 7/A7.23 (7 3/4\" DIFFUSER BOX is HVAC), same width on L2 / L3 / L4", x['source'])
            cambios.append({"n": "O2", "que": f"{sid} corridor cove bottom 1.0 -> 0.375 ft (7/A7.23 4 1/2\")",
                            "delta": {"5/8\" Type X SF": round(new_q - antes, 2)}, "fuente": "7/A7.23"})
c['rev6_cambios'] = cambios
json.dump(c, open(CP, 'w'), indent=1)
for k in cambios:
    print(k)
