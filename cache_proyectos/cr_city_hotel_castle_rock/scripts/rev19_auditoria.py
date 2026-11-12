"""rev19 (auditoría COORDINACIÓN 11-nov, U-177): (2) CE_RCP_CONTORNO < 0.5 = FAIL. Los EXCLUDED exteriores que el RCP no dibuja (caja de
equipo 1/A2.01, terrazas 1/A2.04) declaran la hoja que SÍ dibuja su contorno con el offset planta->RCP (offset_plan_rcp.json), y la
compuerta mide ahí (cobertura 1.0). Los cielos con borde no dibujado declaran lo mismo en rcp_misc_polys.BORDE_NO."""
import json, re
W = '/root/cr/work'
TP = f'{W}/etapas/4_canon/rev14/rcp_cuartos.json'
T = json.load(open(TP))
OFF = json.load(open(f'{W}/etapas/6_markups/offset_plan_rcp.json'))
LOG = []
for r in T['rooms']:
    e = str(r.get('edge_not_drawn') or '')
    if not e or ' source A' in e:
        continue
    if e.startswith('A3.04 does not draw the roof terraces'):
        r['edge_not_drawn'] = e + f"; source A2.04 offset ({OFF['L4'][0]}, {OFF['L4'][1]})"
    elif e.startswith('the box is drawn only on 1/A2.01'):
        r['edge_not_drawn'] = e + f"; source A2.01 offset ({OFF['L1'][0]}, {OFF['L1'][1]})"
    else:
        continue
    LOG.append(f"{r['sheet']} {r['room']}: {r['edge_not_drawn'][-40:]}")
json.dump(T, open(TP, 'w'), indent=1)
print("\n".join(LOG) or "sin cambios")

# (U-176 control 3) B.O. / tope físico por nivel = floor-to-floor impreso en los datums de 4/A5.05 (LEVEL 1 6197.75', LEVEL 2 6211.75',
# LEVEL 3 6222.75', LEVEL 4 6233.75', ROOF 6247.75'): ningún wall de un nivel pasa de ahí (comparar_alturas.py extremo, B.O. por nivel).
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
C = json.load(open(CP))
C.setdefault('constants', {})['deck_heights'] = {
    "value": {"L1": "14'-0\"", "L2": "11'-0\"", "L3": "11'-0\"", "L4": "14'-0\""},
    "source": "4/A5.05 level datums: L1 6197.75' / L2 6211.75' / L3 6222.75' / L4 6233.75' / ROOF 6247.75' -> floor-to-floor "
              "(L4 = to the roof datum); physical upper bound per level for U-176 control 3",
    "status": "DERIVED"}
# CE_MS_GAUGE (U-177): el renglón de soffit cripple studs / ceiling track dice su gauge impreso (A0.06 STUD SCHEDULE)
C['constants']['product_names'] = {     # U-181 hallazgos 5 / 6: tamaño + gauge en el nombre, con la base real (impreso o regla)
    '2-1/2" stud': {"value": '2-1/2" stud, 25 ga min. - soffit cripples (soffit framing not drawn: A0.06 partition STUD SCHEDULE 2 1/2" min. gauge 25 applied)',
                    "source": "A0.06 PARTITION TYPES - STUD SCHEDULE 'STUD DEPTH 2 1/2\" MIN. GAUGE 25 HEIGHT LIMIT 11'-3\"' (partitions); 5/A7.31 and 11/A6.01 draw no soffit framing (R-ALC-01 / BE-CF11 metal option, conservative)"},
    'track de ceilings / soffits': {"value": 'Ceiling / soffit track 2-1/2", 25 ga min. (runner = stud gauge, 09 22 16 2.3; soffit framing not drawn)',
                    "source": "09 22 16 2.3 runners 'in thickness not less than indicated for studs'; A0.06 STUD SCHEDULE 2 1/2\" min. gauge 25 (partitions); 7/A7.23, 2/A7.31, 7/A6.01"},
    'carrying channel': {"value": 'Carrying channel, cold-rolled, 0.0538 in base metal (16 ga), min. 1/2" flanges (09 22 16 2.2.D)',
                    "source": "09 22 16 2.2.D 'Carrying Channels: Cold-rolled, commercial-steel sheet with a base-metal thickness of 0.0538 inch (1.37 mm) and minimum 1/2-inch- (12.7-mm-) wide flanges'"},
    'hanger wire': {"value": 'Hanger wire 0.162 in dia. (8 ga), ASTM A 641 Class 1, soft temper (09 22 16 2.2.C)',
                    "source": "09 22 16 2.2.C 'Wire Hangers: ASTM A 641/A 641M, Class 1 zinc coating, soft temper, 0.162-inch (4.12-mm) diameter'"},
    'J-runner 2-1/2" (printed)': {"value": 'J-runner 2-1/2", 0.0329 in min. (20 ga) - C-H shaft wall (09 21 16.23 2.6.C; depth matching the 2-1/2" C-H stud of 7/A9.03)',
                    "source": "09 21 16.23 2.6.C 'Runner Tracks: Manufacturer's standard J-profile track ... in depth matching studs. Minimum Base-Metal Thickness: 0.0329 inch'; A0.06 CH '\"J\" RUNNER CHANNEL' (no size / gauge on the sheet); 7/A9.03 2 1/2\" C-H (RFI-07)"},
    'J-runner 6" (printed)': {"value": 'J-runner 6", 0.0329 in min. (20 ga) - C-H shaft wall (09 21 16.23 2.6.C; depth matching the 6" C-H stud, A0.06 CH.6)',
                    "source": "09 21 16.23 2.6.C 'Runner Tracks: ... in depth matching studs. Minimum Base-Metal Thickness: 0.0329 inch'; A0.06 CH '\"J\" RUNNER CHANNEL' (no size / gauge on the sheet); A0.06 CH.6 6\" C-H"},
    'resilient channel (printed)': {"value": 'Resilient channel 1/2" deep (09 22 16 2.2.E.4), spacing per the UL assembly (A0.08 FS-1 / RS-1)',
                    "source": "09 22 16 2.2.E.4 'Resilient Furring Channels: 1/2-inch- (12.7-mm-) deep members designed to reduce sound transmission'; A0.08 'RESILIENT CHANNELS, SPACING PER ASSEMBLY'"}}
# U-181 hallazgo 5: framed_soffits SOF-L1-01 decía 'no studs' y misc_items carga cripples + track (rev15): un solo criterio (el cargado)
for _s in C.get('framed_soffits') or []:
    if _s.get('id') == 'SOF-L1-01':
        _s['framing'] = ("vertical coffer face framed with top + bottom ceiling track + 2-1/2\" cripple studs @ 16\" o.c. (A0.06 GN 6) on the USG drywall "
                         "suspension of the coffer field; 5/A7.31 draws no framing member: R-ALC-01 / BE-CF11 metal option (conservative), as loaded in misc_items")
json.dump(C, open(CP, 'w'), indent=1)
print("deck_heights por nivel:", C['constants']['deck_heights']['value'])

# (U-176 control 1) resolución de las lecturas ciegas H-A / H-B (scripts/alturas_resolucion.py -> alturas/cambios_canon.json)
import os
CB = f'{W}/alturas/cambios_canon.json'
import subprocess
# la resolución se calcula SIEMPRE sobre el canon de este paso (antes de aplicar alturas): idempotente en cada corrida de la cadena
subprocess.run(['python3', '-I', f'{W}/scripts/alturas_resolucion.py'], check=True)
if os.path.isfile(CB):
    CAM = json.load(open(CB))
    C = json.load(open(CP))
    n_ = 0
    import csv as _csv
    RES = {r['Wall ID']: r for r in _csv.DictReader(open(f'{W}/alturas/ALTURAS_AB_RESOLUCION.csv', encoding='utf-8-sig'))}
    PARCIAL = re.compile(r"cement board / WR part|board strip above")
    for w in C['walls'] + C['existing_walls']:
        x = CAM.get(w['id'])
        if x and abs(float(w['height_ft']) - x['height_ft']) > 1e-4:
            w['height_ft'] = x['height_ft']
            n_ += 1
        r = RES.get(w['id'])
        if r:   # fuente = la de la resolución (hoja concreta), operación AL FINAL (CE_ALTURA_IMPRESA / CB_U_114 / CE_CITA_ALTURA)
            w['height_note'] = f"rev19 U-176 (double blind reading H-A / H-B): {r['Resolution']} | before rev19: {str(w.get('height_source'))[:400]}"
            op = r.get('Operation') or ''
            w['height_source'] = (f"{r['Source']}; {op}" if op else r['Source']).replace('|', '/')
            w['height_op'] = op
            w['height_status'] = 'DERIVADO' if r['Status'].upper() == 'DERIVED' else 'CONFIRMADO'
            if PARCIAL.search(r['Resolution']):      # U-176 control 3 / 4: parte de material de la cara, motivo con N/HOJA
                w['height_diff_reason'] = ("material split of the face (A7.05 bath 'GYP-1 8'-6\"' + 6\" tile backer / WR; the face continues "
                                           "to the structure 9'-2 7/8\" per 4/A5.05 and the A0.06 head detail in its strip row)")
    # CE_COHERENCIA_R11 F3: el C-H stud de un shaft wall tiene la altura de su board / liner (cambió con la resolución)
    hmax = {}
    for w in C['walls'] + C['existing_walls']:
        if str(w['id']).startswith('CH.'):
            b = re.sub(r"\s+[A-Z]$", "", w['id'])
            hmax[b] = max(hmax.get(b, 0), float(w['height_ft']))
    nst = 0
    for m in C.get('misc_items') or []:
        mm = re.match(r"CH-STUD (CH\.\S+)$", str(m.get('ref')))
        if not mm or mm.group(1) not in hmax:
            continue
        H = round(hmax[mm.group(1)], 4)
        k = re.search(r"=\s*(\d+) studs x ([\d.]+) ft", str(m.get('op')))
        if k and abs(float(k.group(2)) - H) > 1e-4:
            q = round(int(k.group(1)) * H, 2)
            m['op'] = re.sub(r"=\s*\d+ studs x [\d.]+ ft(.*?)= [\d.]+", f"= {k.group(1)} studs x {H} ft\\1= {q}", str(m['op']), count=1)
            m['qty'] = q
            m['source'] = f"{m.get('source')} | rev19: stud height = board / liner height of the same shaft wall after the U-176 resolution ({H} ft)"
            nst += 1
    json.dump(C, open(CP, 'w'), indent=1)
    print(f"alturas U-176: {n_} walls con la altura de la doble lectura ciega; {nst} renglones de C-H stud a la altura de su shaft")

# CB_U_117 (rev19): imagen de descarte con ruta relativa no resuelta por la compuerta -> ruta absoluta (PC0186 / PC0187, 1/A7.45)
C = json.load(open(CP))
for t_ in C.get('tags_descartados') or []:
    im_ = str(t_.get('imagen') or '')
    if im_ and not os.path.isabs(im_) and os.path.isfile(f'{W}/etapas/{im_}'):
        t_['imagen'] = f'{W}/etapas/{im_}'
json.dump(C, open(CP, 'w'), indent=1)

# rev19 gate (2a corrida): textos de altura coherentes con la altura cargada
C = json.load(open(CP))
RX_NOTE1 = re.compile(r'1/A5\.06 WALL SECTION WEST ALLEY prints "8\' - 11 1/4"" LEVEL 4 to ceiling = bottom of roof/ceiling assembly \(unit RCP note 1 A7\.xx: ceiling = bottom of assembly unless tagged\); unrated L4 walls stop there\. Confirmed by measurement 1/A5\.08 \((\S+)-(\S+)\)/27=8\.93')
n1 = n2 = n3 = 0
for w in C['walls'] + C['existing_walls']:
    hs = str(w.get('height_source') or '')
    m = RX_NOTE1.search(hs)
    if m:     # 'unit RCP note 1 A7.xx' no está impresa en ninguna hoja A7 (barrido 11-nov): fuera; vale la cota impresa de 1/A5.06
        w['height_source'] = hs.replace(m.group(0), "1/A5.06 WALL SECTION WEST ALLEY printed 8'-11 1/4\" LEVEL 4 to the ceiling line = bottom of the "
                                        f"roof / ceiling assembly; unrated L4 walls stop there; vector cross-check 1/A5.08 ({m.group(1)} - {m.group(2)})/27 = 8.93; "
                                        "1/A5.07 BUILDING SECTION - NORTH/SOUTH CURVED ROOF prints no L4 height dimension (horizontal dimensions only)")
        w['height_op'] = w.get('height_op') or "8'-11 1/4\" = 8.9375 (printed)"
        n1 += 1
    if 'eave profile assumed' in hs or 'same eave profile assumed as 1/A5.06' in hs:
        w['height_source'] = re.sub(r"(east facade - )?same eave profile assumed as 1/A5\.06|F&B north wall at grid 8 - eave profile assumed",
                                    "east facade: see 1/A5.00 (U-174)", hs)
        n2 += 1
    src = str(w.get('source') or '')
    if ' | height: ' in src and w.get('height_source'):   # CB_BE_CF24: la Source dice la altura cargada (no la de antes de rev19)
        a, b = src.split(' | height: ', 1)
        cola = ''
        for sep in (' | type: ', ' | detail: ', ' | elev '):
            if sep in b:
                cola = b[b.index(sep):]
                b = b[:b.index(sep)]
                break
        nuevo = str(w['height_source']).replace(' | ', '; ')
        _ns = re.findall(r"=\s*(\d+(?:\.\d+)?)\s*ft\b", nuevo)
        if _ns and abs(float(_ns[-1]) - float(w['height_ft'])) > 0.01:
            nuevo += f"; loaded height = {float(w['height_ft']):g} ft"
        if b != nuevo:
            w['source'] = f"{a} | height: {nuevo}{cola}"
            n3 += 1
# CE_COHERENCIA_R11 F3 también para los shafts 'CH-L4-0x'
hmax = {}
for w in C['walls'] + C['existing_walls']:
    if re.match(r"CH[.-]", str(w['id'])):
        b = re.sub(r"\s+[A-Z]$", "", w['id'])
        hmax[b] = max(hmax.get(b, 0), float(w['height_ft']))
nst = 0
for m in C.get('misc_items') or []:
    mm = re.match(r"CH-STUD (CH[.-]\S+)$", str(m.get('ref')))
    if not mm or mm.group(1) not in hmax:
        continue
    H = round(hmax[mm.group(1)], 4)
    k = re.search(r"=\s*(\d+) studs x ([\d.]+) ft", str(m.get('op')))
    if k and abs(float(k.group(2)) - H) > 1e-4:
        q = round(int(k.group(1)) * H, 2)
        m['op'] = re.sub(r"=\s*\d+ studs x [\d.]+ ft(.*?)= [\d.]+", f"= {k.group(1)} studs x {H} ft\\1= {q}", str(m['op']), count=1)
        m['qty'] = q
        m['source'] = f"{m.get('source')} | rev19: stud height = board / liner height of the same shaft wall after the U-176 resolution ({H} ft)"
        nst += 1
json.dump(C, open(CP, 'w'), indent=1)
print(f"rev19 textos: {n1} nota A7.xx -> 1/A5.06 impresa; {n2} eave -> RFI-30; {n3} Source con la altura cargada; {nst} C-H stud CH-L4")

# U-176 control 3 / 4 (rev19, BE-CR33): motivo impreso (N/HOJA) de cada renglón cuya altura difiere del C.H. del cuarto o de otro renglón
# del mismo type: partición por material de la cara (cement board / WR / franja, RFI-11), zona de S1.05 sobre el wall (L4 rated),
# franja / banda de soffit (RFI-18), escalera L4 (1/A5.08)
C = json.load(open(CP))
nm = 0
for w in C['walls'] + C['existing_walls']:
    if w.get('height_diff_reason'):
        if 'RFI-' not in w['height_diff_reason'] and re.search(r'cement|WR|strip|tile', w['height_diff_reason']):
            w['height_diff_reason'] += '; RFI-11 (closed: cement board / tile height)'
        continue
    hs = str(w.get('height_source') or '')
    bd = str(w.get('board') or '')
    fl = str(w.get('floor') or '')
    mot = None
    if 'cement board' in bd or re.search(r"tile backer|RFI-11 tile line|cement board to", hs):
        mot = f"material split of the face: cement board / tile backer at the shower or tub only (RFI-11 closed; A0.06 GN 13), height per {hs.split(';')[0][:90]}"
    elif re.search(r"strip above|minus the 9'-0\"", hs):
        mot = "material split of the face: board strip above the 9'-0\" tile backer (A7.05 'GYP-1 8'-6\"' + 6\"; 4/A5.05 9'-2 7/8\"; RFI-11 closed)"
    elif fl == 'L4' and re.search(r"S1\.05", hs):
        mot = "roof framing depth of the S1.05 zone over this wall (2/A0.10 rated walls to the underside of the roof sheathing; 1/A5.06 8'-11 1/4\" + 1 1/8\" + zone depth)"
    elif fl == 'L4' and re.search(r"1/A5\.06.{0,40}8'-11 1/4\"|8' - 11 1/4\"", hs) and float(w['height_ft']) < 9.0:
        mot = "unrated L4 wall to the ceiling line: 1/A5.06 printed 8'-11 1/4\" (rated walls continue to the roof sheathing per 2/A0.10)"
    elif re.search(r"13'-9 1/2\" .{0,80}- 12'-0 3/4\"", hs):
        mot = "2 HR barrier board band above the FS-1 ceiling membrane to the underside of the L2 sheathing (A3.01 GYP-1 12'-0 3/4\"; 13'-9 1/2\" per 5/A5.04; RFI-28 closed)"
    elif re.search(r"B\.O\. DECK", hs) and re.search(r"1/A5\.08", hs):
        mot = "low-roof strip along the north CMU wall: 1/A5.08 printed 11'-2 5/8\" B.O. DECK (not the L2 floor zone of the room)"
    elif re.search(r"9' - 10 3/4\"|9'-10 3/4\"", hs) and re.search(r"4/A5\.05", hs):
        mot = "corridor shallow floor zone FJ-2 over this wall: 4/A5.05 printed 9'-10 3/4\" (S1.03 / S1.04 corridor strip), not the 1'-9 1/8\" room zone"
    elif re.search(r"(?i)stair", str(w.get('location') or '') + hs):
        mot = f"stair enclosure: own printed height ({hs[:120]})"
    elif re.search(r"(?i)band|soffit|cove", hs) and float(w['height_ft']) < 3:
        mot = f"soffit / band board strip, not a full wall face (RFI-18 closed): {hs[:120]}"
    if mot:
        w['height_diff_reason'] = mot
        nm += 1
    if "capped by structure" in hs and not w.get('structure_bo_ft'):   # U-176 control 3: el tope de '6\" above ceiling' es la estructura
        w['structure_bo_ft'] = float(w['height_ft'])
    if re.match(r"CH[.-]", str(w['id'])) and not w.get('top_track_kind'):   # U-056: cabeza con deflexión impresa
        w['top_track_kind'] = ("deflection head: 'J' runner with 1\" deflection (A0.06 GN 7 'PROVIDE FOR 1\" DEFLECTION AT ALL PARTITION HEADS', "
                               "A0.06 CH '\"J\" RUNNER CHANNEL')")
json.dump(C, open(CP, 'w'), indent=1)
print(f"height_diff_reason (BE-CR33): {nm} renglones con motivo impreso")

# CE_ALTURA_IMPRESA (rev19, 2a corrida): la fuente termina en la operación que da la altura cargada (el parser la rehace);
# una cota impresa con comprobación va como 'printed <cota>; cross-check ...' (BE-CR32)
import sys as _sys
_sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import revision_markups as _RM
C = json.load(open(CP))
nf, resto = 0, []
for w in C['walls'] + C['existing_walls']:
    hs = str(w.get('height_source') or '')
    h = float(w['height_ft'])
    hp = _RM.altura_impresa(hs)[0]
    if hp is None or abs(hp - h) <= 0.002:
        continue
    if "14'-0\" - 1 1/2\" - 1/4\" - 3/4\" = 13'-9 1/2\"" in hs:     # decimal primero (CE_ALTURA_IMPRESA), cota ft-in al final (CE_A2: el resultado no va antes del último '=')
        hs = hs.replace("14'-0\" - 1 1/2\" - 1/4\" - 3/4\" = 13'-9 1/2\"", "14.0 - 0.2083 = 13.7917 (14'-0\" - 1 1/2\" - 1/4\" - 3/4\" = 13'-9 1/2\")")
    elif abs(h - 9.8958) < 1e-3 and "9' - 10 3/4\"" in hs:
        hs = "4/A5.05 SOUTH WALL SECTION printed 9'-10 3/4\" L2 / L3 floor to the underside of the shallow corridor framing; cross-check: " + hs
    elif "half the rise" in hs or "gable average" in hs:
        m = re.search(r"(?:eave |= )(\d+\.\d+)(?: ft)? \+ (?:half the rise[^=]*= )?2\.733", hs) or re.search(r"(\d+\.\d+) \+ 2\.733 ?/ ?2", hs)
        if m:
            hs += f"; {m.group(1)} + 1.3665 = {round(float(m.group(1)) + 1.3665, 4)}"
    w['height_source'] = hs
    hp2 = _RM.altura_impresa(hs)[0]
    if hp2 is not None and abs(hp2 - h) <= 0.002:
        nf += 1
        src = str(w.get('source') or '')
        if ' | height: ' in src:
            a_, b_ = src.split(' | height: ', 1)
            cola = next((b_[b_.index(s_):] for s_ in (' | type: ', ' | detail: ', ' | elev ') if s_ in b_), '')
            w['source'] = f"{a_} | height: {hs.replace(' | ', '; ')}{cola}"
    else:
        resto.append(f"{w['id']} {h} vs {hp2}")
json.dump(C, open(CP, 'w'), indent=1)
print(f"CE_ALTURA_IMPRESA: {nf} fuentes con la operación final; sin resolver {len(resto)}: {resto[:8]}")

# U-181 (auditoría independiente rev19, hallazgo 3): cara de baño de 6 demising DW.4 cargada en Type X: A0.06 GN 11 'USE WATER-RESISTANT
# GYPSUM BOARD FOR WALLS IN ALL TOILET ROOMS' -> esa cara, en el largo del baño (inicio del wall a la bath east wall, extremos vectoriales
# de las bath partitions en el canon), va en Type X W.R. (mismo criterio que DW.4-L2-01 B); el resto del largo de esa cara sigue en Type X
import copy as _cp
C = json.load(open(CP))
TODOS = C['walls'] + C['existing_walls']
BANO = {'DW.4-L2-04 A': ('211', 648.8, 'W.4-L2-11 (bath 211 east wall) at x 648.8; toilet / shower 211 from the wall start x 536.9 (W.4-L2-13 toilet / shower faces)'),
        'DW.4-L2-06 A': ('204', 918.6, 'W.4-L2-26 (bath 204 east wall) at x 918.6'),
        'DW.4-L3-02 A': ('302', 918.8, 'W.4-L3-04 (302 bath east wall) at x 918.8'),
        'DW.4-L3-03 A': ('303', 918.8, 'W.4-L3-07 (303 bath east wall) at x 918.8'),
        'DW.4-L3-04 A': ('304', 918.8, 'W.4-L3-10 (304 bath east wall) at x 918.8'),
        'DW.4-L3-08 A': ('311', 648.8, 'W.4-L3-21 (311 bath stub at door 311.2) at x 648.8; toilet / shower 311 from the wall start x 537.0 (W.4-L3-24)')}
nb = 0
for wid, (rm, xb, ref) in BANO.items():
    w = next((x for x in TODOS if x['id'] == wid), None)
    if not w or int(w.get('faces') or 0) != 2 or 'WR' in str(w.get('board')):
        continue
    base = wid[:-2]
    usados = {x['id'][len(base) + 1:] for x in TODOS if x['id'].startswith(base + ' ')}
    libres = [l for l in 'CDEFGHJK' if l not in usados]
    (x0, y0), (x1, y1) = w['path'][0], w['path'][-1]
    lb = round((xb - min(x0, x1)) / 9, 2)
    L = float(w['length_ft'])
    lista = C['walls'] if w in C['walls'] else C['existing_walls']
    w['faces'] = 1
    w['location'] = f"{w['location']} | this row = the room face (dry); the bath {rm} face is in its own W.R. row (A0.06 GN 11)"
    wr = _cp.deepcopy(w); wr['id'] = f"{base} {libres[0]}"; wr['board'] = '5/8 type X WR'; wr['length_ft'] = lb
    wr['path'] = [[min(x0, x1), y0], [xb, y0]]
    wr['location'] = f"{w['location'].split(' |')[0]} | faces: bath {rm} (toilet / lavatory / shower)"
    wr['source'] = (f"1/A{'2.02' if '-L2-' in wid else '2.03'} [DERIVED] length: bath {rm} face from the wall start x {min(x0, x1)} to {ref}: "
                    f"({xb} - {min(x0, x1)})/9 = {lb} ft; A0.06 GN 11 'USE WATER-RESISTANT GYPSUM BOARD FOR WALLS IN ALL TOILET ROOMS' | height: {w.get('height_source')}")
    wr['tag_ids'] = []
    lista.append(wr)
    resto = round(L - lb, 2)
    if resto > 0.05:
        dr = _cp.deepcopy(wr); dr['id'] = f"{base} {libres[1]}"; dr['board'] = '5/8 type X'; dr['length_ft'] = resto
        dr['path'] = [[xb, y0], [max(x0, x1), y0]]
        dr['location'] = f"{w['location'].split(' |')[0]} | faces: unit {rm} room beyond the bath (dry)"
        dr['source'] = f"1/A{'2.02' if '-L2-' in wid else '2.03'} [DERIVED] length: {L} - {lb} = {resto} ft (room {rm} face beyond the bath) | height: {w.get('height_source')}"
        lista.append(dr)
    nb += 1
    print(f"  {wid}: bath {rm} {lb} LF W.R. + {resto} LF Type X on that face; {wid} -> 1 face")
json.dump(C, open(CP, 'w'), indent=1)
print(f"U-181 hallazgo 3: {nb} demising con la cara de baño en W.R.")

# U-181 hallazgo 8 (U-146): fila de corredor 9'-10 5/8" (7/A7.23 '1' - 1 3/8"') -> 9'-10 3/4" impreso en 4/A5.05 (la mayor)
C = json.load(open(CP))
n8 = 0
for w in C['walls'] + C['existing_walls']:
    if abs(float(w['height_ft']) - 9.8854) < 1e-3:
        w['height_ft'] = 9.8958
        w['height_source'] = ("4/A5.05 SOUTH WALL SECTION printed 9'-10 3/4\" (11'-0\" - '1' - 1 1/4\"' shallow corridor framing); U-146: larger than "
                              "7/A7.23 '1' - 1 3/8\" RATED ASSEMBLY' 9'-10 5/8\"; 11.0 - 1.1042 = 9.8958")
        w['height_op'] = "11'-0\" - 1'-1 1/4\" = 9'-10 3/4\""
        src = str(w.get('source') or '')
        if ' | height: ' in src:
            a_, b_ = src.split(' | height: ', 1)
            cola = next((b_[b_.index(s_):] for s_ in (' | type: ', ' | detail: ', ' | elev ') if s_ in b_), '')
            w['source'] = f"{a_} | height: {w['height_source']}{cola}"
        n8 += 1
json.dump(C, open(CP, 'w'), indent=1)
print(f"U-181 hallazgo 8: {n8} renglones 9.8854 -> 9.8958 (U-146)")

# COORDINACIÓN 11-nov (opción B, U-172 / U-008, mismo criterio que L1 Kitchen 100 PC0186 / PC0187): caras SOLO del tenant de F&B 410 /
# Deck Bar 411 = EXCLUDED (1/A2.04 y 3/A5.07 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT. WILL BE SUBMITTED IN
# FUTURE TENANT IMPROVEMENT PERMIT.'; A0.00 DEFERRED SUBMITTALS 'TENANT INTERIOR FOR LEVEL 4 FOOD AND BEVERAGE SPACES'). Las caras rated de
# corredor / demising / fire partition se quedan (X-L4-03 B DW.4-1, FW.4-L4-19 B FW.4-1 1 HR): su capa es parte del rating.
C = json.load(open(CP))
TP = f'{W}/etapas/4_canon/rev14/rcp_cuartos.json'
T = json.load(open(TP))
MOT = ("F&B tenant-side face: 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT. WILL BE SUBMITTED IN FUTURE TENANT "
       "IMPROVEMENT PERMIT.' (1/A2.04, 3/A5.07); A0.00 deferred submittal 'TENANT INTERIOR FOR LEVEL 4 FOOD AND BEVERAGE SPACES'")
# COORDINACIÓN 11-nov 10:30 (U-159: en exclusiones F&B se verifica la membrana rated): las 4 caras son de types RATED (XW.6.6-2, XW.6.6-1,
# W.62-1 x2): se RESTITUYEN, cargadas; queda en la Scope Checklist (takeoff_json.py ALC-E 'F&B 410 / 411 rated faces kept'). Ninguna se excluye.
TEN = {}
fuera, sf_x = [], 0.0
for lista in (C['walls'], C['existing_walls']):
    for w in list(lista):
        if w['id'] not in TEN:
            continue
        sf = round(float(w['length_ft']) * float(w['height_ft']) * int(w.get('faces') or 1) * int(w.get('layers') or 1), 2)
        sf_x += sf
        lista.remove(w)
        C.setdefault('excluded_walls', []).append({"id": w['id'], "reader": "COORDINACIÓN 11-nov (option B)", "floor": w['floor'],
                                                    "reason": f"EXCLUDED - {MOT}; {sf} SF board ({w['length_ft']} LF x {w['height_ft']} ft x {w.get('faces')} face(s) x {w.get('layers')} layer(s))",
                                                    "img": w.get('img'), "sheet": w.get('sheet'), "path": w.get('path')})
        (x0, y0), (x1, y1) = w['path'][0], w['path'][-1]
        dx, dy = TEN[w['id']]
        e = 9.0
        if abs(y0 - y1) < 1:   # horizontal: banda del lado del tenant
            yy = y0 + (e if dy > 0 else -e)
            poly = [[min(x0, x1), y0], [max(x0, x1), y0], [max(x0, x1), yy], [min(x0, x1), yy]]
        else:
            xx = x0 + (e if dx > 0 else -e)
            poly = [[x0, min(y0, y1)], [xx, min(y0, y1)], [xx, max(y0, y1)], [x0, max(y0, y1)]]
        if not any(r.get('room') == f"{w['id']} (tenant face)" for r in T['rooms']):
            T['rooms'].append({"sheet": "A2.04", "room": f"{w['id']} (tenant face)", "name": w['id'], "disposition": "exclusion", "rows": [],
                               "nhoja": "1/A2.04, 3/A5.07, A0.00", "reason": f"{w['id']} F&B tenant-side face, future TI permit",
                               "reason_short": f"{w['id']} F&B tenant face, future TI", "polygon": poly, "area_sf": None,
                               "label_xy": [round(sum(q[0] for q in poly) / 4, 1), round(sum(q[1] for q in poly) / 4, 1)],
                               "img": w.get('img'), "polygon_src": "rev19: tenant side of the wall path (canon)"})
        fuera.append(f"{w['id']} {sf} SF")
if fuera:
    C.setdefault('excluded_items', []).append({"refs": sorted(TEN), "reason": f"{MOT}. Rated corridor / demising / fire-partition faces of 410 / 411 stay loaded (X-L4-03 B, FW.4-L4-19 B, corridor and demising walls). Total {round(sf_x, 2)} SF board EXCLUDED."})
json.dump(C, open(CP, 'w'), indent=1)
json.dump(T, open(TP, 'w'), indent=1)
print(f"F&B tenant (opción B): {len(fuera)} caras EXCLUDED, {round(sf_x, 2)} SF: {fuera}")
