import json
f='/root/cr/work/etapas/4_canon/rev9/contornos_L2L3.json'; d=json.load(open(f))
N={
'L2 Guest room 203 (Type 1)':"NO CUADRA: misma geometría que 202/204 (impresos 269) y 303 (impreso 269); contorno-bath 266.6 vs 255 impreso (+4.5 %). El 255 impreso de 203 parece inconsistente (no es error de medición). Cargado 255 = impreso.",
'L2 Guest room 207 (Type 2)':"NO CUADRA por poco: contorno 342.91 vs impreso 334 (+2.7 %, incl. bath). Si el borde S del bath se toma en el furring de plomería 1201.44 (en vez de la cara del muro del corridor 1206.0) queda 338.1 (+1.2 %). 206 tiene la misma caja y su impreso (259) excluye el bath.",
'L3 Guest room 307':"Igual que 207: contorno 342.97 vs impreso 334 (+2.7 %); con furring 1201.44 en el bath ~338.1 (+1.2 %).",
'L2 Guest room 211 (Type 8)':"Impreso 403 incluye el bath (+1.9 %); en L3 el mismo cuarto (311) imprime 279 = excl. bath. Tool: bath 154 SF (incluía closet) y lazo en el chase; corregido.",
'L3 Guest room 311':"Mismo contorno que 211; aquí el impreso (279) excluye el bath.",
'L2 Guest room 212 (Type 7)':"Impreso incl. bath (L2); en L3 312 el impreso excluye el bath.",
'L2 Guest room 213 (Type 6)':"Impreso incl. bath (L2); en L3 313 excl. bath (bath sin el closet 213.1).",
'L2 Guest room 214 (Type 13)':"El tool (393.8) dejaba fuera la franja NW 536.88-625.32 x 398.64-427.2 (achurada FS-1 en 1/A3.02); con ella 423.36 cuadra con el impreso 427 incl. bath.",
'L3 Guest room 314':"Igual que 214 (franja NW incluida, shaft restado).",
'L2 Guest room 209 (Type 4)':"Falla del flood: medido a mano. Bath = bath + shower (L). Incluye el vestíbulo de entrada 1594.08-1655.4 x 1144.56-1185.0 (el canon de 218 lo metía en el corridor hasta 1620.8).",
'L3 Guest room 309':"Igual que 209; en A2.03 el fondo del shower es 1276.56.",
'L2 Guest room 210 (Type 9)':"Falla del flood: medido a mano.",
'L2 Guest room 205 (Type 5)':"Tool tenía muesca 970-1005 en 1201.4 (furring tras el WC): borde S llevado a la cara del muro del corridor 1206.0.",
'L2 Guest room 204 (Type 1)':"Tool tenía muesca a 938.8; la cara S es continua en 935.76.",
'L3 Guest room 301':"Contorno completo 363.66 SF. El cargado (181.38) = impreso 296 - 114.62 SF bajo la terraza L4 (RS-6, fila RS6-L3); esa resta NO la decido aquí: la franja RS-6 ocupa el lado E del cuarto.",
'L3 Guest room 302':"Contorno completo 334.18. Cargado 165.45 = impreso 270 - 104.55 bajo la terraza L4 (RS-6); resta no decidida aquí.",
'L3 Guest room 303':"Contorno completo 333.14. Cargado 164.84 = impreso 269 - 104.16 bajo la terraza L4 (RS-6); resta no decidida aquí.",
'L3 Guest room 304':"Contorno completo 333.44. Cargado 164.84 = impreso 269 - 104.16 bajo la terraza L4 (RS-6); resta no decidida aquí.",
'L2 Corridor 216':"Membrana FS-1 del corridor N (caras de muros) hasta la línea de smoke curtain (no hay muro): 457.66 vs 455 impreso/cargado (+0.6 %). El GYP-1 colgado es otro renglón (CLG-L2-56: 360.2 = 455 - WS-1 94.8).",
'L3 Corridor 316':"Igual que 216: 458.21 vs 455 (+0.7 %). GYP-1 en CLG-L3-87 (360.2).",
'L2 Lobby 217':"Límite E abierto al corridor: tomado en 799.2 (cara de muros del corridor). Con la cara W del muro del elevador 797.52 daría 66.4 (= impreso). +2.6 % es solo por dónde se corta.",
'L3 Lobby 317':"NO CUADRA: lobby (68.4) + vestíbulo de 310/311 (56.6) = 124.98 vs 132 impreso (-5.3 %); el impreso parece bruto (incluye el muro 1069.68-1075.32 entre ambos y/o el shaft). En L2 ese vestíbulo no está en 217 (lo puse en 218).",
'L2 Corridor 218':"NO CUADRA (+243 SF): el polígono del canon (565.3) omite el tramo N-S 799.2-852.72 x 979.5-1212 (153.6 SF, entre el smoke curtain de 216 y el corridor E-W), el tramo 799.2-858.7 x 1212-1271 (43.4), y el vestíbulo de entrada a 210/211 (56.75, sin etiqueta en A2.02); y su ramal E llega a 1620.8 cuando la puerta 209.1 está en 1589 (sobra ~15.9). Sin tramo N-S ni vestíbulo: 598.0 SF. Total circulación L2 medida 216+217+218 = 1333.8 vs cargado 1086.3.",
'L3 Corridor 318':"NO CUADRA (+137 SF): el canon (614.5) omite el tramo N-S 799.08-852.72 x 979.5-1212 (153.97) y lleva el ramal hasta 1650 (dentro del vestíbulo de 309, ~31 SF). Sin el tramo N-S: 597.9 SF. Vestíbulo de 310/311 asignado a 317.",
'L2 Elec 221':"NO CUADRA (-6.4 %): el canon usó N 1144.2 (cara exterior del muro); la cara interior es 1147.8. Medido 5.62.",
'L3 ELEC 321':"NO CUADRA (-40 %): el canon ((799-785)x(1203-1147)=9.7) incluye el muro del corridor 793.56-799; cara a cara 784.92-793.56 x 1147.8-1202.76 = 5.86.",
'L2 Cleaning 215':"Falla del flood: medido a mano.",
'L2 Linen 222':"Confirma la operación del canon.", 'L2 Cleaning 223':"Confirma la operación del canon.",
'L3 322 Linen':"Confirma la operación del canon.", 'L3 323 Cleaning':"Confirma la operación del canon.",
}
for k,v in d.items():
    if k in N: v['nota']=N[k]
    if v['nota']=='' and v['cuadra_con'].startswith('impreso excl'): v['nota']="Contorno completo (FS-1 sobre el bath); el impreso excluye la caja del bath."
json.dump(d,open(f,'w'),indent=1,ensure_ascii=False)
print(len(d)); 
s=sum(d[k]['area_sf'] for k in ('L2 Corridor 216','L2 Lobby 217','L2 Corridor 218')); print(round(s,2))
