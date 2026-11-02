# RFI - SPECS (CONFLICT items only) - Chuze Fitness Austin Bluffs

Format: (A) plans/specs with N/SHEET, § and delta; (B) trade code with citation and delta; (C) Other: the estimator writes. 2 RFIs in total.

## RFI-S01 (1 of 2): Stud gauge / limiting height of free-standing partitions to deck (22'-10")

Rows affected: 3-5/8" metal stud (LF of material), 6" metal stud (LF of material) - per source, (track gauge of the same walls)

**Question.** A301 refers stud size/gauge/max height to S501 (not in the set); A2/A301 prints "MIN. 25 GAUGE @ 16" O.C."; RFI-04 assumed 25 ga for head C walls and 20 ga for head D/E. Spec 09 22 16 2.2.B.2 makes thickness a horizontal-deflection performance item and 05 40 00 1.1.A.3 moves framing taller than non-structural limits into 05 40 00 (A1003 structural, G60, bridging <=48" with top row and clip angles). At 5 psf (S100), a 3-5/8" 25 ga stud spans ~13.4 ft (L/240) / ~16.9 ft (L/120). The 16 type-A walls run 22.83 ft, so the spec and the RFI-04 assumption cannot both hold. Which member governs?

**Walls.** A2-3D: A-A422-5, A-A426-5, A-A426-6; A3C: A-A422-2, A-A423-6, A-A424-1/-2/-3, A-A425-1/-2/-3/-4/-5, A-A426-1, A-A435-2, A-A435-3 (233.48 LF of wall, 7,115.29 LF of 3-5/8" stud); A-A421-15 (14.42 ft, 259.56 LF stud); A6C A-A422-3/-4 (6" 25 ga, 388.11 LF stud). A6D/X6D 6" 20 ga at 22.83 ft are marginal (~24.3 ft gross) - verify.

- **(A)** PLANS/SPECS (A301 type notes + A2/A301 "MIN 25 GA" as a minimum; spec 09 22 16 2.2.B.2 + 2.2.C.2 "prevent cracking of finishes" -> L/240 brittle-finish criterion; 05 40 00 1.1.A.3, 2.3.B, 3.5.E-F): upgrade to a member meeting L/240 at 5 psf. 7,115.29 LF 362S125-18 -> 362S162-54 (16 ga) @ 12" o.c. (+2,371.6 LF net, +2,727.3 LF purchase = +137 sticks 20 ft). 259.56 LF (A-A421-15) -> 362S125-30 (20 ga) @ 16". 388.11 LF A6C -> 600S125-30 (20 ga) @ 16". Tracks of those walls to matching gauge (bottom 269.76 LF + top/slip 269.76 LF). 05 40 00 extras: G60/A1003, clip angle at each stud per bridging row (~2,500 clips est.), solid blocking @ 96" in the top row, sealer gasket 269.76 LF.
- **(B)** CODE (IBC 2021 1607.15 = 5 psf; IBC Table 1604.3 interior partitions L/120 flexible finish minimum; AISI S220 / ASTM C754 limiting-height tables): 7,115.29 LF -> 362S162-43 (18 ga) @ 16" o.c. (gauge only, 0 LF). A-A421-15 and A6C pass at 25 ga (0). Tracks of the 16 walls to 18 ga (233.48 LF bottom + 233.48 LF top). Delta: gauge upgrade only, 0 LF.
- **(C)** Other: estimator writes.

_Note:_ Limiting heights computed from gross Ix (centerline C-section, E = 29,500 ksi, 5 psf, 16" o.c.). These are UPPER bounds: manufacturer tables with effective Ix are lower, so every "fails" result stands and every "passes" result needs a check against ClarkDietrich / SSMA tables. Furring types C3C (A-A423-3, -9, A-A426-2, -3) and C3D (6 walls, 1,187.18 LF stud) also reach 22.83 ft. They are not free-standing if braced back to the existing construction, but that brace is not detailed - include in the same RFI.

## RFI-S02 (2 of 2): Hanger wire gauge at C-5 suspended GWB ceilings

Rows affected: Hanger wire, Hanger wire 12 ga - hanger count

**Question.** RCP general note 9 (A121, A421.A ... A435) and 13/A502 print #12 ga galvanized wire @ 4'-0" o.c. The C-5 legend tags 09 51 23 (Armstrong drywall grid), which only invokes ASTM C636 (12 ga). But 09 22 16 1.1.A.2 covers "suspension systems for interior ceilings and soffits" with 2.3.C wire hangers 0.16" dia. (~8 ga). Which governs the C-5 GWB ceilings?

- **(A)** PLANS/SPECS: A-1 RCP note 9 / 13/A502 + 09 51 23 3.2.A -> #12 ga as loaded (2,428.49 LF, 187 hangers), delta 0. A-2 spec 09 22 16 2.3.C -> 0.16" (8 ga) wire on the same 2,428.49 LF / 187 hangers: product upgrade, 0 LF.
- **(B)** CODE: ASTM C636 / C635 and Armstrong drywall-grid installation: 12 ga (0.106") @ 4'-0" o.c. max -> as loaded, delta 0.
- **(C)** Other: estimator writes.

_Note:_ Low impact (wire gauge only). Recommended: A-1 (plan + section the RCP tags).
