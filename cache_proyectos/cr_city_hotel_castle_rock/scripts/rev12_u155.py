"""rev12 (U-155, usuario 8-nov: 'buscar hasta encontrar las respuestas en los planos; si no, usa los códigos del IBC y cita su referencia').
Walls sin tag (RFI-04): el RATING está impreso en los code plans / A0.00 -> se cita en la fila (mismas capas cargadas, sin cambio de cantidad).
 - ELEC 321 (L3): A0.02 'LEVEL 3 CODE PLAN' encierra ELEC 321 / LINEN 322 / CLEANING 323 con la línea '1HR FP' del lado del corridor (verificado a ojo, p5).
 - Demising sin tag (DW.4-1): A0.00 'NOTE: CORRIDOR AND UNIT DEMISING WALLS CONSTRUCTED AS 1HR FIRE PARTITIONS'.
RFI-28 / RFI-25 se cierran en rfis.py (CERR) y DA-7 ya no se crea (rev11_auditoria)."""
import json
W = '/root/cr/work'; CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP)); n = 0
for w in c['walls'] + c['existing_walls']:
    loc, src = str(w.get('location', '')), str(w.get('source', ''))
    if 'TYPE ASSUMED' not in loc or 'U-155' in src:
        continue
    if 'ELEC 321' in loc:
        w['source'] = src + (" | rating (U-155): A0.02 LEVEL 3 CODE PLAN draws the ELEC 321 / LINEN 322 / CLEANING 323 closets with the '1HR FP' line on "
                             "the corridor side; 1 layer 5/8\" Type X each face = 1 HR wood-stud wall per IBC 2018 Table 721.1(2) (same layers as loaded)")
        n += 1
    elif str(w.get('type_id')) == 'DW.4-1':
        w['source'] = src + (" | rating (U-155): A0.00 'NOTE: CORRIDOR AND UNIT DEMISING WALLS CONSTRUCTED AS 1HR FIRE PARTITIONS' (IBC 2018 Section 708) "
                             "-> DW.4-1 as loaded")
        n += 1
# rev12 E1 (COORDINACIÓN): los deltas de las alternativas se recalculan desde las filas ACTUALES (H11 subió W.6-2 de L1 a 13.7917 ft)
IDX = {w['id']: w for w in c['walls'] + c['existing_walls']}
FILAS = {'DA-1': [('W.6-L1-24', 2, 1), ('W.6-L1-23 C', 1, 1), ('W.6-L1-23 D', 1, 2)],     # W: 2nd layer each face; E: ELEC 2nd layer + retail face
         'DA-2': [('W.6-L1-20 C', 2, 1), ('W.6-L1-23 E', 1, 1), ('W.6-L1-23 F', 1, 2)]}
for d in c.get('deduct_alternates') or []:
    if d['id'] in FILAS:
        partes = [(i, float(IDX[i]['length_ft']), float(IDX[i]['height_ft']), f, l) for i, f, l in FILAS[d['id']]]
        tot = round(sum(L * H * f * l for _, L, H, f, l in partes), 2)
        d['filas'] = [{'id': i, 'faces': f, 'layers': l} for i, _, _, f, l in partes]
        d['operacion'] = ' + '.join(f"{i} {L} x {H} x {f} face(s) x {l} layer(s)" for i, L, H, f, l in partes) + f" = {tot} SF"
        print(d['id'], d['delta_sf'], '->', -tot)
        d['delta_sf'] = -tot
# rev12 Obs (COORDINACIÓN): vigas de borde norte de Retail 124 (S1.02 (MF) W27X94, (MF) W21X50, W24X55, 2/S3.02 muro exterior sobre la viga)
# más profundas que las trusses de 18": la membrana FS-1 las envuelve (A0.08 FS-1 'GYP AND RESILIENT CHANNELS WRAP STEEL BEAMS WHERE THEY ARE
# DEEPER THAN TRUSSES'); cara exterior = muro exterior -> fondo + 1 lado (d - 16.5", 3/S3.02). LF medidos en S1.02 (contornos_zR12.json).
Z = json.load(open(f'{W}/etapas/4_canon/rev9/contornos_zR12.json'))['BW-L1-RETAIL']
AISC = {'W27X94': (26.92, 9.99), 'W21X50': (20.83, 6.53), 'W24X55': (23.57, 7.01)}
partes = [(e['beam'], e['lf'], AISC[e['beam']]) for e in Z['edge']]
sf_n = round(sum(l * (bf + (d - 16.5)) / 12 for _, l, (d, bf) in partes), 2)
lf_n = round(sum(l for _, l, _ in partes), 2)
for m in c['misc_items']:
    if m['ref'] == 'BW-L1-RETAIL board' and 'north edge' not in str(m['op']):
        m['qty'] = round(296.78 + sf_n, 2)
        _lt = round(154.23 + lf_n, 2)
        m['op'] = (f"{_lt} LF x {round(m['qty'] / _lt, 5)} ft = {m['qty']} (7 interior beams 154.23 LF beam by beam = 296.78 + north edge beams {lf_n} LF = {sf_n}) | north edge (bottom + inside face, "
                   f"outside face = exterior wall 2/S3.02): " + ' + '.join(f"{b} {l} LF x ({bf} + ({d} - 16.5)) / 12" for b, l, (d, bf) in partes)
                   + f" = {sf_n} SF; d / bf AISC; LF measured on S1.02 (1/8\" = 9 pt/ft)")
        m['source'] = str(m['source']) + (" | north edge beams S1.02 '(MF) W27X94', '(MF) W21X50', 'W24X55' over Retail 124 (A3.01 dashed beam line above the GYP-1 11'-0\" band): "
                                          "A0.08 FS-1 'GYP AND RESILIENT CHANNELS WRAP STEEL BEAMS WHERE THEY ARE DEEPER THAN TRUSSES'")
        print('BW edge', sf_n, m['qty'])
    if m['ref'] == 'BW-L1-RETAIL RC' and 'north edge' not in str(m['op']):
        m['qty'] = round(154.23 * 3 + lf_n * 2, 2)
        m['op'] = f"154.23 LF x 3 lines (bottom + 2 sides) + north edge {lf_n} LF x 2 lines (bottom + inside face) = {m['qty']}"
        print('BW RC', m['qty'])
json.dump(c, open(CP, 'w'), indent=1)
print('U-155 citations', n)
