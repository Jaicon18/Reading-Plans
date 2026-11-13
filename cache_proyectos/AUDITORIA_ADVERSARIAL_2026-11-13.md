# AUDITORÍA ADVERSARIAL U-138 — 2026-11-13 (revisor independiente, no hizo el take-off)

Alcance: Xfinity Interquest rev1c (bid HOY) + muestra Grand Kia rev3b + barrido_drive.py 230.
Modo: solo lectura en Drive (nada renombrado, nada borrado). Recortes de evidencia en
`cache_proyectos/xfinity_interquest/auditoria_2026-11-13/` (rendereados del bid set original
"Xfinity BP_Colorado Springs, CO_Interquest_Complete PDF Set_10-08-26_R0.pdf", md5 b4375092…, escala impresa 1/4" = 1'-0" = 18 pt/ft).

## 0. Archivo auditado = archivo entregado (U-177)
- Drive › Claude outputs › Xfinity - Interquest… › rev1 FINAL PARA REVISAR › Take-off › `XF_Takeoff_FINAL_rev1.xlsx` sha256 da556116… = ENTREGA_OK.json **OK**.
- Planos marcados › `XF_markups_rev1c - OPEN IN BLUEBEAM.pdf` sha256 6b06f37f… = ENTREGA_OK.json **OK**.

## 1. ENTREGA_OK.json (Xfinity) — chequeos en PASS con conteo 0 / implausible
Resumen: 226 PASS / 9 AMBER / 0 FAIL, compuerta **v81cf114** (12-nov 07:02 PST). Todas marcadas plausibilidad "OK" por auditar_compuerta.

| # | Chequeo | Estado | Hallazgo |
|---|---|---|---|
| I-1 | **CB_RCP_TAGS** | PASS "N/A: ninguna hoja de RCP con tags de cielo impresos" | **IMPLAUSIBLE (detector ciego, U-137).** A3.0 (1/A3.0 RCP) imprime 6 tags de cielo en caja: "2x4 ACT 12'-0" AFF" (Retail 100), "2x4 ACT 10'-0" AFF" (Storage 101), "GYP. BD. 8'-6" AFF" (nuevo), "EXISTING GYP. BD. 9'-0" AFF" (Hallway 102, Toilet 103, Toilet 104). Evidencia: `XF_A3.0_storage_hall_rcp.png`. Las cantidades no cambian (el 8'-6" ya está como SOF-01 y el ACT es de otro trade), pero el chequeo pasó en vacío. |
| I-2 | **CB_RCP_APILADOS** | PASS "N/A: sin rcp_tags" | Implausible por arrastre de I-1 (depende de rcp_tags vacío). |
| I-3 | **CE_DOBLE_CIELO** (REGLA DE ORO #3) | AMBER "entrega anterior a U-190, no se re-abre" | Falta `Auditoria/DOBLE_CIELO.csv`. La Regla de Oro #3 dice "falta = NO se entrega"; la entrega se queda con AMBER por U-180 (4). En este set no veo doble cielo (ACT sobre retail/storage, GYP existente en hallway/toilets, sin membrana rated), así que el impacto en cantidades es 0. Hacer la tabla toma 5 min; recomendable antes del bid. |
| I-4 | CB_BE_CF10 | PASS "el set no trae specs del trade" | Dudoso: A0.3 SPECIFICATIONS existe (el propio LEEME lo dice). Revisar si A0.3 tiene párrafos Div. 09 que se debieran citar. Sin impacto de cantidad detectado. |
| I-5 | Versión | — | La compuerta corrió con **v81cf114**; la vigente es **v81cf138**. U-177 (1): "si la compuerta no corrió con la versión vigente… la entrega NO está en verde". Antes del bid: re-correr la compuerta vigente (modo verificación) o dejar escrito que U-180 (4) aplica. |
| — | AMBER restantes (CE_PROPOSAL U-192 "[RATE TO CONFIRM]" en corner bead, CE_TIEMPOS 1166 % sin causa, CE_CAMPOS_CANON, CE_ALTURAS_EXTREMO SOF-01 sin side/faces, CE_PROTOCOLO_3H, CB_U_191_REF GA-216 sin párrafo, CB_DETALLE_CARAS, CB_BE_CR22_VANOS) | AMBER | Todos "no se re-abre (U-180 (4))". **CE_PROPOSAL sí toca el bid de hoy**: la Proposal tiene `[RATE TO CONFIRM]` en "Corner bead and L bead install" (fila 30) que U-192 (3) ya decidió (incluido en taping). |

Los demás N/A revisados (CB_PUERTA_RATING, CB_R_ALC_04, CB_BE_16, CB_U_174_VALOR, etc.) son coherentes con un TI de 1,798 SF con 4 walls nuevos.

## 2. Muestra al azar contra el plano (Xfinity)
El proyecto tiene solo 4 walls + 1 soffit, así que la muestra de "5 walls" los cubre todos.

### Walls (largo, altura, board por cara, BOTH SIDES)
| Wall | Excel | Plano (N/HOJA) | Resultado |
|---|---|---|---|
| W2-01 | 13.973 LF; H 12.5; caras Retail 12.5 / Storage 10.5; board 321.38 SF | Vector del muro 1297.56→1489.08 pt = 10.640 ft + door 3'-0" + 4" impresos (A2.0, 1/A2.0) = 13.973 [DERIVED]; type W2 "5/8" TYPE 'X' GYP. BD. BOTH SIDES OVER 3-5/8" METAL STUDS FROM SLAB TO 6" ABOVE CEILING" (A2.0 wall types); C.H. Retail 12'-0", Storage 10'-0" (1/A3.0) → 12.5 / 10.5; 13.973 × (12.5+10.5) = 321.38 | **CONFIRMED** (`XF_A2.0_W2_crop.png`, `XF_A3.0_storage_hall_rcp.png`) |
| W2-02 | 4.00 LF; caras Retail 12.5 / Hallway 9.5; 88 SF | Cota impresa 4'-0" (A2.0, ticks 1506.96/1578.96 = 72 pt = 4.000 ft); Hallway "EXISTING GYP. BD. 9'-0" AFF" (1/A3.0) → 9.5 | **CONFIRMED** |
| CF-01 / CF-02 | 2.38 LF c/u, 1 cara, H 12.5, 29.75 SF c/u; 250S125-43 | 5/A2.0 "5/8" TYPE 'X' GYP. BD. ONE SIDE OVER 2 1/2" METAL STUDS (TYP. ALL SIDES)"; key note A2.0 "COLUMNS TO BE FURRED… (1) LAYER 5/8" GYP. BOARD TO 6" ABOVE CEILING"; tabla de limiting heights A2.0: 250S125-33 @16 = 12'-0" < 12'-6", 250S125-43 @16 = 13'-0" ≥ 12'-6" | **CONFIRMED** (`XF_5A2.0_column_furring.png`, `XF_A2.0_CF_plan.png`). Nota: el furring dibujado en planta es muy chico (≈ 11" × 9"); es lo dibujado, no hay cota. |
| SOF-01 | 4.25 LF × 3.407 = 14.47 SF a 8'-6" | Tag "GYP. BD. 8'-6" AFF" en 1/A3.0 **sin** la palabra EXISTING (los de 9'-0" sí la llevan) → es nuevo, se carga | **CONFIRMED** |
| Markups | W2-01 Depth 12.5, 13.97 LF, 321.38 SF; W2-02 4.00 LF; CF 6 segmentos 0.72/0.72/0.94; SOF-01 Depth 3.407 | = Excel | **CONFIRMED** |

### Burbujas de detalle (3 + 1)
| Burbuja | Lo que se cargó | Resultado |
|---|---|---|
| 4/A2.0 TYPICAL WALL AND CEILING DETAIL | Wall a 6" sobre el cielo, top track estándar (sin slip track), braces "METAL STUDS AT 8'-0" O.C. MAX… 3 5/8" 20 GA. MIN… MAXIMUM LENGTH OF BRACE 25'-0""; braces 3 + 2 = 5 × (26 − 12.5) × √2 = 5 × 19.09 = 95.46 LF | **CONFIRMED** (`XF_4A2.0_wall_ceiling.png`; 26 FT de A0.1 "HEIGHT IN STORIES: 1 STORY - 26 FT" = RFI-01 U-174) |
| 5/A2.0 NON-RATED COLUMN FURRING | 2-1/2" studs, 1 capa 5/8" X, "FINISH CORNER 'L' BEAD" → 100 LF edge trim | **CONFIRMED** |
| 8/A2.0 BACKING DETAIL FOR MISC. EQUIP. | "16 GA. METAL STUD 16" O.C. @ ALL BACKING STUD TRACKS" + "16 GA. X 6" X 1-1/2" UNPUNCHED METAL TRACK" | Texto **CONFIRMED** (`XF_8A2.0_backing.png`); ver hallazgo E-1 sobre cómo se cargó |
| 7/A2.0 TYPICAL HEAD DETAIL (JAMB SIM) | Header door 101 = 8.67 LF todo como 362T125-33 | Ver hallazgo E-2 (`XF_7A2.0_head.png`) |

### RFIs (2)
| RFI | Resultado |
|---|---|
| RFI-01 (cerrado, U-174, 26'-0") | **CONFIRMED**: A0.1 imprime "HEIGHT IN STORIES: 1 STORY - 26 FT"; ninguna sección / elevación de estructura en el set (A0.1–A5.0, E/M/P); el delta por pie (−7.07 LF braces, −75.71 SF demo) cuadra con 5 braces × 1.414. |
| RFI-06 (PENDING - user manual verification) | **CONFIRMED** el texto base: A2.0 WALL TYPE 1 "EXISTING DEMISING/EXTERIOR WALL TO REMAIN PATCH AND REPAIR AND MAINTAIN ANY EXISTING FIRE RATING (V.I.F.)", WALL TYPE 4 "INTERIOR WALL TO REMAIN. PATCH AND REPAIR…", A0.1 nota 3 "WHERE OCCURS, CONTRACTOR SHALL PATCH ANY EXISTING WALLS AND/OR CEILINGS AS NEEDED…". Aritmética de muestra PR-W1-01 63.36 × 12.5 = 792.0 OK. Observación: la nota 3 dice también "CEILINGS" (hallway/toilets GYP existentes 9'-0"); el RFI-06 solo cubre walls → vale la pena una línea en el Scope ("ceiling patch: allowance / by field"). |

### Renglones del Material Summary (3 + extras)
| Renglón | Resultado |
|---|---|
| Fila 13 — 5/8" Type X 3,072.97 SF | **CONFIRMED** = 321.38 + 88 + 29.75 × 2 + 14.47 (SOF-01) + 2,589.62 (PR-*, RFI-06 A). |
| Fila 19 — Brace 362S125-33 95.46 LF | **CONFIRMED** (4/A2.0). |
| Fila 6 — Top track 362T125-33 17.97 LF | **CONFIRMED** = 13.97 + 4.00 (wall a 6" sobre cielo = track estándar, U-056). |
| Fila 10 — 362S162-54 125 LF | **MISMATCH (E-1)**. |
| Fila 12 — Header 362T125-33 8.67 LF | **MISMATCH menor (E-2)**. |

## 3. Errores encontrados (Xfinity rev1c)
- **E-1 (8/A2.0, A4.0 GF-14496) — doble conteo de studs en la zona de backing.** 8/A2.0 dice que los studs de la zona de backing SON de 16 ga ("16 GA. METAL STUD 16" O.C. @ ALL BACKING STUD TRACKS"), o sea reemplazan a los de 20 ga en esas bahías. El canon (STUD16-GF) agrega 10 studs × 12.5 = 125 LF de 362S162-54 y deja los mismos studs de 20 ga en el renglón W2 ("conservative: the 20 ga studs of the same bays stay in the W2 row; delta −125.0 LF of 20 ga if replaced"). Sobra ≈ 125 LF de 362S125-33 en la fila 9 (250.67 → ≈ 125.67). Es conservador y la nota tiene el delta, pero no tiene RFI ni decisión escrita (U-116 / U-052: lo impreso manda). Evidencia: `XF_8A2.0_backing.png`.
- **E-2 (7/A2.0) — nombre / designación del header.** 7/A2.0 imprime "3-5/8" METAL TRACK" + "3-5/8" METAL STUD NESTED IN METAL TRACK". La fila 12 carga las 2 piezas (8.67 LF) como 362T125-33 (track). Debería ser 4.33 LF de 362T125-33 + 4.33 LF de 362S125-33 (U-177 (4): producto = impreso). Impacto mínimo. Evidencia: `XF_7A2.0_head.png`.
- **E-3 (Proposal, U-192 (3))** — `[RATE TO CONFIRM]` en "Corner bead and L bead install" ya decidido por el usuario (incluido en taping). Toca el bid de hoy (CE_PROPOSAL AMBER).
- **E-4 (proceso, U-177 (1))** — ENTREGA_OK de v81cf114 vs vigente v81cf138; CB_RCP_TAGS ciego (I-1); falta DOBLE_CIELO.csv (I-3).

Sin errores de largo, altura, caras ni BOTH SIDES en los 4 walls + SOF-01.

## 4. Grand Kia rev3b (muestra parcial)
- El `cache_proyectos/grand_kia/ENTREGA_OK.json` de la raíz es el de **rev2** (v81cf94, 11-nov); el VERDE de rev3b (v81cf129, corrida 60914f5fc798) solo está en `compuerta_corridas_rev3b.jsonl`, y la re-corrida con v81cf130 salió **ROJA** (FAIL CE_VERSION_ENTREGA y CE_PROTOCOLO_3H, ambas de proceso, no de cantidades) — `ENTREGA_OK_rev3b_v130_ROJA_post_subida.json`. Recomendación: que el caché tenga un ENTREGA_OK que corresponda a la rev vigente.
- Canon rev3b del caché sha256 1ab5af2c… = hash entregado (LEEME) OK.
- Muestra de 2 walls (A1-Z2-03 A111, 8'-0" de 2/A150; A1-Z3-01 A112, 11'-3 1/2" de 3/A150): **NO VERIFICADO**. El set de Drive "Grand Kia - Current Drawing Set.pdf" (112 págs., sin capa de texto) no corresponde en página / coordenadas al `GK_set_OCR.pdf` que usó la sesión (las bandas del canon caen en zonas vacías de la página 9 / 10). No quise dar por buena una lectura sin mapear el set; queda pendiente y de todos modos la rev nueva por Addendum #2 debe repetirse.
- MS row: no verificado (mismo motivo).

## 5. TAREA B — barrido_drive.py 230 (13-nov, solo lectura, nada renombrado)
Nota: la primera corrida con `timeout 900` se cortó (rc 124, recorre todo Claude outputs incl. carpetas BORRAR, ~20 min); la segunda terminó: **219 rutas > 230, 18 > 260, 0 con caracteres prohibidos**. Salida: `scratchpad/aud/largos.json` (no se sube).
- **Xfinity, Grand Kia, CR City Hotel: 0 rutas vigentes > 230.** Las 3 de Xfinity > 260 están dentro de carpetas/archivos "BORRAR (NO USAR)".
- **Rutas > 260 en entregas VIGENTES (sin BORRAR): 0.** Las 18 > 260 son: Chuze 11, CFA 4, Xfinity 3, todas bajo BORRAR.
- **Vigentes 231–260 (abren en Windows, pero pasan el límite de 230 de U-165) — 65:**
  - Consumer Cellular rev4 FINAL (6): `Take-off/…Takeoff_FINAL_rev4.xlsx.sello.json` 247, `Proposal/…Proposal_rev4b_PROPOSAL.pdf` 240, `…rev4_PROPOSAL.pdf` 239, `Take-off/…Takeoff_FINAL_rev4.xlsx` 236, `…Proposal_rev4b.xlsx` 232, `…Proposal_rev4.xlsx` 231. Causa: nombre de carpeta "rev4 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR" (49 chars).
  - Chick-fil-A #2284 rev10 FINAL (6): 4 PNG `A-xxx_CFA2284_RiverPoint_marked_by_type_rev10.png` 235, `…Takeoff_FINAL_rev10.xlsx.sello.json` 233, `CFA2284_RiverPoint_Markups_Bluebeam_rev10.pdf` 231. Misma causa de carpeta. (Además los PNG no siguen U-158 "IMAGE ONLY" y el PDF no dice "OPEN IN BLUEBEAM", fuera del alcance del barrido.)
  - Barnes & Noble (51) y BOA (2): carpetas viejas sin prefijo BORRAR; U-089 dice que ya no se revisan, pero U-186 pediría marcar las revs reemplazadas (rev1..rev12) con BORRAR. Máximo 256 (< 260).
- No se renombró nada (orden de la tarea).
