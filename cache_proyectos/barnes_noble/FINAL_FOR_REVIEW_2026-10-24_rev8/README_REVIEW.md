# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev8

rev8 = rev7 plus the second Paso 12 pass applied.
- Sources: `../PASO12_rev7/CERTIFICADO_PASO12.md` and `MATRIZ_COBERTURA.xlsx` (484 items, 99.59 %), plus `../../BIBLIOTECA_ERRORES.md` (40 tests).
- Rule v80j: every point was checked on the plan (N/SHEET + circled crop in `../PASO12_rev7/img/`) before it was applied.
- Earlier revisions are unchanged. The only exception is the rev7 README, where the ALC-X40..X44 IDs are corrected (C7-08).
- Wall geometry does not change. The markups PDF and the per-sheet images are regenerated for rev8.

## 9 CORREGIR — verified on the plan and applied
| ID | Plan (N/SHEET) | rev8 |
|---|---|---|
| C7-01 | 5/A-121 "1 5/8" x 16 GA. METAL JOIST FRAMING @ 48" O.C." is the horizontal carrying member; the brace point carries "16 GA. WIRE 12'-0" O.C. EACH WAY" | 1-5/8" stud 131.42 → 0; the same 131.42 LF goes to vertical 16 ga wire (hanger wire row), RFI-38 |
| C7-02 | A-410 note 8.F X-DNI 2 rows @ 16" vs 9/A-410 0.177" PAF @ 24" | Slab pins 640.61 → 960.91 (printed, conservative); alternative in RFI-ACC-slab-pins; "type K box" removed |
| C7-03 | 8/A-410: relief channel #8 pan head self-tapping screws @ 24" + 6" from ends; cross members (1) 3/16" x 3/8" P.A.F. each end | X-EDNI 720 → #8 pan head 291 pcs + P.A.F. 282 pcs; X-EDNI kept as the alternative in RFI-51 |
| C7-04 | A-410 note 8.A: 25/20 ga #8-18 x 1/2" (min 2 per connection); 18/16 ga #10-16 x 3/4" (min 3) | Framing screws split by gauge: #8 1,940 (485 pieces x 4) + #10 1,776 (296 pieces x 6) = 3,716 (+592) |
| C7-05 | A-410 note 8.E: Type S on 25/20 ga, Type S-12 on 18/16 ga; "GA-216" was not a sheet | Drywall screws split: Type S 6,402.26 + S-12 13,039.99 = 19,442.25; N/SHEET A-410 8.E + A-001A Div 09 A.5 |
| C7-06 | 22/A-201 "5/8" CEMENT BOARD"; E/A-221 and A-D/A-221 "1/2"" | One row per thickness: 1/2" 739.90 SF + 5/8" 50.04 SF; screws cite E/A-221, A-D/A-221, 22/A-201 |
| C7-07 | Material Summary FRT blocking = 568.27 LF | RFI-23 and ALC-16 read 568.27 LF (2X wood 17.0 LF in its own row) |
| C7-08 | Scope Checklist ALC-X40..X44 | rev7 README IDs corrected |
| C7-09 | Markups legend "Source: takeoff_canon.json" | Legend reads "Source: the take-off Excel (Partition Takeoff)"; skill tool fixed |

## 2 GAP → destination
| Row | Destination |
|---|---|
| N-01 (3/A-410, 4/A-410 "TO BOTTOM OF NESTED STUD BRACING") | +122.32 LF 3-5/8" stud (one nested stud at the top of each type 3 / 4 wall), RFI-46 extended |
| N-03 (E-301 Sec. 265119 fixture supports by the electrical contractor) | RFI-53 extended: −401.0 LF hanger wire (29 hangers) if by the EC |

## Changes rev7 → rev8 (Material Summary Net)
| Material | Unit | rev7 | rev8 |
|---|---|---|---|
| 1-5/8" metal stud (LF of material) | LF | 131.42 | (replaced, see below) |
| X-EDNI fasteners 0.145" (Hilti), top track to structure (A-410 note 8.C) | PCS | 720.00 | (replaced, see below) |
| Cement board (tile / FRP substrate) | SF | 789.94 | (replaced, see below) |
| Drywall screws 1-1/4" bugle head | PCS | 19,442.26 | (replaced, see below) |
| Framing screws, pan head self-drilling | PCS | 3,124.00 | (replaced, see below) |
| 3-5/8" metal stud (LF of material) | LF | 11,479.27 | 11,601.59 |
| Hanger wire | LF | 2,689.79 | 2,821.21 |
| #8 pan head self-tapping screws, relief channel to structure (8/A-410) | PCS | — | 291.00 |
| P.A.F. 3/16" x 3/8" at cross member ends (8/A-410) | PCS | — | 282.00 |
| 5/8" cement board (tile base) | SF | — | 50.04 |
| 1/2" cement board / cementitious backer | SF | — | 739.90 |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | — | 6,402.26 |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | — | 1,940.00 |
| Power-driven fasteners, slab pins for the bottom track | PCS | 640.61 | 960.91 |
| Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | PCS | — | 1,776.00 |
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | — | 13,039.99 |

Partitions total: no change, **569.82 LF**. Board SF: no change.

## Error library
The back-check runs all 40 tests; the result is in the Gates line.
The skill (v80o) adds rule R80e.28 and makes these changes:
- screws by gauge (8.A / 8.E);
- one row per cement board thickness;
- #8 pan head + P.A.F. families from 8/A-410;
- markups legend without file names;
- slab pin RFI text with the printed spacings.

## Gates
(updated after the back-check)

Drive: not uploaded.
