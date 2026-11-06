# INFORME DE AUDITORÍA ADVERSARIAL U-138 #2 — CR City Hotel rev2 (415 Perry St, Castle Rock CO)

Soy un auditor independiente y no participé en el take-off. Trabajé en modo solo lectura: escribí únicamente en `/root/cr/work/auditoria_U138_2/` (informe, `img/` y `tools/`). No modifiqué el canon, el Excel, los scripts ni los planos.

**Versión auditada:**
- Canon: `etapas/4_canon/takeoff_canon.json`, con 804 `existing_walls`, 52 ceilings y 363 misc.
- Excel: `etapas/8_excel/CR_City_Hotel_Takeoff_FINAL_rev2.xlsx`, 6 hojas.

**Convenciones:**
- Índices de página del PDF en base 0: A2.01..A2.04 = 16..19, A5.05 = 36, A7.03 = 46, A9.03 = 82, S1.02 = 89.
- Escalas: 1/8" = 9 pt/ft; las ampliadas A7.xx a 1/4" = 18 pt/ft.
- Toda medida sale de las líneas vectoriales leídas con pymupdf (`tools/vec.py`, `measure.py`, `showers.py`, `cbu_check.py`, `shower_cov.py`, `shower_missing.py`, `cbu_excess.py`). No hay ninguna medida a ojo.
- Etiquetas: [CONFIRMADO] = cota impresa con su N/HOJA; [DERIVADO] = lleva la operación; [PENDIENTE] = no está dimensionado.
- No mezclo pisos en ninguna cifra.

**Cómo detecté los showers.** Cada shower de guest bath está dibujado con 2 diagonales que salen de las esquinas del muro de cabecera y convergen hacia el drain. El script `showers.py` las detecta en A2.02 (13 showers), A2.03 (12) y A2.04 (4). Con eso obtengo la caja del shower: cabecera de 2.9–3.0 ft y largo de 5.0–7.7 ft [DERIVADO de los vectores]. No detecta los showers de formato distinto: 211, 308, 311 y 402. Esos 4 quedan fuera de los conteos automáticos, así que en F2 los conteos son un mínimo.

---

## 1. Tabla de hallazgos (de más a menos grave)

| # | Sev. | Qué | Evidencia N/HOJA + imagen | Delta estimado | Acción |
|---|---|---|---|---|---|
| F1 | **ALTA** | **Cement board cargado en caras enteras de muro, no solo en el shower (L2 y L4).** Ejemplos: demising DW.4 de 23.52 LF con CBU completo cuando el shower ocupa 2.9–3.0 ft; corridor wall W.62-L2-08 A con 63.82 LF de CBU cuando los showers suman 21.81 ft; muro este de los baños Type 1 201-204 con CBU completo (9.4–9.9 LF) cuando el shower ocupa 3.0 ft. El propio canon (RFI-11, nota 6/A7.02) y las elevaciones A7.03 8/9 dicen que el TILE-1 va **solo en el shower** y fuera hay TF-1 + 4" base. En L3 el mismo stack está bien acotado, lo que demuestra la inconsistencia entre pisos. | A2.02 / A2.04 vectores; A7.03 elev. 8 y 9. `img/F1_L2_205_208_CBU_vs_shower.png`, `img/F1_L2_201_204_CBU_vs_shower.png`, `img/F1_L4_401_405_CBU_vs_shower.png`, `img/A703_elev8_9_tile_shower_only.png` | [DERIVADO, LF sobrante × altura cargada] **L2 −202.01 LF / −1,818.1 SF** de CBU; **L3 −9.83 LF / −88.5 SF** (FW.2-L3-10 A y NULL-L3-07b A); **L4 −72.19 LF / −645.2 SF**. Total **−2,551.8 SF de CBU (≈ −57 sheets 4×12 con 6 % de waste)** | Recortar cada cara de CBU a la proyección del shower medida en vectores: cabecera más paredes laterales (tabla en §2-F1). Mantener W.R. en el resto del baño y Type X en el dormitorio. |
| F2 | **ALTA** | **Faltan caras de CBU en showers (sobre todo en L3).** En los showers detectados hay paredes sólidas (cabecera, back wall o laterales) sin cement board. En L3: 305, 306 y 307 no tienen CBU en el back wall del corridor ni en el demising; 301-304 no lo tienen en la cabecera este de 3.0 ft; 302-304 no lo tienen en el back wall de 6.02 ft; tampoco hay CBU en 310 (extremos N/S), 312, 313 y 309. En L2 faltan, entre otros, el back wall de 213 (DW.4-L2-01, solo Type X), el lado E de 212 y los extremos N/S de 210. | A2.03 / A2.02 vectores. `img/F2_L3_305_308_CBU_faltante.png`, `img/F2_L3_301_304_CBU_faltante.png`, `img/L3_310_canon.png`, `img/F6_L2_213_CBU_mas_WR.png` | [DERIVADO, mínimo: excluyo el lado largo con menos CBU, que tomo como el lado de vidrio] **L3 +71.87 LF / +646.8 SF**; **L2 +25.56 LF / +230.1 SF**; **L4 +3.00 LF / +26.8 SF**. Sin contar 211, 308, 311 y 402 [PENDIENTE] | Cargar las 3 paredes sólidas de cada shower en todos los pisos, con la misma regla. Neto F1+F2: L2 −1,588 SF, L3 +558 SF, L4 −618 SF de CBU. |
| F3 | **ALTA** | **Los shafts 2-HR no se cargan en L3 ni en L4.** El shaft sur (7/A9.03) y el norte (8/A9.03) se cargan en L2 como CH.6-2 (shaftliner + 2 layers + C-H + J-runner). En L3 la misma caja figura como "small shaft box" W.4-0 de 1 layer (NULL-L3-11..14, RFI-09) y el shaft norte solo tiene FW.4 de 1 cara (NULL-L3-15). En L4 el shaft norte solo tiene FW.4-L4-04 W.R. de 1 cara. 7/A9.03 imprime "2-HOUR SHAFTWALL ASSEMBLY (W419, U497) MAX. HEIGHT 54'-0"", es decir, un shaft continuo. Esto también cierra RFI-09: el plano sí resuelve. | A9.03 7 y 8; A2.02 / A2.03 / A2.04. `img/F3_L3_shafts.png`, `img/F3_L2_shafts_ref.png`, `img/F3_L4_north_shaft.png`, `img/F13_A903_shaftwall.png` | [DERIVADO del L2 cargado, tramo por tramo] L3: **+270.2 SF de 1" shaftliner**, **+540.3 SF de 5/8" Type X/W.R.** (menos 181.9 SF de W.4 / FW.4 ya cargados), **+253 LF de C-H stud 6"**, **+49.1 LF de J-runner**. L4 norte (altura 8.9375): **+104.0 SF de shaftliner**, **+208.1 SF de board**, **+98.3 LF de C-H**, **+23.3 LF de J-runner** [PENDIENTE: confirmar la cabeza de shaft en 10/A9.03] | Cargar CH.6-2 en los shafts N y S de L3 y en el N de L4, igual que en L2. Cerrar RFI-09. |
| F4 | MEDIA | **L3: la cara interior de los muros exteriores tiene una altura menor que la impresa.** El canon carga 9'-2 7/8" (zona de piso profunda de los cuartos). 4/A5.05 imprime en el muro exterior **9'-10 3/4" + 1'-1 1/4"** entre L2 y L3, y **8'-11" + 11 3/4"** entre L3 y L4. L2 usa bien 9.8958. | 4/A5.05 (idx 36). `img/A505_4_heights.png` | [DERIVADO 649.65 LF·layer × (9.8958 − 9.2396)] **+426.3 SF en L3** (+337.7 SF Type X, +88.6 SF W.R.) | Subir las caras interiores XW de L3 a 9'-10 3/4" [CONFIRMADO 4/A5.05]. |
| F5 | MEDIA | **La altura del exterior gyp sheathing difiere entre L2 y L3.** El mismo stack se carga a 9.8958 en L2 y a 11'-0" en L3 ("sheathing continuous floor to floor"). Una de las dos está mal. | 4/A5.05; canon XW.6.3-L2-01/04/07 A vs XW.6.3-L3-01/04/08 A. `img/A505_4_heights.png` | [DERIVADO 620.92 LF·layer × (11.0 − 9.8958)] **+685.6 SF de sheathing en L2** si el criterio de L3 es el correcto; −654 SF en L3 si no | Unificar el criterio. El sheathing pasa por delante del rim, así que recomiendo 11'-0" en L2. |
| F6 | MEDIA | **Doble capa W.R. + CBU en muros NO rated, contra lo que dice el propio RFI-11.** RFI-11 dice "non-rated: cement board in place of board". Sin embargo, en W.4-0, W.6-0, FW.2/4/6-0 y XW.6.6-0 la cara del shower lleva CBU (9'-0") **y** W.R. a altura completa sobre la misma cara. Ejemplos: W.4-L2-03 A CBU + B W.R. en 2 caras (shower; toilet) y W.4-L2-08 A + C. | Canon RFI-11 (texto `loaded`); A0.06 GN 13. `img/F6_L2_213_CBU_mas_WR.png` | [DERIVADO Σ LF de CBU no rated, ya recortado por F1, × altura] **−738.9 SF W.R. en L2, −647.7 en L3, −336.1 en L4 = −1,722.8 SF de W.R.** Se mantiene la franja de 0.24 ft sobre el CBU | Aplicar la regla tal como está escrita. Solo los tipos rated (W.62-1, DW.4-1, XW-2) conservan W.R. detrás del CBU. |
| F7 | BAJA | **W.R. y Type X asignados por cara entera en los demising.** En L2, DW.4-L2-07/08/09 C llevan W.R. también en el tramo del dormitorio (13.69 ft) y la cara opuesta (baño 206/207) lleva Type X en el baño. En L3, DW.4-L3-09/10 llevan W.R. en las 2 caras completas. En DW.4-L2-01, la cara de 213 (baño) lleva solo Type X. | A2.02 / A2.03. `img/F7_L3_DW4_WR_2caras.png`, `img/F1_L2_205_208_CBU_vs_shower.png` | ≈ **873 SF** pasan de W.R. a Type X. Por cara: dormitorio 13.69 ft y baño 8.67 ft × 9.24 [DERIVADO]. Cantidad neta ≈ 0; afecta el precio | Partir cada cara en tres tramos (dormitorio / baño / shower), como ya se hizo en W.62-L2-01 y XW.6.3-L2-01. |
| F8 | BAJA | **Los demising DW.4 de L2 se miden a ejes y no a caras.** DW.4-L2-07/08/09 van de 997.35 a 1209.03 = 23.52 ft; las caras van de 1001.16 a 1206.0 = 22.76 ft. En L3 el mismo muro se carga con 22.78 ft. | A2.02 vectores. `img/chk_DW.4-L2-08_A.png` | [DERIVADO 0.76 ft × (9.0 + 9.24 + 9.24) × 3 muros] **≈ −63 SF** en L2 | Medir a caras en las T, como en L3. |
| F9 | BAJA | **XW.6.2-L1-03 lleva 2 caras de Type X interior: Retail 124 y el lado exterior.** El tipo es XW.6.2-0 (no rated). RFI-05, ya cerrado, excluye las caras no rated del retail. El lado exterior de la fila A0.07 es sheathing / brick, no Type X interior. | A2.01 (idx 16); A0.07 XW.6.2-0. `img/XW62_L1_03_retail.png` | **−112 SF Type X** (cara retail, 9.33 × 12.0) y **112 SF pasan de Type X a exterior sheathing** [DERIVADO] | Aplicar RFI-05 y reclasificar la cara exterior. |
| F10 | BAJA | **RFI-20 (beam wraps del retail) se puede acotar con S1.02.** S1.02 imprime "18" PRE-ENGINEERED OPEN WEB WOOD TRUSSES" y vigas W16 a W30 [CONFIRMADO]. La cara expuesta es la peralte menos 18" (≈ 0"–12"). Lo cargado (2 × 1'-0") es el máximo. | S1.02 (idx 89). `img/F10_S102_trusses.png` | Alternativa de 6": **−154 SF Type C** (ya listada en el RFI) | Leer los perfiles de las vigas del retail en S1.02 y fijar las caras por viga. Cerrar o acotar RFI-20. |
| F11 | BAJA | **RFI-21 (canopy de entrada): S1.02 marca "PRE-FABRICATED ROOF CANOPY BY OTHERS" (HSS4x4 hangers, 3/S3.10).** Si es el mismo canopy de 08/A9.05, sale del scope. | S1.02 / S3.10. `img/F11_S102_canopy.png` | **−58.2 SF** de exterior soffit board y **−21.7 LF** de trim, si es "by others" | Confirmarlo en el RFI. |
| F12 | BAJA | **Dos tramos de muestra con longitud de más.** FW.2-L4-11 corre de 706.2 a 765.24, pero la cara de CMU termina en 751.08: sobran 1.57 ft. W.62-L4-11 (11.86 LF) atraviesa 2 vanos de puerta (405.1 y 404.1), lo que la política "vanos no descontados" permite. | A2.04. `img/chk_FW.2-L4-11.png`, `img/chk_W.62-L4-11.png` | **−14.0 SF** (1.57 × 8.9375). Los vanos de W.62-L4-11 suman ≈ −214 SF si se descuentan (2 × 3 ft × 8.94 × 2 caras × 2 layers, [PENDIENTE] ancho de puerta de A8.00) | Corregir FW.2-L4-11. Decidir si los vanos grandes se descuentan. |
| F13 | BAJA | **Cita UL de los shafts.** El canon / RFI-07 cita UL U415 (fila CH de A0.06); 7/A9.03 imprime "W419, U497". | A9.03 (idx 82). `img/F13_A903_shaftwall.png` | 0 SF (cita) | Citar los dos y anotarlo en RFI-07. |

**Impacto en el Material Summary si se aplican F1 a F9 (orden de magnitud):**

| Material | Delta | Origen |
|---|---|---|
| Cement board | ≈ −1,648 SF (≈ −35 sheets) | F1 + F2 |
| Type X W.R. | ≈ −2,500 SF | F6 + F7 |
| Type X | ≈ +1,300 SF | F3, F4, F7 |
| Shaftliner | +374 SF | F3 |
| Exterior sheathing | +686 SF | F5 |
| C-H stud | +351 LF | F3 |
| J-runner | +72 LF | F3 |

---

## 2. Detalle por hallazgo

### F1 — CBU en caras enteras (ALTA)

**Regla impresa:**
- A0.06 GN 13: "USE CEMENTITIOUS BACKER UNITS ... AT PARTITIONS TO RECEIVE CERAMIC TILE".
- A7.03 elevaciones 8 y 9 (Unit Type 2): TILE-1 dentro del shower (3' en la elev. 9); TF-1 y "TILE-1 4" BASE" fuera. Ver `img/A703_elev8_9_tile_shower_only.png`.
- El script del canon (`finalizar_canon.py`, nota _N1) dice lo mismo: "TILE-1 at the shower only".

**Medición.** Para cada cara CBU calculé el solape con una sola arista de shower dentro de 9 pt (`tools/cbu_excess.py`). W.62-L2-08 A toca 4 showers, así que ahí uso la suma de las 4 aristas.

| Piso | Cara | LF canon | Shower (ft) | Sobra LF | SF |
|---|---|---|---|---|---|
| L2 | W.4-L2-08 A (212 sur) | 11.33 | 2.52 | 8.81 | 79.3 |
| L2 | W.4-L2-17 / 20 / 23 / 26 A (este 201-204) | 9.89 / 9.39 / 9.39 / 9.40 | 3.00 / 2.99 / 2.99 / 2.99 | 6.89 / 6.40 / 6.40 / 6.41 | 62.0 / 57.6 / 57.6 / 57.7 |
| L2 | W.62-L2-07 A (210 / elec 221) | 14.09 | 6.51 | 7.58 | 68.2 |
| L2 | W.62-L2-08 A (corridor 218: linen, cleaning, 205-208) | 63.82 | 21.81 | 42.01 | 378.1 |
| L2 | FW.2-L2-12 A (212 norte) | 9.58 | 2.92 | 6.66 | 59.9 |
| L2 | DW.4-L2-07 / 08 / 09 A | 23.52 c/u | 2.99 / 2.91 / 3.00 | 20.53 / 20.61 / 20.52 | 184.8 / 185.5 / 184.7 |
| L2 | DW.4-L2-10 A (208/209, sin shower en ese muro) | 16.03 | 0 | 16.03 | 144.3 |
| L2 | UNTYPED-L2-01 / 02 A (202/203, 203/204) | 22.60 c/u | 6.02 | 16.58 c/u | 149.2 c/u |
| L3 | FW.2-L3-10 A (312) | 10.00 | 3.00 | 7.00 | 63.0 |
| L3 | NULL-L3-07b A (307, tramo WC) | 2.83 | 0 | 2.83 | 25.5 |
| L4 | W.4-L4-03 A / DW.4-L4-04 A (401) | 16.13 c/u | 2.89 | 13.24 c/u | 118.4 c/u |
| L4 | DW.4-L4-01 A (404) | 18.20 | 6.52 | 11.68 | 104.4 |
| L4 | X-L4-03 A (402; shower medido 965.3–996.9) | 16.13 | 3.51 | 12.62 | 112.8 |
| L4 | XW.6.6-L4-03 A (405) | 12.07 | 2.99 | 9.08 | 81.2 |
| L4 | W.62-L4-08 A (405 + shaft 415–457) | 11.16 | 5.68 | 5.48 | 49.0 |
| L4 | FW.2-L4-08 A (403) | 9.84 | 2.99 | 6.85 | 61.2 |

**Totales:**
- L2: **−202.01 LF / −1,818.1 SF**
- L3: **−9.83 LF / −88.5 SF**
- L4: **−72.19 LF / −645.2 SF**

**Imágenes.** El CBU del canon va en azul y el shower real, circulado en rojo.

### F2 — Caras de shower sin CBU (ALTA)

`tools/shower_missing.py` busca, en cada shower detectado, las 3 paredes sólidas sin CBU. Considera lado de vidrio el lado largo con menos CBU, lo que favorece al canon. Detalle en `tools/shower_missing.txt`:

| Piso | Faltante (LF / SF) | Detalle |
|---|---|---|
| L3 | 71.87 LF / 646.8 SF | 313: 9.57 · 312: 8.00 · 310: 5.98 · 302 / 303 / 304: 7.50 / 7.50 / 7.48 · 301: 3.00 · 305: 8.58 · 306: 8.07 · 307: 2.93 · 309: 3.25 |
| L2 | 25.56 LF / 230.1 SF | 213: 6.54 · 212: 5.56 · 210: 5.98 · 204: 4.49 · 208: 3.00 |
| L4 | 3.00 LF / 26.8 SF | 403 extremo N |

Los showers 211, 308, 311 y 402 no se detectan con el script y quedan [PENDIENTE]. El mismo stack entre L2 y L3 tiene geometría idéntica (coordenadas iguales a ±0.1 pt), así que la diferencia de CBU entre pisos (L2 3,325.6 SF y L3 1,086.5 SF en el canon) es un error de carga, no de diseño.

### F3 — Shafts 2-HR en L3 y L4 (ALTA)

| Ubicación | L2 (canon) | L3 (canon) | L4 (canon) |
|---|---|---|---|
| Shaft sur 757–797 × 1073–1097 (7/A9.03) | CH-L2-01..04: shaftliner 142.1 SF + 2 layers Type X, C-H 132 LF, J 25.84 LF | NULL-L3-11..14: W.4-0, 1 layer exterior | CH.6-L4-01..04 en A7.50 ✓ |
| Shaft norte 720–747 × 417–456 (8/A9.03) | CH-L2-05..07: shaftliner 128.0 SF + 2 layers (W.R. lado 214), C-H 121 LF, J 23.28 LF | Solo NULL-L3-15 FW.4 (1 cara) | Solo FW.4-L4-04 W.R. (1 cara) |

**Evidencia:**
- 7/A9.03 "2-HOUR SHAFTWALL ASSEMBLY (W419, U497) MAX. HEIGHT - 54'-0"" (`img/F13_A903_shaftwall.png`).
- 10/A9.03 "HEAD OF SHAFT" y 11/A9.03 "BASE OF NORTH SHAFT": es un shaft continuo de L2 a la cubierta.

**Delta [DERIVADO a la misma altura de 11'-0" que L2]:**
- L3: shaftliner +270.2 SF; board +540.3 SF − 181.9 SF ya cargados = **+358.4 SF**; C-H **+253 LF**; J-runner **+49.1 LF**.
- L4 norte (altura 8.9375): shaftliner **+104.0 SF**, board **+208.1 SF** (menos el W.R. de FW.4-L4-04), C-H **+98.3 LF**, J-runner **+23.3 LF**. Queda [PENDIENTE] hasta verificar 10/A9.03.

**RFI-09** debe cerrarse con el plano: la caja es el shaft sur de 7/A9.03.

### F4 — Altura de la cara interior de los XW en L3 (MEDIA)

4/A5.05, junto al muro exterior (x ≈ 1132 pt de la hoja):
- Entre L2 y L3: "9' - 10 3/4"" + "1' - 1 1/4"" = 11'-0" [CONFIRMADO].
- Entre L3 y L4: "8' - 11"" + "11 3/4"" + "1' - 1 1/4"" = 11'-0", es decir, board a 9'-10 3/4" [DERIVADO].
- Hacia el interior (x ≈ 1458), "9' - 2 7/8"" + "1' - 9 1/8"" aplica a los cuartos, no al muro exterior.

El canon de L3 carga 20 caras interiores XW a 9.2396; L2 las carga a 9.8958. Delta **+426.3 SF** en L3 (`img/A505_4_heights.png`).

### F5 — Altura del exterior sheathing L2 vs L3 (MEDIA)

| Piso | Altura cargada | Fuente que cita el canon |
|---|---|---|
| L2 | 9.8958 (11 entradas, 620.92 LF·layer) | — |
| L3 | 11.0 | "A5.05 sect 4: exterior sheathing continuous floor to floor" |

El mismo detalle no puede dar dos alturas. Delta **±685.6 SF** en L2.

### F6 — W.R. detrás del CBU en muros no rated (MEDIA)

El campo `loaded` de RFI-11 dice: "rated faces: Type X W.R. layers kept + 1 layer 5/8" cement board added ...; **non-rated: cement board in place of board**". El canon no lo aplica: toda cara CBU no rated tiene su gemela W.R. sobre la misma cara (lista en `tools/cbu_list.txt`; ejemplo en `img/F6_L2_213_CBU_mas_WR.png`).

Delta [DERIVADO: Σ (LF CBU no rated − sobrante F1) × altura]: L2 −738.9, L3 −647.7, L4 −336.1 = **−1,722.8 SF de W.R.**

### F7 — Asignación W.R./X en los demising (BAJA)

Conteo de las caras de dormitorio mal clasificadas:
- L2: DW.4-L2-07..09 C, 3 × 13.69 × 9.24 = 379.5 SF.
- L2: DW.4-L2-10 C, completa = 148.1 SF.
- L3: DW.4-L3-09/10, 2 muros × 2 caras × 13.69 × 9.24 = 506 SF.

En sentido contrario, las caras de baño 206/207 (DW.4-L2-07/08 B), 2 × 8.67 × 9.24 = 160 SF, llevan Type X y deberían ser W.R. Neto ≈ 873 SF pasan de W.R. a Type X. Solo afecta el precio.

### F8 — DW.4-L2 medidos a ejes (BAJA)

Las caras del demising 206/207 en vectores van de 1001.16 a 1206.0 = **22.76 ft**; el canon carga 23.52. En L3 el mismo muro se mide 22.78. Delta ≈ −63 SF en L2.

### F9 — XW.6.2-L1-03 (BAJA)

Las 2 caras se cargan como "5/8 type X". La fila XW.6.2 | 0 de A0.07 es "EXTERIOR WOOD - BRICK FINISH - LVL 1 (NON-BEARING)", con Type X 5/8" en el interior y sheathing / brick en el exterior. RFI-05 (cerrado) excluye las caras no rated del Retail 124.

### F10 – F13 (BAJA)

Ver la tabla. Las imágenes son `F10_S102_trusses.png`, `F11_S102_canopy.png`, `chk_FW.2-L4-11.png`, `chk_W.62-L4-11.png` y `F13_A903_shaftwall.png`.

---

## 3. Lo que revisé y está correcto

### 3.1 Muros: muestra aleatoria

Muestra con semilla 138002, 10 por piso (`tools/sample.json`). La columna de vectores da la longitud de la línea de cara a 9 pt/ft (18 en A7.xx).

**L1:**

| Wall | Canon (ft) | Vectores | Resultado |
|---|---|---|---|
| FW.4-L1-05 | 7.66 | 7.65 | ✓ |
| CH.6-L1-02 | 2.01 | 2.01 / 2.13 | ✓ |
| FW.1-L1-03 | 8.15 | 8.15 | ✓ |
| W.6-L1-26 | 25.71 | Cara S con aberturas; T con el jamb 121.1 | ✓ (`img/chk_W.6-L1-26.png`) |
| FW.4-L1-06 | 7.88 | 7.88 | ✓ |
| W.6-L1-28 | 2.25 | 2.20 | ✓ |
| XW.6.4-L1-01 | 2.00 | 2.00 | ✓ |
| W.6-L1-27 | 0.83 | 0.83 | ✓ |
| XW.6.2-L1-03 | 9.33 | 9.33 | ✓ en longitud; caras en F9 |
| W.6-L1-14 | 9.13 | 7.05 / 13.39 (cara cortada por la puerta) | ✓ |

**L2:**

| Wall | Canon (ft) | Vectores | Resultado |
|---|---|---|---|
| XW.6.3-L2-04 | 97.36 | (1271.04 − 394.8)/9 = 97.36 | ✓ |
| UNTYPED-L2-14 | 3.03 | 3.03 | ✓ |
| W.4-L2-03 | 3.41 | 3.41 / 3.41 | ✓ |
| FW.4-L2-18 | 3.46 | 3.79 | ✓ (esquina L) |
| W.4-L2-35 | 9.07 | Líneas finas, revisado en imagen | ✓ |
| W.4-L2-18 | 6.87 | — | ✓ |
| W.4-L2-44 | 7.31 | 7.71 | ✓ (diferencia aceptable) |
| DW.4-L2-08 | 23.52 | 22.76 | ✗ (F8) |
| FW.2-L2-03 | 9.08 | 8.76 / 9.92 | ✓ |
| XW.6.4-L2-02 (type_id XW.6.6-1) | 19.43 | 18.63 / 20.24 | ✓ (eje) |

**L3:**

| Wall | Canon (ft) | Vectores | Resultado |
|---|---|---|---|
| W.4-L3-41 | 3.84 | 3.84 | ✓ |
| W.62-L3-04 | 6.28 | Puerta 315.1 | ✓ |
| FW.4-L3-02 | 2.92 | 3.28 | ✓ |
| FW.2-L3-04 | 10.00 | 9.91 | ✓ |
| FW.4-L3-19 | 3.33 | 3.40 | ✓ |
| FW.6-L3-01 | 15.63 | 16.0 | ✓ |
| FW.6-L3-02 | 6.67 | 6.67 | ✓ |
| W.4-L3-48 | 4.28 | 4.31 | ✓ |
| FW.4-L3-25 | 3.01 | 3.19 | ✓ |
| FW.4-L3-11 | 3.01 | 3.19 | ✓ |

**L4:**

| Wall | Canon (ft) | Vectores | Resultado |
|---|---|---|---|
| FW.4-L4-07 | 3.92 | 3.92 | ✓ |
| W.4-L4-21 | 2.13 | — | ✓ |
| XW.6.6-L4-10 | 13.03 | — | ✓ (ventana) |
| W.6-L4-04 | 5.12 | — | ✓; el resto del tramo está cargado como FW.4-L4-17 / CH.6-L4-02 (`img/chk_W.6-L4-04.png`) |
| FW.4-L4-13 | 5.87 | 5.87 | ✓ |
| W.62-L4-13 | 7.41 | 7.01 | ✓ |
| W.6-L4-06 | 5.68 | 5.68 | ✓ |
| FW.4-L4-11 | 2.83 | 2.84 | ✓ |
| W.62-L4-11 | 11.86 | — | ver F12 |
| FW.2-L4-11 | 6.56 | 4.99 | ✗ (F12) |

**Consistencia Excel–canon.** Las 804 filas del Partition Takeoff coinciden con el canon en LF, altura y SF, con 0 diferencias.

### 3.2 Alturas (fuente impresa)

| Altura | Aplica a | Fuente |
|---|---|---|
| 9'-2 7/8" | Cuartos L2 / L3 | [CONFIRMADO 4/A5.05] |
| 9'-10 5/8" | Cara corridor | [DERIVADO 11'-0" − 1'-1 3/8"]; "1' - 1 3/8" RATED ASSEMBLY" impreso en 7/A7.23 |
| 8'-11 1/4" | L4 | [CONFIRMADO 1/A5.06] |
| 12'-0" | L1 (A7.50) | B.O. DECK [CONFIRMADO 5/A5.04] |
| 11'-2 5/8" | L1 (A7.30) | B.O. DECK [CONFIRMADO A5.04 / 1/A5.08] |
| 9'-10 3/4" | Muros exteriores L2 | [CONFIRMADO 4/A5.05] |
| 9'-0" | CBU | [DERIVADO]: el bath ceiling 8'-6" está impreso en A7.00 / A7.05 / A7.09 / A7.13 / A7.16 (8'-6" + 6"), según el precedente de RFI-11 |
| 8.9375 | CBU en L4 | Limitado por la altura del muro |

Fallan: L3 muro exterior (F4) y la altura del sheathing (F5).

### 3.3 Baños revisados (por piso)

| Piso | Baños |
|---|---|
| L1 | Toilets 110, 111, 112, 113, 119 y Janitor 109: todas las caras húmedas en W.R. ✓. No hay tile de muro impreso: A7.30 solo marca tile floor y remite a interior design, que no está en el set [PENDIENTE] |
| L2 | 201 (corridor y exterior), 205, 206, 207, 208 (corridor), 212, 213, 214 (exterior norte, CBU ✓) |
| L3 | 301, 305, 306, 307 (corridor), 310, 313, 314 (exterior, CBU ✓) |
| L4 | 401 (fachada este, CBU ✓ en XW.6.6-L4-13), 403 (corridor, W.62-L4-13 CBU ✓), 405 (fachada norte) |

### 3.4 Cadenas de burbujas

| # | Cadena | Resultado |
|---|---|---|
| 1 | Corridor W.62 → 7/A7.23 | 1'-1 3/8" ✓ |
| 2 | L4 walls → 1/A5.06 | 8'-11 1/4" ✓ |
| 3 | Room walls → 4/A5.05 | ✓ en cuartos; muro exterior de L3 ✗ (F4) |
| 4 | Shafts → 7/A9.03 y 8/A9.03 | L2 ✓; L3 / L4 ✗ (F3); cita UL (F13) |
| 5 | Tile → A7.03 elev. 8 / 9 | Shower only; canon ✗ en L2 / L4 (F1) |
| 6 | XW.6.3-2 → A0.07 | "2 LAYERS - TYPE X 5/8" GYP BD" interior y 2 layers sheathing ✓ |
| 7 | L1 → 5/A5.04 | "12' - 0" B.O. DECK" ✓ |

### 3.5 RFIs

**Abiertos:**

| RFI | Veredicto |
|---|---|
| RFI-04 | Legítimo: sin tag |
| RFI-09 | **No legítimo**, el plano lo resuelve (F3) |
| RFI-13 | Legítimo: MB-1 sin stud size |
| RFI-15 | Legítimo: A0.08 RS-1 sin board |
| RFI-17 | Legítimo |
| RFI-20 | Acotable con S1.02 (F10) |
| RFI-21 | Revisar "by others" (F11) |

**Cerrados:**

| RFI | Veredicto |
|---|---|
| RFI-01, 03, 10, 12, 14, 16 | ✓ (reglas / precedentes documentados) |
| RFI-02 | ✓ |
| RFI-05 | ✓ en la regla, aplicación incompleta (F9) |
| RFI-07 | ✓ con la nota de F13 |
| RFI-08 | ✓ (mezzanine 219 medida en 2/A5.04 a 27 pt/ft) |
| RFI-11 | Regla correcta, aplicación contradictoria (F1, F2, F6) |
| RFI-18 | ✓ |
| RFI-19 | Cerrado por programa; no re-auditado |

La hoja Pending Items lista los mismos 7 RFIs abiertos que el canon ✓.

### 3.6 Material Summary: filas recalculadas desde el canon

| Fila | Canon recalculado | Excel |
|---|---|---|
| Type X | 83,889.41 (walls + 3,557.07 ceilings RS-1 + 9,299.17 misc) | 83,889.35 ✓ |
| Type X W.R. | 29,173.12 | 29,173.09 ✓ |
| Cement board | 5,652.60 | 5,652.58 ✓ |
| Type C | 19,316.11 ceilings + 399.46 BW = 19,715.57 | 19,715.57 ✓ |
| Exterior sheathing | — | 16,309.09 ✓ |
| Shaftliner | — | 943.15 ✓ |

Otros controles:
- Sheets: ROUNDUP(Net × 1.06 / 48) = 1,853 / 645 / 125 / 436 ✓.
- Waste: 15 % en metal y 6 % en board ✓; 0 % en compound / tape (BE-CF17) ✓.
- Base de compound / tape: 132,778 SF = todo el board (155,683) − sheathing − shaftliner − CBU ✓.
- **GRAND TOTAL del Partition Takeoff: 120,377.57 SF = Σ de las 804 filas = Σ de los 22 subtotales ✓.**

### 3.7 Fixes de la auditoría #1 que se sostienen

| Fix | Estado |
|---|---|
| FS-1 L1 | 7,928.8 SF ✓ |
| Retail GYP-1 | Excluido; BW-L1-RETAIL 399.46 SF ✓ |
| Corridor 412 | 1,350 SF RS-1 ✓ |
| RS6-L3 | 427.5 SF × 2 layers ✓ (las L3 301-304 restadas cuadran con el SF impreso: 296 + 270 + 269 + 269) |
| Mezzanine 219 | En RFI-15 ✓ |
| Ceilings L2 / L3 | Iguales al SF impreso de A2.02 / A2.03 ✓ |
