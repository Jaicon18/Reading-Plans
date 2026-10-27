# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev7

rev7 = rev6 plus the second independent review (Paso 12) applied.
- Sources: `../PASO12_rev6/CERTIFICADO_PASO12.md`, `MATRIZ_COBERTURA.xlsx` (471 items) and `../../BIBLIOTECA_ERRORES.md`.
- Rule v80j: every item is resolved from the drawings; anything not printed is an RFI with a conservative assumption and its delta. Estimator precedents from `DECISIONES_ESTIMADOR.md` are applied.
- Earlier revisions are unchanged. There is no wall geometry change, so A-101 / A-221 images stay as in rev5. The markups PDF is regenerated (Contents carry the rev7 SF).
- New evidence for C-07 (bubble 3 = Top Track Detail, 8 = Typ. Connection) is in `../rev7_evidencia/`. All other evidence crops are in `../PASO12_rev6/img/`.

## 9 CORREGIR — applied
| ID | Correction |
|---|---|
| C-01 | T.O. WD-1 at the Grab & Go header = 15'-0" (5/A-226A, 6/A-226A): + 61.67 SF 5/8" Type X over the plywood to deck; RFI-34 closed |
| C-02 | RFI-13: FRP-1 heights printed (Work Room 10'-0" on 1-4/A-226B; Janitor 96" on A-131 / 8'-0" on A-200); delta 1,030.64 SF; installer still open |
| C-03 | 22/A-201 5/8" cement board base 1'-2" on the restroom faces of new walls: + 50.04 SF cement board, - 50.04 SF W.R. |
| C-04 | C-E1-S cement board on the 19'-0" HOLD exposed face: 586.5 → 475.0 SF |
| C-05 | ALC-24 = QUANTIFIED, Level 4 (A-001A Div 09 A.8) |
| C-06 | Vestibule box members cite 7/A-210 and 8/A-210 (6/A-210 = glazing base) |
| C-07 | Top Track Detail = **3/A-410** (bubble read at 300 dpi; the type 2 head points to 3/A-410); 8/A-410 = Typ. Connection. All citations corrected |
| C-08 | Stud reinforcement at MEP: "skill default (not printed)"; 6/A-410 and 7/A-410 are pipe firestopping only |
| C-09 | Door 4 is in W2-04 (labels corrected; the opening and its jambs were already in W2-04) |

## Changes (rev6 → rev7), Material Summary Net
| Material | Unit | rev6 | rev7 | Δ |
|---|---|---|---|---|
| 6" metal stud (LF of material) | LF | 3,007.50 | 3,162.50 | +155.00 |
| 3-5/8" metal stud (LF of material) | LF | 10,788.75 | 11,479.27 | +690.52 |
| 1-5/8" metal stud (LF of material) | LF | 0.00 | 131.42 | +131.42 |
| Track, ceilings / soffits / canopy | LF | 598.32 | 618.81 | +20.49 |
| Furring channel (ceilings) | LF | 182.79 | 207.45 | +24.66 |
| Carrying channel (ceilings) | LF | 146.92 | 159.16 | +12.24 |
| Hanger wire | LF | 1,438.00 | 2,689.79 | +1,251.79 |
| Blocking FRT / 2X FRT wood | LF | 552.27 | 568.27 | +16.00 |
| 5/8" gypsum board, Type X | SF | 14,902.61 | 15,109.29 | +206.68 |
| 5/8" gypsum board, Type X W.R. (water resistant) | SF | 1,142.63 | 1,092.59 | -50.04 |
| Clip angle 16 ga (5/A-410 bracing clips + 7/A-210 nested header clips) | PCS | 0.00 | 2,522.00 | +2,522.00 |
| X-EDNI fasteners 0.145" (Hilti), top track to structure (A-410 note 8.C) | PCS | 0.00 | 720.00 | +720.00 |
| Plywood screws #10-24 x 1-1/4" Teks/3 (A-410 note 8.D) | PCS | 0.00 | 2,331.00 | +2,331.00 |
| Cement board screws 1-1/4" (manufacturer spacing) | PCS | 0.00 | 1,686.00 | +1,686.00 |
| Nested inner runner at the deflection head (3/A-410) | LF | 0.00 | 479.85 | +479.85 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim | LF | 891.72 | 957.03 | +65.31 |
| Cement board (tile / FRP substrate) | SF | 851.40 | 789.94 | -61.46 |
| Blocking 2X wood (not labeled FRT) | LF | 0.00 | 17.00 | +17.00 |
| FRT plywood substrate (5/8 in.) | SF | 1,886.46 | 1,790.51 | -95.95 |
| FRT plywood substrate (3/4 in.) | SF | 370.46 | 402.46 | +32.00 |
| Hanger wire 12 ga - hanger count (one per hanger, height per room) | PCS | 103.00 | 109.00 | +6.00 |
| Drywall screws 1-1/4" bugle head | PCS | 19,254.29 | 19,442.26 | +187.97 |
| Joint compound, all purpose | LB | 1,155.26 | 1,166.54 | +11.28 |
| Joint tape, paper | LF | 5,936.74 | 5,994.70 | +57.96 |

Partitions total: no change, **569.82 LF**. Gauges per row (A-410 Metal Stud Schedule):
- type 2 and the Cafe 3-5/8" walls to deck: 14 ga SJ;
- 6" walls to deck: 20 ga SJ;
- all other walls: 20 ga.

## 57 matrix rows (47 GAP + 10 CORREGIR) → destination
| Matrix # | Item | Destination in rev7 |
|---|---|---|
| 7 | A-001A Div 05 D Unistrut space frame | EXCLUDED - Scope ALC-X41 (lighting / MEP / sign supports by those trades) |
| 20 | A-001A Div 09 A.8 Level 4 (C-05) | ALC-24 = QUANTIFIED, Level 4 printed |
| 48 | A-002 Acoustical ceiling system | EXCLUDED - ALC-X40 (Div 09 51, ACT contractor) |
| 51 | A-002 Cafe signage strut channel | EXCLUDED - ALC-X41; sign blocking carried (4/A-226A) |
| 53 | A-002 Div 10 seismic bracing | EXCLUDED as a separate item - ALC-X43; ceiling bracing carried (RFI-38) |
| 54 | A-002 FE cabinets | Row FRT blocking BLK-FE-CABINETS 16 LF + RFI-39 |
| 61 | A-101 GN 8 caulk at base of wet walls | EXCLUDED - ALC-X42 (sealant, standing order) |
| 74 | A-101 C11 FE cabinets | = #54 (row + RFI-39) |
| 110 | 4/A-101 FRT wood header + base | = #54 (row + RFI-39) |
| 115 | A-111 KN 9 FE cabinets | = #54 (duplicate) |
| 143 | 5/A-121 16 ga tie wire | Scope ALC-12 note: consumable of the furring / carrying install |
| 145 | 5/A-121 hangers at light fixtures | Row Hanger wire + 401.0 LF (29 hangers) |
| 147 | 5/A-121 seismic splay wires (A-420 not in set) | Rows Hanger wire + 743.29 LF, 1-5/8" stud 131.42 LF + RFI-38 |
| 148 | 5/A-121 ACT grid portion | EXCLUDED - ALC-X40 |
| 149 | A-121 ACT ceiling tags | EXCLUDED - ALC-X40 |
| 154 | A-121 Grab & Go GWB 7'-1" | Ceiling 25.16 SF Type X + furring / carrying / hangers / perimeter track |
| 170 | A-131 Janitor FRP-1 96" (C-02) | RFI-13 corrected (heights printed; installer open) |
| 191 | 22/A-201 cement board base 1'-2" (C-03) | Row Cement board + 50.04 SF; Type X W.R. - 50.04 SF; RFI-12 closed (base) |
| 199 | 2/A-210 vestibule fascia band | Row Type X VEST-GWB-BANDS (+1.63 of 14.96 SF) |
| 200 | 3/A-210 vestibule side bands | Row Type X VEST-GWB-BANDS (+13.33 of 14.96 SF) |
| 203 | 6/A-210 citation (C-06) | Citations to 7/A-210 and 8/A-210 |
| 204 | 7/A-210 clip angles 3x3x16 ga | Row Clip angle 4 pcs + RFI-51 |
| 225 | 1/A-221 19'-0" HOLD C-E1-S (C-04) | Cement board 475.0 SF (- 111.5) |
| 226 | 1/A-221 H2a pier void | RFI-45 (- 66.7 SF if concealed) |
| 230 | E/A-221 E1 / E2 board height | E2 FRT to ACT-1 + 6" = 10.5 ft (- 424.85 SF); E1 = RFI-43 |
| 232 | F/A-221 nested stud bracing | Row 3-5/8" stud + 6.52 LF + RFI-46 |
| 237 | H/A-221 H3a plywood to T.O. WD-1 | RFI-44 |
| 238 | H/A-221 H3b above 8'-0" | Row Type X + 104.89 SF (A-410 Partition Notes 2) |
| 246 | 2/A-221 plywood above T.O. WD-1 | FRT plywood SS-N / SS-E to deck + 328.9 SF |
| 247 | 2/A-221 cross bracing AS REQ'D | Row 3-5/8" stud + 90.0 LF + RFI-42 |
| 260 | 3/A-225 Workroom substrate conflict | RFI-13 text (substrate conflict) |
| 262 | 5/A-225 marine plywood | RFI-47 |
| 266 | 10/A-225 1/2" FRT plywood | RFI-47 |
| 279 | 5,6/A-226A T.O. WD-1 15'-0" (C-01) | RFI-34 closed; Type X + 61.67 SF |
| 283 | 1-4/A-226B FRP-1 10'-0" (C-02) | RFI-13 corrected |
| 297 | 2/A-400A 21'-9" V.I.F. | RFI-03 text extended |
| 315 | A-410 types 1/1A/1B/1C "5/8 GYP BD BY FUTURE TENANT" | EXCLUDED with that citation - ALC-02 + RFI-01 |
| 317 | A-410 Metal Stud Schedule (gauges) | Gauge on every Partition Takeoff row + "By gauge" in the stud rows |
| 318 | Cafe 3-5/8" walls to 25' (> 22') | 14 ga SJ + diagonal braces 44.0 LF (precedent RFI-04) |
| 319 | Schedule note 1 | = #317 |
| 320 | Schedule note 2 (track gauge = stud) | Track rows: "Track gauge = stud gauge" |
| 333 | A-410 note 8.C X-EDNI | Row X-EDNI 720 pcs |
| 334 | A-410 note 8.D plywood screws | Row Plywood screws 2,331 pcs |
| 344 | Partition Notes 4, 5 (min 20 ga) | = #317 |
| 349 | 5/A-410 clip angle at each stud | Row Clip angle 2,518 pcs |
| 352 | 3/A-410 metal runner at studs | Row Nested inner runner 479.85 LF + RFI-40 |
| 355 | Top Track Detail citation (C-07) | 3/A-410 everywhere (8/A-410 = Typ. Connection) |
| 357 | 8/A-410 parallel to structure | Rows 3-5/8" / 6" stud cross members 705.0 LF + RFI-41 |
| 361 | 6/A-410 stud reinforcement (C-08) | Marked skill default (not printed); RFI stays 0 |
| 372 | 7/A-413 remove & replace existing GWB | Inside RFI-01 allowance - ALC-X44 |
| 373 | 7A/A-413 surface mount blocking | RFI-48 |
| 387 | A-500 door 4 location (C-09) | Labels: door 4 in W2-04 (not W2-05) |
| 400 | 2/A-500 cased opening wood blocking | Row Blocking 2X wood 17.0 LF + RFI-49 |
| 421 | A-510 Finish Notes 8 corner bead | Row Metal trim + 65.31 LF (soffit edges) |
| 432 | A-510 ACT legend | EXCLUDED - ALC-X40 |
| 445 | 2/E-103 server room 4x8 FRT plywood BY GC | FRT plywood 3/4" + 32.0 SF + RFI-50 |
| 454 | E-301 terminal board | = #445 |

New RFIs: RFI-38 to RFI-53, each with a conservative assumption and its delta. RFI-52 covers the vestibule bands V.I.F.; RFI-53 covers fixture hangers in the Cafe GWB bands.

## Error library (BE FAIL → fixed)
| Test | Fix |
|---|---|
| BE-08 | Printed dimensions now govern: 19'-0" HOLD, T.O. WD-1 15'-0", FRP heights |
| BE-12 | Citations fixed: 3/A-410, 7/A-210 and 8/A-210, 6/A-410 marked as skill default |
| BE-13 | 2/E-103 backboard carried (32 SF) + RFI-50 |
| BE-40 | Every Material Summary row has N/SHEET + a breakdown summing to Net; framed-soffit row and fire-stop track per wall included |
| BE-41 | No internal file or folder names in the Excel (checked on all visible sheets) |

## Gates
- REGLAS OK (812 rules, 0 failures)
- ALCANCES OK
- `registro.py entregable` OK
- EXCEL v67 OK
- ETAPAS PASA
- BITACORA OK
- Independent back-check: **PASS WITH COMMENTS**.
  - All 57 matrix rows have a destination, and every Net change reconciles.
  - All its comments are resolved in this rev7 (text fixes, RFI-52 / RFI-53, deltas in RFI-01 / RFI-51). See `takeoff_work/etapas/5_auditoria/BACKCHECK_rev7.md`.

Skill: **v80n** (R80e.27, five new families, gauges in Partition Takeoff, project notes in Inputs) in `take-off-metal-frame-drywall_FINAL_v80n.zip` at the repo root.

Drive: not uploaded.
