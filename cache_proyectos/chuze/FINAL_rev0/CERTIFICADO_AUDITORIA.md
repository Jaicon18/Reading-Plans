# CERTIFICADO DE AUDITORÍA — Step 11 independent final audit
**Project:** Chuze Fitness Austin Bluffs, 3630 Austin Bluffs Pkwy Unit #C190, Colorado Springs CO
**Audited deliverables:** `5_entrega/Chuze_AustinBluffs_Takeoff_rev0.xlsx` (sha256 2536ef0c6c7a…), `Chuze_AustinBluffs_Markups_rev0.pdf` (109 annotations), `imagenes/`, `ENSAMBLE_CUADRE.md`
**Plans:** `plano/bidset_SIN_MARKUPS.pdf` (106 p.). **Inputs used:** plans, deliverables, `1_inventario/inventario.json` only. Readings, resolution, canon, other scratch folders and other projects' take-offs were NOT opened.
**Auditor date:** 2026-11-01. Auditor scratch: `/tmp/chuze/scratch/AUD/` (scripts meas.py, reg.py, a101m.py, own2.py, cov.py, tags.py, final_rows.py).

## Method (blind)
* Every markup PolyLine was used only to LOCATE the wall. The auditor then measured the plan vectors himself: the wall's own gray poche (fill 0.754, perpendicular walls excluded) or, where the wall has no poche (low walls D3G/D6G, double-stud A2-3D, RCP soffit lines), the parallel wall lines and the perpendicular end lines. Scales verified from the sheet text: A101 3/32" (6.75 pt/ft); A421–A435 and A421.A–A425.A 1/4" (18 pt/ft); A432, A434 3/16" (13.5 pt/ft).
* Every enlarged sheet was registered onto A101 (translation from matching poche rectangles, 5–18 matches per sheet, scale 6.75/18) and every wall was re-measured a second time on A101. This catches walls cut by an enlarged-plan viewport (A421-14, A422-1, A422-6, A427-3).
* Tag sweep: the 150 inventory tags plus 2 ambiguous ones were each matched to the nearest same-type wall, on the same sheet or through the A101 registration. Every A101 poche rectangle 2 ft or longer was checked for a covering markup: none is uncovered.
* Each evidence image was reopened and checked after it was written (red circle = the item).

## Result

| # | Check | Result |
|---|---|---|
| 1 | Tag sweep (tags ↔ walls, untagged walls) | **PASS** |
| 2 | Blind vector re-measurement of every Partition Takeoff row (|Δ| ≤ 2 %) | **PASS** (89 rows: 87 within 2 %; 2 rows outside by ≤ 0.10 LF, below vector resolution, listed) |
| 3 | Detail chain (N/SHEET opened per family) | **PASS** (open RFIs carried) |
| 4 | Scope sweep G / AD / A / S vs Scope Checklist | **FAIL** (control joints, A103 metal backing, curb caps, corner bead, 81 SF MR) |
| 5 | Arithmetic (Material Summary from the Partition Takeoff) | **FAIL** (all totals recompute exactly; one unexplained 2× ratio: channel AND angle molding both = full C-5 perimeter, 458.91 LF each) |
| 6 | Format | **FAIL (minor)** (8 Material Summary rows have no N/SHEET source: "default (no sheet)"; 7th hidden sheet `_reglas`) |
| 7 | Bluebeam markups | **FAIL** (11 RCP soffit markups calibrated at 3/32" on 1/4" sheets; A421.A-1 drawn as the chord, not the arc; 5 C3C boxes drawn on 4 sides vs 3 sides in the Excel) |
| 8 | Files present / sizes | **PASS** |

The **measured quantities (LF per wall and per type) are confirmed**: auditor total 1,228.35 LF vs take-off 1,226.96 LF (+0.11 %). Every type is within ±0.81 %. The FAILs are missing accessory / backing scope, one duplicate grid molding line, source citations, and the markup calibration. None of them changes a measured wall length.

---

## Check 1 — Tag sweep: PASS
* Inventory: 150 partition tags + 2 ambiguous (A2-3D 11, A3C 32, A6C 5, A6D 56, B2E 8, C3C 13, C3D 8, D3G 8, D6F 4, D6G 2, X6D 3, C3G 0, D3F 0). Each tag resolves to a markup wall. Most are within 1–5 ft of a same-type polyline on their own sheet. The tags with no same-type markup on their own sheet point at a wall that was taken on another enlarged sheet:
  * A431 PT0009–0011 (A2-3D) → A-A422-5 / A-A426-6. A429 PT0095–0099 (A6D) → A-A427-2 (Group X east wall = Recovery west wall) and the A429/A421 storefront stubs. A434 PT0100–0103 (A6D) → A-A427-1 / A-A427-2. A434 PT0124–0125, A427 PT0120–0121 and A429 PT0122–0123 (C3C) → the column boxes A-A421-1 / A-A421-2. A435 PT0104 (A6D) → A-A426-4. A423 PT0130 (C3D) → A-A423-7/-8 (RFI-31). G003 PT0148 (X6D) = egress plan (A-A424-7). PA0002 (A432, ambiguous) → A-A421-10/-11.
  * Evidence: `img/chk1_A429_PT0095_A6D_tag_wall_taken_as_A427-2.png` (A6D/A429), `img/chk1_A434_PT0101_PT0124_tags_same_as_A421-1_A421-2.png` (C3C/A434).
* C3G and D3F: 0 tags on any plan (reason documented).
* Untagged new walls drawn on plan, all documented with an RFI: A-A101-1 (rev-8 cloud, door 141, RFI-20), A-A424-13/-14 and A-A425-5 (RFI-22), A-A434-1 (keynote A2.25 infill, RFI-24), and the `r` returns joined to their tagged wall.
* Reverse sweep: every A101 new-wall poche rectangle 2 ft or longer is covered by a mapped markup (0 uncovered). Evidence: `img/chk1_A101_overlay_SE_all_markups_mapped.png`, `img/chk1_A101_overlay_NE_all_markups_mapped.png` (A101).

## Check 2 — Blind re-measurement: PASS (2 rows listed)
* Rows outside ±2 % (absolute delta below 1.8 pt of vector resolution):
  * **A-A426-3** C3C (A426): 4.67 LF vs auditor 4.57 (3 exposed sides 2.89 + 0.84 + 0.84) = −0.10 LF, −2.1 %.
  * **A-A432-3** D3G (A432, 3/16"): 1.74 LF vs auditor 1.80 (from the face of A-A432-1 to the end cap) = +0.06 LF, +3.4 %.
* Elements that differ individually but match at Excel-row level, because the split point between a wall and its return differs: A-A424-5 / -5r (row 6.72 vs 6.65) and A-A424-10 / -10r (5.30 vs 5.38).
* Viewport-clipped walls, confirmed on A101: A-A422-1 56.44 vs 56.71 (+0.5 %, `img/chk2_A422_…png`, `img/chk2_A101_A-A422-1_…png`); A-A427-3 60.88 vs 61.15 (+0.4 %); A-A421-14 15.85 vs 15.85; A-A422-6 6.93 vs 6.90.
* Circular reception soffit A-A421.A-1 (16/A502, A421.A): circle fitted on 1,376 vector points, R = 13.83 ft; arc above the chord at y = 1707 pt = **62.05 LF vs 62.2 (−0.2 %)**. Evidence: `img/chk2_A421A_A-A421.A-1_…png`.
* Exact poche example: A-A421-15 poche runs 1412.2 → 1775.5 pt = 20.18 ft vs 20.13 (`img/chk2_A421_A-A421-15_…png`). C3C boxes are counted on 3 exposed sides (`img/chk2_A421_C3C_box_…png`).
* Totals per type (auditor vs Excel): A2-3D 98.03/98.05, A3C 206.63/206.17, A6C 23.96/23.83, A6D 391.81/391.07, B2E 103.99/103.96, C3C 24.34/24.54, C3D 44.90/44.86, D3G 60.13/60.01, D6F 22.39/22.41, D6G 26.61/26.44, X6D 5.37/5.37, soffit sides 220.19/220.24.
* Full per-row table: Appendix A. Per-markup table with the measuring method: Appendix B.
* Observation, not a measurement error: A-A427-3 (storefronts F / H) and A-A421-16 (storefront C) carry the storefront spans inside the A6D LF at full height. This is consistent with the standing order that board never deducts openings, and the wall above the storefront runs to the deck. Estimator to confirm.

## Check 3 — Detail chain: PASS
* **Studs (A301 p21):** sizes per the type schedules: A 3-5/8" / 6", B "2"" (loaded as 2-1/2", RFI-32), C 3-5/8", D 3-5/8" (D6F / D6G loaded at 6" by the tag key, RFI-03), X6D 6". Gauge and O.C. are not printed except the A2 note "MIN. 25 GAUGE 3-5/8" … 16" O.C. WITH LATERAL BRACING IN TWO ROWS" (RFI-04 / RFI-18 open). `img/chk3_A301_partition_schedules_types_A_B_C_D_X.png`.
* **Track:** heads D / E use a 2" SLIP TRACK (D/A301, E/A301), loaded as the top / deflection track, one per stud size. D6F uses 600T250-54 top and bottom track with (2) #10 TEK screws (C/S200, `img/chk3_S200_…png`); loaded at 22.41 LF + 128 TEK screws.
* **Board:** one layer of 5/8" each side; furring (B, C) one face; X6D 2 layers each side as drawn (RFI-07). MR per A111 note 3; DensArmor at the pool / spa rooms (sauna loaded as W.R.). Board on head C / E walls stops at ceiling + 6", which explains −5.6 % against an all-full-height bound (see BACKCHECK).
* **Bracing:** head C "WALL BRACING – RE: STRUCT."; A2 two rows. Loaded as 1-1/2" C.R. rows = ROUNDUP(H×12/48) − 1, which recomputes exactly.
* **Soffits A502:** 6" 20 GA @ 24" O.C., corner bead, DIAGONAL BRACING @ 48" O.C. (`img/chk3_A502_…png`). Studs for 6, 7, 8, 13, 15 and 16/A502 are in the 6" stud row; the diagonal bracing is carried as 2 × LF of C.R. channel (different product, same order of LF). Minor: the 3-5/8" member of 9/A502 (7.5 ft soffit) is not in the 3-5/8" stud row (< 10 LF).
* **S200 partial-height walls:** D6F key plan, grids 6–7 / A–B, 4'-4" / 3'-4" / 8'-0" / 3'-3" between HSS posts. Matches A-A429-6 / -7. HSS posts excluded (structural steel).

## Check 4 — Scope sweep: FAIL
Swept G001–G005, AD101–AD103, A000–A611, S100–S300 (text sweep plus details). Items found:
1. **Control joints, note 27** (A010 / A101 and every enlarged plan: "PROVIDE CONTROL JOINTS IN GYPSUM BOARD AT ALL RUNS OVER 30'-0""). ALC-18 says control joints are included, but the metal-trim breakdown holds only soffit corner bead. Auditor: 8 walls over 30 ft → ROUNDUP(L/30) − 1 joints × board face-height sum = **336.3 LF missing** (A-A422-5 45.7, A-A426-6 45.7, A-A435-1 25.0, A-A422-1 45.7, A-A427-2 45.7, A-A427-3 91.3, A-A427-6 14.5, A-A429-3 22.8). `img/chk4_A101_note27_control_joints_over_30ft.png`.
2. **A103 metal backing "IN WALL 6 X 16 GA CONT MTL TRACK"** (tags 1, 8, 18, 33, 36, 40, 41, 45, 46, 48, 50, 51, 52, 55: lockers, base and upper cabinets, cubbies, storage). This is cold-formed metal, so it is in scope. Excel: 0 LF, and there is no Material Summary row. The Excel contradicts itself: RFI-13 says "LOADED: millwork run length per elevation", RFI-28 says "backing loaded at the wall top, 9.99 LF", and ALC-16 says "0 LF loaded". Auditor order of magnitude: ~300 LF of 6" 16 ga track (≈ 12 plan tag occurrences × 1–3 rows × 10–15 ft runs; low confidence, needs the elevations). `img/chk4_A103_backing_schedule_6x16ga_cont_mtl_track.png`.
3. **RTU curb caps 2/A131** (600S162-33 stud frame @ 12" O.C.). RFI-14 says "LOADED: 9 curb caps, size PENDING", but there is no Material Summary row and no Scope Checklist line. Not quantifiable (size not printed). Fix the text or carry an allowance. `img/chk4_A131_600S162-33_curb_cap_RFI14_not_in_summary.png`.
4. **Corner bead at outside corners:** loaded only at the soffit bottoms (193.9 LF). Missing: the 5 C3C column boxes (2 exposed corners each: A421-1/-2 2 × 2 × 10 = 40, A426-2/-3 2 × 2 × 22.83 = 91.3, A423-9 2 × 11.5 = 23, total ≈ 154 LF) and the two cased openings (A426 6'-6" with head 9'-0" ≈ 49 LF; A429 8'-0" with head 7'-0" ≈ 44 LF). **≈ +247 LF.**
5. **MR at A111 note 3 (locker rooms):** soffit faces in Men's Locker 128 are loaded as Type X: A-A424.A-2 5.22 × 4.6 = 24.0 SF and A-A424.A-3 15.94 × 3.6 = 57.4 SF, so **81.4 SF Type X → MR** (no change to the total). `img/chk4_A111_note3_MR_locker_restroom_pool.png`.
* Correctly handled (PASS items): blocking (wood, EXCLUDED); headers (steel by others, RFI-12); access panel 1 + RFI-15; soffits A502; GWB ceilings C-5; Type X / 1 HR X6D (G003, UL U465); partial-height walls S200; demolition AD101 note 5 (furring removed to CMU; new B2E only where tagged, RFI-23 / RFI-26, `img/chk4_AD101_note5_…png`); insulation, ACT, FRP, tile, acoustical sealant and structural steel EXCLUDED as ordered.

## Check 5 — Arithmetic: FAIL (one unexplained ratio)
Recomputed from the Partition Takeoff:
* Track = Σ LF × rows (A2-3D × 2): 3-5/8" 196.10 + 206.17 + 24.54 + 44.86 + 60.01 = **531.68** ✓; 6" 23.83 + 391.07 + 26.44 + 5.37 = **446.71** ✓; 600T250-54 **22.41** ✓; 2-1/2" **103.96** ✓. Top track = bottom track ✓. Soffit track 440.48 = 2 × 220.24 ✓.
* Board: Σ Partition Takeoff board 34,688.03 SF + C-5 ceilings 1,024.02 SF (Type X 693.70 + W.R. 330.32) = **37,404.45** = MR 5,402.49 + X 30,526.94 + W.R. 1,475.02 ✓ (every wall in the breakdowns matches its row).
* Studs (per row (ROUNDUP(LF/OC) + 1) × H × rows): 3-5/8" 8,848 vs 10,090 (×1.14); 6" 9,942 vs 10,952 (×1.10); 2-1/2" 1,941 vs 2,009 (×1.035). The excess is jamb, corner and intersection studs; per-row ratio 0.9–2.0, and the 2.0 rows are short walls with doors or returns. ✓
* Bracing: partitions 4,874.1 + soffits 440.5 = 5,314.6 vs 5,372.66 (−1.1 %) ✓.
* Yields: drywall screws 1.2 × 37,404.4 = 44,885 ✓; framing screws 4 × 1,229 = 4,916 ✓; pins 1,104.77 / 1.3333 = 828.6 ✓; compound 0.072 × 37,404.4 = 2,693.1 ✓; tape 0.37 × 37,404.4 = 13,839.6 ✓; Pieces = ROUNDUP(Purchase / stock) ✓.
* **Out of range without an explanation:** *USG channel molding DGCM27* 458.91 LF **and** *USG angle molding DGWM24* 458.91 LF, each equal to the full C-5 perimeter (ratio 2.0 × perimeter). These are alternative perimeter trims; no detail calls for both. **Possible duplicate: −458.91 LF.**
* Warnings (explained in the row, estimator's call): main tee 523.35 LF for 1,024 SF (0.51 LF/SF, bounding box ROUNDUP + 1 per area; area method ≈ 300 LF); cross tee 969.8 LF (area method ≈ 770 LF); 187 hangers for 1,024 SF (≈ 5.5 SF per hanger vs 16 SF at 4' × 4').

## Check 6 — Format: FAIL (minor)
* Sheets: Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist = 6 visible ✓. There is also a 7th hidden sheet `_reglas` (tool seal). Deviation from "6 sheets": keep it hidden or move the seal out of the client file.
* Schedule order A2-3D, A3C, A6C, A6D, B2E, C3C, C3D, D3G, D6F, D6G, X6D ✓, then OTHER FRAMING. Subtotal per type ✓. Grand total (partitions) 1,006.721 LF / 34,688.03 SF ✓ (cached values present). OTHER FRAMING has no subtotal row.
* English ✓. Status tokens [DERIVED] / [CONFIRMED] / [RFI] ✓. Every Partition Takeoff row cites DETAIL/SHEET ✓.
* **Missing sources:** "N/SHEET: default (no sheet)" on *2-1/2" stud* (also has no breakdown), *Hanger wire*, *USG main tee*, *USG cross tee*, *channel molding*, *angle molding*, *hanger count* (should cite A121 / 09 51 23 / B2E A301 / A502), plus 4 zero rows.
* ENSAMBLE_CUADRE.md lists its own size as 10,272 bytes; the file is 10,319 bytes (stale self-reference).

## Check 7 — Bluebeam: FAIL
* 109 annotations = 97 wall / element PolyLines (= 97 elements; 89 Excel rows after joining the `r` returns) + 12 legend lines (page 107 "LEGEND"). Every wall markup has Subject = type ✓, Page Label = sheet ✓, Measure dictionary (scale / Length) ✓, Depth = height ✓, NM = wall id ✓, and Contents with LF / H / SF / detail ✓.
* **Scale error:** the 11 OTHER FRAMING markups on A421.A, A422.A, A423.A, A424.A and A425.A carry Measure R = "3/32 in = 1 ft" (C = 0.148148). These RCP sheets are 1/4" = 1'-0", so Bluebeam shows Length × 2.667. Example: A-A423.A-1 shows 206.67 ft against 77.50 LF (`img/chk7_A423A_…png`).
* **Geometry:** A-A421.A-1 is drawn as the 21.94 ft chord; the LF is the 62.2 ft arc. The C3C boxes A-A421-1/-2, A-A426-2/-3 and A-A423-9 are drawn on 4 sides (Length 7.77 / 7.77 / 7.49 / 7.47 / 3.17) while the Excel uses 3 sides (4.77 / 4.77 / 4.67 / 4.67 / 2.34).
* Σ per type, Bluebeam vs Excel: all other types within ±0.1 % (Appendix C). **C3C +50.7 %** (36.98 vs 24.54) and **OTHER FRAMING +117.9 %** (480.00 vs 220.24). Σ Wall Area (Length × Depth) matches the Contents SF (LF × H) to within 0.2 % for every type except C3C and OTHER FRAMING.

## Check 8 — Files: PASS
| File | Bytes |
|---|---|
| Chuze_AustinBluffs_Takeoff_rev0.xlsx | 49,409 |
| Chuze_AustinBluffs_Markups_rev0.pdf (107 pages, 109 annotations) | 220,449,999 |
| ENSAMBLE_CUADRE.md | 10,319 |
| RESPUESTA_FINAL.md | 1,417 |
| imagenes/ (A101, A421, A421.A, A422, A422.A, A423, A423.A, A424, A424.A, A425, A425.A, A426, A427, A429, A431, A432, A434, A435 *_walls_by_type.png + imagenes_resumen.json) | 19 files, 27.9 MB |
Local only. The Drive upload happens after this audit.


## Appendix A — Partition Takeoff rows: Excel vs auditor
| # | Excel row | Type | Sheet | Excel LF | Auditor LF | Δ % | Result |
|---|---|---|---|---|---|---|---|
| 1 | A-A422-5 | A2-3D | A422 | 32.42 | 32.41 | -0.0 | ok |
| 2 | A-A426-5 | A2-3D | A426 | 27.32 | 27.31 | -0.0 | ok |
| 3 | A-A426-6 | A2-3D | A426 | 38.31 | 38.31 | +0.0 | ok |
| 4 | A-A421-15 | A3C | A421 | 20.13 | 20.19 | +0.3 | ok |
| 5 | A-A422-2 | A3C | A422 | 20.17 | 20.17 | +0.0 | ok |
| 6 | A-A423-6 | A3C | A423 | 5.13 | 5.13 | +0.0 | ok |
| 7 | A-A424-1 | A3C | A424 | 12.25 | 12.36 | +0.9 | ok |
| 8 | A-A424-2 | A3C | A424 | 10.13 | 10.12 | -0.1 | ok |
| 9 | A-A424-3 | A3C | A424 | 12.25 | 12.36 | +0.9 | ok |
| 10 | A-A424-5+A-A424-5r | A3C | A424 | 6.72 | 6.65 | -1.0 | ok |
| 11 | A-A424-6 | A3C | A424 | 5.37 | 5.37 | -0.0 | ok |
| 12 | A-A424-13+A-A424-13r | A3C | A424 | 2.66 | 2.67 | +0.4 | ok |
| 13 | A-A424-14+A-A424-14r | A3C | A424 | 2.65 | 2.65 | +0.0 | ok |
| 14 | A-A425-1 | A3C | A425 | 7.28 | 7.28 | -0.0 | ok |
| 15 | A-A425-2 | A3C | A425 | 14.76 | 14.76 | -0.0 | ok |
| 16 | A-A425-3 | A3C | A425 | 6.98 | 6.97 | -0.1 | ok |
| 17 | A-A425-4 | A3C | A425 | 1.49 | 1.49 | +0.1 | ok |
| 18 | A-A425-5 | A3C | A425 | 5.13 | 5.13 | -0.1 | ok |
| 19 | A-A426-1 | A3C | A426 | 21.00 | 21.00 | +0.0 | ok |
| 20 | A-A435-1 | A3C | A435 | 33.21 | 33.27 | +0.2 | ok |
| 21 | A-A435-2 | A3C | A435 | 6.73 | 6.83 | +1.5 | ok |
| 22 | A-A435-3 | A3C | A435 | 12.13 | 12.23 | +0.8 | ok |
| 23 | A-A421-13 | A6C | A421 | 7.68 | 7.79 | +1.4 | ok |
| 24 | A-A422-3 | A6C | A422 | 7.52 | 7.52 | +0.0 | ok |
| 25 | A-A422-4 | A6C | A422 | 8.63 | 8.65 | +0.2 | ok |
| 26 | A-A101-1 | A6D | A101 | 5.23 | 5.23 | +0.0 | ok |
| 27 | A-A421-6 | A6D | A421 | 26.41 | 26.41 | +0.0 | ok |
| 28 | A-A421-7 | A6D | A421 | 2.96 | 2.95 | -0.3 | ok |
| 29 | A-A421-8 | A6D | A421 | 2.96 | 2.95 | -0.3 | ok |
| 30 | A-A421-9 | A6D | A421 | 5.08 | 5.08 | +0.0 | ok |
| 31 | A-A421-10 | A6D | A421 | 13.46 | 13.47 | +0.1 | ok |
| 32 | A-A421-11 | A6D | A421 | 21.23 | 21.17 | -0.3 | ok |
| 33 | A-A421-12 | A6D | A421 | 7.68 | 7.79 | +1.4 | ok |
| 34 | A-A421-14 | A6D | A421 | 15.85 | 15.85 | +0.0 | ok |
| 35 | A-A421-16 | A6D | A421 | 12.17 | 12.23 | +0.5 | ok |
| 36 | A-A422-1 | A6D | A422 | 56.44 | 56.71 | +0.5 | ok |
| 37 | A-A423-1 | A6D | A423 | 9.98 | 9.97 | -0.1 | ok |
| 38 | A-A423-2 | A6D | A423 | 3.16 | 3.16 | +0.0 | ok |
| 39 | A-A423-4 | A6D | A423 | 2.91 | 2.91 | +0.0 | ok |
| 40 | A-A423-5 | A6D | A423 | 5.17 | 5.13 | -0.8 | ok |
| 41 | A-A424-8 | A6D | A424 | 15.34 | 15.39 | +0.3 | ok |
| 42 | A-A424-9 | A6D | A424 | 10.71 | 10.71 | +0.0 | ok |
| 43 | A-A424-11 | A6D | A424 | 3.40 | 3.40 | +0.0 | ok |
| 44 | A-A424-12+A-A424-12r | A6D | A424 | 4.64 | 4.69 | +1.1 | ok |
| 45 | A-A426-4 | A6D | A426 | 12.46 | 12.53 | +0.6 | ok |
| 46 | A-A427-1 | A6D | A427 | 26.92 | 26.95 | +0.1 | ok |
| 47 | A-A427-2 | A6D | A427 | 36.57 | 36.57 | +0.0 | ok |
| 48 | A-A427-3 | A6D | A427 | 60.88 | 61.15 | +0.4 | ok |
| 49 | A-A429-4 | A6D | A429 | 10.77 | 10.76 | -0.1 | ok |
| 50 | A-A429-5 | A6D | A429 | 15.54 | 15.49 | -0.3 | ok |
| 51 | A-A434-1 | A6D | A434 | 3.16 | 3.16 | +0.0 | ok |
| 52 | A-A423-10 | B2E | A423 | 4.64 | 4.64 | +0.0 | ok |
| 53 | A-A427-6 | B2E | A427 | 34.29 | 34.35 | +0.2 | ok |
| 54 | A-A429-1 | B2E | A429 | 16.92 | 16.95 | +0.2 | ok |
| 55 | A-A429-2 | B2E | A429 | 15.05 | 15.00 | -0.3 | ok |
| 56 | A-A429-3 | B2E | A429 | 33.06 | 33.05 | -0.0 | ok |
| 57 | A-A421-1 | C3C | A421 | 4.77 | 4.76 | -0.2 | ok |
| 58 | A-A421-2 | C3C | A421 | 4.77 | 4.76 | -0.2 | ok |
| 59 | A-A423-3 | C3C | A423 | 3.32 | 3.32 | +0.0 | ok |
| 60 | A-A423-9 | C3C | A423 | 2.34 | 2.34 | +0.0 | ok |
| 61 | A-A426-2 | C3C | A426 | 4.67 | 4.59 | -1.7 | ok |
| 62 | A-A426-3 | C3C | A426 | 4.67 | 4.57 | -2.1 | OUT >2% |
| 63 | A-A422-6 | C3D | A422 | 6.93 | 6.90 | -0.4 | ok |
| 64 | A-A423-7+A-A423-7r | C3D | A425 | 2.68 | 2.68 | -0.0 | ok |
| 65 | A-A423-8+A-A423-8r | C3D | A425 | 2.68 | 2.68 | -0.0 | ok |
| 66 | A-A424-10+A-A424-10r | C3D | A424 | 5.30 | 5.38 | +1.5 | ok |
| 67 | A-A431-1 | C3D | A431 | 10.06 | 10.05 | -0.1 | ok |
| 68 | A-A431-2 | C3D | A431 | 17.21 | 17.21 | +0.0 | ok |
| 69 | A-A421-3 | D3G | A421 | 28.34 | 28.34 | +0.0 | ok |
| 70 | A-A421-4 | D3G | A421 | 1.71 | 1.71 | +0.0 | ok |
| 71 | A-A421-5 | D3G | A421 | 1.71 | 1.71 | +0.0 | ok |
| 72 | A-A432-1+A-A432-2 | D3G | A432 | 26.51 | 26.57 | +0.2 | ok |
| 73 | A-A432-3 | D3G | A432 | 1.74 | 1.80 | +3.4 | OUT >2% |
| 74 | A-A429-6 | D6F | A429 | 16.92 | 16.95 | +0.2 | ok |
| 75 | A-A429-7 | D6F | A429 | 5.49 | 5.44 | -0.9 | ok |
| 76 | A-A429-11 | D6G | A429 | 19.87 | 19.92 | +0.3 | ok |
| 77 | A-A429-11r | D6G | A429 | 6.57 | 6.69 | +1.8 | ok |
| 78 | A-A424-7 | X6D | A424 | 5.37 | 5.37 | -0.0 | ok |
| 79 | A-A421.A-1 | OTHER FRAMING - SOFFIT SIDE | A421.A | 62.20 | 62.05 | -0.2 | ok |
| 80 | A-A421.A-2 | OTHER FRAMING - SOFFIT SIDE | A421.A | 14.39 | 14.39 | +0.0 | ok |
| 81 | A-A421.A-3 | OTHER FRAMING - SOFFIT SIDE | A421.A | 7.50 | 7.50 | +0.0 | ok |
| 82 | A-A422.A-1 | OTHER FRAMING - SOFFIT SIDE | A422.A | 13.33 | 13.33 | +0.0 | ok |
| 83 | A-A423.A-1 | OTHER FRAMING - SOFFIT SIDE | A423.A | 77.50 | 77.60 | +0.1 | ok |
| 84 | A-A423.A-2 | OTHER FRAMING - SOFFIT SIDE | A423.A | 9.00 | 9.00 | +0.0 | ok |
| 85 | A-A424.A-1 | OTHER FRAMING - SOFFIT SIDE | A424.A | 5.33 | 5.33 | +0.0 | ok |
| 86 | A-A424.A-2 | OTHER FRAMING - SOFFIT SIDE | A424.A | 5.22 | 5.22 | +0.0 | ok |
| 87 | A-A424.A-3 | OTHER FRAMING - SOFFIT SIDE | A424.A | 15.94 | 15.94 | +0.0 | ok |
| 88 | A-A425.A-1 | OTHER FRAMING - SOFFIT SIDE | A425.A | 4.83 | 4.83 | +0.0 | ok |
| 89 | A-A425.A-2 | OTHER FRAMING - SOFFIT SIDE | A425.A | 5.00 | 5.00 | +0.0 | ok |

## Appendix B — Per markup: Bluebeam Length, content LF, auditor LF and method
| Markup (NM) | Type | Page label | Bluebeam Length (Measure) | Content LF | Auditor LF | Method |
|---|---|---|---|---|---|---|
| A-A101-1 | A6D | A101 | 5.23 | 5.23 | 5.23 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-1 | C3C | A421 | 7.77 | 4.77 | 4.76 | 3 exposed sides of box from markup vertices 3.00+0.88+0.88 (4th side against storefront wall) |
| A-A421-2 | C3C | A421 | 7.77 | 4.77 | 4.76 | 3 exposed sides 3.00+0.88+0.88 |
| A-A421-3 | D3G | A421 | 28.34 | 28.34 | 28.34 | sheet lines, end on perpendicular line (low wall drawn without poche) |
| A-A421-4 | D3G | A421 | 1.71 | 1.71 | 1.71 | sheet lines from face of A421-3 |
| A-A421-5 | D3G | A421 | 1.71 | 1.71 | 1.71 | sheet lines from face of A421-3 |
| A-A421-6 | A6D | A421 | 26.41 | 26.41 | 26.41 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-7 | A6D | A421 | 2.89 | 2.96 | 2.95 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-8 | A6D | A421 | 2.94 | 2.96 | 2.95 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-9 | A6D | A421 | 5.08 | 5.08 | 5.08 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-10 | A6D | A421 | 13.41 | 13.46 | 13.47 | A101 lines end 13.47 |
| A-A421-11 | A6D | A421 | 21.23 | 21.23 | 21.17 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-12 | A6D | A421 | 7.68 | 7.68 | 7.79 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-13 | A6C | A421 | 7.68 | 7.68 | 7.79 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-14 | A6D | A421 | 15.85 | 15.85 | 15.85 | A101 poche (A421 viewport clips the wall at 9.5 ft) |
| A-A421-15 | A3C | A421 | 20.13 | 20.13 | 20.19 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421-16 | A6D | A421 | 12.17 | 12.17 | 12.23 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A421.A-1 | OTHER FRAMING - SOFFIT SIDE | A421.A | 58.52 | 62.20 | 62.05 | arc of circular C-5 ceiling above chord: R 13.83 ft fitted on 1,376 vector points; chord y=1707 |
| A-A421.A-2 | OTHER FRAMING - SOFFIT SIDE | A421.A | 38.37 | 14.39 | 14.39 | dashed soffit line at 1/4" (markup length / 2.667) |
| A-A421.A-3 | OTHER FRAMING - SOFFIT SIDE | A421.A | 20.00 | 7.50 | 7.50 | dashed soffit line at 1/4" |
| A-A422-1 | A6D | A422 | 56.44 | 56.44 | 56.71 | A101 poche 0..56.71 (A422 viewport clips at 50.0 ft; continues on A431 to A2-3D) |
| A-A422-2 | A3C | A422 | 20.17 | 20.17 | 20.17 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A422-3 | A6C | A422 | 7.52 | 7.52 | 7.52 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A422-4 | A6C | A422 | 8.65 | 8.63 | 8.65 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A422-5 | A2-3D | A422 | 32.42 | 32.42 | 32.41 | sheet lines 0..32.41 (double-stud wall drawn as lines) |
| A-A422-6 | C3D | A422 | 6.93 | 6.93 | 6.90 | A101 poche (A422 viewport clips at 3.9 ft) |
| A-A422.A-1 | OTHER FRAMING - SOFFIT SIDE | A422.A | 35.56 | 13.33 | 13.33 | soffit line at 1/4" |
| A-A423-1 | A6D | A423 | 9.98 | 9.98 | 9.97 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-2 | A6D | A423 | 3.16 | 3.16 | 3.16 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-3 | C3C | A423 | 3.32 | 3.32 | 3.32 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-4 | A6D | A423 | 2.91 | 2.91 | 2.91 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-5 | A6D | A423 | 5.13 | 5.17 | 5.13 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-6 | A3C | A423 | 5.13 | 5.13 | 5.13 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-9 | C3C | A423 | 3.17 | 2.34 | 2.34 | 3 exposed sides 0.82+0.76+0.76 |
| A-A423-10 | B2E | A423 | 4.64 | 4.64 | 4.64 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423.A-1 | OTHER FRAMING - SOFFIT SIDE | A423.A | 206.67 | 77.50 | 77.60 | headwall line x 1347..2744 pt at 1/4" (visual + dims) |
| A-A423.A-2 | OTHER FRAMING - SOFFIT SIDE | A423.A | 24.00 | 9.00 | 9.00 | soffit line at 1/4" |
| A-A424-1 | A3C | A424 | 12.36 | 12.25 | 12.36 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-2 | A3C | A424 | 10.12 | 10.13 | 10.12 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-3 | A3C | A424 | 12.36 | 12.25 | 12.36 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-5 | A3C | A424 | 4.96 | 4.96 | 4.53 | own poche (split point with 5r differs; row sum checked) |
| A-A424-5r | A3C | A424 | 1.76 | 1.76 | 2.12 | own poche |
| A-A424-6 | A3C | A424 | 5.37 | 5.37 | 5.37 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-7 | X6D | A424 | 5.37 | 5.37 | 5.37 | sheet lines end 5.37, start at face of wall (dims 1'-0" + 4'-6") |
| A-A424-8 | A6D | A424 | 15.39 | 15.34 | 15.39 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-9 | A6D | A424 | 10.71 | 10.71 | 10.71 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-10 | C3D | A424 | 3.76 | 3.71 | 3.45 | own poche |
| A-A424-10r | C3D | A424 | 1.59 | 1.59 | 1.93 | own poche |
| A-A424-11 | A6D | A424 | 3.40 | 3.40 | 3.40 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-12 | A6D | A424 | 3.40 | 3.40 | 3.40 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-12r | A6D | A424 | 1.24 | 1.24 | 1.29 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-13 | A3C | A424 | 2.08 | 2.08 | 2.08 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-13r | A3C | A424 | 0.58 | 0.58 | 0.59 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-14 | A3C | A424 | 2.08 | 2.08 | 2.08 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424-14r | A3C | A424 | 0.57 | 0.57 | 0.57 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A424.A-1 | OTHER FRAMING - SOFFIT SIDE | A424.A | 14.22 | 5.33 | 5.33 | soffit line at 1/4" |
| A-A424.A-2 | OTHER FRAMING - SOFFIT SIDE | A424.A | 13.93 | 5.22 | 5.22 | soffit line at 1/4" |
| A-A424.A-3 | OTHER FRAMING - SOFFIT SIDE | A424.A | 42.52 | 15.94 | 15.94 | soffit line at 1/4" |
| A-A423-7 | C3D | A425 | 2.07 | 2.07 | 2.07 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-7r | C3D | A425 | 0.61 | 0.61 | 0.61 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-8 | C3D | A425 | 2.07 | 2.07 | 2.07 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A423-8r | C3D | A425 | 0.61 | 0.61 | 0.61 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A425-1 | A3C | A425 | 7.28 | 7.28 | 7.28 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A425-2 | A3C | A425 | 14.76 | 14.76 | 14.76 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A425-3 | A3C | A425 | 6.98 | 6.98 | 6.97 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A425-4 | A3C | A425 | 1.49 | 1.49 | 1.49 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A425-5 | A3C | A425 | 5.13 | 5.13 | 5.13 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A425.A-1 | OTHER FRAMING - SOFFIT SIDE | A425.A | 12.89 | 4.83 | 4.83 | soffit line at 1/4" |
| A-A425.A-2 | OTHER FRAMING - SOFFIT SIDE | A425.A | 13.33 | 5.00 | 5.00 | soffit line at 1/4" |
| A-A426-1 | A3C | A426 | 21.00 | 21.00 | 21.00 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A426-2 | C3C | A426 | 7.49 | 4.67 | 4.59 | 3 exposed sides 2.91+0.84+0.84 |
| A-A426-3 | C3C | A426 | 7.47 | 4.67 | 4.57 | 3 exposed sides 2.89+0.84+0.84 |
| A-A426-4 | A6D | A426 | 12.46 | 12.46 | 12.53 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A426-5 | A2-3D | A426 | 27.36 | 27.32 | 27.31 | A101 poche 0..27.31 |
| A-A426-6 | A2-3D | A426 | 38.31 | 38.31 | 38.31 | sheet lines to 38.31 (start at perpendicular wall) |
| A-A427-1 | A6D | A427 | 26.94 | 26.92 | 26.95 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A427-2 | A6D | A427 | 36.57 | 36.57 | 36.57 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A427-3 | A6D | A427 | 60.88 | 60.88 | 61.15 | A101 poche 0.05..61.20 (A427 viewport clips at 55.8 ft); includes storefront F/H spans |
| A-A427-6 | B2E | A427 | 34.29 | 34.29 | 34.35 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A429-1 | B2E | A429 | 16.95 | 16.92 | 16.95 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A429-2 | B2E | A429 | 15.00 | 15.05 | 15.00 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A429-3 | B2E | A429 | 33.05 | 33.06 | 33.05 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A429-4 | A6D | A429 | 10.76 | 10.77 | 10.76 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A429-5 | A6D | A429 | 15.49 | 15.54 | 15.49 | collinear poche A429-6+A429-5 = 32.44; type change at D6F/A6D |
| A-A429-6 | D6F | A429 | 16.95 | 16.92 | 16.95 | poche start at perpendicular wall; type change at A429-5 |
| A-A429-7 | D6F | A429 | 5.49 | 5.49 | 5.44 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A429-11 | D6G | A429 | 19.87 | 19.87 | 19.92 | sheet lines |
| A-A429-11r | D6G | A429 | 6.57 | 6.57 | 6.69 | sheet lines |
| A-A431-1 | C3D | A431 | 10.06 | 10.06 | 10.05 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A431-2 | C3D | A431 | 17.21 | 17.21 | 17.21 | sheet lines + poche 7.2..17.2, ends on perpendicular lines (visual) |
| A-A432-1 | D3G | A432 | 24.82 | 24.82 | 24.82 | sheet lines |
| A-A432-2 | D3G | A432 | 1.69 | 1.69 | 1.75 | sheet lines from face of A432-1 to end cap |
| A-A432-3 | D3G | A432 | 1.74 | 1.74 | 1.80 | sheet lines from face of A432-1 to end cap |
| A-A434-1 | A6D | A434 | 3.16 | 3.16 | 3.16 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A435-1 | A3C | A435 | 33.23 | 33.21 | 33.27 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A435-2 | A3C | A435 | 6.73 | 6.73 | 6.83 | sheet-poche (own poche of the wall, perpendicular walls excluded) |
| A-A435-3 | A3C | A435 | 12.13 | 12.13 | 12.23 | sheet-poche (own poche of the wall, perpendicular walls excluded) |

## Appendix C — Bluebeam sums per type
| Subject (type) | Markups | Σ Bluebeam Length | Excel LF | Δ % | Σ Wall area (Length x Depth) | Σ SF in markup text (LF x H) | Excel board SF (all faces) |
|---|---|---|---|---|---|---|---|
| A2-3D | 3 | 98.08 | 98.05 | +0.0 | 2239.3 | 2238.4 | 4476.98 |
| A3C | 22 | 206.43 | 206.17 | +0.1 | 3939.0 | 3933.4 | 6437.09 |
| A6C | 3 | 23.85 | 23.83 | +0.1 | 465.7 | 465.3 | 672.74 |
| A6D | 27 | 390.93 | 391.07 | -0.0 | 8874.9 | 8878.2 | 17733.80 |
| B2E | 5 | 103.93 | 103.96 | -0.0 | 2372.8 | 2373.4 | 2049.34 |
| C3C | 6 | 36.98 | 24.54 | +50.7 | 652.8 | 442.6 | 382.01 |
| C3D | 9 | 44.91 | 44.86 | +0.1 | 1025.2 | 1024.2 | 1024.12 |
| D3G | 6 | 60.02 | 60.01 | +0.0 | 300.1 | 300.1 | 609.90 |
| D6F | 2 | 22.44 | 22.41 | +0.1 | 269.3 | 268.9 | 543.96 |
| D6G | 2 | 26.44 | 26.44 | -0.0 | 132.2 | 132.3 | 267.45 |
| X6D | 1 | 5.37 | 5.37 | +0.0 | 122.7 | 122.7 | 490.64 |
| OTHER FRAMING - SOFFIT SIDE | 11 | 480.00 | 220.24 | +117.9 | 5723.4 | 2582.0 | 1692.40 |

## Evidence images (img/)
* chk1_A101_overlay_NE_all_markups_mapped.png
* chk1_A101_overlay_SE_all_markups_mapped.png
* chk1_A429_PT0095_A6D_tag_wall_taken_as_A427-2.png
* chk1_A434_PT0101_PT0124_tags_same_as_A421-1_A421-2.png
* chk2_A101_A-A422-1_full_length_56.71_vs_56.44.png
* chk2_A421A_A-A421.A-1_circular_soffit_arc_62.05_vs_62.2_markup_is_chord.png
* chk2_A421_A-A421-15_poche_20.18_vs_20.13.png
* chk2_A421_C3C_box_A-A421-1_3_sides_4.76_LF.png
* chk2_A422_A-A422-1_runs_past_viewport_clip_checked_on_A101.png
* chk3_A301_partition_schedules_types_A_B_C_D_X.png
* chk3_A502_soffit_6in_20ga_24oc_diagonal_bracing_48oc.png
* chk3_S200_600T250-54_partial_height_wall.png
* chk4_A101_note27_control_joints_over_30ft.png
* chk4_A103_backing_schedule_6x16ga_cont_mtl_track.png
* chk4_A111_note3_MR_locker_restroom_pool.png
* chk4_A131_600S162-33_curb_cap_RFI14_not_in_summary.png
* chk4_AD101_note5_remove_furring_to_CMU.png
* chk7_A423A_soffit_markup_scale_3-32_on_quarter_inch_sheet.png
