# Independent Final Audit Certificate - CFA #2284 River Point (Sheridan, CO)

Auditor: independent final auditor (step 11). Date: 2026-11-02.
Sources used: only the clean bid set `cfa_work/plano/bidset_CLEAN_SIN_MARKUPS.pdf` and the deliverables in `FINAL_FOR_REVIEW/`. No other take-off or reasoning files were opened.
Evidence crops: this folder (`proceso/*.png`). Each crop was rendered with pymupdf and reopened to confirm it.

**Overall result: NOT CERTIFIED.** 2 checks pass, 5 fail and 1 is pending. The quantities hold up arithmetically. The failures are format, labeling and citation problems, plus two small scope omissions. Details are in COMPARATIVA_AUDITORIA.md.

| # | Check | Result |
|---|---|---|
| 1 | Tag sweep | **PASS** |
| 2 | Blind re-measure | **FAIL (minor, 1 row)** |
| 3 | Detail chain | **FAIL** |
| 4 | Scope sweep | **FAIL (minor omissions)** |
| 5 | Arithmetic | **PASS (with traceability notes)** |
| 6 | Format | **FAIL** |
| 7 | Bluebeam markups | **FAIL** |
| 8 | Drive | **PENDING (checked after upload by the orchestrator)** |

---

## (1) Tag sweep - PASS
- A-202 (p13) has 24 partition tags on the plan, found from the text layer and circled in `chk1_tags_A202.png`: W6 x12, SW6 x4, W4 x1, W4.1 x2, W8 x2, M2.1 x1, M3.5 x2.
- Every tag maps to a row in the Excel:
  - W4 = PT0010; W4.1 = PT0011 and PT0012; W6 = PT0013 to PT0024; W8 = PT0025 and PT0026; SW6 = PT0006 to PT0009.
  - M2.1-01, M3.5-01 and M3.5-02 are on Partition Takeoff rows 6, 9 and 10.
- The untagged new infill at the removed Eliason door (A-050 KN1, heavy outline at y 617-677 pt, circled blue) is loaded as MB-01, with RFI-17.
- All 75 board-only rows (Partition Takeoff rows 25-99) give a location and a source.
- No new wall drawn on A-202 was found without an Excel row.

## (2) Blind re-measure (vectors and printed dimensions, 1/4" = 1'-0" = 18 pt/ft) - FAIL (minor, 1 row)

Metal walls (all within 2 %):

| Wall | Excel LF | Auditor LF | Δ |
|---|---|---|---|
| M2.1-01 | 14.167 | 14.167 (gray fill 1816.8-2071.8 pt; printed 14'-2") | 0 % |
| M3.5-01 | 7.15 | 7.140 (vector); 7.146 (printed 7'-1 3/4") | +0.1 % |
| M3.5-02 | 3.75 | 3.733 (vector); 3.771 (printed 3'-9 1/4") | +0.5 % / -0.6 % |
| MB-01 | 3.33 | 3.333 (heavy outline 617-677 pt) | 0 % |

Metal wall heights:
- M2.1 and M3.5 framing height is 10'-8". That is the kitchen ceiling (C.H. 10'-2", A-221) plus 6" per note C.1/A-202. Confirmed.
- Board height is 10'-6". That is 4" above the ceiling per G.4. Confirmed.
- MB-01 is loaded at 10'-6". By C.1 it would be 10'-8", a -1.6 % difference, which is within tolerance.

Board-only sample (13 rows; all within 2 % except one):

| Row | Excel LF | Auditor LF | Δ |
|---|---|---|---|
| W8-02W-DIN | 8.15 | 8.147 (vector) | 0 % |
| W8-02E-DT | 7.65 | 7.607 (vector) | +0.6 % |
| R-W6-11-N | 4.20 | 4.208 (printed 4'-2 1/2") | -0.2 % |
| W4-01W-SRV | 3.39 | 3.396 (printed 3'-4 3/4") | -0.2 % |
| W6-02N-SRV | 5.70 | 5.700 (fill) | 0 % |
| EX-DT-01 | 11.01 | 11.063 (printed 2'-4 1/4" + 7'-0" + 1'-8 1/2") | -0.5 % |
| W8-01S-OFF | 7.08 | 7.167 (printed 7'-2") | -1.2 % |
| W6-09-OFF | 14.68 | 14.52 (printed 3'-4" + 4'-0 1/4" + 7'-2") | +1.1 % |
| R-W6-12-W | 16.79 | 16.792 (printed 16'-9 1/2") | 0 % |
| W6-05W-MOP | 2.37 | 2.373 (vector); 2.417 (printed 2'-5") | -1.9 % vs printed |
| SS-GT-N/S/W/E | 4 / 4 / 8 / 8 | 4 / 4 / 8 / 8 (A-221 printed 2'-0"+2'-0", 4'-0"+4'-0") | 0 % |
| SS-SRV-W | 18.12 | 18.12 (vector, A-221) | 0 % |
| **W6-04-KIT** | **2.32** | **2.229 (printed 2'-2 3/4", A-202; `w604.png`)** | **+4.1 %, FAIL** |

The W6-04-KIT difference is 0.09 LF and 0.27 SF.

Board-only heights all match their notes:

| Height | Rows | Source |
|---|---|---|
| 5" | dining / vestibule base | A.3/A-621, H.2/A-202 |
| 1'-0" | BOH base | G.3/A-202 |
| 18" | kitchen base | A-050 KN16 (RFI-03 closed) |
| 1'-0" base + 9'-8" above | walk-ins | G.11/A-202 (6" above 10'-2") |
| 6'-8 1/2" | restroom tile top | A-611 |
| 9'-4" | restroom ceiling | A-221 / A-611 |
| 7'-8" | drive-thru furr-down | C1/A-603 |
| 10'-2" | mop chase | E3/A-604, 10'-2" ceiling |

Evidence: `chk2_M35_W8.png`, `w604.png`, `srv_soffit.png`.

## (3) Detail chain - FAIL

These citations open and confirm the row:
- A1/A-605: 2" metal Z channel and 1/2" cement board.
- A2/A-605: 8" metal stud wall.
- A-202 schedule: M2.1 and M3.5 have 1/2" sheathing on the exposed side.
- C4/A-624: 3-5/8" @ 16", 6" minimum above the ceiling, corner bead.
- C3/S-801: 362T125-54 strongback.
- A2/S-241: LGS 600S162-33 @ 16", mid-span.
- A.3/A-621: 5" cementitious board.
- A-050 KN16: 1/2" Dura Rock to 18".
- C1/A-603: 7'-8" B.O. furr-down.
- A-611: T/TILE 6'-8 1/2".
- E3/A-604: cement board on inside walls only.
- C09250 §2.1.B and §2.2.B (A-909).

These citations fail:
- **a. Wrong Z-channel size.** Material Summary row 8 reads "1-1/2" Z-furring channel". A-202 M2.1 and A1/A-605 print **2"** metal Z channel. Partition Takeoff F6 correctly says 2".
- **b. Bracing does not match its citations.** Material Summary row 13 loads 56.79 LF of 1-1/2" C.R. channel bracing on M2.1, M3.5 and MB-01. It cites A1/A-605, A2/A-605, C2/S-801 and C09111 3.2.C. None of these confirms it:
  - A1/A-605 and A2/A-605 show no bracing; the furring and the sistered studs sit on the existing framing.
  - C2/S-801 shows a "362S162-33 BRACE @ 48" O.C." diagonal kicker, not C.R. channel. See `s801_C2.png`.
  - C09111 3.2.C is "Seismic Bracing: sway-brace **suspension systems**", not wall bracing.
- **c. Wrong ceiling board type.** Row 15 says "5/8" gypsum board, regular". C09250 §2.1.E and §3.2.A.3 call for 5/8" **Ceiling Type (sag-resistant)** board on ceiling surfaces.
- **d. Malformed citations.** Material Summary I16 and I20 contain citations that are not real detail/sheet references: "3/CT-73B", "2/A-202", "1/A-202", "3/A-202", "7/A-202", "11/A-202", "4/A-601", "11/A-221", "4/A-211", "3/A-621". They look like note numbers with the letter prefix stripped.

## (4) Scope sweep - FAIL (minor omissions)

Present and justified:
- Blocking (metal at hoods and menu board; wood excluded).
- Backing.
- Soffits.
- 5/8" gyp ceilings (Entry A 46.36 SF and Entry B 67.92 SF, both re-measured against S-241).
- Ceiling bridging (RFI-09).
- Headers (none).
- Control joints (none printed).
- Corner bead at the soffits.
- Cement board.
- Level 5 (A-050 KN12).
- Demolition (19 elements).
- Exclusions: wood, fasteners, ACT, insulation, FRP, tile, stainless steel, plywood, paint, wallcovering, millwork, canopies, walk-in panels, MEP.

Omitted:
- **Soffit cross braces.** C4/A-624 prints "3-5/8" metal stud cross brace at 32" O.C." and C1/S-801 prints "362S162-33 @ 32" O.C." on both the parallel and perpendicular conditions. They are not loaded. See `c4_a624.png` and `s801_C1.png`. Roughly 14 pieces; their length depends on the RFI-15 hang height.
- **Menu-board wall kicker brace.** C2/S-801 prints a 362S162-33 kicker @ 48" O.C. with a height-based brace schedule. It was loaded as C.R. channel instead (see 3b).
- **Observations (RFI suggested, no quantity change proposed):**
  - A2/A-624 prints a "J" trim at the top of the play-area/dining cement board.
  - A-050 KN10 ("remove existing wall finishes") applies to the restrooms, where 617 SF of new cement board is loaded on existing walls. No removal of existing board is loaded there.

## (5) Arithmetic - PASS (with traceability notes)

Recomputed and matching:
- Every Partition Takeoff row gives board SF = LF x H x faces, except row 9 (see notes).
- Subtotal of the board-only rows: 950.94 LF and 2,896.28 SF.
- 1/2" cement board: 1,502.37 board-only + 298.16 on metal walls = **1,800.53 SF**, which equals the Material Summary.
- 5/8" gypsum ceilings: 332.06 SF. 6" joists: 304.49 LF. 3-5/8" studs: 165.84 LF. Ceiling/soffit track: 197.38 LF. Bracing: 107.66 LF.
- Demolition: 2,646.58 SF; DEMO-01 = 16.733 x 12.333 x 2 = 412.74.
- M2.1 Z channel: 9 x 10.667 = 96 LF. M3.5 studs: 7 x 10.667 and 4 x 10.667. MB-01 studs: 4 x 10.5.
- Bracing rows: ROUNDUP(10.667 x 12 / 48) - 1 = 2 rows.
- Joint compound: 0.072 x 1,915.72 = 137.93 lb. Tape: 0.37 x 1,915.72 = 708.82 LF.
- Level 5: 59.69 x 12.25 = 731.2 SF.
- Waste: 15 % on metal and 6 % on everything else, applied once.
- Purchase quantity = ROUNDUP(Net x (1 + waste) / stock) for every row. Examples:
  - 1/2" gyp: 1,678.68 SF / 48 = 35 sheets.
  - Cement board: 1,908.56 SF / 48 = 40 sheets.
  - 6" studs: 350.17 LF / 20 = 18 sticks.

Notes:
- Row 9 merges M3.5-01 (8") and MB-01 (3-5/8") into one row. Its Height column is a weighted 10.614 and its Layers column reads 1.32. As a result, LF x H x faces gives 111.22 SF against the 121.7 SF listed; the 121.7 SF is right when summed face by face.
- 1/2" gyp total of 1,583.66 SF: 1,483.64 SF can be traced to the Partition Takeoff. The other 100.02 SF (soffit bottoms) has no Partition Takeoff row, and the Material Summary I16 breakdown is cut off after 3 items ("...(Sco"). My geometric estimate of the soffit bottoms is 96-100 SF, which is consistent.
- The board SF values in the Partition Takeoff and the Net values in the Material Summary are typed values, not formulas linked to the Partition Takeoff.

## (6) Format - FAIL
- **The workbook has 7 sheets, not 6.** There is a hidden sheet `_reglas` with Spanish content ("reglas.py compuerta OK" plus hashes).
- **No subtotal row** for the "TYPE OTHER FRAMING (NOT A PARTITION)" block (rows 15-22).
- **Inconsistent RFI cross-references.** Partition Takeoff J33-J40 point the kitchen base height to "RFI-02", but Pending RFI-02 is about M3.5 stud spacing. The kitchen base question is RFI-03, closed in the Scope Checklist.
- **Review Items row 8 (item 6/8)** says "A 3-5/8"", but the take-off loads 8".
- These pass: schedule order (M2.1, M3.5, other, board only); per-type subtotals for the partitions; English in the 6 visible sheets; project data in Inputs rows 32-65; RFIs in A/B/C format with a delta for each option.

## (7) Bluebeam markups (pymupdf annotation audit of `CFA2284_RiverPoint_Markups_Bluebeam_rev1.pdf`) - FAIL

Correct:
- There are 106 take-off PolyLine markups plus 4 legend markups on an added page 173.
- One markup per item: 4 metal walls, 8 soffit sides (A-221), 75 board-only entries (A-202) and 19 demolition elements (A-050 / A-052). These counts match the Excel.
- Every markup has a Subject, a `/Measure` scale of "1/4 in = 1 ft" (C = 0.0556 ft/pt) and Contents. Vertex length matches the Contents LF within 0.011 ft.
- Every markup has `/Depth` equal to its height, except the 6 area-type ceiling demolitions (DEMO-C1 to C6), which have no height.

Failures:
- **Wrong Page Labels.** The demolition pages carry Page Labels "6" and "7" instead of **A-050** and **A-052**. Pages 13 and 15 are labeled correctly.
- **Spanish in the demolition Contents:** "(DERIVADO)", "(PENDIENTE)".
- **Metal-wall markup SF differs from the Excel board SF.** The markups use LF x framing height. M2.1: 151.1 vs 148.75. M3.5-01: 76.2 vs 75.03. M3.5-02: 40.0 vs 39.38.
- **MB-01 has Subject "M3.5"**, but it is an untagged 3-5/8" infill (RFI-17).
- **Observation:** the gyp ceilings (CLG x5, 332 SF), the soffit bottoms (about 100 SF), the Level 5 area, the roof-hatch shaft and the pin-and-sleeve recess have no markup.

Evidence: `chk7_markups_A202.png`.

## (8) Drive - PENDING (checked after upload by the orchestrator)
