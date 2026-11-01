# CERTIFICADO DE AUDITORÍA — rev2 (Step 11 re-audit)
**Audited:** `5_entrega/Chuze_AustinBluffs_Takeoff_rev2.xlsx` (54,644 B), `Chuze_AustinBluffs_Markups_rev2.pdf` (220,450,979 B, 107 p., 109 annotations), `imagenes_rev2/` (19 files), `CAMBIOS_rev2.md`.
**Sources used:** the bid set (M110 p78 included), `plano/specs.pdf` (spec citations only), the deliverables and CAMBIOS. The forbidden paths were not opened. Each evidence image was reopened and checked after it was written.

## Result
| # | Check | rev1 | rev2 |
|---|---|---|---|
| 1 | Tag sweep | PASS | **PASS** (walls unchanged; 97 elements + 12 legend lines) |
| 2 | Re-measurement | PASS | **PASS**. The Partition Takeoff is identical to rev1 and rev0 in all 101 rows. Bluebeam A-A426-2/-3 = 4.67 = printed 10" + 3'-0" + 10" (A426 dims) |
| 3 | Detail chain | PASS | **FAIL**: the new top-track split puts 166.58 LF of top track at walls framed to the deck under "standard top track (walls not reaching structure)" |
| 4 | Scope sweep | PASS | **PASS** (MEP crossings spot-checked on M110: 3 of 3 show a duct crossing the wall) |
| 5 | Arithmetic | PASS | **PASS** (every breakdown sums to its Net; track family total 1,104.77 unchanged; molding 396.71 + 62.20 = 458.91; framing screws 4 × 1,285 = 5,140) |
| 6 | Format | FAIL | **PASS** (0 change ids, "soffit_side", "skill", MEP diagnostics, "grep" or phantom ids left in the visible sheets; 3 minor residuals noted) |
| 7 | Bluebeam | PASS | **PASS** (C3C Σ 24.53 vs 24.54; soffit sides 220.23 vs 220.24; every type within ±0.13 %) |
| 8 | Files | PASS | **PASS** |

## Check 3 — FAIL: top-track split
rev2 splits the top track per stud size into "slip / deflection (2" leg, walls to structure)" for heads D/E and "standard (walls not reaching structure)" for heads C/F/G. The split is by head letter, not by whether the wall actually reaches structure. The take-off itself frames 19 head-C walls to the deck: Partition Takeoff height 22.83 ft, stud LF at full height, and L-bead "where the board meets exposed structure" (RFI-21). These 19 walls sit in the "standard … not reaching structure" rows:
* **3-5/8" (17 walls, 150.43 LF):** A-A435-2 6.73, A-A435-3 12.13, A-A422-2 20.17, A-A423-3 3.32, A-A423-6 5.13, A-A423-9 2.34, A-A424-1 12.25, A-A424-2 10.13, A-A424-3 12.25, A-A425-1 7.28, A-A425-2 14.76, A-A425-3 6.98, A-A425-4 1.49, A-A425-5 5.13, A-A426-1 21.00, A-A426-2 4.67, A-A426-3 4.67.
* **6" (2 walls, 16.15 LF):** A-A422-3 7.52, A-A422-4 8.63.
* **What the documents require:** spec 09 22 16 Part 3 "Slip-Type Head Joints: Where framing extends to overhead structural supports, install to produce joints at tops of framing systems that prevent axial loading of finished assemblies". D/A301 (2" SLIP TRACK at the roof deck) is the drawn condition for a partition at the deck.
* **Required correction:** move **150.43 LF** from "Top track 3-5/8" – standard" (290.72 → 140.29) to "Top slip / deflection track 3-5/8"" (240.96 → 391.39). Move **16.15 LF** from "Top track 6" – standard – per source" (53.43 → 37.28) to "Top slip / deflection track 6"" (393.29 → 409.44). The family total is unchanged at 1,104.77 LF.
* Where part of a wall reaches the deck (A-A435-1 Retail Storage segment 5.91 LF, studs to deck since rev1), that portion also needs slip track. This is an optional refinement: +5.91 LF slip / −5.91 LF standard.

All other new or changed items were checked and confirmed:
* **Blocking row:** now cites the A103 schedule keys (8, 50, 51, 52, 33, 45, 41, 18, 48, 7, 9, 16/A103) + 10/A505.B. Keys 51/52 (2 × 8.75 ft × 2 rows = 35.0 LF) are now hosted on A-A426-4 (Team Lounge 125 / Studio Entry wall, 12.46 LF, so an 8.75 ft run fits). The total stays 225.31 LF ✓.
* **L-bead row:** cites D/A301, E/A301, C/A301 and spec 09 29 00 3.1.C. "A2.23" now appears only inside two wall location texts, where it is a keynote reference, not a citation ✓.
* **Curved molding:** SC151220EQ 62.20 LF (my vector arc measure 62.05) + KAM151220E 396.71 LF; both products are in spec 09 51 23 2.6 ✓.
* **Framing screws:** +50 pieces (box headers, kickers, braces) × 4 = +200 ✓.

## Check 4 — MEP crossings (spot-check against M110)
I registered M110 to A101 myself from the grid bubbles: offset +6.9 / +36.7 pt, from 14 matching labels. This agrees with CAMBIOS.
* **A-A427-2 (31"):** a rectangular supply duct crosses the Group X / Recovery wall at diffuser tag 1. Confirmed. `img/rev2_chk4_M110_duct_crossing_A-A427-2.png`.
* **A-A425-2 (6"):** a small duct runs south through the Laundry 152 wall line. Confirmed. `img/rev2_chk4_M110_duct_crossing_A-A425-2.png`.
* **A-A424-1 (41"):** heavy parallel duct lines cross the wall line east of the grid line. Plausible; the exact width was not re-measured. `img/rev2_chk4_M110_duct_crossing_A-A424-1.png`.
* Result: 10 stud-reinforcement plates and 6 sleeves, MAX(1, ROUNDUP(w/16)) recomputed: 2 + 3 + 1 + 2 + 1 + 1 = 10 ✓. The unconfirmed candidates are carried as an RFI range ✓.

## Check 6 — format: PASS
Scanned every visible cell. These tokens are absent: R1-/R2- ids, soffit_side, skill, canon, .py, familias, votes, grep, mep.cruces, plantilla, internal status tokens, "A-A435-4". Three minor residuals do not block:
* Inventory tag ids "PT0009" (A-A422-5 location) and "PT0130" (RFI-31) are internal inventory numbers.
* ALC-05 says "Jamb studs counted by the tools".
* The hidden `_reglas` seal is kept by design.

## Check 8 — files: PASS
Takeoff_rev2.xlsx 54,644 B; Markups_rev2.pdf 220,450,979 B; imagenes_rev2/ 19 files; CAMBIOS_rev2.md 4,495 B; ENSAMBLE_CUADRE.md 16,688 B.

## Back-check registration / gates
Not registered, because check 3 fails on a real defect: the purchase split contradicts spec 09 22 16 and the take-off's own wall heights. Per the instruction, `reglas.py compuerta` and `bitacora.py compuerta` were not run. BACKCHECK_rev2.md is written and ready. After the 166.58 LF reclassification (no other change), register it on the corrected Excel and run the two gates.
