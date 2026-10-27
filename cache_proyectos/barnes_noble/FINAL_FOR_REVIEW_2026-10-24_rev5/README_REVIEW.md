# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev5

rev5 = rev4 + the independent final audit of rev4, applied: `../AUDITORIA_rev4/CERTIFICADO_AUDITORIA.md` and `../AUDITORIA_rev4/COMPARATIVA_AUDITORIA.xlsx` (24 rows, evidence in `../AUDITORIA_rev4/img/`).

Rule v80j (total autonomy): every difference was resolved from the drawings and applied without asking. What the plan does not print is an RFI with a conservative assumption and its delta. Earlier revisions are unchanged.

## Files
| Folder | File |
|---|---|
| Take-off/ | `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev5.xlsx` (6 sheets, formulas recalculated) |
| Planos marcados/ | `Barnes_Noble_ColoradoSprings_FINAL_markups_rev5.pdf` (Bluebeam: A-101 68 annots, A-221 26 annots, incl. SS-GG, C-I-E1, C-I-E2, C-I-P.1) |
| Planos marcados/ | `A-221_partitions_by_type_rev5.png`, `A-221_GrabGo_soffit_and_type_I_end_faces_zoom_rev5.png`, `by_type/A-221_type_I_rev5.png`, `by_type/A-221_OTHER_FRAMING_soffit_sides_rev5.png` |

Only A-221 changed geometry: the Grab & Go soffit and the type I end faces. A-101 images stay as in rev3 (`FINAL_FOR_REVIEW_2026-10-24_rev3/Planos marcados/`, `_v2`).

## Changes (rev4 → rev5)
| Item | rev4 | rev5 | Audit row | Source |
|---|---|---|---|---|
| Partition total | 568.61 LF | 569.82 LF | 1 | Type I end faces "I SIM." at C-H3a and C-H1-N: 2 × 7 1/4" = 1.21 LF, finish only (framing already in the host wall) – 1/A-221, I/A-221 |
| 6" metal stud | 2,900.00 LF | 3,007.50 LF | 6 | Grab & Go soffit SS-GG: 6 studs × 17.917 ft (25'-0" − 7'-1") = 107.5 LF – 3/A-221, 6'-2" HOLD 1/A-221, 1/A-121 |
| 3-5/8" metal stud | 10,778.08 LF | 10,788.75 LF | 5 | Water heater backing 8.0 + steel blocking 2.67 LF (conservative, RFI-32) – P-201 |
| Track, ceilings / soffits | 321.78 LF | 564.25 LF | 6, 7 | Fire stop track at ceiling line 230.14 LF (3-5/8" 142.74 + 6" 87.40) – 8/A-410, RFI-35; SS-GG track 12.33 LF |
| Bracing C.R. channel | 2,858.98 LF | 2,883.65 LF | 6 | SS-GG 4 rows × 6.167 = 24.67 LF – 5/A-410 |
| 5/8" Type X | 15,579.48 SF | 14,902.61 SF | 1, 3, 6, 9 | −692.66 to W.R.; +12.07 type I end faces GWB; +3.73 SS-GG bottom |
| 5/8" Type X W.R. | 1,020.33 SF | 1,713.00 SF | 3, 9 | Restroom GWB ceilings 122.30 SF (A-410 Partition Notes 2); Cafe Work Room 104 faces 570.36 SF (A-410 "*" note KITCHEN, 2/A-410) |
| 5/8" FRT plywood | 2,709.63 SF | 2,838.21 SF | 1, 6 | SS-GG east face 110.49 SF (T.O. WD-1 not printed, RFI-34); end faces 2 × 0.603 × 15.0 = 18.09 SF |
| 3/4" FRT plywood | 353.46 SF | 370.46 SF | 4 | Janitor 2.125 × 8'-0" = 17.0 SF (upper bound, RFI-33) – 11/A-200 |
| Additional head track | 0 LF | 10.67 LF | 8 | Doors 3 and 11 (4'-0"), 2 × (4.00 + 1.33) – RFI-31; the old "> 4'-0"" note citation was a skill default, not printed – corrected |
| Drywall screws / framing screws / joint compound / joint tape | 19,919.77 / 3,100 / 1,195.19 / 6,141.93 | 19,938.73 / 3,124 / 1,196.32 / 6,147.78 | – | follow board and stud pieces |

Auditor figures that differ slightly, and why:
- **Restroom ceilings:** 122.30 SF vs 120.2. The take-off keeps the RCP area; the auditor deducted the chase notch.
- **Additional head track:** 10.67 LF vs 11.17. The R.O. is the measured 4.00 ft jamb gap; the auditor assumed 4'-3". The +0.50 LF is written in RFI-31.

## RFIs
**New (36 in the log; closed ones are not shown in the Excel):**
- **RFI-31:** additional head track.
- **RFI-32:** water heater backing (P-201).
- **RFI-33:** janitor plywood extent (11/A-200).
- **RFI-34:** Grab & Go T.O. WD-1 (3/A-221).
- **RFI-35:** fire stop track confirmation (8/A-410).
- **RFI-36:** W-3 surface blocking (1/A-414, 7/A-414).

**Updated:**
- **RFI-11:** W.R. now includes the restroom ceilings and Cafe Work Room 104.
- **RFI-12:** Corridor 110 wall tile backer added.
- **RFI-13:** FRP, with the A-510 rooms.
- **RFI-20:** CLOSED, quantified.
- **RFI-23** and **RFI-27:** text updated.

## Traceability (audit checks 5 and 6)
- **Material Summary "Where it comes from":** every row cites N/SHEET; no internal file names remain. Each row also carries a `Breakdown [DERIVED]` per wall or element that adds up to the Net.
  - The 3-5/8" stud row (10,788.75 LF) is the per-wall studs (field + jambs + nodes + cripples × height) + column wraps + diagonal braces + vestibule posts + water heater backing.
  - The 6" stud row (3,007.50 LF) is per wall + SS-GG.
  - The 5/8" FRT plywood row (2,838.21 SF) is per strip.
  - This closes audit rows 13–15. The auditor's "1,967 LF / 275 LF / 2,528 SF not traceable" were the jambs, nodes, cripples and elements that rev4 did not list.
- **Partition Takeoff:** the 21 rows with Board ≠ L × H × Layers show the height of each face ("Board by face: side room length × height (board)").
- **Scope Checklist:** ALC-04 / 06 / 07 / 08 / 10 / 11 / 12 / 13 / 15 / 16 / 20 are rewritten with the rev5 figures and the closed RFIs (8/A-410, RFI-15 / RFI-17 closed, RFI-20 closed).
- **Wall ID:** C-E1-P.1 is renamed C-I-P.1 in the Excel, markups and images (audit row 21).

## No change (audit rows 2, 12, 17)
- Curved walls: 25.68 LF each (RFI-18).
- Insulation: excluded.
- Cross tee: 457.96 LF / 124 pcs. The 443.19 LF in DECISIONES_ESTIMADOR.md is the outdated figure.

## Gates
- `registro.py entregable`: OK.
- `alcances.py compuerta`: OK (24 scope rows reviewed, 2 RFI).
- `plantilla_excel.py verificar`: EXCEL v67 OK.
- `etapas.py compuerta`: PASA.
- closer: 61 walls sealed, 0 rejected.
- planmark and markups: OK.
- `reglas.py compuerta --excel` and `bitacora.py compuerta`: see the back-check line below.

Skill updated to **v80k** (rules R80e.22–R80e.25, new tool `trazabilidad.py`): `take-off-metal-frame-drywall_FINAL_v80k.zip` at the repo root.

Drive: not uploaded (as requested).
