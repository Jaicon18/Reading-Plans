# INFORME DE AUDITORÍA ADVERSARIAL U-138 — CR City Hotel (415 Perry St, Castle Rock CO)

Auditor independiente: no participé en el take-off. Esta auditoría solo leyó los archivos del proyecto y escribió únicamente en `/root/cr/work/auditoria_U138/`.

**Versión auditada.** El Excel y el canon se regeneraron mientras auditaba. A las 05:55:56 UTC (21:55 PT) GYP-2 pasó a cargarse como MB-1. Las cifras de este informe corresponden a esa versión:
- `CR_City_Hotel_Takeoff_FINAL_rev1.xlsx`, 05:55:56 UTC.
- `takeoff_canon.json`, 05:54:58 UTC.
- Copia de la versión auditada en `snap/takeoff_canon_0555.json`.

**Etiquetas de cada número:**
- [CONFIRMADO]: cota impresa, con N/HOJA.
- [DERIVADO]: incluye la operación.
- [PENDIENTE]: no se pudo cerrar con el plano.

**Índices de página.** Uso el índice 0-based de `bidset_SIN_MARKUPS.pdf`: A0.06=9, A0.07=10, A0.08=11, A2.01..A2.04=16..19, A2.05=20, A3.01..A3.04=21..24, A5.05=36, A7.45=74, A7.50=75.

Las imágenes están en `img/` y las herramientas en `tools/`. Las rectas azules son los paths del canon, los círculos rojos marcan la evidencia.

---

## 1. Tabla de hallazgos

| # | Sev. | Qué | Evidencia N/HOJA + imagen | Delta estimado | Acción propuesta |
|---|---|---|---|---|---|
| 1 | **ALTA** | **Falta la membrana rated FS-1 en el cielo de L1, que es la cara inferior del piso de Level 2.** El tipo FS-1 de A0.08 dice "LEVEL 2, 3, 4 – THROUGHOUT – 1 HOUR – UL L546" y tiene una 2.ª fila: "LEVEL 2 – ABOVE PARKING AT ALLEY". La nota del detalle dice: "GYP AND RESILIENT CHANNELS WRAP STEEL BEAMS WHERE THEY ARE DEEPER THAN TRUSSES. **IN THE LOBBY**…". El canon solo carga FS-1 en los cielos de L2 y L3 (pisos 3 y 4) y RS-1 en L4. El piso de **Level 2** (cielo de L1: parking, lobby, staff, toilets, retail) no tiene FS-1. En el canon no aparecen "ABOVE PARKING" ni "WRAP STEEL BEAMS". | A0.08 tipo FS-1 (2 filas) `img/A008_FS1.png`, `img/A008_full.png`; A3.01 `img/A301_plan.png` | [DERIVADO] Uso como proxy de la huella de L2 sobre L1 el área FS-1 de L2 del propio canon, 5,997.4 SF. Resultado: **≈ +6,000 SF 5/8" Type C** y **+4,500 LF de resilient channel** (6,000 / 1.333). A eso se suman los beam wraps [PENDIENTE]. Se descuentan las zonas de L1 bajo roof (bar/courtyard). | Cargar FS-1 en L1 bajo toda la huella de L2, con el polígono de A2.02 sobre A3.01. Mantener debajo los GYP-1/ACT colgados. Cargar los beam wraps de FS-1 y reabrir ALC-15. |
| 2 | **ALTA** | **Retail 124: el sistema y el área del cielo están mal.** Se cargan **2,373 SF de GYP-1** (Type X + USG suspension + hanger wire 149 LF), que es el área impresa de todo el local. En A3.01 solo hay una **franja GYP-1 11'-0"** a lo largo de grid 7-8. El resto del campo está **sin hatch**, con una cota de 12'-0 3/4" y la nota "ASSEMBLY TO WRAP BOTTOM OF STEEL BEAMS. TYP.", es decir, la membrana FS-1 (hallazgo 1). Además, A2.01 dice "GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT". | A3.01 `img/A301_retail124.png`; A2.01 nota; canon CLG-L1-21 | **−2,373 SF Type X** de GYP-1 y su grid: main tee −593 LF [DERIVADO 2,373/4], cross tee −1,780 LF [DERIVADO 2,373/1.333], hanger −149 LF. Queda: franja GYP-1 [PENDIENTE de medir, ≈ 76 ft × 6 ft ≈ 450 SF a ojo en la imagen, sin cota] + FS-1 (va en el hallazgo 1). | Reemplazar CLG-L1-21 por la franja GYP-1 medida más FS-1 con beam wraps. Decidir si "by future tenant" excluye también la franja, que no es rated. |
| 3 | **ALTA** | **Falta el cielo de campo del corridor 412 (L4).** A3.04 muestra el corridor con stipple de gyp, una banda perimetral y un panel WS-1. El canon solo carga el cove perimetral (SOF-L4-02). No hay ningún renglón de cielo para 412. | A3.04 `img/A304_corr412_419.png`; A2.04 "1350 SF CORRIDOR 412" | [CONFIRMADO 1,350 SF/A2.04] **≈ +1,350 SF de board** (RS-1 o GYP-1, según el criterio de L2/L3), menos el WS-1 [PENDIENTE], y ≈ +1,013 LF de RC [DERIVADO 1,350/1.333] o grid. | Agregar el cielo de 412 con el mismo criterio que los corridors 216/218/316/318. |
| 4 | **ALTA** (en cantidad) | **Corner bead.** Hay esquinas que **no existen** y faltan otras obvias. (a) En CB_A2.02 se cuentan como "L corner" las esquinas exteriores del edificio (NW de la 214, por ejemplo) y las 2 esquinas E de la mezzanine 219. Desde adentro son *inside corners* y por fuera llevan siding: no llevan bead (≈ 4 × 9.9/5.9 ft ≈ 31.6 LF solo en esa vista). (b) Se marcan esquinas en jambas de puerta (201.2, 202.2). (c) **No se cuenta** el bead de los **window returns** (WIN-RET L2/L3/L4) ni de los bordes de **soffits/coves**, aunque ALC-18 dice que se tomaron de "window returns". (d) No se cuentan las esquinas de las cajas de elevador/escalera que sobresalen en los corridors. | `etapas/4_canon/img/cb/CB_A2.02_L2.png`, zoom `img/CB_A202_zoom_N.png`; Scope Checklist ALC-18 | **Faltan:** window returns ≈ **1,101 LF** [DERIVADO (324.51+324.51+85.28) SF / 0.667 ft de return]; soffit edges ≈ **1,207 LF** [DERIVADO: SOF-L1-01 295.78 + L2 152.26 + 167.54 + L3 170 + 170 + L4 8.73 + 242.72]. **Sobran:** ≈ 30–60 LF por hoja. Neto ≈ **+2,200 LF** sobre 1,939 LF. | Excluir las esquinas en XW y en la envolvente. Sumar el bead de window returns, soffits y cajas de shaft. Revisar A2.03/A2.04 con el mismo criterio. |
| 5 | MEDIA | **Franja de L3 bajo las terrazas 420/421 (RS-6).** A2.05 marca RS-6 sobre la franja de terraza. El detalle RS-6 de A0.08 dice "2 LAYERS, 5/8" TYPE X GYP BOARD". La fachada E de L4 está en x=1007.35 y la de L3 en x=1065.5. La franja de 301-304 queda bajo la terraza y el canon la carga como FS-1, 1 layer de Type C. | A2.05 `img/A205_terraces.png`; A0.08 `img/A008_RS6.png`; A2.04 `img/A204_terraza_vs_L3.png`; terraza impresa 29'-10" + 37'-6 1/4" [CONFIRMADO A2.04] | [DERIVADO (1065.5−1007.35)/9 = 6.46 ft × 66.17 ft = 427 SF] → **+854 SF Type X, −427 SF Type C**. | Partir las ceilings 301-304: la franja de 427 SF va como RS-6. Verificar la franja de la 309 bajo el deck de 411 ("RS-6 AT LEVEL-4"). |
| 6 | MEDIA | **¿Es correcto aplicar MB-1 a 104 y 116?** (cambio de las 21:55 PT) Para **Generator 103 está bien**: MB-1 dice "LEVEL 1 – GENERATOR ROOM – 2 HR – BXUV.1516" y A3.01 marca la 103 como GYP-2. Para **ELEC 104 y ELEVATOR CONTROLS 116 es un supuesto**. MB-1 solo nombra el generator room. GYP-2 remite a otro listado ("RATED 2-HOURS, **AER-09038**"), no a BXUV.1516. La 116 es "ELEVATOR CONTROLS… OUTSIDE OF SHAFT PER IBC 3005.4 EXC. 2" (A7.45), así que el 2 HR es razonable, pero el ensamble no está impreso. La aritmética del cambio cuadra: Type X +401.35 SF (802.7→1,204.05), shaftliner +401.35 SF (541.8→943.15), C-H stud +252.86 LF, J-runner +83.46 LF, main tee −100.34 LF [DERIVADO 401.35/4]. | A0.08 `img/A008_MB1.png`; A3.01 `img/A301_GYP2_gen.png`; A7.45 nota de la 116 (en `img/A745_nota_FB_NIC.png`); Pending Items RFI-13 | Si 104/116 llevan AER-09038 como 2 layers con suspension: **−219.65 SF Type X, −219.65 SF liner, −143.06 LF de C-H stud, −50.36 LF de J-runner** [DERIVADO 165.3 + 54.35; 97.1 + 45.96; 34.04 + 16.32] y +grid. | Dejar MB-1 en la 103. En RFI-13, abrir una alternativa explícita para 104/116 (AER-09038 sin MB-1) con ese delta. Hoy la opción B solo pregunta el stud y la C-channel. La C-channel tampoco está cargada (anotado en RFI). |
| 7 | MEDIA | **Walls que atraviesan vanos de puerta.** En 4 de los 20 walls de la muestra el LF incluye el ancho de la puerta. En **W.4-L3-44** (4.29 LF) **todo el path es el vano** de la puerta 308.2. El barrido por vector (cobertura de líneas de muro < 60 % del path en A2.02-A2.04) da 28 walls interiores con este problema. El Material Summary dice "length x face height x layers **- openings**", pero **ningún** renglón descuenta vanos (0 de 765). | `img/muestra_walls_2.png` (W.62-L3-15), `img/muestra_walls_3.png` (W.4-L3-44, W.62-L4-12), `img/hallazgo_paths_por_puertas.png`; `snap/coverage.json` | [DERIVADO, sumando LF × (1−cobertura) en los 28] **≈ −100 LF / −2,350 SF de board** si se descuentan vanos. Mínimo: quitar los walls fantasma (W.4-L3-44, partes de W.4-L2-18/21/24/27, W.4-L3-02/05/08/11, W.62-L2-02, W.62-L3-06, W.62-L4-11). | Decidir la política (deducir o no los vanos de puertas) y alinear el texto del Summary. Recortar los paths que solo son vano. |
| 8 | MEDIA | **F&B "NOT IN SCOPE": criterio inconsistente con RFI-05.** A7.45, A7.50, A7.55, A2.04 y A5.07 dicen: "INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT…". Con el mismo criterio de RFI-05 (no-rated → fuera), se cargan caras **no-rated** de Kitchen 100 (L1), F&B 410, Deck Bar 411 y Warming Kitchen 419. | A7.45 `img/A745_nota_FB_NIC.png`; canon: W.6-L1-03 A, W.6-L1-04 (cara Kitchen), FI.2-L1-03, FW.4-L4-16, XW.6.6-L4-16, W.6-L4-15, FI.6-L4-01, W.6-L4-05 A, W.6-L4-07 A | [DERIVADO: 255.8 + 446.8 + 442.1 + 30.9 + 44.8 + 17.2 + ≈ 400 (419)] **≈ −1,600 SF Type X**. Las caras rated (W.62-L4-04/05/06/07, XW rated, W.6-1) quedan. | Aplicar la regla de RFI-05 a F&B o documentar por qué no. La warming kitchen 419 tiene la nota NIC dentro de su recinto en A7.50. |
| 9 | MEDIA | **Partition Takeoff: el GRAND TOTAL vale 0 LF / 0 SF.** El valor está escrito a mano y la hoja no tiene ninguna fórmula. Los subtotales LF suman registros cara/capa, no LF físico: W.62-1 da 1,462.47 LF y el físico es 771.9 LF [DERIVADO, IDs únicos]. | Excel, Partition Takeoff fila 5 | La suma real de board es 121,867.05 SF [DERIVADO] = Type X 73,237.5 + WR 26,528.6 + CBU 5,308.3 + liner 541.8 + ext. sheathing 16,250.9. | Poner fórmula en el total. Mostrar LF físico y LF de cara por separado. |
| 10 | BAJA | **Walls marcados en la hoja equivocada y a escala equivocada.** W.4-L4-21 y W.4-L4-22 tienen coordenadas de 3/A7.50 (1/4") pero están marcados en A2.04 y medidos a 9 pt/ft. En A2.04 caen en espacio vacío (cobertura 0.0). | `img/hallazgo_paths_por_puertas.png` (2 primeras viñetas) | [DERIVADO] L real = 51.1/18 = 2.84 ft (no 5.68) y 19.17/18 = 1.07 ft (no 2.13). Sobran **3.9 LF ≈ 70 SF** WR, y el markup queda en la hoja equivocada. | Moverlos a A7.50 y recalcular a 18 pt/ft. |
| 11 | BAJA | **Supuesto silencioso en la mezzanine 219.** El cielo de 462 SF se carga como GYP-1 con suspension. La fuente dice "PENDIENTE (sloped roof… roof type not tagged)" y la superficie inclinada es 536.7 SF, pero no figura en Pending Items. | canon CLG-L2-64 | [DERIVADO 536.7 − 462] **+74.7 SF** si el board sigue la pendiente. | Llevarlo a Pending Items con su delta. |
| 12 | BAJA | **Waste.** Joint compound y tape tienen 0 % de waste, pero Inputs dice "Waste – EVERYTHING THAT IS NOT METAL = 6 %". | Material Summary | +546 lb y +2,815 LF [DERIVADO 9,129.91 × 0.06; 46,917.58 × 0.06] | Aplicar 6 % o documentar la excepción. |
| 13 | BAJA | **RFI-15 contradice la carga del RS-1 de L4.** El texto dice "1 layer 5/8" Type X on **hat channel**", pero lo cargado es **resilient channel** a 16" o.c. (sistema "resilient_channel", que forma parte de los 10,516.4 LF de RC). | Pending Items RFI-15; canon ceilings 42-49 | 0 SF; cambia el producto de 1,655 LF [DERIVADO 2,207.07/1.333]. | Unificar el producto. |
| 14 | BAJA | **Dimensión impresa vs path.** W.6-L1-31: cota impresa **9'-1 1/2"** en 1/A7.50 [CONFIRMADO] contra 8.82 LF cargados. | `img/muestra_walls_1.png` | −0.31 ft × 12 × 2 × 2 = −14.7 SF (subcarga) | Menor, sin acción. |
| 15 | BAJA | **Exclusión mal razonada.** ALC-15 excluye los "L1 retail steel beam wraps by future tenant", pero son parte del ensamble rated FS-1 (nota del detalle A0.08). Según la propia lógica de RFI-05 (rated → se carga), van incluidos. | Scope Checklist ALC-15; A0.08 FS-1 | [PENDIENTE] LF de vigas × desarrollo | Va con el hallazgo 1. |

---

## 2. Muestra de 20 walls (punto 1)

La selección fue aleatoria con seed 138 y estratificada (`snap/sample.json`). Cada LF se re-midió como |path|/escala impresa: 9 pt/ft en A2.0x y 18 pt/ft en A7.50. Después revisé cada path contra el dibujo (`img/muestra_walls_1..4.png`).

| Wall | Tipo | Hoja | LF canon | Verificación |
|---|---|---|---|---|
| XW.6.3-L1-01 | XW.6.3-0 | A2.01 | 5.58 | OK: pier en la puerta 108.1, tag XW.6.3. 1 cara de Type X correcta según A0.07 (exterior de plywood). |
| CH.6-L1-04 | CH.6-2 | A7.50 | 2.01 | OK [DERIVADO 36.18/18]. Tag CH.6 2. Liner + 2 layers Type X correcto según A0.06 CH (2 HR). |
| W.6-L1-15 | W.6-2 | A7.50 | 8.19 | OK frente a la cota 8'-1" [CONFIRMADO 1/A7.50] más el espesor de muro. |
| W.6-L1-31 | W.6-2 | A7.50 | 8.82 | Cota 9'-1 1/2" (hallazgo 14). 2 layers en 2 caras correcto (tag W.6 2). |
| W.62-L2-06 | W.62-1 | A2.02 | 10.59 | Incluye el vano de la puerta 210.1 (hallazgo 7). 2 layers por cara correcto. |
| W.62-L2-03 | W.62-1 | A2.02 | 0.83 | OK, return corto. |
| XW.6.3-L2-09 | XW.6.3-2 | A2.02 | 8.16 | OK. Tag XW.6.3 2. 2 ext + 2 int correcto. H 9.8958 [CONFIRMADO 9'-10 3/4" 4/A5.05]. |
| FW.4-L2-02 | FW.4-0 | A2.02 | 4.18 | OK geométricamente. Furring sobre CMU de la escalera. |
| CH-L2-02 | CH.6-2 | A2.02 | 4.46 | OK (shaft sur de la lobby 217). |
| DW.4-L2-03 | DW.4-1 | A2.02 | 18.03 | OK. Tag DW.4 1. 1 layer por cara (U341). |
| W.62-L3-15 | W.62-1 | A2.03 | 4.61 | **El path cruza la puerta 309.1.** Solo hay un stub de unos 0.3 ft (hallazgo 7). |
| XW.6.3-L3-03 | XW.6.3-2 | A2.03 | 10.17 | OK. |
| XW.6.3-L3-06 | XW.6.3-0 | A2.03 | 6.84 | OK (notch 2'-3" × 9'-7"). |
| W.4-L3-44 | W.4-0 | A2.03 | 4.29 | **Wall fantasma: todo el path es el vano de la puerta 308.2.** |
| FW.6-L3-02 | FW.6-0 | A2.03 | 6.67 | OK (respaldo de shower, CBU + WR). |
| XW.6.6-L4-07 | XW.6.6-2 | A2.04 | 8.90 | OK. 1 ext + 2 int correcto según A0.07 XW.6.6-2. |
| XW.6.6-L4-03 | XW.6.6-2 | A2.04 | 12.07 | OK. |
| W.62-L4-12 | W.62-1 | A2.04 | 6.82 | **Incluye la puerta 403.1** (≈ 50 % del path). |
| CH.6-L4-04 | CH.6-2 | A7.50 | 4.10 | OK [DERIVADO 73.8/18]. |
| FW.2-L4-05 | FW.2-0 | A2.04 | 18.67 | OK. |

**Alturas.** Verifiqué en 4/A5.05: "9'-2 7/8"" interior (9.2396 ft) [CONFIRMADO], "9'-10 3/4"" en la zona exterior (9.8958 ft) [CONFIRMADO] y "1'-9 1/8"" de floor zone [CONFIRMADO]. Imagen: `img/A505_4_alturas.png`.

**Tipos y capas.** Contrasté W.62-1, W.6-1/2, DW.4-1, CH.6-2 y XW.6.2-2/6.3-0/6.3-2/6.6-1/6.6-2 contra A0.06 y A0.07. Imágenes: `img/A006_Wtable.png`, `img/A006_CH.png`, `img/A007_*.png`.

**Resultado:** 16 de 20 walls OK en LF, tipo, capas y altura; 4 de 20 tienen vanos de puerta dentro del LF.

## 3. Barrido A2.02 / A2.04 (punto 2)

**A2.02.** Superpuse los paths del canon sobre el plano completo y lo revisé por cuadrantes (`img/ov_A2.02*.png`). No encontré walls dibujados sin path, salvo stubs de shower y curbs menores. Tampoco encontré tags sin wall.

Notas sobre tags de A2.02:
- Los tags "XW.6.3 | 1" y "XW.6.4 | 1" no existen en A0.07. Se mapearon a XW.6.6-1 por la regla de RFI-02 (cerrado); el board es igual y el delta es 0.
- XW.6.3-L2-06 tiene impreso "XW.6.3 1" y está cargado como XW.6.6-1.

**A2.04.** La revisión fue a nivel general (`img/ov_A2.04.png`), no tan fina como la de A2.02. Encontré walls fantasma (hallazgo 10) y la falta del cielo de 412 (hallazgo 3). El barrido por cobertura vectorial (`snap/coverage.json`) cubrió A2.02-A2.04.

## 4. Cielos (punto 3)

- **FS-1, room 201:** 294 SF [CONFIRMADO A2.02, unidad completa incluido el baño]. OK.
- **RS-1, room 402:** 461.17 = 556 − 94.83 [DERIVADO]. OK aritméticamente. Producto: ver hallazgo 13.
- **GYP-1 Retail 124:** error (hallazgo 2).
- **MB-1 Generator 103:** 181.7 SF [DERIVADO 297.9 × 197.6/324]. OK. 104/116: hallazgo 6.
- **GYP-1, corridor 216:** 455 SF bruto [CONFIRMADO A2.02], bajo FS-1. OK como criterio.
- **Corridor 412 (L4):** falta (hallazgo 3).
- **Franja L3 bajo RS-6:** hallazgo 5.
- **Membrana FS-1 de L1:** falta (hallazgo 1).

## 5. Material Summary (punto 4)

Todos los renglones de board reconcilian al 0.01 contra el canon:
- **Type X 86,187.00** = walls 73,237.52 + misc 10,742.47 + RS-1 2,207.07.
- **WR 28,802.47** = 26,528.61 + 2,273.90.
- **CBU 5,308.33**, **ext. sheathing 16,250.89**, **liner 943.15**, **Type C 11,814.80** = FS-1 L2 5,997.4 + L3 5,817.4.
- **RC 10,516.4** = 14,021.87 SF / 1.333.
- **Grid y track:** cuadran con misc_items.
- **CB 1,939.18** = la suma de trim_items. **CJ 849.36**.
- **JC y tape** = 0.072 y 0.37 × 126,804 SF (Type X + WR + Type C).

Pieces = ROUNDUP(Net × (1 + w)/stock) es correcto en todos los renglones revisados (Type X 1904, liner 21, C-H 46, etc.). El waste está bien aplicado (metal 15 %, no-metal 6 %), salvo JC y tape (hallazgo 12).

## 6. RFIs (punto 5)

- **RFI-13:** el cambio a MB-1 de las 21:55 resolvió la parte impresa. Queda el supuesto de 104/116 (hallazgo 6).
- **Supuestos silenciosos:**
  - FS-1 de L1 nunca preguntado ni cargado (hallazgo 1).
  - Retail con GYP-1 en toda el área (hallazgo 2).
  - Techo de la mezzanine (hallazgo 11).
  - Criterio F&B (hallazgo 8).
- **RFI-05, retail:** coherente para muros, pero no se extendió al cielo ni a F&B.
- **RFI-15:** el texto no coincide con la carga (hallazgo 13).
- **RFI-17 (Water Entry 128) y RFI-09:** sin evidencia impresa nueva.

## 7. Corner bead (punto 6)

Revisé CB_A2.02_L2 (zoom `img/CB_A202_zoom_N.png`) y la lógica de CB_A7.50. Hay esquinas contadas que no son outside corners de drywall y faltan familias enteras (hallazgo 4).

## 8. Exclusiones (punto 7)

- **Excluido por error:** los beam wraps de FS-1 del retail (ALC-15, hallazgo 15).
- **Correctas:** wood/FRT/LP (Div. 06), fasteners, ACT/WS-1, insulation, CMU, separate-permit, acoustical sealant (orden permanente).
- **Cargado ajeno al alcance:** las caras no-rated de F&B (hallazgo 8).

## Verificado OK

- Escalas por hoja.
- Alturas de 4/A5.05.
- Capas por tipo según A0.06/A0.07.
- Conciliación completa del Material Summary.
- Roundups y waste (salvo hallazgo 12).
- Aritmética del cambio a MB-1.
- 16 de 20 walls de la muestra.
- El barrido de A2.02 no encontró walls dibujados que falten.
