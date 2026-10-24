# BACKCHECK rev1 - Barnes & Noble Colorado Springs take-off

Date: 2026-10-24. Inputs were not modified; nothing committed.

## Method
Loaded rev1 and rev0 with openpyxl (values and formulas), diffed Partition Takeoff row by row, recomputed W.R. SF from `board_out.json` faces (wall x room x SF), recomputed FRT/plywood sums, tested net x waste = waste and net + waste = purchase on every Material Summary row, and scanned all sheets for Spanish words/accents and the word PENDING. Compared against DECISIONES_ESTIMADOR.md.

## 1. Perimeter removal - PASS
- Removed from Partition Takeoff: 17 walls (1A: EXT-01, 03; 1: EXT-02, 07; 1B: 9 walls; 1C: 4 walls) plus 4 type headers and 4 subtotals = 26 rows. No other row differs between rev0 and rev1 (all interior rows identical; the only new/changed row is the grand total).
- Perimeter LF = 81.11 + 216.32 + 99.74 + 20.26 = 417.43. Grand total LF: rev0 979.87 - 417.43 = 562.44 = rev1 562.44. PASS.
- Interior subtotals unchanged (Type 2 273.57, 5 5.70, 3 38.68, 4 82.47, H1 42.15, ... ).
- Board SF column: 17,852.41 - 2,469.21 (1B sheathing) = 15,383.20 = rev1. PASS.
- Material Summary: 3-5/8" bottom/top track 761.54 -> 443.85 (-317.69 = 1A+1+1C LF); 8" track 99.74 -> row removed; 8" stud 2,332.99 -> row removed; 1/2" exterior sheathing row removed; slab pins 1,051.87 -> 634.44 (-417.43 exact); 3-5/8" stud 16,751.65 -> 10,059.08; bracing 5,230.74 -> 2,827.81. PASS.

## 2. W.R. (Type X W.R.) - PASS
Recomputed from board_out.json (16 faces tagged `5/8 type X WR`): 1,024.02 SF.
- Women's 109 = 226.62, Men's 108 = 223.02, Janitor 107 = 485.75 (13 faces, all faces of those rooms; no non-WR face in those rooms) = 935.39
- Drinking-fountain alcove corridor faces W2-06.2 21.18 + W2-06.3 46.27 + W2-06.4 21.18 = 88.63 (W2-06.1/.5, W2-05, W2-08 corridor faces correctly stay Type X)
- 935.39 + 88.63 = 1,024.02 = Excel (Material Summary row 20, Pending RFI-11, Scope ALC-07/08). Reconciliation of rev0 935.4 and audit ~1,326 is stated in RFI-11. Break room kitchenette wall is existing (EXT-07), so no W.R.

## 3. Board types - PASS
- Type X 14,557.36 (canon sum 14,557.38; 0.02 rounding) + W.R. 1,024.02 + regular 981.38 (ceilings only) = 16,562.76 vs rev0 regular 16,562.77 (-0.01 SF). Perimeter had 0 board in rev0, so total unchanged. PASS.
- Wording: RFI-27 correctly flags that ceilings stay regular and asks to confirm (4/A-121, 5/A-121 call Type X).

## 4. FRT - PASS (0.02 SF rounding)
- Blocking row: 552.27 LF = 387.0 + 69.0 + 85.6 + 10.67 (exact). Pieces 636 = ROUNDUP(635.11).
- 3/4" FRT plywood: rev0 63.48 -> 137.40. Expected 63.48 + 60.605 (23.46 x 31/12) + 13.33 = 137.42; delta -0.02 SF (rounding of 60.605 to 60.61 and hand-keyed value). Immaterial; sheets 4 unchanged either way.
- Restroom 13.33 SF (10 pcs x 16" x 12") rests on an assumed 12" height; this is documented as Review Item 12/12 and in RFI-23.

## 5. Material Summary / text - PASS with notes
- Arithmetic: all rows pass net x waste% = waste and net + waste = purchase (live formulas; pieces use ROUNDUP). No failures.
- Subtotals: Partition Takeoff subtotals/grand total add up (562.44 LF, 15,383.20 SF).
- Spanish: none in cells (only the `_reglas` hash sheet, English). PENDING: no quantities marked PENDING in Partition Takeoff (statuses [DERIVED]); "Pending:" appears only in RFI-16 prose in Pending Items.
- Closed RFIs state the decision: RFI-01, 11, 23, 27 say "CLOSED - estimator decision 2026-10-24 (rev1)" with Applied figures; RFI-02, 07, 10, 25, 26 marked N/A / merged after RFI-01.

## Findings (non-blocking)
1. Unexplained 6" stud change: 2,925 -> 2,900 LF (-25, one 25-ft stud) while 6" track is unchanged (118.59). No perimeter wall is 6", and RFI-01 text does not mention it (git diff of familias_out.json shows the key moved 2925 -> 2900). Total stud reduction is 9,050.56 LF (6,692.57 + 2,332.99 + 25.00) vs "-8,901 LF" quoted in the decisions file (the decision figure used a different baseline, 16,812.96 incl. soffit studs; 149.56 LF gap not reconciled). Estimator should confirm the -25 LF.
2. Additional head track at openings > 4'-0": 19 LF -> 0 with no explanation in Pending Items (presumably perimeter doors 10/12/13, consistent with RFI-10 N/A, but not stated).
3. Scope Checklist ALC-01 still lists types 1A, 1, 1B, 1C and "8" stud families" as quantified framing - stale text vs rev1 (ALC-02/09 are updated correctly).
4. RFI-01 Applied figures quote 3-5/8" stud 16,812.96 -> 10,120.39, which differ from the Material Summary rows (16,751.65 -> 10,059.08) by 61.31 LF (soffit stud row listed separately). Delta (6,692.57) is identical; label the baseline.
5. Pre-existing, unchanged vs rev0: Partition Takeoff wall board 15,383.20 SF vs Material Summary wall board 15,581.38 SF (diff 198.18 SF) - same gap in rev0, not a rev1 regression.

## Verdict
PASS. All five checks pass; rev1 reconciles to rev0 and the decisions to within 0.02 SF. Recommend fixing/confirming findings 1-3 (text and the -25 LF 6" stud) before release; none changes the check totals.

---
## Addendum (main session) — disposition of the non-blocking findings
- **6" stud −25 LF (and the extra 3-5/8" difference):** the walls that ended on the body of a perimeter wall (W2-02, W2-05, W2-07, W2-08, W2-09, W5-01) had T nodes. The T added the backing stud inside the perimeter wall. With the perimeter wall existing, each end becomes a free end (one end stud), so each wall loses one stud at its height. 3-5/8": 5 x 25 = 125 LF; 6": W5-01 1 x 25 = 25 LF. This explains the gap between 9,050.56 and the −8,901 LF in the decisions file (8,901 was the perimeter walls' own studs).
- **Additional head track 19 → 0 LF:** the 19 LF belonged to the existing doors 12 and 13 (openings > 4'-0" in perimeter walls). They are now listed as existing, with no work in our scope (RFI-10 N/A).
- **ALC-01 stale text:** fixed. The Excel was re-armed after this fix; only the Scope Checklist text changed.
- **Baseline 61.31 LF (soffit stud row) and the 198.18 SF board gap (same as rev0):** noted; no quantity change.
