#!/usr/bin/env python3
"""rev9 grupo MISC: contornos reales de los misc (escalados / localizadores) medidos en vectores.
Salida: contornos_MISC.json + PNG por clave en etapas/4_canon/img/rev9/MISC_*.png"""
import sys, json
sys.path.insert(0, '/root/cr/work/etapas/4_canon/rev9')
import fitz
from PIL import Image, ImageDraw
from MISC_util import page, area
W = '/root/cr/work'
OUT = f'{W}/etapas/4_canon/rev9/contornos_MISC.json'
IMG = f'{W}/etapas/4_canon/img/rev9'
SC = {'A7.45': 324, 'A7.30': 324, 'A7.31': 324, 'A7.50': 324, 'A6.01': 324,
      'A2.01': 81, 'A2.02': 81, 'A2.03': 81, 'A2.04': 81, 'A3.01': 81, 'A3.02': 81, 'A3.03': 81, 'A3.04': 81}
PTFT = {k: v ** 0.5 for k, v in SC.items()}


def rect(x0, y0, x1, y1): return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def img(sh, fn, clip, red=(), blue=(), lines=(), holes=(), S=None, txt=''):
    p = page(sh); clip = fitz.Rect(*clip)
    S = S or min(4.0, 1400 / max(clip.width, clip.height))
    pix = p.get_pixmap(matrix=fitz.Matrix(S, S), clip=clip)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); d = ImageDraw.Draw(im)
    T = lambda q: ((q[0] - clip.x0) * S, (q[1] - clip.y0) * S)
    for P in blue:
        Q = [T(q) for q in P]; d.line(Q + [Q[0]], fill=(0, 90, 255), width=3)
    for P in list(red) + list(holes):
        Q = [T(q) for q in P]; d.line(Q + [Q[0]], fill=(225, 0, 0), width=3)
    for a, b in lines:
        d.line([T(a), T(b)], fill=(225, 0, 0), width=4)
    d.rectangle([0, 0, 8 + 7 * len(txt), 16], fill=(255, 255, 255)); d.text((4, 3), txt, fill=(225, 0, 0))
    fn = f'{IMG}/MISC_{fn}.png'; im.save(fn); return fn


R = {}


def put(k, **kw):
    R[k] = kw


def err(a, b): return round((a - b) / b * 100, 2)


# ---------------- CLG-L1-01 GENERATOR 103, 3/A7.45 ----------------
P = [[1483.56, 666.84], [1782.24, 666.84], [1782.24, 864.36], [1445.52, 864.36], [1445.52, 720.0], [1483.56, 720.0]]
a = area(P) / 324
put('CLG-L1-01', sheet='A7.45', polygon=P, area_sf=round(a, 2), sf_cargado=200.4, sf_impreso=None,
    cuadra_con='cargado' if abs(err(a, 200.4)) <= 2 else 'NO CUADRA', err_pct=err(a, 200.4), nhoja='3/A7.45',
    metodo='caras 3/A7.45: N y=666.84 (cara int. muro N) / S y=864.36 / E x=1782.24 (cara int. muro E; el op usó 1781.5) / '
           'W x=1445.52 = línea de la reja CHAIN LINK FENCE AND GATE (el op usó 1441.7 = extremo del muro S); muesca W de x=1483.56 sobre y<720.0 '
           '(muro 1472.16-1483.56 / 708.6-720.0). Rectángulos del op sin escalar, bordes ajustados a la cara dibujada.',
    img=img('A7.45', 'CLG-L1-01', (1420, 640, 1810, 890), red=[P], txt=f'CLG-L1-01 {a:.1f} SF vs 200.4'),
    nota='[DERIVADO] 199.0 SF = 336.72x197.52 - 38.04x53.16 pt2 /324. El cargado (200.4) cuadra (-0.7 %). El polígono actual (escalado desde 214.1) sobra.')

# ---------------- CLG-L1-08 JANITOR 109 + vestíbulo, 1/A7.30 ----------------
P1 = rect(2150.04, 246.96, 2222.28, 299.04); P2 = rect(2150.04, 309.12, 2222.28, 437.52)
a = (area(P1) + area(P2)) / 324
put('CLG-L1-08', sheet='A7.30', polygons=[P1, P2], area_sf=round(a, 2), sf_cargado=40.25, sf_impreso=None,
    cuadra_con='cargado', err_pct=err(a, 40.25), nhoja='1/A7.30',
    metodo='caras 1/A7.30: W x=2150.04 / E x=2222.28 (muros de los toilets 110/111), N y=246.96; muro janitor/vestíbulo y=299.04-309.12 '
           'descontado; S y=437.52 = cara exterior de los muros S de los toilets (vestíbulo abierto al corredor, sin muro).',
    img=img('A7.30', 'CLG-L1-08', (2100, 220, 2280, 470), red=[P1, P2], txt=f'CLG-L1-08 {a:.2f} SF vs 40.25'),
    nota='El op dice (2222.3-2150.0)*(437.5-247.0)/324 = 42.5, pero el 40.25 cargado = ese rectángulo menos el muro janitor/vestíbulo '
         '(72.24 x 10.08 pt = 2.25 SF): janitor 11.61 + vestíbulo 28.63 = 40.24. Cuadra; el texto del op omite la deducción.')

# ---------------- CLG-L1-10 WATER ENTRY 128, A2.01 ----------------
P = rect(1249.2, 316.68, 1394.4, 421.56)
a = area(P) / 81
alt = (1394.4 - 1253.88) * (421.56 - 316.68) / 81
put('CLG-L1-10', sheet='A2.01', polygon=P, area_sf=round(a, 2), sf_cargado=182.0, sf_impreso=182.0,
    cuadra_con='NO CUADRA', err_pct=err(a, 182.0), nhoja='A2.01 (RCP 1/A3.01 sin cielo dibujado)',
    metodo='caras A2.01: W x=1249.2 (cara int. muro W 1244.16-1249.2) / E x=1394.4 (cara CMU) / N y=316.68 / S y=421.56 (cara N del muro de los toilets).',
    img=img('A2.01', 'CLG-L1-10', (1230, 300, 1415, 440), red=[P], blue=[rect(1253.88, 316.68, 1394.4, 421.56)],
            txt=f'CLG-L1-10 {a:.1f} SF vs 182 (azul: a la linea 1-HR = {alt:.1f})'),
    nota=f'[DERIVADO] 188.0 SF a caras (+3.3 % sobre 182 impreso/cargado). El 182 impreso coincide con medir el lado W a la línea '
         f'de rating discontinua x=1253.88 ({alt:.1f} SF, azul), no a la cara del muro: Revit/impreso toma ese límite. No se fuerza: '
         f'el cielo real va a la cara (188.0); el cargado queda corto 6.0 SF. En A3.01 el cuarto no tiene cielo dibujado (tipo no indicado, RFI-CR-CLG).')

# ---------------- CLG-L1-12 LOBBY field, 1/A7.31 ----------------
outer = [[1028.88, 592.08], [1548.12, 592.08], [1548.12, 1392.96], [1028.88, 1392.96], [1028.88, 1135.44], [1175.52, 1135.44],
         [1175.52, 795.12], [1028.88, 795.12]]
cof = [rect(1051.8, 631.8, 1186.68, 751.68), rect(1237.68, 631.8, 1498.56, 751.68)]
for y0, y1 in [(784.68, 904.56), (937.56, 1057.56), (1090.44, 1210.44)]:
    cof += [rect(1237.68, y0, 1351.56, y1), rect(1384.56, y0, 1498.56, y1)]
cof += [rect(1051.8, 1243.44, 1186.68, 1357.32), rect(1237.68, 1243.44, 1498.56, 1357.32)]
gross = (1548.12 - 1028.88) * (1392.96 - 592.08) / 324
stair = (1175.52 - 1028.88) * (1135.44 - 795.12) / 324
cofa = sum(area(c) for c in cof) / 324
a = area(outer) / 324 - cofa
put('CLG-L1-12', sheet='A7.31', polygon=outer, holes=cof, area_sf=round(a, 2), area_bruta_sf=round(gross, 2),
    stair_sf=round(stair, 2), cofres_sf=round(cofa, 2), sf_cargado=590.9, sf_impreso=None,
    cuadra_con='cargado', err_pct=err(a, 590.9), nhoja='1/A7.31',
    metodo='caras/líneas 1/A7.31: W x=1028.88 (cara muro W) / N y=592.08 / E x=1548.12 (borde millwork del bar = borde W de CLG-L1-125) / '
           'S y=1392.96 (borde de la banda WS-1 11\'-0"); muesca Stair 1 x<=1175.52, y 795.12-1135.44; huecos = 10 cofres en su rectángulo '
           'INTERIOR (3 líneas por cofre; el op usa la interior: 134.88/260.88/113.88 x 119.88/113.88).',
    img=img('A7.31', 'CLG-L1-12', (1000, 570, 1580, 1420), red=[outer], holes=cof, txt=f'CLG-L1-12 neto {a:.1f} SF (bruto {gross:.1f}) vs 590.9'),
    nota=f'El cargado 590.9 = campo 11\'-0" ENTRE cofres (bandas de viga, det. 5/A7.31): rectángulo {gross:.1f} - Stair 1 {stair:.1f} - '
         f'10 cofres {cofa:.1f} = {a:.1f}. El "medido 1283.4" era el rectángulo bruto. Cuadra (0.0 %). OJO: el fondo de los cofres '
         f'(GYP-1 12\'-0 3/4", tag en 1/A7.31) = {cofa:.1f} SF no aparece cargado en ningún misc (solo sus caras verticales SOF-L1-01): posible omisión [PENDIENTE].')

# ---------------- CLG-L1-125 BAR field, 1/A7.31 ----------------
oval = json.load(open(f'{W}/etapas/4_canon/rev9/MISC_oval_A731.json'))
P = rect(1548.12, 592.08, 2171.4, 762.6)
ao = area(oval) / 324
a = area(P) / 324 - ao
put('CLG-L1-125', sheet='A7.31', polygon=P, holes=[oval], area_sf=round(a, 2), area_bruta_sf=round(area(P) / 324, 2), oval_sf=round(ao, 2),
    sf_cargado=121.6, sf_impreso=None, cuadra_con='NO CUADRA', err_pct=err(a, 121.6), nhoja='1/A7.31',
    metodo='1/A7.31: W x=1548.12 / E x=2171.4 (línea del borde de la banda WS-1, 678-762) / S y=762.6 (borde N banda WS-1 en L) / '
           'N y=592.08 (cara del muro, línea del lobby); hueco = óvalo WS-1 trazado por su polilínea exterior (60 vértices, 0.48 pt): '
           'x 1548.12-2087.76, y 610.08-736.08, rectas 1602.0-2033.76.',
    img=img('A7.31', 'CLG-L1-125', (1520, 570, 2200, 790), red=[P], holes=[oval], txt=f'CLG-L1-125 {a:.1f} SF vs 121.6'),
    nota=f'[DERIVADO] {a:.1f} SF (+3.6 %). El op descontó el óvalo como 431.8x126 + pi*63^2 = 66,875.8 pt2 (extremos semicirculares r=63, '
         f'ancho 557.8 que se sale del campo 9 pt por el W); el óvalo dibujado mide 539.6 de ancho (extremos de ~54 pt con tramo recto) = '
         f'{area(oval):,.0f} pt2. El cargado sobre-descuenta {66875.8 / 324 - ao:.1f} SF.')

# ---------------- CLG-L1-126 LOBBY S strip, 2/A7.50 ----------------
P1 = rect(1570.8, 78.12, 1941.84, 175.2); P2 = rect(1793.4, 175.2, 1873.2, 188.3)
a = (area(P1) + area(P2)) / 324
put('CLG-L1-126', sheet='A7.50', polygons=[P1, P2], area_sf=round(a, 2), sf_cargado=119.0, sf_impreso=None,
    cuadra_con='NO CUADRA', err_pct=err(a, 119.0), nhoja='2/A7.50',
    metodo='2/A7.50: W x=1570.8 (cara muro W) / E x=1941.84 (cara del tabique de vidrio, línea 78.0-175.2) / N y=78.12 (cara interior '
           'del storefront) / S y=175.2 (cara N de los muros 1647-1792 y 1873-2027) + franja del op sobre el pasaje x 1793.4-1873.2 hasta y=188.3.',
    img=img('A7.50', 'CLG-L1-126', (1540, 50, 1980, 210), red=[P1, P2], txt=f'CLG-L1-126 {a:.1f} SF vs 119.0'),
    nota=f'[DERIVADO] {a:.1f} SF (-3.9 %). El op midió el borde N en y=74.4 (línea gruesa 0.72 = eje/mullion del storefront, no la cara '
         f'interior 78.12): 371.0 x 3.7 pt = 4.3 SF de más. El cargado 119.0 está alto.')

# ---------------- CLG-L1-18 ELEVATOR CONTROLS 116, 1/A7.50 ----------------
P = [[1410.36, 1053.12], [1488.96, 1053.12], [1488.96, 1091.52], [1557.24, 1091.52], [1557.24, 1190.88], [1410.36, 1190.88]]
a = area(P) / 324
put('CLG-L1-18', sheet='A7.50', polygon=P, area_sf=round(a, 2), sf_cargado=54.35, sf_impreso=None, cuadra_con='cargado',
    err_pct=err(a, 54.35), nhoja='1/A7.50 (RCP 2/A7.50 GYP-2 9\'-6")',
    metodo='caras 1/A7.50: W x=1410.36 / N y=1053.12 / S y=1190.88 / E x=1557.24; chase NE restado a su cara exterior x=1488.96, y=1091.52.',
    img=img('A7.50', 'CLG-L1-18', (1390, 1030, 1580, 1215), red=[P], txt=f'CLG-L1-18 {a:.2f} SF vs 54.35'),
    nota='Cuadra exacto con el op (rect - chase). El "medido 70.5" del polígono escalado era erróneo.')

# ---------------- L2/L3 corridors ----------------
def corr216(x_e=852.72, x_w=799.2):
    return [[x_w, 446.76], [x_e, 446.76], [x_e, 1007.64], [x_w, 1007.64], [x_w, 613.8], [765.0, 613.8], [765.0, 622.2],
            [709.44, 622.2], [709.44, 523.44], [x_w, 523.44]]


def corr218(x_w=799.2):
    return [[x_w, 1212.0], [1424.52, 1212.0], [1424.52, 1144.56], [1588.56, 1144.56], [1588.56, 1185.0], [1478.04, 1185.0],
            [1478.04, 1227.12], [1484.04, 1227.12], [1484.04, 1271.04], [x_w, 1271.04]]


ws_mid = rect(808.18, 654.9, 843.58, 726.9)      # 1/A3.02 821.28-856.68 x 674.4-746.4 -> plano (-13.1,-19.5)
ws_sur = rect(722.26, 1020.3, 843.58, 1060.5)    # 1/A3.02 735.36-856.68 x 1039.8-1080.0 (LOBBY 217)
conector = rect(799.2, 1007.64, 852.72, 1212.0)
for k, sh, num, nh in [('CLG-L2-56', 'A2.02', '216', '1/A2.02 (RCP 1/A3.02, 1/A7.23)'), ('CLG-L3-87', 'A2.03', '316', '1/A2.03 (RCP 1/A3.03, 2/A7.23)')]:
    P = corr216(); g = area(P) / 81; net = g - 34.5
    put(k, sheet=sh, polygon=P, area_sf=round(g, 2), area_neta_sf=round(net, 2), ws1_dentro_sf=34.5, sf_cargado=360.2, sf_impreso=455.0,
        cuadra_con='NO CUADRA', err_pct=err(net, 360.2), err_bruto_vs_impreso_pct=err(g, 455.0), nhoja=nh,
        metodo='caras: N y=446.76 (muro de 215/415) / E x=852.72 (cara W muros de unidades) / W x=799.2 (caras E de ascensor N y Stair) / '
               'jog del tag x 709.44-799.2, y 523.44-613.8/622.2 / S y=1007.64 = línea del frente del ascensor S donde está el SMOKE CURTAIN. '
               'Neto = contorno - panel WS-1 medio (3.94 x 8.75 = 34.5, en azul).',
        img=img(sh, k, (690, 430, 870, 1225), red=[P], blue=[ws_mid, ws_sur, conector],
                txt=f'{k} {num}: contorno {g:.1f}, neto {net:.1f} vs 360.2 (azul: WS-1 medio, WS-1 sur=LOBBY, conector)'),
        nota=f'Cargado 360.2 = 455 impreso - WS-1 medio 34.5 - WS-1 "sur" 60.3. El panel sur (13.49 x 4.47) NO está en el corredor {num}: '
             f'en 1/A3.0x está al S del SMOKE CURTAIN, sobre el LOBBY {int(num) + 1} (x<799) y el conector (azul). Contorno medido {g:.1f} SF '
             f'({err(g, 455.0):+.1f} % sobre el impreso 455; el límite Revit {num}/conector no está dibujado: con 455 caería en y~975). '
             f'Neto {net:.1f} (o 455-34.5 = 420.5): el cargado está bajo ~60-80 SF. Además el conector x 799.2-852.72, y 1007.64-1212.0 '
             f'({area(conector) / 81:.1f} SF, azul) entre {num} y {int(num) + 2} no está en ningún op [PENDIENTE].')
for k, sh, num, carg, opg in [('CLG-L2-58', 'A2.02', '218', 525.4, 565.3), ('CLG-L3-88', 'A2.03', '318', 574.6, 614.5)]:
    P = corr218(799.2 if sh == 'A2.02' else 799.08); g = area(P) / 81; net = g - 39.9
    put(k, sheet=sh, polygon=P, area_sf=round(g, 2), area_neta_sf=round(net, 2), ws1_dentro_sf=39.9, sf_cargado=carg, sf_impreso=None,
        cuadra_con='NO CUADRA' if abs(err(net, carg)) > 2 else 'cargado', err_pct=err(net, carg), nhoja=nh.replace('216', '218') if False else
        ('1/A2.02 (RCP 1/A3.02, 1/A7.24)' if sh == 'A2.02' else '1/A2.03 (RCP 1/A3.03, 2/A7.24)'),
        metodo='caras: N y=1212.0 (caras S de unidades) / S y=1271.04 (muro exterior) / W x=799.2 (cara E de 210/221 y 310/321: esquina incluida) / '
               'jog x=1424.52 hasta y=1144.56 / brazo E y 1144.56-1185.0 cerrado en el muro de la puerta 209.1/309.1 x=1588.56 / Stair 2 W '
               'x=1478.04 (1185-1227) y 1484.04 (1227-1271). Neto = contorno - WS-1 39.9 (8.74 x 4.56).',
        img=img(sh, k, (780, 1120, 1640, 1290), red=[P], blue=[rect(799.2, 1007.64, 852.72, 1212.0)], txt=f'{k} {num}: contorno {g:.1f}, neto {net:.1f} vs {carg}'),
        nota=(f'Op {opg} bruto: ' + ('arranca en x=858.7 (deja fuera la esquina 799.2-858.7 = 43.4 SF) y lleva el brazo E hasta 1620.8, '
                                     'cruzando el muro de la puerta 209.1 (+16 SF).' if sh == 'A2.02' else
                                     'omite la parte baja del jog (1424.5-1478 x 1186-1212 = 17 SF) y lleva el brazo E hasta 1650, cruzando el '
                                     'muro de la puerta 309.1 en x=1588.56 (+31 SF).') +
              f' Contorno a caras {g:.1f} -> neto {net:.1f} vs cargado {carg} ({err(net, carg):+.1f} %).'))

# ---------------- CLG-L2-122 CLEANING 215, A2.02 ----------------
P = [[745.92, 353.64], [852.72, 353.64], [852.72, 440.76], [793.2, 440.76], [793.2, 455.4], [745.92, 455.4]]
a = area(P) / 81
put('CLG-L2-122', sheet='A2.02', polygon=P, area_sf=round(a, 2), sf_cargado=123.0, sf_impreso=123.0, cuadra_con='impreso / cargado',
    err_pct=err(a, 123.0), nhoja='1/A2.02 (RCP 1/A3.02)',
    metodo='caras A2.02: W x=745.92 / N y=353.64 / E x=852.72 / S y=440.76 (muro con puerta 215.1, desde x=793.2) y y=455.4 (frente del '
           'ascensor N, línea del smoke curtain) en x 745.92-793.2.',
    img=img('A2.02', 'CLG-L2-122', (725, 335, 875, 475), red=[P], txt=f'CLG-L2-122 {a:.1f} SF vs 123'),
    nota='El op (118.6) cortaba en y=463.4-19.5 sin el entrante hasta el ascensor; con él cuadra con el impreso 123 (+0.3 %).')

# ---------------- CLG-L3-104 closet 323, A2.03 ----------------
P = rect(932.64, 1183.56, 964.08, 1206.0); a = area(P) / 81
put('CLG-L3-104', sheet='A2.03', polygon=P, area_sf=round(a, 2), sf_cargado=8.8, sf_impreso=None, cuadra_con='cargado', err_pct=err(a, 8.8),
    nhoja='1/A2.03 (A7.05 2 GYP-1 9\'-2")', metodo='caras A2.03: W 932.64 / E 964.08 / N 1183.56 / S 1206.0 (muro del corredor con puerta 323.1).',
    img=img('A2.03', 'CLG-L3-104', (915, 1165, 985, 1220), red=[P], txt=f'CLG-L3-104 {a:.2f} SF vs 8.8'), nota='Cuadra (-1.0 %).')

# ---------------- CLG-L4-118 MEN 418 / CLG-L4-119 ELEC 421, A2.04 ----------------
P = rect(684.48, 1143.36, 781.32, 1222.2); a = area(P) / 81
put('CLG-L4-118', sheet='A2.04', polygon=P, area_sf=round(a, 2), sf_cargado=94.0, sf_impreso=94.0, cuadra_con='impreso / cargado',
    err_pct=err(a, 94.0), nhoja='1/A2.04 (3/A7.50)', metodo='caras A2.04: W 684.48 / E 781.32 (muro hacia ELEC 421) / N 1143.36 / S 1222.2.',
    img=img('A2.04', 'CLG-L4-118', (665, 1125, 815, 1240), red=[P], blue=[rect(784.92, 1147.8, 796.68, 1222.2)], txt=f'CLG-L4-118 {a:.2f} SF vs 94'),
    nota='Cuadra (+0.3 %); el op usaba 683.5-784.0 (eje/cara opuesta) = 97.1.')
P = rect(784.92, 1147.8, 796.68, 1222.2); a = area(P) / 81
put('CLG-L4-119', sheet='A2.04', polygon=P, area_sf=round(a, 2), sf_cargado=11.0, sf_impreso=11.0, cuadra_con='impreso / cargado',
    err_pct=err(a, 11.0), nhoja='1/A2.04 (3/A7.50)', metodo='caras A2.04: W 784.92 / E 796.68 / N 1147.8 (cara del cierre N del cuarto; la caja del montante/tubería queda entre 1143.2 y 1147.8) / S 1222.2.',
    img=img('A2.04', 'CLG-L4-119', (770, 1130, 812, 1235), red=[P], txt=f'CLG-L4-119 {a:.2f} SF vs 11'),
    nota='Cuadra (-1.8 %); el op (12.7) tomaba ejes 784.4-797.0 x 1142.4-1224.0.')

# ---------------- CLG-L2-64 mezzanine 219 (localizador) ----------------
P = rect(1129.56, 405.36, 1352.16, 573.0); a = area(P) / 81
dev = a * (2 * 10.85) / ((573.0 - 405.36) / 9)
put('CLG-L2-64', sheet='A2.02', polygon=P, area_sf=round(a, 2), area_desarrollada_sf=round(dev, 2), sf_cargado=536.7, sf_impreso=462.0,
    cuadra_con='impreso (planta) ; cargado = planta x pendiente', err_pct=err(dev, 536.7), err_planta_vs_impreso_pct=err(a, 462.0),
    nhoja='1/A2.02 (A3.02 sin cielo; pendiente 1/A4.04)',
    metodo='contorno_cielos.medir(A2.02, 219) = flood + ajuste a caras: x 1129.56-1352.16 (24.73 ft), y 405.36-573.0 (18.63 ft).',
    img=img('A2.02', 'CLG-L2-64', (1100, 380, 1380, 600), red=[P], txt=f'CLG-L2-64 planta {a:.1f} (impreso 462); desarrollado {dev:.1f} vs 536.7'),
    nota=f'Planta {a:.1f} SF = impreso 462 (-0.3 %). El cargado 536.7 = 2 x 10.85 ft (faldón medido en 1/A4.04) x 24.73 ft: es el área '
         f'desarrollada sobre la pendiente del techo (factor 21.70/18.63 = 1.165), no un error. Antes era un LOCATOR en el tag 219.')

# ---------------- CAN-L1-ENTRY ----------------
P = rect(1070.76, 858.96, 1124.76, 917.4); a = area(P) / 81
put('CAN-L1-ENTRY', sheet='A3.01', polygon=P, area_sf=round(a, 2), sf_cargado=58.2, sf_impreso=None, cuadra_con='NO CUADRA',
    err_pct=err(a, 58.2), nhoja='1/A3.01 (=1/A7.31 1693.44-1801.32 x 1228.56-1346.0); sección 08/A9.05',
    metodo='rectángulo dibujado en el RCP fuera del vestíbulo de acero y vidrio 108.1 (STEEL ENTRANCE CUSTOM): x 1070.76-1124.76 '
           '(6.00 ft), y 858.96-917.40 (6.49 ft); el mismo en 1/A7.31 a 1/4" (5.99 x 6.52 ft).',
    img=img('A3.01', 'CAN-L1-ENTRY', (1000, 820, 1150, 950), red=[P], txt=f'CAN-L1-ENTRY {a:.1f} SF vs 58.2'),
    nota=f'El localizador estaba en VESTIBULE 114 (vestíbulo de parking, techo ACT-1): lugar equivocado. La huella dibujada del canopy '
         f'en la entrada del lobby (108.1) es 6.0 x 6.49 ft = {a:.1f} SF; el cargado usa 4.85 ft (08/A9.05) x 12\'-0" supuesto (RFI-21) = 58.2. '
         f'Con la huella dibujada: {a:.1f} SF ({err(a, 58.2):+.0f} %). Cargado alto; confirmar en RFI-21.')

# ---------------- LINES ----------------
def lf(L, sh): return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in L) / PTFT[sh]


L = []
for c in cof:
    L += [[c[i], c[(i + 1) % 4]] for i in range(4)]
v = lf(L, 'A7.31')
put('SOF-L1-01', sheet='A7.31', lines=L, lf=round(v, 2), lf_cargado=295.78, sf_cargado=314.41, area_sf=round(v * 1.063, 2),
    cuadra_con='cargado', err_pct=err(v, 295.78), nhoja='1/A7.31',
    metodo='perímetro de los 10 cofres en su línea interior (la misma que el op), vectores 1/A7.31 a 18 pt/ft.',
    img=img('A7.31', 'SOF-L1-01', (1000, 570, 1580, 1420), lines=L, txt=f'SOF-L1-01 {v:.2f} LF vs 295.78'),
    nota='Recorrido real dibujado (antes 15 líneas paralelas de localizador). SF = LF x 1.063 ft de cara.')
L = [[[303.84, 1328.34], [460.8, 1328.34]]]
v = lf(L, 'A6.01')
put('SOF-L4-01', sheet='A6.01', lines=L, lf=round(v, 2), lf_cargado=8.73, sf_cargado=74.99, area_sf=round(v * 8.59, 2),
    cuadra_con='cargado (7/A6.01 8\'-8 3/4" impreso)', err_pct=err(v, 8.73), nhoja='7/A6.01 (sección 11/A6.01)',
    soffit_planta=rect(303.84, 1328.34, 460.8, 1446.96),
    metodo='7/A6.01: caras de acabado W 303.84 / E 460.8 (= 8\'-8 3/4" impreso), cara S 1446.96; borde libre del soffit a 6.59 ft '
           '(119.2 pt medidos en 11/A6.01) de la cara S: y=1328.34. La línea es ese borde a todo el ancho.',
    img=img('A6.01', 'SOF-L4-01', (270, 1090, 500, 1480), lines=L, blue=[rect(303.84, 1328.34, 460.8, 1446.96)], txt=f'SOF-L4-01 {v:.2f} LF vs 8.73'),
    nota='La planta 7/A6.01 no dibuja el soffit/FCU: ubicación derivada de 11/A6.01 (soffit contra el muro S, lado grid 6). '
         'Antes el localizador estaba sobre el texto de la nota.')

cv = json.load(open(f'{W}/etapas/4_canon/rev9/MISC_cove_A304.json'))
L = []
def addH(y, x0, x1): L.append([[x0, y], [x1, y]])
def addV(x, y0, y1): L.append([[x, y0], [x, y1]])
for k, k2, a_, b_ in cv['V']:
    if k == 818.16 or k == 857.04 or (k == 728.88) or (k == 759.36) or k == 1487.28:
        addV(k, a_, b_)
for k, k2, a_, b_ in cv['H']:
    if k in (547.8, 632.76, 1124.16, 1102.44, 1148.16, 1236.6, 1281.0) or (k == 1226.28 and a_ > 1390):
        addH(k, a_, b_)
v = lf(L, 'A3.04')
Lb = [l for l in L if not (l[0][0] in (728.88, 759.36) or l[0][1] in (547.8, 632.76, 1124.16, 1102.44, 1148.16))]
vb = lf(Lb, 'A3.04')
put('SOF-L4-02', sheet='A3.04', lines=L, lf=round(v, 2), lf_sin_entrantes=round(vb, 2), lf_cargado=242.72, sf_cargado=222.57,
    area_sf=round(v * 0.917, 2), cuadra_con='NO CUADRA', err_pct=err(v, 242.72), nhoja='1/A3.04 (3/A7.23, 3/A7.24; det. 7/A7.23)',
    metodo='doble línea del soffit (0.24 pt, separación 3.36 pt = 4 1/2" de 7/A7.23) en 1/A3.04, línea exterior (lado muro): lado W x=818.16, '
           'lado E x=857.04 (tramo N-S), N y=1236.6 / 1226.28 y S y=1281.0 (tramo E-W), cierre E x=1487.28, más los entrantes del '
           'lobby de ascensor N (x 728.88-818.16, y 547.8-632.76) y del entrante S (x 728.88-818.16, y 1102.44-1148.16). Excluidos: '
           'panel WS-1 (1035.6-1082.5) y travesaños.',
    img=img('A3.04', 'SOF-L4-02', (700, 420, 1520, 1310), lines=L, txt=f'SOF-L4-02 {v:.1f} LF (sin entrantes {vb:.1f}) vs 242.72'),
    nota=f'Recorrido dibujado {v:.1f} LF ({vb:.1f} sin los entrantes) vs 242.72 cargado (= LF de walls hacia 412, no el trazo del RCP). '
         f'El cargado está bajo {err(vb, 242.72):+.0f} a {err(v, 242.72):+.0f} %. Aplicabilidad a L4 sigue siendo supuesta (RFI-18).')

L = [[[1076.64, 1023.12], [1076.64, 1224.24]], [[1222.8, 1023.12], [1222.8, 1224.0]], [[1369.8, 1023.12], [1369.8, 1224.24]],
     [[1515.06, 1022.4], [1515.06, 1205.04]], [[1631.22, 1020.6], [1631.22, 1196.04]],
     [[1080.72, 1228.32], [1365.72, 1228.32]], [[1517.88, 1199.76], [1659.72, 1199.76]]]
v = lf(L, 'A3.01')
put('BW-L1-RETAIL', sheet='A3.01', lines=L, lf=round(v, 2), lf_cargado=154.23, sf_cargado=399.46, area_sf=round(v * 2.59, 2),
    cuadra_con='cargado', err_pct=err(v, 154.23), nhoja='1/A3.01 (retail 124)',
    metodo='ejes de las 7 vigas de acero (par de líneas de ala 0.59 ft) en 1/A3.01: verticales x 1076.64/1222.8/1369.8/1515.06/1631.22, '
           'horizontales y 1228.32 (1080.72-1365.72) y 1199.76 (1517.88-1659.72).',
    img=img('A3.01', 'BW-L1-RETAIL', (1040, 1000, 1700, 1250), lines=L, txt=f'BW-L1-RETAIL {v:.2f} LF vs 154.23'),
    nota='Recorrido real (antes 4 líneas de localizador). Cuadra exacto; el drop 1\'-0" de los lados sigue sin cota (RFI-20).')

# =============== PASADA 2: polygons_final (keyhole, shoelace = área a cargar) ===============
def sarea(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2


def orient(P, sign):
    return P if (sarea(P) > 0) == (sign > 0) else P[::-1]


def pip(x, y, P):
    c = False
    for i in range(len(P)):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % len(P)]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def keyhole(outer, holes):
    """un solo anillo: exterior (+) con cada hueco (-) unido por un puente de ancho cero (ida y vuelta por el mismo segmento),
    puente = el más corto (perpendicular a un borde o a un vértice) que no atraviesa otro hueco."""
    ring = [list(map(float, q)) for q in orient(outer, 1)]
    todo = [[list(map(float, q)) for q in orient(h, -1)] for h in holes]
    hechos = []
    while todo:
        best = None
        for hi, h in enumerate(todo):
            otros = [o for j, o in enumerate(todo) if j != hi] + hechos
            for wi, w in enumerate(h):
                for ri in range(len(ring)):
                    a, b = ring[ri], ring[(ri + 1) % len(ring)]
                    cands = [(a, None)]
                    if abs(a[1] - b[1]) < 1e-6 and min(a[0], b[0]) < w[0] < max(a[0], b[0]): cands.append(([w[0], a[1]], ri))
                    if abs(a[0] - b[0]) < 1e-6 and min(a[1], b[1]) < w[1] < max(a[1], b[1]): cands.append(([a[0], w[1]], ri))
                    for pnt, ins in cands:
                        d = ((pnt[0] - w[0]) ** 2 + (pnt[1] - w[1]) ** 2) ** 0.5
                        if best and d >= best[0]: continue
                        ok = True
                        for t in [i / 20 for i in range(1, 20)]:
                            x, y = w[0] + (pnt[0] - w[0]) * t, w[1] + (pnt[1] - w[1]) * t
                            if any(pip(x, y, o) for o in otros) or pip(x, y, h) or not pip(x, y, ring if not hechos else outer):
                                ok = False; break
                        if ok: best = (d, hi, wi, ri, pnt, ins)
        d, hi, wi, ri, pnt, ins = best
        h = todo.pop(hi); hechos.append(h)
        hr = h[wi:] + h[:wi] + [h[wi]]
        if ins is None:
            ring = ring[:ri + 1] + hr + [ring[ri]] + ring[ri + 1:]
        else:
            ring = ring[:ri + 1] + [pnt] + hr + [pnt] + ring[ri + 1:]
    return [[round(x, 3), round(y, 3)] for x, y in ring]


def ringcheck(ring, holes_n):
    return abs(sarea(ring))


K2 = {k: SC[R[k]['sheet']] for k in R}


def final(k, rings, k2, sheet=None, huecos=0, extra=None):
    A = sum(abs(sarea(r)) for r in rings)
    R[k]['polygons_final'] = rings
    R[k]['sheet_final'] = sheet or R[k]['sheet']
    R[k]['huecos_keyhole'] = huecos
    R[k]['area_cargar_sf'] = round(A / k2, 2)
    R[k]['shoelace_pt2'] = round(A, 1)
    if extra: R[k].update(extra)
    print(f'  {k:13} shoelace {A:12.1f} pt2 / {k2} = {A / k2:8.2f} SF  anillos {len(rings)} huecos {huecos}')


print('--- pasada 2: polygons_final')
# simples
for k in ['CLG-L1-01', 'CLG-L1-10', 'CLG-L1-18', 'CLG-L2-122', 'CLG-L3-104', 'CLG-L4-118', 'CLG-L4-119', 'CAN-L1-ENTRY', 'CLG-L2-64']:
    final(k, [orient(R[k]['polygon'], 1)], K2[k])
final('CLG-L1-08', [orient(P_, 1) for P_ in R['CLG-L1-08']['polygons']], 324)   # 2 piezas separadas por el muro janitor/vestíbulo
final('CLG-L1-126', [[[1570.8, 78.12], [1941.84, 78.12], [1941.84, 175.2], [1873.2, 175.2], [1873.2, 188.3], [1793.4, 188.3],
                      [1793.4, 175.2], [1570.8, 175.2]]], 324)   # campo + franja sobre el pasaje en un solo anillo
R['CLG-L2-64']['factor_pendiente'] = 1.165
R['CLG-L2-64']['factor_pendiente_op'] = ('[DERIVADO] 2 x 10.85 ft (faldón desarrollado, 1/A4.04, op del canon) / 18.63 ft de planta '
                                         '((573.0-405.36)/9) = 21.70/18.63 = 1.165; cargado 536.7 = planta 460.7 x 1.165 = 536.6')
# lobby: exterior con muesca Stair 1 + 10 cofres
final('CLG-L1-12', [keyhole(R['CLG-L1-12']['polygon'], R['CLG-L1-12']['holes'])], 324, huecos=10)
# bar: óvalo WS-1 (toca el borde W del campo en x=1548.12)
final('CLG-L1-125', [keyhole(R['CLG-L1-125']['polygon'], R['CLG-L1-125']['holes'])], 324, huecos=1)

# corredores: se pasa el contorno del plano A2.0x al RCP A3.0x (offset del brief) y se restan los paneles WS-1 medidos en el RCP
OFF = {'A2.02': (13.1, 19.5, 'A3.02'), 'A2.03': (13.3, 18.7, 'A3.03')}
WS = {('CLG-L2-56'): rect(821.28, 671.04, 856.68, 749.76), ('CLG-L3-87'): rect(821.64, 670.2, 857.16, 748.92),
      ('CLG-L2-58'): rect(1217.52, 1240.8, 1296.24, 1281.84), ('CLG-L3-88'): rect(1217.88, 1239.96, 1296.6, 1281.0)}
WSsrc = {'CLG-L2-56': '1/A3.02 marco del panel x 821.28-856.68 (líneas del soffit) y 671.04-749.76 (= 3.93 x 8.75 ft; 1/A7.23 imprime 8\'-9")',
         'CLG-L3-87': '1/A3.03 x 821.64-857.16, y 670.2-748.92 (3.95 x 8.75 ft)',
         'CLG-L2-58': '1/A3.02 x 1217.52-1296.24 (8.75 ft = 8\'-9" impreso 1/A7.24), y 1240.8-1281.84 (entre líneas del soffit, 4.56 ft)',
         'CLG-L3-88': '1/A3.03 x 1217.88-1296.6, y 1239.96-1281.0 (8.75 x 4.56 ft)'}
for k in ['CLG-L2-56', 'CLG-L3-87', 'CLG-L2-58', 'CLG-L3-88']:
    dx, dy, rs = OFF[R[k]['sheet']]
    Pr = [[round(x + dx, 2), round(y + dy, 2)] for x, y in R[k]['polygon']]
    ws = WS[k]
    assert all(pip(x, y, Pr) for x, y in ws), k
    ring = keyhole(Pr, [ws])
    final(k, [ring], 81, sheet=rs, huecos=1,
          extra={'ws1_panel_rcp': ws, 'ws1_panel_sf': round(area(ws) / 81, 2), 'ws1_fuente': WSsrc[k],
                 'nota_final': f'polygons_final en {rs}: contorno de caras del plano {R[k]["sheet"]} trasladado ({dx}, {dy}) pt (comprobado: cara E '
                               f'{"865.68" if rs == "A3.02" else "866.04"} en el RCP vs plano+dx {852.72 + dx:.2f}) menos el panel WS-1 ubicado en el RCP.'})
    img(rs, k + '_final', (Pr and (min(q[0] for q in Pr) - 15, min(q[1] for q in Pr) - 15, max(q[0] for q in Pr) + 15, max(q[1] for q in Pr) + 15)),
        red=[ring], blue=[ws], txt=f'{k} final {R[k]["area_cargar_sf"]} SF (rojo keyhole, azul WS-1)')
# respuesta 3
for k, rs in [('CLG-L2-56', 'A3.02'), ('CLG-L3-87', 'A3.03')]:
    R[k]['rcp_gyp1'] = (f'{rs}: el corredor no lleva tag propio (el único GYP-1 9\'-2" de la zona es de CLEANING 215); el GYP-1 8\'-11" está en '
                        f'1/A7.23 (L2) / 2/A7.23 (L3). En {rs} el campo colgado está entre las dobles líneas del soffit: lado W x=817.92/821.28 '
                        f'(y 637-1036.4) y 817.9/821.3 a lo largo del ascensor N, lado E x=856.68/860.16 (y 475.6-1240.8), cierre N H 472.2/475.56 '
                        f'(contra el muro de 215). Los dos SMOKE CURTAIN (texto en (800,437) y (816,994)) apuntan a las puertas de los ascensores, '
                        f'al W de la franja: no cruzan el corredor. Por eso el "entre smoke curtains" del op es lo mismo que N y=446.76 (plano; '
                        f'466.3 RCP) a S y=1007.64 (1027.1 RCP, frente del ascensor S). Ninguna línea del RCP corta el GYP-1 ahí: el soffit E sigue '
                        f'hasta 1240.8 y el campo continúa por el conector hasta {"218" if rs == "A3.02" else "318"}. El corte S en 1007.64 es solo el límite '
                        f'de cuarto (no dibujado); el conector queda PENDIENTE. Imágenes: MISC_{k}_final.png y MISC_{k}.png.')

# 4) cofres del lobby
cof_r = [orient(c, 1) for c in cof]
put('CLG-L1-COFRES', sheet='A7.31', polygons=cof, area_sf=round(sum(area(c) for c in cof) / 324, 2), sf_cargado=None, sf_impreso=None,
    cuadra_con='NO CARGADO (clave nueva)', err_pct=None, nhoja='1/A7.31 (secciones 2/A7.31, 4/A7.31, 7/A7.31)',
    altura='[CONFIRMADO] GYP-1 12\'-0 3/4" (tag en 1/A7.31 dentro del cofre x1384-1498 y1090-1210; cota "12\' - 0 3/4"" en 2/A7.31 y 7/A7.31)',
    estructura=('[CONFIRMADO] 2/A7.31: el fondo de cofre a 12\'-0 3/4" queda en la cara inferior del "1\'-11 1/4" RATED ASSEMBLY" '
                '(joist "1\'-6" OPEN WEB" / "1\'-5 7/8" STL BEAM") bajo LEVEL 2 6211.75\'; "DROPPED SOFFIT 1\'-0 3/4"" = bandas a 11\'-0". '
                '7/A7.31: "W18X71 (DEEPEST BEAM IN LOBBY)" con 12\'-0 3/4"; nota 1/A7.31 "HIGHEST CEILING LOBBY IS DRIVEN BY DEPTH OF STEEL BEAM". '
                'En el lobby la cara inferior de estructura está a ~12\'-0 3/4", no a los 12\'-0" B.O. DECK de 5/A5.04: '
                'el fondo de cofre va prácticamente pegado a la estructura (sin bajada de colgante).'),
    metodo='rectángulo INTERIOR (3 líneas por cofre; la misma línea que el op de CLG-L1-12 y SOF-L1-01) de los 10 cofres en 1/A7.31, 18 pt/ft.',
    img=img('A7.31', 'CLG-L1-COFRES', (1000, 570, 1580, 1420), red=cof, txt='CLG-L1-COFRES 538.6 SF (10 fondos de cofre GYP-1 12\'-0 3/4")'),
    nota='Complementa CLG-L1-12 (campo 590.8 a 11\'-0") + SOF-L1-01 (caras verticales). Si se carga, son 538.6 SF de GYP-1 más.')
final('CLG-L1-COFRES', cof_r, 324)
img('A7.31', 'CLG-L1-12_final', (1000, 570, 1580, 1420), red=R['CLG-L1-12']['polygons_final'], txt=f'CLG-L1-12 final {R["CLG-L1-12"]["area_cargar_sf"]} SF keyhole')
img('A7.31', 'CLG-L1-125_final', (1520, 570, 2200, 790), red=R['CLG-L1-125']['polygons_final'], txt=f'CLG-L1-125 final {R["CLG-L1-125"]["area_cargar_sf"]} SF keyhole')

for k, r in R.items():
    r.setdefault('bath', None); r.setdefault('bath_sf', 0.0)
    if 'area_sf' in r and 'lines' not in r: r.setdefault('contorno_menos_bath_sf', r['area_sf'])
json.dump(R, open(OUT, 'w'), indent=1)
for k, r in R.items():
    print(f"{k:13} {r['sheet']:6} med {r.get('area_neta_sf', r.get('lf', r.get('area_sf')))!s:8} carg {r.get('lf_cargado', r.get('sf_cargado'))!s:7} "
          f"imp {r.get('sf_impreso')!s:6} {r['cuadra_con'][:22]:22} err {r['err_pct']}")
