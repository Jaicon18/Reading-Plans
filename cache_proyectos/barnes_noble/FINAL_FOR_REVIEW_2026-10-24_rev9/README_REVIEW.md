# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev9

rev9 = rev8 plus the 8 CORREGIR from the rev8 plan check (`../PASO12_rev8/CERTIFICADO_PASO12.md`: coverage 100 %, 0 GAP).
- Each finding was checked on the plan (circled crop, N/SHEET) before it was applied.
- Rule R80e.30: only the changed items were re-verified (targeted review).
- Wall geometry does not change. The markups PDF is regenerated; the per-sheet images are the rev8 ones.

## Files
| Folder | File |
|---|---|
| Take-off/ | `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev9.xlsx` (6 sheets, formulas recalculated) |
| Planos marcados/ | `Barnes_Noble_ColoradoSprings_FINAL_markups_rev9.pdf`, `A-101_partitions_by_type_rev9.png`, `A-221_partitions_by_type_rev9.png` |

## 8 CORREGIR — verified on the plan and applied
| ID | Plan (N/SHEET) | rev9 |
|---|---|---|
| C8-01 | 3/A-410, 4/A-410 "3 5/8" X 20GA TRACK W/ (2)-1/4"ø X 1 5/8" HILTI KWIK HUSEZ CONCRETE SCREW AND MOMENT CLIP - SEE DETAIL" (A/A-410) | Slab pins 960.91 → **777.43** ((640.61 − 122.32) LF / 0.667). HUS-EZ and moment clips stay in RFI-28 |
| C8-02 | A/A-410 "(1) #10-16 SCREW @ EACH FLANGE" | RFI-28 delta + 324 #10-16 screws (162 clips x 2) |
| C8-03 | 8/A-410 "ATTACH TO TOP CORD OF EXIST'G STRUCTURE W/ #8 SCREWS"; "(2) #8 SCREW AT EACH STUD"; "ATTACH TO TRACK W/ #8 SCREWS AT 24" O.C." | Own row **775 pcs** = 282 (2 per cross member) + 141 (track @ 24") + 282 (top chord, 2 ends) + 70 (one per joist crossing on the perpendicular walls, joists at 5'-0" as in RFI-41). RFI-41: at 4'-0" joists + 15; if "(2) per stud" means each wall stud @ 16": 380 instead of 282 (+ 98). The plan check estimated ≈ 849 with that second reading. The rev7 matrix note N-13 ("covered by framing screws") is corrected |
| C8-04 | 8/A-210, 4/A-210, 3/A-410, 2/A-221, 3/A-221 | The 618.81 LF row is split by size: Track 3-5/8" 281.09 + Track 6" 144.06 + 8" ledger 12.67 + ceiling perimeter track 180.99 (size not printed, **RFI-54** new) |
| C8-05 | Purchase units | LF rows now buy real pieces: 2x lumber 8 ft, main tee 12 ft, cross tee 4 ft (132 pcs vs RFI-15 124 net), molding 12 ft, 16 ga wire in coil |
| C8-06 | ALC-04 | X-EDNI 8.C is the alternative in RFI-51, not quantified |
| C8-07 | Client texts | Plan-check item codes removed (Material Summary and Pending Items) |
| C8-08 | 22/A-201 base on the 14 ga walls: (38.15 − 6.66) LF x 1'-2" = 36.74 SF | S-12 **13,328.22**, Type S **6,114.04** (total unchanged). Framing screws cite A-410 note 8.A with the full piece breakdown (781 = 673 walls + 108 column wraps; 485 light + 296 heavy) |

## Changes rev8 → rev9 (Material Summary)
| Material | Unit | rev8 Net | rev9 Net | rev8 pieces | rev9 pieces |
|---|---|---|---|---|---|
| Track, ceilings / soffits / canopy | LF | 618.81 | (split, see below) | 72.00 | — |
| Blocking FRT / 2X FRT wood | LF | 568.27 | 568.27 | 654.00 | 82.00 |
| USG drywall suspension main tee DGLW26 | LF | 194.16 | 194.16 | 224.00 | 19.00 |
| USG drywall suspension cross tee DGLW424 | LF | 457.96 | 457.96 | 527.00 | 132.00 |
| USG channel molding DGCM27 | LF | 107.21 | 107.21 | 124.00 | 11.00 |
| USG angle molding DGWM24 | LF | 107.21 | 107.21 | 124.00 | 11.00 |
| 16 ga wire at seismic brace points (5/A-121) | LF | 131.42 | 131.42 | 152.00 | 152.00 |
| Blocking 2X wood (not labeled FRT) | LF | 17.00 | 17.00 | 20.00 | 3.00 |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 6,069.95 | 6,114.04 | 6,070.00 | 6,115.00 |
| Power-driven fasteners, slab pins for the bottom track | PCS | 960.91 | 777.43 | 961.00 | 778.00 |
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | 13,372.31 | 13,328.22 | 13,373.00 | 13,329.00 |
| Ceiling perimeter track at GWB ceilings (size not printed, RFI) | LF | — | 180.99 | — | 21.00 |
| Track 3-5/8" at soffits, fire stop at ceiling line and nested columns | LF | — | 281.09 | — | 33.00 |
| Track 6" at soffits, fire stop at ceiling line and nested beam | LF | — | 144.06 | — | 17.00 |
| 8" ledger track (4/A-210) | LF | — | 12.67 | — | 2.00 |
| #8 screws at the top chord, cross members and track (8/A-410) | PCS | — | 775.00 | — | 892.00 |

Partitions total: no change, **569.82 LF**. Board SF: no change.

## RFI-51 (back-check fixes)
- 9/A-410 alternative now reads − 518.29 pins (518.29 LF of track on slab).
- Diagonal brace end screws (3/A-410) are not printed and not carried; + 512 #8 if 2 per end.

## Error library
GATES_AND_LIBRARY

Skill **v80p**: rule R80e.31 (other anchorage, full RFI deltas, inherited coverage, family splits by size, purchase units, per-face deductions, yield citations) in `take-off-metal-frame-drywall_FINAL_v80p.zip` at the repo root.

Drive: not uploaded. Nothing sent to the client.
