# CERTIFICADO DE AUDITORÍA — rev1 (Step 11 re-audit)
**Project:** Chuze Fitness Austin Bluffs. **Audited:** `5_entrega/Chuze_AustinBluffs_Takeoff_rev1.xlsx` (53,701 B), `Chuze_AustinBluffs_Markups_rev1.pdf` (220,451,000 B, 107 p., 109 annotations), `imagenes_rev1/` (19 files), `CAMBIOS_rev1.md`.
**Sources used:** the bid set, `plano/specs.pdf` (used only to verify the spec citations), the deliverables and CAMBIOS_rev1.md. The forbidden paths (2_lectura, 3_revision, 4_canon, other scratch folders, bn_ref) were not opened. Same rules and methods as the rev0 certificate. Each evidence image was reopened and checked after it was written.

## Result
| # | Check | rev0 | rev1 |
|---|---|---|---|
| 1 | Tag sweep | PASS | **PASS** (walls and markups unchanged: 97 elements + 12 legend lines) |
| 2 | Blind re-measurement | PASS | **PASS**. The Partition Takeoff is identical to rev0 in all 101 rows (LF, H, layers, stud, O.C., board SF): 1,006.72 LF partitions + 220.24 LF soffit sides. The same 2 sub-inch rows remain: A-A426-3 −0.10 LF (−2.1 %), A-A432-3 +0.06 LF (+3.4 %) |
| 3 | Detail chain | PASS | **PASS** (every new family checked against its detail; see below) |
| 4 | Scope sweep | FAIL | **PASS** (all 5 rev0 scope findings fixed; observations below) |
| 5 | Arithmetic | FAIL | **PASS** (every breakdown sums to its Net; yields exact; molding duplicate removed) |
| 6 | Format | FAIL | **FAIL (presentation)**: internal tokens and some citations, listed below |
| 7 | Bluebeam | FAIL | **PASS** (RCP calibration, arc and C3C boxes fixed) |
| 8 | Files | PASS | **PASS** |

## Check 3 — new families vs their N/SHEET (all confirmed)
* **Control joints:** 27/A101 (= A010 note 27, elevation general note 5). 363.93 LF = my rev0 figure of 336.3 LF on 8 walls + soffit sides A-A421.A-1 (2 joints × 10.83 = 21.66) and A-A423.A-1 (2 × 3.0 = 6.0). ✓
* **A502 MTL STUD BOX HEADER:** located on A502 by text position inside details 6 ("WALL BEYOND BOX HEADER"), 7, 13 and 15. It also appears in 5, 11 and 14, which are not called on any plan. 2 studs + 1 track × 117.1 LF (6: 5.33 + 5.00, 7: 15.94, 13: 77.50, 15: 13.33) = 234.2 LF stud + 117.1 LF track ✓. **Diagonal bracing @ 48"** is in 6 (also in 10, 11, 14, not called): 6 braces × 2.83 ft = 16.96 LF (RFI-35) ✓. `img/rev1_chk3_A502_box_header_6_7_15_diag_bracing_6.png`, `img/rev1_chk3_A502_13_box_header.png`.
* **Head F:** F/A301 "METAL EDGE, TYP." with the board drawn over the wall top. 2 × 22.41 = 44.82 LF edge + 11.13 SF Type X cap ✓. `img/rev1_chk3_A301_head_F_G_metal_edge.png`.
* **Head C kickers:** C/A301 "WALL BRACING – RE: STRUCT." (no structural brace detail in S100–S300, RFI-36). Recomputed for A-A421-15: ROUNDUP(20.13/4) + 1 = 7 kickers × √2 × (22.83 − 14.42) = 83.3 LF vs 83.26 ✓. Total 424.23 LF (3-5/8" 380.74 + 6" 43.49).
* **L-bead edge trim:** spec 09 29 00 3.1.C ("trim edges with edge trim where edges of panels are exposed" at structural abutments) and 2.6 L-Bead ✓. 1,290.95 LF along the faces finished to the deck (per-face breakdown).
* **Tile backer:** A301 type notes "PROVIDE 5/8" CEMENT BACKER BOARD BEHIND ALL TILE"; spec 09 29 00 2.5 Cementitious Backer Units, 5/8" ✓. 1,209.77 SF; screws 1.2/SF = 1,451.72 ✓.
* **RTU curb caps:** 2/A131 "600S162-33 STUD FRAME 12" OC … (2) #10 TCK SCREWS AT 6" OC" (`img/chk4_A131_…png`); 9 caps per AD103 D0.18. 9 × (20 + 7 × 4) = 432 LF ✓; TEK 9 × 108 = 972 ✓ (size assumed, RFI-14).
* **A103 metal backing:** 6 × 16 ga continuous track, tags 8, 18, 33, 41, 45, 48, 50, 51, 52 + metal strap tags 7, 9, 16 + 10/A505.B = 225.31 LF (RFI-13). My rev0 order-of-magnitude estimate was ~300 LF; 225 LF is plausible. Tags 1, 30, 36, 40, 46 and 55 have no occurrence on the A103 plan, which agrees with my rev0 tag count.
* **1/A506 roof hatch:** "16 GA x 4" LEGS DEFLECTION TRACK … ALL SIDES OF OPENING" + "16 GA TOP RUNNER TRACKS" ✓ (11 + 10 LF). `img/rev1_chk3_A506_1_hatch_16ga_4in_deflection_track.png`.
* **A-A435-1 Retail Storage 126 segment:** 6 studs × (22.83 − 10.50) = 73.98 LF ✓, + 3 bracing rows × 5.91 = 17.73 LF ✓.
* **Grid:** spec 09 51 23 2.6 product schedule lists HD8906 main runner, XL8945P 48" cross tee, KAM151220E knurled angle molding ✓. A single perimeter molding (458.91 LF) ✓.

## Check 4 — scope: PASS (rev0 findings closed)
Control joints ✓; A103 metal backing ✓ (RFI-13, RFI-28 and ALC-16 now consistent); curb caps ✓ (RFI-14 text matches the row); corner bead +247.32 LF (my rev0 estimate was ≈ +247) ✓; MR on the Men's Locker 128 soffit faces ✓ (MR 5,483.88 = 5,402.49 + 81.39).
Observations (estimator's call, not defects):
* **Gypsum behind the cement backer is not deducted** (1,209.77 SF, mostly MR). The A301 note puts the cement board behind tile in place of gypsum. Carrying both is conservative and documented in RFI-06. Possible delta: −1,209.77 SF of gypsum.
* The spec 09 51 23 schedule includes **SC151220EQ SimpleCurve knurled angle molding**. The reception circle (≈ 62 LF of arc) would take the curved product, not KAM151220E.
* Framing screws (4 × 1,235 pieces) cover only the partition / soffit studs + the A-A435-1 studs to deck. The new box-header, kicker and diagonal-brace studs (≈ 675 LF, roughly 70 pieces ≈ 280 screws) are not counted. Small.

## Check 5 — arithmetic: PASS
* Board 5,483.88 + 30,456.68 + 1,475.02 = 37,415.58 = rev0 37,404.45 + 11.13 (head F cap) ✓.
* Yields: drywall screws 1.2 × 37,415.58 = 44,898.7 ✓; compound 0.072 × 37,415.58 = 2,693.92 ✓; tape 0.37 × 37,415.58 = 13,843.76 ✓.
* Every Material Summary breakdown sums to its Net. Rows checked: tracks; studs 6" 11,246.87 + 432 = 11,678.87; 3-5/8" 10,545.09; 2-1/2" 2,009.04 (now with its per-wall breakdown); soffit track 567.58; bracing 5,390.39; MR / X / W.R.; cement board; control joint; corner bead 441.22; edge trim 1,335.77; blocking 225.31; #10 TEK 1,148. Each matches the CAMBIOS family table. The grid rows show their operation per area. The molding ratio is now 1.0 × perimeter ✓.

## Check 6 — format: FAIL (presentation; no quantity effect)
* 6 visible sheets in A301 schedule order, with subtotals, grand total (1,006.721 LF / 34,688.03 SF), English and a sheet citation on every Material Summary row ✓ (rev0 "default (no sheet)" rows fixed).
* **Internal process tokens still visible:**
  * The rev1 change ids **R1-BH, R1-BK, R1-CB, R1-CC, R1-CJ, R1-DB, R1-ET, R1-GS, R1-HF, R1-HT, R1-KC, R1-TB** appear 206 times across 15 Material Summary breakdown cells.
  * **"soffit_side"** is used as the scope label in 11 Partition Takeoff rows (e.g. "soffit_side #A-A424.A-2").
  * **"skill standing input / skill standing rule"** appears in 7 cells (Inputs B23/B24, Pending Items, Scope Checklist ALC-19 / ALC-X30 / ALC-X45 "the skill's cladding rule").
  * MEP registration diagnostics ("M110 dx −7.0 / dy −38.3 pt, 190/184 votes …") appear in Material Summary "Stud reinforcement at MEP penetrations" and Pending Items RFI-ACC-stud-reinforcement-mep, plus "grep 'ATM'" in the ATM row.
* **Traceability:** the metal blocking breakdown cites wall **"A-A435-4"** twice (2 × 17.5 LF, Team Lounge cabinets, tags 51/52). There is no such wall in the Partition Takeoff or the markups.
* **Citations:** the blocking row's N/SHEET cites only 10/A505.B; it should cite the A103 schedule / plan. The edge-trim row's N/SHEET includes "A2.23", which is a keynote, not a sheet.
* The hidden 7th sheet `_reglas` is still present (tool seal).
* Minor: Excel A-A426-2 / -3 stay at 4.67 LF each, while the rev1 3-side markups measure 4.59 / 4.57.

## Check 7 — Bluebeam: PASS
* All 11 RCP markups now carry Measure R = "1/4 in = 1 ft". Σ OTHER FRAMING Length is **220.23** vs Excel 220.24 (`img/rev1_chk7_A423A_calibrated_quarter_inch.png`).
* A-A421.A-1 is a 49-point arc lying 0.9–2.1 pt outside the fitted circle (R 13.83 ft), length 62.17 vs 62.2 LF (`img/rev1_chk7_A421A_…png`).
* The C3C boxes are open 3-side polylines: Σ 24.36 vs 24.54 (−0.7 %) (`img/rev1_chk7_A421_C3C_box_3_sides_4.77.png`).
* Every other type is within ±0.13 %. Subject / Page Label / Depth / NM are present on every wall markup. PDF keywords and creator are empty; the author field still holds the architect's original value.

## Check 8 — files: PASS
| File | Bytes |
|---|---|
| Chuze_AustinBluffs_Takeoff_rev1.xlsx | 53,701 |
| Chuze_AustinBluffs_Markups_rev1.pdf | 220,451,000 |
| imagenes_rev1/ (18 PNG + imagenes_resumen.json) | 19 files |
| CAMBIOS_rev1.md | 6,872 |
| ENSAMBLE_CUADRE.md | 13,844 |
| RESPUESTA_FINAL_rev1.md | 878 |
Note: the CAMBIOS family table includes Spanish labels ("todos los gauges", "track de ceilings"). This is an internal file, not the Excel.

## Back-check registration
Not registered. Check 6 still fails on real presentation defects that were explicitly in scope ("no internal tokens", sheet citations), and on one phantom wall id. Per the instruction, the back-check on rev1 and the `reglas.py compuerta` run wait for those fixes. BACKCHECK_rev1.md is written and ready; no quantity changes are needed.
