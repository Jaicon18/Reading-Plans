# CERTIFICADO PASO 12 — Matriz de cobertura total (segunda revisión independiente)

**Proyecto:** Barnes & Noble – Colorado Springs (3173 Cinema Point) · **Entrega revisada:** rev6 (`FINAL_FOR_REVIEW_2026-10-24_rev6`)
**Fecha:** 2026-10-27 · **Skill:** take-off-metal-frame-drywall v80m (§0.F Paso 12, AUTONOMÍA TOTAL, R80e.26)
**Fuentes usadas:** solo el bid set (69 págs., Drive) y los entregables: el Excel rev6, el PDF de markups rev5 (la geometría no cambia en rev6) y `DECISIONES_ESTIMADOR.md`, que solo se usó para separar las decisiones del estimador de los errores. No se abrió `takeoff_work/`, `AUDITORIA_rev4/`, `investigacion_WR_FRT/` ni ningún take-off de terceros. **No se editó el take-off.**

## Veredicto

**NO PASA — la entrega queda bloqueada hasta aplicar las correcciones.** Hay tres motivos:
1. La cobertura de rev6 es **90.0 %**, por debajo del 100 % exigido.
2. Hay **9 CORREGIR** confirmados por el plano.
3. La biblioteca de errores tiene **5 pruebas en FAIL**.

Cada GAP ya trae su destino propuesto (renglón, exclusión o RFI con delta). Si se aplican todos, la cobertura sube al 100 %.

## (a) Matriz de cobertura — `MATRIZ_COBERTURA.xlsx`

| Concepto | Cantidad |
|---|---|
| Ítems Div 05 / Div 09 extraídos (69 págs.) | **471** |
| COVERED (renglón del Excel) | 209 |
| EXCLUDED (con motivo) | 147 |
| RFI (RFI existente) | 58 |
| CORREGIR (filas de la matriz; únicos = 9) | 10 |
| GAP (sin destino; ~35 temas únicos, con duplicados entre hojas) | 47 |
| **Cobertura rev6** = (471 − 47) / 471 | **90.0 %** |
| Cobertura si se aplican los destinos propuestos | 100 % |

**Hojas del libro:**
- Coverage Matrix: Sheet, Item type, Text, Destination, Excel row / Exclusion reason / RFI, Status, más Ref, motivo y valor correcto, imagen y página.
- Summary: conteos por hoja.
- CORREGIR
- Error Library
- Proportions
- Bluebeam vs Excel

**Barrido:** se leyeron las 69 páginas. La mayoría de las hojas A tienen el texto vectorizado y se leyeron sobre la imagen, por zonas. Las hojas E/M/P y las narrativas de revisión se leyeron sobre el texto y se verificaron en la imagen. Las 118 imágenes con anillo rojo están en `img/`, cada una reabierta y verificada.

## Lista de CORREGIR (valor correcto + evidencia)

| ID | Qué | Plano (N/HOJA) | Corrección | Imagen |
|---|---|---|---|---|
| C-01 | RFI-34 dice que el T.O. WD-1 del Grab & Go header no está impreso | 5/A-226A: 11'-0" + 4'-0" · 6/A-226A: 15'-0" [CONFIRMADO] | Cerrar RFI-34 con T.O. WD-1 = 15'-0". **+61.67 SF de 5/8" Type X** arriba del WD-1 hasta el deck [DERIVADO 6.167 × 10.0]. El plywood no cambia | `A-226A_5-TO-WD-1-15ft-grab-go.png` |
| C-02 | RFI-13 dice que la altura del FRP-1 no está impresa | 1–4/A-226B: Work Room a 10'-0" · A-131: Janitor 96" AFF · 9–12/A-200: 8'-0" | Corregir el texto y el delta de RFI-13: 87.52 × 10 = 875.2 SF + 19.43 × 8 = 155.44 SF bruto [DERIVADO]. Quién lo instala sigue abierto | `A-226B_4-FRP-1-full-height-10ft.png`, `A-131_janitor-frp-96aff.png` |
| C-03 | RFI-12 dice que el backer del tile no está detallado | 22/A-201: 5/8" CEMENT BOARD BASE 1'-2", W.R. arriba · A-001A Div 09 J.2 | Cargar cement board 1'-2" en la base de los walls nuevos de los restrooms y descontar lo mismo de W.R. Tope superior: 75.44 SF bruto, ~68.4 SF neto [DERIVADO]; recalcular sobre caras nuevas | `A-201_22-tile-base.png` |
| C-04 | Cement board de C-E1-S sobre 23.46 LF | 1/A-221: "19'-0" HOLD" en la cara expuesta [CONFIRMADO] | 19.00 × 25 = **475.0 SF (−111.5 SF)** en Material Summary R27; studs y track sin cambio | `A-221_E1-S-19-0-HOLD.png` |
| C-05 | ALC-24 dice "no finish level specified" | A-001A Div 09 A.8: "LEVEL 4 FINISH" | Cambiar ALC-24 a QUANTIFIED, Level 4 impreso; corregir la nota de Inputs!R23. Sin cambio de cantidad | `A-001A_div09-A8-level4.png` |
| C-06 | Se cita 6/A-210 para el vestibule box | 6/A-210 es el Base Detail del glazing | Cambiar la cita a 7/A-210 y 8/A-210 en R10, R12 y R13. Sin cambio de cantidad | `A-210_6-base-detail.png` |
| C-07 | Se cita 8/A-410 como Top Track Detail | El Top Track Detail es 3/A-410; 8/A-410 es Typ. Connection | Cambiar la cita en R12, R13, R47, RFI-04, RFI-35, ALC-04 y ALC-06 | `A-410_3-top-track-detail.png`, `A-410_2-type2-detail.png` |
| C-08 | Las plates de MEP se citan a 6/A-410 | 6/ y 7/A-410 son firestop de pipe; no imprimen plates | Marcar como "skill default (not printed)"; RFI en 0 | (filas G7) |
| C-09 | Door 4 rotulada "inside W2-05" | A-101 / A-500: la door 4 está en el wall norte del corridor = W2-04 | Mover el rótulo y los jamb studs a W2-04; el board no cambia | `A-500_door-4-location-A101.png` |

## GAP principales (sin destino en rev6; destino propuesto en la matriz)

**Montos impresos o derivables:**
- **A-410:** los types 1/1A/1B/1C rotulan "5/8" GYP BD BY FUTURE TENANT", y A-002 no pone el board a cargo del LL.
  - Pide un RFI frente a la decisión RFI-01, que no se cambia.
  - Delta tope: ≈10,436 SF de Type X [DERIVADO 417.43 × 25].
- **A-410 stud schedule y notas:**
  - Calibres: el Excel no tiene gauge en ningún renglón. Type 2 = 14 ga SJ; track del mismo gauge; mínimo 20 ga.
  - Los walls Cafe de 3-5/8" llegan a 25' y superan el máximo de 22'.
- **A-410, renglones faltantes:**
  - Clip angle en cada cruce del C.R. channel (5/A-410): ≈2,163 clips.
  - Fasteners de top track a estructura (8.C).
  - Screws de plywood (8.D).
  - Runner anidado (3/A-410): lectura plausible.
  - Cross members paralelos a los joists (8/A-410).
- **2/A-221:** el FRT plywood sigue arriba del WD-1 (+328.9 SF) y hay cross bracing "AS REQ'D".
- **E/A-221 y H/A-221:**
  - Alto del board en E1/E2 (E2 FRT −424.85 SF si se aplica el criterio de ceiling + 6").
  - H3b arriba de 8' (+104.9 SF).
  - H3a: T.O. WD-1 no impreso.
  - Pier void de H2a (−66.7 SF).
  - F: nested stud bracing.
- **A-225:** conflicto de material (marine plywood en 5/A-225 y FRT de 1/2" en 10/A-225).
- **Vestibule:**
  - Bandas de GWB 3/A-210 (+13.33 SF) y 2/A-210 (+1.63 SF), V.I.F.
  - Clip angles 7/A-210.
- **5/A-121:**
  - Splay wires sísmicos; la nota manda a A-420, que no está en el set.
  - Hangers adicionales en luminarias.
  - Tie wire.
- **A-002:**
  - Seismic bracing F/I del TC.
  - ACT ceilings (A-121, A-510, A-002): ni cuantificados ni excluidos.
- **Corner bead en bordes de soffits** (A-510 finish note 8): +65.31 LF.
- **Grab & Go GWB ceiling a 7'-1":** ≈25.2 SF.
- **FE cabinets empotrados:** 4/A-101 "F.R.T. WOOD STUD HEADER ABOVE AND BASE BELOW CABINET", C11, A-111 KN9, A-002 Div 10. Son 4 en walls nuevos; el tamaño está [PENDIENTE].
- **A-101 general note 8:** caulk en la base de los walls de wet areas.
- **2/E-103:** 4'x8' FRT plywood "BY GC" en el server room. Delta +32 SF.
- **Strut channel / Unistrut:** A-001A Div 05 D y la Cafe signage de A-002.
- **Remove & replace de GWB existing** para blocking (7/A-413). 7A/A-413 dice surface-mount y 7/A-413 dice in-partition.
- **2/A-500:** wood blocking del cased opening.
- **RFI-03:** el rango del deck se amplía (A-400A 21'-9" V.I.F., A-400B 23'-8" V.I.F.).

## (b) Biblioteca de errores — `cache_proyectos/BIBLIOTECA_ERRORES.md`

**29 pruebas: 21 PASS · 5 FAIL · 3 N/A.**

**FAIL:**
- **BE-08:** no se respetó la cota impresa (C-01, C-02, C-04).
- **BE-12:** citas que no corresponden a la hoja o detalle (C-06, C-07, C-08).
- **BE-13:** backboard de las hojas E sin destino (2/E-103).
- **BE-40:** la R28 de Material Summary (61.31 LF de studs del framed soffit) no trae desglose; FIRESTOP-TRACK tampoco tiene desglose por wall.
- **BE-41:** nombres internos (`AUDITORIA_rev4/…xlsx`, `ri07_rcp/`) en Pending Items.

**PASS destacados:**
- Fire-stop track presente.
- W.R. en walls y ceilings de wet rooms y no donde no hay gypsum.
- Capas por lado (R80e.26): las secciones de A-221 cuadran con el Excel.
- Soffits por lado.
- Caras de remate I SIM.
- Perímetro existing.
- Track = partitions.
- Orden y subtotales.
- 6 hojas.
- Cuadre Bluebeam.

## (c) Proporciones (hoja Proportions)

Todas están en rango o explicadas:
- **Board vs Σ LF × H × capas:** 0.74. Se explica por las caras hasta ceiling + 6" (RFI-19) o hasta B.O. GYP CEILING (2/A-410). Cada fila cuadra con su altura.
- **Conciliación de board:** Δ 0.06 SF.
- **Screws:** 1.20/SF. Compound: 0.072 lb/SF. Tape: 0.37 LF/SF. Todos iguales a los yields de Inputs.
- **Studs/LF:** 1.0–1.4 típico. Los valores mayores (W2-06 2.01, caps type 4 1.64, column wraps 1.71) se explican por jambs, nodos y cajas.
- **Track = partitions − caras de remate:** 1.206 LF.
- **Pins = bottom track.**
- **Bracing:** 6 filas en walls de 25 ft.

Observaciones:
- El cement board (851.4 SF) no tiene fasteners.
- R28 no trae desglose.
- El fire-stop track no trae desglose por wall.

## (d) Cuadre Bluebeam vs Excel (hoja Bluebeam vs Excel) — OK

- Σ Length y Σ Wall Area (Length × Depth) cuadran en los 18 types. El Δ máximo es 0.01 LF, en el type I, por redondeo.
- Las 77 anotaciones están dentro del 2 % de su geometría y su Depth es igual a la altura del Excel.
- Los 17 walls EXISTING están marcados "EXISTING – EXCLUDED".

## Pasos siguientes (para la sesión del take-off, regla de autonomía)

1. Aplicar C-01 … C-09.
2. Dar destino a cada GAP: RFI con delta, renglón o exclusión, según la matriz.
3. Corregir BE-40 y BE-41.
4. Volver a correr el Paso 12 sobre la rev7.
