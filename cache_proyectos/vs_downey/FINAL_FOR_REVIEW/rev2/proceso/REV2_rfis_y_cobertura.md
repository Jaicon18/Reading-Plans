# REV2: take-off of Victoria's Secret #679 Downey (metal framing + gypsum board)

`python3 validar_canon.py takeoff_canon_AB.json tools` printed CANON OK after each task and at the end.

## Task 1: RFI-18 / RFI-19, shelving on the walls (both closed)

**Rule used:** S01.01 N note: where shelving occurs on both faces of a single stud wall, the stud spacing is halved and the A/S03.01 diagonal spacing is halved.

**Reading the sheets:** A06.01 fixture codes plus A02.01 keynotes 33 and 39. B/A10.03 shows "GLASS SHELF W/ BRASS TRIM (TYPICAL OF 5)", so a Garcy panel counts as shelving.

| Wall | Change | N/SHEET | Stud delta |
|---|---|---|---|
| W089 TRANS #5 N | 16" -> 8" | S01.01 N note; A06.01 WPNF / WP2F-VDB4 on both faces | 5 -> 8 studs (+36.0 LF) |
| W090 TRANS #5 S | 16" -> 8" | A06.01 WP1FR both faces; A02.01 14'-1 1/2" + 14'-6" OVERALL | 14 -> 25 (+132.0 LF) |
| W101 TRANS #3 S | 16" -> 8" | A06.01 + A02.01 keynote 39, both faces | 15 -> 27 (+144.0 LF) |
| W106 TRANS #2 N | 16" -> 8" | same | 15 -> 27 (+144.0 LF) |
| W107 TRANS #2 S | 16" -> 8" | same | 15 -> 27 (+144.0 LF) |
| W099 TRANS #3 N | 8" zone, 4.73 ft (vector), TRANS #4 face against Room 2 | A06.01 | 17 -> 22 (+60.0 LF) |
| W076 RFID | 8" zone, CW CLOSET #1 4'-10": keynote 33 shelving on one face, 2442F racks on the other | A02.01, K/A10.05 | 20 -> 25 (+60.0 LF) |
| W040 break room / MGR | two 8" zones (3.74 + 2.70 ft) where A-2 shelving is on both faces | A02.01 keynote 33, A/A14.01 | 12 -> 19 (+84.0 LF) |
| I03 RECEIVING (supports the 2442F rack) | 16" -> 12": TABLE A3 362S162-43 @12", max 14'-0" | S01.01 TABLE 3 -> S03.02 A3 | 17 -> 22 (+60.42 LF) |
| W001 STOCK run, W067, W075/W076 | Unchanged: TABLE A1 362S162-33 @16", max 13'-0" | S03.02 A1 | 0 |
| A1 continuous horizontal stud | +28.0 LF, 3-5/8" (8 racks 2442F x 3.5 ft) | A/S03.02 A1 | +28.0 LF |
| Diagonals | Spacing @24" on the walls above: +21 diagonals = +114.91 LF (W089 +1, W090 +4, W101 +4, W106 +4, W107 +4, W099 +1, W076 +1, W040 +2) | S01.01 N note, A/S03.01 | DIAG-BRACE 1306.85 -> 1411.15 LF (with the Task 2 rise change); DIAG-CLIP 234 -> 255 EA |
| Bridging clips | Recounted for the new studs (W099 22x2, I03 22x3) | R/S03.01 | 1006 -> 1031 EA |
| Garcy blocking, TRANS #5 W faces | +56.50 LF + 18.50 LF (4 rows each) | A02.01 OVERALL + A06.01 + B/A10.02 | +75.0 LF |

## Task 2: review of every open RFI

| RFI | Result | Quantity delta |
|---|---|---|
| RFI-02 | CLOSED. C/A12.01 (board 6" above the ACT) + M/A02.01 (studs 6"-12" above the ceiling) with STOCK at 12'-0" give a 12'-6" wall. W020, W067, W074 and W075 raised to 12.5 ft (stud and STOCK face); W001 STOCK run gets an extension line. | +17.0 LF stud on the 4 walls, +7.0 LF stud on W001; +17.31 SF Type X (incl. 9.09 SF on W001) and +9.22 SF 5/8 regular foil-back (W074); diagonals -10.61 LF (rise 0.5 ft shorter) |
| RFI-04 | CLOSED. A/A08.05 and A08.10 print 1/2" MR; A00.01 gives the storefront finish system to G/G. | 0 |
| RFI-05 | CLOSED. A15.04 092900 H.3 lists the 3 cores as equivalent and the wall is not rated, so regular foil-back is carried. | 0 |
| RFI-06 | CLOSED. S/S03.01 shows a continuous 3 5/8" 20 GA stud on hanger wire @24" O.C. | +85.62 LF 3-5/8" stud; +275.08 LF hanger wire |
| RFI-07 | CLOSED. On A03.01 the FR LOUNGE 9'-0" tag covers the alcove; it is one continuous ceiling. | 0 |
| RFI-08 | CLOSED. A00.02 door + A/A10.08 and H/A10.08 frame ±2" give R.O. 3'-4". | 0 |
| RFI-09 | CLOSED. A03.01 places E/A12.02 at this opening, so the head is 8'-0" (the corridor ceiling). | 0 |
| RFI-11 | Narrowed. D/A13.02 prints 8'-0" T.O. shelf, so the jack studs are now CONFIRMADO; only the shelf plan size stays open. | 0 |
| RFI-12 | REMOVED. It was an internal schema placeholder; the carrying_direction text was fixed. | 0 |
| RFI-14 | CLOSED. Corner bead per A15.04 092900, counted on the wall geometry: 88 outside corners. | +924.25 LF metal trim (corner bead) |
| RFI-16 | REMOVED. It was a method note (vector-derived lengths), not a question for anyone. | 0 |
| RFI-20 | CLOSED. The details (G/A10.01, A/A10.01, B/A10.02, K/A10.02, A/A10.02, B/A10.03) print 5/8" gyp bd. | 0 |
| RFI-21 | CLOSED. A05.01 key note 8 + E/A13.02 give WC-1 at 4'-0" (already carried). | 0 |
| RFI-22 | Narrowed to A03.01 general note 1 (access panels the landlord requires). | 0 |
| RFI-23 | CLOSED. D/A08.10 and J/A08.10 print 1/2" MR gyp bd under SF-91: 18'-1" x 4'-3 7/8". | +78.17 SF 1/2" (sheathing row) |
| RFI-24 | CLOSED. M/A10.08 draws new framing; the R.O. and head are derived from the frame ±2" and A/A10.08. | 0 |
| RFI-27 | CLOSED. The hanger stud is per S/S03.01; the steps come from the A03.01 ceiling heights. | +44.66 LF hanger wire |
| RFI-10, 13, 15, 17, 25, 26 | Still open. Nothing is printed for them. RFI-15 and RFI-17 texts were cleaned. | 0 |

Text clean-up: "~", internal rule codes and file names were removed from the sources, ops and labels that go to the Excel.

## Task 3: COBERTURA_17.md

All 17 items are resolved:
- **Cited (11):** the source now names the sheet. One of these also added a quantity: the 1/2" MR portal soffit, 78.17 SF (A08.10).
- **Added (2):** S/S03.01 suspended stud + hanger wire, and H/S03.01 framing clips, 24 EA.
- **Excluded (3):** K/S A08.10 slab fasteners, D/A12.01 graphic anchors, and M/A12.02 (not called).
- **Reviewed, no change (1):** P/A12.01.

## Changes by material (tool totals, rev1 -> REV2)

| Material | rev1 | REV2 | Delta |
|---|---|---|---|
| 3-5/8" stud (LF) | 13748.44 | 14854.78 | +1106.34 (walls +881.42, diagonals +104.30, A1 horizontal +28.0, suspended stud +85.62, W001 extension +7.0) |
| Hanger wire (LF) | 4256.39 | 4576.13 | +319.74 |
| 5/8" gyp Type X (SF) | 18093.85 | 18111.16 | +17.31 |
| 5/8" gyp regular (SF) | 545.60 | 554.82 | +9.22 |
| 1/2" sheathing row, MR (SF) | 424.00 | 502.17 | +78.17 |
| Clip angle (EA) | 1289 | 1359 | +70 (21 diagonal clips + 25 bridging clips + 24 H/S03.01 clips) |
| Metal stud blocking (LF) | 1507.10 | 1614.40 | +107.30 |
| Bracing C.R. channel (LF) | 1706.76 | 1739.06 | +32.30 (bridging channel recalculated by the tool) |
| Metal trim, corner bead (LF) | 305.11 | 1229.36 | +924.25 |
| Joint compound / tape | 1342.04 / 6896.60 | 1343.95 / 6906.41 | +1.91 / +9.81 |

## Open RFIs (final list)

- **RFI-10:** In-wall blocking with no printed length: restroom accessories, break-room cabinetry, coat rack, wall shelving runs.
- **RFI-11:** Water heater shelf plan size (N/S03.01 "2'-6" MAX / 4'-0" MAX SEE ARCH"). Maximum size is carried.
- **RFI-13:** (E) demising walls: quantity of Type X board to repair or replace (U465) is not printed.
- **RFI-15:** Framed duct penetrations where M02.01 ducts cross the partitions. No duct elevation is printed.
- **RFI-17:** Storefront head framing: beam spans, box post height, head-truss diagonal length and the 2 1/2" stud length are not dimensioned.
- **RFI-22:** Access panels the landlord requires under A03.01 general note 1; no quantity is printed.
- **RFI-25:** Blocking widths and rows for fitting room signage, locker banks and communication boards.
- **RFI-26:** Display window platform joist length and the edge members (F, K/S02.01) are not dimensioned.
