# BACK-CHECK REPORT: Metal Framing & Drywall Take-off
**Project:** O'Reilly Auto Parts, 23rd Ave., Evans, CO #1
**Bid set:** EV1 Current Conformed Set 11-20-2025 (`bidset.pdf`, 68 pages, raster sheets; trade sheets per `SHEET_MAP.md`)
**Take-off checked:** `OReilly_Evans_CO1_Takeoff_pasada2_FINAL.xlsx` (Claude take-off, pass 2, dated 2026-10-31). The Excel was **not modified**.
**Back-check date:** 2026-11-02
**Global verdict:** **FAIL**. 33 of 34 rows are OK (|Δ| ≤ 2 %). 1 row differs by more than 2 %: **Z-furring 1-1/2" LF, +13.4 %**.

---

## 1. Header: sources, revision, quarantine

| Item | Status |
|---|---|
| Sources available | #2 Claude take-off (the Excel) and #3 this back-check. **No #1 estimator / Bluebeam source was supplied.** Because the only other reader is the same model, independence here comes from **method** (dimensional closure, cross-sheet check, magnitude check), not from a second reader. |
| Set revision | Both sources use the same set. The Excel header says "EV1 Current Conformed Set 11-20-2025", the same set as `bidset.pdf`. Revision dates: A1.1 4-18-25, A1.2 9-9-25, S4.1 3-20-25. No source used a different revision. |
| Quarantine | **Partial.** The check ran inside a subagent, not in a separate chat. The partition LF was re-quantified blind from the printed dimensions and written to `work/blind_LF_before_excel.txt` **before** the Excel was opened. Heights, board SF, studs, track and Z-furring were derived after the Excel's Partition Takeoff sheet was open. Those figures were rebuilt from printed elevations with code (`work/backcheck_calc.py`), but they count as a method and arithmetic audit, not as a blind count. |
| Adjustments made after opening the Excel (declared) | (a) **S41 box-outs.** The blind gross LF was 7.17 LF, adding the printed legs without netting the corners. The net-leg convention gives 6.458 LF, so the net-leg figure was adopted. (b) **South storefront 6'-0" piers.** The blind pass assumed these were CMU and gave S21 a range of 251 to 263 LF. The Excel carries them as EXT-MS 8"/6" CFMF walls (3/S5.3, S4.1). The printed 6'-0" segments on A1.1 confirm the lengths, so they were removed from S21. |
| Memory leakage | No persisted quantities for this project were found or used. |
| Standing orders applied | Screws and anchors excluded. MEP, electrical, civil, cabinets, ACT, insulation, stucco and wood trim excluded. Board not deducted at openings. RFIs closed by the estimator (Scope Checklist) applied as given, including RFI-01 (8" purlin assumed) and RFI-29 (S42-02 extension of 7.2 ft). |
| Skill steps not run | The pause for user confirmation at the end of STEP 2 was not possible because a subagent cannot pause. The tools and Drive steps (STEP 0-B and 6-C) were skipped because the brief limits work to this folder. The corrected Excel (deliverable B) was **not** produced because the brief says not to change the Excel. |

## 2. Scope and method

**Scope checked:** the A1.1 Interior Wall Types S21, S24, S41, S42, S43 and S61, plus the LF of the EXT-8CFMF and EXT-6CFMF rows. For each type the check covers LF, heights, board SF by face, studs by size and O.C., standard top track vs deep-leg track, and Z-furring with its runners.

**Not re-quantified (limitation):** the S5.1 structural extras (S42 header kickers, lateral and angle struts, clip angles), FRT blocking, trims, control joints, GWB ceilings (hard lid 7/A4.2, vestibule), the head and cornice framing (HEAD-A, CORN-S height, VH-*), glass-mat sheathing, 1/4" gypsum board, RC channel and W-4 panels. These were accepted as cited and not verified. Spot check: the office and R.R. GWB ceiling areas equal the printed room dimensions net of 5/8" board on both sides. For example, (11'-0" − 1¼") × (8'-0" − 1¼") = 86.03 SF, which matches the Excel.

**Method**
1. **Blind sweep of A1.1 at 130 to 250 dpi.** Every tag was located (S21, S24, S41, S42, S43, S61) and every dimension string was read. Feet and inches were rebuilt separately in code. The sheet was **never scaled**.
2. **Heights from printed elevations:**
   - T.O. LOW EAVE EL. 114'-7 ½" (2/A3.2, grid A side)
   - T.O. HIGH EAVE EL. 116'-4 ¾" (1/A3.2, grid C side)
   - FINISH CEILING EL. 111'-6" + 6" (5/A4.2)
   - B.O. FRAMING EL. 106'-10", with 4'-8" + 6" (6/A4.2)
   - 8'-6" (7/A4.2, A1.1 S24/S43/S61, A1.2 C-3)
   - 12'-0" A.F.F. (A1.1 S41/S42)
   - RFI-01: an 8" purlin is assumed. The purlin depth is not printed.
3. **Dimensional closure** of every A1.1 chain against 86'-4" and against the interior clear span (section 4).
4. **Cross-sheet check:** A1.1 against S4.1 (framing key plan), A4.2 (5/6/7), A1.2 (ceiling schedule), A3.2 (wall sections) and A5.1/A5.2 (jamb details).
5. **Three-way comparison.** Back-check vs Excel, each tied to a printed N/SHEET dimension. The tolerance is |Δ| ≤ 2 %, with Δ % = (Excel − back-check) / back-check.

**Derived base dimension:** interior clear span = 86'-4" − 2 × (7⅝" CMU + 1½" furring) = **84'-9 ¾"** = 84.8125 ft. [DERIVED: the 7⅝" and 1½" values are printed at every corner of A1.1.]

**Wall numbering:** the back-check uses grid lines. The Excel names facades by true north. The equivalence is:

| Back-check (grid) | Excel |
|---|---|
| grid A | S21-E (East) |
| grid 1 | S21-N (North) |
| grid 4 | S21-S (South) |
| grid C | S21-W1 / S21-W2 (West) |

All other wall IDs are the same as the Excel's (S24-OF, S42-01…04, and so on).

## 3. Comparison tables

### 3a. LF by partition type

| Type | Back-check LF | Excel LF | Δ % | Printed basis N/SHEET | Tag | Verdict |
|---|---:|---:|---:|---|---|---|
| S21 | 288.58 | 288.625 | +0.01 | 86'-4"/A1.1; 7⅝" + 1½"/A1.1; grid C: 4'-0" + 6'-8" and 22'-4" + 4'-0" less the 8" pilaster and 9⅛"/A1.1 | [DERIVED] | PASS |
| S24 | 37.29 | 37.385 | +0.25 | 11'-0", 7'-10" + 6" + 7'-10", 8'-6"/A1.1 + wall 3⅝" + 2 × ⅝"/A1.1 types | [DERIVED] | PASS |
| S41 | 6.458 | 6.46 | +0.03 | 2'-2", 1'-8" (×3)/A1.1, net of 4¼" at the corners | [DERIVED] | PASS |
| S42 | 123.106 | 123.106 | 0.00 | 1'-8" + 37'-0" + 18'-4" = 57'-0"/A1.1 (+4⅞"); 50'-4" + 8'-2"/A1.1; +7.2 ft RFI-29 (closed) | [CONFIRMED] by closure; RFI-29 [PENDING-closed] | PASS |
| S43 | 52.885 | 52.729 | −0.30 | 8'-0", 11'-0", 8'-6", 7'-10" + 6" + 7'-10"/A1.1 | [DERIVED] | PASS |
| S61 | 8.50 | 8.50 | 0.00 | 8'-6"/A1.1 (R.R. depth) | [CONFIRMED] | PASS |
| EXT-8CFMF | 12.00 | 12.00 | 0.00 | 6'-0" + 6'-0"/A1.1 grid C chain | [CONFIRMED] | PASS |
| EXT-6CFMF | 48.00 | 48.00 | 0.00 | 36'-0"/A1.1 grid 4 chain + 2 × 6'-0"/A1.1 | [CONFIRMED] | PASS |

### 3b. Heights (cross-sheet)

| Item | Back-check (ft) | Excel (ft) | Δ % | N/SHEET (two sheets or more) | Verdict |
|---|---:|---:|---:|---|---|
| S21 grid A, to the underside of the purlin | 13.958 | 13.958 | 0.00 | 114'-7 ½"/2-A3.2 − 8" RFI-01 | PASS |
| S21 grid 1 and 4, average of the rake | 14.844 | 14.844 | 0.00 | 114'-7 ½"/2-A3.2 and 116'-4 ¾"/1-A3.2 | PASS |
| S21 grid C | 15.729 | 15.729 | 0.00 | 116'-4 ¾"/1-A3.2 − 8"; board above the ACT confirmed on 3/A3.2 | PASS |
| S42, Parts A face | 12.00 | 12.00 | 0.00 | 111'-6" + 6"/5-A4.2; "12'-0" A.F.F."/A1.1 S42 | PASS |
| S42 header, Parts A face (B.O. 6'-10") | 5.167 | 5.17 | +0.06 | 4'-8" + 6"/6-A4.2; header wall keynote 4/S4.1 | PASS |
| S42-01, Parts C face at grid B | 14.502 | 14.51 | +0.06 | interpolated from the two eaves (no grid-B elevation printed) | PASS |
| S42-03, Parts B face (header to roof) | 8.198 | 8.20 | +0.02 | same interpolation − 6'-10"/6-A4.2 | PASS |
| S42-04, Parts B face | 15.644 | 15.64 | −0.03 | same interpolation | PASS |
| S24 / S43 / S61 room side | 8.50 | 8.50 | 0.00 | 8'-6"/A1.1 types; 7/A4.2; C-3 8'-6"/A1.2 | PASS |
| S43, exposed (Parts C) face | 9.00 | 9.00 | 0.00 | 8'-6" + 6" joist/7-A4.2 | PASS |
| S41 | 12.00 | 12.00 | 0.00 | "studs and board to 12'-0" A.F.F."/A1.1 S41 | PASS |

### 3c. Board (5/8" Type X and X W.R.) by type, by face

| Type | Back-check SF | Excel SF | Δ % | Faces | Verdict |
|---|---:|---:|---:|---|---|
| S21 | 3,903.2 | 3,891.05 | −0.31 | 1 face, plus the plenum strip above the hard lid behind S24 (RFI-02 closed) | PASS |
| S24 | 317.0 | 317.77 | +0.25 | 1 face (interior) to 8'-6" | PASS |
| S41 | 77.5 | 77.52 | +0.03 | 1 face to 12'-0" | PASS |
| S42 | 2,274.1 | 2,274.59 | +0.02 | 2 faces, asymmetric (A: 12'-0"; B/C: to the roof framing) | PASS |
| S43 | 925.5 | 922.76 * | −0.30 | 2 faces (8'-6" room / 9'-0" exposed) | PASS |
| S61 | 144.5 | 144.5 | 0.00 | 2 faces, X W.R., 8'-6" | PASS |

\* 902.76 (Partition Takeoff H33) + 20.0 SF "GWB-S43-RR-W-ABOVE-WR", which the Material Summary lists on its own line. Added so both sides compare the same thing.

### 3d. Main materials (net, before waste)

| Material | Back-check | Excel | Δ % | N/SHEET | Verdict |
|---|---:|---:|---:|---|---|
| **1-1/2" Z-furring 150ZF125-18 @ 24" (LF)** | **2,220.6** | **2,517.5** | **+13.37** | S21/A1.1; **2/A5.1; 12/A5.2** | **FAIL** |
| Z-furring runner, top and bottom (LF) | 577.17 | 577.25 | +0.01 | S21/A1.1 (estimator answer 16) | PASS |
| Bottom track 3-5/8" (LF) | 219.74 | 219.68 | −0.03 | A1.1 types | PASS |
| Top track 3-5/8", standard (S24 / S43 / S41) (LF) | 96.64 | 96.57 | −0.07 | A1.1 types | PASS |
| Deep-leg slotted deflection track 3-5/8", S42 (LF) | 123.11 | 123.11 | 0.00 | A1.1 note 2.C; S5.1 | PASS |
| Track 6", S61 (LF each, top and bottom) | 8.50 | 8.50 | 0.00 | S61/A1.1 | PASS |
| 362S162-33 @ 24" O.C., partition studs only (LF) | 1,560.4 | 1,570.19 ** | +0.63 | A1.1 types; double studs at the jambs per 7/A5.1 | PASS |
| 600S162-33 @ 24" O.C., S61 (LF) | 68.0 | 68.0 | 0.00 | S61/A1.1 | PASS |
| Board on partition faces, total X + X W.R. (SF) | 7,641.8 | 7,628.2 | −0.18 | as in 3c | PASS |

\** These are the Excel's partition stud components only. Its full 362S162-33 row (1,912.02 LF) also includes 341.83 LF of S5.1 kickers, struts and doubled control-joint studs, which were not re-quantified (see the limitation in section 2).

**Row count:** 8 (3a) + 11 (3b) + 6 (3c) + 9 (3d) = **34 rows. 33 PASS, 1 FAIL.**

## 4. Dimensional closure (A1.1), residuals computed in code

| Chain | Sum | Target | Residual | Result |
|---|---|---|---:|---|
| Grids along A: 8" + 30'-0" + 30'-0" + 25'-0" + 8" | 86'-4" | 86'-4" | 0" | Closes |
| Grids along 1: 8" + 25'-0" + 60'-0" + 8" | 86'-4" | 86'-4" | 0" | Closes |
| Grid 1 openings: 4'-0" + 3'-0" + 6'-0" + 3'-4" + 22'-0" + 3'-4" + 8" + 4'-0" + 36'-0" + 4'-0" | 86'-4" | 86'-4" | 0" | Closes |
| Grid A pilasters: 4'-0" + 37'-8" + 4'-0" + 38'-0" + 4'-0" | 87'-8" | 86'-4" | +16" | Closes only if read pilaster face to pilaster face (+2 × printed 8"); see I2 |
| Grid C: 4'-0" + 6'-8" + 6'-0" + 18'-8" + 8'-0" + 12'-0" + 6'-0" + 22'-4" + 4'-0" | 87'-8" | 86'-4" | +16" | Same as above |
| Grid 4: 4'-0" + 39'-8" + 4'-0" + 36'-0" + 4'-0" | 87'-8" | 86'-4" | +16" | Same as above |
| Interior row: 45'-5 ¼" + 11'-0" + 11'-0" + 7'-10" + 6" + 7'-10" + 3 walls of 4⅞" | 84'-9 ⅞" | 84'-9 ¾" | +⅛" | Closes (≤ ⅛"). S43, S24 and S61 LF are [CONFIRMED] |
| S42 at grid B: 1'-8" + 37'-0" + 18'-4" | 57'-0" | 57'-0" (printed) | 0" | Closes. S42-01 / S42-02 are [CONFIRMED] |
| E-W at grid B: 57'-0" + 4⅞" + 27'-6 ⅛"± | 84'-11" | 84'-9 ¾" | +1 ¼" | ± field dimension; acceptable |
| N-S, office column: 8'-0" + 4⅞" + 17'-4 ⅞"± + 4⅞" + 50'-4" + 8'-2" | 84'-8 ⅝" | 84'-9 ¾" | −1 ⅛" | ± field dimension; acceptable |

**Magnitude check:** footprint 86'-4" × 86'-4" = 7,453 SF gross. Partition board is 7,642 SF, about 1.0 × the footprint. That is consistent with a fully furred perimeter of 339 LF at about 14.6 ft (about 4.95k SF) plus S42 (2.27k SF). No order-of-magnitude problem.

## 5. Differences (> 2 %)

### F1 — Z-furring jambs not printed: double count with the FRT jamb blocking. Severity MAJOR. Class: SPECIFICATION / METHOD. Against: Excel (#2).

- **Excel** (Material Summary row 19): 2,517.5 LF. Per its own breakdown, this includes "+12 jambs" on S21-N (doors 2, 3 and 7; 4 Z pieces per opening) and "+8 jambs" on S21-S (windows D1 and D2), framing the Z-furring jambs like stud walls. The extra is 20 pieces × 14.844 ft = **296.9 LF**.
- **Printed:**
  - **2/A5.1 JAMB DETAIL** (exterior HM doors in CMU) shows "FIRE TREATED 2X4 WOOD BLOCKING ANCHORED TO MASONRY" at the jamb and "150ZF125-18 … Z-FURRING FRAMING AT 24" O.C.". No doubled or extra Z member is drawn at the jamb.
  - **12/A5.2 JAMB DETAIL** (windows D1/D2) shows the same: "FIRE TREATED WOOD BLOCKING" plus Z-furring "AT 24" O.C.".
  - The Excel already carries this jamb blocking (row 31: BLK-EXT-DOORS 57.33 LF, BLK-WIN-D 58.92 LF), so the Z jambs are a second member at the same location.
- **Back-check:** 2,220.6 LF. This is field pieces at 24" + 1 less the pieces inside the rough openings + the Excel's corner nodes + the Excel's cripples, with no extra jamb pieces:

  | Wall | Calculation | LF |
  |---|---|---:|
  | Grid 1 | 40 × 14.844 + 35.89 | 629.64 |
  | Grid A | 46 × 13.958 | 642.08 |
  | Grid 4 | 35 × 14.844 + 114.79 | 634.32 |
  | Grid C (W1) | 6 × 15.729 | 94.37 |
  | Grid C (W2) | 14 × 15.729 | 220.21 |

- **Δ:** +296.9 LF net (+13.4 %), or +341.4 LF with 15 % waste, about 18 pieces of 20 ft. The quantity is not critical to the bid total, but it is a real method error.
- **Evidence (re-opened and checked):** `img/F1a_Zfurring_jamb_2-A5.1.png` and `img/F1b_Zfurring_jamb_12-A5.2.png`. The circles mark the FRT blocking at the jamb and its callout, and the Z-furring "@ 24" O.C." callout.
- **Recommendation:** either remove the 20 Z jamb pieces, or have the estimator confirm explicitly that a doubled Z jamb is wanted in addition to the printed FRT blocking.

## 6. Informational items (within tolerance or already decided; not counted as FAIL)

- **I1 — S42-02 extension east of the S42-03 corner (RFI-29, closed at 7.2 ft).** A1.1 draws the grid-B wall continuing past the corner with no dimension (`img/I1_S42_ext_A1.1.png`). The **S4.1 framing key plan** shows the dashed header turning at the corner with **no extension** (`img/I1_S42_noext_S4.1.png`). This conflict between sheets belongs in the RFI. The 7.2 ft affects S42 LF, the deep-leg track and about 110 SF of board. It is applied here per the standing order.
- **I2 — Pilaster chains.** The chains on grid A, grid C and grid 4 sum to 87'-8", while the grid-1 chain and the overall dimension are 86'-4". The +1'-4" equals the two printed 8" offsets, so the chains run from pilaster face to pilaster face. S21-W1 and S21-W2 depend on that reading: back-check 9.24 / 24.91 vs Excel 9.156 / 24.823, Δ ≤ 0.9 %. This should be confirmed in the RFI log.
- **I3 — S21 on grids 1 and 4.** The Excel uses 85.0 ft (grid to grid). The furring line is 84'-9 ¾" (CMU + furring at both ends). Δ is 0.22 % per wall, so this is MINOR.
- **I4 — S5.1 structural extras and the RFI-01 purlin depth.** All heights to the roof framing use the assumed 8" purlin (RFI-01, not printed). Every S21 and S42 height above is [DERIVED] from the printed eaves, the RFI-01 assumption and a linear rake interpolation. No grid-B or grid-3 roof elevation is printed.

## 7. Classification

- **VERIFIED** (passes dimensional closure or matches a printed dimension, by a method independent of reading): S42 LF (57'-0" chain plus 50'-4" + 8'-2"), S43, S24 and S61 LF (interior row closes within ⅛"), EXT-8CFMF and EXT-6CFMF LF, and the S24/S43/S61/S41/S42 heights confirmed on two sheets or more.
- **NON-INDEPENDENT AGREEMENT** (same model; DERIVED values that nobody proved from a printed dimension): S21 heights and the S42 to-roof heights (RFI-01 purlin depth plus interpolation), S21-W1 and S21-W2 (pilaster reading), and S41 (net-leg convention adopted after seeing the Excel).
- **OPEN DISCREPANCY:** none between the sources. The cross-sheet conflict I1 belongs in the RFI.
- **FINDING AGAINST THE EXCEL:** F1 (Z-furring jambs).

## 8. Verdict

| Block | Rows | PASS | FAIL |
|---|---:|---:|---:|
| LF by type | 8 | 8 | 0 |
| Heights | 11 | 11 | 0 |
| Board by type | 6 | 6 | 0 |
| Main materials | 9 | 8 | 1 (Z-furring +13.4 %) |
| **Total** | **34** | **33** | **1** |

**GLOBAL: FAIL**, because one row exceeds the 2 % tolerance (F1, Z-furring). Every partition LF, height and board quantity is within ±0.4 %. As section 2 states, the S5.1 structural extras, blocking, trims, control joints and ceilings were not re-quantified.

Files:
- Calculation script: `work/backcheck_calc.py`
- Results: `work/backcheck_results.json`
- Blind LF recorded before opening the Excel: `work/blind_LF_before_excel.txt`
- Crops: `img/`

## Resolution (applied, run15)
The only FAIL (1-1/2" Z-furring +13.4 %) was confirmed on 2/A5.1 and 12/A5.2: the furring jamb is FRT wood blocking (already in the blocking row), not king + jack studs. The stud tool no longer adds jamb studs on Z-furring / hat-channel walls. Re-run: Z-furring 2,220.63 LF vs back-check 2,220.6 LF (0.0 %). All 34 rows now within ±2 %. Global verdict after resolution: PASS.

## Addendum rev5 (03-nov-2026, skill v81cf25) — the only quantity that changed vs run15
- **Additional head track at openings over 4'-0" wide: 32.73 LF -> 0 LF.** Independent reading (sub-agent that did not see
  the Excel, `../../lect_datos/head_track.json`, 11 candidates, circled crops in `img_rev5/HT_*.png`): no sheet prints a
  head track at door / window heads in stud walls, nor a 4'-0" rule. 7/A5.1 prints only the 600S162-33 cold form metal box
  header; the three openings that carried the 32.73 LF (Door 3 6'-0" in S21-N, Windows D1 / D2 11'-4 3/8" in S21-S) are in
  S21 = 150ZF125-18 Z-furring on CMU (no studs, masonry lintels per S4.1). Tool fix R80e.144 (accesorios.py: furring walls
  have no stud head) + test `tools/test_head_track_furring.py`.
- Every other Material Summary row = run15 (checked row by row by program: 67 rows, 0 other differences; one row only
  renamed: ceiling perimeter track 72 LF).
- Result of this addendum: **PASS** (the run15 back-check FAIL F1 was resolved in run15; no new difference).

## Addendum rev6 (03-nov-2026, skill v81cf26) — no quantity change vs rev5
- Material Summary: 67 rows, identical to rev5 (checked by program).
- Added per the day-1 rules (gate v81cf26): face height status [CONFIRMED] / [DERIVED] with its operation (U-114; S43 / S61
  faces carried as [DERIVED] = studs to 8'-6" A.F.F., board height not printed); tag sweep of A1.1 (29 tags, raster sheet,
  visual sweep with circled crops reopened, assigned to their walls: U-117); circled height evidence for every wall (U-118);
  deliverable text in English (U-119); project data not printed cites R-ALC-09 (U-116).
- Result of this addendum: **PASS**.
