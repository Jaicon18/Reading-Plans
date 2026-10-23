# ARBITRAJE #25 (pruebas 25A y 25B, skill v76-ciego) y PAQUETE v77 — 2026-10-20

Material de arbitraje: lleva números de BOA. **NO viaja con el paquete v77** (E24).
Autoridad: plano (cota impresa + N/HOJA + imagen) > decisiones del usuario D1–D6 (Bluebeam, hoy) > rangos > reglas.
MEP fuera de calificación. Sin cambio (el usuario los revisa uno por uno, van en v78): criterios de partición y valores
aceptados de 3-5/8" stud, A1, G, G1, B2K, Exterior 6" CFMF.

## 0. Calificación (grader local del arbitraje #23, sin MEP)

| Prueba | ref v4 + rangos_v18m | ref v5 + rangos_v22 |
|---|---|---|
| 25A entregado | **95.0 %** (90.0 / 100) | 94.4 % (88.8 / 100) |
| 25B entregado | **92.6 %** (88.8 / 96.4) | 92.0 % (87.5 / 96.4) |
| 25A con v77 (canon77_A) | 93.8 % | **96.9 %** (93.8 / 100) |
| 25B con v77 (canon77_B) | 92.6 % | **94.5 %** (92.5 / 96.4) |

Reproduce el aviso (25A 95.0 / 25B 92.6; único MAL de familia: extra framing ATM 18.0 / 22.42). "Con v77" = tools v77
sobre el canon de cada prueba con las lecturas que las compuertas nuevas obligan a declarar (`anexos/canon77_A.json`,
`canon77_B.json`, armados por `anexos/armar_canon77.py`; cada lectura cita su detalle). Sobre los canons originales
canon.py v77 se detiene (las dos en D2: CONT. BOX BEAM sin `front_line`): es lo que debe pasar. Con v77 y la ref v5 ya
no queda ningún MAL. Contra v4 el renglón del ATM sale FALTA porque cambió de nombre (D1): es esperado.

## 1. Decisiones del usuario D1–D6 (regla genérica · compuerta · test)

| D | Regla (SKILL §24) | Compuerta | Test (test_v77.py) |
|---|---|---|---|
| D1 ATM | R77.1: extra framing ATM = la wall completa del ATM: studs de esa wall (studs_nodos, piso a deck) + bottom + top runner; la wall sale de su familia de stud / track (una vez). Fórmula sistered + furring borrada. | canon.py `_atm_wall`; accesorios.py `atm_recess_valido` (`{source N/HOJA, drawn}`; width / sistered / furring / alternativas = error; extra_framing kind atm_recess = error); chequeos_v72 R72.11 (fórmula vieja o ATM fuera de un wall = falla) | "D1 la wall del ATM completa…", "D1 fórmula vieja…" (malo: width / sistered / furring, sin drawn, kind atm_recess a mano; bueno: una wall, dos ATM = una vez) |
| D2 header / box beam | R77.2: box = 4 × (R.O. + 1'-4"); CONT. BOX BEAM = un run por frente, primera a última jamb + 1'-4" × 4; schedule con las piezas de su rótulo. | headers.py: `front_line {sheet, ori, c_pt, jambs_pt, scale_pt_per_ft, source}` obligatorio, ro_w_ft = jambs / escala, dos runs en la misma línea = error, run_ends solo jamb_to_jamb; `_piezas_rotulo` (SINGLE 1, DOUBLE 2, "2-…" 2) | "D2 CONT. BOX BEAM…" (malo: 4 runs por oficina en la misma línea, sin front_line, R.O. ≠ jambs, wall_to_wall), "D2 header schedule…" |
| D3 léelo | R77.3 (inviolable): lo impreso se aplica sin RFI; lo no impreso, por vector a la escala del detalle verificada contra algo impreso, imagen y [DERIVADO]. | `scale_check {printed_in, measured_pt}` ±5 % en chequeos_v77; schedule en headers.py | dentro de "D4 strip de pier…" |
| D4 piers | R77.4: 3/4" FRT plywood solo strip en cada jamb del storefront; ancho por vector × alto impreso; 2 capas con rótulo singular = 1 ply + RFI; las caras (nailbase, gypsum board) no van ahí. | chequeos_v77.py `r77_4` (lo llama canon.py): width_pt / escala, scale_check, jambs × height_ft = lf, plies + layers_drawn + rfi, label de cara = error; pier con `jamb_strips` o `jamb_strips_none_reason` | "D4 strip de pier…" (malo: ancho 4" a ojo, escala que no cierra, label de la cara, lf ≠ jambs × alto, sin rfi, pier sin strips) |
| D5 sill | R77.5: > 4'-0" × 2, ≤ 4'-0" × 1, solo con sill; door con sill = error. | headers.py | "D5 sill track…" |
| D6 transición | R77.6: borde de transición sin track de perímetro del ceiling (confirma R73.16 / R76.6). | chequeos_v76 `bordes_transicion` + canon.py `generar` (ya restaba) | "D6 borde de transición…" |

Imágenes de la ref v5 (abiertas después de marcar): `img/D1_A0201_ATM_wall.png` (rojo = wall del ATM 21.46 ft, azul =
ticks impresos 5'-1 1/4" y 14'-10" que verifican 18 pt/ft, verde = R.O. del DU ATM), `img/D1_A0811_6_DU_ATM_section.png`
(rótulos 6" METAL STUD FRAMING / 2 1/2" METAL STUD SISTERED), `img/D2_A0201_OF_east.png` / `_west.png` (primera a
última jamb), `img/D2_A0201_MW01_opening.png` (3'-1 1/2"), `img/D2_A1203_B3_MW01_sched_partition.png`,
`img/D4_A0925_1_pier_strips.png` / `_2_` (strips medidos), `img/D4_A0901_T_GLAZING.png` (T/GLAZING 8'-6").

## 2. Referencia v5 (archivo nuevo; la v4 no se tocó)

`BOA_Broomfield_REFERENCIA_v5.xlsx`: hoja "CAMBIOS v5" (v4 → v5 con operación y N/HOJA), hoja "D1-D6 v5 detail"
(cada abertura, cada strip, la wall del ATM), Material Summary y Familias actualizados (amarillo).

| Renglón | v4 | v18m | **v5** | Operación |
|---|---|---|---|---|
| Extra framing ATM (renombrado: "Extra framing - ATM wall (full wall framing, floor to deck + bottom and top runner)") | 109.87 | 49.87–51.41 | **381.39** [DERIVADO] | 6/A08.11 + A02.01 grid 2: wall 21.46 ft (454.44 → 840.72 pt / 18; ticks 5'-1 1/4" y 14'-10" verifican la escala); studs S1.11 6" @ 16" + zona 12" a 6 ft de la esquina: 1 + 12 + 6 = 19 − 1 en R.O. + 4 jambs + 1 L = 23 × 14.3583 = 330.24 + cripple 8.23 = 338.47; + 2 × 21.46 = **381.39** |
| 6" metal stud | 4,525.47 | 4,392.44–4,580.41 | 4,186.99 | − 338.47 (la wall del ATM una vez) |
| Bottom / Top track 6" | 293.04 c/u | familia 1,347.53 | 271.58 c/u | − 21.46 c/u |
| Header / metal stud box beam | 305.63 | 791.96 | **796.76** [DERIVADO] | 13 doors 3'-0" (R.O. 3'-4", A00.30) × 4.667 × 1 (SINGLE, 7/S5.20) + 102 (3'-10") × 2 = 10.33 + ATM-WU 2'-3" × 1 = 3.58 + MW01 3'-1 1/2" × 1 = 4.46 + ATM-DU box 2'-2 1/2" × 4 = 14.17 + 6 windows 8'-0" box × 4 = 224.0 + door 123 box = 18.67 + grille 103 2 box × 4 = 117.33 + VB-101 15.6458 × 4 = 67.92 + VB-100A 6.4167 × 4 = 31.0 + CONT. E (1,100.55 − 380.97)/18 = 39.977 → 165.24 + CONT. W (1,179.12 − 845.97)/18 = 18.508 → 79.37 |
| Sill track | 67.76 | 119.09 | **119.14** [DERIVADO] | 2/S5.20: 6 windows × 9.333 × 2 = 112.00 + ATM-WU 3.58 × 1 + ATM-DU 3.54 × 1 |
| 3/4" FRT plywood at storefront piers | 26.86 | (en FRT 6,481.82–6,855.85) | **23.59** [DERIVADO] | 1/A09.25: 81.96 y 81.84 pt; 2/A09.25: 81.96 y 54.00 pt, a 108 pt/ft (1 1/2" = 1'-0"; ply dibujado 6.72–6.84 pt = 0.75–0.76" vs 3/4" impreso) = 0.7589 + 0.7578 + 0.7589 + 0.5000 = 2.7756 ft × 8.5 (T/GLAZING 8'-6", A09.01) × 1 ply |
| Track, ceilings / soffits / canopy | 1,168.97 | 1,323.03 | **1,246.00** [DERIVADO] | 1,323.03 − 77.03 (track de perímetro en los bordes de transición de Waiting 104, RFI-CEIL-104 del arbitraje #21); 7/A09.33 remata con shadow molding (D6) |

`RANGOS_v22_propuesta.md` trae los rangos nuevos (y `anexos/rangos_v22.json`), las propuestas no aplicadas (A5,
acoustical sealant) y los RFIs con delta (RFI-H6 R.O. del DU ATM, RFI-H7 sill del DU ATM, RFI-ATM-H alto "piso a
deck" literal +23.38, RFI-PIER-PLY +23.59, RFI-CEIL-DIR).

## 3. Compuertas que bloqueaban datos verdaderos (R76.7 → R77.8)

| # | Problema | Arreglo | Test |
|---|---|---|---|
| a | A_BLOCKING no leía "F.R.T." con puntos (4/A09.26) | `RX_FRT_ROTULO = F\.?R\.?T\.?(W)?\|fire retardant / treated` | "R76.7 a" (malo "2X WOOD" sigue fallando) |
| b | `es_texto_es` marcaba rutas, archivos, "EL." e ids / coordenadas ("y 974.8") como español | `_sin_ids`: quita rutas, archivos, ids con dígito y guion, coordenadas x / y, "EL." antes de buscar | "R76.7 b" ("la cara del muro sur" sigue siendo español) |
| c | vigas_sobre_walls cruzaba bands de otra hoja | `cruzar(..., hoja=)` + `hoja_band` (band.sheet o w.sheet); salida `bands_de_otras_hojas` | "R76.7 c" |
| d | bitácora sin lock y sin resolver symlinks | `anotar` con fcntl.flock + fsync; hashes y `_vigente` por realpath (acepta claves viejas abspath) | "R76.7 d" (8 hilos, cadena intacta, symlink vigente) |
| e | inventario_tags / alcances leían el PDF con markups | `copia_limpia.py` (pikepdf, o pymupdf de respaldo); inventario_tags.inventario y alcances.escanear la usan siempre; arranque.json en la carpeta de trabajo (antes ruta fija) | "R76.7 e" |

Además: R77.7 (`carrying_direction` obligatoria con ceilings suspendidos) y plantilla_excel no valida como "repartida"
la familia FRT plywood cuando la rehace desde `frt_plywood_by_material` (un takeoff.json viejo con otro total la
bloqueaba).

## 4. Varianza 25A vs 25B (detalle: `anexos/VARIANZA.md`, imágenes `img/A5_*`, `img/CC_*`, `img/SEAL_*`)

| Familia | 25A | 25B | Causa | Qué respalda el plano | Regla / RFI |
|---|---|---|---|---|---|
| A5 | 42.63 (no 39.12: ese es un renglón de fascia sheathing) | 45.75 | PT0015: 25B mete en el run el tramo frente al MW01 (+3.127); 25A lo deja sin dueño. Door 116: tramo acotado 6'-11 1/4" en una cadena a 247 pt (cotas_banda win 72 no la ve) | 25B: A02.01 3'-1 1/2" con ticks sobre la línea A5; B3/B4 A12.03 dibujan la partición sobre el cabinet | R77.9 (lectura). A5 es criterio de partición → propuesta 45.75 para el usuario (no aplicada). Compuertas propuestas para v78: "tramo acotado sin dueño" y cota tick-aligned sin límite de distancia |
| carrying channel | 316.45 | 353.10 | 25B sin `carrying_direction`: lado largo por room (+35.75) + dims (+0.89) | ninguna hoja imprime la dirección; A08.01 imprime 11'-7 1/2" × 6'-6 3/4" (dims de 25A) | **R77.7 compuerta** + RFI-CEIL-DIR (N-S 316.45 / E-W 321.05 / lado largo 347.81). Con v77: 316.45 / 317.34 |
| acoustical sealant | 1,193.62 | 1,437.39 | 25B: OF jambs +193.00 (10/A12.01 "SEALANT", office front BY BANK VENDOR) y vestibule terminations +40.00 (8/A12.10 1/4" SEALANT del wall channel GL-4); walls +7.68 (MW01 +6.25) | 8/A12.10 es glazing (excluir); 10/A12.01 no concluyente | RFI de interfaz con otro trade (excluir ambos 1,204.39 / solo jambs 1,397.39 / ambos 1,437.39). Con D2 el bead del bulkhead sigue al box beam: +53.92 (RFI) |
| header / box beam | 759.67 | 796.71 | 25A: 6 CONT. BOX BEAM por oficina (212.00 vs 244.59) + sin MW01 (4.46); el resto igual (547.67 / 547.66) | D2 + 7/S5.20 | **D2 compuerta** (dos runs en la misma línea = error). Con v77: 792.27 / 796.73 (queda MW01 en 25A: R77.9 lectura) |

## 5. Paquete v77

| Archivo | file id | md5 |
|---|---|---|
| take-off-metal-frame-drywall_v77-dev.zip | 1wDcGRmYM4cpoUVBbBKETf4WMSD1z47ID | ca61aded536ab7b60561d4e1865d58a1 |
| take-off-metal-frame-drywall_v77-ciego.zip (armar_ciego.py) | 1EYlZHUB9gs8QYNt71jwcTpBk15R1BEkV | fc11afd1e2fcbee7fbdf979f5572c4c4 |
| BOA_Broomfield_REFERENCIA_v5.xlsx | 1gNWhBicbnvUDJzBnSPwK1Mbd8QHluq-Q | — |

SKILL.md md5: dev 83ff6f3eae3372b42223119ab64d507a; ciego cf650f2e005fcfcdeb2cf8e897fb6d61.

- Suite dev desde carpeta limpia (zip descomprimido, `correr_suite.py`): **56/56 OK** (test_v77.py nuevo, 13 casos;
  tests de ATM, CONT. BOX BEAM y ceilings actualizados al esquema v77).
- Ciego (desde el zip): test_smoke_ciego OK; test_ciego_tools --estricto **0 hallazgos**, y 0 con 646 valores externos
  (615 del arbitraje #24 + los de la ref v5 / rangos_v22); test_ciego.py modo prueba OK. canon.py del ciego da familias
  idénticas al dev sobre canon77 A y B.

## 6. Tabla antes / después (tools v77 sobre los canons de 25A y 25B)

| Item | Ref v4 (rangos_v18m) | Ref v5 (rangos_v22) | 25A antes (v76) | 25B antes (v76) | 25A v77 | 25B v77 |
|---|---|---|---|---|---|---|
| extra framing ATM | 49.87–51.41 | 381.39 | 18.00 MAL | 22.42 MAL | 385.44 IGUAL | 381.39 IGUAL |
| header / box beam | 791.96 | 796.76 | 759.67 | 796.71 | 792.27 | 796.73 |
| sill track | 119.09 | 119.14 | 119.12 | 115.58 | 119.12 | 115.58 |
| 3/4" FRT plywood piers (SF) | 26.86 (17.0–26.86) | 23.59 | 0.00 | 11.33 | 23.59 | 23.59 |
| track de ceilings / soffits | 1,323.03 | 1,246.00 | 1,365.05 | 1,294.10 | 1,365.05 | 1,294.10 |
| carrying channel | 235.04–321.79 | 235.04–321.79 | 316.45 | 353.10 | 316.45 | 317.34 |
| A5 (LF) | 39.12–42.76 | sin cambio (propuesta 45.75) | 42.63 | 45.75 | 42.63 | 45.75 |

Calificación completa en `anexos/grader_antes_despues.txt`.

## 7. Residuales (no MAL; siguiente ronda)
- ATM 25A 385.44 vs 25B 381.39: dueño de la esquina 2/D (wall 21.72 vs 21.46 ft, R70.2). La ref usa 21.46.
- Sill: 25B no pone sill al DU ATM (lee el 6" abierto hasta el plinth): RFI-H7 (−3.54). La ref sigue el R.O. acotado
  desde la línea de sill (R77.5).
- Track de ceilings: 25A +119 (bulkheads TF-R11A/C con track 112 LF) y 25B +48 (canopy soffit W 150.08 vs 114.82): no
  son de D6; quedan para la ronda de ceilings con imagen.
- MW01 en 25A (header 4.46 y tramo A5 3.13): R77.9 es lectura; la compuerta "tramo acotado sin dueño" va en v78.

## 8. Archivos
`ARBITRAJE_25.md`, `CAMBIOS_v77.md`, los dos zips, `BOA_Broomfield_REFERENCIA_v5.xlsx`, `RANGOS_v22_propuesta.md`,
`img/` (16 imágenes), `anexos/` (canon77_A / B, armar_canon77.py, excel77.py, grader.py, grader_antes_despues.txt,
rangos_v22.json, v5_valores.json + scripts que la arman, VARIANZA.md, Excel77 sin compuerta). Nada se borró ni se
sobrescribió; LISTO / PROCESADO sin tocar.
