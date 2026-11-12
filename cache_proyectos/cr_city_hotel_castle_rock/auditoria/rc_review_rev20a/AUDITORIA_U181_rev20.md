# AUDITORIA U-181 rev20 - CR City Hotel - 2026-11-12 07:44 (PST)

Independent background audit (U-181) of rev20, run by reviewers that did not build the take-off (read-only on the work folder):
1) change audit (re-read blind from the bid set: corridor band 7/A7.23, smoke curtain 12/A9.03, coffers 5/A7.31, retail beam wraps; rev20a: resilient channel UL L546, finding 13);
2) coverage audit of EVERY governing detail and EVERY RCP sheet (U-189 (3)); 3) blind double readings H-A / H-B of every new Depth row.

Audited files (current delivery):
- Excel: CR_City_Hotel_Takeoff_FINAL_rev20.xlsx sha256 834fc00cdf17924058743bebd4e2e41546774449b0254c4ec649327a49d49298
- Markups PDF: CR_markups_rev20 - OPEN IN BLUEBEAM.pdf sha256 fe550b85f057723fe1cb3a3ed999f5c9402dd858069ea440f5c41cb434e94598

## FINDINGS and closure

| # | Finding (reviewer) | Closure in rev20 (by the chain) |
|---|---|---|
| 1 | Smoke-curtain housing 12/A9.03: the shaft-side face 23.73" was missing (3.06 -> 5.04 ft) | rev20_soffits: 5.04 ft, 5 faces in side / faces |
| 2 | Corridor box face drawn above the GYP-1 field (plenum, 11 5/8") not loaded | rev20_campo: SOF-L2-01P..L4-02P (one side, band LF / 2); Review Item = deduction |
| 3 | SOF-L4-02 source cited the old 242.72 LF | source rewritten: measured run 343.67 LF |
| 4 | Retail north edge beams on the rev19 basis | AISC basis: +3.58 SF (BW-L1-RETAIL 379.14) |
| 5 | Coffer outer edge (U-114) | measured 124.92 LF: 0 SF to add; possible bottom double count -104.77 = Review Item (coordination decision 1.25 kept, U-052) |
| 6 | L4 bath RS-1 missing above the hung GYP-1 (double ceiling) | CLG-L4-106R..114R: +484.63 SF Type X + 363.48 LF RC |
| 7 | RCP GAP-1: underside of mezzanine 219 floor (2/A5.04) | CLG-L1-219U Type C (A0.03 1 HR horizontal assembly, A0.08 FS-1) |
| 8 | RCP GAP-3 / GAP-4 and details GAP-1: lobby 217 / 317 + vestibule + corridor strip dropped GYP-1 | CLG-L2-217F / CLG-L3-317F; band loop SOF-*-217V / 317V; border box SOF-*-217B / 317B |
| 9 | Details GAP-2: L1 passage 'CEILING APPLIED TO UNDERSIDE OF DECK' (5/A5.04) | CLG-L1-129P |
| 10 | Details N3: grid-1 north edge beams over Kitchen 100 / Elec 104 not wrapped (FS-1) | BW-L1-NORTH (W24X68 + W24X55) + RC |
| 11 | Details N1: lobby field GYP-1 (A3.01) vs WS-1 (1/A7.31) conflict | gypsum kept (larger); Review Item deduction -590.81 SF |
| 12 | RCP GAP-2: F&B 410 / 419 ceiling reason | covered by rcp_cuartos exclusion (printed F&B note) with EXCLUDED markups: delta 0 |
| 13 | RC (largest rev20 change, +7,526.67 LF): independent rebuild by a reviewer that did not build the take-off (Auditoria/rc_review/RC_REVIEW.md): 27,124.96 LF vs 27,124.98 LF (rounding). FS-1 12 in o.c. [CONFIRMED A0.08 FS-1 + S1.02 18" trusses + UL L546 Items 5 / 6]; end-joint channels [CONFIRMED UL L546 Item 6], 1,757.19 LF by level SF / 12 (room-by-room check 1,590-1,845 LF); beam wraps 600.29 + 92.24; waste once (15 %, row 14). Bridge rev19->rev20: spacing +5,313.79, end joints +1,757.19, L4 baths +363.47, north wrap +92.24 = +7,526.69 | Verdict OK with notes, no change. N1: RS-1 16 in o.c. is not printed (A0.08 RS-1 no UL #, spec 09 22 16 3.1.A = ASTM C 754): stays in RFI-14 with its delta (24 in o.c. = -1,140.02 LF; the 363.47 LF over the L4 baths follows the RS-1 double-ceiling decision B6). N2: beam-wrap bottom line overlaps field RC <= ~160 LF (conservative). N3: W18 beams 1-2 in below the trusses not all checked (lobby handled). N4: splice laps ~2.8 % inside the 15 % waste |

abiertos: 0

## COBERTURA

Details that govern quantity (compuerta_entrega.cobertura_esperada over the current canon): 57. RCP sheets: 25.

| Detail | Verdict (independent reviewer) |
|---|---|
| 1/A2.02 | OK |
| 1/A2.03 | OK |
| 1/A2.04 | OK |
| 1/A3.01 | GAP (GAP-2: the passage east of CLG-L1-127, grid M to the fire wall, is drawn with no tag and has no row) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 1/A3.02 | GAP (GAP-1 L2: the gypsum stipple in Lobby 217 and the corridor junction, between CLG-L2-56 and CLG-L2-58, has no GYP-1 row) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 1/A3.03 | GAP (GAP-1 L3: same zone at Lobby 317) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 1/A3.04 | OK |
| 1/A4.04 | OK |
| 1/A5.06 | OK |
| 1/A5.08 | OK |
| 1/A7.23 | GAP (GAP-1 L2: gypsum at 8'-0" around WS-1 in Lobby 217 [CONFIRMED tags 1/A7.23]) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 1/A7.24 | GAP (GAP-1 L2: the N-S strip south of match line 1/A7.23, tagged 8'-11" [CONFIRMED 1/A7.24], lies outside CLG-L2-58) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 1/A7.30 | OK |
| 1/A7.31 | GAP (GAP-2: passage x 2295.5-2406.24; see also note N1) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 1/A7.50 | OK |
| 10/A7.00 | OK |
| 10/A7.05 | OK |
| 10/A7.09 | OK |
| 10/A9.03 | OK |
| 11/A6.01 | OK |
| 11/A9.03 | OK |
| 12/A9.03 | OK |
| 2/A5.04 | OK - RCP coverage auditor GAP-1 ('GYP BD APPLIED TO B.O. WOOD JOIST'): loaded CLG-L1-219U |
| 2/A7.00 | OK |
| 2/A7.05 | OK |
| 2/A7.09 | OK |
| 2/A7.16 | OK |
| 2/A7.23 | GAP (GAP-1 L3) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 2/A7.24 | GAP (GAP-1 L3: N-S strip south of match line) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 2/A7.31 | OK |
| 2/A7.50 | OK |
| 3/A5.04 | GAP (GAP-2) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 3/A7.23 | OK |
| 3/A7.24 | OK |
| 3/A7.45 | OK |
| 3/A7.50 | OK |
| 3/S3.02 | OK (note N3) |
| 4/A5.05 | OK |
| 4/A6.02 | OK |
| 4/A7.05 | OK |
| 4/A7.16 | OK |
| 4/A7.31 | OK |
| 4/S3.08 | OK - blind readers H-A / H-B (north edge beams): loaded BW-L1-NORTH |
| 5/A5.04 | GAP (GAP-2) -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| 5/A6.02 | OK |
| 5/A7.23 | OK - blind readers H-A / H-B (lobby border box): loaded SOF-L2-217B / SOF-L3-317B |
| 5/A7.31 | OK |
| 6/A7.00 | OK |
| 6/A7.23 | OK - blind readers H-A / H-B (lobby border box): loaded SOF-L2-217B / SOF-L3-317B |
| 7/A6.01 | OK |
| 7/A7.13 | OK |
| 7/A7.23 | OK |
| 7/A7.31 | OK |
| 7/A9.03 | OK |
| 8/A7.13 | OK |
| 8/A9.03 | OK |
| 9/A7.09 | OK |

| RCP sheet | Verdict (independent reviewer) |
|---|---|
| A0.08 | OK. RS-1 and RS-6 are loaded, along with MB-1 (CLG-L1-00/01/18), FS-1 (L1 plate 7,711.49 SF, L2/L3 rooms) and BW-L1-RETAIL. RS-2, RS-3, RS-5 and RS-7 have no gypsum in the assembly. RS-4 is TBD / future F&B TI. Each has a types_none_reason. |
| A0.10 | N/A. This is a generic detail. No unit RCP draws an in-unit soffit apart from the bath drops, which are loaded. No quantity changes. |
| A3.01 | GAP-1. The underside of mezzanine 219 is not in the canon. The L1 FS-1 contour says 'Mezzanine 219 ... NO incluido', and there is no row or none_reason. Everything else is covered: Retail 124 strip by tenant (RFI-05); lobby coffers = FS-1 (excluded_items CLG-L1-11); Water Entry 128 excluded (RFI-17); Bar 107 CLG-L1-125 (RFI-22); ACT and WS-1 belong to other trades; the gray area is under a separate permit. -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| A3.02 | GAP-3. Lobby 217 + vestibule + the corridor N-S strip y 1007.6-1212 have FS-1 but no dropped GYP-1 row: CLG-L2-56 stops at y 1007.64 and CLG-L2-58 starts at y 1212.0. -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| A3.03 | GAP-4. Same as GAP-3: Lobby 317 (+ vestibule) + corridor strip y 1007.6-1212 have no dropped GYP-1 row (CLG-L3-87 ends at 1007.64, CLG-L3-88 starts at 1212.0). -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| A3.04 | GAP-2 (documentation, delta 0). 410 F&B and 419 Warming Kitchen are drawn with gypsum stipple and have no ceiling row or ceiling none_reason. The 'NOT IN SCOPE' note is printed on 1/A2.04, 2/A7.55 and 3/A7.50, but the canon only states it for wall faces and for RS-4 (411). -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| A7.00 | OK |
| A7.05 | OK |
| A7.09 | OK |
| A7.13 | OK |
| A7.16 | OK |
| A7.23 | GAP. This is the source drawing of GAP-3 / GAP-4: the south end of 1/A7.23 and 2/A7.23 (lobby WS-1 zone with its 1'-4 1/2" gyp border at 8'-0", and the vestibule field with its 1'-0" band) has no dropped row. It is the same SF as GAP-3/4, not additional. -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| A7.24 | GAP (shared). The E-W runs are covered. The west stub at the 1/A7.23 match line (x 799-853, y below 1212) belongs to the GAP-3/4 strip. It is the same SF, not additional. -> CLOSED in rev20 (rows loaded by the chain, see FINDINGS) |
| A7.31 | OK. Retail strip by tenant (RFI-05). CLG-L1-125 bar, CLG-L1-127 niche, CLG-L1-07/08/09 toilets. |
| A7.45 | OK. ACT is other trade; Kitchen F&B is not in scope (note printed on 1/A7.45). |
| A7.50 | OK |
| A7.55 | OK (RS-4 none_reason). See GAP-2 for the explicit 410/419 ceiling none_reason. |
| A9.03 | OK. SOF-L2/L3/L4-SCN/SCS, CLG-L1-SHN/SHS. 10/A9.03 shows no lid at the shaft head. |
| A9.04 | N/A. Exterior wood/metal soffits and the casework panel are not drywall. The bar CLG refers to CLG-L1-125. |
| E0.00 | N/A. Lighting and devices only. |
| E2.01 | N/A. Lighting only. |
| E2.02 | N/A |
| E2.03 | N/A |
| E2.04 | N/A |
| T0.01 | N/A. Index / standards only. |

Not reviewed: 0

