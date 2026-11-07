"""Evidencia rev6 (auditoría COORDINACIÓN): marcas verificadas sobre tinta (planmark.Hoja.verify vía imgs2.png)."""
import sys, json
sys.path.insert(0, '/root/cr/rev_codigo/code'); sys.path.insert(0, '/root/cr/work/scripts')
import imgs2, pymupdf as fitz
imgs2.O = '/root/cr/work/etapas/4_canon/img/rev6/'
B = '/root/cr/work/plans/bidset.pdf'; L = '/root/cr/work/plans/bidset_SIN_MARKUPS.pdf'
d = fitz.open(B)
def w(pg, txt, clip=None):
    r = d[pg].search_for(txt, clip=fitz.Rect(*clip) if clip else None)
    assert r, (pg, txt); return [(x.x0, x.y0, x.x1, x.y1) for x in r]
# E1: 2/ y 4/A7.31 (rated assembly, 12'-0 3/4" en su underside), 7/A7.31
m = [(f'RATED{i}', r) for i, r in enumerate(w(69, "RATED", (150, 30, 1600, 300)))]
m += [(f'L12_{i}', r) for i, r in enumerate(w(69, "12' - 0 3/4\"", (150, 30, 1600, 300)))]
imgs2.png('E1_A731_sections_2_4.png', B, 69, (150, 30, 1600, 300), marcas=m, label='E1 - 2/A7.31 & 4/A7.31: 12\'-0 3/4" = underside of the 1\'-11 1/4" RATED ASSEMBLY (FS-1 membrane)')
m = [(f'L7_{i}', r) for i, r in enumerate(w(69, "12' - 0 3/4\"", (150, 560, 800, 1600)))] + [('PANEL', w(69, "CEILING PANEL", (150, 1300, 800, 1600))[0])]
imgs2.png('E1_A731_detail_7.png', B, 69, (150, 760, 800, 1600), marcas=m, label='E1 - 7/A7.31: 12\'-0 3/4" at the rated membrane; suspended ceiling panel at 11\'-0"')
m = [('NOTE', w(11, "IN THE LOBBY")[0])]
imgs2.png('E1_A008_note.png', B, 11, (170, 1085, 500, 1155), marcas=m, label='E1 - A0.08: GC MAY ADD LAYER OF GYP BD (GC option, not in the base)')
# E2: 1/A2.02 shower 201: cara del wall y=353.6 (antes 358.0)
imgs2.png('E2_A202_shower201.png', L, 17, (840, 335, 935, 400), lineas=[('WALLFACE', (858.7, 353.6), (917.0, 353.6)), ('CURB', (858.7, 385.0), (876.4, 385.0))],
          label='E2 - 1/A2.02 shower 201: side length = wall face y 353.6 to curb y 385.0 = 31.4/9 = 3.49 ft (was 3.0 from the pan diagonals)')
# O2: 7/A7.23
m = [('B', w(66, '4 1/2"', (600, 1400, 700, 1460))[0]), ('V', w(66, '6 1/2"', (480, 1400, 520, 1460))[0]), ('DIFF', w(66, 'DIFFUSER BOX')[0]), ('T', w(66, '7 3/4"', (240, 1470, 700, 1500))[0])]
imgs2.png('O2_A723_detail_7.png', B, 66, (180, 1200, 760, 1600), marcas=m, label='O2 - 7/A7.23: cove bottom 4 1/2" (7 3/4" = DIFFUSER BOX, HVAC), vertical 6 1/2"; same on L2 / L3 / L4')
# O1: cuartos medidos en vectores (rectángulos = dibujo; el SF impreso se circula)
pa = json.load(open('/root/cr/work/etapas/4_canon/out/perimetros_angle.json'))
PG = {'A2.01': 16, 'A2.04': 19, 'A3.02': 22, 'A3.03': 23}
for r in pa['filas']:
    if r.get('metodo') != 'vector':
        continue
    pg = PG[r['hoja']]; R_ = r['rects']
    clip = (min(a[0] for a in R_) - 25, min(a[2] for a in R_) - 25, max(a[1] for a in R_) + 25, max(a[3] for a in R_) + 25)
    imgs2.png(f"O1_{r['ref']}.png", L, pg, clip, rects=[(a[0], a[2], a[1], a[3], (230, 0, 0)) for a in R_],
              label=f"O1 - {r['ref']} angle molding = room perimeter {r['despues']} LF ({r['hoja']}; polygon {r['area_chk'][0]} SF vs printed {r['area_chk'][1]} SF)")
print('\n'.join(map(str, imgs2.LOG[-20:])))
