# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev8

rev8 = rev7 plus the second plan check (on rev7) applied.
- Sources: `../PASO12_rev7/CERTIFICADO_PASO12.md` and `MATRIZ_COBERTURA.xlsx` (484 items, 99.59 %), plus `../../BIBLIOTECA_ERRORES.md` (40 tests).
- Rule v80j: every point was checked on the plan (N/SHEET + circled crop in `../PASO12_rev7/img/`) before it was applied.
- Earlier revisions are unchanged. The only exception is the rev7 README, where the ALC-X40..X44 IDs are corrected (C7-08).
- Wall geometry does not change. The markups PDF and the per-sheet images are regenerated for rev8.

## 9 CORREGIR — verified on the plan and applied
| ID | Plan (N/SHEET) | rev8 |
|---|---|---|
| C7-01 | 5/A-121 "1 5/8" x 16 GA. METAL JOIST FRAMING @ 48" O.C." is the horizontal carrying member; the brace point carries "16 GA. WIRE 12'-0" O.C. EACH WAY" | 1-5/8" stud 131.42 → 0; the same 131.42 LF goes to its own row "16 ga wire at seismic brace points" (hanger wire stays 2,689.79 LF of 12 ga), RFI-38 |
| C7-02 | A-410 note 8.F X-DNI 2 rows @ 16" vs 9/A-410 0.177" PAF @ 24" | Slab pins 640.61 → 960.91 (printed, conservative); alternative in RFI-ACC-slab-pins; "type K box" removed |
| C7-03 | 8/A-410: relief channel #8 pan head self-tapping screws @ 24" + 6" from ends; cross members (1) 3/16" x 3/8" P.A.F. each end | X-EDNI 720 → #8 pan head 291 pcs + P.A.F. 282 pcs; X-EDNI kept as the alternative in RFI-51 |
| C7-04 | A-410 note 8.A: 25/20 ga #8-18 x 1/2" (min 2 per connection); 18/16 ga #10-16 x 3/4" (min 3) | Framing screws split by gauge: #8 1,940 (485 pieces x 4) + #10 1,776 (296 pieces x 6) = 3,716 (+592) |
| C7-05 | A-410 note 8.E: Type S on 25/20 ga, Type S-12 on 18/16 ga; "GA-216" was not a sheet | Drywall screws split: Type S 1.2 x 5,058.29 = 6,069.95 + S-12 1.2 x 11,143.59 SF (all faces of the 14 ga walls, no door deduction) = 13,372.31; total 19,442.26; N/SHEET A-410 8.E + A-001A Div 09 A.5 |
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
| 3-5/8" metal stud (LF of material) | LF | 11,479.27 | 11,601.59 |
| 1-5/8" metal stud (LF of material) | LF | 131.42 | (replaced, see below) |
| X-EDNI fasteners 0.145" (Hilti), top track to structure (A-410 note 8.C) | PCS | 720.00 | (replaced, see below) |
| Cement board (tile / FRP substrate) | SF | 789.94 | (replaced, see below) |
| Drywall screws 1-1/4" bugle head | PCS | 19,442.26 | (replaced, see below) |
| Framing screws, pan head self-drilling | PCS | 3,124.00 | (replaced, see below) |
| Power-driven fasteners, slab pins for the bottom track | PCS | 640.61 | 960.91 |
| #8 pan head self-tapping screws, relief channel to structure (8/A-410) | PCS | — | 291.00 |
| #10-16 x 3/4" Tek screws, pan head, at 16 ga clip angles and nested header / column / beam (5/A-410; 7/A-210; 8/A-210; A-410 note 8.A) | PCS | — | 10,668.00 |
| 16 ga wire at seismic brace points (5/A-121) | LF | — | 131.42 |
| P.A.F. 3/16" x 3/8" at cross member ends (8/A-410) | PCS | — | 282.00 |
| 5/8" cement board (tile base) | SF | — | 50.04 |
| 1/2" cement board / cementitious backer | SF | — | 739.90 |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | — | 6,069.95 |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | — | 1,940.00 |
| Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | PCS | — | 1,776.00 |
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | — | 13,372.31 |

Partitions total: no change, **569.82 LF**. Board SF: no change.


## Back-check findings applied in rev8 (each verified on the plan before applying)
| Test | Finding | rev8 |
|---|---|---|
| BE-17 | S-12 used a door deduction | S-12 = 13,372.31; Type S = 6,069.95 (see C7-05) |
| BE-12 / BE-47 | RFI-38 "metal joist post"; slab-pin quote cut off; RFI-51 "12" O.C." and "posts" | Texts rewritten from the plan |
| BE-46 | 16 ga wire inside hanger wire | Own row, 131.42 LF |
| BE-16 / BE-17 | 5/A-410 "(4) TEK SCREWS" per clip; 7/A-210 and 8/A-210 Teks | One row "#10-16 x 3/4" Tek screws" (A-410 note 8.A, 16 ga clip) = **10,668 pcs**: 5/A-410 2,518 clips x 4 = 10,072 + 7/A-210 clips 16 + 7/A-210 runner tracks 44 + 8/A-210 nested beam 88 + nested columns 432 + 7/A-210 head attachment 16. RFI-51: the "8 per member" reading = −464 pcs |
| Text | Process tags in client texts | Removed; the markups PDF metadata is cleared |

## Error library
Independent back-check of the final Excel: **PASS WITH COMMENTS — LIBRARY 37 PASS · 0 FAIL · 3 N/A**. See `takeoff_work/etapas/5_auditoria/BACKCHECK_rev8_recheck.md`. The first pass (`BACKCHECK_rev8.md`) had 5 FAIL; all of them are fixed.

Open non-blocking comments (for estimator review):
- **RFI-28:** A/A-410 "(1) #10-16 SCREW @ EACH FLANGE" (≈ +324 pcs) is not listed. The slab pins may also overlap the type 3 / 4 HUS-EZ anchors (≈ 183 pins).
- **8/A-410:** the "#8 SCREWS" to the top chord are only covered by the "+724" mention in RFI-51.
- **ALC-04:** still names X-EDNI 8.C, which is now the alternative in RFI-51.
- **16 ga wire row:** the selling unit is "piece"; it should be coil.
- **S-12 / Type S split:** ignores ≈ 37 SF of cement board base on the 14 ga walls (≈ 45 screws). The total is unchanged.
- **Citations:** some still carry plan-check item codes (C7-01, C-03, C-07) or "skill default".

Skill **v80o**: rules R80e.28 and R80e.29, in `take-off-metal-frame-drywall_FINAL_v80o.zip` at the repo root. R80e.29 adds:
- family order;
- screws by face;
- one row per wire gauge;
- no process tags in client texts;
- full quotes;
- PDF metadata;
- fastener size from note 8.A;
- every arrow of a detail.

## Gates
- REGLAS OK (814 rules, 0 failures)
- ALCANCES OK (24 reviewed, 2 RFI)
- `registro.py entregable` OK
- EXCEL v67 OK
- ETAPAS PASA
- BITACORA OK (17 mandatory tools current + back-check)

Drive: not uploaded. Nothing sent to the client.
