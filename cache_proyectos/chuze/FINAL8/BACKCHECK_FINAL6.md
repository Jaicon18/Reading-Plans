# BACKCHECK FINAL6 — independent back-check, Chuze Fitness Austin Bluffs
Excel: `5_entrega/Chuze_AustinBluffs_Takeoff_FINAL6.xlsx` (rebuilt 22:29, after REBUILT.flag). Markups: `Chuze_AustinBluffs_Markups_FINAL6.pdf` (22:29). Base: BACKCHECK_FINAL5.md.
FINAL6 has two changes: (1) 257 canon heights stored rounded → exact ft-in (list `takeoff_canon.json.alturas_exactas.json`); (2) a second MR face on 7 type-A walls at A424 (A/A301 "- BOTH SIDES"). Change 1 was audited against `scratch/E45/canon_pre_FINAL6.json`, change 2 against `canon_pre_FINAL6b.json` and a snapshot of the change-1-only Excel (`scratch/AUD6/FINAL6a_snapshot.xlsx`). Scripts are in `scratch/AUD6/`. Crops are in `6_auditoria/img_final6/`. I did not read CAMBIOS_FINAL6.md until my own numbers were done; its Material Summary table matches them.

## 0. Canon diff (auditor)
- pre → post (change 1): 257 float changes. Each one is in the producer's list with identical before/after values (245 `height_ft`, 12 `head_ft`), and nothing else changed. All 255 deltas are ≤ 0.0034 ft. Exceptions: the two soffit faces A-A424.A-2 (4.6 → 4.5833) and A-A424.A-3 (3.6 → 3.5833), each −0.0167 ft. These correct a 1-decimal rounding and are verified against the print below.
- **Not converted (still 22.83, 22'-10" rounded):** `deck_height.value` = 22.83. The 15 `ceilings[].hanger_drop_ft` keep 10.83 / 13.83 / 14.33 / 12.83 / 14.83. So do the `misc_items` ops built from "deck 22.83": head-C kickers [56–62], Retail Storage 126 studs [63], control joints [2–10], and `trim_items` [130–131] (corner bead 2 × 22.83). The values 14.83 and 13.83 were made exact on the soffit walls but left rounded in the hanger drops.
- pre6b → post (change 2): 7 `faces` arrays changed, and nothing else. Each wall gets one new face B that is a copy of face A, with only side / room / source text changed.

## 1. Partition Takeoff FINAL5 vs FINAL6, row by row (146 rows)
| Check | FINAL5 | FINAL6 | Auditor | Δ | Comment |
|---|---|---|---|---|---|
| Length (LF), Type, Wall #, Stud, O.C. | 146 rows | identical | identical | 0 | |
| Layers (board faces) | — | 4 rows 1 → 2 | A-A424-6, -12+12r, -13+13r, -14+14r | — | change 2 only (this column is the count of boarded faces) |
| Height (FT) | 82 rows changed | 22.83 → 22.833 (wall rows, 3 dec), 22.8333 (EX rows), 14.42 → 14.417, 12.58 → 12.583, 10.83 → 10.833, 12.83/13.83/14.33/14.83/11.33 → x.x33 | every changed row maps to a canon height change; 16 rows already at 22.833 / 12.583 show no visible change (canon 22.833 → 22.8333) | max 0.0033 ft | ≤ 0.005 OK. The wall rows still store 3 decimals (22.833) while the EX rows store 22.8333. This is cosmetic. |
| Board (SF), change 1 | — | 89 rows | Σ face LF × layers × Δh per face, wall by wall | all within 0.02 SF | per-face 2-dec rounding (A-A426-2/-3 0.03 vs 0.015, A-A423-4 0.00 vs 0.019) |
| Board (SF), change 2 | 48.35 / 105.94 / 32.12 / 32.02 | 96.70 / 211.88 / 64.24 / 64.04 | 5.372 × 9.0; 3.4 × 22.8333 + 1.24 × 22.8333; 2.078 × 12.0833 + 0.58 × 12.0833; 2.08 × 12.0833 + 0.57 × 12.0833 | 0 | +218.43 SF MR |
| Location text | — | A-A424.A-2 "4.6 ft" → "4.58"; A-A424.A-3 "3.6" → "3.58"; 4 rows list face B | — | — | consistent |
| Any other difference | | | none | | |

## 2. Printed heights (crops in img_final6/)
| Height | Canon source cites | What the print shows (crop) | Exact = print? |
|---|---|---|---|
| 22'-10" (22.8333) | A423.B / A425.A/B "B.O. DECK 22'-10" VARIOUS" | A423.B and A425.B print only "B.O. DECK / VARIOUS". The 22'-10" string is in the text layer under VARIOUS and does not render (h01, h02, h09, h13). It is visibly printed on **A429.B** as "EL.+ 22'-10"" at the deck (h11). | YES (A429.B). The cited sheets are hidden text. |
| 14'-5" (14.4167) | A422.C elev 6 "B.O. DECK 14'-5" VARIOUS", height_status CONFIRMED | A422.C prints only "B.O. DECK / VARIOUS". The 14'-5" exists only as text hidden under VARIOUS (h03, h10). It is not visible anywhere in the set. | **NOT CONFIRMABLE by print** (carried over from FINAL5; the conversion itself matches the hidden text) |
| 12'-1" (12.0833) | A421.A tag at 105 Family Restroom | "12'-1" AFF C-5 P-4" printed (h04); A424.A "12'-1" EXISTING C-3" Men's Locker 128 (h06) | YES |
| 12'-7" (12.5833) | 12'-1" + 6" (head C) | 12'-1" printed (h04, h06) + 6" = 12'-7" | YES |
| 7'-2" (7.1667) | A601 door 105/106 3'-0" × 7'-0" + 2" frame (6/A602) | A601 rows 105 FAMILY RESTROOM WD1 and 106 SMOOTHIE STORAGE LV1 print 7'-0" (h05). 7'-0" + 2" = 7'-2". | YES (derived) |
| 14'-10" (14.8333) | 22'-10" − 8'-0" (A-A424.A-1, 6/A502) | A424.A "8'-0" AFF C-5" at the 6/A502 box (h07) | YES (derived from a printed value) |
| 4'-7" (4.5833) | 12'-1" + 6" − 8'-0" (A-A424.A-2, 16/A502) | "12'-1" EXISTING" (h06) and "8'-0" EXISTING" corridor (h07) | YES (old 4.6 was off by 0.0167) |
| 3'-7" (3.5833) | 12'-1" + 6" − 9'-0" (A-A424.A-3, 7/A502) | "9'-0" AFF C-5 P-1" at the 7/A502 headwall, 12'-1" locker room (h06) | YES |

## 3. Material Summary FINAL5 vs FINAL6 (FINAL5 | FINAL6 | Auditor | Δ | Comment)
| Family | FINAL5 | FINAL6 | Auditor | Δ | Comment |
|---|---|---|---|---|---|
| 2-1/2" stud | 2,009.04 | 2,009.34 | Σ pcs × Δh: 27 + 15 + 15 + 26 + 5 = 88 pcs × 0.00333 = +0.29 | 0.01 | OK |
| 6" stud per source | 10,858.76 | 10,860.38 | wall terms +1.54 (pcs × Δh) + cripples under the 7'-2" heads; kicker A-A421-13 at the exact deck −0.009 | 0.08 | OK (< 0.1) |
| 6" 600S125-30 | 388.11 | 388.17 | 17 pcs × 0.00333 = +0.06 | 0 | OK |
| 3-5/8" stud per source | 3,170.24 | 3,170.47 | wall terms +0.23 ✓, **plus head-C kickers +0.098 and Retail Storage 126 studs +0.020 at the exact deck** = +0.348 | **−0.118** | **FAIL**: 6 kicker rows and the 73.98 LF retail studs still use deck 22.83 (stored misc_items) |
| 3-5/8" 362S125-30 | 259.56 | 259.50 | 18 pcs × (−0.00333) = −0.06 | 0 | OK |
| 3-5/8" 362S162-54 | 8,953.56 | 8,954.65 | +1.04 (pcs) + cripples at the 7'-2" heads | 0.05 | OK |
| Bracing C.R. | 6,301.09 | 6,301.09 | ROUNDUP(H × 12/48) unchanged for every wall | 0 | OK |
| **Hanger wire** | 2,497.64 | **2,497.64** | 192 hangers; drops at the exact deck: 56 × 10.8333 = 606.67 … Σ = **2,498.25** | **−0.61** | **FAIL**: height-dependent row did not change; `hanger_drop_ft` still 22.83-based |
| Board MR (09 29 00 2.3.E) | 5,483.88 | 5,702.30 | −0.016 (change 1) + 218.43 (change 2) | 0.01 | OK (arithmetic; see change 2 below) |
| Board Type X | 58,393.09 | 58,400.89 | walls +3.778 + existing EX-01…EX-20 +4.043 = +7.82 | 0.02 | OK |
| Board Type X W.R. | 1,493.04 | 1,493.20 | +0.165 | 0 | OK |
| Joint compound | 4,706.64 | 4,722.94 | 0.072 × (7.95 + 218.43) = +16.30 | 0 | OK |
| Joint tape | 24,186.90 | 24,270.66 | 0.37 × 226.38 = +83.76 | 0 | OK |
| Control joints | 363.93 | 363.93 | at the exact deck: +0.05 | 0.05 | below tolerance (misc_items 3–10 still 45.66 etc.) |
| Corner bead | 441.22 | same | trim 130/131 2 × 22.83 → +0.013 | 0.01 | below tolerance |
| Cement backer / mesh tape / gasket / tracks / grid / trim | — | unchanged | not height-dependent (tile cap below face height; ROUNDUP) | 0 | OK. Change 2 did not add cement board. |

## 4. Markups (FINAL6 PDF annotation /Depth vs Excel Height vs print), 16 walls
| Wall | /Depth | Excel H | Print | SF label = Excel |
|---|---|---|---|---|
| A-A421-6, A-A422-5, A-A426-6, A-A427-6 | 22.8333 | 22.833 | 22'-10" | yes |
| A-A421-15 | 14.4167 | 14.417 | 14'-5" (hidden text, see §2) | yes |
| A-A421-13 | 12.5833 | 12.583 | 12'-1" + 6" | yes |
| A-A421.A-1 / A-A422.A-1 / A-A423.A-1 | 10.8333 / 14.3333 / 11.3333 | same (3 dec) | deck − 12'-0" / 8'-6" / 11'-6" | yes |
| A-A424.A-1 / -2 / -3, A-A425.A-1 | 14.8333 / 14.8333 / 13.8333 / 14.8333 | same | deck − 8'-0" / 8'-0" / 9'-0" / 8'-0" | yes (23.92 = 5.22 × 4.5833) |
| A-A424-12, A-A424-6, A-A424-13 | 22.8333 / 9.5 / 12.5833 | same | — | 155.26 (2 faces), 96.70, 50.22 per segment; the Excel row sums to 211.88 / 96.70 / 64.24 |
In all 16 the Depth equals the Excel Height within 0.0003 ft (the Excel shows 3 decimals) and equals the exact printed or derived ft-in value. PASS.

## 5. Change 2: second MR face on 7 A424 walls
| Wall | Face B opens onto | Plan (A424, crops A424_*.png) | Buildable? | SF |
|---|---|---|---|---|
| A-A424-12 / -12r | chase between the ADA stall wall and the existing east wall (8'-9 1/2" bay) | open space several feet wide (A424_shower_12) | YES | 77.63 + 28.31 |
| A-A424-13 / -13r | cavity to the EXISTING west wall, dimension "9 1/2"" printed | closed cavity between the new niche side, its stub and the existing wall (A424_niche_dims) | **NO**: board cannot be hung or finished in a 9½" cavity against an existing wall | 25.11 + 7.01 |
| A-A424-14 / -14r | chase to the A3C urinal wall, "1'-0"" printed, vent pipe inside | closed 12" chase | only if hung before the adjacent wall is framed; this is not a finished face | 25.13 + 6.89 |
| A-A424-6 | gap to the X6D wall south (≈ 8–9" by vector), pipe inside | closed chase (A424_urinal_6) | same as -14 | 48.35 |
- A/A301 prints "…AT ALL "WET" ROOMS. - BOTH SIDES." (crop A301_typeA_both_sides.png). Confirmed.
- The quantity arithmetic is exact: +218.43 SF MR, compound +15.73, tape +80.82, and there is no other row effect.
- Data defect: `final6_canon.py` copies face A wholesale (`dict(a)`), so the chase faces of -6, -13, -13r, -14 and -14r carry `tile_backer` (5'-0" tile wainscot) inside a plumbing chase. This has no quantity effect today: the cement backer stays 1,209.77 because it comes from stored misc_items. It would add cement board to a chase if those were ever regenerated.

## Verdict of the first pass (superseded)
The first pass found 3 failures: (1) the deck-based items were not made exact (hanger wire −0.61, 3-5/8" per source −0.118); (2) the closed-cavity faces had no disclosure; (3) 14'-5" is not visible on the print. See the re-verification below.

## 6. Re-verification after REBUILT2 (canon_pre_FINAL6c → canon; Excel and markups 22:37)
| Item | Producer claim (delta.md) | FINAL6 Excel | Auditor | Δ | Comment |
|---|---|---|---|---|---|
| deck_height.value / 15 hanger_drop_ft | exact | 22.8333; 10.8333 … 14.8333 (105: 10.75) | = 22'-10" − printed ceiling height | 0 | OK. No rounded height-like float is left in the canon. |
| Hanger wire | +0.60 | 2,497.64 → 2,498.24 | Σ per ceiling at 2 dec: 0.19 + 0.04 + 0 + 0.02 + 0.03 + 0.03 + 0.03 + 0.04 + 0.03 + 0.02 + 0.07 + 0.03 + 0.04 + 0.03 + 0.02 = +0.60 | 0 | OK (was FAIL) |
| 3-5/8" stud per source | +0.35 | 3,170.24 → 3,170.59 | wall terms +0.23 + kickers (83.26 → 83.31, 139.5 → 139.51, 4 × +0.01) +0.10 + Retail Storage 73.98 → 74.00 +0.02 = +0.35 | 0 | OK (was FAIL) |
| 6" stud per source | +1.61 | 10,860.37 | previous +1.62, plus kicker A-A421-13 43.49 → 43.48 (−0.01) | 0 | OK |
| Control joints | +0.06 | 363.93 → 363.99 | misc 3–7 (+0.01 × 5 joints) + misc 10 (21.66 → 21.67) = +0.06 | 0 | OK |
| Corner bead (trim 130/131, 2 × 22.83) | — | 441.22 (unchanged) | +0.013 at the exact deck | 0.01 | below tolerance; not converted (cosmetic) |
| Other 9 changed rows (2-1/2", 6" 600S125-30, 362S125-30, 362S162-54, MR, X, WR, compound, tape) | +0.30 / +0.06 / −0.06 / +1.09 / +218.42 / +7.80 / +0.16 / +16.30 / +83.76 | same | same as §3 / §5 | 0 | OK. All 13 changed rows match delta.md. Unchanged rows (bracing, cement 1,209.77, mesh 447.61, tracks, grid, trim) are correctly unchanged. |
| Closed-cavity faces | kept as printed + Review Item 4/5 | Review Item 4 lists each face, its cavity, its SF, "buildable only if boarded before the adjacent wall is framed" and the alternative −112.49 SF MR (+ tape / compound) | 32.12 + 32.02 + 48.35 = 112.49 | 0 | DISCLOSED → accepted. Auditor note: -13 / -13r face the EXISTING wall, so in practice they are not buildable. The estimator should take the alternative for at least those 32.12 SF. |
| tile_backer on chase faces | removed | — | removed from -6, -12, -13r, -14, -14r chase faces; **still present on A-A424-13 face B** (9½" cavity) | no qty effect | data hygiene only (cement backer row comes from stored misc_items, 1,209.77 unchanged) |
| A-A421-15 14'-5" | height_source + Review Item 5/5 | Review Item 5: hidden text, not visibly printed; alternative 12'-7" (−1.83 ft on the zone) | matches the auditor crops h03/h10 | — | DISCLOSED → accepted |
| Markups (16 walls) | — | Depth = Excel = print | re-run, identical to §4 | 0 | OK |

## Verdict
VERDICT: PASS. All failures from the first pass are fixed or disclosed. The deck-based quantities now reconcile (hanger wire +0.60, 3-5/8" +0.35, control joints +0.06). The closed-cavity faces (−112.49 SF alternative) and the 14'-5" hidden-text height are disclosed as Review Items with their deltas. All 13 Material Summary deltas FINAL5 → FINAL6 match the auditor's recompute and delta.md.
Residual observations (no quantity impact or below tolerance): `tile_backer` is still on the A-A424-13 chase face B; corner bead trim 130/131 is still 2 × 22.83 (+0.013 LF); Excel wall-row heights display 3 decimals (22.833).


# Back-check round 2 (FINAL6 after producer rounds e-j, 2026-11-04)
Scope: final6e…final6j_canon.py, final6g/i_takeoff.py, final6_demo_extract.py, final6_demo_cruce.py, final6_evid_r2.py; `4_canon/demo_cruce.md` (the file is not in `work/` root). Excel and markups are dated 00:10 / 00:09. Clean set: `plano/bidset_SIN_MARKUPS.pdf`, read with python3 -I + pymupdf. Auditor scripts are in `scratch/AUD6b/` (dash.py, meas.py, ledger.py, legs.py, ms2.py, hs.py). Crops `r2_*.png` are in `img_final6/`. Every crop cited below was rendered and looked at.

## R2-1 Demolition (AD101)
**Scale check.** The AD101 title says 3/32" = 1'-0". Printed 109'-11 1/2" spans ticks 326.64 → 1068.96 = 742.32 pt, which is 6.751 pt/ft. Printed 10'-0 1/2" spans 1428.00 → 1495.92 = 67.92 pt, which is 6.764 pt/ft. Printed 9'-11 1/2" spans 1835.28 → 1902.48 = 67.20 pt, which is 6.749 pt/ft. 6.75 pt/ft is confirmed.
**Keynotes / legend (text layer + crop).** D0.35 "DEMOLISH EXISTING PARTITION. REPAIR SUBFLOOR & DECK ABOVE…"; D0.45 "…FROM 60\" A.F.F. TO DECK. RETAIN PARTIAL HEIGHT WALL."; D0.04 "DEMOLISH EXISTING PARTITION UP TO 10'-11\" AFF AND KEEP THE STRUCTURAL BULKHEAD."; legend "EXISTING TO BE REMOVED" = dashed. The plan area has 22 D0.35 tags, 1 D0.45 and 1 D0.04. Tags are not runs: several tags have two leaders, and some point at solid stubs.

### R2-1a Re-measure of every producer run (23 of 23; vector chain along both faces, cross-checked on crops)
| Run | producer LF | auditor LF | Δ | comment |
|---|---|---|---|---|
| DEMO-01 D0.35 | 6.58 | 6.58 | +0.0 | vector chain 1272.96-1317.36 = 6.58 ft; line ends = drawn ends |
| DEMO-02 D0.35 | 9.99 | 9.99 | +0.0 | vector chain 784.08-851.52 = 9.99 ft; = drawn |
| DEMO-03 D0.35 | 18.88 | 18.88 | +0.0 | vector chain 806.4-955.2 = 22.04 ft; auditor chain runs on into the restroom-box door jamb (806-828); producer stop at the door is correct |
| DEMO-04 D0.35 | 35.63 | 35.63 | +0.0 | vector chain 1286.64-1558.32 = 40.25 ft; auditor chain picks up AUD-A (1286-1318, separate wall, see below); producer value correct for its own run |
| DEMO-05 D0.35 | 30.33 | 30.33 | +0.0 | vector chain 1598.88-1803.6 = 30.33 ft; = drawn |
| DEMO-06 D0.35 | 19.73 | 19.73 | +0.0 | vector chain 851.52-984.72 = 19.73 ft; = drawn |
| DEMO-07 D0.35 | 10.74 | 10.74 | +0.0 | vector chain 1245.12-1317.6 = 10.74 ft; = drawn |
| DEMO-08 D0.35 | 10.24 | 10.24 | +0.0 | vector chain 1317.6-1386.72 = 10.24 ft; = drawn |
| DEMO-09 D0.35 | 11.8 | 11.8 | +0.0 | vector chain 856.8-941.76 = 12.59 ft; end at door frame (941.8 vs 936.5): +0.8 ft within the door jamb, accepted |
| DEMO-10 D0.35 | 4.02 | 4.02 | +0.0 | vector chain 1441.2-1487.04 = 6.79 ft; 1441-1460 is a glazed panel in the wall; producer excluded it here but kept the glazed panel inside DEMO-15 (inconsistent, small) |
| DEMO-11 D0.35 | 12.98 | 12.98 | +0.0 | vector chain 856.8-955.2 = 14.58 ft; end at door frame, accepted |
| DEMO-12 D0.35 | 11.34 | 11.34 | +0.0 | vector chain 1481.76-1558.32 = 11.34 ft; = drawn |
| DEMO-13 D0.35 | 19.63 | 19.63 | +0.0 | vector chain 851.04-983.52 = 19.63 ft; = drawn |
| DEMO-14 D0.35 | 12.73 | 12.73 | +0.0 | vector chain 851.04-936.96 = 12.73 ft; = drawn |
| DEMO-15 D0.35 | 23.04 | 23.04 | +0.0 | vector chain 1648.08-1803.6 = 23.04 ft; straight chord; the wall jogs twice by ~6.4 pt (~+1.9 ft), glazed panel 1768-1790 kept in the run |
| DEMO-16 D0.35 | 3.59 | 3.59 | +0.0 | vector chain 696.24-720.48 = 3.59 ft; = drawn (dashed stub) |
| DEMO-17 D0.35 | 73.03 | 63.36 | -9.67 | vector chain 696.24-1189.2 = 73.03 ft; **ends at 1123.92: 1123.92-1177.92 is the D0.56 storefront (glazing mullions) + 1177.9-1189.2 solid jamb -> -9.67 ft** |
| DEMO-18 D0.35 | 34.8 | 34.8 | +0.0 | vector chain 1206.0-1461.12 = 37.8 ft; top corner jog 1193.5-1206 included, accepted |
| DEMO-19 D0.45 | 10.0417 | 10.0417 | +0.0 | vector chain 1406.16-1496.16 = 13.33 ft; printed 10'-0 1/2" (1428.0-1495.92 = 67.92 pt) = producer |
| DEMO-20 D0.35 | 10.1 | 10.1 | +0.0 | vector chain 712.32-780.48 = 10.1 ft; = drawn |
| DEMO-21 D0.35 | 9.96 | 9.96 | +0.0 | vector chain 1103.76-1170.96 = 9.96 ft; = drawn |
| DEMO-22 D0.35 | 5.3 | 5.3 | +0.0 | vector chain 1280.88-1330.8 = 7.4 ft; = drawn (auditor chain continues into AUD-D corner) |
| DEMO-23 D0.35 | 18.56 | 18.56 | +0.0 | vector chain 1787.52-1909.2 = 18.03 ft; = drawn to 1909.2 (-0.53 ft); **same line as EX-17 (D0.07 remain + new board 2 faces), see finding R2-D3** |

All 23 runs are real dashed partitions with D0.35 (22) or D0.45 (1) per legend and leaders: each one was checked on the crops, and none of them is casework, a bench, a toilet partition or a pool line. 14 of them match the drawn line ends exactly. The only material difference is DEMO-17: the D0.56 storefront is not a gypsum partition (crop `r2_demo_grid4_storefront.png`, orange box).

### R2-1b Completeness: demolished gyp / metal partitions NOT loaded
| Item | producer | auditor | Δ LF | comment |
|---|---|---|---|---|
| AUD-A | 0 | 10.74 LF / 490.46 SF | +10.74 | restroom south / office north wall, dashed both faces (lines y 851.52 / 861.6); H 856.56 pt, 1245.12-1317.6 |
| AUD-B | 0 | 5.87 LF / 268.06 SF | +5.87 | partition at y 1186 right of rev-cloud 8, D0.35 leader tip at x 913 (EX-01 ends at 882); H 1186.2 pt, 882.0-921.6 |
| AUD-C | 0 | 11.88 LF / 542.52 SF | +11.88 | corridor east wall above EX-18, dashed (lines x 1316.64 / 1320), D0.35 leaders; V 1318.32 pt, 1710.72-1790.9 |
| AUD-D | 0 | 7.47 LF / 341.13 SF | +7.47 | corridor head wall with D0.32 column, dashed, D0.35 leader (1342,1683); H 1705.9 pt, 1280.4-1330.8 |
| AUD-E | 0 | 12.41 LF / 566.72 SF | +12.41 | locker-area south wall, dashed (lines y 1825.2 / 1828.8), D0.35 leader (1223,1797); H 1827.0 pt, 1200.72-1284.48 |
| AUD-F | 0 | 14.86 LF / 678.61 SF | +14.86 | spa room west wall, dashed (x 780.48 / 784.56), D0.35 leader (742,1561) 2nd arrow; V 782.52 pt, 1534.56-1634.88 |
| AUD-S1 | 0 | 2.99 LF / 136.54 SF | +2.99 | solid stub with a D0.35 leader: stub W of grid 4 (D0.35 leader 1104,1054) |
| AUD-S2 | 0 | 2.99 LF / 136.54 SF | +2.99 | solid stub with a D0.35 leader: stub W of grid 4 (same leader) |
| AUD-S3 | 0 | 2.95 LF / 134.72 SF | +2.95 | solid stub with a D0.35 leader: stub at grid 7 (D0.35 leader 1746,1049) |
| AUD-S4 | 0 | 1.74 LF / 79.46 SF | +1.74 | solid stub with a D0.35 leader: stub (D0.35 leader 505,1526) |
| AUD-S5 | 0 | 1.78 LF / 81.29 SF | +1.78 | solid stub with a D0.35 leader: stub at north wall (D0.35 leader 1414,721) |
| D0.04 (spa north, y≈1540, x 854.9-1029.8 ≈ 25.9 ft drawn dashed together with the D0.49 storefront line) | Review Item | not added | — | Disclosed, but the stated reason ("extent / height not dimensioned") is inaccurate. The 10'-11" is printed and the run is drawn. Its overlap with the storefront makes the extent ambiguous, so it is kept as a Review Item (observation). |
| Corridor east wall lower part x 1318, 1790.9-1902.5 | EX-18 (D0.07 remain, new board 2 faces) | conflict | — | It carries a D0.35 leader (1337,1845) **and** a D0.07 leader (1340,1860). The west twin is handled the opposite way, see R2-D3. |
| Locker-room east wall x≈1436 / spa east wall x≈853 (dashed, D0.07 leaders) | EX-12 / EX-15 / EX-19 | accepted | — | D0.07 "remove finish materials and substrate where required": existing wall to remain (observation). |
Crops: `r2_demo_NE_offices.png` (AUD-A), `r2_demo_corridor_lockers.png` (AUD-C/D/E, DEMO-23 vs EX-17), `r2_demo_spa_west.png` (AUD-F), `r2_demo_grid4_storefront.png` (AUD-B, S1/S2, DEMO-17 storefront).

### R2-1c Height, formula, totals
| Check | producer | auditor | Δ | comment |
|---|---|---|---|---|
| Height D0.35 | 22.8333 (B.O. deck 22'-10", 6/A429.B 'EL.+ 22' - 10"' + RFI-01), status DERIVED | same | 0 | D0.35 "REPAIR … DECK ABOVE" supports full height to deck. The deck source is the one already accepted in round 1. |
| Height D0.45 | 22.8333 − 5.0 = 17.8333 | 60" printed → 17.8333 | 0 | OK |
| SF formula | L × H × 2 faces × 1 layer | L × H × 2 | 0 | Both faces are counted once. Layers are not printed and that is disclosed. Cosmetic: the MS row header says "length x height x layers" and its N/SHEET cites D0.17, which is not loaded. |
| Producer arithmetic | Σ 23 = 403.04 LF / 18,305.14 SF | recomputed from demo_geom = markups (23 PolyLines on AD101, Depth = H, label = SF) = MS row | 0 | OK |
| **Total (auditor ledger)** | **403.04 LF / 18,305.14 SF** | **469.05 LF / 21,319.54 SF** (dashed only, without stubs: 456.6 LF / 20,750.99 SF) | **+66.01 LF / +3,014.4 SF (+16.5 %)** | −9.67 LF storefront; +63.23 LF of dashed partitions; +12.44 LF of tagged stubs. Not included: DEMO-15 jogs (~+1.9 ft), DEMO-23 end (−0.53 ft), D0.04, the EX-18 conflict. |
| Unloaded items disclosed | D0.32 ×10, D0.17 (AD102 7 + AD101 2), gen. note 5, D0.04 → Review Item 6/8 + ALC-X55; D0.33 ceilings EXCLUDED | present in the Excel Review Items and Scope Checklist | — | Disclosed. The reason is valid for D0.32 / D0.17 / note 5 (no extent or height). For D0.04 it is inaccurate (see above). The six AUD-A…F walls and the five stubs are **neither loaded nor disclosed**. |

**R2-D3 contradiction.** DEMO-23 (x 1282.4, 1787.5-1912.8, demolished) and EX-17 (x 1285.0, 1790.9-1902.5, "existing to remain", new board on 2 faces, 754.87 SF) are the same wall. The wall carries both a D0.35 leader (1250,1850) and a D0.07 leader (1246,1869). It cannot be both demolished and kept and re-boarded. The producer's `demo_cruce.md` says DEMO-23 has "new wall lines… existing to remain" 100 % and still loads it as demolition. This needs one decision (or an RFI) and a Review Item with the delta (−847.57 SF demo or −754.87 SF board), and the east twin EX-18 needs the same decision.

## R2-2 BE-03 board swaps
| Face | producer | auditor | Δ | comment |
|---|---|---|---|---|
| A-A425.A-1 face A | Type X → MR, 4.83 × 14.8333 = 71.64 SF | A425.A crop: the wall at x 1539 separates 135 WOMEN'S LOCKER ROOM (C-7 exposed, west) from the 8'-0" C-5 corridor soffit. Face A is in the locker room. A111 note 3 (p17) "LOCKER ROOMS, RESTROOMS, AND POOL AREAS TO BE MOISTURE RESISTANT GYP BOARD" → MR | 0 | OK |
| A-A424.A-1 face B | Type X → MR, 5.33 × 14.8333 = 79.06 SF | A424.A: 5'-4" soffit edge of 6/A502 "SOFFIT - SECTION @ LOCKER ROOMS ENTRY". Face B faces the men's locker entry corridor → note 3 → MR | 0 | OK |
| Net | MR +150.71 / X −150.71 | 71.64 + 79.06 = 150.70 | 0.01 | rounding |
| A-A424-7 face B | 2 × 5/8 Type X (X6D 1-HR, UL U465), not MR | A424 crop: X6D under the A3C urinal wall. Face B faces the existing south wall zone, not a room, so note 3 (room rule) does not apply. U465 needs Type X on both sides. | 0 | OK. Cosmetic: the face height_source text still says "deck 22'-10\" loaded [PENDING]". |

## R2-3 BE-06 headwall bottom (A-A422.A-1)
| Check | producer | auditor | Δ | comment |
|---|---|---|---|---|
| 15/A502 (p60) | bottom board 7.25" = 6" stud + 2 × 5/8" | printed: "6\" METAL STUD 20 GA FRAMING @ 24\" O.C.", "5/8\" GYP. BD." both sides and under the "MTL STUD BOX HEADER", 2 × "CORNER BEAD" | 0 | OK. The drawn width scales ≈ 4.9" at 1 1/2" = 1'-0", but the printed members govern. |
| SF | 0.6042 × 13.33 = 8.05 SF Type X | 8.054 | 0 | OK. Compound +0.58 / tape +2.98 follow from it. The 2 × 13.33 corner beads were already in trim_items (no double count). |

## R2-4 Height labels: CONFIRMED spot-check (montage `r2_confirmed_heights.png`, plus the A421.A C-5 crop)
| # | Value / face(s) | cited sheet | visibly printed? |
|---|---|---|---|
| 1 | 10'-0" (A-A421-1 A) | A421.A "10' - 0\" AFF C-5" | YES |
| 2 | 9'-0" (A-A421-13 A, -15 A) | A421.A "9' - 0\" AFF C-5" | YES |
| 3 | 12'-1" (A-A421-13 B) | A421.A "12' - 1\" AFF C-5" | YES |
| 4 | 8'-0" (A-A421-15 B, A-A422-2/-3) | A422.A 109 "8' - 0\" AFF C-5" | YES |
| 5 | 9'-6" (A-A422-4 B) | A422.A 112 "9' - 6\" AFF C-1" | YES |
| 6 | 14'-0" (A-A423-3 B) | A423.A 124 "14' - 0\" AFF C-12" | YES |
| 7 | 12'-1" (A-A424-1 A, -3 B) | A424.A 128 "12' - 1\" EXISTING C-3" | YES |
| 8 | 9'-0" (A-A424-5 B) | A424.A 130 "9' - 0\" EXISTING C-5 P-11" | YES |
| 9 | 10'-0" (A-A435-1/-2/-3) | A435 "EL.+ 10' - 0\" C-1" and A435.A elevations "EL.+ 10' - 0\"" | YES |
| 10 | 5'-0" (A-A421-3, A-A432-1) | A101 "T.O. WALL 60\" ABOVE FFE" | YES |
| 11 | 12'-0" (A-A429-6/-7) | A101 "T.O. WALL 144\" ABOVE FFE" (= 12'-0"); A429.A "EL.+ 12' - 0\"" | YES |
12 of 12 are printed and visible (none is hidden text). Observation: the canon has 65 CONFIRMED, 46 DERIVED and 1 PENDING (A-A421-15 14'-5"), plus 96 faces with **no `height_status` field**. Of those 96, 44 carry the text "[PENDING]" for the same deck 22'-10" that is labelled DERIVED on 46 other faces. The labels are inconsistent, with no quantity effect.

## R2-5 Split markups (U-120), legs vs Excel
| Wall | legs | Σ legs LF | Excel LF | leg Depth | Excel H | Δ |
|---|---|---|---|---|---|---|
| EX-03 | 2 | 26.67 | 26.67 | 22.8333 | 22.8333 | 0 |
| EX-15 | 3 | 38.98 | 38.98 | 22.8333 | 22.8333 | 0 |
| EX-19 | 2 | 27.60 | 27.60 | 22.8333 | 22.8333 | 0 |
| A-A421-1 | 3 | 4.77 | 4.77 | 10.5 | 10.5 | 0 |
| A-A426-2 | 3 | 4.67 | 4.67 | 22.8333 | 22.833 | 0.0003 (display) |
| (also A-A421-2, A-A423-9, A-A426-3) | 3 each | 4.77 / 2.34 / 4.67 | same | = | = | 0 |
PASS. The leg SF labels add up to the Excel Board SF.

## R2-6 Material Summary FINAL5 → FINAL6 (all 67 rows compared)
| Row | FINAL5 | FINAL6 | auditor explanation | Δ | comment |
|---|---|---|---|---|---|
| 2-1/2", 6" ×2, 3-5/8" ×3, hanger wire, X W.R., control joints | as round 1 | same as round 1 (+0.30 / +1.61 / +0.06 / +0.35 / −0.06 / +1.09 / +0.60 / +0.16 / +0.06) | exact heights (round 1) | 0 | OK |
| MR | 5,483.88 | 5,853.01 | +218.42 (both sides) + 150.71 (BE-03) = +369.13 | 0 | OK |
| Type X | 58,393.09 | 58,258.24 | +7.80 − 150.71 + 8.05 = −134.86 | 0.01 | OK |
| Joint compound | 4,706.64 | 4,723.52 | 16.30 + 0.072 × 8.05 = +16.88 | 0 | OK. MR↔X swaps do not change compound. |
| Joint tape | 24,186.90 | 24,273.65 | 83.76 + 0.37 × 8.05 = +86.74 | 0.01 | OK |
| Demolition (new row) | — | 18,305.14 SF | Σ DEMO-01…23 | 0 | Arithmetic OK. The quantity is short, see R2-1. |
| Text-only rows (tracks: BE-16 "METAL RUNNER CHANNEL" note; bracing; screws; blocking; head track) | | | final6e/i text edits | — | no numeric change |
Nothing else moved. Documentation gap: `CAMBIOS_FINAL6.md` still says "Rows changed: 13 of 67" and does not list the added Demolition row (66 → 67 rows), BE-03 or BE-06. The MR / X / compound / tape figures include them without saying so (observation).

## Round 2 verdict
Items 2, 3, 4, 5 and 6 pass. Item 1 (demolition) fails:
- F1: six dashed partitions on AD101 are not loaded and not disclosed (AUD-A…F: 63.23 LF / 2,887.50 SF). Four of them carry D0.35 leaders. Five D0.35-tagged solid stubs are also missing (12.44 LF / 568.55 SF). The Review Item says each run was "checked against its keynotes", which is not true for these.
- F2: DEMO-17 includes the D0.56 storefront and its jamb (−9.67 LF / −441.65 SF).
- F3: DEMO-23 is the same wall as EX-17 (D0.07 remain + new board on both faces). It is loaded as both demolition and new board, and it carries leaders for both keynotes. EX-18 (its twin) also has a D0.35 leader and is not demolished. There is no decision and no disclosure.
- Net demolition: producer 403.04 LF / 18,305.14 SF vs auditor 469.05 LF / 21,319.54 SF (+3,014.4 SF, +16.5 %).
Observations (no failure): the D0.04 reason is inaccurate; the height_status labels are inconsistent (96 faces unlabelled); CAMBIOS_FINAL6.md does not list the demolition row, BE-03 or BE-06; the MS demolition N/SHEET cites D0.17; DEMO-10 / DEMO-15 treat glazed panels inconsistently.

VERDICT: FAIL. F1: six AD101 dashed partitions (AUD-A to F, 63.23 LF / 2,887.50 SF) and five D0.35-tagged stubs (12.44 LF / 568.55 SF) are neither loaded nor disclosed. F2: DEMO-17 includes 9.67 LF of D0.56 storefront (−441.65 SF). F3: DEMO-23 is the same wall as EX-17, which is loaded as kept and re-boarded, and EX-18 has the same D0.35 / D0.07 conflict; the demolition total goes from 18,305.14 to 21,319.54 SF (+3,014.40 SF).

# Back-check round 3 (after final6k/l/m_canon.py, final6k_takeoff.py, docs_final6_post.py; Excel / markups 00:45)
| Item | producer | auditor | Δ | comment |
|---|---|---|---|---|
| F1 AUD-A…F | DEMO-24…29 loaded | coordinates = auditor ledger (856.56 / 1186.2 / 1318.32 / 1705.9 / 1827.0 / 782.52 pt); LF 10.74 / 5.87 / 7.47 / 12.41 / 14.86; DEMO-26 east wall now 1710.72 → 1891.2 = 26.74 | 0 | FIXED |
| F1 stubs | DEMO-30…34 loaded, 2.99 / 2.99 / 2.95 / 1.74 / 1.78 | = auditor | 0 | FIXED |
| F2 DEMO-17 | 696.24 → 1123.92 = 63.36 LF / 2,893.44 SF | stops at the first D0.56 mullion (1123.92) | 0 | FIXED |
| F3 east wall | DEMO-26 dashed to 1891.2; EX-18 1891.2-1902.5 = 1.67 LF kept | crop `r3_corridor_west_east_lower.png`: dashed double line to the solid end block 1891-1902.7. The D0.35 leader tip (1319, 1859) is on the dashed part. The D0.07 leader tip (1320, 1896) is on the solid block. | 0 | Reading CONFIRMED |
| F3 west wall | DEMO-23 1787.52 → 1861.9 = 11.02 LF; EX-17 1861.9-1902.5 = 6.01 LF kept | Dashed to 1861.92. A dark solid piece runs 1861.92-1878.48 and **the D0.35 leader (1250,1850) has its tip on it at y≈1866**. The D0.07 leader tip (≈1885) is on the light double line 1878.5-1902.5. A leader-based reading demolishes 2.45 LF more (+111.9 SF demolition / −111.9 SF Type X). | +2.45 LF | Observation, not a failure. The case is disclosed in Review Item 9/10 with the delta of each alternative (west wall all demolished: +344.33 SF demolition / −274.46 SF board), which brackets the auditor reading. Treatment is consistent with the stubs only if the solid piece is demolished; that is left to the estimator. |
| D0.04 | not loaded; Review Item 10/10 +565.92 SF (25.92 LF × 10'-11" × 2) | The leader tip (≈950, 1533) is on the top line of the spa-north element 854.9-1029.8. It is drawn with the storefront mullion symbol, on the same line D0.49 points to (crop d04 round 2). | 0 | Accepted as disclosed. The reason is now accurate (height printed, element drawn as glazing), and 25.92 × 10.9167 × 2 = 565.92 ✓ |
| Markups AD101 | 34 DEMO PolyLines; EX-17 6.01 / EX-18 1.67 | 34 DEMO annotations read; EX-17 (1861.9-1902.5) and EX-18 (1891.2-1902.5) = Excel | 0 | OK |
| Height labels | consistent | 208 faces carry `height_status`: 131 DERIVED, 74 CONFIRMED, 3 PENDING (A-A421-15 14'-5", A-A425-2 B, A-A422.A-1 A, all Review Items). No unlabelled face is left. | — | FIXED |
| Demolition total | 34 runs, 476.37 LF / 21,653.88 SF | auditor round-2 ledger 21,319.54 + DEMO-26 extension 1790.9 → 1891.2 (+14.86 LF, +678.61) − DEMO-23 shortened 18.56 → 11.02 (−7.54 LF, −344.33) = 476.37 LF / 21,653.82 SF | 0.06 | OK (rounding of the per-run SF) |

## Material Summary FINAL5 → FINAL6 (round 3)
| Row | FINAL5 | FINAL6 | auditor | Δ | comment |
|---|---|---|---|---|---|
| 2-1/2", 6" ×2, 3-5/8" ×3, hanger wire, MR, X W.R., control joints | — | unchanged since round 2 (+0.30 / +1.61 / +0.06 / +0.35 / −0.06 / +1.09 / +0.60 / +369.13 / +0.16 / +0.06) | as round 2 | 0 | OK |
| Type X | 58,393.09 | 57,099.22 (−1,293.87) | round 2 −134.86; EX-17 −10.52 × 22.8333 × 2 = −480.41; EX-18 −14.86 × 22.8333 × 2 = −678.61 → −1,293.88 | 0.01 | OK |
| Joint compound | 4,706.64 | 4,640.07 (−66.57) | +16.88 + 0.072 × (−1,159.02) = −66.57 | 0 | OK |
| Joint tape | 24,186.90 | 23,844.81 (−342.09) | +86.75 + 0.37 × (−1,159.02) = −342.09 | 0 | OK |
| Demolition (new) | — | 21,653.88 | as above | 0.06 | OK |
| Other rows | | text only (tracks, bracing, screws) | | 0 | nothing else moved |
CAMBIOS_FINAL6.md now lists the Demolition row ("14 of 67, 66 → 67 rows"). OK.

Round 3: F1, F2 and F3 are resolved, and F3 is disclosed with the delta of each alternative. D0.04 is disclosed with its delta. The Material Summary deltas reconcile. Residual observation: on the west corridor wall the D0.35 leader lands on the solid piece 1861.9-1878.5 (2.45 LF, ±111.9 SF). That falls within Review Item 9/10's disclosed alternative.

VERDICT: PASS

# Back-check round 4 (R-Z7 soffit-side resolution: final6q/r/s_canon.py, final6q_takeoff.py; Excel 02:46; baseline `scratch/E45/final6/FINAL6_backchecked.xlsx`)
Method: each band was overlaid on its RCP (pymupdf, clean set) and the drawn lines were read from the vectors. RCP scale is 18 pt/ft: A424.A 5'-4" ticks = 96.3 pt (18.05), and A421 14'-7 1/2" ticks y 1046.8 → 1309.6 = 262.8 pt (14.60 ft). The floor plans under each edge were checked as well. Crops are `r4_*.png` in `img_final6/`.

| R-Z7 | producer | auditor | Δ LF | comment |
|---|---|---|---|---|
| 01 A-A421.A-2 | 14.63 (printed 14'-7 1/2") | A421 prints 14'-7 1/2" along the overhead dashed headwall pair x 1522.8 / 1533.6 (`r4_A421_14-7.png`) | 0 | Printed dimension wins. OK. |
| 02 A-A421.A-1 arc | r 249.2 pt, 140.17° → 400.74°, 62.96 | The black polyline circle has mean r 249.04 pt and is drawn from 140.08° to 399.83° (gaps 253.2-255.8° and 359.9-2.8°) → 249.04 × 4.5335 rad / 18 = 62.72 | −0.24 | Observation (0.4 %): the producer runs 0.9° past the drawn line end. Review Item 3/11 still quotes the old 673.63 SF and r 13.83 ft (now 682.06 SF): stale text. |
| 03 A-A421.A-3 | 7.65 | lines x 1402.32 / 1403.28, 1711.92 → 1849.68 = 137.76 pt | 0 | OK |
| 04 A-A422.A-1 | 12.79 | lines y 1768.3-1775.5, 1560.48 (end of the west wall poche) → 1790.64 = 230.16 pt (`r4_A422A_headwall.png`) | 0 | OK. The END face and corner beads follow (12.79 × 0.6042 = 7.73 SF). |
| 05 A-A423.A-2 / new -3 | 9.39 + 2.64 | south edge 1694.88 → 1863.84 = 168.96 pt; west end 911.52 → 959.04 = 47.52 pt. A423 floor plan: the alcove's L wall has the VIP lounge (herringbone) on its west side, so the west end faces the VIP like the south edge does (`r4_A423A_box.png`). | 0 | OK. Same face treatment as the already-accepted -2. |
| 06 A-A424.A-1 + new -4/-5/-6 | headwall 4.75 between the corridor wall faces; box 5.33 + 2.0 + 2.0, face 1.98 ft | A424.A prints 5'-4" and 2'-0" for the box (`r4_A424A_6A502_box.png`). The headwall line y 943 runs 1323.36 → 1408.8 between the corridor wall faces. 6/A502 (1" = 1'-0", `r4_A502_detail6.png`) draws a headwall to structure plus a braced box with a front face and an open top. The box face is drawn ≈ 137-143 pt = 1.9-1.98 ft and is not dimensioned. | 0 | OK. The 1.98 ft is disclosed as Review Item 11/11 with its alternative (1'-6": −4.48 SF = 9.33 × 0.48 ✓). Type X on the gym side is correct (not a locker room). |
| 07 A-A424.A-2 kept at y 1177; B-A424.A-105 (y 1214) rejected | 5.22 | The 16/A502 bar sits at y ≈ 1181, next to the 1177 line. D0.43 is printed in the "8'-0\" EXISTING" corridor on A424.A (`r4_A424A_R-Z7-07.png`). Reader B itself marked the 1214 edge EXISTING and did not count it (B cites AD102 D0.47). | 0 | Rejection OK. Observation: the stipple runs on past 1177 to 1214. If the 1177-1214 strip is the existing D0.47 soffit B cites, the 1177 face could also be existing. That is the quantity accepted in rounds 1-3 (23.92 SF MR), unchanged here. |
| 08 A-A424.A-3 | 11.52 | gray pair y 1527.6 / 1532.16, 1737.84 (west wall face) → 1945.2 (end of the 9'-0" strip) (`r4_A424A_shower.png`) | 0 | OK |
| 09 A-A425.A-1 | 5.01 | x 1542.24 / 1543.2, 1096.56 → 1186.8 = 90.24 pt | 0 | OK |
| 10 A-A425.A-2 diagonal | 7.54 | black segments (2006.64, 953.28) → (2110.32, 865.68) = 135.73 pt | 0 | OK |
| **10 B-A425.A-102 east edge rejected** | "runs along the existing wall at grid E / 2.5, no exposed face" | **Not supported.** On A425.A the edge is the 1-pt line pair x 2106.0 / 2106.96 from y 868.56 to 953.28, drawn like every other soffit edge, not a wall poche. Grid 2.5 is at x ≈ 2059, 47 pt west of it. The 6/A502 marker bar is parallel to this edge, and east of it is unstippled open gym (`r4_A425A_triangle_wide.png`, `r4_A425A_triangle_east_edge.png`). The A425 floor plan, registered by the grid 2 / 2.5 / F bubbles (+352, +2 pt), shows **no wall** north of the corridor under this edge (`r4_A425_floor_at_east_edge.png`). | **+4.71** | **FAIL.** This is an exposed soffit side, and it is neither loaded nor disclosed in the Excel (no Review Item). Missing: 4.71 × 14.8333 = 69.86 SF Type X, about 59.33 LF of 6" stud (4 pcs × 14.83), 9.42 LF of track, about 14.13 LF of C.R. bracing, 4.71 LF of corner bead, plus tape / compound. |

## Material Summary FINAL6_backchecked → FINAL6 (all 67 rows; 2 text-only changes)
| Row | Δ producer | auditor recompute | Δ | comment |
|---|---|---|---|---|
| 6" stud per source | +56.30 | Stud pieces = ROUNDUP(L/2)+1 (+ L corners): A423.A-2 +13.83, A424.A-3 −27.67, A425.A-2 +14.84, A423.A-3 +41.50, A424.A-4/-5/-6 +11.88 +3.96 +3.96; box-header studs 2 × ΔL: −1.16 +5.08 −8.84 −1.08. A421.A-1/-2, A422.A-1, A424.A-1 and A425.A-1 keep their piece counts. Total +56.30 | 0 | OK |
| Ceiling / soffit track | +18.38 | 2 × ΔL per side = +21.38; header tracks −0.58 +2.54 −4.42 −0.54 | 0 | OK |
| C.R. bracing | +2.87 | runs × ΔL: +1.52 +0.72 −1.62 +1.17 −1.74 −13.26 +0.54 +7.62 +7.92 (the 1.98 ft box faces get no runs) | 0 | OK |
| MR | −21.78 | A424.A-1 −0.58 × 14.8333, A424.A-3 −4.42 × 3.5833, A425.A-1 +0.18 × 14.8333 = −21.77 | 0.01 | OK |
| Type X | +75.12 | A421.A-1 +8.23, -2 +6.16, -3 +0.30, A422.A-1 −0.54 × 6.1042 = −3.30, A423.A-2 +0.98, A423.A-3 +6.60, box 9.33 × 1.9792 = +18.47, A425.A-2 +2.54 × 14.8333 = +37.68 → +75.12 | 0 | OK |
| Corner bead / curved | +5.36 / +0.76 | Σ ΔL × qty of the soffit-bottom beads = 6.12, of which the 0.76 is the curved A421.A-1 bead | 0 | OK |
| Compound / tape | +3.84 / +19.73 | 0.072 / 0.37 × (75.12 − 21.78) = 3.84 / 19.74 | 0.01 | OK |
| Partition LF / soffit sides | 220.24 → 230.93 (15) | the 10 R-Z7 changes add up to +10.69 | 0 | OK. No other row moved. final6n/p changed text only. |

Round 4: R-Z7-01…09 and the diagonal of R-Z7-10 are confirmed against print and geometry. The 6/A502 box height is disclosed. The D0.43 rejection is consistent, and every Material Summary delta follows from the new lengths. One decision fails. Observations: the R-Z7-02 arc is +0.24 LF past the drawn end; Review Item 3/11 numbers are stale; the existing/new status of the R-Z7-07 strip is open.

VERDICT: FAIL. F4: R-Z7-10 rejects B-A425.A-102, the east edge of the 6/A502 women's entry triangle, x 2106 / y 868.6-953.3 on A425.A. The rejection cites an "existing wall at grid E / 2.5" that is not drawn on A425.A or on A425, and grid 2.5 is 47 pt away. The edge is an exposed soffit side, 4.71 LF / 69.86 SF of Type X with framing, and it is neither loaded nor disclosed as a Review Item.

# Back-check round 5 (targeted: final6t / u_canon.py; Excel 03:10; compared with the round-4 Material Summary)
| Item | producer | auditor | Δ | comment |
|---|---|---|---|---|
| (a) A-A425.A-3 length | 4.71 LF (x 2106.0 / 2106.96, y 868.56 → 953.28) | the round-4 vectors give the same line pair, 84.72 pt / 18 = 4.71 (`r4_A425A_triangle_east_edge.png`) | 0 | OK |
| (a) height | 14.8333, 1 × 5/8" Type X, faces the open gym | = A-A425.A-2: deck 22'-10" (RFI-01) − corridor C-5 8'-0" AFF printed on A425.A; gym side, so Type X (not a locker room) | 0 | OK. Partition Takeoff row 4.71 × 14.833 = 69.86 SF. |
| (b) 6" stud +92.06 | breakdown: A-A425.A-3 59.33 + A-A425.A-2 74.17 → 89.00 (apex L node) + header studs 9.42 + braces 8.48 | 6/A502: 6" 20 ga studs @ 24" o.c. from structure to the box header, MTL STUD BOX HEADER, DIAGONAL BRACING @ 48" o.c. Studs ROUNDUP(4.71/2)+1 = 4 × 14.8333 = 59.33. Apex L corner +1 × 14.8333 = 14.83 (same rule as the 6/A502 men's box corners and the A423.A box L). Header 2 × 4.71 = 9.42. Braces ROUNDUP(4.71/4)+1 = 3 × 2.828 = 8.48 (same formula as -2, length RFI-35). Arc trim: 33 pieces both before and after = 0. Total 92.06. | 0 | **Not inflated.** It is the same per-side framing as A-A425.A-2 / A-A424.A-1. About 64 % is the four full-height 14.83 ft headwall studs that 6/A502 draws to structure. The only debatable stud is the apex corner (14.83 LF), and the producer's L-node rule is applied the same way everywhere. |
| (c) arc trim | 62.96 → 62.72 (mean r 249.04 pt, 140.08° → 399.83°) | = auditor round-4 value 62.72 | 0 | OK. Board 62.72 × 10.8333 = 679.46. Curved bead −0.24. Control joint unchanged (2 joints). Track / bracing −0.48 each (2 runs). |
| (c) Review Item 3/11 + Scope Checklist RFI-S03 | 679.47 SF, r 13.84 ft; alternative +1,358.94 / −679.47 | 249.04 / 18 = 13.84; 62.72 × 10.8333 = 679.47; × 2 = 1,358.94 | 0 | OK. The canon ceiling texts still say "r = 249.0 pt / 18 = 13.83 ft" in the ceiling area / curved-molding ops; these are ceiling items and nothing in them moved (observation). |
| (d) Material Summary, round 4 → 5 | 6" +92.06; track +13.65; bracing +13.65; X +67.26; curved bead −0.24; bead +4.71; compound +4.84; tape +24.89 | track 3 × 4.71 − 0.48 = 13.65; bracing 3 runs × 4.71 − 0.48 = 13.65; X 69.87 − 0.24 × 10.8333 = 67.27; compound / tape 0.072 / 0.37 × 67.26 = 4.84 / 24.89 | ≤ 0.01 | OK. Against the round-1 baseline, only the same 9 rows differ, and each of them = round-4 Δ + round-5 Δ. MR 5,831.23 is unchanged. The two screw rows changed text only (EXCLUDED, value 0). Nothing else moved. |

Round 5: F4 is resolved, the stud quantity is justified by 6/A502 and consistent with the other soffit sides, the arc trim and RFI-S03 text agree, and no other row moved.

VERDICT: PASS

# Back-check round 6 (FINAL7: detail-callout dispositions only; final7a_canon.py, final7b_no_aplican.py)
Note: `callouts_no_aplican.json` holds **40** entries on 12 sheets, not 37 (A503.B 7, A505.A 9, A505.B 6, A503.C 4, A201 / A428.A / A437 3 each, the rest 1). The canon has 583 `callout_refs` on 135 distinct callouts.

## (a) Declared out of scope: 15 opened on the clean PDF (crops `r6_*.png`)
| Callout | detail as printed | in our scope beyond the take-off? |
|---|---|---|
| 9/A503.C CEILING MOUNTED TV | "G.C. TO PROVIDE ALL THREAD…", "G.C. TO PROVIDE UNISTRUT OR EQUAL", rod and bracket by vendor | No: all-thread / unistrut support, not stud, track or board |
| 4/A503.C DRY VANITY | countertop on the wall, silicone; no framing note | No |
| 5/A503.C WET VANITY | "WALL TYPE PER PLAN", mounting carrier / carrying plate per manufacturer (plumbing) | No |
| 6 and 8/A503.C | cubby / lower-cabinet elevations (millwork) | No (casework) |
| 1/A503.B GROUP X STORAGE CABINET | cabinet elevation and section, "SCHEDULED BASE" | No |
| 2/A503.A SHOE CUBBY | millwork | No |
| 9/A504 SAUNA HEATER 1 | Magma heater clearances, sensor | No (3/A504 steam-room soffit, the one that does print 6" stud, is not in the list) |
| 2/A505.A TILE TO WALL | "WALL AS SCHEDULED", Schluter, thin-set, moisture barrier | No (tile backer is already on the tile faces) |
| 17/A505.A PERCUSSION GUN 2 | product heights, references 5/A505.A | No. 5/A505.A, the one with blocking, is cited, and its blocking is A103 item 39 (wood, excluded) |
| 3/A505.B LIGHTING COVE | 12"×8" bracket @ 60" o.c. screwed to "SCHEDULED WALL ASSEMBLY" | No |
| 13/A424.C VANITY LIGHT HEIGHTS | mounting heights, mirrors, EL.+9'-0" | No |
| 1/A428 LIFT LAB PLAN | perimeter tagged EXISTING (14×). X3B / X1B / T1B are light-fixture tags on the RCP, not wall types | No new walls |
| 2/A428.A LIFT LAB SOUTH | finishes P-16 / WC-7 / A1.11 / A1.15 (open RFIs), EXISTING 16'-0" | No |
| 1/A437 WEIGHTS WEST | paint, mirrors A2.185, WP-21, B.O. DECK VARIOUS | No |
All 15 confirmed: none draws stud, track, board, backing, soffit or demolition in our scope that the take-off does not already carry. The backing details that are **not** in the list (2/A503.C, 5/A505.A, 10 and 12-13/A505.B) are carried in `blocking_pending_info` / A103 rows.

## (b) Cited callouts (8 checked)
| Callout | cited on | check | result |
|---|---|---|---|
| 9, 10, 11, 12/A423.B "SAUNA 2-" | A-A423-1 (IT/AV 132 north wall) and A-A423-2 (IT/AV south infill) | On A423 the 4-way mark A423.B 9-12 sits inside room tag "IT/AV 132" (`r6_A423_itav.png`). The four elevations draw roof ladder A2.163, rack A2.28 and room tag 132, with P-4 paint to "B.O. DECK VARIOUS" (`r6_A423B_9-12.png`). No sauna content is drawn. | Typo claim confirmed. The walls are right, and full height to deck = the loaded 22.8333. Nothing changes. |
| 1/A434.A INDOOR TURF EAST-1 | A-A421-3 (D3G low wall, 5'-0") | The A434 mark (arrow 1 east, `r6_A434_mark13.png`) faces the low wall between turf and the smoothie corridor. The elevation draws "EL.+ 5'-0"", SS-2 cap, WP-21, P-4 (`r6_A434A_1.png`). | Right wall. 5'-0" = loaded 5.0 ft (A101 "T.O. WALL 60\""). Cap and protection are finishes. Nothing changes. |
| 3/A434.A INDOOR TURF NORTH | A-A427-3 (Group X 119 / Recovery 113 south line) | Arrow 3 points north to the A6D / C3C line with the 119 / 113 storefronts. The elevation draws that wall to the truss with P-2 graphics, WD-3, A2.08 / A2.105 (`r6_A434A_3.png`). | Right wall. Full height = the loaded 22.8333. Nothing changes. |
| 2 and 4/A434.A | A-A434-1 | 4-way mark inside LIGHT WEIGHTS 149 | Right room. Finishes only. |

## (c) FINAL7 vs FINAL6 Excel
All 6 sheets were compared cell by cell (values): Inputs 64, Partition Takeoff 159, Material Summary 70, Pending 1, Review 13, Scope 86 rows. **0 differing rows.** The FINAL7 Material Summary equals FINAL6.

Round 6: the dispositions checked are correct, and the cited walls and the typo claim hold. FINAL7 = FINAL6 numerically and textually. Observation: the out-of-scope count is 40 entries, not 37.

VERDICT: PASS

# Back-check round 7 (FINAL8: text fixes; `Chuze_AustinBluffs_Takeoff_FINAL8.xlsx`)
FINAL7 → FINAL8 cell by cell: 0 numeric cells changed. 86 text cells changed (Partition Takeoff 72, Scope Checklist 11, Material Summary 3), which confirms the coordinator's count.

| Check | producer | auditor (scratch/AUD6b/r7.py) | Δ | comment |
|---|---|---|---|---|
| 1) Scope Checklist numbers (ALC-01/04/06/07/08/12/16/18/20/X55, RFI-05/-32): 36 values | as written | All 36 match: 6" studs 11,828.90 = Σ 3 rows; 3-5/8" 12,384.74 = Σ 3; bottom and top track 1,104.77 = Σ 7 / Σ 9 rows; metal trim 1,787.58 = Σ 4; blocking 253.31 = 247.31 + 6; EX- board 26,818.18 = Σ EX rows; Type X 57,241.60, MR 5,831.23, W.R. 1,493.20, bracing 6,317.61, soffit track 599.61, hanger 2,498.24, grid rows, CJ 363.99, cement 1,209.77, mesh 447.61, demolition 21,653.88 SF / 476.37 LF (Σ DEMO geometry) = their rows. ALC-01 "+910.70 LF" = Σ top slip-track rows (393.29 + 16.15 + 65.77 + 331.53 + 103.96), i.e. one C.R. row per slip-track LF. "±1,788.27" = the RFI-S01 alternative in the MS breakdown. | 0 | OK. Observation: ALC-01 says "sealer gasket under the 600T250-54 bottom track 22.41 LF", but the loaded gasket row is 353.94 (22.41 + 331.53 under the 16 upgraded 362T125-54 tracks). The 22.41 is option B's figure, so the note should cite 353.94. |
| 2) 9/A502 spacing | A-A421.A-3 at 16"; 15 other soffit sides at 24" | 9/A502 "CEILING DETAIL AND SOFFIT" prints "3 5/8\" x 20 GA METAL STUDS @ 16\" O.C." and "6\" x 20 GA METAL STUDS @ 16\" O.C." (`r7_A502_9.png`). 6/7/8/13/15/16 A502 print 6" 20 ga @ 24". Partition Takeoff O.C.: 15 × 24, 1 × 16 (A-A421.A-3 "3-5/8\" + 6\" 20 ga") | 0 | CONFIRMED |
| 3) Stud-column texts | — | 135 rows scanned. No stud cell says "not printed / not shown / assumed". Every RFI-cited cell (RFI-04, RFI-09) names the printed source and the closed decision. All 44 RFIs in the Scope Checklist are CLOSED. | 0 | OK |
| 4a) RFI-05 | decision: Type X everywhere + MR in the note-3 rooms; loaded 57,241.60 / 5,831.23 SF; alternatives (A) regular 5/8" where plans say GYP BD and (B) IBC Type X only on X6D: 0 SF each (price only) | values = MS; FINAL7 text was "applied in the quantities (0)" | 0 | OK. Decision, loaded value and the delta of each alternative are stated. |
| 4b) RFI-32 | decision: 2-1/2" on B2E; 2,009.34 LF stud, 103.96 + 103.96 LF track; alternatives (A) 1-5/8" = same LF (0), (B) SSMA 250 = as loaded (0); MR per the note-3 room list = 5,831.23 SF | stud and track values = MS, unchanged | 0 | **Incomplete.** The RFI-32 MR alternative ("MR only behind fixtures would move part of it to Type X") gives **no delta**. Every other alternative states one. |

VERDICT: FAIL. F5: the RFI-32 Scope Checklist row states its MR alternative ("MR only behind fixtures") without the SF delta, against the rule that each alternative carries its delta. No quantity is affected. Observation: the ALC-01 gasket figure (22.41 LF) should be the loaded 353.94 LF.

# Back-check round 8 (FINAL8: F5 fix + texts; checker U-037)
| Check | producer | auditor | Δ | comment |
|---|---|---|---|---|
| (a) RFI-32 MR alternative | −4,482.54 SF MR / +4,482.54 SF Type X = 57 MR faces 5,831.20 − 11 fixture faces 1,348.66 | Canon: 57 faces with board "5/8 MR", Σ L × H × layers = 5,831.20 (MS row 5,831.23, rounding). `wet_fixtures` has 13 fixtures on 11 walls. The MR face on the fixture's room side of each: A-A421-13 B 92.80, A-A421-15 B (109) 73.76, A-A424-2 A 231.26, A-A424-3 A 279.71, A-A423-6 A 117.13, A-A424-6 A 48.35, A-A424-11 A 77.63 + B 77.63, A-A424-12 A 77.63, A-A424-12r A 28.31, A-A424-9 B 244.45 = **1,348.66** (11 faces) → 5,831.20 − 1,348.66 = **4,482.54** | 0 | OK. Written in the RFI-32 Scope row and ALC-08. ALC-01 now reads "353.94 LF loaded … option B … 22.41 LF". |
| (b) 6/A429.B | "EL.+ 22' - 10\"" visibly printed | page 49, text at (675, 1620), inside 6 MASSAGE SOUTH (title x 576-741), rendered on a gray band at the deck line (`r8_A429B_EL22-10.png`) | — | CONFIRMED. All 24 canon `existing_walls[].height_source` cite it plus RFI-01. Observation: the Excel EX- rows' Source cell still says only "height = B.O. deck 22'-10\" (RFI-01 closed)". |
| (c) U-037 (v40 `chequeos_biblioteca.py`) | a tag is excused if its id is in some wall's `tag_ids` or in `tags_descartados` with a motive of ≥ 8 characters | Code read. Tested with a stub (`scratch/AUD6b/t_u037.py`): owned by a wall on another sheet → PASS; discarded with a motive → PASS; discarded with an empty motive → **FAIL**; **truly unowned A101 tag (no wall, no discard) → FAIL**; unowned tag without an id → FAIL | — | The change cannot hide a truly unowned tag. Observations: `tag_ids` ownership does not check that the claiming wall has the same type. The older per-(type, sheet) count rule still lets an unowned tag pass when another wall of its type exists on that sheet; this predates the change. |
| (d) new texts | R-ALC-09 owner [PENDING] (Inputs C36); U-116 on ALC-X48; RFI-32 / ALC-08 delta; ALC-01 gasket | C36: tenant from G001, owner not printed → [PENDING]. ALC-X48: Level 1 not loaded because the extent is not printed (conservative). Deltas are recomputed above. No decision is invented. | — | OK. Observation: the canon `rfis` RFI-32 option A "texto" still says "MR loaded on the 13 fixture faces only; the other 36 wet-room faces (~3,990 SF) loaded 5/8\" type X". That contradicts the loaded state (MR on all 57 note-3 faces) and the new delta in the same object. It is not in the FINAL8 Excel, but an RFI log regenerated from the canon would print it, so it should be corrected. |

VERDICT: PASS
