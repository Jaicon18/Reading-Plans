# RESUMEN rev15 — CR City Hotel (Castle Rock, CO)

rev15 reemplaza a rev14. Origen: tu orden del 10-nov, "revisa todo otra vez". Tres revisores independientes revisaron rev14 completa (walls, RCP + PDF, RFI + materiales), sin muestreo. COORDINACIÓN pasó 18 puntos.

Cada punto quedó en uno de tres estados, siempre con N/HOJA e imagen:
- **Cargado:** se corrigió la cantidad.
- **Refutado:** lo impreso dice otra cosa, y se cita.
- **Decidido:** por una regla fija.

Las imágenes están en `Auditoria/revision_completa_rev15/`: REV_* es lo que encontró el revisor, AFTER_* es cómo quedó y GEO_* / A_ / B_ / C_ / E_ / F_* son las mediciones.

## Punto por punto

| # | Punto | Resultado | N/HOJA | Imagen | Delta |
|---|---|---|---|---|---|
| 1 | C-H y MB-1 a 16" o.c. | **CARGADO**. RFI-16 cerrado por lo impreso. Pieces de C-H: un stick de 20 ft por stud de más de 10 ft | A0.06 GN 6 "ALL METAL STUDS TO BE SPACED @ 16" O.C. UNLESS NOTED OTHERWISE"; spec 09 21 16.23 3.1.A.1 | REV_rfi_F01_A0.06_GN6_16in_oc | C-H 2-1/2" +185.32 LF; C-H 6" +166.70 LF (CH.6 +44.88, MB-1 +121.82); Pieces 2-1/2" = MAX(LF, 86); Pieces 6" = MAX(LF, 62) |
| 2 | Duct chases 401 NE y 401/402 | **CARGADO**, como CLG-L4-405C (RS-1 + RC) | 1/A3.04, stipple de cielo dentro de los dos chases (densidad 7.1–7.2 marcas/SF, igual que los cielos cargados) | GEO_A3.04_duct_chases_stipple, AFTER_A3.04_duct_chases_loaded | +17.72 SF Type X (10.40 + 7.32), +13.29 LF RC |
| 3 | 2HR SHAFT CEILING | **CARGADO, supuesto conservador + RFI-29** (U-048). Ensamble = MB-1, la única membrana horizontal 2 HR impresa. El south shaft también: ninguna sección corta su base, se aplica IBC 2018 Section 713.11 item 1 | 1/A5.08 "2HR SHAFT CEILING"; 11/A9.03 (solo la plataforma); 8/A9.03 2'-3" × 4'-3 5/8" = 9.68 SF; 7/A9.03 3'-8" × 2'-0 1/8" = 7.37 SF | B_A5.08_1_2HR_SHAFT_CEILING, B_A9.03_8 / _7 / _11 | +51.15 SF Type X, +17.05 SF liner, +19.29 LF C-H 6", +15.93 LF J-runner |
| 3b | Detector U-137 | **ARREGLADO**. barrer() cortaba los hits a 60 / 12, ordenados alfabéticamente, y A5.08 quedaba fuera del corte. Ahora lista todos, por término. Compuerta nueva CB_CR_R15_BARRIDO con test | rfis.py | — | 0 |
| 4 | ELEC 221 / 321 / 421 a 2 HR | **REFUTADO con lo impreso**. Los code plans de cada piso dibujan los muros de los tres ELEC con línea 1HR FP; "2HR FB" solo rodea ELEC/TELE 120 (2/A0.01). El 118B es 2 HR por tu decisión (RFI-24). La alternativa 2 HR queda visible en RFI-04 | 3/A0.01 (221), 1/A0.02 (321), 2/A0.02 (421); A2.02 tag "W.62 \| 1" en 221 | A_A0.01_L2_ELEC221_1HR_FP, A_A0.02_L3_ELEC321_1HR_FP, A_A0.02_L4_ELEC421_1HR_FP, A_A0.01_L1_ELEC-TELE120_2HR_FB | 0 cargado; alternativa en RFI-04: +521.58 SF Type X + cara de 421 en W.6-L4-08 B |
| 5 | RFI-22 BAR | **DECIDIDO por R-ALC-10** (opción A, el dibujo específico manda). ALC-E08 ahora dice que el cielo del bar es la excepción | A0.00 "CORE AND SHELL ... SEPARATE PERMIT" vs A5.04 "BAR SUSPENDED GYP CEILING" + 3/A7.31 "SECTION - BAR CEILING" | F_A0.00_bar_core_and_shell, F_A5.04_..., F_A7.31_3_... | Opción B visible: −125.98 SF, −31.5 LF main tee, −94.49 LF cross tee, −88.2 LF angle, −8.29 LF hanger. El −121.6 de rev14 era el área anterior a rev9 |
| 6 | U-160: texto y polígono | **ARREGLADO**. 21 EXCLUDED, todos con polígono gris. El texto va dentro del cuarto: multi-línea y letra reducida en shafts, sin tapar notas impresas (410), sin línea de callout. CE_RCP_CUARTOS endurecida: ≥ 90 % del texto dentro, polígono obligatorio, sin /CL | A3.04, A7.45 (4/A7.45 RCP), A7.50 (2/A7.50 RCP), A3.01 | REV_rcp_F03_before → AFTER_A3.04_N_shafts_excluded, AFTER_A3.04_S_410_411_excluded, AFTER_A7.50_2_RCP_view, AFTER_A7.45_4_RCP_view | 0 |
| 7 | Cielos mal ubicados | **ARREGLADO**. (a) CLG-L2-56/58 y CLG-L3-87/88: el contorno ya estaba en coordenadas del RCP y se le sumaba otra vez el offset; ahora se dibujan sin él. (b) CLG-L1-14..18 y las ACT de 115/117/118B/119 pasan a 2/A7.50 ENLARGED RCP (dy −721.5 pt); 100/105 a 4/A7.45 (dy −727.1 pt); los offsets se midieron por voto de segmentos de muro. Compuerta nueva CE_RCP_CONTORNO: borde ≥ 60 % sobre las líneas del plano limpio y vista RCP | 1/A3.02, 1/A3.03, 2/A7.50, 4/A7.45 | GEO_CLG-L2-56_offset_fix …, GEO_A7.50_plan_to_rcp_view, AFTER_A3.02_CLG-L2-56_on_corridor | 0 (ubicación) |
| 8a | W.62-L4-02/03, cara del corridor | **CARGADO**. La cara x=853.6 es continua en el cruce DW.4 | A2.04 vectores | REV_walls_F01_…, AFTER_A2.04_W62-L4-02C_corridor_face | +16.07 SF Type X |
| 8b | XW.6.6 L4, cara exterior | **CARGADO**. 9 huecos cerrados en los cruces (corrida continua, como en L2 / L3) | A2.04 vectores | REV_walls_F02_…, AFTER_A2.04_XW66-L4-08A_09A_continuous | +5.77 LF, +58.98 SF exterior sheathing |
| 8c | W.6-L4-09 | **CARGADO**. Separado en dos caras: 421 x=1060.08 = 8.77 ft; corridor x=1070.16 = 9.89 ft. El markup va en cada cara | 3/A7.50 vectores | REV_walls_F05_…, AFTER_A7.50_W6-L4-09_two_faces | +11.45 SF Type X |
| 8d | Break 115 (W.6-L1-20/24/29/30/22/31) | **SIN CAMBIO** (el revisor lo marcó como duda). Es asignación, no cantidad: los muros W.6-L1-22 / -31 se miden de cara a cara pasando por el muro vertical, así que el área de la cara de Break 115 está en esos renglones. Neto ~0 | 1/A7.50 | REV_walls_F03 / F04 | 0 |
| 9 | RFI-17 | **CORREGIDO**. Delta −188.01 SF + grid. La opción A cita A0.01, que no dibuja FB en 128, y A8.00 128.1 "90 MIN" | A0.01, A8.00, A3.01 | — | texto |
| 10 | RFI-04 limpio | **CORREGIDO**. Se quitaron demising y lobby 217/317 (cerrados en rev14), igual que el rótulo "[TYPE ASSUMED]" de UNTYPED-L2-01/02 A/B/C y NULL-L3-01 | 3/A0.01, 1/A0.02 | — | 0 |
| 11 | Opción B = código | **CORREGIDO**. RFI-21 B: IBC 2018 Section 107.3.4.1 / 107.2.1. RFI-24 B: IBC 2018 Section 509.1 / Table 509 + 707.3. RFI-23: se quitó "refers to NFPA 70" | — | — | 0 |
| 12 | Spec 09 29 00 2.6.E | **PARCIAL**. CBU: **CARGADO**, mesh tape + setting compound por fabricante (2.6.E.3, 3.6.G). W.R.: **REFUTADO**. 2.6.E.1 es para W.R. usado como tile backer, y A0.06 GN 13 manda CBU en toda partición con tile, así que el W.R. no es tile backer | 09 29 00 2.6.E.1-3, 3.6.F-G; A0.06 GN 13 | — | +1,366.92 LF mesh tape, +266.00 LB setting compound |
| 13 | 118B / 120, alturas de capa | **CARGADO**. La 1ª capa de las caras 2 HR sube a 13.7917 ft, igual que la 2ª (IBC 2018 Section 707.5): renglones W.6-L1-20 D, -23 G, -23 H | 5/A5.04, S1.02 | — | +36.73 SF Type X |
| 14 | Cove 7/A7.23 | **DECIDIDO por R-ALC-01 / BE-CF11**. El legend GYP-1 dice "ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING", así que va metal. 7/A7.23 dibuja el símbolo de madera, sin texto. Se completó el soffit metálico: cripple studs 2-1/2" a 16" o.c. (GN 6) en todos los SOF | 7/A7.23, legend GYP-1 | C_A7.23_7_cove_framing | +664.97 LF 2-1/2" stud |
| 15 | Hanger wire | **CARGADO**. Los corridors toman el drop impreso de 9 1/2" de 7/A7.23 y la cantidad de hangers por área (antes se escalaba a 0.5 ft) | 7/A7.23 | C_A7.23_7_cove_framing | +36.54 LF |
| 16 | ALC-E12 | **CORREGIDO**. Cita S1.02 "L3x3x1/4 KICKER AT 4'-0" O.C.", 5/S3.08, S3.02, S3.04/06/08, S4.02 "CLIP ANGLE ... A36 THREADED RODS" = structural steel (Div. 05, structural steel) | S1.02, 5/S3.08 | E_S1.02_kicker, E_S3.08_5_kicker | 0 |
| 17 | Cajas de closet L2 / L3 | **CARGADO** unidad por unidad. 24 cajas con stipple: 201–214 y 305–314. Las 301–304 ya estaban cubiertas por RS6-L3. La caja NW de A7.45 cita ahora 1/A3.01: está fuera del edificio y A3.01 no la dibuja | 1/A3.02, 1/A3.03, 1/A2.01 | F06_chase_boxes_A3.02 / _A3.03 (+ detalles), AFTER_A3.02_201C_closet_loaded, GEO_A7.45_NW_box | +168.92 SF Type C, +126.72 LF RC |
| 18 | GUIA | **ARREGLADO**. Abre con "CAMBIOS rev15 vs rev14". Compuerta nueva guia_cambios_fallas con test | GUIA_DE_REVISION_DEL_ESTIMADOR.md | — | 0 |

## Delta total por material, rev14 → rev15 (NET)

| Material | Unit | rev14 | rev15 | Delta |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 87,517.65 | 87,650.77 | +133.12 |
| 5/8" gypsum board, Type C (ceiling) | SF | 21,600.06 | 21,768.98 | +168.92 |
| 5/8" exterior gypsum sheathing, Type X | SF | 18,193.73 | 18,252.71 | +58.98 |
| 1" gypsum shaftliner panel | SF | 1,371.66 | 1,388.71 | +17.05 |
| C-H stud 2-1/2" 20 GA | LF | 620.81 | 806.13 | +185.32 |
| C-H stud 6" 20 GA | LF | 577.14 | 763.13 | +185.99 |
| J-runner 6" | LF | 139.78 | 155.71 | +15.93 |
| 2-1/2" stud (soffit cripples) | LF | 0.00 | 664.97 | +664.97 |
| Resilient channel | LF | 19,551.54 | 19,691.55 | +140.01 |
| Hanger wire | LF | 483.40 | 519.94 | +36.54 |
| Joint compound, all purpose | LB | 8,469.39 | 8,491.14 | +21.75 |
| Joint tape, paper | LF | 50,760.75 | 50,872.50 | +111.75 |
| Alkali-resistant mesh tape (CBU) | LF | 0.00 | 1,366.92 | +1,366.92 |
| Setting-type joint compound (CBU) | LB | 0.00 | 266.00 | +266.00 |

Cómo cuadra el Type X (+133.12 SF) [DERIVADO]:
- Walls: +16.07 + 11.45 + 36.73 = +64.25 SF.
- Duct chases: +17.72 SF.
- Shaft ceilings: +51.15 SF.

## RFI abiertos

- **RFI-04:**
  - Tipo de los plumbing furring.
  - Chase L4 X-L4-02/03/04/05.
  - Janitor 109 y nichos.
  - ELEC 221/321/421 contra A0.00 (alternativa 2 HR +521.58 SF).
- **RFI-13:** tamaño del stud y C-channel de MB-1. El espaciado ya está resuelto: 16".
- **RFI-17:** cielo de 128.
- **RFI-29 (nuevo):** ensamble del 2HR shaft ceiling.
- **RFI-21 y RFI-24:** siguen siendo tu decisión (U-052).
