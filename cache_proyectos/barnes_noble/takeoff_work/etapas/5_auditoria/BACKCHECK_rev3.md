# BACKCHECK rev3 vs rev2 (independent, openpyxl data_only)

## Verdict: PASS WITH FLAGS (2 text/number inconsistencies, 1 unreconciled stud delta, 1 expected-total slip)

## 1. Grand total
- rev2 562.44 LF; rev3 568.61 LF. Delta +6.17 = W2-05 +5.00 + type 4 +1.17.
- FAIL on the brief's number: 562.44 + 5.00 + 1.17 = 568.61, NOT 567.61. The brief (567.61) has an addition slip; the workbook is right.
- Subtotals: type 2 273.57 -> 278.57; type 4 82.47 -> 83.64 (12 walls); type I 3.31 LF unchanged. Board SF grand total 15,383.20 -> 15,446.22 (+63.02 = W2-05 +95.21, type 4 +17.46, type I -49.65). PASS (soffit rows 103-106 sit outside the grand total).

## 2. Partition Takeoff changes (all explained)
- W2-05: 7.92 -> 12.92 LF, board 146.52 -> 241.73 (RI 1). PASS.
- W4-29a-f / W4-30a-f: 25.68 each (4.27-4.29 per chord), +1.17 LF total (RI 2 / RFI-18). PASS.
- C-I board 57.75 -> 23.10 (2.31 x 10 ft GWB above 15'); C-E1-P.1 25 -> 10 (1.00 x 10); type I 82.75 -> 33.10 (RI 8). PASS.
- SS-E 141.68 -> 101.20 (10.12 x 10 GWB; FRT 10.12 x 4 = 40.48). SS-N unchanged in this sheet (318.78), FRT 22.77 x 2 = 45.54 is in RFI-14 text. PASS (see flag C).

## 3. Material Summary changes (rev2 -> rev3 net; arithmetic net x waste = waste and net + waste = purchase PASS on every row)
- Bottom and Top track 3-5/8: 443.85 -> 450.02 (+6.17 LF = W2-05 + type 4). PASS.
- Bracing C.R. channel 2827.81 -> 2858.98 (+31.17; consistent with +5 LF type 2 and +1.17 type 4 rows). PASS.
- Braces: 117 x 4 = 468 LF, RFI-04 text matches. Included in 3-5/8 stud.
- Furring 493.02 -> 182.79 = -310.23 exact. Carrying 341.09 -> 146.92 = -194.17 exact. PASS.
- Ceiling track 385.99 -> 321.78 = -64.21 (net of -107.21 cloud track and +43.0 vestibule track: 6" 25.33 + 8" ledger 12.67 + 3-5/8" 5.0). PASS.
- New rows: DGLW26 main tee 194.16 (5 x 38.833); cross tee 457.96 = 31 x 14.773 (124 pcs; the decisions file's 443.19/120 is superseded, agrees with session note); DGCM27 107.21; DGWM24 107.21. PASS.
- New rows 8" joist 88.0 (11 x 8.0) and 8" stud 25.33 (box beam). PASS.
- Type X GWB 15,538.74 -> 15,670.56 (+131.82). Explained part: partitions +63.02, SS-E -40.48, vestibule +105.5 (97.1 + 8.4) = +128.04. Residual +3.78 SF not attributed (flag B).
- W.R. GWB 1024.02 -> 1020.33 (-3.69 SF) with no matching Partition Takeoff change (flag A).
- FRT 5/8: 2528.42 -> 2664.09 (+135.67 = 49.65 + 40.48 + 45.54 exactly). PASS. FRT 3/4: 141.84 -> 248.46 (+106.62 = vestibule 106.6). PASS.
- 3-5/8 stud 10059.08 -> 10778.08 (+719.00): braces +8 and vestibule posts +126 explain 134; remaining +585 LF (W2-05 extra studs at 25 ft, type 4 chords, soffit studs to deck) cannot be reconciled from the notes alone (flag B2, low risk).
- Screws, tape, compound, pins, framing screws move proportionally to the above (plausible).

## 4. Other checks
- Spanish text in the Excel: none found (accent and common-word regex over all sheets). PASS. (familias_out.json keys are Spanish, internal only.)
- Review Items sheet: header rows only, no open items. PASS.
- RFIs: RFI-04, 06, 08, 15, 18, 19 CLOSED; RFI-14, 17 PARTLY CLOSED with open deltas; RFI-16 CLOSED except post sheathing. Deltas updated (RFI-03 414.54, RFI-22 122.32, slab pins). PASS.

## 5. Flags
- A. RFI-11 note says W.R. = 1,020.33 SF but its components (226.62 + 223.02 + 485.75 + 88.63) still sum to 1,024.02. Number and note disagree by 3.69 SF.
- B. RFI-27 note: Type X 15,670.56 = "walls 14,557.36 + ceilings 981.38" sums to 15,538.74 (stale breakdown, +131.82 SF missing). Ties to the 3.78 SF residual and the 585 LF stud delta being only partly attributed.
- C. SS-N GWB stays 318.78 in the soffit row although 45.54 SF of it is now FRT; confirm whether GWB net in the Material Summary was reduced by 45.54 (not visible; residual +3.78 SF suggests it may not have been).
- D. Brief's expected total 567.61 is an arithmetic slip; correct value 568.61.

---
## Addendum (main session) — disposition of the flags
- **Grand total:** 568.61 LF is correct (the brief's 567.61 was an addition slip).
- **RFI-11 / RFI-27 delta text:** FIXED to the rev3 figures.
  - W.R. 1,020.33 = Women's 222.93 + Men's 223.02 + Janitor 485.75 + alcove 88.63. The W2-05 Women's face is 7.51 LF (A-101).
  - Type X 15,670.56 = walls 14,583.68 + ceilings 981.38 + vestibule 105.5. That covers the +3.78 residual.
  - The Excel was re-armed; only the Pending Items text changed.
- **3-5/8" stud +719 LF:**
  - braces 468 (no braces were carried in rev2);
  - vestibule posts 126;
  - W2-05 +5.00 LF at 25 ft, about 5 more studs = 125.
  - Total 719.
- **SS-N:** the 2 ft FRT band is 9'-0" to 11'-0", below the soffit side GWB (11'-0" to 25'-0", 14 ft). The two do not overlap, so the GWB stays as it is (soffit height conflict = RFI-14).
