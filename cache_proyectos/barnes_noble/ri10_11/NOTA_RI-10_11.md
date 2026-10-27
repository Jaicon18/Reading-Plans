# RI 10 (RFI-15) and RI 11 (RFI-16) — resolved from the drawings (Excel not changed yet)

## RI 10 a) Cafe Seating GWB cloud = USG drywall suspension grid (4/A-121)
- **Printed on 4/A-121 "USG Drywall Suspension System Details":**
  - "USG DRYWALL SUSPENSION CROSS TEE DGLW424"
  - "MITERED USG DRYWALL SUSPENSION MAIN TEE DGLW26"
  - "USG DGCM27 CHANNEL MOLDING", "USG DGWM24 ANGLE MOLDING"
  - "J-BEAD", "USG SHEETROCK BRAND DUR-A-BEAD CORNER BEAD"
  - "5/8" USG ECOSMART FIRECODE X (UL TYPE ULIX) PANELS", "HANGER WIRE"
  - Image: `1_A-121_4_USG_drywall_suspension.png`.
- **Cloud:** 573.69 SF, 38.833 x 14.773 ft, perimeter 107.21 LF (A-121, measured), height 12'-0".

| Item | Quantity | Operation | Status |
|---|---|---|---|
| Main tee DGLW26 (12') | 194.17 LF = 17 pcs | mains @ 48" O.C. across 14.773: ROUNDUP(14.773/4)+1 = 5 x 38.833 | DERIVED; 48" spacing = USG standard, not printed |
| Cross tee DGLW424 (4') | 443.19 LF = 120 pcs | @ 16" O.C. along 38.833: ROUNDUP(38.833/1.333)+1 = 30 rows x 14.773 (4 pcs / row) | DERIVED; 16" spacing = USG drywall standard, not printed (24" alternative = 21 rows, 84 pcs) |
| Channel molding DGCM27 | 107.21 LF | cloud perimeter | DERIVED |
| Angle molding DGWM24 | 107.21 LF | cloud perimeter | DERIVED |
| Hanger wire | 55 pcs x 13.0 ft = 715 LF | 5 mains x (ROUNDUP(38.833/4)+1 = 11); drop 25'-0" - 12'-0" | unchanged |
| Remove from cloud: furring channel −310.23 LF, carrying channel −194.16 LF | | hat-channel system replaced by the grid | |
| J-bead / corner bead | 107.21 LF each | already carried (audit F-06) | |

## RI 10 b) Carrying channel direction = E-W (CONFIRMED)
- No S sheets in the set.
- **1/A-400A** (north wall, E-W extent): the joists are drawn cut, in section, at regular spacing.
- **2/A-400A** (east wall, N-S extent): the joists are drawn in profile, bearing on a girder.
- So the joists run N-S, and the carrying channel runs perpendicular to them = **E-W**, which is the assumption already carried.
- No recalculation needed.
- Images: `2_A-400A_1_joists_in_section_run_N-S.png`, `3_A-400A_2_joists_in_profile_N-S.png`.

## RI 11 Vestibule GWB ceiling box (1/A-210, 4/A-210, 5/A-210, 6/A-210, A-121 key note 5)
- **Printed:**
  - 4/A-210: "ONE LAYER OF 3/4" PLYWOOD", "8" JOISTS @ 16" O.C.", "8" BOX BEAM BEARING ON CORNER POST", "(1) LAYER OF 5/8" GYP. BD.", "8" LEDGER", "B.O. CEILING 10'-6"".
  - 1/A-210: "8" JOIST @ 16" O.C." (arrow E-W), "5" X 5" BOXED COLUMN, SEE TYPICAL DETAIL THIS SHEET (TYP.)".
  - 6/A-210 NESTED COLUMN: "(2) 3 5/8" X 18 GA STUDS", "3 5/8"x16 GA TOP & BOTTOM TRACK", "(8) #10-16 TEKS 16" O.C.". NESTED BEAM: "(2) 8" X 18 GA STUDS", "6"x16 GA TOP & BOTTOM TRACK".
  - 5/A-210: "NEW 3 5/8" NESTED LT GAUGE POST", "5/8 GYP. BOARD SHEATHING AS REQUIRED".
- **Plan dimensions:**
  - E-W: 5" + 2" + 7'-8" + 2" = 8'-5".
  - N-S: 5" + 2" + 2'-2" + 2" + 5" + 6'-0" + 5" + 2" + 2'-2" + 2" + 5" = 152" = 12'-8".
- Images: `4_A-210_1_vestibule_plan.png`, `5_A-210_4_vestibule_section.png`, `6_A-210_6_nested_column_beam.png`.

| Item | Quantity | Operation | Status |
|---|---|---|---|
| 8" joist (new family) | 11 pcs x 8.0 ft = 88.0 LF | ROUNDUP(152/16)+1 = 11; length 7'-8" + 2" + 2" (box beam to ledger) | DERIVED |
| Box beam (nested): 8" x 18 ga stud | 25.33 LF | (2) x 12.667 | DERIVED |
| Box beam: 6" x 16 ga track | 25.33 LF | (2) x 12.667 | DERIVED |
| 8" ledger (track) | 12.67 LF | 1 x 12.667 (east, at the existing storefront) | DERIVED |
| Posts 5" x 5" nested: 3-5/8" x 18 ga stud | 126.0 LF (6 posts) | 6 x (2) x 10.5 ft (to B.O. ceiling 10'-6"); 6 drawn on 1/A-210 (4 west + 2 east corners - confirm the east 2 are not existing storefront) | DERIVED |
| Posts: 3-5/8" x 16 ga track | 5.0 LF | 6 x 2 x 5" | DERIVED |
| 3/4" FRT plywood (A-410 "ALL PLYWOOD NEEDS TO BE FRT") | 106.6 SF | 8.417 x 12.667 | DERIVED |
| 5/8" Type X GWB ceiling (underside) | 97.1 SF | 7.667 x 12.667 | DERIVED |
| 5/8" GWB at box beam faces | 8.4 SF | 12.667 x 8" | DERIVED |
| 5/8" GWB post sheathing (5/A-210 "AS REQUIRED") | — | extent not printed | PENDING |
| Trim | — | none drawn | — |
