# RESUMEN rev19 FINAL — CR City Hotel (Castle Rock, CO)

rev19 FINAL reemplaza a rev18 / rev18b. Origen: auditoría adversarial de COORDINACIÓN del 11-nov (U-138) y las reglas U-175 / U-176 (REGLA DE ORO #2, alturas), U-177 y U-165 / U-168.

| # | Punto de la auditoría | Qué quedó | Delta |
|---|---|---|---|
| 1 | La entrega vigente no tenía compuerta (ENTREGA_OK de rev18 validaba el PDF viejo) | Compuerta completa del skill vigente sobre rev19 (todas las compuertas: CE_USO_REAL, CE_ALTURAS_3LADOS, CE_ALTURAS_EXTREMO, CE_CHECKLIST_USUARIO, CE_A1 / A2, CE_CITA_ALTURA, CB_U_174, /NM únicos) | — |
| 1b | Alturas U-175 / U-176 | Dos lecturas ciegas H-A / H-B (907 walls, cuartos) sin ver el Excel; 377 diferencias resueltas con recorte (Auditoria/ALTURAS_AB_RESOLUCION.csv); 198 walls cambian de altura (ver abajo); comparación a 3 lados Bluebeam = Excel = impreso; ALTURAS_REVISADAS.pdf; capa HEIGHTS en el PDF de Bluebeam; CHECKLIST B2 con N/N y muestra al azar | ver tabla |
| 2 | CE_RCP_CONTORNO pasaba con un polígono a 0.0 | Era el EXCLUDED de la caja de equipo exterior (1/A3.01, no dibujada en el RCP). Ahora < 0.5 = FAIL siempre; cada polígono con borde no dibujado declara la hoja que sí lo dibuja ('source A2.0x offset (dx, dy)') y ahí coincide (caja, terrazas, chases 214C / 314C: 1.0) | 0 |
| 3 | Demising DW.4 bajo la zona somera de 4/A5.05 (9'-10 3/4") | Medido a escala (27 pt/ft): la zona somera es la tira de 6.70 ft de FJ-2 (9 1/2" TJI) bajo el corredor sur 218 / 318 (S1.03 / S1.04). Ningún DW.4 queda bajo ella: todos bajo trusses FT-1 de 18" -> se quedan en 9'-2 7/8" | 0 |
| 3b | (hallazgo de las lecturas) | Lo contrario sí pasaba: 40 caras interiores de muros exteriores estaban a 9'-10 3/4" -> 9'-2 7/8" | menos SF |
| 4 | Detalles destino 14/A8.02, 1/A9.06, 12/A9.05 | Existen: 14/A8.02 'SECTION DETAIL - SLIDING SILL AT RESTAURANT', 1/A9.06 'ROOF DETAIL - EQUIPMENT SCREEN', 12/A9.05 'ROOF DETAIL - PARAPET CAP AT SOUTH FACADE CMU/ADJACENT' | 0 |

## Auditoría independiente de fondo (U-181) y correcciones aplicadas en rev19

| # | Hallazgo (revisor independiente) | Qué quedó | Delta |
|---|---|---|---|
| A1 | East facade L4 cargado a 14'-0" (1/A5.00 es el storefront del Deck Bar 411, no las caras de 401 / 402) | XW.6.6-L4-12 B / 13 C / 14 B / 15 B = eave de 1/A5.06 (9.844), 1/A4.05 corta 401 bajo el eave 04/A9.05; XW.6.6-L4-17 A = 3/A5.07 (10.25) | vuelve al valor del eave |
| A2 | 6 demising DW.4 con la cara de baño en Type X | A0.06 GN 11 'WATER-RESISTANT GYPSUM BOARD FOR WALLS IN ALL TOILET ROOMS': 51.57 LF de cara de baño en Type X W.R. (largo medido con las bath partitions) | ~476.5 SF de X a X W.R. |
| A3 | 29 renglones de corredor a 9'-10 5/8" | 9'-10 3/4" impreso en 4/A5.05 (U-146, la mayor) | ~+11 SF |
| A4 | Nombres del Material Summary sin tamaño / gauge, o con una base no impresa | carrying channel 0.0538 in (16 ga) 09 22 16 2.2.D; hanger wire 0.162 in 2.2.C; RC 1/2" 2.2.E.4; soffit studs / track 25 ga min. (A0.06 partition STUD SCHEDULE aplicado; soffit framing no dibujado) | 0 |
| A5 | F&B 410 / 411 caras del lado tenant | Las 6 caras son de types RATED (U-159): se quedan cargadas; línea en la Scope Checklist | 0 |
| A6 | CBU en baños | No es doble conteo (rated: capa extra sobre UL; non-rated: reemplaza) | 0 |

Totales del Material Summary = suma de renglones; 931 filas SF = LF x H x caras x capas; ~40 alturas y 10 largos verificados contra el plano por el revisor.

## Alturas que cambian (198 walls)

| Grupo | Antes | rev19 | Walls | Fuente |
|---|---|---|---|---|
| Caras interiores de muros exteriores L2 / L3 | 9'-10 3/4" | 9'-2 7/8" | 40 | 4/A5.05; la zona somera es solo el corredor sur (S1.03 / S1.04 FJ-2) |
| L1 bajo la membrana FS-1 | 12'-0" | 12'-0 3/4" | 37 | A3.01 / A7.31 GYP-1 '12'-0 3/4"' (el 12'-0" B.O. DECK de 5/A5.04 es solo la zona de metal deck en el fire wall) |
| Muros rated de L4 (a la cara inferior del roof sheathing, 2/A0.10) | 8'-11 1/4" + estructura | + 1 1/8" | 54 | 1/A5.06: 8'-11 1/4" es la línea del cielo; RC 1/2" + board 5/8" hasta la estructura (H-B midió 10.533) |
| Furrings FW.2 / FW.4 / FI.6 en corredor y baños | 9'-5" / 9'-0" | 9'-10 3/4" / 9'-2 7/8" | 32 | A0.06 head: board a la LINE OF STRUCTURE |
| Caras exteriores de L4 (sheathing) | 10.24 | 9.844 | 16 | 1/A5.06 a la cara exterior en el alero |
| Shafts CH.6 de L1 | 12'-0" | 14'-0" | 9 | 1/A5.08 'SHAFT WALLS CONTINUOUS TO UNDERSIDE OF ROOF SHEATHING' |
| Otros (stair SE interior, corredor, low roof, bandas 2 HR) | — | — | 10 | ver ALTURAS_AB_RESOLUCION.csv |

## Delta rev18 → rev19 (NET)

| Material | Unit | rev18 | rev19 | Delta |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 87,943.77 | 87,140.05 | −803.72 |
| 5/8" gypsum board, Type X W.R. | SF | 28,169.25 | 28,498.16 | +328.91 |
| 1" gypsum shaftliner panel, Type X | SF | 1,388.71 | 1,416.91 | +28.20 |
| 5/8" exterior gypsum sheathing, Type X | SF | 18,252.71 | 18,184.98 | −67.73 |
| C-H stud 6" 20 GA | LF | 763.13 | 796.63 | +33.50 |
| C-H stud 2-1/2" 20 GA | LF | 806.13 | 807.44 | +1.31 |
| Joint compound, all purpose | LB | 8,510.18 | 8,476.00 | −34.18 |
| Joint tape, paper | LF | 50,970.34 | 50,794.66 | −175.68 |
| Soffit studs / track, carrying channel, hanger wire, RC, metal trim | — | — | — | 0 (renombrados con tamaño + gauge y su sección de spec, U-177 / U-181) |

Ver Auditoria/DELTA_rev18_rev19.md (generado por programa).
