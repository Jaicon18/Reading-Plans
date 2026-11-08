import sys, json; sys.path.insert(0,'/root/cr/work/scripts')
import contorno_cielos as cc
A=lambda P: round(cc.area(P)/81,2)
c=json.load(open('/root/cr/work/etapas/4_canon/takeoff_canon.json'))
CL={x['room']:x for x in c['ceilings']}
d=json.load(open('L4L1_polys.json')); U=d['U']; l=json.load(open('L4L1_l1polys.json'))
IMG='/root/cr/work/etapas/4_canon/img/rev9/'
RS={
 "401":[(858.72,356.64),(974.52,356.64),(974.52,391.92),(1003.92,391.92),(1003.92,547.32),(858.72,547.32)],
 "402":[(862.8,620.76),(974.52,620.76),(974.52,646.32),(1003.92,646.32),(1003.92,889.08),(858.72,889.08),(858.72,823.56),(862.8,823.56)],
 "403":[(539.88,794.28),(793.2,794.28),(793.2,855.72),(668.04,855.72),(668.04,922.44),(667.92,922.44),(667.92,1070.28),(568.44,1070.28),(568.44,1017.84),(539.88,1017.84)],
 "404":[(641.64,573.36),(703.68,573.36),(703.68,787.32),(568.44,787.32),(568.44,762.24),(539.88,762.24),(539.88,653.52),(659.64,653.52),(659.64,609.48),(641.64,609.48)],
 "405":[(539.88,427.2),(631.32,427.2),(631.32,427.08),(714.48,427.08),(714.48,517.2),(703.68,517.2),(703.68,566.4),(539.88,566.4)],
}
names={"401":"L4 401 Guest Room Type 11 (bedroom/closet, excl. bath)","402":"L4 402 Guest Room Type 12 (bedroom/closet, excl. bath)",
 "403":"L4 403 Guest Room Type 10 (bedroom/closet, excl. bath)","404":"L4 404 Guest Room Type 6 (bedroom/closet, excl. bath)","405":"L4 405 Guest Room Type 13 (bedroom/closet, excl. bath)"}
met={
 "401":"caras: N y=356.64 (XW.6.6 int) / W x=858.72 (W.62 corridor; 862.8 furring X-L4-01 en bath) / E x=1003.92 (XW.6.6 int) / S y=614.28 (DW.4-L4-04 cara 401); duct box FW.4 NE 974.52-1003.92 x 356.64-391.92 restado; bath = banda y 547.32 (cara dormitorio de W.4-L4-03) a 614.28, ancho completo",
 "402":"caras: N y=620.76 (DW.4-L4-04 cara 402) / W x=862.8 (FW.6 furring) y 858.72 en closet 823.56-892.2 / E x=1003.92 / S y=951.24 (X-L4-03 cara bath); duct box NE 974.52-1003.92 x 620.76-646.32 restado; bath = y 889.08 (cara closet de W.4-L4-07) a 951.24",
 "403":"caras: N y=794.28 (DW.4-L4-02 / FW.2-L4-06) / W x=539.88 (XW.6.6 int) / E x=793.2 (W.62-L4-12/13) hasta y=922.44 (FW.2-L4-08 ascensor) y x=667.92 (W.62-L4-14) / S y=1070.28 (muro 417); duct box SW 539.88-568.44 x 1017.84-1070.28 restado; bath = 668.04-793.2 x 855.72-922.44 (caras exteriores W.4-L4-14/15)",
 "404":"caras: N y=573.36 (DW.4-L4-01 cara 404) / W x=539.88 / E x=703.68 (FW.2-L4-04 escalera + W.62-L4-11) / S y=787.32 (DW.4-L4-02); duct box SW 539.88-568.44 x 762.24-787.32 restado; bath en L (closet 641.64-659.64 x 573.36-609.48 queda en el cielo) = caras exteriores W.4-L4-10/12/13",
 "405":"caras: N y=427.2 (FW.4-L4-01 cara de la franja chase) y bath N y=356.64 / W x=539.88 / E x=714.48 (FW.4-L4-05 sobre CMU ascensor servicio) y x=703.68 (W.62-L4-11) / S y=566.4 (DW.4-L4-01 cara 405); bath 631.32-739.92 x 356.64-427.08 (ducha hasta y=412.08); franja chase 539.88-628.32 x 401.64-427.2 (27.91 SF) y shaft 8/A9.03 restados",
}
out={}
for k,u in U.items():
    C=A(u['c']); B=A(u['b']); R=A(RS[k]); assert abs(R-(C-B))<0.05,(k,R,C-B)
    nm=names[k]; ld=CL[nm]['area_sf']; imp=u['imp']
    ei=(C-imp)/imp*100; ee=(C-B-imp)/imp*100
    if abs(ei)<=2: cq,err="impreso incl. bath",ei
    elif abs(ee)<=2: cq,err="impreso excl. bath",ee
    else: cq,err="NO CUADRA",min(ei,ee,key=abs)
    nota={
     "401":f"Impreso 443 INCLUYE el bath (contorno {C} vs 443, +{ei:.2f}%). RS-1 = contorno - bath = {R} vs cargado {ld} ({(R-ld)/ld*100:+.2f}%): el cargado (443 - 109.36) es correcto en definición; difiere sólo la caja del bath (medida {B} vs 109.36 en source).",
     "402":f"Impreso 556 ~ contorno incl. bath ({C}, {ei:+.2f}%, apenas fuera de ±2 %; excl. bath daría {ee:+.1f}%) -> el impreso INCLUYE el bath. Diferencia 14 SF sin causa vectorial clara (nube de revisión 1 en el cuarto: posible SF impreso no actualizado). RS-1 = {R} vs cargado {ld} ({(R-ld)/ld*100:+.2f}%) -> el cargado es correcto.",
     "403":f"Impreso 521 EXCLUYE el bath (contorno - bath {C-B:.2f} vs 521, {ee:+.2f}%; contorno {C} = +{ei:.1f}%). El cargado {ld} = 521 - 94.81 RESTA EL BATH DOS VECES: RS-1 real = {R} ({(R-ld)/ld*100:+.1f}% vs cargado, +{R-ld:.1f} SF).",
     "404":f"Impreso 317 EXCLUYE el bath (contorno - bath {C-B:.2f} vs 317, {ee:+.2f}%; contorno {C} = +{ei:.1f}%). El cargado {ld} = 317 - 100.14 RESTA EL BATH DOS VECES: RS-1 real = {R} ({(R-ld)/ld*100:+.1f}% vs cargado, +{R-ld:.1f} SF).",
     "405":f"Contorno (sin franja chase ni shaft) {C} no cuadra con 427 ({ei:+.1f}%) ni con 427 excl. bath ({ee:+.1f}%). Contorno + franja chase 27.91 = {C+27.91:.2f} ({(C+27.91-427)/427*100:+.1f}%); + shaft 8/A9.03 (~14 SF, 718.56-745.92 x ~415-457) = ~{C+27.91+13.6:.0f} (~-0.3%) -> el impreso 427 incluye bath + franja chase + shaft. RS-1 = contorno - bath = {R} vs cargado {ld} ({(R-ld)/ld*100:+.1f}%); si la franja chase NO interrumpe el RS-1: {R+27.91:.2f}. Causa: el cargado parte del impreso (que incluye chase+shaft) y resta un bath de 85.49.",
    }[k]
    out[nm]=dict(sheet="A2.04",polygon=[list(p) for p in RS[k]],area_sf=R,contorno_sf=C,contorno_polygon=[list(p) for p in u['c']],bath=[list(p) for p in u['b']],bath_sf=B,
        contorno_menos_bath_sf=R,sf_cargado=ld,sf_impreso=imp,cuadra_con=cq,err_pct=round(err,2),err_vs_cargado_pct=round((R-ld)/ld*100,2),
        metodo=met[k],nhoja="1/A2.04",img=IMG+"L4L1_A204_unidades_401-406.png",nota=nota)
# 406
a=A(d['c406']); nm="L4 406 Cleaning"; ld=CL[nm]['area_sf']
out[nm]=dict(sheet="A2.04",polygon=d['c406'],area_sf=a,bath=None,bath_sf=0,contorno_menos_bath_sf=a,sf_cargado=ld,sf_impreso=124,cuadra_con="NO CUADRA",
   err_pct=round((a-124)/124*100,2),metodo="caras: N y=356.64 (XW.6.6-L4-04 int) / W x=745.92 (W.62-L4-08 + CH-L4-06 cara 406) / E x=852.72 (W.62-L4-01 cara 406) / S y=440.76 (W.62-L4-09, línea de puerta 406.1) y y=455.88 (cara N CMU ascensor servicio) entre x 745.92-793.2 (jamba W.62-L4-10)",
   nhoja="1/A2.04",img=IMG+"L4L1_A204_unidades_401-406.png",
   nota=f"El polígono actual (rcp_polys) cae fuera del edificio; el bueno es este, dentro del cuarto 406 (entre baño 405/shaft 8/A9.03 y la unidad 401, al N del ascensor de servicio). Medido {a} vs impreso 124 ({(a-124)/124*100:+.1f}%): con el nicho de la puerta 406.1 (799-831 x 440.8-446.8, +2.4 SF) = {a+2.36:.1f} (-1.7%). No se fuerza; el cargado 124 queda ~4 SF alto.")
# escaleras
for nm,P,ref,img in [("L4 Lobby stair (top floor, under roof; roof hatch + alternating tread device)",d['st1'],"7/A6.01","L4L1_A204_lobby_stair.png"),("L4 SE stair 413 (top floor, under roof)",d['st413'],"4/A6.02","L4L1_A204_SE_stair_413.png")]:
    a=A(P); ld=CL[nm]['area_sf']; w=(P[1][0]-P[0][0])/9; h=(P[2][1]-P[1][1])/9
    out[nm]=dict(sheet="A2.04",polygon=P,area_sf=a,bath=None,bath_sf=0,contorno_menos_bath_sf=a,sf_cargado=ld,sf_impreso=None,cuadra_con="cargado",err_pct=round((a-ld)/ld*100,2),
      metodo=f"caras interiores del CMU FW.2 en A2.04: x {P[0][0]}-{P[1][0]} ({w:.3f} ft) / y {P[0][1]}-{P[2][1]} ({h:.3f} ft)",nhoja="1/A2.04 (cotas "+ref+")",img=IMG+img,
      nota=f"Contorno medido = caja interior del CMU {w:.3f} x {h:.3f} ft vs cotas impresas {ref} 8'-8 3/4\" x 17'-4 3/4\" (8.729 x 17.396) -> coincide; el cargado {ld} es correcto.")
# 412
cor=d['cor']; i=cor.index([801.84,1138.32])
corr=cor[:i+1]+[[709.92,1138.32],[709.92,1075.32],[755.28,1075.32],[755.28,1098.48],[799.2,1098.48]]+cor[i+2:]
C=A(corr); assert abs(C-(A(cor)+A(d['vrr'])))<0.05
nm="L4 412 Corridor (field ceiling)"; ld=CL[nm]['area_sf']; ws=94.7+39.9; F=round(C-ws,2)
out[nm]=dict(sheet="A2.04",polygon=corr,area_sf=F,contorno_sf=C,ws1_restado_sf=ws,bath=None,bath_sf=0,contorno_menos_bath_sf=C,sf_cargado=ld,sf_impreso=1350,cuadra_con="NO CUADRA",
   err_pct=round((C-1350)/1350*100,2),err_vs_cargado_pct=round((F-ld)/ld*100,2),
   metodo="caras: tramo N-S x 799.2 (CMU ascensores/escalera, W.62-L4-12/13) a 852.72 (W.62-L4-02/03/04), N y=446.76 (W.62-L4-09); vestíbulo 405.1/404.1 709.68-799.2 x 523.8-622.8 (nicho FEC 764.5-799.2 hasta 613.8); lobby ascensor 706.2-799.2 x 1007.64-1070.28; vestíbulo baños 417.1/418.1 709.92-799.2 x 1075.32-1138.32 menos shaft 755.28-799.2 x <1098.48; tramo S y 1212.6 (W.62-L4-07) / 1221.84 (FW.4-L4-19) a 1271.04 (FI.6-L4-02), x 766.56 (puerta 419.1) a 1485.6 (CMU escalera 413); 801.84 = W.6.1",
   nhoja="1/A2.04",img=IMG+"L4L1_A204_412_corridor.png",
   nota=f"Contorno del corredor (con perímetro de cove en A3.04) = {C} vs impreso 1350 ({(C-1350)/1350*100:+.1f}%). Field = contorno - WS-1 134.6 (del source, no re-medido) = {F} vs cargado {ld} ({(F-ld)/ld*100:+.1f}%). Si se suma el vestíbulo entre F&B 410 y Deck Bar 411 (puertas 410.1/411.2; 1239.48-1297.44 x 1086-1212.6 = {A(d['v410'])} SF, naranja; en A3.04 tiene el punteado de F&B y el cove del corredor pasa por debajo, por eso lo excluyo) = {C+A(d['v410']):.2f} ({(C+A(d['v410'])-1350)/1350*100:+.1f}%). Ojo: la etiqueta 'CORRIDOR 412 1350 SF' está impresa dentro del sector NW de F&B 410 (858-1005 x 974-1209), que NO es corredor (F&B 410 ~1005 SF ≈ 990 impreso). No se fuerza: el 1350 impreso no se reproduce con caras; el cargado 1215.4 queda ~{ld-F:.0f} SF alto.")
# L1
inn=l['inn']; I=A(inn); s1=A(l['st1']); s2=A(l['st2']); hs=A(l['hs']); hl=A(l['hl']); N=round(I-s1-s2,2); O=A(l['out'])
nm="L1 FS-1 membrane under the LEVEL 2 floor (whole floor plate)"; ld=CL[nm]['area_sf']
T=lambda P:[[round(x+13.7,2),round(y+18.66,2)] for x,y in P]
out[nm]=dict(sheet="A2.02",polygon=inn,holes_restados={"lobby_stair":l['st1'],"SE_stair":l['st2']},area_sf=N,contorno_sf=I,escaleras_sf=[s1,s2],hoistways_sf={"service_elev":hs,"lobby_elev":hl},
   polygon_A3_01=T(inn),offset_A2_02_a_A3_01=[13.7,18.66],bath=None,bath_sf=0,contorno_menos_bath_sf=N,sf_cargado=ld,sf_impreso=8587,cuadra_con="cargado",err_pct=round((N-ld)/ld*100,2),
   metodo="caras interiores de los muros exteriores de L2 en A2.02: W x=536.88 (XW.6.3-L2-04), N y=353.64 (XW.6.3-L2-01) con jog 214 (628.32 / 398.64), E x=1062.12 (XW.6.3-L2-05), muesca 204/205 y=941.76 / x=1010.76, N ala sur y=1001.16 (XW.6.3-L2-07), E x=1758.24 (XW.6.3-L2-08), jog SE 1684.8 / 1226.4, S y=1271.04 (FI.6 / XW.6.3-L2-11). Escaleras = caja interior CMU (712.56-791.16 x 630.12-786.6; 1491.36-1647.84 x 1192.32-1270.8). Hoistways = caja interior CMU (723.6-791.16 x 462.72-514.44; 712.56-789.0 x 930.96-998.76).",
   nhoja="1/A2.02 (transportado a 1/A3.01 con +13.7/+18.66: A2.02->A2.01 dy +9.96 verificado en las 2 escaleras, A2.01->A3.01 offset L1 13.7/8.7)",
   img=IMG+"L4L1_A202_L1_FS1_placa.png",img_A3_01=IMG+"L4L1_A301_L1_FS1_placa.png",
   nota=f"Contorno interior {I} - 2 escaleras ({s1}+{s2}) = {N} vs cargado {ld} ({(N-ld)/ld*100:+.2f}%). Control: contorno EXTERIOR de L2 = {O} vs A0.01 8,587 gross ({(O-8587)/8587*100:+.2f}%) -> la placa está bien; la diferencia viene de la banda de muro: medida {O-I:.1f} SF (perímetro ext. 497 LF, espesor ~0.86 ft) vs 354.5 supuesta (472.7 LF x 0.75). Mezzanine 219 (460.7 SF int.) NO incluido (no está en el 8,587). Hoistways no restados: {hs} + {hl} = {hs+hl:.2f} SF (neto sin ellos {N-hs-hl:.2f}). Además, sobre A3.01 el ala sur de L2 vuela ~8'-2\" al E del muro exterior de L1 (x 1682.76-1758.24 x 1001.16-1226.4 en A2.02 = {75.48*225.24/81:.1f} SF sobre exterior/cubierta, no sobre cielo interior de L1); si FS-1 se limita al interior de L1: {N-75.48*225.24/81:.1f}. Los muros exteriores de L1 (CMU) son más gruesos que los de L2, por lo que el cielo interior de L1 bajo la placa es algo menor aún.")
json.dump(out,open('contornos_L4L1.json','w'),indent=1,ensure_ascii=False)
for k,v in out.items(): print(f"{k[:40]:40} | {v['area_sf']:8} | {v['sf_cargado']:7} | {v['sf_impreso']} | {v['cuadra_con']} | {v['err_pct']} | vs carg {v.get('err_vs_cargado_pct')}")
