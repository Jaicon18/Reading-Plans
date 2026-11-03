# Stage 3 - Resolution of readings A and B - Harbor Freight Tools, Loveland CO

Base: reading A (more complete for walls, openings, control joints, trim, FRP); reading B taken where it was more complete
(receiving enclosure CFS, restroom-block demo pieces, west-wall 209 furring, shelf family split). Every difference got ONE
directed look; crops (circled) in `etapas/3_revision/img/`. Output: `etapas/4_canon/takeoff_canon.json` (CANON OK),
`demo_geom.json`, `demo_cruce.md`.

## Decisions

| # | Difference | Decision | Source N/SHEET | Crop | Status |
|---|---|---|---|---|---|
| 1 | D-02 vs D-2+D-3; D-03 "only in A" | Same walls in both readings (D-02 18.62, D-03 5.70, D-04 5.70; D total A 239.12 = B 239.09): matcher artifact. Kept A. | A1.1 printed 18'-7 1/2" / 6'-1 1/2" | R01_A1.1_south_chain.png | CONFIRMED |
| 2 | A-01 11.54 vs B A-11 10.93 | A: printed 11'-6 1/2" governs | A1.1 dim chain | R01_A1.1_south_chain.png | CONFIRMED |
| 3-8 | RR/BR cluster on A4.0 (A-05..A-14 vs A-1..A-10, A-6a/b) | Same geometry, only corner ownership differs (cluster A 84.95 vs B 84.80 LF). Kept A segmentation: it carries the printed 20'-8", 4'-0" HOLD, 2'-0 1/2" | 1/A4.0 | R02_A4.0_RR_cluster.png | CONFIRMED (printed pieces) / DERIVED (rest) |
| 9 | B-03 9.44 vs B-2 8.83 | A kept (furring runs to the existing wall corner; B gives that 0.6 ft to A-6a) - no double count either way | 1/A4.0 | R02_A4.0_RR_cluster.png | DERIVED |
| 10-11 | E-02 13.54 / E-03 3.67 vs 14.41 / 4.70 | A: printed 13'-6 1/2" and +-3'-8" V.I.F. govern | A1.1 dim chain | R01_A1.1_south_chain.png | CONFIRMED |
| 12-15 | Receiving enclosure RE-1..3 (B only) | Carried (Div. 05 40 CFS = ours): 600S162-54 @ 16" (S2.1), 19'-10" / 19'-8" / 19'-10" (S2.1). Heights: RE-1 16.0 ft (B.O. deck 16'-0" @ LP, 1/A4.3), RE-2 / RE-3 16.42 ft (+-16'-5" HP, 1/A4.3; slope 1/4"/ft toward RE-1, S2.1) - B loaded 16.0 on all | S2.1, 1/A4.3, 4/A4.3 | R03_S2.1_receiving_encl.png, R05_A4.3_encl_section1.png | CONFIRMED (members, lengths, LP/HP) / RFI-03 (stud top vs box-beam bearing) |
| 16 | Enclosure headers (B: H-1 at both, RFI-05) | S2.1 roof plan ASSIGNS H-2 to the 6'-0" opening (RE-1) and H-1 to the 10'-0" opening (RE-3): H-2 = 4 pcs, H-1 = 5 pcs, (R.O.+1'-4") by tool = 29.3 + 56.7 LF. Jamb closure track 600T150-54 per jamb = 64.8 LF (RE-JAMB). B RFI-05 CLOSED | S2.1 header schedule + plan, S4.1 | R04_S2.1_header_boxbeam_sched.png, R03 | CONFIRMED (pieces) / DERIVED (opening widths from vector 5.94 / 9.93 ft) |
| 17 | BB-1 box beams | B kept: 4 lines x 19.667 x (2) 1200S162-54 + (2) 400T150-54 = 314.7 LF | S2.1 box beam schedule + roof plan | R03, R04 | CONFIRMED |
| 18 | Vestibule bulkhead: A walls VH (30.97 LF) vs B misc (31.6 LF track + 255.8 SF board) | ONE representation: A's VH walls (band measured). VH-02/03 length = A5.2 printed 8'-11" (B) not vector 8.59 (A). Stud 7.67 ft = vestibule B.O. deck +-18'-2" (A2.0) - 10'-0" storefront - 6" box header; sales face 8.17 ft; vestibule face 1.0 ft (6" above 10'-6" ACT). B's VB-* misc items dropped (no double count) | 1/A5.3, A5.2, A2.0 | R06_A5.3_vest_bulkhead.png | CONFIRMED (length) / DERIVED (heights) |
| 19 | Bulkhead kickers A 98.6 LF / B 78.0 LF | 13 kickers (ROUNDUP(L/4)+1 per run: 5+4+4) x 6.0 ft = 78.0 LF; length not printed -> RFI-04 | 1/A5.3 | R06 | PENDING (RFI-04) |
| 20 | Bulkhead box header A 123.88 / B 126.5 | (13.79 + 8.92 + 8.92) x 4 pcs = 126.52 LF | 2/A5.3 | R06 | CONFIRMED pcs / DERIVED LF |
| 21 | Bi-parting door box header: A 53.48 (R.O.+1'-4", header family) vs B 48.2 (storefront structural family) | 9/A5.3 attaches the header jamb-to-jamb with T162-54 track clips (no bearing): 12.042 x 4 = 48.17 LF in **header / box beam** + 2.17 LF T162-54 clips | 8/A5.3, 9/A5.3, D1.0 219 | R07_A5.3_box_header_attach.png | CONFIRMED |
| 22 | Interior door / window headers (A RFI-02, B RFI-08 "not called") | PRINTED: 2/A5.1 TYP. INTERIOR DOOR HEAD DETAIL and 5/A5.1 INTERIOR WINDOW HEAD DETAIL draw one track at the head ("STEELSTUD TO MATCH WALL CONSTRUCTION"): header metal, 1 piece, (R.O.+1'-4") by tool; window 306 with sill track. D08 (existing H.M. door in masonry) = existing lintel, not metal framing. Both RFIs CLOSED | 2/A5.1, 5/A5.1 | R08_A5.1_int_door_head.png | CONFIRMED |
| 23 | Wall A top track slip (B RFI-07) vs standard (A) | A/A4.1 prints "6" x 20 GA steel track" at existing deck -> standard track (A). B RFI-07 CLOSED | A/A4.1 | - (text, A4.1) | CONFIRMED |
| 24 | Demolition A 7,605.7 SF / 9 vs B 11,095.1 SF / 14 | Keynote by keynote + D1.0 dashed vectors: 14 elements, **11,412.0 SF** (see table below) | D1.0 207/208/209/211 + Demo Legend; A1.2 chart | R09, R10, R11, R12 | DERIVED (vector) / CONFIRMED (+-29'-7", +-6'-1") |
| 25 | Control joints A 282 LF (B none) | Carried: D-01 218 LF (D/A4.1 "CONTROL JOINTS @ 30' O.C. PER 9/A4.1") + E-01 64 LF (A4.1 note 6, 7/A4.1) | D/A4.1, 9/A4.1, 7/A4.1, A4.1 note 6 | - | CONFIRMED rule / DERIVED qty |
| 26 | Metal trim A 106 LF (B none) | Carried: A4.1 Wall Type Note 5 "ALL GYPSUM BOARD RETURNS SHALL HAVE METAL CORNER BEADS" | A4.1 note 5 | - | CONFIRMED rule / DERIVED qty |
| 27 | FRP 583 SF (A = B) | Kept FRP-01 530 + FRP-02 53 SF, familia "FRP" (tool family name; no "FRP panels" family exists). Note: "FRP carried per A1.3 finish schedule (G.C. scope)" | A1.3 WC-1, 1/A4.1, A4.0 701 | - | CONFIRMED |
| 28 | Mop shelf | B split kept (joists 6.1 LF 3-5/8" stud, track 5.2 LF ceiling track, MR 5.27 SF) | 1/A4.1, A2.0 514 | - | CONFIRMED |
| 29 | Type E hat channel | Kept in Z-furring family 1,393.75 LF (E-01 139.42 @16'-0", E-02 / E-03 to deck 18'-3") | E/A4.1 | - | CONFIRMED |

**TOOL LIMIT (for the calc stage):** there is no hat-channel family. Type E (E/A4.1 "1-1/2" METAL HAT CHANNEL @ 24" O.C.
MOUNTED VERTICALLY") is counted in the family "1-1/2" Z-furring" -> the **label must read 1-1/2" hat channel**; fix the
family label in the tool (also recorded as misc_info TOOL-LIMIT-HAT). Second limit: no "FRP panels" family - FRP is in
familia "FRP".

## Demolition (final)

| id | keynote | LF | H | layers | SF | from |
|---|---|---|---|---|---|---|
| DEMO-01 west bay partition | 207+211 | 78.62 | 15.79 | 2 | 2,482.8 | A (vector to west wall, R12) |
| DEMO-02 east block N-S | 207+211 | 31.60 | 16.75 | 2 | 1,058.6 | merged (4'-0" past lease line) |
| DEMO-03 east block E-W | 207+211 | 14.84 | 16.75 | 2 | 497.1 | A=B |
| DEMO-04 E-W with door 208 | 207/208 | 9.84 | 16.75 | 2 | 329.6 | A (B's run to 1816 not drawn) |
| DEMO-05 RR north | 207 | 23.35 | 16.75 | 2 | 782.2 | B |
| DEMO-06 RR south | 207 | 29.58 | 16.75 | 2 | 991.0 | printed +-29'-7" |
| DEMO-07 RR west | 207 | 23.64 | 16.75 | 2 | 791.9 | B (A's 36.30 not drawn past y 1175) |
| DEMO-08 RR interior | 207 | 16.04 | 16.75 | 2 | 537.3 | B |
| DEMO-09 riser west (rebuilt D-02) | 207/200 | 16.04 | 16.75 | 2 | 537.3 | A=B |
| DEMO-10..12 RR corridor walls | 207 | 4.68+9.42+6.36 | 16.75 | 2 | 156.8+315.6+213.1 | B |
| DEMO-13 south furring | 209 | 6.08 | 16.75 | 1 | 101.8 | printed +-6'-1" |
| DEMO-14 west furring | 209 | 156.24 | 16.75 | 1 | 2,617.0 | drawn dashed extent (R11) - closes B RFI-03 |
| **Total** | | | | | **11,412.0** | |

Existing lay-in ceiling (210): no ceiling type shown -> EXCLUDED 0 SF. Masonry (224, 218-220), tile, flooring, MEP: not ours.

## Final RFI list

| id | question | A option (delta) | B option (delta) | value loaded |
|---|---|---|---|---|
| RFI-01 | D-01 demising wall under sloped deck (+-16'-11" .. +-18'-3"): height basis per bay | per-bay B.O. deck callouts A2.0/A1.2 (approx -380 SF Type X, -140 LF 6" stud) | high point full length (0) | 18.17 ft full length |
| RFI-02 | Construction / layers of demolished partitions (207/209) not printed | 1 layer per face (0, loaded) | 2 layers per face if rated (+8,693 SF) | 1 layer per face; furring 1 face |
| RFI-03 | Receiving enclosure stud top vs BB-1 bearing / opening heads (14'-0" vs 10'-0") | studs to T.O. steel L.P. 16'-0" all walls (approx -13 LF) | HP / lower heads (0, loaded) | RE-1 16.0, RE-2/RE-3 16.42 ft; heads 10'-0" |
| RFI-04 | Vestibule bulkhead kicker length not printed (1/A5.3) | geometry 45 deg = 5.4 ft (-7.8 LF) | 6'-0" each (0, loaded) | 13 x 6.0 = 78.0 LF |

Closed (printed, applied with N/SHEET): A RFI-02 / B RFI-08 interior headers (2/A5.1, 5/A5.1); A RFI-04 receiving enclosure
scope (standing order + S2.1/S4.1); B RFI-03 west furring extent (D1.0 dashed extent); B RFI-05 enclosure header assignment
(S2.1 plan H-1/H-2); B RFI-07 slip vs standard track at A walls (A/A4.1); demo heights (standing order R-ALC-07).
Every RFI carries `fuentes_revisadas` = all 50 sheets + the stage-3 text sweep (incl. SHX annots) terms.

## Review items
See `review_items.json`: (1) RE opening widths DERIVED from S2.1 vector (5.94 / 9.93 ft), not printed; (2) DEMO-14 west
furring run all in Sales bay (east of DEMO-01) at 16'-9" - verify bay boundary; (3) D-01 per-bay heights (RFI-01) - A1.2
B.O. DECK / JOIST / BEAM spot values exist and could split D-01 into height zones; (4) tool warnings VH-02/03 drawn 8.59 vs
printed 8.92 (printed governs); (5) 8/A5.3 box header piece count (4 = 2 C + 2 track per tool rule #20) vs drawn section;
(6) tool family labels (hat channel, FRP).

## Totals (canon.py on the resolved canon)
Walls LF: D 239.12 - A 143.30 - B 32.04 - C 22.86 - E 156.63 (hat channel 1,393.75 LF) - VH 31.63 - RE 59.33.
Board: 5/8 Type X 8,689.6 SF - 5/8 regular 6,128.8 SF - 5/8 MR 809.8 SF (incl. shelf 5.3). Header / box beam 618.56 LF.
Demo 11,412.0 SF. FRP 583 SF. Control joint 282 LF. Metal trim 106 LF.
