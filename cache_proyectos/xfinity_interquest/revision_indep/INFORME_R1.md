# INFORME R1 - Independent adversarial review (U-138 / U-168 part A)
Project: Xfinity Interquest TI, 1333 Interquest Pkwy, Colorado Springs CO
Reviewed: `etapas/8_excel/XF_Takeoff_FINAL_rev1.xlsx` + `etapas/4_canon/takeoff_canon.json`
Source: `plans/bidset_SIN_MARKUPS.pdf` (visible pt, 18 pt/ft on A1.0/A2.0/A3.0)
Crops: `/root/xf/work/revision_indep/R1/*.png` (red circle = evidence). Every crop was re-opened after it was drawn.
Read only: nothing outside this folder was edited.

Counts: **ERROR 4**, **FALSE ALARM risk 2**, **MINOR 8**

---

## Findings

### 1. ERROR: brace stock length. Each 19.09 ft brace is cut from a 14 ft stick.
- **What:** Material Summary row 19 ("Metal stud brace to structure") has 5 braces x 19.092 LF = 95.46 LF, bought as "stick 14 ft", Pieces = ROUNDUP(109.78/14) = **8**. A 19.09 ft brace cannot come out of a 14 ft stick. Eight sticks are enough only if all 5 braces are spliced, and 4/A2.0 shows no splice. It prints a single member: "BRACE TO STRUCTURE ... MATCH WALL STUD SIZE & GAUGE (3 5/8" 20 GA. MIN.) ... MAXIMUM LENGTH OF BRACE 25'-0"".
- **Evidence:** 4/A2.0 `F01_4A2.0_brace_25ft.png`; A0.1 26 FT `F01_A0.1_26FT.png`.
- **Correct:** buy one piece per brace at a stock length of at least 19.1 ft. That is **5 pcs x 20 ft** (3-5/8" 362S125-33), = 100 LF. The other way is 10 x 14 ft with splices, and the estimator would have to accept those splices. Add a "Brace stock length" Inputs cell (20 ft), or a per-piece rule n_braces x ceil(19.09/stock).

### 2. ERROR: door 101 header is missing the nested stud (7/A2.0)
- **What:** row 12 "Header / metal stud box beam" = 4.33 LF, "(3.0 + 1.333) x **1** pieces TRACK HEADER". 7/A2.0 "TYPICAL HEAD DETAIL (JAMB SIM)" prints two members: "3-5/8" METAL TRACK" **and** "3-5/8" METAL STUD NESTED IN METAL TRACK".
- **Evidence:** 7/A2.0 `F02_7A2.0_head_track_nested_stud.png`.
- **Correct:** 2 pieces x (3.0 + 1.333) = **8.67 LF** (4.33 track + 4.33 stud 362S125-33). Purchase: 8.67 x 1.15 = 9.97 LF, 1 stick of 14 ft. The pieces to buy do not change, but the LF is wrong.

### 3. ERROR: DEMO-03 / DEMO-04 stop at the removed door instead of running through it
- **What:** on A1.0 the existing swing door that key 7 removes sits in the line of the dashed wall. It runs from the DEMO-03 corner (x 866.28) to the start of DEMO-04 (x 928.32), y 1452.5-1459.8. Excel measures DEMO-04 from 928.32, so it leaves out the wall over the door head. Standing rule: walls are measured through door openings.
- **Evidence:** A1.0 `F03_A1.0_door_gap_DEMO03_04.png`, `a10_door_gap_DEMO03_04.png`.
- **Correct:** (928.32 - 866.28)/18 = **3.447 LF**. x 26.0 ft = **+89.6 SF**. Demolition 1,651.88 becomes **1,741.5 SF**, and the sensitivity in RFI-01 / RI 3/6 becomes 66.98 SF per ft.

### 4. ERROR: no backing for the GF-14496 graphic frame on the new W2 wall, and the canon reason "no backing called" is wrong
- **What:** A4.0 hangs GF-14496 "144" x 96" GRAPHIC FRAME" (fixture schedule count 1, dim "12'-0" GRAPHIC") on the W2 line, starting 8'-6 3/8" from the north wall. The Retail 100 room tag on A4.0 carries key notes **1** 2 5 10 15. Key 1 reads "PROVIDE BLOCKING SUPPORT BEHIND WALL-MOUNTED EQUIPMENT - SEE DTL 8/A2.0". A2.0 key note 2 says the same. The canon (`walls[W2-01].openings_note`) says "no backing called", and the Excel has no row or reason for it. The plans settle the question, so no RFI is needed.
- **Evidence:** `F04_A4.0_GF-14496_on_W2_and_Retail_key1.png` (frame + Retail key tags), `F04_A4.0_key1_text.png`, 8/A2.0 `F07_8A2.0_backing_16ga.png`, 9/A5.0 "WALL MOUNTED GRAPHIC PANEL" (`a50_top.png`).
- **Correct:**
  - The frame runs from 8.531 to 20.531 ft from the north face. It lies on W2-01 from 8.531 to 13.973 = 5.44 ft, on the existing post for 1.0 ft, on W2-02 for 4.0 ft, and on existing W4 for 1.57 ft.
  - 8/A2.0 backing is 16 ga x 6" x 1-1/2" unpunched track, extended 1 bay beyond the edge of the equipment. On the new walls one row is 5.44 + 1.333 + 4.0 = **10.78 LF**. The number of rows is not printed: 1 row is the minimum, and 2 rows (top and bottom of a 96" frame) = 21.55 LF.
  - 8/A2.0 also prints "16 GA. METAL STUD 16" O.C. @ ALL BACKING STUD TRACKS". About 9 W2 studs in that zone (12.5 ft each) change from 33 mil to 16 ga (54 mil), with the same LF moving between gauges.
  - Add a row, or a Review Item that states the row count.

### 5. FALSE ALARM risk: DEMO-08 / DEMO-09 counter core carried at 26 ft
- **What:** the L-shaped core between two dashed counters with sinks (RFI-03 closed as "wall"), 18.507 LF, is carried at 26 ft = **481.2 SF** (29% of all demolition). Its height is printed nowhere, and a core between counters is often a pony wall. The rule (highest printed value plus RFI) is followed, but RFI-01 does not show this element on its own line.
- **Evidence:** A1.0 `F05_A1.0_DEMO08_09_counter_core.png`.
- **Correct:** keep 26 ft. In RFI-01 / RI 3/6, add a separate alternative for DEMO-08/09: at 4 ft high the result is 74.0 SF, delta -407.2 SF.

### 6. FALSE ALARM risk: stud gauges heavier than the printed minimum
- **What:**
  - CF studs are 250S125-43 @16" (13'-0"). The A2.0 table also passes **250S125-33 @12" = 13'-2" ≥ 12'-6"**. Each furring face is ≤ 11.3" (0.94 / 0.72 ft), so the corner studs are already ≤ 12" o.c.
  - W2 studs are 362S125-33. The printed minimum, 4/A2.0 "3 5/8" 20 GA. MIN.", is also met by **362S125-30** (20 ga EQ, 15'-6" @16").
  - RFI-05 rests on a table that assumes walls "FULLY SHEATHED ... ON BOTH SIDES", but 5/A2.0 is one side.
- **Evidence:** `F06_A2.0_limiting_heights_2-5-8.png`, `F06_A2.0_limiting_heights_362S125-30.png`.
- **Correct:** LF does not change. Either state the choice as conservative, or price 250S125-33 / 362S125-30 and say so in the RFI-05 / gauge note.

### 7. MINOR: blocking material rows have the wrong product description
- Row 15 calls the EV-44/45 item "stud blocking ... stick 14 ft". The A5.0 legend prints "PROVIDE 6" SHEET METAL BLOCKING STRAPPING" 7'-3" at 7'-9 1/2". That is a flat strap with the gauge not printed, not a stud.
- Row 16 "backing (per source)" does not name the 8/A2.0 product: "16 GA. X 6" X 1-1/2" UNPUNCHED METAL TRACK".
- Evidence: `a50_top.png`, `F07_8A2.0_backing_16ga.png`.
- Fix the labels and the selling unit. Quantities are unchanged (14.5 / 5.33 LF).

### 8. MINOR: wrong source cited for the track gauge
- Rows 4 and 6 give the track gauge as "4/A2.0 'MATCH WALL STUD SIZE & GAUGE (3 5/8" 20 GA. MIN.)'". That note is for the **brace**, not the track.
- Cite instead: track = stud gauge (2/A2.0 + limiting heights table), and 4/A2.0 "TOP OF TRACK SECURED TO STUDS".

### 9. MINOR: trims run to 6" above the ceiling
- CB-6A20 = 12.5 + 10.5 = 23.0 LF. The exposed edge stops at the ceilings, 12.0 + 10.0 = **22.0 LF**.
- LB-COL-CORNERS and LB-COL-PIER use 12.5. They should use **12.0**, giving 48 + 48 = **96 LF**.
- No purchase change (corner bead 4 pcs, L bead 12 pcs).

### 10. MINOR: board above an existing hard ceiling
- W2-02 hallway face is 9.5 ft and the SOF-01 hallway face top is 9.5 ft. The hallway ceiling is "EXISTING GYP. BD. 9'-0" AFF" to remain (A1.0 key 16), so the 6" above it cannot be boarded without opening that ceiling.
- Difference: (4.0 + 4.247) x 0.5 = **4.1 SF**. No sheet change.
- Evidence: `A2_A3.0_hallway_9-0.png`.

### 11. MINOR: "Layers" column on the Partition Takeoff
- It shows 2 for W2, which is 2 faces with 1 layer each. Rename the column to "Faces x layers", or put 1.

### 12. MINOR: A1.0 key 13 storefront bulkhead
- Key 13 reads "EXISTING STOREFRONT BULKHEAD ABOVE. PATCH AND MATCH AS REQUIRED (V.I.F.)". ALC-13 says only "existing to remain".
- Add it to the patch-and-repair allowance (ALC-E12 / RI 1/6).

### 13. MINOR: EV-44 / EV-45 count not reconciled in writing
- The A4.0 fixture schedule says EV-44 = 6 and EV-45 = 1. The take-off has 2 straps of 7'-3": the north group of 3 modules (EV-45 + 2 EV-44) and the south group of 3 EV-44. That matches the legend's single 7'-3" strap per 3-module unit, but the reconciliation is not written down. Add one line to BK-EV44-N/S.
- Evidence: `a40_north_EV44_45.png`, `a40_south_wall_EV44.png`.

### 14. MINOR: SOF-01 header has no support line
- The 4.25 ft x 2 ft box header has no stated support (to the walls at its ends, or hangers to structure). RI 6/6 covers the framing method. Add "support: end bearing on existing restroom wall / post" so the bid is not challenged.

---

## A1. Re-measure (vector, 18 pt/ft)

| Wall / element | Sheet | Excel LF | Measured LF | Operation | Delta | OK |
|---|---|---|---|---|---|---|
| W2-01 | A2.0 | 13.973 | 13.973 | stub 1237.56-1243.56 (0.333) + door 1243.56-1297.56 (3.000) + hatch 1297.68-1489.08 (10.633) = (1489.08-1237.56)/18 | 0.000 | OK |
| W2-02 | A2.0 | 4.000 | 4.000 | hatch (1578.96-1506.96)/18; printed 4'-0" | 0.000 | OK |
| CF-01 | A2.0 | 2.380 | 2.380 | box 1546.92-1559.88 x 1346.52-1363.44: (16.92 + 2 x 12.96)/18 | 0.000 | OK |
| CF-02 | A2.0 | 2.380 | 2.367 | box 1546.92-1559.76 x 1706.52-1723.44: (16.92 + 2 x 12.84)/18 | -0.013 | OK |
| SOF-01 header | A3.0 | 4.247 | 4.247 | strip 846.84-923.28 (y 1618.2/1625.52): 76.44/18 | 0.000 | OK |
| DEMO-01 | A1.0 | 4.260 | 4.260 | dashed y1495.92, x 758.52-835.2 | 0 | OK |
| DEMO-02 | A1.0 | 1.320 | 1.320 | 842.52-866.28 | 0 | OK |
| DEMO-03 | A1.0 | 2.413 | 2.413 | x 858.96, y 1452.48-1495.92 | 0 | OK |
| DEMO-04 | A1.0 | 25.900 | 25.900 (+3.447 through door, F3) | outer face y1459.8, x 928.32-1394.52 | 0 / +3.447 | OK as drawn; F3 |
| DEMO-05 | A1.0 | 5.647 | 5.647 | x 1387.2, y 1350.84-1452.48 | 0 | OK |
| DEMO-06 | A1.0 | 2.500 | 2.500 | x 1348.08, y 1244.52-1289.52 | 0 | OK |
| DEMO-07 | A1.0 | 2.987 | 2.987 | y 1296.84, x 1340.76-1394.52 | 0 | OK |
| DEMO-08 | A1.0 | 11.240 | 11.240 | y 1629.48, x 897.96-1100.28 | 0 | OK |
| DEMO-09 | A1.0 | 7.267 | 7.267 | x 1092.96, y 1636.8-1767.6 | 0 | OK |

Crops: `A1_W2-01_W2-02_A2.0.png`, `A1_CF-01_A2.0.png`, `A1_CF-02_A2.0.png`, `A1_SOF-01_A3.0.png`, `A1_DEMO01-09_A1.0.png`.

Corner overlaps were checked: there is no double count at the corners DEMO-04/05, 06/07, 08/09 or 02/03.

Swept with no new wall found:
- the long single dashed line at A1.0 x 835.2 (y 1244-1496), which is the key 14/15 ceiling-scope boundary and not a wall;
- the untagged dashed rectangle at x 1462-1513, which is not a key 7 wall.

## A2. Heights

| Height | Where used | Printed source N/SHEET | Value | OK? |
|---|---|---|---|---|
| W2 stud height | W2-01, W2-02 | A3.0 RETAIL "2x4 ACT 12'-0" AFF" + 2/A2.0 "FROM SLAB TO 6" ABOVE CEILING U.N.O." + 4/A2.0 6" TYP; 9/A5.0 "12'-0" TO B.O. CEILING" | 12.5 | OK |
| W2-01 face A (Retail) | board | A3.0 12'-0" + 6" | 12.5 | OK |
| W2-01 face B (Storage) | board | A3.0 "EXIST. GRID & NEW TILES 2x4 ACT 10'-0" AFF" + 6" (A4.0 RFS 10'-0") | 10.5 | OK |
| W2-02 face A (Retail) | board | A3.0 12'-0" + 6" | 12.5 | OK |
| W2-02 face B (Hallway) | board | A3.0 "EXISTING GYP. BD. 9'-0" AFF" + 6" | 9.5 | MINOR F10 (9.0 max under the existing hard ceiling) |
| Column furring CF-01/02 | studs + board | A2.0 key note 1 "(1) LAYER 5/8" GYP. BOARD TO 6" ABOVE CEILING" + 12'-0" | 12.5 | OK |
| SOF-01 bottom | header | A3.0 "GYP. BD. 8'-6" AFF" | 8.5 | OK |
| SOF-01 storage face | 8.5 -> 10.5 | A3.0 storage 10'-0" + 6" | 2.0 ft | OK |
| SOF-01 hallway face | 8.5 -> 9.5 | A3.0 hallway 9'-0" + 6" | 1.0 ft | MINOR F10 (0.5 ft) |
| Door 101 head | header / cripples | A2.0 door schedule 7'-0" + 2" HM head (derived) | 7.167 | OK (derived) |
| Demo height | DEMO-01..09 | A0.1 "HEIGHT IN STORIES: 1 STORY - 26 FT" (highest printed value; RFI-01) | 26.0 | OK per rule; F5 |
| Brace rise | 4/A2.0 | 26.0 - 12.5 at 45 deg = 19.09 ≤ 25'-0" max | 19.09 | OK; F1 stock |
| Trim heights | CB / L bead | exposed to ceiling 12.0 / 10.0 | 12.5 / 10.5 used | MINOR F9 |

Crops: `A2_A3.0_retail_12-0.png`, `A2_A3.0_storage_10-0.png`, `A2_A3.0_hallway_9-0.png`, `A2_A2.0_keynote1_CF.png`, `F01_A0.1_26FT.png`.

## A3. Sweep

- **RCP A3.0:** every room is either quantified or excluded with a reason.
  - Retail and Storage are ACT (rule).
  - Hallway, Toilet 103 and Toilet 104 have existing gyp. bd. to remain (A1.0 key 16).
  - Landlord is N.I.C.
  - SOF-01 is the only new gyp ceiling element.
  - 2/A3.0 (ceiling spans) and 3-4/A3.0 belong to the ACT or unused framing; they are not needed for a 0.41 ft wide underside.
- **A2.0 plan:** the only new walls are W2-01, W2-02, CF-01 and CF-02. W2A and W3 appear in the legend only.
- **A2.0 key notes 1-15:** swept. The only gap is key 2 / A4.0 key 1 for GF-14496 (F4).
- **Other items swept:** A5.0 blocking legend, EV-10-6 (plywood, Div. 06), elevations 8 and 9, A4.0 keys 1 / 4 / 13, and details 3-8/A2.0. Missed items: the 7/A2.0 nested stud (F2) and the GF-14496 backing (F4).

## A4. Exclusions and RFIs

- **Exclusions:** every Scope Checklist EXCLUDED item cites a printed note or a standing rule (ACT, painting, insulation, Div. 06, fasteners, sealant, doors, MEP, ducts, existing-ceiling demolition, N.I.C.). Gap: A1.0 key 13 bulkhead patch (F12).
- **RFI-01 (open): valid.** No B.O. structure, deck or joist elevation is printed on A0.1-A5.0 or in the E/M/P SHX annotations (412 / 172 / 136 / 13 / 86 / 512 / 116 / 2 / 140 annotations searched). M1.0 has only "EXISTING CONCRETE BEAM ABOVE CEILING" and E2.0 only "18" ABOVE ROOF" (WeBoost); neither gives a structure height.
- **Closed RFIs:**
  - **RFI-02:** supported by the A3.0 tag "GYP. BD. 8'-6" AFF", which lacks "EXISTING".
  - **RFI-03:** supported by the key 7 arrow to the core (height: see F5).
  - **RFI-04:** supported by "3'-0" DOOR".
  - **RFI-05:** supported by the table row 250S125-43 @16" = 13'-0", but the lighter 250S125-33 @12" also passes (F6).

## Materials vs details (summary)

| Item | Status |
|---|---|
| Studs 3-5/8" 33 mil @16" | OK (F6 lighter option) |
| 2-1/2" 43 mil, 6 studs per column (2 per exposed face, 5/A2.0 "TYP. ALL SIDES") | OK |
| Bottom / top track by size | OK (F8 cite) |
| Board both faces, no opening deduction | OK |
| Header | F2 |
| Braces 4/A2.0 @8'-0" max, n = 3 + 2 | OK; stock F1 |
| EV-44/45 6" strap | label F7 |
| 8/A2.0 16 ga track | label F7; missing at GF-14496 F4 |
| Corner bead 6/A2.0, L bead 5/A2.0 | OK; F9 |
| Compound / tape by yield on 483.35 SF | OK; it changes only if board changes |
