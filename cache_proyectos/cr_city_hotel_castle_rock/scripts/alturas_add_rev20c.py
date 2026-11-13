"""rev20c (U-176, U-199): doble lectura ciega de alturas de los 16 renglones nuevos de la revisión U-199 (lectores A y B independientes,
alturas/A_add, alturas/B_add) agregada a las lecturas A / B del proyecto, y la RESOLUCIÓN de cada diferencia (A != B, o A = B distinto de la
regla del proyecto) en alturas/ALTURAS_AB_RESOLUCION.csv con N/HOJA e imagen. Regla del proyecto (rev19 / rev20, U-146 / U-010): el board
del wall llega al rated assembly / a la estructura; la cota impresa gana a la medida vectorial; entre dos impresas, la mayor. Idempotente."""
import csv, os, shutil
AL = '/root/cr/work/alturas'
IMG_R6 = '/root/cr/work/auditoria_u199/rev/R6_duda/R6_NT-L1-03_NT-L1-05.png'


def leer(p):
    return list(csv.DictReader(open(p, encoding='utf-8-sig'))) if os.path.isfile(p) else []


def escribir(p, filas):
    cols = list(dict.fromkeys(k for r in filas for k in r))
    with open(p, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=cols, restval=''); w.writeheader(); w.writerows(filas)


for L in ('A', 'B'):
    add = leer(f'{AL}/{L}_add/ALTURAS_IMPRESAS_{L}_add.csv')
    base = f'{AL}/{L}/ALTURAS_IMPRESAS.csv'
    filas = leer(base)
    ids = {r['Wall ID'] for r in add}
    filas = [r for r in filas if r['Wall ID'] not in ids]
    os.makedirs(f'{AL}/{L}/img', exist_ok=True)
    for r in add:
        im = os.path.basename(r.get('Image') or '')
        if im and os.path.isfile(f'{AL}/{L}_add/img/{im}'):
            shutil.copy2(f'{AL}/{L}_add/img/{im}', f'{AL}/{L}/img/{im}')
            r['Image'] = f'{AL}/{L}/img/{im}'
        if not str(r.get('Printed H') or '').strip():
            r['Printed H'] = '0'          # PENDING del lector: queda en su lectura; la tabla final toma la resolución
        filas.append(r)
    escribir(base, filas)
A5 = f'{AL}/A/img/A505_4_typ_floor_assembly.png'
L4 = f'{AL}/A/img/A506_1_L4_ceiling.png'
BAR = f'{AL}/A/img/A504_3_BAR_BOdeck_CLG.png'
NIC = f'{AL}/A/img/A735_niches_11ft.png'
S_L23 = ("4/A5.05 SOUTH WALL SECTION prints \"9' - 2 7/8\"\" under the \"1' - 9 1/8\"\" floor / ceiling zone (underside of the rated FS-1 assembly, A0.08; "
         "A0.10 det. 3/4 walls stop at the rated assembly); 1/A5.06 prints 9'-2\" for the same condition: larger taken (U-146)")
S_BAR = "3/A5.04 prints \"11' - 2 5/8\" B.O. DECK\" at the BAR (also 2/A5.04); wall heads to LINE OF STRUCTURE (A0.06), as the abutting W.6-L1-32"
RES = [
 ('DW.4-L2-06b', 9.2396, S_L23, "H-A 9'-2 7/8\" (4/A5.05) / H-B 9'-2\" (1/A5.06): the larger printed value of the same condition (U-146), as every L2 / L3 unit wall", A5, 'CONFIRMED'),
 ('W.4-L3-44 A', 9.2396, S_L23, "H-A 9'-2 7/8\" / H-B 9'-2\": larger printed (U-146), as the twin W.4-L3-43 A", A5, 'CONFIRMED'),
 ('W.4-L3-44 B', 9.2396, S_L23, "H-A 9'-2 7/8\" / H-B 8'-6\" (bath GYP-1 ceiling tag 10/A7.00): the wet face board runs to the rated assembly like the twin W.4-L3-43 B; the 8'-6\" is the bath ceiling below it", A5, 'CONFIRMED'),
 ('W.4-L4-22 A', 8.9375, "1/A5.06 WALL SECTION WEST ALLEY prints \"8' - 11 1/4\"\" LEVEL 4 to the ceiling = bottom of the roof / ceiling assembly; unrated L4 walls stop there (as W.4-L4-19)",
  "H-A = H-B 8.8267 by a vector measurement on the schematic 1/8\" section 4/A4.03; the printed 8'-11 1/4\" of 1/A5.06 for the same L4 condition governs (U-010: printed over measured)", L4, 'CONFIRMED'),
 ('W.4-L4-22 B', 8.9375, "1/A5.06 WALL SECTION WEST ALLEY prints \"8' - 11 1/4\"\" LEVEL 4 to the ceiling = bottom of the roof / ceiling assembly (as W.4-L4-19 B)",
  "H-A = H-B 8.8267 (vector on 4/A4.03); printed 8'-11 1/4\" (1/A5.06) governs (U-010)", L4, 'CONFIRMED'),
 ('NT-L1-01', 12.5625, "U-178(4): the build-out stands in lobby 108 under the 12'-0 3/4\" FS-1 ceiling (2/A7.31) -> board to C.H. + 6\" = 12'-6 3/4\"",
  "H-A = H-B 11' (3/A7.35, raster elevation of the niche build-out); COORDINACIÓN 13-nov: wall under the room C.H. -> U-178(4) C.H. + 6\"; delta if it stops at 11': see RFI-33", NIC, 'DERIVED'),
 ('NT-L1-02', 12.5625, "U-178(4): lobby 108 ceiling 12'-0 3/4\" (2/A7.31) + 6\" = 12'-6 3/4\"",
  "H-A = H-B 11' (2/A7.35, raster); U-178(4) C.H. + 6\" (COORDINACIÓN 13-nov); delta in RFI-33", NIC, 'DERIVED'),
 ('NT-L1-03 A', 11.2188, S_BAR, "H-A 11'-2 5/8\" (B.O. deck) / H-B 11'-0\" (bar ceiling): the lining head runs to the line of structure (A0.06), as W.6-L1-32", BAR, 'CONFIRMED'),
 ('NT-L1-03 C', 12.9956, "2/A5.04 (3/8\" = 1'-0\" = 27 pt/ft): LEVEL 1 to the mezzanine floor line (1536.6 - 1185.72) / 27 = 12.9956; the facade above is counted as XW.6.3-L2-12 A / B",
  "H-A PENDING / H-B 19.6267 (whole facade to the eave on 1/A5.04): the exterior sheathing above the L1 storey is already in the canon as XW.6.3-L2-12 A / B, so this row stops at the mezzanine floor (no double count)", IMG_R6, 'DERIVED'),
]
for k in ('A', 'B', 'C', 'D'):
    RES.append((f'W.6-L1-06S {k}', 11.2188, S_BAR, "H-A 11'-2 5/8\" (B.O. deck, W head to line of structure A0.06) / H-B 11'-0\" (bar ceiling 2/A5.04): the block is drawn cut on the RCP 1/A7.31 (rises through the ceiling), as the abutting W.6-L1-32", BAR, 'CONFIRMED'))
RES.append(('XW-L1-BAR15 A', 11.2188, S_BAR, "H-A 11'-2 5/8\" / H-B 11'-0\": interior face of an exterior wall runs to structure (A0.07 / A0.06), as the BAR walls", BAR, 'CONFIRMED'))
RES.append(('XW-L1-BAR15 B', 11.2188, S_BAR, "H-A PENDING / H-B 11'-2 19/32\" (B.O. deck at the courtyard edge, 2/A5.04): the printed 11'-2 5/8\" B.O. DECK governs", BAR, 'CONFIRMED'))
# renglones FALTA de la revisión U-199 (5b) (auditoria_u199/diag/G*/faltas.json): donde A o B difiere de la altura cargada (que es la del
# muro gemelo / contiguo del mismo plano, con su N/HOJA), la resolución toma la cargada y cita las dos lecturas
import glob, json
TOL = 1 / 48 + 1e-6
la = {r['Wall ID']: r for r in leer(f'{AL}/A_add/ALTURAS_IMPRESAS_A_add.csv')}
lb = {r['Wall ID']: r for r in leer(f'{AL}/B_add/ALTURAS_IMPRESAS_B_add.csv')}
for pf in sorted(glob.glob('/root/cr/work/auditoria_u199/diag/G*/faltas.json')):
    for row in json.load(open(pf)):
        wid, h = row['id'], float(row['height_ft'])
        if wid in ('DG-A2.04-1', 'DG-A7.50-1'):   # duplicados no cargados (rev20c_u199.py DG_DUP)
            continue
        a, b = la.get(wid), lb.get(wid)
        def f_(x):
            try:
                return float(x['Printed H'])
            except (TypeError, ValueError, KeyError):
                return None
        ha, hb = f_(a), f_(b)
        if ha is not None and hb is not None and abs(ha - h) <= TOL and abs(hb - h) <= TOL:
            continue
        img = (a or {}).get('Image') or (b or {}).get('Image') or ''
        img = img if os.path.isabs(img) else (f'{AL}/A_add/{img}' if a and a.get('Image') else f'{AL}/B_add/{img}')
        RES.append((wid, h, str(row.get('height_source') or ''),
                    f"H-A {ha if ha is not None else 'PENDING'} / H-B {hb if hb is not None else 'PENDING'}: the loaded height is the one of the same wall "
                    f"line already in the take-off (twin / adjacent row of the same face, U-199 (5b) reviewer {os.path.basename(os.path.dirname(pf))}), "
                    "with its printed N/HOJA; the readers' vector measurements on the 1/8\" building sections or the room ceiling tag are not the wall head",
                    img, 'CONFIRMED' if str(row.get('height_status')).upper().startswith('CONF') else 'DERIVED'))
rp = f'{AL}/ALTURAS_AB_RESOLUCION.csv'
filas = [r for r in leer(rp) if r['Wall ID'] not in {x[0] for x in RES}]
OPS = {
 'DW.4-L2-06b': "11.0 - 1.7604 = 9.2396", 'W.4-L3-44 A': "11.0 - 1.7604 = 9.2396", 'W.4-L3-44 B': "11.0 - 1.7604 = 9.2396",
 'NT-L1-01': "12.0625 + 0.5 = 12.5625", 'NT-L1-02': "12.0625 + 0.5 = 12.5625",
 'NT-L1-03 A': "11 + 2.625 / 12 = 11.2188", 'NT-L1-03 B': "11 + 2.625 / 12 = 11.2188", 'NT-L1-03 C': "(1536.6 - 1185.72) / 27 = 12.9956",
 'XW-L1-BAR15 A': "11 + 2.625 / 12 = 11.2188", 'XW-L1-BAR15 B': "(1536.6 - 1185.72) / 27 = 12.9956",
 'DG-A6.00-3': "14.0 - 1.9375 = 12.0625", 'DG-A6.01-1': "(791.5 - 628.7) / 18 = 9.0444",
 'DG-A6.02-1': "11.0 - 1.1042 = 9.8958", 'DG-A6.02-2': "11.0 - 1.1042 = 9.8958",
}
for k in ('A', 'B', 'C', 'D'):
    OPS[f'W.6-L1-06S {k}'] = "11 + 2.625 / 12 = 11.2188"
# W.6-L4-02 / 03 / 04: re-tipados W.6-1 por U-199 R2 (2/A0.02 '1HR FP'): el muro rated sube al roof sheathing (2/A0.10), como W.6-L4-01 / 08
R2I = '/root/cr/work/auditoria_u199/rev/R2_rated'
S_R = ("1/A5.06 '8' - 11 1/4\"' = LEVEL 4 to the CEILING line; + ceiling assembly 1/2\" RC + 5/8\" board (A0.08 RS-1) = 9'-0 3/8\" = 9.03125 ft to the underside "
       "of the roof framing; + roof framing 1.5000 ft; 2/A0.10 'FIRE PARTITIONS AND FIRE BARRIERS EXTEND TO UNDERSIDE OR ROOF SHEATHING'")
for wid, img in (('W.6-L4-02 A', '6_A2.04-45.png'), ('W.6-L4-02 B', '6_A2.04-45.png'), ('W.6-L4-03 A', '6_A2.04-38.png'),
                 ('W.6-L4-03 B', '6_A2.04-38.png'), ('W.6-L4-04', '6_A2.04-11.png')):
    RES.append((wid, 10.5312, S_R, "H-A / H-B 8'-11 1/4\" (rev19 readings, the wall was W.6-0, unrated, stopping at the ceiling); U-199 R2 re-typed it W.6-1 "
                "(2/A0.02 1HR FP): a rated wall runs to the roof sheathing (2/A0.10), same height as W.6-L4-01 / W.6-L4-08", f'{R2I}/{img}', 'DERIVED'))
    OPS[wid] = "9.03125 + 1.5 = 10.5312"
# NT-L1-03 B: A = B = 11.2188, la fila de A no trae aritmética -> resolución con su operación
RES.append(('NT-L1-03 B', 11.2188, S_BAR, "H-A = H-B 11'-2 5/8\" B.O. DECK (3/A5.04): interior layers of the rated exterior wall to structure", BAR, 'CONFIRMED'))
_dg = {'DG-A6.01-1': 9.0444}
for wid, h, src, res, img, st in RES:
    h = _dg.get(wid, h)
    if wid == 'XW-L1-BAR15 B':
        h, src = 12.9956, ("exterior sheathing of the same L-shaped grid-4 courtyard wall as NT-L1-03 C: 2/A5.04 (27 pt/ft) LEVEL 1 slab line y1536.6 to "
                           "the mezzanine floor y1185.72")
        res = "H-A PENDING / H-B 11'-2 19/32\" (B.O. deck): the exterior skin is the one of NT-L1-03 C (same wall, U-199 R6), not the interior face (CR-R13-E1)"
    if wid == 'NT-L1-01' or wid == 'NT-L1-02':
        src = "U-178(4): the build-out stands in lobby 108 under the GYP-1 / FS-1 ceiling 2/A7.31 (C.H. + 6\"): 12'-0 3/4\" + 6\" = 12'-6 3/4\""
    filas.append({'Wall ID': wid, 'Resolution': res, 'Image': img, 'Printed H': f'{h:.4f}', 'Source': src, 'Operation': OPS.get(wid, ''),
                  'Status': 'DERIVED' if OPS.get(wid, '').startswith('(') or '+' in OPS.get(wid, '') or (' - ' in OPS.get(wid, '') and st == 'DERIVED') else st})
escribir(rp, filas)
print('alturas rev20c: A / B +', len(leer(f'{AL}/A_add/ALTURAS_IMPRESAS_A_add.csv')), '/', len(leer(f'{AL}/B_add/ALTURAS_IMPRESAS_B_add.csv')), '| resoluciones', len(RES))
