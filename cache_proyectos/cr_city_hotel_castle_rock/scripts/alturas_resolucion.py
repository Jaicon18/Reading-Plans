"""rev19 (U-176 control 1, auditoría COORDINACIÓN 11-nov): resolución de las dos lecturas ciegas H-A / H-B contra el canon.
Criterio, el mismo para todos los grupos:
  - A = B = canon: nada que resolver.
  - A = B != canon: se adopta A = B (el canon cambia), salvo que el renglón del canon sea una condición que los lectores no modelaron
    y que imprime un detalle (cara parcial de baño a 6" sobre el cielo, franja sobre el cement board, FW a 6" sobre el cielo del
    corredor, sección de escalera medida): ahí queda el canon, con su operación e imagen.
  - A != B: el valor que cierra con lo impreso / la medición más específica (ver REGLAS abajo), con su recorte.
Salidas en /root/cr/work/alturas/: ALTURAS_AB_RESOLUCION.csv (Wall ID, Resolution, Image, Printed H, Source, Operation, Status) y
cambios_canon.json ({Wall ID: {height_ft, nota}}) que aplica rev19_auditoria.py."""
import csv
import json
import os
import re
import sys

sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import comparar_alturas as CA  # noqa: E402

W = '/root/cr/work'
AL = f'{W}/alturas'
T = 1 / 48 + 1e-6
C = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
CW = {w['id']: w for w in C['walls'] + C['existing_walls']}
L = lambda p: {r['Wall ID']: r for r in csv.DictReader(open(p, encoding='utf-8-sig'))}   # noqa: E731
A, B = L(f'{AL}/A/ALTURAS_IMPRESAS.csv'), L(f'{AL}/B/ALTURAS_IMPRESAS.csv')
IMG = f'{W}/etapas/4_canon/img/rev19'


def ftin(h):
    t = round(h * 192) / 16
    ft, inch = int(t // 12), t - 12 * int(t // 12)
    e = int(inch); fr = round((inch - e) * 16)
    if not fr:
        return f"{ft}'-{e}\""
    n, d = fr, 16
    while n % 2 == 0:
        n, d = n // 2, d // 2
    return f"{ft}'-{e} {n}/{d}\""


res, cambios = [], {}


EAST_U174 = ('XW.6.6-L4-12 B', 'XW.6.6-L4-13 C', 'XW.6.6-L4-14 B', 'XW.6.6-L4-15 B', 'XW.6.6-L4-17 A')


def resolver(wid, h, src, op, status, img, motivo):
    res.append({"Wall ID": wid, "Resolution": motivo, "Image": img, "Printed H": f"{h:.4f}", "Source": src, "Operation": op, "Status": status})
    hc = float(CW[wid]['height_ft'])
    if abs(hc - h) > 1e-4:
        cambios[wid] = {"height_ft": round(h, 4), "antes": hc, "nota": f"rev19 U-176 (double blind reading H-A / H-B): {motivo}"}


def img_canon(w):
    p = w.get('height_img') or ''
    return p if p and os.path.isfile(p) else f'{IMG}/R19_H1_4-A505_zonas_somera_profunda.png'


n = {}
for wid, w in CW.items():
    hc = float(w['height_ft']); a = float(A[wid]['Printed H']); b = float(B[wid]['Printed H'])
    src_c = str(w.get('height_source') or '')
    ab = abs(a - b) <= T
    if ab and abs(a - hc) <= T:
        continue
    k = None
    # U-181 (auditoría independiente rev19): las caras de terraza 401 / 402 están bajo el eave inclinado 04/A9.05 (1/A4.05 corta 401;
    # A2.05 roof plan '3"/1'-0"' hacia el muro) = el eave de 1/A5.06 (9.844); la cara norte de F&B 410 en grid 8 la corta 3/A5.07 (H-A 10.25).
    # 1/A5.00 (14'-0") es el storefront del Deck Bar 411, otro plano de fachada: NO aplica (error de la 3a corrida corregido)
    if wid in EAST_U174:
        k = 'east_eave'
        if wid == 'XW.6.6-L4-17 A':
            resolver(wid, 10.2533, "3/A5.07 BUILDING SECTION - N/S SPEAKEASY (3/8\" = 1'-0\" = 27 pt/ft) cuts F&B 410 at grid 8 under the pitched L4 eave "
                     "04/A9.05 Sim: LEVEL 4 at vertical coordinate 523.44 pt to the top of the exterior layer at 246.60 pt; (523.44 - 246.60)/27 = 10.2533",
                     "(523.44 - 246.60) / 27 = 10.2533", "DERIVED",
                     f'{IMG}/R19_E3_3-A507_grid8_eave_04-A905.png',
                     f"H-A {a:.4f} (3/A5.07 cuts F&B 410 at grid 8) / H-B {b:.4f} (west-alley eave): the section drawn at this wall governs: H-A")
        else:
            r = B[wid]
            resolver(wid, 9.8444, "1/A5.06 eave (L4 to underside of roof sheathing at the eave, outer face): same pitched L4 roof eave 04/A9.05 at the "
                     "401 / 402 terrace faces (1/A4.05 BUILDING SECTION - EAST/WEST2 cuts 401 under that eave; A2.05 roof plan slope 3\"/1'-0\" to this wall)",
                     "(459.12 - 193.32) / 27 = 9.8444", "DERIVED", f'{IMG}/R19_E2_1-A405_401_eave.png',
                     f"H-A {a:.4f} (1/A5.08) / H-B {b:.4f} (1/A5.06) agree within 0.05 ft; 1/A4.05 draws this face under the 04/A9.05 eave: 9.844")
        n[k] = n.get(k, 0) + 1
        continue
    # --- canon kept: conditions the readers did not model (printed detail) ---
    if ab and abs(hc - 9.0) < 1e-3 and 'Bath ceiling GYP-1' in src_c:
        k = 'bath_partial'
        resolver(wid, 9.0, "A7.05 unit RCP bath 'GYP-1 8'-6\"' (same tag A7.00 / A7.09 / A7.13) + 6\" (estimator precedent #15, RFI-11 closed): tile backer / WR layer height; the same face continues to the structure (A0.06 head detail 'LINE OF STRUCTURE', 4/A5.05 9'-2 7/8\") in its own strip row",
                 "8'-6\" + 6\" = 9'-0\"", "DERIVED", f'{IMG}/R19_R1_bano_8-6_mas_6.png',
                 "both readers gave the full wall height (9'-2 7/8\"); this row is only the cement board / WR part of the bath face (material split to 9'-0\"), the gypsum above to the structure is a separate row: canon kept")
    elif ab and abs(hc - 0.2396) < 1e-3:
        k = 'strip'
        resolver(wid, 0.2396, "4/A5.05 '9'-2 7/8\"' (A0.06 head detail: board to the LINE OF STRUCTURE) minus the 9'-0\" tile backer part of the face (A7.05 'GYP-1 8'-6\"' + 6\")",
                 "9'-2 7/8\" - 9'-0\" = 0'-2 7/8\"", "DERIVED", f'{IMG}/R19_R1_bano_8-6_mas_6.png',
                 "both readers gave the full wall; this row is only the board strip above the 9'-0\" bath face (the full face is another row): canon kept")
    elif re.search(r"\(791\.5-628\.7\)/18 = 9\.04|9\.04", src_c) and wid.startswith(('FW.2-L4', 'FW.4-L4-15')):
        k = 'stair_l4'
        resolver(wid, hc, "11/A6.01 stair section (1/4\" = 1'-0\" = 18 pt/ft): L4 floor at vertical coordinate 791.5 pt to the underside of roof framing at 628.7 pt",
                 "(791.5 - 628.7) / 18 = 9.04", "DERIVED", img_canon(w),
                 "readers used the typical unit value (8'-11 1/4\") or the corridor joists (9.64); the wall is at the lobby stair, drawn in 11/A6.01: canon vector measurement on that section kept")
    elif wid in ('FI.2-L4-01', 'FI.2-L4-02', 'X-L4-02'):
        k = 'stair_se'
        resolver(wid, hc, "5/A6.02 SE stair section (1/4\" = 1'-0\" = 18 pt/ft): L4 at vertical coordinate 797.4 pt to the underside of roof framing at 609.4 pt",
                 "(797.4 - 609.4) / 18 = 10.44", "DERIVED", img_canon(w),
                 "readers differ (11.16 building section / 14'-0\" roof datum / 8'-11 1/4\"); the SE stair section 5/A6.02 draws this wall: canon vector measurement kept")
    # --- A = B != canon: adopt the readers ---
    elif ab:
        k = 'AB'
        r = A[wid]
        resolver(wid, a, r['Source'], r['Operation'], r['Status'], r['Image'],
                 f"both blind readers agree on {ftin(a)} ({a:.4f}); canon had {hc:.4f}: changed to the readers' printed value")
    # --- A != B ---
    elif abs(hc - 12.0) < 1e-3 and abs(a - 12.0625) < 1e-3:
        k = 'L1_FS1'
        resolver(wid, 12.0625, "A3.01 / A7.31 ceiling tag 'GYP-1 12'-0 3/4\"' (FS-1 membrane under the L2 floor) = 14'-0\" (4/A5.05) - 2/A7.31 '1'-11 1/4\" RATED ASSEMBLY'; A0.10 det. 3/4 walls stop at the rated assembly",
                 "14'-0\" - 1'-11 1/4\" = 12'-0 3/4\"", "DERIVED", A[wid]['Image'],
                 "H-A 12'-0 3/4\" (printed GYP-1 tag); H-B 12'-2 1/8\" is the bottom of the joists above the membrane; the canon's 12'-0\" 'B.O. DECK' belongs to the metal-deck zone of 5/A5.04 only: changed to 12'-0 3/4\"")
    elif abs(hc - 1.7917) < 1e-3:
        k = 'band'
        resolver(wid, 1.7292, "13'-9 1/2\" (2 HR barrier to the underside of the L2 sheathing) - 12'-0 3/4\" (A3.01 GYP-1 FS-1 membrane)",
                 "13'-9 1/2\" - 12'-0 3/4\" = 1'-8 3/4\"", "DERIVED", A[wid]['Image'],
                 "the band above the membrane follows the 12'-0 3/4\" membrane height (H-A); H-B used its 12'-2 1/8\": changed")
    elif '8\'-11 1/4" (LEVEL 4 to underside of roof framing, 1/A5.06) +' in src_c:
        k = 'L4_rated'
        fr = hc - 8.9375
        h = round(8.9375 + 0.09375 + fr, 4)
        resolver(wid, h, "1/A5.06 '8'-11 1/4\"' = LEVEL 4 to the CEILING line; + ceiling assembly 1/2\" RC + 5/8\" board (A0.08 RS-1): 8'-11 1/4\" + 1 1/8\" = 9'-0 3/8\" = 9.03125 ft to the underside of roof framing; + roof framing depth of the S1.05 zone over the wall; 2/A0.10 'FIRE PARTITIONS AND FIRE BARRIERS EXTEND TO UNDERSIDE OR ROOF SHEATHING'. Check: H-B measured 1/A5.06 (459.12 - 174.72)/27 = 10.533 at the unit roof",
                 f"9.03125 + {fr:.4f} = {h:.4f}", "DERIVED", B[wid]['Image'],
                 f"H-A measured to the TOP of the roof framing on 2/A4.03 (11.16, too high); H-B measured the underside of the sheathing on 1/A5.06 / 4/A5.05 ({b:.4f}); the canon started from the ceiling line, 1 1/8\" low: changed to {h:.4f}")
    elif abs(hc - 10.24) < 1e-3 and wid.startswith('XW.6.6-L4') and abs(b - 9.8444) < 1e-3:
        k = 'L4_ext'
        resolver(wid, 9.8444, B[wid]['Source'], B[wid]['Operation'], B[wid]['Status'], B[wid]['Image'],
                 f"H-A 9.80 (1/A5.08) and H-B 9.844 (1/A5.06, outer face at the eave) agree within 0.05 ft; the canon measured to the inner sheathing line y=182.64 (10.24): changed to 9.844")
    elif abs(hc - a) <= T or abs(hc - b) <= T:
        k = 'canon_eq'
        r = A[wid] if abs(hc - a) <= T else B[wid]
        otro = 'H-B' if r is A[wid] else 'H-A'
        resolver(wid, float(r['Printed H']), r['Source'], r['Operation'], r['Status'], r['Image'],
                 f"canon = {'H-A' if r is A[wid] else 'H-B'} ({float(r['Printed H']):.4f}); {otro} gave {(b if otro == 'H-B' else a):.4f} ({(B if otro == 'H-B' else A)[wid]['Source'][:120]}); kept the value that matches the governing detail")
    elif wid in ('FI.2-L1-01', 'XW.6.6-L4-18 B', 'XW.6.4-L2-02 A'):
        k = 'canon_detail'
        fijo = {'FI.2-L1-01': ("1/A5.08 printed '11'-2 5/8\" B.O. DECK' (low-roof strip along the north CMU wall, grid 0)", "", "CONFIRMED"),
                'XW.6.6-L4-18 B': ("2/A5.01 printed 'B.O. FRAMING 11'-4 3/4\"' above LEVEL 4 at the grid 8 courtyard wall", "", "CONFIRMED"),
                'XW.6.4-L2-02 A': ("2/A5.04 (27 pt/ft) exterior sheathing at the eave (1185.48 - 1006.2)/27 = 6.64 + half the rise of the sloped roof (1026.1 - 952.3)/27 = 2.733",
                                   "6.64 + 2.733 / 2 = 8.0065", "DERIVED")}[wid]
        resolver(wid, hc, fijo[0], fijo[1], fijo[2], img_canon(w),
                 f"H-A {a:.4f} / H-B {b:.4f} / canon {hc:.4f}: the canon reads the value printed on (or measured in) the detail drawn at this wall: kept")
    else:
        k = 'canon_detail'
        m = re.findall(r"\(?\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*\)?\s*/\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)", src_c)
        op = (f"({m[0][0]} - {m[0][1]}) / {m[0][2]} = {hc:.4f}" if m else src_c[:200])
        resolver(wid, hc, src_c[:300], op, "DERIVED", img_canon(w),
                 f"H-A {a:.4f} / H-B {b:.4f} / canon {hc:.4f}: the canon operation on its own detail (vector measurement at the printed scale) kept")
    n[k] = n.get(k, 0) + 1

# check every resolution operation closes (control 2)
malas = []
for r in res:
    if r['Status'].upper() == 'DERIVED':
        ok, det = CA.cierre(r['Operation'], float(r['Printed H']))
        if not ok:
            malas.append((r['Wall ID'], det, r['Operation'][:120]))
with open(f'{AL}/ALTURAS_AB_RESOLUCION.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(res[0])); w.writeheader(); w.writerows(res)
json.dump(cambios, open(f'{AL}/cambios_canon.json', 'w'), indent=1)
print("grupos:", n)
print("resoluciones:", len(res), "cambios de canon:", len(cambios))
print("operaciones que no cierran:", len(malas))
for x in malas[:25]:
    print("  ", x)

# ---------- cuartos (U-176 control 1 también para los C.H.): mismas etiquetas leídas, distinta subzona como 'el cuarto' ----------
RC = [("108", 12.0625, "A3.01 / 1/A7.31 tag 'GYP-1 12'-0 3/4\"' (lobby coffered main field)", "both readers read the same tags; the 11'-0\" rows are the dropped band, the WS-1 strip and the millwork feature (soffit / band, not the room ceiling): room = main field 12'-0 3/4\"", f'{AL}/A/img/A301_L1_RCP_tags.png'),
      ("216", 8.9167, "1/A7.23 tag 'GYP-1 8'-11\"' (corridor 216)", "both readers read the same tags; 8'-0 1/2\" is the WS-1 wood slat nook (other trade), not the corridor ceiling: room = 8'-11\"", f'{AL}/A/img/A723_1_L2_corridor_tags.png'),
      ("102", 5.3333, "1/A3.01 tag 'ACT-1 5'-4\"' as printed", "only H-B listed it; the tag is printed 5'-4\" (below every wall of the level, a drafting default); no wall height depends on it", f'{AL}/B/img/R01_A3.01_L1_RCP_tags.png'),
      ("103", 5.3333, "1/A3.01 tag 'GYP-2 5'-4\"' as printed", "only H-B listed it; printed 5'-4\" (drafting default); no wall height depends on it", f'{AL}/B/img/R01_A3.01_L1_RCP_tags.png'),
      ("114", 5.3333, "1/A3.01 tag 'ACT-1 5'-4\"' as printed", "only H-B listed it; printed 5'-4\" (drafting default); no wall height depends on it", f'{AL}/B/img/R01_A3.01_L1_RCP_tags.png'),
      ("122", 5.3333, "1/A3.01 tag 'ACT-1 5'-4\"' as printed", "only H-B listed it; printed 5'-4\" (drafting default); no wall height depends on it", f'{AL}/B/img/R01_A3.01_L1_RCP_tags.png'),
      ("124", 12.0625, "1/A3.01 ceiling elevation '12'-0 3/4\"' (retail main field)", "only H-B listed it (A left the retail ceiling unprinted); main field 12'-0 3/4\", the 11'-0\" north band is a band", f'{AL}/B/img/R01_A3.01_L1_RCP_tags.png'),
      ("109", 9.5, "A3.01 tag 'GYP-1 9'-6\"' (janitor / vestibule 109)", "only H-A listed it; printed tag", f'{AL}/A/img/A301_L1_RCP_tags.png'),
      ("217", 8.0417, "1/A7.23 tag 'WS-1 8'-0 1/2\"' (lobby 217)", "only H-A listed it; printed tag (WS-1, other trade)", f'{AL}/A/img/A723_1_L2_corridor_tags.png'),
      ("316", 8.9167, "1/A7.23 / A7.24 corridor 316 'GYP-1 8'-11\"' (same as 216)", "only H-B listed it (A: 'Sim' tag without text); printed 8'-11\" in the typical corridor detail", f'{AL}/B/img/R01_A3.01_L1_RCP_tags.png'),
      ("318", 8.9167, "corridor 318 'GYP-1 8'-11\"' (same as 216 / 218)", "only H-B listed it (A: 'Sim' tag without text); printed 8'-11\" in the typical corridor detail", f'{AL}/B/img/R01_A3.01_L1_RCP_tags.png')]
for k_, h_, s_, m_, im_ in RC:
    res.append({"Wall ID": "ROOM " + k_, "Resolution": m_, "Image": im_, "Printed H": f"{h_:.4f}", "Source": s_, "Operation": "", "Status": "CONFIRMED"})
with open(f'{AL}/ALTURAS_AB_RESOLUCION.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(res[0])); w.writeheader(); w.writerows(res)
print("cuartos resueltos:", len(RC))
