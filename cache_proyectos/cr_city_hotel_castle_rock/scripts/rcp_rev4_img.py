#!/usr/bin/env python3
"""CR City Hotel rev4 - evidencia visual de la revisión de RCP y del barrido de walls -0 hacia Retail 124 (orden del usuario:
'revisa los rcp ... algunas areas que no tomaste en cuenta' / 'todo ese numero de paredes en realidad existe').
Cada imagen = recorte de la hoja citada con el área medida (rectángulo / polígono en ROJO) o la nota / tag circulado.
Salida: etapas/4_canon/img/rcp_rev4/*.png y copia en etapas/4_canon/img/rfi/REV4_*.png (Review Items del Excel)."""
import os, json, math, shutil
import pymupdf as fitz
W = '/root/cr/work'
D = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
HS = list(json.load(open(f'{W}/set_texto.json'))['hojas'])
OUT = f'{W}/etapas/4_canon/img/rcp_rev4'; RFI = f'{W}/etapas/4_canon/img/rfi'
os.makedirs(OUT, exist_ok=True); os.makedirs(RFI, exist_ok=True)
ROJO, AZUL = (1, 0, 0), (0, 0.3, 1)


def img(name, sh, clip, rects=(), polys=(), ovals=(), circ_txt=(), title='', dpi=110, minus=()):
    doc = fitz.open(); doc.insert_pdf(D, from_page=HS.index(sh), to_page=HS.index(sh)); p = doc[0]
    for r in rects:
        p.draw_rect(fitz.Rect(*r), color=ROJO, width=2.5)
    for pl in polys:
        p.draw_polyline([fitz.Point(*q) for q in pl] + [fitz.Point(*pl[0])], color=ROJO, width=2.5)
    for r in ovals:
        p.draw_oval(fitz.Rect(*r), color=ROJO, width=2.5)
    for r in minus:   # zonas deducidas (WS-1, otro oficio) en azul
        p.draw_rect(fitz.Rect(*r), color=AZUL, width=2.0)
    for t in circ_txt:
        for r in p.search_for(t, clip=fitz.Rect(*clip)):
            p.draw_oval(fitz.Rect(r.x0 - 8, r.y0 - 8, r.x1 + 8, r.y1 + 8), color=ROJO, width=2.5)
    p.insert_text((clip[0] + 6, clip[1] + 16), f"{title} ({sh})", fontsize=12, color=ROJO)
    p.get_pixmap(dpi=dpi, clip=fitz.Rect(*clip)).save(f'{OUT}/{name}.png')
    shutil.copy(f'{OUT}/{name}.png', f'{RFI}/RCPREV_{name}.png')
    return f'{OUT}/{name}.png'


hechos = [
    # F1 BAR 107: campo de gyp (rojo) menos el óvalo WS-1 (azul) en 1/A7.31
    img('F1_bar107_A731', 'A7.31', (1450, 520, 2350, 840), rects=[(1548.1, 592.1, 2171.4, 762.6)],
        title='rev4 F1 BAR 107 suspended GYP field (red box) minus the WS-1 oval inside it = 121.6 SF'),
    img('F1_bar107_A504', 'A5.04', (0, 0, 2592, 1728), circ_txt=['BAR SUSPENDED', "CLG 11' - 0\""], title='rev4 F1 A5.04 BAR SUSPENDED GYP CEILING, CLG 11\'-0"', dpi=45),
    # F2 franja sur del lobby en 2/A7.50
    img('F2_lobby_south_A750', 'A7.50', (1450, 40, 2050, 300), polys=[[(1570.8, 74.4), (1941.8, 74.4), (1941.8, 175.4), (1570.8, 175.4)]],
        circ_txt=["11' - 0\""], title='rev4 F2 LOBBY south strip GYP-1 11\'-0" 119.0 SF'),
    # D6 nicho entre el BAR y los toilets 110/111
    img('D6_niche_A731', 'A7.31', (2050, 480, 2450, 760), rects=[(2171.4, 572.4, 2295.5, 677.3)], title='rev4 D6 niche 40.2 SF (outside CLG-L1-08)'),
    # D4 GENERATOR 103 en forma de L hasta la línea del portón (3/A7.45)
    img('D4_generator103_A745', 'A7.45', (1380, 620, 1840, 910),
        polys=[[(1483.6, 666.8), (1781.5, 666.8), (1781.5, 864.4), (1441.7, 864.4), (1441.7, 720.0), (1483.6, 720.0)]],
        title='rev4 D4 GENERATOR 103 GYP-2 200.4 SF (L-shape)'),
]
# D2 paneles WS-1 (medidos por las tablillas vectoriales) en A7.23 / A7.24
WS = {'A7.23': [(1416.2, 510.5, 1487.2, 667.8), (1244.3, 1247.8, 1487.2, 1328.2), (1892.9, 510.2, 1963.9, 667.7), (1721.0, 1247.8, 1963.9, 1328.2),
                (2369.6, 510.2, 2440.6, 667.7), (2197.7, 1247.8, 2440.6, 1328.2)],
      'A7.24': [(1723.7, 344.2, 1881.0, 426.2), (1723.7, 847.9, 1881.0, 930.0), (1723.7, 1351.6, 1881.0, 1433.6)]}
for sh, rs in WS.items():
    hechos.append(img(f'D2_WS1_{sh.replace(".", "")}', sh, (1100, 300, 2592, 1500), rects=rs, title='rev4 D2 WS-1 wood slat panels deducted from the GYP-1 corridor ceilings', dpi=50))
# F3 franja GYP-1 11'-0" al sur del storefront = dentro de Retail 124 (A3.01) + nota de tenant (A2.01)
hechos.append(img('F3_retail_band_A301', 'A3.01', (980, 900, 1820, 1140), circ_txt=['GYP-1'], title='rev4 F3 GYP-1 11\'-0" band inside RETAIL 124 (by tenant, RFI-05)', dpi=80))
hechos.append(img('F3_retail_note_A201', 'A2.01', (980, 900, 1820, 1140), circ_txt=['*NOTE:', 'RETAIL', '124'], title='rev4 F3 RETAIL 124 + tenant note', dpi=80))
# Vestíbulo 114: ACT-1 (otro oficio)
hechos.append(img('V114_A301', 'A3.01', (480, 980, 820, 1200), circ_txt=['ACT-1'], title='rev4 Vestibule 114: ACT-1 (other trade)'))
# Walls -0 hacia Retail 124: corte de XW.6.3-L1-01 y FI.2-L1-06, XW.6.4-L1-04 fuera (1/A2.01)
hechos.append(img('W_retail_A201_pier', 'A2.01', (1000, 870, 1160, 1000), rects=[(1060.5, 908.4, 1070.5, 926.6)], minus=[(1060.5, 926.6, 1070.5, 958.6), (1056.2, 958.6, 1066.2, 967.6)],
                  title='rev4 XW.6.3-L1-01 kept (red) / retail parts excluded (blue)', dpi=150))
hechos.append(img('W_retail_A201_FI2', 'A2.01', (930, 1150, 1340, 1310), rects=[(952.1, 1280.0, 1017.2, 1289.3)], minus=[(1017.2, 1280.0, 1312.4, 1289.3)],
                  circ_txt=['FI.2'], title='rev4 FI.2-L1-06 kept (red) / Retail 124 part excluded (blue)', dpi=110))
print(len(hechos), 'imagenes en', OUT)
# F4 / F5: Cleaning 215 GYP-1 9'-2" (1/A3.02) y closets 222 / 223 (2/A7.05)
print(img('F4_cleaning215_A302', 'A3.02', (650, 300, 960, 480), circ_txt=['GYP-1', "9' - 2\""], title='rev4 F4 Cleaning 215 GYP-1 9\'-2" (dropped, below FS-1)'))
print(img('F5_closets_A705', 'A7.05', (900, 620, 1250, 760), circ_txt=["9' - 2\""], title='rev4 F5 closets GYP-1 9\'-2"'))
