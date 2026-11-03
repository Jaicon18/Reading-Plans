# Tool fixes and tool limits - stages 4-9 (Harbor Freight Tools - Loveland, CO, skill v81cf18)

Originals of every modified tool kept in scratchpad/skill_originales_hft/; each fix has its test (fails on the original).

## Fixes made in the tool (with test)
| Id | Tool | Problem | Fix | Test |
|---|---|---|---|---|
| BE-HF1 (BE-CF15 line) | canon.py STUD_FAM + nombres_contexto.z_kind; plantilla_excel.nombre_plantilla + track-row skip; trazabilidad.py breakdown | No hat-channel family: type E "1-1/2\" METAL HAT CHANNEL @ 24\" O.C. MOUNTED VERTICALLY" (E/A4.1) was labelled "1-1/2\" Z-furring channel" in the Material Summary | "hat channel" in stud_size -> vertical-furring family (pieces by O.C., no runner rows); Excel label = "1-1/2\" metal hat channel, vertical furring (LF of material)"; Z-furring sets unchanged | test_hat_channel_label.py |
| BE-HF2 | canon.py MISC_ALIAS | misc_items.familia written with the Excel product name ("FRP panels") stopped canon.py | alias -> family "FRP" (Excel row "FRP panels") | test_frp_misc_alias.py |
| BE-HF3 (CFA TOOL_LIMITS #8) | canon.py furring_sin_bracing | C.R. channel bracing rows generated on vertical furring fastened to masonry (type E) | furring family without declared bracing_rows -> 0 rows with source; declared rows still win | test_furring_no_bracing.py |
| BE-HF4 | vigas_sobre_walls.py --min-size | grid-bubble label size fixed at >= 14 pt | option --min-size (default 14) | test_vigas_min_size.py |
| BE-HF5 | reglas.py A_BRACING (53.4) | check used a fixed 48" spacing; the set prints CRC @ 8'-0" (A4.1 note 7) used by canon.py | printed constants.bracing_spacing_in, 48" by default | test_bracing_spacing_regla.py |
| BE-HF6 | reglas.py A_HEADER_LF (E1) | box beams / box headers drawn in a detail and carried as misc_items (S2.1 BB-1, 2/A5.3, 8/A5.3) were not in the E1 sum | misc_items of the header / box beam family added | test_header_misc_regla.py |
| BE-HF6b | trazabilidad.py header breakdown | same defect in the Material Summary breakdown ("desglose suma != NET", no Excel) | misc box beams listed in the header row breakdown | test_header_misc_regla.py |
| BE-HF7 | trazabilidad.py tamano_stud | per-size track breakdown compared stud_size by exact text: '6" (600S162-54)' (receiving enclosure) dropped -> no Excel | leading printed size compared, same rule as canon.track_by_element | test_track_size_designacion.py |
| BE-HF8 | trazabilidad.py citation | rows whose items cite only a bare sheet (A4.1 note 5 corner beads, window sill 5/A5.1) got "N/SHEET: default (no sheet)" -> verificar rejected the Excel | bare sheets of the item / family-row / headers sill sources | test_cita_hoja_suelta.py |
| BE-HF1b | familias.py | the new hat-channel label was not read back as its family (reglas R80.4 "family without row") | label pattern added to the vertical-furring family | test_hat_channel_label.py |
| BE-HF9 | markups_bluebeam.py board_sf | wall declared without gypsum (faces_none_reason: enclosure CFS walls, plywood by others) had LF x H SF in its markup vs 0 SF board in the Excel (BE-117 FAIL) | 0 SF board for such walls | test_markup_sin_board.py |
| BE-HF10 | auditoria_entrega.py | (a) "Pending Items empty" failed every delivery with open RFIs (this brief requires them, options A/B/C + conservative value); (b) drawn length vs LF ignored the cause written on the canon element (verificar_markups_excel accepts it) | --rfis-abiertos: each open RFI must carry (A)/(B)/(C) + delta; length_cause / area_cause / measure_cause / markup_cause honoured | test_auditoria_rfis_causa.py |

| BE-HF11 (rev2 F3) | canon.py track_by_element | a head element (vestibule bulkhead) always went to the "roof step and heads" track row, even with a slip head (3/A5.3) | a head carried as a Partition Takeoff row goes by size / kind: slip 3-5/8" row | test_braces_rows_rev2.py |
| BE-HF12 (rev2 F1) | canon.py braces_to_structure, families "metal stud brace to structure" / "spacing bar at the brace line"; plantilla_excel names + purchase class; familias.py | printed bracing of the wall top to structure (A1.1 note 1, 2/A4.1) had no family -> 0 | pcs = ROUNDUP(L x 12 / spacing) + 1 per wall with unsheathed studs above the board; brace length = printed B.O. structure - top of board (conservative); bar LF = wall LF; printed product labels | test_braces_rows_rev2.py |
| BE-HF13 (rev2 F4) | canon.py bracing_min_altura; trazabilidad.py bracing text | C.R. bracing generated on 8'-6" walls although A4.1 note 7 = partitions higher than 12'-0"; breakdown text said "/ 48" while 96" was used | constants.bracing_min_height_ft; text with the spacing used | test_braces_rows_rev2.py |
| BE-HF14 (rev2 F6 / O2) | partition_types.py (partition_row_rule "wall_id", partition_row typed element BULKHEAD-<tag>); markups_bluebeam.tipo | joined rows A-14+A-12+A-13 / C-01+C-02 did not match the per-wall markups; bulkhead rows below the GRAND TOTAL | one row per wall id; the vestibule bulkhead as type BULKHEAD-VH inside the grand total | test_braces_rows_rev2.py |
| BE-HF15 (rev2 O5) | markups_demo.py | demo contents said "2 layer(s)" for 2 faces x 1 layer | label from layers_info ("2 faces x 1 layer") | test_braces_rows_rev2.py |
| BE-HF16 (rev2 F5 / OBS-6) | trazabilidad.py | sill track row without breakdown; breakdown totals off NET by rounding without a note | per-opening sill breakdown (headers.py); "difference = rounding of the items" note | test_braces_rows_rev2.py |
| BE-HF17 | markups_bluebeam.py legend page | legend page sorted alphabetically | schedule order (constants.type_order) | test_braces_rows_rev2.py |

## Limits documented (not bypassed)
1. vigas_sobre_walls.py S2.0 vs A1.1: even with --min-size the only small labels found are title-block numbers; the grid bubbles of this set are drawn as vector letters (no text) -> "1 grid comun", not registrable. Run of record `vigas_sobre_walls.py ... NONE A1.1@p8` (rc 0, 0 beams). Its printed message "the bid set index has no structural (S) sheet" is the tool's generic text and is NOT true here: S1.0-S4.1 exist. Walls to deck carry slip track 10/A4.1 (D) or the A/A4.1 standard track at the existing deck; no beam stop is printed on A4.1 / S2.0 for our walls.
2. mep.py M1.0 / M1.1 / M1.2 vs A1.1: registration ok False (< 25 votes) -> declared mep_sweep.registro.no_usable (ducts EXCLUDED by standing order; no quantity depends on it).
3. (rev2: fixed by BE-HF13) C.R. bracing only on walls higher than 12'-0" (A4.1 note 7).
4. (rev2: fixed by BE-HF12) Bracing to structure carried: 50 braces / 412.5 LF 6" x 20 GA + 125.97 LF Spazzer 9200 bar; brace length RFI-05.
5. Face sides R72.6: the readings wrote room words ("HFT side", "Inside", "Room"); scripts/formato_canon.py sets A / B by program from the printed room numbers / names (side_info on each face).
6. Corners R70.2: esquinas.py found corner squares without owner (D-03/A-04, B-01/A-03, C-01/A-03, C-01/C-02, B-02/A-07, B-03/A-07): the thicker wall is extended by the measured gap (formato_canon.py, length_op written); double corners of printed lengths / boundary studs / two-face furring declared in corners_ok; fountain alcove gap A-10/A-14 in gaps_ok.
7. bitacora / reglas compuerta final mode fail ONLY for the separate back-check (done by another session).
8. Deflection track label "2\" deflection leg": 10/A4.1 does not print the leg; the canon has no top_track_leg -> tool default 2" (BE-117c). Estimator to confirm the leg of the 20 GA deflection track.
9. auditoria_entrega.py was run with --rfis-abiertos (4 open RFIs in Pending Items, each with options A / B / C and delta, conservative value loaded).
10. Tool suite (correr_suite.py --skill): 61/61 OK after the rev2 fixes (test_ciego_tools OK, 0 findings).
