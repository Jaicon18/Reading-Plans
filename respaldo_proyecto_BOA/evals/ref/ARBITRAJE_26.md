# ARBITRAJE #26 y PAQUETE v78 — 2026-10-21

Material de arbitraje: lleva números de BOA. **NO viaja con el paquete** (E24). Autoridad: decisiones del usuario
(W1–W4, 2026-10-21) > plano > rangos > reglas. Base: v77c-dev (md5 93d2ed3fc48b2f870646dde430e995da), referencia v7,
rangos v24; pruebas 26A y 26B (v77c-ciego).

## 0. Calificación de partida (reproducida)
Grader v77c, ref v7, rangos v24 con las dos claves MEP restauradas en modo excluir: **26A 88.6 %** (materials 87.9 /
types 89.3), **26B 95.7 %** (91.4 / 100). El encargo cita 89.5 / 94.8; con el grader del paquete no salen esos números
(diferencia de 1 familia en materials: el grader local que los dio califica familias que el del paquete no tenía).

## 1. Bugs (a)–(l): regla, compuerta, test (todos con caso malo / bueno)
| Bug | Regla | Tool / compuerta | Test |
|---|---|---|---|
| (a) deduct de abertura por todas las layers (26A +722.5 SF) | R78.1 `deduct_opening_sf` × layers; `deduct_sf` en face de >1 layer = error | board_caras `_deduct` | test_v78_g1 R78.1 |
| (b) metal trim `lf` × qty (26A 6,494.8) | R78.2 `lf` = total; `lf_each` × qty | canon `_trim_lf` | test_v78_g1 R78.2 |
| (c) detector de idioma con ids sin dígito ("-LO") | R78.3 quitar ids sin dígito y `#id+id` antes de detectar | idioma_es `quitar_ids`, plantilla_excel `_sin_ids` | test_v78_g1 R78.3 (el Excel 26B rearmado pasa `verificar`) |
| (d) cripples / vestibule head bajo viga desde el piso | R78.10 `stops_under_beam.base_ft` | canon `_v68_checks` §6 | test_v78_g2 R78.10 |
| (e) `thickness_measured_in` rechazado / exigido | R78.11 un solo campo numérico | canon `WALL_KEYS` + `_r78_espesor`; chequeos_v73 | test_v78_g2 R78.11 ×2 |
| (f) citas fijas de otro set (6/S5.20, 10/A09.33…) | R78.12 fuente del canon o "default (no sheet)" | headers, corridas, canon, accesorios, plantilla, studs_nodos… | test_v78_g2 R78.12 ×3 (barrido de literales) |
| (g) glass mat forzado en banda sin rótulo | R78.13 `band.sheathing: none` + fuente + img | canon `_banda_sin_sheathing` | test_v78_g2 R78.13 |
| (h) luminarias lineales sin ancho impreso | R78.25 SIDES_ONLY + RFI de los ends; R78.26 `length_add_in` | framed_openings `calcular` | test_v78_mk R78.25 / R78.26 |
| (i) plywood del fondo del fascia box | R78.14 `sheathing_bottom_ft` | canon `_fascia_sheathing` | test_v78_g2 R78.14 |
| (j) jamb return END con 1 layer | R78.4 `details[d].end_layers` / `face.layers_source` | board_caras `_end_layers` | test_v78_g1 R78.4 |
| (k) tag ambiguo no contado (PA0034) | R78.5 candidato que exige disposición | inventario_tags, comparar, etapas compuerta | test_v78_g1 R78.5 |
| (l) grupos "para otra tarea" sin dueño | R78.15 `owner` que exista en el canon | chequeos_v71 `r71_5` + `r78_15`, canon | test_v78_g2 R78.15 ×2 |

## 2. Varianza: causa, regla y decisión (cada número con su estado)

| Familia | 26A | 26B | ref v7 | v8 | Causa (plano) | Regla genérica |
|---|---|---|---|---|---|---|
| 2-1/2" CFMF coiling grille head | 4.93 | 10.43 | 7.85 | **10.43** [DERIVADO] | 4/A08.21 imprime la cadena 6" + 1'-6" = 2'-0" (tope del box superior → fondo terminado). 26A usó solo 1'-6" (stud 0.448); v4 escaló el stud contra 1'-6" (0.714). Operación: 2.0 − 2 × 0.5 (box 6") − 0.625/12 (board bajo el box) = 0.948 ft (medido 249 px / 263 px por ft = 0.947) × 11 studs (ROUNDUP(13.333/1.333) + 1, 1/A08.21 13'-4") = 10.43 | R78.30 cadena de cotas completa |
| B2K (type) | 1.50 | 1.773 | 1.773 | **1.773** (sin cambio) | U5 / R77.10 (usuario): medida al jamb / esquina, 1622.04 → 1653.96 pt / 18. 26A midió la extensión del rayado (1626.96) | R78.31 largo nodo a nodo, nunca el hatch |
| A5 (type) | 46.57 | 42.63 | 39.12 | **45.76** [DERIVADO] | R77.10: el largo corre a través de las doors. MW01 (R.O. 3'-1 1/2", A1/A12.03) es abertura de la A5 oeste y la door 116 está dentro de la A5 sureste; v7 traía #15 y #17 netos. Vector: el core del north wall (rect 1224.0–1529.4 × 968.4–973.8 pt) cruza NW y NE → las A5 arrancan en y 974.76. #14 (1324.08 − 974.76)/18 = 19.4067; #15 (1229.04 − 974.76)/18 = 14.1267; #16 (1324.08 − 1229.04)/18 = 5.28; #17 (1488.1 − 1363.1)/18 = 6.9444; Σ 45.7578. 26A dio la NW al A5 (+0.41); 26B dejó fuera MW01 (−3.13) | R77.10 + R78.35 dueño de esquina = core que cruza |
| purlin | 192.92 | 237.19 | 214.40 | 214.40 (rango 163.97–285.87) | 26B carga purlin en el top track del roof step (A-EXT-RS-3, 51.73 LF) y la chase C1 en 2 rows; 26A no. Ambos dentro del rango | R59.1 (purlin es regla de track): ya vigente; RFI-PURLIN-RS si el roof step no va a deck (delta ≈ −51.73 × factor) |
| gypsum board jamb return | 67.91 | 60.88 | 95.94 | 95.94 (rango corregido 60.88–95.94) | Mismo ancho 0.5 ft (6" stud, criterio, RFI); difiere el juego de aberturas con jamb return (26A 135.81 LF de bordes, 26B 121.75, ref 191.88). El rango v24 dejaba la ref fuera de su propio rango | RFI-JR: lista de aberturas cuyos detalles rotulan "GYPSUM BOARD JAMB RETURN" (2/A09.26, 11/A09.27, 1–3/A09.25); delta −28.0 a −35.1 SF |
| Level 5 | 874.86 | 712.87 | 874.83 | 874.83 (sin cambio) | A05.01 key note 9 "TO PREP FOR WALLCOVERING WC-20 PROVIDE LEVEL 5 FINISH" está en 24 HR VESTIBULE 101, sobre la face de la wall F diagonal: 161.98 SF. 26B no barrió el key note | R78.34 key notes de acabado = tags |
| metal trim | 1,153.05 (Excel 6,494.8) | 995.68 | 1,267.55 | 1,267.55 (rango 632.76–1,620.57) | Bug (b): `lf` total × `qty`. Resto: jamb returns × 2 y ceiling transitions (dentro del rango) | R78.2 |
| FRT blocking | 791.91 | 676.82 | 1,083.90 | 1,080.38 (W2 −3.52) | 4/A09.26 DIBUJA 2 plies rayados de 3/4" F.R.T. plywood en el tope del parapet; las dos pruebas cargaron 1 ply (≈ −270 LF) | R78.32 plies obligatorios con fuente |
| stud blocking 4/S5.20 | 717.27 (+89.15 items) | 561.99 (+64.23) | 466 | **591.55** [DERIVADO] (familia 591.55–680.70) | 26A: (i) usa el largo COMPLETO del wall si una face parcial pasa de 12 ft; (ii) cuenta 6 door bulkheads (face 14.2–15.4 ft desde el piso, pero la pieza de board arranca en el head: ~7 ft, sin junta) = +90. 26B: no leyó las faces "open to structure" (MW01 recess, ELECTRICAL 120/NER 121; A04.01 key note 1). Sobre las faces de 26A con (i)+(ii): EXT 212.13 + G 161.45 + B 60.27 + C1 47.64 + B2 38.40 + G1 35.49 + A1 22.13 + A1K 8.60 + A5 3.94 + B2K 1.50 = 591.55 | R78.33 (pieza de board y largo de la face alta); alternativa (a) sigue RFI |

Evidencia (reabierta, la marca cae donde debe): `img/V1_coiling_grille_4A0821_chain_2-0.png` (rojo: 6" y 1'-6"; azul: stud entre boxes y rótulo 2 1/2" CFMF @ 16" O.C.),
`img/V2_parapet_blocking_4A0926_2plies.png` (rojo: las 2 plies rayadas), `img/V3_Level5_A0501_keynote9_vestibule.png` (rojo: key note 9 en 24 HR VESTIBULE 101),
`img/V4_A5_gross_overlay_26A_red_26B_blue.png` (rojo 26A, azul 26B; verde: esquinas NW/NE, MW01 R.O., door 116), `img/W1_A0811_6_DU_ATM_sistered_furring.png` (rojo: los dos rótulos impresos; azul: título 6/A08.11).

Detalles de A08.21 revisados: 1 COILING GRILLE PLAN (13'-4"), 2 ELEVATION, 3 PLAN DETAILS @ JAMB (blocking de jambs, FRT), 4 HEAD DETAIL (fuente del renglón). A09.26: 2 storefront head (jamb return), 3 entrance canopy, 4 PARAPET (2 plies), 5 ACM base ("3/4" F.R.T. PLYWOOD BLOCKING AS REQUIRED" es de 4, leader al tope del parapet), 6 storefront base, 7 side canopy: sin cambio de cantidad aquí.

## 3. REFERENCIA v8 vs v7 (`BOA_Broomfield_REFERENCIA_v8.xlsx`, md5 beb454977501627aa9ba91efc0c016e4; hoja "CAMBIOS v8"; v4–v7 sin tocar)
| Item | v7 | v8 | Operación |
|---|---|---|---|
| extra framing ATM | 0 | **49.87** | W1: 6/A08.11 imprime sistered + furring (v4 EXT-6CFMF #65 columna AD, restaurada); walk-up nada impreso = 0 |
| EXT-PARAPET #160 (north) | 14.95 | **13.19** | W2 = wall norte #60; studs ROUNDUP(13.19 × 20/14.95) = 18 (−2 × 2.042 = −4.08); parapet tracks −1.76 c/u; ext gyp −3.59; FRT+polyiso −3.59; FRT blocking 2 plies × −1.76 = −3.52; PAF −1 |
| 2-1/2" CFMF coiling grille head | 7.85 | **10.43** | cadena 6" + 1'-6" (ver §2) |
| A5 (type) | 39.12 | **45.76** | R77.10 gross (ver §2); materiales solo por el largo sólido: #14 +0.4067, #16 −0.13 → 6" stud −13.05 (#16 −1 pc × 13.052), board +6.30, 6" tracks +0.28 c/u, bracing +0.83 |
| stud blocking 4/S5.20 | 466 | **591.55** | R78.33 (ver §2) |
| B2K | 1.773 | 1.773 | sin cambio (U5) |
Fórmulas y totales: `anexos/armar_ref_v8.py` (reproducible: `python3 armar_ref_v8.py v7.xlsx v8.xlsx`).

## 4. Markups Bluebeam (W3)
`markups_bluebeam.py <bid_set.pdf> <takeoff_canon.json> <salida.pdf>`: copia del bid set con una anotación PDF real
por wall (Line, o PolyLine para diagonales / cajas) sobre el eje de su `band` en la hoja donde se midió; color fijo
por partition type (OTHER FRAMING lavanda punteado); Subject = type; Contents = "TYPE · LF · N/HOJA · id"; Author
"Take-off"; /NM = TO-<id>; página de leyenda AL FINAL (las páginas del set conservan su número) con totales por type
y una línea de muestra por color; JSON resumen con el sha del canon. `verificar(pdf, canon)`: tipo, Subject, Contents,
Author, color, vértices ≤ 3 pt del eje y cubriendo los dos extremos. Compuerta: bitacora `markups_fallas` + entregar.py
paso 19b (sin PDF verificado = NO ENTREGABLE). Test: test_v78_mk.py (10 casos malo / bueno).

Verificación (pymupdf, reabierto por el árbitro): 26A 115 annots (A02.01 86 = 76 Line + 10 PolyLine; A02.02 10;
A04.01 19) + 15 de leyenda; 26B 110 (81 / 13 / 16) + 15; un color por type (15 types), 0 walls sin geometría,
`verificar` OK. Imágenes reabiertas: `img/markups_26B_zona2.png` (A1 rojo, A5 verde, G teal, G1 rosa, B2K celeste,
C1 marrón: cada línea cae sobre su wall), `img/markups_26A_*`.
PDF demo: **26A `1_bjzbdB9IgxU_n92r8nDVJNWbMBlueSi`**, **26B `1nKf3oV75n2-I1dWbT5gYg1SlrYGBy7BV`** (carpeta markups/).

## 5. Paquete v78
| Archivo | file id | md5 |
|---|---|---|
| take-off-metal-frame-drywall_v78-dev.zip | 1Xv7vRnF2pwz9owG_wLiKZD06N5Io1SGG | 80186f5cccea7b5282c2d6b90bb6e239 |
| take-off-metal-frame-drywall_v78-ciego.zip | 1ca1FYde-BPbRMD0kvlCez-iV6Aze7KYP | 70676512a4a24e1219e025b0883ccaeb |
SKILL.md md5: dev c7c079cfc918c3d62ec2d3c580111484; **ciego 207b7b19d18c48c96ea3ca37e0112988**.
Suite dev desde carpeta limpia (zip descomprimido, `correr_suite.py`): **61/61 OK** (+4 tests: test_v78_g1, _g2, _mk, _w).
Ciego: `armar_ciego.py` con rutas absolutas; test_ciego_tools --estricto **0 hallazgos** (y 0 con 298 valores externos
de v8/v25, `anexos/valores_v8_26.json`); test_smoke_ciego OK; test_ciego modo prueba OK.

## 6. Calificación antes / después (grader v78 completo, ref v8 + rangos v25)
Antes = Excel entregado por la prueba. Después = tools v78 sobre su canon con migración SOLO de esquema
(`anexos/migrar_canon_v78.py`; log en `anexos/migracion_canon_26*_v78.txt`: thickness texto→número, deduct_sf→
deduct_opening_sf, base_walls + lf_override "MIGRACIÓN", board_base_ft = head de su propio deduct_op, owner nombrado
en su propio motivo) y Excel rearmado con plantilla v78 (`anexos/regenerar_excel_v78.py`; 26B no subió takeoff.json:
se reconstruyó de su Excel). No se metieron correcciones de lectura del árbitro (plies, A5, coiling grille).

| | 26A antes | 26A después | 26B antes | 26B después |
|---|---|---|---|---|
| metal stud blocking | 806.42 MAL | 680.70 IGUAL | 626.22 IGUAL | IGUAL |
| metal trim | IGUAL | IGUAL | IGUAL | IGUAL |
| extra framing ATM (49.87) | 0 MAL | 12.0 MAL (solo sistered, sin furring) | 0 MAL | 12.0 MAL |
| coiling grille (10.43) | 4.93 MAL | 4.93 MAL | 10.43 IGUAL | IGUAL |
| B2K / A5 | MAL / IGUAL | MAL / IGUAL | IGUAL / CERCA | IGUAL / CERCA |
| framed openings MEP / stud reinf. MEP (excluir) | MAL / MAL | MAL / MAL | MAL / MAL | MAL / MAL |
| **Total** | **86.8** | **88.1** | **92.0** | **92.0** |
| Total sin calificar MEP | 89.1 | 90.6 | 94.5 | 94.5 |
Referencia vieja (grader v77c, v7, v24+MEP): 26A 88.6, 26B 95.7.

## 7. PARA REVISAR (total 2, una a la vez)
1/2. **MEP "excluido":** en modo excluir, todo renglón de framed openings MEP / stud reinforcement MEP sale MAL, y las
tools v78 los siguen emitiendo (son alcance hasta hoy). ¿MEP queda EXCLUIDO del alcance en todos los proyectos (como
U8: sin renglón, exclusión en Clarifications), o solo fuera de la calificación? Delta: 26A +2 familias (88.1 → 90.6),
26B (92.0 → 94.5).
2/2. **Extra framing ATM:** las pruebas cuentan solo el sistered (2 jambs × 6'-0" = 12.0); la v4 / v8 da 49.87
(sistered + furring). Delta −37.87 LF. ¿La operación de la v4 (49.87) sigue siendo la del usuario?

## 8. Protocolo de error (dos bloques)
Corto (system prompt):
```
v78: lo que un detalle IMPRIME en un recess de ATM (sistered/furring) se cuenta; el parapet sigue la wall exterior de su fachada; entrega SIEMPRE el PDF de markups Bluebeam verificado; alturas por la cadena de cotas COMPLETA; largo nodo a nodo (no el hatch); plies = los que dibuja el detalle; key notes de acabado se barren como tags; dueño de esquina = core que cruza.
```
Completo (skill): SKILL.md §26 (R78.1–R78.38), en el paquete v78.
